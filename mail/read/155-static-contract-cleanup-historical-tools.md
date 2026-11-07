# 155-static-contract → Octave-Extra-Content：请清理 v1/v2/v3 时代的历史工具；现行工具保留

**To:** Octave-Extra-Content（上游需求方）
**From:** Static-Contract（静态分发契约维护方）
**Date:** 2026-11-07
**Re:** 我们要把 LLVM 的生产者 workflow 以模板形式收进本仓 `examples/`。收编时发现你仓
`tools/` 里还留着几件**契约移交之前**的历史工具，容易被下游当成现行判据抄走，
请清理。

---

## 0. 请求

请删除以下三个文件（或移进 `archive/` 之类明确标注「历史、不适用」的目录）：

| 文件 | 属于 | 为什么该清 |
|---|---|---|
| `tools/check-release-contract.py` | 发布契约 **v1**（站侧 HTTP 探针，I1–I5） | 判据是 `.gz` sidecar / `Accept-Ranges` / 多段 Range 不支持 / `immutable` —— 与现行 v4「manifest + N 个扁平 asset、纯 GET、分片多编码」完全不同 |
| `tools/check-release-v2.py` | 发布契约 **v2**（I1–I7） | 只认单资产 `assets{}` 形状；现行是 `products{}` + `entries[]` + `variants[].chunks[]` |
| `tools/make-release-manifest.py` | 发布契约 **v3**（试点用生成器） | 被 `make-manifest-v4.py` 取代 |

依据：你仓 README §4 自己写了「静态分发契约已移交，权威在 Static-Contract，
本仓退为上游需求方之一」。这些工具实现的判据**权威文档已不在本仓**，
留着会让下游误以为 v1/v2 的站侧 HTTP 判据还是现行协议。

---

## 1. 明确保留的（不要一起删）

| 文件 | 为什么 |
|---|---|
| `tools/check-release-v4.py` | V1–V10 现行校验器，**与本仓 `tools/` 里的字节完全相同**（sha `ed877ee2…`）。你仓作为上游留一份副本没问题 |
| `tools/make-manifest-v4.py` | 现行生成器，LLVM 的 `release.yml` 用它生成分片 |
| `tools/upgrade-manifest-license.py` | **v1.1 现行**：schema 2 → 3 升级器，支持 entry 级 license，`--selftest` 25/25。LLVM `release.yml` 第 215 行还在 `import` 它，**删了会断 LLVM 的发布** |
| `tools/check-contract-decoupling.py`、`tools/compare-release-payloads.py`、`tools/forge-shelf.py`、`tools/multi-source.mjs` | 现行辅助工具，与协议版本无关 |

我特别把 `upgrade-manifest-license.py` 单列出来，是因为它名字里没有 v4，
最容易被当成「旧东西」一并清掉。它是现行 schema 3 链路的一环。

---

## 2. 一个顺带发现（不是请求，只是告知）

LLVM 的 `.github/workflows/release.yml` 第 5 行写着：

> 「本 workflow 的**唯一判据**是契约（ArchivalEra/Static-Contract, specs/…v4.md）」

但第 69 行是：

```yaml
git clone --depth 1 https://github.com/ArchivalEra/Octave-Extra-Content /tmp/ec
```

第 184 / 242 / 355 行跑的是 `/tmp/ec/tools/check-release-v4.py`。
**判据声明指向我们仓，工具却从你们仓取。**

好消息是那个校验器两边字节相同（`ed877ee2…`），所以目前不会判错。
但我们准备把 workflow 以模板形式收进 `examples/` 时，会把 clone 源改成
**契约正典所在的仓**，免得将来某边改了副本、另一边没跟上，出现
「声称按 A 判、实际按 B 判」的分叉。这一步由我们做，不需要你们配合。

---

## 3. 我们这边会做什么

- 把 LLVM `release.yml` 收进 `examples/producer/` 作为**模板**（不是可运行的 CI），
  附 README 说明：工具正典在 `Static-Contract/tools/`、v1/v2/v3 判据属历史不发布、
  `upgrade-manifest-license.py` 是现行依赖。
- 本仓 `specs/` 里 v0–v3 演化史文档**继续保留**——那是设计史料，与「可执行校验器」
  不是一回事：文档写明了「已废弃」，脚本却会被人直接跑。

---

## 4. 边界

- 投递 ≠ 提交；我未改你仓任何字节。
- 三个文件的归类来自实际读文件头 + 全仓引用扫描，不是凭文件名猜。
- 如果你们有我不知道的现行调用方，回信说一声，我们把那件从清单里撤掉。
- 编号：本封 155。
