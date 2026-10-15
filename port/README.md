# 端口（port）· 内容清单规范

> **权威产地 = 宿主仓 `Octave-Full-Wasm` 的 `build/extra-content/`**（★待落地）。
> 本目录是**消费侧副本**，供本仓与生产者自证时对照；**两侧不一致时以宿主为准**。
> 设计结论 = 宿主 `build/113/NOTES-extra-content-seam.md`（2026-10-14 判决）。
>
> ★ **产地裁决（2026-10-14，回应本仓 `mail/003` 的分歧，见宿主 `mail/004`）**：
> 接缝 §4（产地 = 宿主）与 §8.1（把端口写进"内容契约"= 本仓）曾**自相矛盾**。
> **裁决 = 产地归宿主**（依据：端口 = 应用核心的接受面；宿主已有 `check-forge-catalog.py`
> 的 R1–R4 判据范式；UI 读的是宿主站点的表）⇒ **schema + 校验器归宿主**，
> 本仓**符合**它并**共发布副本**（本文件即那份副本，身份与上面那句"以宿主为准"**不变**）。
> 本仓悬案 `questions/03-port-origin.md` 据此结案。
> **内容语义**（四态含义 / `content` 诚实 / 版本策略 / 许可台账）仍归本仓 —— 见
> 「归属 ≠ 投送」：归属 = 本仓，投送 = 宿主（站点里的表），对话 = 经 `mail/`。

## 端口是什么（一句话）

**三仓之间的接缝长在「记录」上，不长在「方法」上** —— 各生产者（本仓、LLVM-wasm、以及
将来的运行时供给方）发布**同一种记录**，宿主作为**消费适配器**读它。宿主的方法名是它内部的事。

## 记录形状（schema 2；见接缝 §2 + 宿主产地 `content-list.schema.json`）

```json
{ "schema": 2, "producer": { "id": "octave-extra-content", "pin": "submodule:<sha>" },
  "octave": "11.3.0",
  "entries": [ {
    "name": "optim",
    "version": "1.6.3",
    "url": "assets/forge/optim-1.6.3.tar.gz",   // 交付路径（站点态必同源相对；生产者态可为上游绝对）
    "upstream_url": "https://…",                // 出处（记账用，不参与运行期）—— 两段式
    "sha256": "59fb…",                          // 必填，fail-closed
    "size": 422679,
    "form": "pkg",                              // 投送形态：pkg | tree | oct | octdir | file | js
    "content": ["m", "src"],                    // 内容构成：m | src | oct（**只对 form:"pkg" 有意义**）
    "license": "GPL-3.0-or-later",              // 许可（逐条目；能力层可带说明）
    "consumer": ["octave"],                     // 消费面（可选；octave | omc；缺省 = octave）
    "deps": ["statistics", "struct"]
  } ] }
```

**两条命名纪律**（收编实测缺陷：`kind` 与 `kinds` 同名两义 —— manifest 的 `kind` 是投送形态、
catalog 的 `kinds` 是内容构成）：
- **`form`** = 投送形态（**供给期从字节派生**，不是作者手写）；
- **`content`** = 内容构成（今天的 `kinds`）。

**能力层（Pyodide / clang）= `form:"tree"` 的普通条目**，进**同一张 `deps` 图** ⇒
客户端只有一种遍历；"这条还要拉多少"从「闭包 ∩ tree 条目」推出，不需要新字段。
（"普通"是说**它不特殊** —— **不限于一条**；LLVM-wasm 的 13 条即合法，见下裁决。）

### ★ 宿主三裁决（2026-10-14，回应本仓 `mail/007`；已落产地 `build/extra-content/`）

| # | 缺口 | 裁决 | 落地 |
|---|---|---|---|
| ① | `content` 对能力层无合法取值 | **不扩枚举；能力层 `content: []`** | schema 描述写死 + 校验器**反向断言**（`form:"tree"` 带非空 content ⇒ 必红） |
| ② | 消费面无处声明 | **加 `consumer` 可选轴**（`octave`/`omc`；**缺省 = `octave`**，向后兼容） | schema `entry.properties.consumer` + 校验器取值校验 |
| ③ | `pin` 的"未发布"无判据 | **建议前缀形态**（`release:` / `commit:` / `submodule:`），**不强制** | schema 描述；「核 release 存在性」登记为宿主悬案（未实现） |

