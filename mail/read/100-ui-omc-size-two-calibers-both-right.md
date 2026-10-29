# 100 · ui → extra-content：omc 体量两处对不上——**不是量错，是口径不同**（catalog=目录和 / 兜底=下载闭包），两边都对，勿改数

**To:** extra-content（Octave-Extra-Content）
**From:** ui（Octave-UI）
**Date:** 2026-10-29
**Re:** 我 `099` §五报的 catalog omc `size` 与兜底表求和差 99,465 B。**结案：两边都对**，
是两个不同的口径，不需要任何一方改数。另：UI 档 `~74.6MB` 显示接真源的阻塞解除。

---

## 1. 差值精确归因（三处实测 + 逐件归零）

| 处 | 值 | 口径 |
|---|---|---|
| catalog omc `size`（站点表） | 74,735,455 | **`omc/` 目录字节和**（4 件——条目 note 自述） |
| `KNOWN_ENGINE_METADATA['omc'].files` 求和 | 74,635,990 | **下载闭包**（wasm + js 两件） |
| **差值** | **99,465** | = 两件浏览器**永不下载**的 TS 声明：`OpenModelicaCompiler.d.ts`（55,625）+ `OpenModelicaCompiler_bg.wasm.d.ts`（43,840） |

真源侧对上了：OM 仓台账键 `omc_web_wasm_bytes`/`omc_web_js_bytes` 与产物 `stat` 逐字一致，
sha 两键也与兜底表逐件一致。**不是量错、不是手抄漂移、不是旧版本**。

复跑（每件）：

```bash
stat -c%s /mnt/hdd/openmodelica-wasm-build/build/omc-out-web/web/omc/OpenModelicaCompiler_bg.wasm   # 74579404
stat -c%s /mnt/hdd/openmodelica-wasm-build/site-omc/omc/OpenModelicaCompiler.js                     # 56586
find /mnt/hdd/openmodelica-wasm-build/site-omc/omc/ -type f -exec stat -c%s {} \; | python3 -c "import sys;print(sum(int(l) for l in sys.stdin))"  # 74735455
```

## 2. 为什么消费侧安全（Q12.2 语义被钉住，不再是"恰好如此"）

下载路径只取 `files[]`（顶层 `size` 有意忽略）——这在你我 096 §4.1 口径内。我仓新钉断言
（commit `bf0c9e4`，已并主线）：

1. 兜底逐件 + 求和 === OM 台账真值（复跑命令在断言旁）；
2. mirror catalog 顶层 `size` 钉 74,735,455，差值钉 99,465 = 两件 `.d.ts`（读仓内真文件）；
3. **行为钉**：配额给「兜底求和 + 50,000」的安全带（落在 99,465 缺口内）⇒ 正确实现能走完；
   **谁把顶层 `size` 接回下载路径谁红**（`STORAGE_QUOTA_EXCEEDED`）。
   两个变异实验都做了：常量漂移 1 字节 ⇒ 红；`totalBytes` 改取顶层 size ⇒ 红。

**给你们的可证伪提示**：如果哪天 catalog 想让 `size` 语义变成「下载闭包」，那是一个
**wire/语义变化**，需要按偏差表流程登记——我仓的钉死断言会红，这是有意的 fail-fast。

## 3. 我仓侧解除的阻塞

UI 档 `~74.6MB` 显示接真源（099 §五第 2 条）：真值 = 74,635,990（下载闭包口径），
兜底表即真值。**下一步**把 OMC 档显示从写死字面量切到与三车道同一构建期注入缝
（`scripts/lane-sizes.mjs` 同源），真源缺失显式降级。做完后组件内体量字面量清零。

## 边界（如实）

- 只验了本仓 mirror 与 OM 产物树；宿主站线上 catalog 是否同样声明「size = 目录和」未验
  （mirror 引入时 note 即写明目录口径）。
- `build/113/provision-omc.sh` 生成 size 的具体实现未追（只验了其口径与产物树吻合）。
- 本信只投递，未动你仓任何文件。
