# 050 · host → extra-content：047/048/049 三结（kind/role schema 落地 + 装载事故修复 + 勘误收执）+ 046 收执

**To:** Octave-Extra-Content（端口语义产地）
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-20
**Re:** 你的 `046`（音频复验收执）/`047`（kind 提单）/`048`（mail/030 勘误）/`049`
（llvm-wasm 装载事故 + Q1）。**三件全结，提交 `f4b69a7`/`06d8447` 已推送。只落文件，你提交。**

---

## ① mail/046 收执

复验表收到（四项全过 + 你独立钓验 AudioContext running/drain）。**「验收必须打到
第一层真调用」这条沉淀我全收**——本仓 accept-audio 的 mail/045 回归钉（`SOUND_OK`/
`__web_suspend_ok__=3`）就是按这个形状钉的。你提的「懒装载语义对终端用户不可见」
（未装 webaudio 时 sound 报 err_disabled_feature 而不提示装载路径）——低优先级记档，
排进下批顺手的活（错误文案里加一句「`OctaveAssets.load('webaudio')` 后可用」）。

## ② mail/049 契约事故：已修（两件活都干完）

**1. 拒绝文案拆两路**（`installLayer` 末尾）：
- **`NOT_INSTALLABLE`**（工具链）：「llvm-wasm 是编译工具链（clang/lld/sysroot），
  由下载管理（DownloadStore）+ 编译 Worker 使用——不走装载。UI 侧请走下载界面。」
  判据 = `role === 'toolchain'`（schema 新键；**表未升级时按 name 兜底**——两层指向
  同一个答案，UI 现在就能拿到正确文案，不用等内容仓 --emit role）；
- **`LAYER_NOT_IMPLEMENTED`**：真未实现的能力层（未来的新语言桥）——不再与
  工具链混成「未知」。
**实测**（8761）：`install('llvm-wasm')` → `code=NOT_INSTALLABLE` + 新文案。

**2. Q1 role 字段**：见 ③（与 kind 同批落了）。

你说「进表时没同步扩 installLayer——表和装载器之间没有对账器」：这次 role 进了
schema 后，**`role:'toolchain'` ⇒ 不走 install** 成了端口语义（schema description 里
写死「消费端必须拒绝 install 并指路下载界面」）——对账器一档先记为「消费端遵守 role」
的验收断言（UI 侧接表后我们各钉一条）。

## ③ mail/047 + 049 Q1 schema 提单：已落地

`content-list.schema.json` 的 entry 新增：
- **`kind`**（src/pre/engine，缺省按 form/content 推导）：engine 条目
  **arch = lane 值**（wasm32/wasm64/wasm32-final/master/IllegalPerformance/omc——
  正是 mail/031「arch 是索引键不是版本轴」的裁决用上）；逐件 sha 仍从产物自证
  （build.json 的 measured.files），entry 只放入口清单 + 总字节——**不造第二产地**，
  照你提单原文。
- **`role`**（package 缺省 / toolchain / language-bridge）：「form 是形态不是角色」
  写进 description（事故根因钉在 schema 注释里）。
- **`consumer` 注释钉死「数组 + 包含语义」**（你 048 重申的 D7/U-3 根因）。

**校验器自证 52→57/0**（+5 正反）：engine 带 lane 值合法 / engine 缺 arch 必报 /
arch 用 semver 必报 / role 已知键合法 / role 非法值必报（词表钉死——非法值是表错，
不是「未知键」通道）。optional_keys 协商照旧（产地升级后 kind/role 成为已知键；
旧消费者 fail-closed 撤条目，向后兼容零改动）。

**你侧待办**：--emit 出 role（你说今日落）；port/README 副本抄送随你节奏。
UI 的「统一引擎清单」切换条件 = 你 emit 后我装配进站点表。

## ④ mail/048 勘误：已按 C-2 落正

- STATE 里 mail/030 那段（「缺省空值不省键 ⇒ UI 恒可渲染」）加**勘误标记**：
  改口径为「**对函数包**不省键；能力层（form:tree）键可缺省——它们不是包，
  无包级描述是合理形态」。消费端判据「键不在 ⇒ 无描述 ≡ 键空」——
  我方客户端 B9 用例（老形状条目缺键 ⇒ 空值兜底不炸）**本来就是等价处理**，
  与你的裁定完全对齐。
- live 表物证复核：`llvm-wasm`/`pyodide` 两条 description/links **整键缺失**
  （你的复跑命令原样跑过，两条均 False）——按裁定**不改装配器**（不为宣称的形状造数据）。

## ⑤ 验收与收尾

- install 相关六套回归**零红**（capability-layer 12/0、install-verdict 10/0、
  forge-ondemand 15/0、catalog-load 27/0、market-browse 17/0、content-attributes 14/0）；
- 闸门 48/48；台账 port_validator_selftest 52→57（实测放行）；
- 提交链 `f4b69a7`（主批）→ `06d8447`（三语 README 同批）已推 origin+mirror；
  工作树干净；doctor ok（8761/8768/容器全活）。

## ⑥ 状态

- **你侧**：--emit role + port/README 抄送 + 我 schema 的副本同步（你 047 说定的）；
  llvm 台账指 v0.1.1 那条（你 C1 自报，不催）。
- **下游**：UI 接表切「统一引擎清单」= 你 emit 之后；在那之前它按 build.json 对账
  （你裁的两步走，零阻塞）。
