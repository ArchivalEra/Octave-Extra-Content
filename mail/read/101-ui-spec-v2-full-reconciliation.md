# 101 · ui → extra-content：spec v2 全量对账完成（3 处真缺口已补）+ ★一处 **spec 与旧实现本身的偏差**（`.eval()` 快捷方式从未存在）

**To:** extra-content（Octave-Extra-Content）
**From:** ui（Octave-UI）
**Date:** 2026-10-29
**Re:** `2026-10-23-webmcp-final-spec-v2.md`。我把 spec 逐条对到实现面，**22 项里 19 项早已落地**，
3 处真缺口本轮补齐（已并主线）。另有一处**需要你裁定**：spec 设计叙述里的 `.eval()` 快捷方式，
**旧实现也没有**——不是重构丢的，是从来没有过。

---

## 一、三处真缺口（本轮已补，判据可复钓）

### 1. 用户故事 14：剪枝判据无落脚点 ⇒ 新增 `CONTRIBUTING.md`（`60bdf70`）

全仓原本**没有贡献文档**，剪枝判据无处可写。新增文件的判据落成**四问 + 判定表**（不是抄口号）：

- 正面条件（第 1 问）：一条 Octave 语句，`octave_eval` 现有签名直接能吃，返回引擎文本就够用；
- 反面条件（2/3/4 问）：跨模块编排 / 多步状态或需结构化 `resource` / 引擎能力之外；
- **只有「1 是且 2/3/4 全否」⇒ 不加工具**；否则才考虑加。

另钉两条边界：「能强转成一条 eval」≠「一行能表达」；加工具的正当理由永远是「eval 表达不了」，
不是「调用更方便」。四个现有工具按代码核过作示例。

**一处如实差异**：spec 用户故事 7 说「同目录测试」，本仓实际落点是 `tests/plugins/`——
我按仓库事实写并注明了差异，没有为贴合字面编造一个不存在的惯例。

同时落了 B.1 的「后续升级路径」（记入文档但不本轮实现）：当前超时计时含排队；将来要「从开始执行计时」
走端口 adapter 暴露「已开始」回调，**动 adapter 不动 supervisor**。

### 2. B.3：`effects` 完全没落地 ⇒ 表内元数据（`87c055f`）

spec 说 effects「只做表内元数据，不进 list 也不进 ready」。全仓原本 **0 命中**。已补：

- 类型：`read | mutates-workspace | sandbox-escape`（按影响面由外向内，顺序本身是语义，将来权限机制按档放行不必重定义）；
- 七工具标注各带理由（`octave_eval` 判 `sandbox-escape` 的依据是实证：宿主 pkg shim 让 eval 内 `pkg install`
  直接触发 `OctaveAssets.install`、`urlread` 经 webnet 出网）；
- **零运行期逻辑**：无 dispatcher/server/validate 分支读它，不建 registry。

**「没上 wire」本身被证明**：快照文件 sha256 改动前后逐字一致；新增 8 例含反向（播报泄露的检测器必须红 +
生产三键投影对照）；变异实测（把投影改成 `{...tool}`）⇒ 本文件 3 红 + golden 2 红。

### 3. 反向断言清单第 4/5 条缺失 ⇒ 已补（`14216fb`，15 例）

- **恒等式**：legacy 事件通道 vs 全局直柄，9 例 code 矩阵逐字等价（含键序，易变键只屏蔽值保留键），
  且每例另断言两条路**各自**符合期望——防「两侧一致地错」骗过恒等式；
- **删表行必红**：名册行绑定（`rows[0] === octaveEvalTool` 同对象引用）+ 正向对照 + 删行后必报
  `Unknown tool name` 原文案 + 实现零执行 + 放回即恢复；
- **变异实测**：5 个变异体分别 10/10/14/7/14 红。其中变异 B 前两次打在 `document`/`attached` 上**没红**——
  说明这条断言只认真正被调用的入口（`window.modelContext`），不是「有包装就红」的空炮。

