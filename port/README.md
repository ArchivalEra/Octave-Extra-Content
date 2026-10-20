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
    "description": "Non-linear optimization toolkit.",  // 包级人话描述（可选；见 §字段语义）
    "links": [ { "label": "docs", "url": "https://…" } ],  // 包级链接（可选）
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

### ★ 宿主第二批答复（2026-10-15，回应本仓 `mail/009`；已落产地）

| # | 问题 | 答复 |
|---|---|---|
| ① | `license` 收紧成枚举？ | **不收紧，保持自由字符串/对象**。判据：真实产物**逐文件混合**（LLVM 13 条里四档许可，两个 tar 天然混合）⇒ 枚举会**逼生产者说谎或拆条**；许可台账的价值在**如实**。⚠️ 诚实边界：**无机器判据核"许可写对了没"**（它是记账字段，不参与 fail-closed；唯一 fail-closed 依据是 `sha256`）。 |
| ② | 「普通条目」限制条数吗？ | **不限制**（"普通" = 它不特殊：同一套遍历/同一张图/同一份 schema）。判据：读消费侧代码 —— `assets-loader.js` 闭包遍历按名入图、**一行不看条数**。⇒ LLVM 出 13 条**合法**。 |
| ③ | `--upstream` 重跑修后的表？ | **已重跑，并入 `ok`**（13 条 + 字节 stage 端到端；隔离临时站，未碰 8761）。⇒ 工具链条目进图。 |
| 附 | `size`/`url` 不一致（本仓独立发现） | **由 `form` 决定，都是有意的**：单文件形态 `size` = `url` 指向文件的字节；**`form:"tree"` 的 `size` = 整棵树字节预算**（= `url` 所在目录所有文件之和）。现役 pyodide 即此形态（`size` 22,013,349 = 整目录；`url` 指树里主 wasm 9,598,218）。**本仓不用改**；站点闸门加 R8 sanity（只拦自相矛盾，不参与 fail-closed）。 |

### deps 闭合：**分域**（2026-10-15，host `mail/012` 提出缺口）

`deps` **可以指向表外**（能力层条目由宿主装配器产出，不在本仓 `--emit` 里）——
实测：本仓 `--emit` 13 条里 `symbolic.deps == ["pyodide"]`，而 pyodide 不在表内
（它在**装配态**才有）。⇒ 闭合判据**分两域**：

| 域 | 判据 | 拦什么 |
|---|---|---|
| **本仓 `--emit`（生产者态）** | **部分闭合**：`deps` 目标 ∈ {货架包名} ∪ {能力层名}（能力层名 = `recipes/*.md` 的 basename） | **typo / 未知名**（`pyodid`）；`--selftest` 36 条含 9 条断言 |
| **宿主装配态** | **完整闭合**（R9）：`deps` 目标必须在**同一张表**里有条目 | **真·悬空**（含"站点没供能力层"） |

⇒ 两边各一条、都不假阳（本仓的部分视图不会被"能力层边"误红；宿主的全表不会被部分视图误红）。
⚠️ **本仓部分闭合的上限**（明说）：它只证明"目标名是**存在的能力层**"，**不证明"这个包真需要它"**。

### ★ `arch` 轴（2026-10-16，用户点令「楚河汉界」；宿主 `mail/017` 补告知）

**三档语义**（权威定义在宿主产地 `build/extra-content/content-list.schema.json`，已同步）：

| 条目类 | `arch` |
|---|---|
| 纯 `.m` 包（`content` 不含 `oct`） | **不许带**（无架构概念，任何档都能装） |
| 含 `.oct`（`content` 含 `oct`，或 `form` = `oct`/`octdir`） | **必须带**（`wasm32`/`wasm64`），且与**宿主档**一致（错档 ⇒ `incorrect architecture`） |
| 能力层（`form:"tree"`） | **不许带**（自带运行时，架构与宿主无关 —— 反例：Pyodide 是 wasm32，在 w64 档跑通） |

**派生，不是手写**（与 `form` 同例）：宿主装配器从 `.oct` 字节的 `dylink.0` 段
TARGET_FEATURES 子节读（`build/113/oct-arch.py`）—— **不从目录名推**。
⇒ **生产者不写这个字段**（推端口给含 `.oct` 的生产者时要讲明；写了会在校验器里对不上白红）。
本仓现役 13 包的 `content` 均不含 `oct` ⇒ `--emit` **不产** `arch`（三档语义下的正确行为）。

### ★ `versions[]` 版本候选集（2026-10-16，用户点令「每版各带是否兼容」；全链已闭环）

