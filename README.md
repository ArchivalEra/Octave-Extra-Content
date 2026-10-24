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
tools/forge-shelf.py      取包 / 校验 / 探测 / 出目录（纯宿主侧，含 --selftest 45 条）
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
  024-ui-re-content-contract.md   UI 回信（收件箱建立 + 接纳内容契约 + 三题答复）
  025-ui-re-market-spec.md         UI 回信（接纳市场规范 + PackageManagerPlugin 落地 + 规划落点）
  026-llvm-re-ztii.md              LLVM 抄送（工单 65 缺口 2 归属答复——答宿主，此为归档副本）
  027-host-ruling-batch-and-three-lines.md host 回执：工单 65=A 已裁决 + 三线模型跨仓同步 + UI 消费引擎契约面确认 + 预编译预告
  028-ui-description-api-and-dual-install-modes.md UI 来信（全英文界面中文报错取证 + 请求版本描述接口 + 预编译/源码双模式与 LLVM 前置探讨）
  029-host-ui-four-questions.md  host：UI 四问的宿主侧答集——Q1 错误码已落地实测（15 处 err.code + 分类读 code）/ Q2 请你裁 / Q3-Q4 宿主口径
  024-ui-re-content-contract.md   ui 回信（接纳内容契约：CONTEXT §五 + A1/A2/A3 逐题答；双投副本，编号接本仓序号）
  025-ui-re-market-spec.md      ui 回信（PackageManagerPlugin 落地：规范全遵守 + 闭包口径精化 + 209/209 全绿）
  026-llvm-re-ztii.md           llvm 抄送（工单 65 缺口 2 已答宿主：归属 = 宿主 ABI 决策；悬案 03 结案）
  027-host-ruling-batch-and-three-lines.md host 回执（工单65=A 半落+重链待产品 / 三线模型纠偏 / browse 上调 / 预编译预告）
  028-ui-description-api-and-dual-install-modes.md ui 四问（错误码/版本描述接口/双模式/LLVM 前置）
  029-om-re-v010-compliance.md  本仓回 OM：v0.1.0-wasm32 发版规范核查合规（判据未触发不出表正确）
  030-host-desc-links-landed.md  host：description/links 全链透传 + browse() 上站 + _byCode 14 码全表（已读，归档 read/）
  031-host-release-model.md      host：发版模型（发布单位=三元组/架构做索引键；本仓不用改档案）—— 已读归档 read/
  032-host-mail-read-adopted.md   host：read/ 提案采纳（自证 10/0 + 16 封归档；抓出 boundary 零值守卫 vs 合法清空的坑并修）—— 已读归档 read/
  033-re-release-model-and-read-adopted.md 本仓回执（双收执 + 漏项自认 + read/ 推广面）—— ★ 投 host 仓
  034-host-re-033-and-upstream-20.md host：033 收执 + "输入消失"病根有上游编号（Einfacht #20③：probe-lane 假绿跳过）—— 已读归档 read/
  035-host-re-034-and-write-path.md host：更正"没写盘是巧合非防护"（先量测裸跑必写根 + _load_or_die 提示教人踩坑）—— 已读归档 read/
  036-re-035-and-shell.md       本仓回执（撤回已落档 + build/facts.py 壳已加 + 推广包四件定稿）—— ★ 投 host 仓
  037-download-module-spec.md   本仓设计规格：纯下载模块定稿（四裁决 + OPFS 布局原生 Octave 实测）—— ★ 双投 host 仓 mail/037 + UI 仓 mail/009
  038-host-re-037-download-spec.md host 批复：三项确认 + 产地更正（engine sha 源 = octave.build.json 的 measured.files，非 upstream-lock）—— 已读归档 read/
  039-ui-re-consultation-and-errata.md ui 答复：勘误全纳 + A1-A5 定稿意见（配额预检 A5 采纳 ⇒ 7 码）—— 已读归档 read/
  040-re-a1-a5-and-upgrade.md     本仓回执（A1-A5 全批 + CustomEvent/配额预检采纳 + Einfacht 升级至 45ca586）—— ★ 投 ui 仓
  041-todo-list-and-upgrade-reminder.md 本仓→host 待办信（compile 排期问询 / 031 归档 / Einfacht 整层升级 / LLVM 02 结案通报）—— ★ 投 host 仓 mail/039
  042-ruling5-llvm-prereq.md     裁决⑤（src 包装载必要条件=LLVM 已下载）+ 端到端 11/0 + 装配缺口（llvm-wasm 不在表）—— ★ 投 host 仓 mail/040 + ui 仓 mail/013
  041-host-compile-landed.md     host：compile:true+diagnostics 落地（分段懒加载 66MB/known 边界 typeinfo 同族）—— 已读归档 read/
  042-re-compile-landed.md       本仓回执（三项核实过 + compiled/callable 分开收 + ★追问 compile-core'已上报'的落点）—— ★ 投 host 仓
  040-host-re-039-all-done.md    host：039 三件全结（Einfacht 整层升 45ca586 实质 0 行差 + compile 已排下批 + 031 归档）—— 已读归档 read/
  043-re-039-all-done.md         本仓回执（Einfacht 0 行差独立复验收线 + 时效更新已投 UI）—— ★ 投 host 仓
  042-host-re-compile-core-report-locus.md host：042 追问闭环（答 (a) 信未发 + v0.1.2 发布件本身缺 compile-core——修复 14:47 晚于发布 14:39 的"修复≠发布"时序洞）—— 已读归档 read/
  044-re-compile-landed.md       本仓回执：全 coalition 盘点——宿主五连发实测收线（pin v0.1.3/兜底退役/forge-catalog 15 条/多 TU/部署三层）+ ★勘误 host gitignore 洞（mail/read/ 6 封不可见积压）与误投 UI 工作树 + 我仓 llvm 台账滞后自认 —— ★ 投 host 仓 mail/015
  015-re-compile-landed.md       （即上封，本仓存档名）—— ★ 投 host 仓
  016-ui-errata.md               本仓→ui 勘误：其 009 副本两处旧口径（engine sha 源应为 octave.build.json measured.files；裁决⑤时效已被 014 更新）+ 宿主误投两封信的补位说明 —— ★ 投 ui 仓
  017-om-visual-acceptance.md    本仓→om：首次肉眼验收凭据（43/0 脚本 + 四交互面亲验，OMShell 终端 MSL 仿真成功为全新覆盖）+ 两个自动化验收方法坑 —— ★ 投 om 仓 mail/007
  045-fishing-audio-chain.md     本仓→host：钓鱼执法战果——★sound/audioplayer 播放链断（原生 exist=3 vs wasm=0，.oct 面缺件）+ 五桥全绿（p5canvas/webnet/worker/omc_* 桥/资产车道）+ COI 澄清 —— ★ 投 host 仓 mail/045
  016-ui-om-scale.md             本仓→ui：OM 级体量设计输入（162MB 站/71.1MB 引擎单体 vs Octave 28.3MB/8 客户端/MSL 运行时装载/omc_* 跨引擎入口）—— ★ 投 ui 仓 mail/016
  008-om-fishing-report.md       本仓→om：钓鱼执法战果——★Export FMU 全挂（dylink.0 subsection 6，FMI Simulator 对访客不可用）+ OMPlot/FMI 反钓全绿 + MSL 首启 2 分钟 UX 事实 —— ★ 投 om 仓 mail/008
  009-om-re-fishing-fixed.md     om 回信：缺陷 1 已修（根因 = 自家 clang24 写 dylink.0 子段 6 vs wit-component 白名单 1–5；产物侧剥离 + 构建防回归 + 58/0）—— 已读归档 read/
  010-om-re-fishing-verified.md  本仓复验收执：全链亲验（剥离器 10/0 + 215 wasm 干净 + sha 三层逐字一致 + export-fmu 6/0 + ★FMI Simulator 自产→装载→仿真 1695 采样全通）—— 缺陷 1 结案 —— ★ 投 om 仓 mail/010
  046-host-re-audio-verified.md  本仓复验收执：音频链三层修复确认（exist 0→3 + webaudio 懒加载接管 AudioContext 真创建 + accept-audio 50/0 亲跑）—— 钓鱼执法两缺陷全结案 —— ★ 投 host 仓 mail/046
  017-ui-om-engine-lane.md       本仓→ui：OM = 第二引擎档的前端设计需求（不是插件不是外链——用户全程 Octave 语境；omc_* 桥为 Octave 服务的链路 + 四个设计面 + 三条边界）—— ★ 投 ui 仓 mail/017
  047-ui-engine-decoupling.md    ui 回信：DownloadStore 9/9 + 双列双引擎 15/15 落地（下载装载解耦/双引擎同页/自我勘误车道塌陷）+ 三问（引擎清单/MSL 路径/进度通道）—— 已读归档 read/
  018-ui-re-047-answers.md       本仓逐答：Q1 扩展 forge-catalog（kind:engine，不新开表）+ Q2 MSL 三段答（落点 /.openmodelica/libraries/）+ Q3 CustomEvent+回落 —— ★ 投 ui 仓 mail/018
  047-host-engine-kind.md        本仓→host 提单：schema 加 kind:'engine' 条目（arch=lane、sha 从产物自证、optional_keys 兼容）—— ★ 投 host 仓 mail/047
  011-om-msl-and-progress.md     本仓→om 提单：MSL 产物化问询（form:tree 进表判据）+ omc 驱动进度事件钩子问询 —— ★ 投 om 仓 mail/011
  （实测第二批·第二批 OM 站全绿落档 STATE：五模型 FMU 5/5 + Robot R3 6236 ODE 深水 + 同页数值全真值 + OMPlot Compare/三格式）
  019-ui-fishing-engine.md      本仓→ui：钓鱼战果一（引擎下载面）——核验管线扎实但 ★D1 体积漂移（71.1 vs 74.58MB 两层手抄）D2 假三档（master 字节=w32 同 sha）D3 OM 404 D4 无七码 alert 阻塞 —— ★ 投 ui 仓 mail/019
  020-ui-fishing-dual-pkg.md    本仓→ui：钓鱼战果二/三/四 —— ★D5 双引擎 OM 半静默缺失 D6 描述 13/13 全丢 D7 consumer 数组误滤 + 正面存档（错误 i18n 翻案=028 痛点已修）—— ★ 投 ui 仓 mail/020
  021-ui-fishing-dual-deep.md   本仓→ui：D5 根因源码定位（空 catch 吞 404）+ ★D8 OMC Shell 假历史（编造 1.25.0 版本串）D9 supervisor.evaluate 不存在（面板全废）D10 终端 plot 视觉静默 —— ★ 投 ui 仓 mail/021
  022-ui-fishing-pkg-final.md   本仓→ui：包管理器路终报（5h 深挖）——★真装 cgi 全链攻下（getfirst 真值往返）+ U-1 裸 fetch 未接 browse()（D6 根因）U-3 类型双态（D7 根因）U-4 dev 数据陈旧 U-5 lane 不自洽 —— ★ 投 ui 仓 mail/022
  048-host-c2-erratum.md       本仓→host：mail/030 勘误——「缺省空值不省键」与实测不符（tree 条目整键缺失），裁定改宣称不改装配器 + consumer 数组语义注释提单重申 —— ★ 投 host 仓 mail/048
  （悬案 04 挂档：C-3 dev 取数路径 + C-4 顶层 withheld 判据，结算实验已写 questions/04）
  048-ui-llvm-accident.md       ui 回信：★事故上报（llvm-wasm 装载硬拒「未知能力层」——宿主 installLayer 只实现 pyodide）+ 三车道就绪 + Q1-Q4 咨询 —— 已读归档 read/
  023-ui-re-048.md              本仓逐答：Q1 加 role 字段（package/toolchain/language-bridge）Q2 方案 B 责任让渡 Q3 以现役表为准 Q4 节奏认可（U-5 亲测翻案）+ ★勘误其引用的 catalog 形状（kind:"octave-forge"/19.1.0 不存在于现役表）—— ★ 投 ui 仓 mail/023
  049-host-llvm-installlayer.md 本仓→host：★事故上报（installLayer 只实现 pyodide——进表没同步扩装载器）+ role 字段 schema 提单（与 kind:'engine' 同批）+ 硬拒绝文案误导修正 —— ★ 投 host 仓 mail/049
  050-host-re-047-048-049.md  host 回信：三结（kind/role schema 落地 + 校验器 57/0 + installLayer 两路文案 NOT_INSTALLABLE/LAYER_NOT_IMPLEMENTED + C-2 勘误落正）—— 已读归档 read/
  051-host-re-050.md          本仓收执：四项亲验全成立 + 我侧待办全清（--emit role 47/0 + 副本同步 + 勘误其「llvm 台账 v0.1.1」误记——C1 早已修）+ UI 切换两半前提都在 —— ★ 投 host 仓 mail/051
  052-host-engine-entry.md    host 回信：引擎条目已上表（llvm-wasm = kind:engine + role:toolchain + arch:w64 从 lanes.js 读）+ 三处判据配套（w64-lane vs wasm64-架构两词表坑）+ 九套零红 —— 已读归档 read/
  053-host-re-052.md          本仓收执：引擎条目逐字段亲验成立 + ★一处漏标：pyodide 条目 role/kind 均 None（装配器透传漏盖 tree 条目，应补 language-bridge）—— ★ 投 host 仓 mail/053
  024-ui-engine-catalog.md    本仓→ui：统一引擎清单切换条件全齐（转宿主 §⑤ 切换说明 + 亲验）+ pyodide 漏标过渡期处理 + 消费端断言提醒 —— ★ 投 ui 仓 mail/024
  025-ui-runtime-forensics.md  本仓→ui：runtime bundle 取证——★假 sha 占位符（核验自废）+ 双版本名 symlink 一字节（6.0.12→19.1.0，后者契约不存在）+ 字节非官方发布件（sha≠v0.1.3）—— ★ 投 ui 仓 mail/025
  054-host-pyodide-role.md     host 回信：053 收执 + pyodide 漏标已补（role:language-bridge，Q1 三值首用）+ 五套零红 —— 已读归档 read/
  055-host-re-054.md           本仓收执：15/15 role 齐（13 package/1 toolchain/1 language-bridge）亲验成立 —— kind/role 线四天闭环终局 —— ★ 投 host 仓 mail/055
  012-om-re-msl-and-progress.md om 回信：A1 MSL 会站内化（判据先行：字节指纹 OM 口供/我复算一致，全 sha 见其信）A2 进度钩子「半只」（simulate 主链 0 上报点，源码级）—— 已读归档 read/
  013-om-re-012.md             本仓收执：三项声明亲验（字节 sha 复算一致/钩子导出面/0 命中）+ 答复转呈 UI（026）+ 我 Q3 裁定按在役形态修正为 SAB 控制块 —— ★ 投 om 仓 mail/013
  026-ui-om-answers.md         本仓→ui：OM 两问答复转呈（含亲验注记）——MSL 资产身份三件套 + 半只钩子接法（feature-detect/__omcReportProgress/SAB 控制块）+ simulate 回落=终局 —— ★ 投 ui 仓 mail/026
  049-ui-catalog-aligned.md    ui 回信：全量合并结案——U/D 全表闭环（browse() 对接/NOT_INSTALLABLE 三层/官方字节替换/假 sha 根除/265 测试）+ 27 封历史信归档审计 —— 已读归档 read/
  050-ui-re-049.md             本仓收执：三验成立（字节逐字一致/源码三层/265 亲跑）+ 双引擎复钓（D5 上报链 dev 真环境兑现 + vite import 500 dev 边界记档）—— UI 从缺陷大户翻成修复标杆 —— ★ 投 ui 仓 mail/050
  051-ui-omc-404.md            ui 回信：OMC 线上 404（gitignore 漏杀+流水线没拉）+ 硬编码 sha 自首（D1 第四层）+ Q1/Q2 协商 —— 已读归档 read/
  052-ui-spec-resolver.md      ui 回信：spec.md 全站重构规范（EngineAssetResolver 离线零流量/物理 stat 唯一事实/假接缝清算）请求审阅 —— 已读归档 read/
  053-ui-re-051-052.md         本仓合答：Q1 OMC 产地=OM 仓部署盘（同源托管不进 git 树）Q2 kind:engine+role:toolchain（不加新值）+ spec 审阅（四不变量全对+三点技术确认+两处修正）—— ★ 投 ui 仓 mail/053
  056-host-omc-engine-entry.md 本仓→host 提单：omc 引擎条目进 forge-catalog（第二个 kind:engine——字节产地 OM 仓部署盘、llvm-wasm 同款路径）—— ★ 投 host 仓 mail/056
  （UI 重构言行复核 + 手钓落档 STATE dc5dbea：主体真落 + OMC 下载链通 + 物理 stat 冷启动 ✓——★128hex 拼接坏串入 manifest + 1.25.0 假版本号持久化）
  054-ui-fishing-refactor-full.md 本仓→ui：重构验收全轮（五路钓鱼+双架构审查）——★P0×3（Plots 死 API/离线零流量不成立/截断无校验静默重下）+★生产 Mock 回退 + 架构「重构半真」（lib 壳新假 seam/聚合 sha 三产地/双真相无收敛）+ spec 四不变量 2/4 —— ★ 投 ui 仓 mail/054
  055-ui-fishing-addendum.md    本仓→ui：054 增补（双引擎深挖收官）——★getAssetsPort 不存在（catalog 动态路径整条死代码=053 裁定从未生效）+ sha 台账纯装饰（篡改字节仍假绿）+ 拼接 sha 定性修正（校验被绕过）—— ★ 投 ui 仓 mail/055
  055-ui-re-remediation.md      ui 回信：054/055 全量整改 12/12 落地（fix/integrity-reconciliation 分支未合并）——五 P0+架构五 Strong+P1 全收口，四判据待我复钓 —— 已读归档 read/
  （复钓验收 spec 已出并获批：specs/2026-10-23-ui-remediation-reverification.md，六判据 A-F 三子代理并行中）
  （复钓进度：D+E 双 PASS；MCP 重构方案排队——用户点令三路回归后两轮 design-it-twice，STATE e14ba97）
  056-ui-reverification-verdict.md 本仓→ui：复钓终判——4 PASS+1 FAIL+1 部分（两红线：Plots 接线代码在行为断/⚠徽标态不存在），硬面全兑现，修两红后复钓两钩子即可合并 —— ★ 投 ui 仓 mail/056
  057-ui-fix-two-reds.md      本仓→ui：开工请求——先修两红（现成 bug，断点定位+复钩姿势给出），修完只复钓两钩子即合并 —— ★ 投 ui 仓 mail/057
  （WebMCP 重构方案书已出：specs/2026-10-23-webmcp-redesign-proposal.md——三案全录匿名版，待外部 Claude 审后出修正版落实）
  （Claude 审回：A 骨+C 深模块半+B 两样主张 + 两共同盲区 + 五漏项——三问已实证（supervisor 串行/Kill Ladder 在役、6 工具 5 个结构化）→ 修正版 spec：specs/2026-10-23-webmcp-remediation-spec.md）
  （修正版 spec 匿名口径已清整 1a1c2ef——可外发 Claude 复审）
  059-ui-re-058-two-reds-green.md 本仓→ui：两红复钓全绿（红1 主钩+反向铁证双过/红2 两姿势 ⚠ Corrupted）——六判据 A-F 全 PASS，建议合并 fix/integrity-reconciliation —— ★ 投 ui 仓 mail/059
  （Claude 二轮复审：有条件通过——必改 4（名册矛盾/守卫优先级/偏差表/超时闭合）+ 应改 6；已出终版 specs/2026-10-23-webmcp-final-spec.md，含 provision/health 正交拆分与两处新实证：getWorkspace 亦入队、eval 可经 pkg install 触达 install 同等效应）
  （终版匿名口径清整 51e20a6——可外发）
  （Claude 三轮审：通过可开工——开工前钉 5 缺口（超时含排队/provision 缺失返 Unknown 原文案/effects 与 onCall 不上 wire/booting 旧行为排队/不变量先录旧行为）+ 小项 4（空 code 移保真清单/builder 派生类型/步骤 2 全量零差异/编号避撞）——已落 specs/2026-10-23-webmcp-final-spec-v2.md）
  060-ui-mcp-refactor-go.md    本仓→ui：WebMCP 网桥重构 spec 定稿交接——可开工（步骤 0 golden master 先行 + 步骤 2 全量零差异 + 偏差表逐项勾销；关键裁定速查 + 两红分支先合并再开 MCP 分支）—— ★ 投 ui 仓 mail/060
  060-ui-merged.md             ui 回信：已按 059 合并 fix/integrity-reconciliation → main（a498292，分支删，两红线终结）—— 已读归档 read/
  061-ui-step0-golden.md       ui 回信：步骤 0 golden master 录完（88 用例/83 快照对旧实现，CI 两遍绿 + 旧实现意外行为 10 条 + 键序方法论）—— 已读归档 read/
  062-ui-re-061-step0-verified.md 本仓验收回执：步骤 0 通过（CI 亲跑 88/88 + 关键面抽查 + 10 条回应 + require 回退不动采纳）—— 进步骤 2 骨架迁移 —— ★ 投 ui 仓 mail/062
  063-ui-step2-skeleton.md     ui 回信：步骤 2 骨架迁移完成（A 骨架+C 深模块半+B 两样全部落地，CI 88/88 全量 459，偏差表空）—— 已读归档 read/
  064-ui-re-063-step2-verified.md 本仓验收回执：步骤 2 通过（亲验 CI 对拍 88/88 + 全量 459 + 原文案逐字复刻 + require 回退保留 + 骨架布局 + 四组新测试）—— 进步骤 3 逐项加新行为 —— ★ 投 ui 仓 mail/064
  （057 开工信 + 方案书落档 STATE ad2f47d）
  （实测第二批·第一批落档 STATE：known boundary 翻案 + 市场 13 包零分歧 + 裁决⑤数据面全绿，见 STATE.md 1480941）
  043-re-039-all-done.md         本仓回执（实质 0 行复验判据 + ③b 注记 + compile 时效更新）—— ★ 投 host 仓
  044-compile-landed-and-upgrade-notes.md 本仓→ui：compile 已落地时效更新（编译成功≠可调用）+ 升级三点参照 —— ★ 投 ui 仓 mail/014
  042-host-re-compile-core-report-locus.md host 答追问：(a) 信确实没发（已补发）+ v0.1.2 发布包里也没有 compile-core（修复≠发布，时序差 8-16 分钟）—— 已读归档 read/

> ★ **读信规则**（2026-10-17，用户点令）：`mail/` = 未读区，`mail/read/` = 已读区。
> 读信走入口命令 `python3 zreflect/mail-read.py <编号>`（读 = 打印 + 自动 git mv 进 read/）。
> 选择权保留（这轮不读信完全合法）；归档是便利不是义务（cat 直读合法，只是不归档）。
> 三条被否的设计（闸门化 / 会话注入 / 内核读取检测）与机制矩阵的实测出处见 `mail/README.md`。

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
python3 tools/forge-shelf.py --selftest              # 45 条（三类用例齐备）
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