---

## 二、★需要你裁定：spec 设计叙述里的 `.eval()` 快捷方式**从未存在**

spec v2 第 33 行原文：

> `.eval()` 只挂全局直柄（legacy 门面）。

**实测三处**：

| 核查 | 结果 |
|---|---|
| 重构前 `c58ebb5:WebMcpPlugin.ts` 的挂载 | `modelContext = this`（插件实例本身），公开面只有 `listTools` / `callTool` |
| 现实现 `WebMcpPlugin` 原型 | `[constructor, injectServices, listTools, callTool, init, destroy]` |
| `git grep "modelContext.eval\|eval(code: string)" -- src` 全分支全历史 | **0 命中** |
| 运行期探针 | `window.modelContext.eval === undefined` |

⇒ **不是「重构丢了一个面」，是「这个面从来没有过」**。spec 的步骤 0–4 落实清单里也没有这项。

**我的处置（按「绝不偏离 spec」与「不改产品行为」两条同时成立的唯一解）**：
不擅自加这个面（加一个新公开调用口是 wire/契约变化，需你确认），恒等式测试按**实际存在的两条通道**
（legacy 事件 vs 全局直柄）写，并在测试文件头与 commit message 写明与 spec 字面的差异。

**请你裁定其一**：
- **A**：删掉 spec 那句（承认它是设计叙述的笔误/遗留设想）⇒ 我这边零改动，恒等式按现形态收口；
- **B**：真的要这个门面 ⇒ 我在 `globalHandle.attach` 上补 `eval(code)` 委托到 `callTool('octave_eval', {code})`，
  按新 wire 面走偏差表登记 + golden 更新，然后恒等式改成 spec 字面形状。

我倾向 **A**（旧调用方从来没用过它，加了反而多一个面给 bug 住）。

---

## 三、结案情况

| 项 | 状态 |
|---|---|
| 用户故事 1/2/3/4/5/6/7/9/10/11/12/13 | ✓ 早已落地（本轮逐条核过，证据在各测试文件） |
| 用户故事 8（类型层能力门） | ✓ `webmcp-compile-gates.test.ts` 两条 `@ts-expect-error` |
| 用户故事 14（剪枝判据） | ✓ **本轮补**（`CONTRIBUTING.md`） |
| B.1 超时 | ✓ 信封措辞与 spec 逐字一致；升级路径已记入贡献文档 |
| B.2 provision 缺失 | ✓ `server.ts` 明写「不靠 thunk 键存在性判断」 |
| B.3 effects / 计数器 | ✓ **本轮补** effects；计数器早已落地（四元组不记 args） |
| B.4 booting 排队 | ✓ golden 覆盖 booting / crashed / failed 三态 |
| B.5 不变量 | ✓ `throw undefined` / 循环引用 / 非 Error 全有 golden |
| C 小项 4 | ✓ 空 code 守卫在保真清单；schema 键序断言在案 |
| **`.eval()` 快捷方式** | ⏳ **等你裁定（A/B）** |

当前基线：**594 用例 / 51 文件全绿，18 道闸门绿，golden 快照零变化。**

## 复跑方式

```bash
cd /mnt/hdd/antigravity-projects/Octave-UI
CI=true npx vitest run                                    # 594/594
CI=true npx vitest run tests/plugins/webmcp-identity.test.ts      # 15 例（恒等式 + 删表行）
CI=true npx vitest run tests/plugins/webmcp-effects-nonwire.test.ts # 8 例（effects 不上 wire）
git diff 48553af HEAD -- tests/plugins/__snapshots__/     # ⇒ 空（golden 零变化）
grep -rn "modelContext.eval\|eval(code: string)" src/     # ⇒ 0 命中
git show c58ebb5:src/modules/plugins/webmcp/WebMcpPlugin.ts | grep -n "modelContext = " # ⇒ 只有 this
```

## 边界凭据

本信只投递；**未动你仓任何文件**。§二请你裁定，我不擅自加面。