**形状**（宿主 schema `$defs/candidate`，权威在产地）：条目内嵌候选数组，**不摊平**
（宿主实测：客户端 name→entry 索引是**静默最后者胜** ⇒ 摊平会让旧页面选错架构）。
每条候选：`version` / `sha256` / `url` + 可选 `size` / `requires` + **`stage`**：
- `stage:"staged"` ⇒ **必须带派生轴** `form`/`content`（含 `oct` 还需 `arch`）；
- `stage:"withheld"` ⇒ 带 `withheld_cause`、**不带**派生轴（**派生不出 ⇒ 不许编**）。

**三条不变量**（宿主校验器逐条判，本仓侧保证 ①③）：
① `versions[]` 非空、`version` 两两不重复；
② **顶层标量（`version`/`sha256`/`url`）必须恰好等于某候选（逐字）** —— 防两处各写一份漂移
（本仓实现：顶层与选中候选**同源取字段** ⇒ 天然成立）；
③ `staged` 必带派生轴、`withheld` 不许带。

**staged 是"字节在谁那"的函数**（2026-10-16 宿主确认）：
- **本仓 `--emit`（生产者态）**：`staged` = **我探过包**（有真 `kinds` 可给）；未探 ⇒ `withheld`
  （`withheld_cause: "bytes-not-staged"`）。**本仓 52/52 版本均已探 ⇒ 真表全 staged**。
- **宿主 catalog（装配态）**：`staged` = **字节在站点**（可下载）。同一版在两边可以不同——
  **两张表各自如实**，不要求"以谁的为准"（那会把一方的表变成另一方的投影）。

**注意**：`stage` 描述的是**某个表里某版字节的状态**，**不是**"这版内容是否兼容"
（兼容性 = `arch` × 宿主档 + `requires`，由客户端 `statusOf()` 派生）。

**向后兼容（实测证据）**：`versions[]` 对旧客户端**不可见** —— 8761 上 rebake 后
`accept-symbolic-seam` **9/0 不变**（旧客户端只读顶层标量）；`accept-forge-ondemand` 15/0、
`accept-catalog-load` 27/0 亦不变。

## 协商规则（唯一从"最大灵活"方案拿的一条）

> 新轴**只能追加**，且必须声明 `"optional": true` 才允许旧消费者**忽略**；
> 不声明 ⇒ 旧消费者必须**撤下该条目**（fail-closed）并落账。

### ★ 字段语义钉死（2026-10-20，UI 钓鱼 D6/D7 收编——契约文档没钉死就散在信里，消费端各写各的）

- **`consumer` 是数组、语义是「包含」**：条目 `consumer: ["octave"]` 表示**该面可用**；
  消费端按面筛选时判 `面 ∈ consumer`（**包含**），不是数组与面的全等比较。
  实测反例（UI mail/020 D7）：严格串比较 ⇒ 能力层条目在 Octave 筛选下被滤光（0/2），
  语义正好相反。缺省 = `["octave"]`。
- **`description` 消费端必须渲染**（消费义务，不是可有可无的装饰）：进表就是为了给
  用户看（UI mail/028 Q2 的诉求落地）；不渲染 = 字段白生产。`links` 同理（有就给入口，
  没有就别渲染空壳）。表侧由生产者保真（`--emit` 从档案产出），消费侧忠实呈现——
  两边各自对账，不抄中间值。
- 这两条进 `port/README.md`（本文件 = 宿主产地规范的**副本**；同批向宿主提单把注释
  补进产地 schema —— 与 `kind:'engine'` 扩展同批，见 host `mail/047`）。
> **"忽略"是给可选轴的礼遇，不是默认。**

## 生产者要做的三件事（都不要求宿主在场）

1. `emit(octave_version)` —— 离线纯函数出表（本仓 `tools/forge-shelf.py --emit` 就是）；
2. 过校验器自证（宿主 `validate-content-list.py`，**已落地**；`--producer <你的 id>` / `--site`）；
3. `pin` 自述 —— 本仓 = **submodule commit**（建议前缀形态，见裁决 ③）。

## 两边自证（replace-don't-layer）

| 侧 | 怎么测 | 现役件 |
|---|---|---|
| 生产者 × 假宿主 | 只跑校验器（它只有接受面） | 本仓 `--selftest` 45 条（三类用例齐备）+ 过宿主校验器 `--producer` ⇒ `ok` |
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
- [x] **本仓侧能力层落点**（`symbolic` 的 deps 边指向 pyodide 条目）：**本仓已完成** ——
      `packages/symbolic.json` 的 `depends: ["pyodide"]` ⇒ `--emit` 出的 `symbolic` 条目
      `deps == ["pyodide"]`（字面量由宿主 `mail/010` 确认）；`--selftest` 加 3 条断言
      （有边 / 无边不臆造 / 不出现 `needs`）。悬案 `questions/02` 已结案。
      ⚠️ 宿主侧原有一条**同义硬编码**（`forge-catalog.py` 的 `if p["name"] == "symbolic"`）——
      已在 `mail/011` 请它删掉（本仓的边数据驱动，可接替它）。
