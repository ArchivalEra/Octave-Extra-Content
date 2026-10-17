# Octave-Extra-Content

**额外内容仓**（extra content）：本仓管**非核心内容**的**档案事实**与**供给配方** ——
包、运行时、工具链的"从哪取、什么 sha、能不能用"。**不含字节**。

给 [Octave-Full-Wasm](https://github.com/ArchivalEra/Octave-Full-Wasm)（浏览器版 Octave，
**核心宿主**）的**按需拉取**供货。宿主是**消费适配器**，本仓是**生产适配器**，
两者之间的接缝定义在宿主仓 `build/113/NOTES-extra-content-seam.md`。**本仓不运行任何服务。**

> 本仓由 `Octave-Forge-Shelf` 升格而来（2026-10-14）。历史保留 ⇒ 原货架的 commit 仍可达
> （宿主 submodule pin `980e093` **不变**，只换了 URL）。

## 组织结构（用户点令 2026-10-14：去中间商）

```
   上游                    ┌────────────────────────────────┐
   gnu-octave ─┐           │  Octave-Full-Wasm（核心宿主）    │ ← UI 仓对它立**引擎契约**
   LLVM-wasm ──┤ 供货      │  引擎 / embed API / 四态 install │   （docs/embed-api.md）
   Pyodide ────┘           └───────────┬────────────────────┘
                                       │ 接缝：content-list（本仓产，宿主消费）
                           ┌───────────▼────────────────────┐
                           │  Octave-Extra-Content（本仓）    │ ← UI 仓对它立**内容契约**
                           │  档案事实 + 供给配方 + 端口      │   （端口 schema + 校验器）
                           └────────────────────────────────┘
```

**本仓负责**（**生产适配器**，接缝 §8.1）：包档案（`packages/`）、供给配方（`recipes/`）、
端口规范副本（`port/`）、**事实系统运维**（`zreflect/` + `build/` + `questions/`），
**「内容契约」面向 UI 的那条边**（**内容语义**：目录四态含义 / `content` 诚实 /
版本策略 / 许可台账），以及 **content-list 端口的推广 + 内容记录收口**
（把标准推给各生产者；各生产者的内容记录汇总到本仓 —— **收口 = 生产侧汇总，不是运行期端点**，
见下）。**本仓不负责**：运行站点、装配站点字节、运行服务、定义引擎接口 —— 那些是宿主的事
（字节同源由宿主装配：同源是 COEP 下的硬约束，跨域 fetch 实测被拦）。

> **平级铁律**（用户点令 2026-10-14）：**任何不作为引擎插件的仓库都与引擎同级** ⇒
> 本仓与 `LLVM-wasm` / `OpenModelica-Full-Wasm` / UI 仓**同级**；本仓推端口**不是派活**
> （唯一约束来自标准）。**端口产地仍是宿主** —— 推广 ≠ 产地方，本仓推的是宿主定稿的标准。

### 两条契约（接缝 §8.1；本仓各占哪一条）

| 契约 | 谁 ↔ 谁 | 本仓的角色 |
|---|---|---|
| **引擎契约** | 宿主 ↔ UI（embed API / 选档 / 四态 `install`） | **不碰**（引擎契约只能属于引擎） |
| **内容契约** | **本仓 ↔ UI**（**内容语义**：四态含义 / `content` 诚实 / 版本策略 / 许可台账） | **本仓接**（归属面，见下） |

> ⚠️ **端口产地 = 宿主**（2026-10-14 宿主裁决，回应本仓 `mail/003`）：接缝 §4 与 §8.1 曾
> 自相矛盾（§4 说产地 = 宿主，§8.1 把端口写进"内容契约"= 本仓）。**裁决 = 产地归宿主**
> （端口 = 应用核心的接受面；宿主已有 `check-forge-catalog.py` 的 R1–R4 判据范式；
> UI 读的是宿主站点的表）⇒ **schema + 校验器归宿主**，本仓**符合**它并共发布副本
> （`port/README.md`）。**内容语义**仍归本仓。裁决与依据见 `mail/004`、`questions/03-port-origin.md`。

> ⚠️ **归属 ≠ 投送**（同一裁决）：**归属**（谁定语义、负内容契约的责）= **本仓**；
> **投送**（UI 实际拿到什么）= **宿主** —— 站点里的表 + 宿主发布的面向 UI 的文档；
> **对话**（深语义问题）= 经 `mail/`（必要时宿主转达）。
> 运行期只有**一个同源端点 = 宿主站点**（COEP 拦跨域）；本仓是**归属面**的对话对象，
> **不是数据通道**（本仓 private、UI 仓 public ⇒ UI 侧无直接通道，这是可见性决定的）。

## 三层事实（各归谁核对）

| 层 | 载体 | 谁核对 |
|---|---|---|
| 内容**有哪些、哪个版本** | 本仓 git 历史 + 宿主的 submodule pin | 宿主 `witness-upstream-pin.py`（每提交） |
| **字节是不是那份** | 每个版本的 `sha256` | `tools/forge-shelf.py --verify`（每提交） |
| 能不能**真用** | 每版本的 `kinds` + 包级 `verified` | `--probe`（实测，非推断） |

## 布局

```
packages/<包名>.json      每包一个档案（多版本数组；加包只加文件）
tools/forge-shelf.py      取包 / 校验 / 探测 / 出目录（纯宿主侧，含 --selftest 41 条）
recipes/                  ★ 供给配方（非包内容）
  llvm-wasm.md            clang+lld wasm 工具链（URL+sha256+首拉预算；与 LLVM-wasm release 同源事实）
  pyodide.md              Pyodide + SymPy 运行时（符号计算的共享能力层）
port/                     ★ 端口规范副本（权威产地 = 宿主 build/extra-content/）
  README.md               端口是什么、谁产地、怎么自证
docs/                     ★ 经验集（来自姊妹仓的实测，接手先读这三份）
  FORK-PIPELINE.md        供给管线：三件套 + sha256 三关 fail-closed + pin 三形态 + 5 条实测坑
                          + 迁移/改名清点表（本仓 2026-10-14 那次迁徙的流程化）
  FACT-SYSTEM.md          事实系统：为什么档案仓需要它 + 接入六步 + 三纪律 + 5 坑
                          + 本仓第一批事实建议表（6 键，各带裸命令）
  LANES-AND-MEMORY-MODEL.md  内存架构与分支线：两档判据 + 三次混编事故原话
                          + 架构纯度闸门三判据 + 多档站点与择档 + 性能线封口清单
zreflect/                 ★ 事实系统机制层（vendored 自上游 Einfacht）+ 本仓数据层
  measure_extra_content.py  本仓数据层（**唯一自己写的那个文件**：量货架/工具/配方字节）
  check_*.py / facts.py / … 机制层（声明即闸门；执行面读 registry --run <相位>）
reflect-hooks/            git hooks（core.hooksPath 指这里）+ Einfacht.env 旋钮载体
gates-selftest.sh         闸门自证台（每个闸门先证明自己会红）
build/                    ★ 事实台账（FACTS.json）/ 翻案台账（retractions.json）/ 锁定源清单
questions/                ★ 悬案（未结案的问题，每条挂可跑的结算件）
mail/                     ★ 跨 agent 通信：其他 agent 写来的信 + 回信（只追加不删）
  README.md               命名规范 + 一封信必须有什么 + 回信纪律
  001-host-role-boundary.md  host 问职责边界（接缝 §8.1「内容契约 ↔ UI」与口头「不管 UI」冲突）
  002-host-r002-fixed.md     host 告知其 R-002 已修（附路径）
  003-re-role-boundary.md    本仓回信（A1 以仓库为准 / A2 接内容契约 / A3 确认 + 端口产地分歧）
  004-host-ruling.md         host 裁决端口产地 = 宿主 + 归属≠投送（回应 003 的分歧）
  005-host-port-landed.md    host 端口产地已落地 + 两件本仓侧小事（--emit 缺 producer 等）
  006-re-port-landed.md      本仓回信（A① --emit 加 producer 已做 / A② URL 两段式确认）
  007-port-gaps-to-host.md   本仓上报三个端口缺口请裁决（能力层 content 枚举 / consumer 轴 / pin 形态）
  008-host-port-rulings.md   host 三裁决（content 留空 / consumer 轴 / pin 前缀）+ 确认收口方窄定义
  009-re-rulings-synced.md   本仓回信（三裁决已同步 port/ + LLVM 已修 + 三个待确认）
  010-host-rulings-2.md      host 三答（license 自由串 / 能力层条数不限 / --upstream 并入 ok）+ 两附件 + deps 字面量
  011-re-rulings-2.md        本仓回信（三答已同步 + 本仓已出能力层边 + 请删宿主硬编码）
  012-host-re-hardcode.md    host 收到 011：同意删硬编码（前置 = bump 宿主 shelf pin）+ 一处语义分叉请裁决 + 悬空 dep 缺口
  013-host-mailboundary.md   host：投递落点纠正（host 补了收件箱，今后发 host 的信投 Octave-Full-Wasm/mail/）+ 回 012 待裁问题
  014-re-hardcode-and-hard-dep.md  本仓回信（裁硬依赖 / R9 部分闭合 / 投递落点已改）—— ★ 按新投递规则**只投 host 仓**（不再留本仓）；信在 `Octave-Full-Wasm/mail/014`
  015-host-deps-hardcode.md  host：014 三件已落（两行凭据）+ 投递协议纠正（投递≠提交）+ 更正空头 CI 声明
  016-host-market-design.md host：市场架构判决（design-it-twice）+ 你仓一处**逐版本声明漂移**（N5，附复跑）+ 请出 `versions` 轴 + `ways` 不属记录请确认
  017-host-arch-axis-and-consensus.md host 补告知（漏寄两封）：端口 schema 加了 arch（楚河汉界三档）⇒ 请同步 port/README.md 副本 + 角色共识走信 + 三属性信息性告知（可命名）
  018-re-n5-and-versions.md    本仓回信（N5 已修 52/52 + versions 裁「出+只出已 stage」+ 三属性现名确认）—— ★ 投进 host 仓
  019-host-versions-landed.md   host：018 七件复核全过 + versions[] 已进 schema（三不变量，自证 41/0）+ N6 修复上站（工单 68 结案）
  020-re-versions-landed.md    本仓回信（--probe 逐版探 + --emit 出 versions[] 落地，附样件）—— ★ 投进 host 仓
  021-host-three-layer-verdict.md host：三层对账全过 + 抓出我一处缺口（货架路径不产候选集，已修）+ staged 语义确认
  022-re-optim-query-gap.md    本仓回信（optim query-URL 今天就成立 + withheld 保留 upstream_url + 四类形状观察）—— ★ 投进 host 仓
  023-host-ruling-a-and-two-defects.md host：判 (a) + 两件已落 + ★ 端到端又抓两处宿主真缺陷（假目录树 / 上游缺同源改写）
  024-ui-re-content-contract.md   ui 回信（接纳内容契约：CONTEXT §五 + A1/A2/A3 逐题答；双投副本，编号接本仓序号）
  025-ui-re-market-spec.md      ui 回信（PackageManagerPlugin 落地：规范全遵守 + 闭包口径精化 + 209/209 全绿）
  026-llvm-re-ztii.md           llvm 抄送（工单 65 缺口 2 已答宿主：归属 = 宿主 ABI 决策；悬案 03 结案）

> ★ **投递规则**（2026-10-15/16 立，四仓同款）：**投递落点 = 收信方的 `mail/`**；
> **投递 ≠ 提交**（落文件 = 发信方；提交/推送 = 收信方 —— 那是它的仓、它的闸门）；
> **只读自己箱子**（例外极窄：`To:` 指名本仓的信若因本仓 private 落在对方仓，读它算收信）。
> 写给宿主的信投 `Octave-Full-Wasm/mail/`（本仓不留投递副本，上方标注 ★ 的那些即此类）。

> **推广面**（本仓对外，四仓同级 —— 用户点令：任何不作为引擎插件的仓库都与引擎同级）：
> ① `LLVM-wasm`（工具链表已并入宿主 `ok`）；② `OpenModelica-Full-Wasm`（缺席合法，
> 判据 = 发运模型集出现 `import Modelica.` 时出表）；③ **`Octave-UI`**（2026-10-16 建箱 +
> 首封推广**内容契约**：四态 / `content` 诚实 / `consumer` / `versions` 语义 + 「归属 ≠ 投送」）。

> **角色共识再确认（2026-10-16，用户原话）**：「内容仓负责推广标准，然后作为 OCTAVE 核心的
> 我们做好适配」—— 非**新判决**，是对既有分工的**再确认**（推广 ≠ 产地方：标准由宿主定稿，
> 本仓推它、收口内容记录；宿主做消费适配）。已落 `STATE.md` 的活状态。
STATE.md / AGENTS.md      活状态文档 + agent 硬规矩（机器块由 facts.py 渲染，不手改）
```

> **接手先读**（按顺序）：① 本 README（角色与边界）→ ② `docs/FORK-PIPELINE.md`（供给纪律）
> → ③ `AGENTS.md`（本仓硬规矩 + 复跑命令）→ ④ `STATE.md`（活状态：现在是什么，数字引用台账键）
> → ⑤ `docs/FACT-SYSTEM.md`（事实系统为什么这样接）→ ⑥ `docs/LANES-AND-MEMORY-MODEL.md`
> （内容有"档"属性，决定档案怎么标）。
> 与宿主的对话面 = 宿主仓 `build/113/NOTES-extra-content-seam.md`（接缝）与其 §8（组织判决）。

## 包档案形状

```json
{ "schema": 1, "name": "quaternion",
  "depends": [],                                  // 包间依赖（闭包由客户端解析）
  "upstream": { "index": "gnu-octave/packages", "description": "…", "links": {…} },
  "verified": { "octave": "11.3.0", "how": "detect_kinds（tar 内容判 m/oct）", "tarball_sha": "…" },
  "versions": [ { "version": "2.4.2", "url": "https://…", "sha256": "…", "size": 47838,
                  "requires": ["octave (>= 4.0.0)"], "date": "…",
                  "kinds": ["m"], "in_index": true } ] }
```

`kinds` **三态**（后果完全不同，实测精化）：
`m` = 纯 `.m`（开箱可用）· `src` = 带 `src/` 源码但**没有**现成 `.oct`（`.m` 照样可用，
只是缺加速件）· `oct` = 随包带预编译 `.oct`（异架构，wasm 里必须重编）。

⚠️ **`kinds` 有一个已知会说谎的角落**（实测，2026-10-14）：`symbolic` 探出 `['m']`
（与真·开箱即用的 `cgi` 判得一模一样），但它的 `DESCRIPTION` 明写
`SystemRequirements: python, sympy (>= 1.5.1), mpmath (>= 1.0)` —— 本构建没有 Python
运行时 ⇒ **装上跑不动**。⇒ 这类包的**能力层需求 = `depends` 边**指向能力层条目
（`symbolic` → `pyodide`，配方见 `recipes/pyodide.md`）。
规模实测：144 个上游包里只有 **2 个**（`symbolic`、`pythonic`）。

> 该表示法**已落地并结案**（悬案 `questions/02` resolved；接缝 §2 判决：能力层 =
> `form:"tree"` 的普通条目 + 依赖边，**不引入新字段**）。本文曾把它错引成「接缝 §2 的
> `needs` 轴」——**已翻案，见 R-002**。能力层依赖是**硬依赖**（站点没供能力层 ⇒ `install`
> 响亮失败，2026-10-15 裁决，见 `mail/014`）。

★ **逐版真探**（2026-10-16，修 N5）：`kinds` 与 `size` **全部 52 条版本记录都从真字节探出**
（先逐条核 sha256 再 `detect_kinds`，fail-closed）—— 不再有"未经探包的作者主张"。
曾有的 1 条矛盾（`statistics-1.7.3` 声明 `['m','oct']` 而字节里 0 个 `.oct`，系上游索引手抄）
与 38 条空 `kinds`（`verified` 条目级、只覆盖选中版的根因）已全修。
`--probe` 已改**逐版探**（防再犯：探档案里全部版本，缺字节明说跳过、sha 不符拒探）。

★ **`versions[]` 版本候选集**（2026-10-16，用户点令「每版各带是否兼容」）：`--emit` 现在出
候选数组（条目内嵌不摊平），每条带 `stage`（`staged` 必带派生轴 / `withheld` 不许带 ——
**派生不出不许编**）；顶层标量与选中候选**同源**（防两处漂移）。
**全链已闭环**（五段：宿主 schema 三不变量 → 本仓 `--emit` → 宿主 `resolve()` → catalog →
浏览器；宿主三层对账全过）。**向后兼容有实测**：旧客户端只读顶层标量 ⇒ 8761 上
`accept-symbolic-seam` 9/0 不变。轴语义与三条不变量见 `port/README.md`。

## 用法

```bash
python3 tools/forge-shelf.py --list
python3 tools/forge-shelf.py --fetch quaternion --cache /path/to/cache
python3 tools/forge-shelf.py --probe quaternion --cache /path/to/cache
python3 tools/forge-shelf.py --verify --cache /path/to/cache
python3 tools/forge-shelf.py --emit out.json --octave 11.3.0
python3 tools/forge-shelf.py --add <包名>            # 从上游索引加新包档案
python3 tools/forge-shelf.py --selftest              # 41 条（三类用例齐备）
```

## 纪律

- **只上验证过的**：`verified: null` 的条目 `--emit` 默认跳过（`--allow-unverified` 才带）。
- **fail-closed**：sha256 不符 ⇒ 拒绝（`--fetch` / `--verify` 都查）。
- **零值守卫**：空货架 / 空缓存 / 空改动集 ⇒ 全部报错，不当"通过"。
- **每个子命令都有判据**，`--selftest` 三档齐备（正常不报 / 该报的必须报 / 空输入必须报）。
- **诚实优先于好看**：探到什么写什么 —— 上面那个 `['m']` 的谎就是这条纪律发现的。

## 边界（不做什么）

- **不托管站点 / 不装配字节 / 不运行服务**（纯客户端铁律；字节同源由宿主装配）。
- **不定义引擎接口**（引擎契约只能属于引擎 —— 见接缝 §8.1）。
- **不改宿主仓**（路径铁律）；宿主的消费面由宿主维护。

## 许可

本仓只含**元数据与配方**（上游公开事实 + sha256 + URL）。包本身的许可见各自 `COPYING`；
取包不改变上游许可。工具链 / 运行时的许可逐条记在 `recipes/*.md`。本仓自身 AGPL-3.0-or-later。
