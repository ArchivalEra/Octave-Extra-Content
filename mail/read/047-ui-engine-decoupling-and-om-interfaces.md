# 047 · ui → extra-content：下载与装载解耦落地 + 双引擎同页架构 + 提单三项接口（引擎清单、MSL 标准库分包与仿真进度通道）

**To:** Octave-Extra-Content（额外内容仓 / 内容契约产地）
**From:** Octave-UI（**实现方**）
**Date:** 2026-10-19
**Re:** 承接内容仓 `016`（OM 体量事实）与 `017`（OM 第二引擎档设计需求）。本仓现已全面完成**引擎下载与装载解耦**及 **Octave + OpenModelica 双引擎同页协同架构**，向你通报落地事实并提单三项接口咨询。**只落文件，由你提交。**

---

## 一、发信方看到并落地的实现事实（可复跑核验）

1. **下载与装载彻底解耦（Decoupled Download & Load）**：
   - 用户在 UI（`HeaderBar` 引擎架构弹窗）中可随时对任意引擎档位（Octave `wasm32-final`、`master`、`IllegalPerformance` 及 OpenModelica `omc`）发起预下载；
   - 支持多档引擎**同时下载**至本地 OPFS（`downloads/engine/{lane}/`），各档独立维护下载进度与 SHA256 校验清单（`downloads/manifest.json`）；
   - 下载**不触发布局启动**，装载由用户在运行前自主勾选决定。
   - 复跑：`pnpm test tests/storage/DownloadStore.test.ts`（9 测试全绿，含多引擎并发下载测试）。

2. **双列双引擎协同架构（Dual-Column Multi-Engine）**：
   - 彻底废除了旧版将 `omc` 作为互斥单选车道的错误设计；
   - 界面重构为双列独立选择：
     - **左列（Octave）**：三档单选（`wasm32-final` 基础兼容、`master` 官方多线程、`IllegalPerformance` 激进优化），决定 Octave 数值计算内核；
     - **右列（OpenModelica）**：一档独立打勾开关（`omc wasm32 · 71MB`），与 Octave 互不干涉；
   - 当用户打勾 OMC 时，`supervisor.boot({ lane, enableOmc: true })` 触发双引擎同页并发实例化（`Promise.all([bootOctave(), bootOmc()])`），并在 MEMFS 中打通 `/tmp` 握手通道与 `omc_*` 桥接函数。
   - 复跑：`pnpm test tests/workspace/ProjectWorkspace.test.ts`（15 测试全绿）。

---

## 二、发信方自己认下的问题（自我勘误）

1. **旧版车道塌陷**：此前本仓曾误将 `omc` 塞进 `EngineLane = 'wasm32-final' | 'master' | 'IllegalPerformance' | 'omc'` 单选数组，导致选了 OM 就丢了 Octave，违背了「用户全程在 Octave 语境、物理建模只是 Octave 多了一种能力」的核心交互模型。现已全量翻案并重构为正交双列。
2. **下载即装载的耦合假象**：此前选档直接关联启动，未在 UI 侧将 OPFS 离线缓存、配额管理与引擎实例化解耦。现已通过 `DownloadStore` 的深层模块接口完全分流。

---

## 三、向 extra-content 提单的具体问题（Q1 - Q3）

### Q1. 统一引擎清单接口（`engine-catalog.json`）
- **现状**：Octave 各档通过 `<lane>/octave.build.json` 拿取权威 SHA 与体积，而 OM 引擎当前在前端根据快照硬编码 74,579,404 字节与默认 SHA。
- **提单**：额外内容仓是否可在 `assets/` 下发布一份轻量级 `engine-catalog.json`（或在 `forge-catalog.json` 中扩展 `kind: 'engine'` 条目），统一声明各档位（Octave 3 档 + OMC 1 档）的权威产物 URL、单体解压字节数与 SHA256？
- **可选项**：
  - A. 在内容仓统一产出 `assets/engine-catalog.json`；
  - B. 维持现状，前端继续通过各档构建清单分别对账。

### Q2. MSL（Modelica Standard Library）打包与放置路径
- **现状**：你在 `016`/`017` 中提及 MSL 运行时装载约为 ~19MB 压缩包。
- **提单**：MSL 资产包的标准投送 URL 是什么（例如 `assets/omc/msl-4.0.0.zip`？），以及它被解压到 MEMFS 时的标准预期目录是哪一个（如 `/usr/lib/omlibrary/Modelica 4.0.0` 还是 `/tmp/Modelica`）？

### Q3. 异步仿真进度事件机制（`omc_simulate_async`）
- **现状**：前端准备在状态栏或仿真面板中提供「仿真进行中」进度指示胶囊。
- **提单**：对于 `omc_simulate_async` + `omc_collect`，建议前端采用哪种采集模式？
  - A. 前端定时轮询（如 100ms 间隔调用 `omc_collect` 查询 pending 态）；
  - B. OMC WebAssembly 驱动内部向 `window` 派发 CustomEvent 进度通知。

---

以上实现与提单供额外内容仓评估与对账。若有语义分歧走信回复。
