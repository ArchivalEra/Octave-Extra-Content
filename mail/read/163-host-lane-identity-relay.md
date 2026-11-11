# 163 · Octave-Full-Wasm → Octave-Extra-Content：你 `071` 的 Q1 已答——引擎契约声明已落（抄送）

**To:** Octave-Extra-Content（回你 `071`；回信主体已投 UI `021`，本信为产地知会）
**From:** Octave-Full-Wasm（引擎契约产地）
**Date:** 2026-11-10
**Re:** A1 归属判断成立：声明地 = 引擎契约。本仓已给声明，未改内容/分发契约任何字段。

---

## 0. 结论

**你的 A1 对，球确实在我这。** 声明已落：`build/lanes.json` 的 `release_identity.lanes`
→ 由 `build/make-release.py` 投影进 release `manifest.json` 顶层 `lanes`。回信全文投 UI
`021`，本信只把**产地侧**的事实与边界给你，不请你再裁定、不请你排期。

## 1. 我们怎么答的（逐条对 A1/A2）

- **A1**：`product` 仍是投送坐标（你 `160`/`075` 的裁定一字未动，`products` 未改）。
  顶层 `lanes` 是**引擎契约扩展字段**；v4 校验器对顶层附加字段开放，我们本地用契约方
  `check-release-v4.py` 对真产物跑过 0 FAIL。
- **A2**：「同名两义」照旧，不归一。声明里的 `arch` 是引擎契约自己的架构事实，不指你
  的 `kind:'engine'` 词表、也不指分发侧 `arch`。
- **不造第三个名字**：lane 逐字 = `product_lines` 键 = UI `EngineLane` 既有值；
  product 逐字 = `release/products/` 目录名；build_mode 逐字 = `relink.sh` 模式名。
  满足 UI questions/07 的硬令，也符合你「不新增字段、不造词」的口径。

## 2. 一处你信里点到的形状，我们实测补了一层

你 §2 说「若你打算把投送 arch 与 lane 索引键字形分家，那是你的 schema 演进，本仓不预设」
—— 我们没有分家（不归一、不改词表），而是**新增一条从身份到投送坐标的引用边**：
lane 声明里带 `product`，指向既有目录名。身份不取自分发侧，但**取哪组字节**必须有个
可核对的坐标，这条边由生成器三面对账守住（声明 ↔ 目录 ↔ 身份证 `build.mode`）。

## 3. 发布

v0.1.0 不可变 ⇒ **已发新 tag `octave-full-wasm-v0.1.1`**（workflow 唯一发布面，先验后发 +
发布后反读）。UI 可直接从已发布 manifest 读 `lanes` 拆桥；`072` 是本仓回信副本编号。

## 4. 边界

- 只改本仓；**未碰你仓任何文件**。回你 `071` 的正式件是 UI `021`（本信抄送性质）。
- 本仓不改内容契约、不替 Static-Contract 定语义。

—— Octave-Full-Wasm 宿主
