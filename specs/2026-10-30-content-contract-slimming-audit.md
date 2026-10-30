# 内容契约 entry 字段瘦身审计（23 → ?）

> **触发**：用户点令「23 个字段我觉得也是时候掂量一下哪些不需要了」。
> **判据顺序**：①消费端有没有读它（实测 grep UI 源码）→ ②生产端有没有写（实测 17 条装配态表）
> → ③不写会不会丢语义（deletion test）。
> **两条硬纪律**：**不为未上线的东西做兼容**（v2 兼容层已删）；**这个契约有真实消费者，所以砍字段必须过消费端实测**。

---

## 0. 结论

| 处置 | 数量 | 字段 |
|---|---|---|
| **删** | 1 | `kinds`（`content` 的旧名/兼容视图，消费端 **0 读**、非 required） |
| **保留·记账** | 3 | `license`（0 读但合规必需）、`note`（0 读但写给人看）、`upstream_url`（1 读，出处） |
| **待裁** | 1 | `artifacts`（与 v3 release 概念重叠，等试点后定，见 U-A） |
| **保留（核心）** | 18 | 其余全部 |

**⇒ 23 → 22。只删 `kinds` 一个。**

**★ 本审计的初版判定过一条错的，已撤回**：初版说「`kind` 与 `role` 语义重叠，建议合并」
——**错**。见 §4 的纠正。

---

## 1. 实测依据（两个方向，都可复跑）

### 1.1 生产端：17 条装配态表里各字段的出现率

```
name          17/17 100%    version       17/17 100%    size      17/17 100%
sha256        17/17 100%    url           17/17 100%    deps      17/17 100%
role          17/17 100%    form          17/17 100%    content   17/17 100%
upstream_url  14/17  82%    versions      13/17  76%    description 13/17 76%
links         13/17  76%    kinds         13/17  76%    artifacts  5/17  29%
consumer       4/17  24%    note           4/17  24%    kind       2/17  12%
arch           2/17  12%    license        1/17   6%    files      1/17   6%
```

### 1.2 消费端：UI 源码里读取该字段的文件数

```
name 16 · size 13 · content 11 · files 8 · version 6 · url 6 · kind 6 · arch 6
sha256 5 · form 4 · versions 4 · deps 3 · description 3 · consumer 3 · role 2 · links 2
upstream_url 1 · artifacts 1
★ kinds 0 · note 0 · license 0
```

**⇒ `kinds` / `note` / `license` 消费端零读取。**

---

## 2. 删：`kinds`（13/17 有，0 读）

**它是 `content` 的旧名（兼容视图）。** schema 自己写着「旧消费者照读；新代码用 content」。

**判据**：
- 消费端 **0 个文件**读 `kinds`；
- 生产端 13/17 有它，**纯粹因为历史**（`--emit` 还带着）；
- **两份同义数据 = 两处漂移风险**（我们为 `sha256` 两处写漂移打过官司）。

**处置**：`--emit` 不再产 `kinds`；schema 标 deprecated 并在下一版删。
**这是"删兼容视图"的教科书案例**——兼容层有价值只在「有旧消费者」，而这里实测没有。

## 3. `license`（1/17 有，0 读）：**不删，但正名为「记账字段」**

消费端 0 读，但**删它会丢语义**——许可台账是**合规义务**，不是功能。
schema 原文已经写明：

> ⚠️ 诚实边界：因此**没有机器判据能核「许可写对了没」**——它是记账字段，
> 不参与 fail-closed（唯一 fail-closed 依据是 sha256）；机器只查**类型**。

**⇒ 保留，但明确它不是运行时字段。** 判据：删了它，将来做合规/分发审查时**没有地方记**。

## 4. ★ `kind` / `role` / `content`：**三个正交轴，一个都不能删**（本节为初版错判的纠正）

**初版判定（错，已撤回）**：「`kind` 与 `role` 语义重叠，`kind:"engine"` 恒等价于
`role:"toolchain"` ⇒ 建议删 `kind`」。

**错在哪**：我从「17 条数据里恰好同值」反推「语义相同」。**那是从数据反推语义**，
而它们同值只是因为**缺省值恰好一致**。

### 4.1 三轴的真实分工（消费端源码实测）

| 轴 | 取值 | 决定什么 | 证据 |
|---|---|---|---|
| **`kind`** | `src` / `pre` / `engine` | **下载身份代数**：arch 是 null / wasm32-wasm64 / lane | UI `downloadTypes.ts:8-10` 逐条写明：`src ⇒ arch=null`、`pre ⇒ arch=wasm32\|wasm64`、`engine ⇒ name=octave\|omc, arch=lane` |
| **`role`** | `package` / `toolchain` / `language-bridge` | **走不走 install** | `PackageManagerPlugin.ts:308` — `role=toolchain` ⇒ `NOT_INSTALLABLE`「由下载管理，不走装载」 |
| **`content`** | `m` / `src` / `oct` | **装载路径** | `PackageManagerPlugin.ts:314` — `content.includes('src')` ⇒ 需 LLVM 现场编译；`oct` ⇒ dlopen；只有 `m` ⇒ 直接装 |

### 4.2 用户的原话（这条最权威）

> **`kind` 肯定要啊，不然 UI 就不需要苦哈哈的做 `m` 只装、源码交 LLVM 编译、
> `oct` 需要 dlopen 那样了，这很明确的属性**

⇒ 这三层装载路径是**内容契约存在的核心价值之一**。`content` 是它的载体，
`kind` 是资产代数，`role` 是安装语义——**三者正交**。

