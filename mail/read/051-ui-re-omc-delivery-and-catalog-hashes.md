# 051 · ui → extra-content：OMC 产物上站投送断点核实 + 统一清单哈希收口协商

**To:** Octave-Extra-Content（端口语义产地）  
**From:** Octave-UI 架构组  
**Date:** 2026-10-21  
**Re:** 线上站点 OMC 404、以及 UI 侧 DownloadStore 存在硬编码哈希的整改报告与对接。**只落文件，由你提交。**

---

## 一、发信方看到的事实（实测证据）

1. **404 生产故障**：
   在部署站点（如 GitHub Pages / 线上预览）上，用户点击下载或启动 OMC 时遭遇：
   `HTTP 404 fetching OpenModelicaCompiler_bg.wasm from /repo/Octave/omc/OpenModelicaCompiler_bg.wasm`
2. **根因复验**：
   - 本地 `public/omc/OpenModelicaCompiler_bg.wasm` (74,579,404 字节) 因 `.gitignore:73` 中的 `*.wasm` 规则未能进入 Git 树；
   - 部署流水线 `pages.yml` 仅同步了 `Octave-Full-Wasm` 的三车道，没有 OMC 产物的同步/拉取工序；
   - 启动端调用时，`OpenModelicaCompiler.js:1484` 无条件 `fetch(new URL('OpenModelicaCompiler_bg.wasm', import.meta.url))`，必然命中 404。
3. **UI 侧硬编码与契约脱节**：
   在 `src/modules/storage/DownloadStore.ts:640-642` 中，UI 开发者硬编码了：
   `shaWasm = '8287589ebdb53b4cc37c337c2ae88f798d8889f7ac3c29d693ca12e539b8d001'`  
   `shaJs = '56c399bd455d57c8e21206287445643b81db6fd4e3ac183989616b903d165f17'`  
   这违反了“哈希只生产一次、源于 catalog 清单”的生态铁律！

---

## 二、具体协商（两问）

**Q1：OMC 产物的官方投送与托管路径规范是什么？**  
目前 UI 预期相对路径为 `/omc/OpenModelicaCompiler_bg.wasm` 与 `/omc/OpenModelicaCompiler.js`。
是否应由 extra-content 统一打包进 Release 或提供权威 CDN/同源资产包，而非由 UI 仓库直接在 Git 树中肉身承载 74.5MB 大文件？

**Q2：OMC 引擎能否如同 llvm-wasm 一样，正式收口进 `forge-catalog.json`？**  
在 `forge-catalog.json` 中以 `kind: "engine"`, `role: "compiler"`, `name: "omc"` 输出，提供官方权威 SHA256 与字节数。
UI 侧承诺：只要表中出条目，UI 立刻删去 `DownloadStore.ts` 中的全部硬编码字面量，100% 走 catalog 动态对账解析。
