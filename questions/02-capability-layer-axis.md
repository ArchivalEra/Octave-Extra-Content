# 02: 能力层条目（`symbolic` 要 Python/SymPy）落在谁的输出里？

**Status:** resolved

**Settling:** `tools/forge-shelf.py` —— 跑 `tools/forge-shelf.py --emit /tmp/e.json` 后读 `symbolic` 条目：`deps == ["pyodide"]` ⇒ 边落在本仓输出（rc=0，结案）；`deps == []` 或与 `cgi` 无从区分 ⇒ 边未落（rc=1，本单第一交付物 = 定落点）。

## 结论（2026-10-15 结案）

**边落在本仓输出**：`packages/symbolic.json` 的 `depends: ["pyodide"]` ⇒ `--emit` 出的
`symbolic` 条目 `deps == ["pyodide"]`（实测：`--emit` 后读该条 `deps`）。

**字面量由宿主确认**（`mail/010` 末节）：`deps` 目标名 = **`"pyodide"`**（逐字照写，
即宿主产的那条能力层条目的 `name`）。**不需要别的字段**（接缝 §2：**不加 `needs`**）。

判据（复跑）：`python3 tools/forge-shelf.py --emit /tmp/e.json` ⇒ `symbolic.deps == ["pyodide"]`；
且该表过宿主校验器（`validate-content-list.py --list /tmp/e.json --producer octave-extra-content` ⇒ `ok`）。

## ★ 顺带发现：宿主侧有一条**同义的硬编码**，本仓这条边可接替它

`Octave-Full-Wasm/build/forge-catalog.py` 的 `catalog_doc()` 里写着：

```python
if p["name"] == "symbolic" and any(e["name"] == "pyodide" for e in extra):
    if "pyodide" not in p["deps"]:
        p["deps"] = list(p["deps"]) + ["pyodide"]
```

⇒ 宿主**按包名硬编码**了这条边。**本仓现在从档案出这条边**（数据驱动）⇒ 两处同义。
**已在 `mail/011` 请宿主删掉那段硬编码**（它的闸门不查表外 deps，本仓的边会照常流过）。
在它删之前：两处结果一致（幂等），**不冲突**。

## 背景（当时的实测）

`symbolic` 是**纯 `.m`** 却**装上跑不动**（`DESCRIPTION` 要 `python, sympy, mpmath`，
而本构建无 Python 运行时）；`detect_kinds` 探得 `['m']` ⇒ **`kinds` 对这类包会说谎**。

## 表示法与落点的裁决链

1. **表示法**由接缝 §2 定：能力层 = `form:"tree"` 的**普通条目** + 一条**依赖边**，**不加新字段**；
2. **「普通」不限条数**（宿主 `mail/010` 裁决②，读消费侧代码判的）；
3. **落点** = 本仓输出（本单结案）；
4. 假引用「接缝 §2 的 `needs` 轴」已进翻案台账 `R-002`；宿主侧同步修了两处文档漂移并新增 `R-015`。
