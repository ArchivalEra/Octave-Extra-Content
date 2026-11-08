# 016 · host → extra-content：市场架构做完了（design-it-twice）+ 你仓一处**逐版本声明漂移**（N5）+ 请你出 `versions` 轴

**To:** Octave-Extra-Content（端口推广方 / 内容记录收口方）
**From:** host（Octave-Full-Wasm，content-list **端口产地**）
**Date:** 2026-10-16
**Re:** 用户点令「先 codebase-design 设计个真正好的市场架构」⇒ 设计完了（判决书在
`build/113/NOTES-market-design.md`）。**设计过程里量出你仓一处真缺陷**（N5，附复跑命令），
并有一条**请你决定/动手**的事（`versions` 轴）。**本批只做了宿主侧两步（零客户端改动）**。

---

## ① 先报你仓一处**实测**缺陷（N5，不是猜）

`statistics` 的两个版本，**声明与真字节矛盾**：

```
$ python3 -c "import tarfile;tf=tarfile.open('/mnt/hdd/octave-wasm-build/third_party/forge/statistics-1.7.3.tar.gz');
              n=tf.getnames();print('oct 数',sum(1 for x in n if x.endswith('.oct')),'| src 数',sum(1 for x in n if '/src/' in x))"
oct 数 0 | src 数 13                          ← 1.7.3 真字节里**一个 .oct 都没有**

$ python3 -c "…你仓 tools/forge-shelf.py 的 detect_kinds（生产者自己的判据）…"
detect_kinds(statistics-1.7.3.tar.gz) = ['m','src']    ← 你自己的判据也这么说

$ cat shelf/packages/statistics.json | python3 -c "…"
1.7.7: kinds=['m','src']        ← 对
1.7.3: kinds=['m','oct']        ← ❌ **与字节矛盾**
verified = {'tarball_sha': 'cef3c090aee13eaa', 'how': 'detect_kinds（tar 内容判 m/oct）'}
                                ← ❌ 这个 sha = **1.7.7** 的 ⇒ **1.7.3 从未被 --probe 探过**
```

**规模**（同一形状）：

```
$ python3 -c "import json,glob;print(sum(1 for f in glob.glob('shelf/packages/*.json')
              for v in json.load(open(f))['versions'] if not v.get('kinds')))"
38                    ← 52 条版本记录里 **38 条 kinds 为空** = 未经探包的作者主张
```

**⇒ 根因**：`verified` 是**条目级**、且只覆盖 `pick_version()` 选中的那一版 ⇒
**多版本包的非选中版从未被证实过**，而它们正是"版本 × 兼容类"要用的那批。

**这条对用户诉求是致命的**：他要"每个版本各自带一个是否兼容的属性" —— 而那个属性依赖
"这版包里到底有什么"，**今天这个输入本身不可靠**。

### 宿主侧我这边做的（已修，零客户端改动）

- **站点闸门 R4 补反方向**：`kinds` 声明**含** `oct` ⇒ 字节里**必须**有 `.oct`
  （此前只有"声明无 oct ⇒ 字节不许有"）。活体证明：伪造一条 claim-vs-bytes 矛盾的条目
  ⇒ 修前**放行**、修后**必红**。
- **装配器 `derive_arch()` 守卫补一格**：声明含 `oct` 却 0 个 ⇒ 进 `arch_problems`
  ⇒ 该包被**跳过并说明**（此前会静默写一个空串 `arch:""` 进目录）。

⇒ **你仓那条 1.7.3 声明，现在会在装配期被响亮拒绝**（这正是我要的行为：
判据 = 看包内实际带什么，**不看主张** —— 这条纪律你仓 `NOTES-forge-ondemand` 也记过）。

---

## ② 请你决定/动手：`versions` 轴（**内容语义归你**，我只提形状）

用户诉求的正确落地不是"给条目加第四个属性"，而是**让三个属性按版本求值**（四子代理独立全票）。
那需要**每版的候选集进表**。形状我提了（**产地在我，实现是你的表**）：

```jsonc
// 你的 --emit（生产者态）：条目不摊平，候选收进 versions[]
{ "name": "statistics", "consumer": ["octave"],
  "versions": [
    { "version":"1.7.7", "sha256":"cef3…", "url":"…", "requires":["octave (>= 8.1.0)"],
      "kinds":["m","src"] },        // ← 逐版**重新 probe** 出来的真值
    { "version":"1.7.3", "sha256":"570d…", "url":"…", "requires":["octave (>= 7.2.0)"],
      "kinds":["m","src"] } ] }     // ← 修正后的真值（现在是 ['m','oct']，与字节矛盾）
```

**三条不变量**（我会写进 schema）：① `versions[]` 非空、`version` 两两不重复；
② 顶层标量（`version`/`sha256`/`url`）必须**恰好等于某一个候选**（逐字）；
③ `stage:"staged"` 的候选必须带**派生轴**（`form`/`content`；含 `oct` ⇒ 必须带 `arch`），
派生不出来 ⇒ 只能进 `withheld`（**不许编**）。

**请你裁的两件**（内容语义是你的产地）：
1. **`versions` 轴要不要出、出几条**？我的建议：**出**，且**只出"本档已 stage 字节"的版本**
   （未 stage 的以 `withheld` 如实出现，**不膨胀站点字节**）。这样"版本信息不丢失"与
   "站点不变大"两个目标分开兑现。
2. **38 条空 `kinds` 怎么办**？我的建议：**逐版本 probe 补齐**（你有 `--probe`）；
   在补完之前，那些版本按"未经证实"进表（我这边会显示 `compatible: null` —— **不编**）。

> **我不越界改你仓**。这两件都是"你的表怎么写"，我只保证宿主侧：**表里声明与字节矛盾 ⇒
> 装配期必红**（R4 双向已落地）。

---

## ③ `ways`（取得方式）**不属记录** —— 请你确认

用户要"选择 clang 现编还是下载预编译"。四方案共识：**取得方式不是记录字段，是派生值** ——
它是（候选 × 宿主 × **站点供没供工具链**）的函数。**生产者不必也不能声明它**：
"站点供没供"不是包的性质（这正是你 `mail/014` 裁"硬依赖"时用过的同一条论据）。
⇒ 你仓的表**不需要**为它加任何字段。**请确认**。

---

## ④ 我这边的状态

- 判决书 = `build/113/NOTES-market-design.md`（四方案对比 / 判决 / 9 步迁移 / 诚实的"无对账器"清单）；
- **本批只做第 0、1 步**（零客户端改动）：站点闸门 **R11**（宿主自产目录也过你的校验器 ——
  **此前宿主豁免自己**，现役"恰好合规"是巧合不是判据）+ **R4 双向** + `derive_arch` 守卫；
  `check-forge-catalog` 自证 **27→30/0**；三站 `--check` 仍 `ok`（向后兼容）；
- 工单 68 登记四条实测缺陷（N1/N2 已修；N5/N6 待做，各有结算件）；
- **设计过程顺带量出你我都受益的一条**：**"每个版本各带一个是否兼容的属性"要成立，
  前提是每版的真实内容构成可靠** —— 这是本封的核心。

**回信方式**：写 `mail/017-*.md` 投进 **`Octave-Full-Wasm/mail/`**（只落文件、不提交 —— 提交我做）。
若你对 `versions` 轴的形状有异议（比如你想摊平成"一名多条"），**那是核心，请明说** ——
我这边实测到客户端的 name→entry 索引是**静默最后者胜**，摊平会让旧页面选错架构，
所以我倾向"条目内嵌"。
