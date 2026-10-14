# 02: 能力层条目（`symbolic` 要 Python/SymPy）落在谁的输出里？

**Status:** ready-for-agent

**Settling:** `tools/forge-shelf.py` —— 跑 `tools/forge-shelf.py --emit /tmp/e.json` 后读 `symbolic` 条目：若它带一条**指向能力层的依赖边**（`deps` 含一个 `form:"tree"` 条目的 name）⇒ 边落在本仓输出（rc=0，结案）；若 `symbolic` 条目与 `cgi` 在字段上无从区分、边只在宿主侧表里 ⇒ 边落在宿主输出（rc=1，本单第一交付物 = 与宿主对齐由谁出这条边）。

## 背景（实测，2026-10-14）

`symbolic` 是**纯 `.m`** 却**装上跑不动**：其 `DESCRIPTION` 明写
`SystemRequirements: python, sympy (>= 1.5.1), mpmath (>= 1.0)`，而本构建 wasm 里没有
Python 运行时。实测 `detect_kinds('symbolic-3.2.2.tar.gz')` 返回 `['m']` —— 与真·开箱即用的
`cgi` **判得一模一样** ⇒ **`kinds` 对这类包会说谎**（本仓 README 记载的已知角落）。

## 表示法已定，未定的是落点（2026-10-14 修，据宿主 mail/002 与接缝 §2）

**表示法**已由接缝 §2 定：能力层 = **`form:"tree"` 的普通条目**，靠**一条依赖边**
（`symbolic` → 该条目）连进同一张 `deps` 图，**不引入新字段**。
**未定的是**：这条 `form:"tree"` 条目与这条边，**落在谁的输出里** ——
- **本仓侧**：本仓 `--emit` 出一条 `form:"tree"` 能力层条目 + `symbolic` 指向它的边；
- **宿主侧**：宿主在装配表里补这条边（本仓只出包条目）。

两侧**都还没落地**（宿主 `build/extra-content/` 端口产地仍是待办）⇒ 这是**两仓共同的缺口**，
不是本仓单方的。宿主建议：悬案留在本仓（本仓出 `form:"tree"` 条目），宿主补 schema + 校验器，
两边各挂一条、交叉引用。

## ★ 一条被推翻的引用（R-002）

本仓文档曾把这件事说成「接缝 §2 的 `needs` 轴」。**实测：接缝 §2 没有 `needs` 这个轴**
（`grep needs` 该文件返回空），宿主侧也无任何代码读它。已进翻案台账 `R-002`；
宿主侧同步修了它自己的两处文档漂移并新增 `R-015`（见 `mail/002`）。

## 结案判据（复跑）

- 跑上面那条命令，读 `symbolic` 条目；
- 它带一条指向 `form:"tree"` 条目的依赖边 ⇒ 边落在本仓（结案）；
- 与 `cgi` 无从区分、边只在宿主侧 ⇒ 边落在宿主（与宿主对齐后结案）。