> ⚠️ 裁决 ② 与接缝 §2 的「不引入新字段」**不冲突**：§2 禁的是"**为了表达能力层**而加字段"，
> `consumer` 是**消费面标注**且**可选** ⇒ 合规（协商规则本就允许追加 optional 轴）。
>
> ⚠️ 裁决 ① 的实测背景：LLVM-wasm 的 13 条表填了 `wasm`/`module`/`tree`/… ⇒ 校验器 17 条
> PROBLEM。根因**不是它的错** —— `content` 的原意是"包的源构成"，能力层**没有合法取值**。
> 它已改为 `content: []` ⇒ 现在 `ok`。

## 协商规则（唯一从"最大灵活"方案拿的一条）

> 新轴**只能追加**，且必须声明 `"optional": true` 才允许旧消费者**忽略**；
> 不声明 ⇒ 旧消费者必须**撤下该条目**（fail-closed）并落账。
> **"忽略"是给可选轴的礼遇，不是默认。**

## 生产者要做的三件事（都不要求宿主在场）

1. `emit(octave_version)` —— 离线纯函数出表（本仓 `tools/forge-shelf.py --emit` 就是）；
2. 过校验器自证（宿主 `validate-content-list.py`，**已落地**；`--producer <你的 id>` / `--site`）；
3. `pin` 自述 —— 本仓 = **submodule commit**（建议前缀形态，见裁决 ③）。

## 两边自证（replace-don't-layer）

| 侧 | 怎么测 | 现役件 |
|---|---|---|
| 生产者 × 假宿主 | 只跑校验器（它只有接受面） | 本仓 `--selftest` 24 条（三类用例齐备）+ 过宿主校验器 `--producer` ⇒ `ok` |
| 宿主 × 假生产者 | 用夹具站（摘掉某个随站包造"只在货架上"的场景） | 宿主 `test/browser/accept-catalog-load.mjs`（27/0）+ `build/113/prep-catalog-accept-site.sh` |

## 待办

- [x] 宿主 `build/extra-content/{content-list.schema.json, validate-content-list.py, golden/, bad/}`
      —— **宿主已完成**（2026-10-14，见宿主 `mail/005`）。本目录是消费侧副本，仍以宿主为准。
- [x] 本仓 `--emit` 输出加 `form`/`content` 两轴（`kinds` 保留为兼容视图）—— 2026-10-14 完成
- [x] 本仓 `--emit` 顶层加 `producer` 自述（`{id, pin}`，接缝 §4「pin 自述」）+ 每条
      `upstream_url`（两段式的生产者态）—— 2026-10-14 完成。实测：过宿主
      `validate-content-list.py --list <表> --producer octave-extra-content` ⇒ `ok`。
- [x] **三裁决同步**（宿主 `mail/008`：`content` 能力层留空 / `consumer` 可选轴 / `pin` 建议前缀）
      —— 2026-10-14 同步进本副本（见上「宿主三裁决」表）。
- [x] `packages/symbolic.json` 建档（`--add`/`--fetch`/`--probe` 实测，含能力层需求事实）
      —— 2026-10-14 完成。⚠️ 能力层的**表示法已定**（接缝 §2：`form:"tree"` 普通条目 +
      依赖边，**不引入新字段**）；宿主已出 `golden/{runtime,toolchain}.json` 两个样件示范。
      假引用 `needs` 已进翻案台账 `R-002`。
- [ ] **本仓侧能力层落点**（`symbolic` 的 deps 边指向 pyodide 条目）：**宿主侧已完成**
      （`provision-pyodide.sh` 供三件资产 + 装配器产 `form:"tree"` 条目并入同一张 packs +
      `symbolic` 靠 deps 边指向；`accept-capability-layer` 12/0）—— 本仓侧要在 `--emit`
      里出这条边（见悬案 `questions/02-capability-layer-axis.md`）。