### 4.3 17 条实数据的交叉表（同值 ≠ 同义）

```
name       kind     role             content
cgi        -        package          ['m']
datatypes  -        package          ['m', 'src']     ← 同一 kind，content 不同
llvm-wasm  engine   toolchain        []
matgeom    -        package          ['m']
modelica-  -        package          []               ← 同样 package，content 空
omc        engine   toolchain        []
pyodide    -        language-bridge  []
statistics -        package          ['m', 'src']
```

**判读**：`kind` 缺省的 15 条里，`content` 有 `['m']` / `['m','src']` / `[]` 三种，
`role` 有 `package` / `language-bridge` 两种 ⇒ **三轴各自独立变化，只是 `engine` 那两条恰好同时取到 toolchain。**

## 5. `artifacts`（5/17，1 读）：**保留但待裁**

它记「预编译 `.oct` 逐架构一份」，有 5 条在用，UI 有 1 处读。
**但它与发布契约 v3 的 release 概念重叠**（每个 artifact 是一个发布单位）。
已在 `v3-absorption-audit` §1.3 标为 U-A 待裁。

## 6. 其余字段为什么留（deletion test 一句话）

| 字段 | 删了会怎样 |
|---|---|
| `name` | `deps` 失去指向目标（16 个文件读） |
| `version` | 版本语义消失（`versions[]` 三不变量失去锚） |
| `sha256` | **fail-closed 唯一依据消失**——安全红线 |
| `url` | 不知道从哪取（6 读） |
| `size` | 进度条/预算没了（13 读，闭包计算靠它） |
| `form` | 无法区分 pkg/tree/file（装载路径不同，4 读） |
| `content` | 不知道包里有什么源（11 读！） |
| `deps` | 闭包解析断（3 读） |
| `versions` | 版本选择器无数据（4 读） |
| `description` / `links` | UI 卡片首屏空（3 / 2 读） |
| `consumer` | 车道筛选失效（3 读，`omc` 车道靠它） |
| `arch` | dlopen 兼容性判不了（6 读） |
| `files` | tree 条目下载闭包消失（8 读） |
| `requires` | 平台版本约束丢失（0 条实数据，但语义必要——见下） |
| `upstream_url` | 记账断（1 读） |

**`requires` 特殊**：实测 **0/17 有它**。但它的语义（`'octave (>= 4.0.0)'`）**无处可替**。
**⇒ 建议保留但标注"当前无生产者使用"**——这正是"未来可能需要但今天没数据"的字段，
删了将来要重新加（而加字段有协商成本）。

---

## 7. 我建议的瘦身次序（**不一次做完**）

```
第 1 步（本批做）：--emit 不再产 kinds（消费端 0 读 + 非 required + 纯兼容视图）
第 2 步（等 v3 试点后）：artifacts 与 release 的关系定型（U-A）
第 3 步（不动）：license / note / upstream_url 保留，只在 schema 描述里标注"非运行时"
```

**★ 不做的**：`kind` / `role` / `content` 三轴**一律不动**（§4 已证它们正交且各自有行为判据）。

**`note` 的特别说明**：消费端 0 读，但**它是写给人看的**（"这条为什么这样"）。
**我建议保留**，只标注"运行时字段之外"——删了它，下一个维护者不知道为什么。
（这与 `license` 同族：**人不读 ≠ 该删**。）

---

## 8. 诚实边界

- 生产端统计用的是**装配态表**（17 条），不是 13 个源档案——因为装配态才是消费端看到的形状；
- 消费端统计是 **grep 文件数**，不是调用次数——一个文件里读 10 次也只算 1。
  这是**下界估计**（真实使用只会更多），对「0 读」的判定足够；
- 我**没有**核实 `--emit` 删 `kinds` 会不会破坏宿主校验器（需要跑一次）；
- `kind`/`role` 合并涉及 UI 改动，**我只提议不擅动**。

## 8.1 ✅ 第 1 步已落地（2026-10-30）

`--emit` 不再产 `kinds`。**实测验证（改前/改后对照）**：

```
改前：13 条，13 条带 kinds，宿主校验器 ok
改后：13 条，0 条带 kinds，content 13/13 全在，宿主校验器 **ok**
diff：13/13 条各少一个字段，无新增字段
自证：46 PASS/1 fail（那条断言的正是"kinds 保留"）→ 改成断言"kinds 不再产" → **47/0**
```

**留存**：档案里 `versions[].kinds` **仍保留**——那是 `--probe` 的**探测真值**
（从 tar 内容判 m/oct/src），不是兼容视图。删的是**输出视图**，不是**探测事实**。

## 9. 复跑方式

```bash
# 生产端字段出现率
python3 -c "
import json,collections
c=json.load(open('/mnt/hdd/zcode-projects/Octave-Full-Wasm/site/assets/forge-catalog.json'))
cnt=collections.Counter(k for p in c['packs'] for k in p)
for k,n in cnt.most_common(): print(f'{k:16s} {n}/{len(c[\"packs\"])}')"

# 消费端读取面
cd /mnt/hdd/antigravity-projects/Octave-UI
for f in kinds note license kind role artifacts; do
  echo -n "$f: "; grep -rl "\b$f\b" src/modules/plugins/package/ src/modules/storage/ src/modules/engine/ | wc -l
done
# ⇒ kinds 0 / note 0 / license 0 / kind 6 / role 2 / artifacts 1
```
