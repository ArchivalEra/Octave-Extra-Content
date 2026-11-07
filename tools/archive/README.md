# tools/archive/ · 历史工具（**不适用，不要跑，不要抄**）

> 2026-11-07 按 `Static-Contract` 的清理请求归档。它们是**契约移交之前**（v1/v2/v3 时代）
> 的可执行判据/生成器，实现的协议已被现行 **v1 / v1.1** 完全取代。
>
> **现行工具在 `tools/` 上一级目录**；权威文本在
> [`ArchivalEra/Static-Contract`](https://github.com/ArchivalEra/Static-Contract) 的 `specs/`。
> 本仓 `specs/` 里 v0–v3 的演化史文档也**继续保留**（设计史料，与可执行脚本不是一回事）。

## 归档清单

| 文件 | 属于 | 判据为什么不再适用 |
|---|---|---|
| `check-release-contract.py` | 发布契约 **v1**（站侧 HTTP 探针，I1–I5） | 判的是 `.gz` sidecar / `Accept-Ranges` / 多段 Range / `immutable`。现行 v1 是「`manifest.json` + N 个**扁平** asset、纯 GET、分片多编码」，完全不同 |
| `check-release-v2.py` | 发布契约 **v2**（I1–I7） | 只认单资产 `assets{}` 形状。现行是 `products{}` + `entries[]` + `variants[].chunks[]` |
| `make-release-manifest.py` | 发布契约 **v3**（试点生成器） | 已被 `tools/make-manifest-v4.py` 取代 |

## 为什么是「归档」而不是「删除」

`specs/2026-10-30-release-contract-v3.md` 里还引用了其中两件的**历史命令**（如
`tools/check-release-v2.py --selftest`），那份文档已标明「历史、不要按它实现」，
但删掉脚本会让史料彻底失去可读性。**⇒ 留痕但不放行。**

## 现行工具（**不要一起清**）

| 文件 | 用途 |
|---|---|
| `check-release-v4.py` | V1–V10（+ v1.1 V11）现行校验器，与本仓 `tools/` 之外 Static-Contract 那份**字节相同**（`ed877ee2…`） |
| `make-manifest-v4.py` | 现行生成器，LLVM `release.yml` 用它产分片 |
| `upgrade-manifest-license.py` | **v1.1 现行**：schema 2 → 3 升级器，支持 entry 级 license。LLVM `release.yml` 还在 import 它，**删了会断 LLVM 的发布** |
| `check-contract-decoupling.py` | 分发协议 ↔ 市场协议解耦闸门 |
| `compare-release-payloads.py` | 两 release 载荷对账（顺序无关） |
| `forge-shelf.py` | 货架出表（`--emit` / `--probe`） |
| `multi-source.mjs` | 跨源续传示例 |

⚠️ **`upgrade-manifest-license.py` 名字里没有 `v4`，最容易被当成旧东西一并清掉**——
它是现行 schema 3 链路的一环，不是历史。

## 复跑（验本目录确实不在执行面）

```bash
# 现行 pre-commit 只跑 tools/*.py，不进 archive/
grep -n "for t in" reflect-hooks/pre-commit
#   ⇒ make-manifest-v4 check-release-v4 upgrade-manifest-license
#     check-contract-decoupling compare-release-payloads

# 全仓引用扫描（应只剩史料与 archive 自身）
grep -rn "check-release-contract\|check-release-v2\|make-release-manifest" \
  --include=*.py --include=*.sh --include=*.yml . | grep -v "^./tools/archive/" | grep -v "^./mail/"
```
