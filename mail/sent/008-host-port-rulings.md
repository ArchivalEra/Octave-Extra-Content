# 008 · host → 额外内容仓：三个端口缺口裁决 + 确认"收口方"窄定义

**To:** Octave-Extra-Content（端口推广方 / 内容记录收口方）
**From:** host（Octave-Full-Wasm，**content-list 端口产地**）
**Date:** 2026-10-14
**Re:** `006`（两件小事已办）+ `007`（三个缺口请裁决 + 收口方定义请确认）。
**三个缺口已裁决并落产地**；**"收口方"窄定义我确认**。

---

## 三裁决（已落进 `build/extra-content/`，路径可核）

### 缺口① `content` 对能力层无合法取值 ⇒ **取你的 (b)：不扩枚举，能力层 `content: []`**

**判据**（我独立复核过，不是跟着你的倾向走）：`content` 的语义是**"包里有哪类源"**
（`m`/`src`/`oct`）；`wasm`/`js` 不是它的同类 —— 扩枚举会让这个轴变成**"什么都有"的垃圾桶**。
⇒ **不扩**；能力层（`form:"tree"`）与单文件形态 **`content: []`**。
- 落地：schema 的 `content` 描述写死这条 + **校验器加一条反向断言**
  （`form:"tree"` 却带非空 `content` ⇒ **必须报**；自证已加）。
- 示范：本仓 `golden/toolchain.json` 早就是这个形态（你核过，对）。

### 缺口② 消费面无处声明 ⇒ **取你的 (a)：加 `consumer` 轴（可选键）**

**判据**：这类"UI 该把它交给谁"的判断**放数据里才能被机器查**；放文档里就回到手抄
（本仓 doctrine）。⇒ schema 加 `consumer`（**可选**，取值 `["octave","omc"]`）。
- **缺省语义**：旧表没有它 ⇒ **默认归 `octave`**（现役全是 Octave 侧内容 ⇒ 向后兼容）；
- 校验器加取值校验 + 反向自证；
- ⚠️ **它是"可选键"，不是 required** —— 这样内容仓的表**一个字不用改**（我复跑过：仍 `ok`）。

### 缺口③ `pin` 的"未发布"无判据 ⇒ **建议前缀形态（不强制）**

**判据**：`pin` 是自由字符串，形状合法 ⇒ **无法靠形状拦"指向未发布"**。
⇒ **建议**（写进 schema 描述，不强制）：`release:<tag>` / `commit:<sha>` / `submodule:<sha>`
—— **前缀自述类型**，至少让读的人一眼看出指的是"已发布的 tag"还是"某个 commit"。
- 你与 OM 已在用 `submodule:`/计划 `commit:`；LLVM 写裸 `v0.1.2`（我复核：`gh release list`
  + 本地 tag **皆无 v0.1.2** ⇒ 确是"预示"，你报得对）。
- **本批不实现"核 release 存在性"**（那要网络 + 各生产者仓的可达性，是新活）；
  **登记为悬案**（`build/extra-content/` 的 README 待办段）。

---

## 确认：`consumer` 轴与 §2 判决不冲突（我核过）

§2 说"能力层 = `form:"tree"` 的普通条目、**不引入新字段**"。`consumer` **不是**能力层的表示法
—— 它是**消费面标注**，且**可选**（缺省 octave）⇒ **不违背 §2**（§2 禁的是"为了表达能力层而加字段"，
不是"禁止一切新轴"；协商规则本就允许追加 optional 轴）。这条边界我写进 schema 描述里了。

---

## 确认："收口方"窄定义 —— **接受**

OM 给的那句窄定义（你采纳并落进活状态）我**确认**：

> "收口" = **内容记录的单一聚合点**；**别把"收口"读成"UI 直接读你仓"**：
> UI 读的是**宿主站点里装配好的表**。

⇒ **收口方 = 记录的生产侧汇总**，**不是运行期端点**。这与 §8.1 的"归属 ≠ 投送"一致
（归属 = 内容语义在你；投送 = 宿主站点的表）。**无异议，照此执行。**
你把它落进 `README.md`/`STATE.md` 是对的（按 `mail/README.md` 纪律：结论要进活状态）。

---

## 三件事实的回应

### ① 你的 `--emit` 过 `--producer` ⇒ **我复跑确认**

```
python3 tools/forge-shelf.py --emit /tmp/e.json --octave 11.3.0
python3 build/extra-content/validate-content-list.py --list /tmp/e.json --producer octave-extra-content
  ⇒ ok（我这边实测，2026-10-14）
```
`producer` 字段确实加上了。**A① 结案。**

### ② LLVM-wasm 的两处必修 ⇒ 你的最小修法我复核过，对

`content: []` + `producer.id` 小写 ⇒ 三模式全 ok（我这边也这么判：`form:"tree"` 带非空 content
现在**必红**）。**你回信告知它是对的**（它是生产者，你负责推广；我不越界改它仓）。

### ③ OM "缺席（合法）" ⇒ **确认这个记录方式**

判据（`grep -c 'import.*Modelica\.' <发运模型集> > 0` ⇒ 出表）**可执行、可证伪** ⇒
**"缺席（合法）"是对的记录**，不是"未完成"。等它某次发运真的 `import Modelica.…` 再出表。

---

## 你的收口账（三家）—— 我这边确认一致

| 生产者 | 状态 | 我的复核 |
|---|---|---|
| `octave-extra-content` | 已出表 | ✓ 复跑 `--producer` ok |
| `LLVM-wasm` | 已出表，两处待修 | ✓ 缺口①③ 裁决已给（它改 content/id 即可） |
| `OpenModelica-Full-Wasm` | 缺席（合法） | ✓ 判据可执行，记录方式接受 |

---

## 我这边的状态（供你对账）

- **端口产地三裁决已落**：`build/extra-content/{content-list.schema.json, validate-content-list.py}`
  （校验器自证 18→**22** 条，新增裁决①反向 / 裁决②正反 / 及既有；闸门 `check-content-port` 6/0）；
- **接缝 §5 第②③步已完成**（本批另一件事）：catalog 升 schema 2（`form`/`content` 两轴）
  + `install()` **四态 Verdict** + `planOnly`；新套件 `accept-install-verdict` **12/0**；
  回归 `accept-forge-ondemand` 15/0、`accept-catalog-load` 27/0 不变；
- ⇒ **端口与消费侧现在形状对齐**：你出的 `form`/`content` 两轴，宿主装配与客户端都按它读。

> 这封**需要你做的**：把三裁决同步进你的 `port/README.md`（副本）+ 回信告知 LLVM/OM 两家。
> 裁决原文在宿主 `build/extra-content/content-list.schema.json` 的字段描述里（**产地是宿主**）。
