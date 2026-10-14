# 02: 能力层需求（`symbolic` 要 Python/SymPy）该用什么表示法？

**Status:** ready-for-agent

**Settling:** `tools/forge-shelf.py` —— 跑 `tools/forge-shelf.py --emit /tmp/e.json` 后读 `symbolic` 条目：它与 `cgi` 在字段上可区分（有一条指向能力层的边）⇒ 表示法已定（rc=0，结案）；两者字段无从区分 ⇒ 未定（rc=1，本单第一交付物 = 定表示法）。

## 背景（实测，2026-10-14）

`symbolic` 是**纯 `.m`** 却**装上跑不动**：其 `DESCRIPTION` 明写
`SystemRequirements: python, sympy (>= 1.5.1), mpmath (>= 1.0)`，而本构建 wasm 里没有
Python 运行时。实测 `detect_kinds('symbolic-3.2.2.tar.gz')` 返回 `['m']` —— 与真·开箱即用的
`cgi` **判得一模一样** ⇒ **`kinds` 对这类包会说谎**（本仓 README 记载的已知角落）。

## ★ 一条被推翻的引用（R-002）

本仓文档曾把这件事说成「接缝 §2 的 `needs` 轴」。**实测：接缝 §2 没有 `needs` 这个轴**
（`grep needs` 该文件返回空），且宿主侧**没有任何代码读 `needs`**。§2 的原话是：

> **能力层（Pyodide / clang 工具链）= `form:"tree"` 的普通条目**，进**同一张 `deps` 图**。
> ⇒ 客户端只有**一种**遍历；……**从数据推出，不需要新字段**。

⇒ 按 §2 判决，能力层**不引入新字段**，而是**一条 `form:"tree"` 的普通条目**，靠**依赖边**
把 `symbolic` 连到它。本单的「表示法待定」= 这条边在**本仓 `--emit` 的输出里**怎么落
（本仓现在只出 `form:"pkg"` 的包条目；能力层条目由谁出、边怎么指，见 port/README.md 待办）。

## 结案判据

- 跑上面那条命令，读 `symbolic` 条目；
- 它与 `cgi` 在字段上可区分（有一条指向能力层的边）⇒ 结案；
- 仍无从区分 ⇒ 维持未结案，本单第一交付物 = 定表示法（**优先按 §2 的 `form:"tree"` 边方案**，
  除非有实测证据表明该方案不够）。
