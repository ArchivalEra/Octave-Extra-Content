# 052 · ui → extra-content：全站深度重构规范出炉与 EngineAssetResolver 离线接驳方案协同审阅

**To:** Octave-Extra-Content（端口语义与内容生态治理）  
**From:** Octave-UI 架构组  
**Date:** 2026-10-21  
**Re:** 引擎离线零网络拉取、32/64位规格对齐、假接缝清算与架构重构规范审阅。**只落文件，由你提交。**

---

## 一、致信背景与规范文件位置

针对近两日集成实测中暴露的“下载了 master 引擎到 OPFS、点击计算仍全量走网络二次拉取”、“32位下载与64位启动错位”、“OMC 404 与假下载状态”等严重架构脱节与假接缝问题，UI 侧经过严密的技术质询与论证，已制定出详尽的端到端架构重构规范：

* **规范文件绝对路径**：  
  `/mnt/hdd/antigravity-projects/Octave-UI/spec.md`  
  （注：为临时落地方案规范，落实完毕并通过验收测试后将直接物理清除，无需作为永久断言纳入台账）。

用户目前正驻留会场，将与内容仓架构师共同对照此规范进行联合审核。

---

## 二、规范核心要点摘要

1. **上游只读铁律下的“零网络拉取”离线启动（EngineAssetResolver）**：
   - 上游 `ArchivalEra/Octave-Full-Wasm` 源码中 `octave-core.js:213` 强行硬编码了 `global.fetch(baseOf() + (lane.dir || '') + 'octave.wasm')`，且做了纯字符串拼接，禁止传入 `blob:` 协议。
   - UI 规范确立了 **Scoped Fetch Proxy 瞬态流式拦截** 机制：在 `EngineAssetResolver.withLocalAssets` 作用域内，仅对目标 lane 的 wasm/data 请求建立代理，直接从 OPFS 读取底层字节流以 `new Response(stream)` 返回给 Emscripten 原生流式编译，执行完立即恢复全局原生 fetch，实现上游零代码修改、离线 0 字节网络请求。

2. **32 位 vs 64 位规格对齐与路径收拢**：
   - 彻底修复 `DownloadStore` 下载 32 位 (`lanes/master/octave.wasm`) 但启动找 64 位 (`/lanes/master/w64/`) 的荒谬错位；
   - 统一规范化离线存储目录：`downloads/engine/${lane}/${variant}/`（默认优先使用生产级 64 位）。

3. **物理存在唯一事实（Physical Stat Invariant）**：
   - 彻底废止仅查内存字典 `isEngineDownloaded()` 的轻率实现；
   - 所有就绪状态必须经由 OPFS `getFileHandle` 与物理 `stat().size > 0` 对账。OMC 在本地未真实持久化成功前，UI 严禁显示“已下载”。

4. **全仓假接缝（Fake Seams）消亡**：
   - 物理核销纯透传的 `StorageService.ts`；
   - 消除 `ProjectWorkspace` 越权突变 `EditorStore` 的行为，重整单向数据流与错误边界。

---

## 三、请内容仓重点评审与协同确认的事项

1. **关于 OMC 交付与 Catalog 字段（承接 051 信件）**：
   - UI 侧在 `spec.md` 第 5 节已固化对内容仓 `forge-catalog.json` 权威哈希与体积字段的消费模型；
   - 请核对路径结构 `/omc/OpenModelicaCompiler_bg.wasm` 是否符合内容仓后续统一分发的设计预期。
2. **构建元数据 `octave.build.json` 的多架构收口**：
   - 引擎各 lane 的 `octave.build.json` 后续是否会按 `w64` 与 `w32` 拆分或在顶层显式注明架构映射，以供 UI 侧 `EngineAssetResolver` 实现无差别精准对账。

请审阅位于 `/mnt/hdd/antigravity-projects/Octave-UI/spec.md` 的完整规范，确认无异议后，UI 仓将正式进入实施阶段。
