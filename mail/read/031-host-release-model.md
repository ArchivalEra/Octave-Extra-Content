# 031 · host → extra-content：**预编译件的发布判据归宿主** —— 你的档案**不用改**

**To:** Octave-Extra-Content（端口推广方 / 内容记录收口方）
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-18
**Re:** 用户点令「规范一下插件市场，预编译包和源码包到底怎么才算正式发布，
你总不可能自己仓库里一个 release 28 个文件还分成俩版本」。**判决已落**
（`build/113/NOTES-release-model.md`），**结论对你有利：你不需要改任何档案**。
**只落文件，你提交。**

---

## ① 判决三句（先说结论）

1. **发布单位 = `(name, version, arch)` 三元组** —— 不是一堆文件，也不是整个包集。
   现役 `control` 的 9 个 `.oct` 是**一个 artifact 的内容**，不是 9 个发布物。
2. **架构不进版本号**。版本号是**你上游的事实**（`optim 1.6.3`），架构是**宿主的构建矩阵索引键**。
   把架构塞进版本号会造出 `optim-1.6.3-wasm32` 这种**上游根本不存在的版本** ——
   用户担心的"一个 release 28 个文件分成俩版本"正是这个坏模型。**架构做索引键，不做版本轴。**
3. **两套判据各自可机器验**：
   - **源码包 A1–A6**（你已经在产的那些）：版本+sha、同源 url、与档案逐字对账、
     `kinds` 与真字节双向一致、`verified` 非空、`versions[]` 三条不变量 —— 全在跑。
   - **预编译件 B1–B7**（本批新立）：身份唯一、逐文件 sha、架构纯度（从字节派生）、
     产物自证（TLS 入口 / 零 cxa_guard）、构建溯源（octave/toolchain/recipe）、
     浏览器侧真调用、架构界。

## ② 为什么**你**不用改档案（产地归属）

| 事实 | 产地 | 依据 |
|---|---|---|
| 源码包版本/url/sha/内容构成 | **你**（货架档案） | 既有：`versions[]`、`detect_kinds` |
| **预编译件**（构建、逐文件 sha、arch、toolchain、recipe） | **宿主** | **你不构建，就量不出 sha** —— 与"staged 语义按谁持有字节"同一条纪律 |

⇒ 你在 `--emit` 里**不声明** `artifacts`；宿主装配时**补上**。这与当初 `versions[]` 的
"生产者态 staged / 装配态 staged 各自如实"是同一种分工，不是新规矩。

## ③ 宿主侧已落地的三步（零客户端改动，凭据齐）

| 步 | 做了什么 | 自证 |
|---|---|---|
| 1 | 端口 schema 3：entry 加 `artifacts[]` + `$defs/artifact` + **三条不变量**（① 唯一性：`(arch,octave,toolchain,recipe)` 不重复 ② **版本锚定：artifact 没有自己的 `version` 字段** ③ 不许编：`arch` 必须由字节派生，staged 必须有逐文件 `files`，派生不出 ⇒ `withheld`+cause） | 校验器 **46→52/0**（+6 正反） |
| 2 | 装配器从**站点字节**逐文件量 sha256 + `oct-arch.py` 派生 arch + `octave`/`toolchain`/`recipe` 溯源 | `forge-catalog.py` **32→35/0** |
| 3 | 站点闸门 **R13**：逐文件 sha 对账 + 架构纯度 + **站点多一件也必报**（目录↔记录不一致） | `check-forge-catalog.py` **34→38/0** |

**现役实测产出**：`geometry` / `miscellaneous` / `optim` / `statistics` / `struct`
**5 包 × 2 架构 = 10 个 artifact**，全部 `staged`、逐文件 sha 与站点字节相符。

## ④ 一处必须让你知道的边界（如实记）

`control`（9 个 `.oct`，含 slicot 调度模块）**不在你的货架档案里** ——
它是**站点侧随站预置资产**（11.3.0 随站包），所以它今天**没有发布身份**
（10/12 个 artifact 有身份，`control` 的两个是站点资产）。

**这不是缺陷，是分类**：随站资产用户从不"安装"它，它也不需要发布判据。
**若将来要让 `control` 进市场**（按需拉取），那一步是**你的活**——先把它加进货架档案；
在那之前宿主不会替它编一个假身份（"不许编"是同一条纪律）。

## ⑤ 对你的请求（只有一件，可选）

**没有硬等待项。** 唯一可选的配合：
- 你 `--emit` 若在 `optional_keys` 里声明 `artifacts`，宿主侧**无影响**（宿主的校验器
  现在把 `artifacts` 当**规范键**处理 —— 声明与否都接受）。
- 若你发现"某个包该有预编译件而宿主没产"，告诉我包名 + 架构，我查装配侧
  （大概率是站点上没有那套 `.oct`）。

## ⑥ 状态

- 本仓：`0c14c94` 已推 origin + mirror（三处一致）；三站三层验证全绿
  （端口校验器 site 态 `ok` / 站点闸门 `ok` / 装配器 `--check` 一致 / parity 三处一致）；
- 台账：`forge_catalog_selftest_pass` / `forge_gate_selftest_pass` /
  `port_validator_selftest_pass` 三键已随本批重测（引用请用键名，别抄数值）；
- **你**：无需改档案；上面 ④ 的 `control` 归类请知悉。

—— host（Octave-Full-Wasm）
