# 悬案 06：上游 Einfacht b815cd1 升级后的三处结构性不兼容 + STATE 裸数字迁移

**Status:** needs-triage
**Raised:** 2026-11-07（「额叶移除」：机制层整层换成上游 HEAD）

## 背景

2026-11-07 把本仓 `zreflect/`（27 个 py）整层换成上游 `b815cd1`（33 个 py + `lang/` +
9 个新模块），钩子骨架换成上游 `gate.py` 薄壳。试验场（`/tmp/lobotomy`）已验证
**6 处可修不兼容并全部修好**（见下），但留下 **3 处上游结构性问题**，本仓不改 vendored 代码。

## 已修（主仓已落地，全部实测通过）

| # | 不兼容 | 修法 |
|---|---|---|
| 1 | 上游 `facts.py` 不再默认 `measure_extra_content`；不配 `REFLECT_MEASURE_MODULE` 就回落 `measure_example()`（量出空表、掉 14 条 FATAL） | 数据层移到仓根 `measure_extra_content.py`；`Einfacht.env` 显式配旋钮；`build/facts.py` 壳加 `PYTHONPATH=REPO` |
| 2 | 新增 `check_i18n` 扫 `zreflect/` 里的中文输出（本仓 `mail-read.py` **22 处** + `measure` **16 处**，实测 `i18n_cover.bare_text`） | 两件自有工具移出机制层：`tools/mail-read.py` + 仓根数据层；机制层恢复零语言 |
| 3 | 新增「套件文件必须有声明」判据抓 `zreflect/__init__.py`（上游根本没有这个文件） | 删除本仓多余的 `__init__.py` |
| 4 | 上游薄壳 `pre-commit`（`exec gate.py commit`）只做「重渲染 + registry」，**不跑本仓 5 个 tools 自证 + 解耦真实数据检查** | 混合壳：先 `gate.py commit`（上游唯一产地），再追加本仓 6 道防线 |
| 5 | 上游 `check_facts` 反向判据（issue #24 白名单式）：本仓 STATE 239 个手抄数字全无出处 | **迁移期** `REFLECT_NAKED_MIN=99999999`（作用域实测见 §待办 A）；见 §待办 A |
| 6 | `facts --check` 无条件扫 `PRINCIPLES.md`（本仓没有） | 本仓 `pre-push` 兼容层复用上游 `_push_readmes_together` / `_new_content_refs`，只把 `--check` 换成 `--check STATE.md` |

**主仓复验（2026-11-07）**：`registry 9 ran / 0 failed / 7 off`（升级前 7 ran）、
`replay 14 条逐字一致`、`stale OK`、`i18n OK（36 文件零语言）`、5 工具自证全绿、
解耦真实数据 OK、混合 pre-commit rc=0、真实 `git push` 通过。

⚠️ **`gates-selftest.sh` 当前 rc=1（如实记）**，两套失败：
- `source Einfacht.env` 后直接跑 ⇒ `check_facts` 4 条反向自证被 `REFLECT_NAKED_MIN`
  短路，且 harness 的 `rc or` 让后 4 个 section 不执行 ⇒ 只有 1 个 heading。
  修法（AGENTS.md 已改）：`env -u REFLECT_NAKED_MIN sh gates-selftest.sh` 隔离旋钮。
- 即便隔离旋钮，仍有 **3 条上游夹具失败**（见 §附），上游自己仓 rc=0。
  **不造假 `PRINCIPLES.md` 占位，不改 vendored 自证。** 生产判据以
  `registry --run commit` 为准。

## 待办 A：STATE.md 的 239 个手抄数字要按新规范迁移（本仓技术债）

**事实**：上游 `check_facts` 的 `_unaccounted_numbers`（issue #24，正是我 10-31 反哺的 #22
被上游修好后的形态）是**白名单式**：正文里每个 ≥ 阈值的整数必须有出处之一
（`[[键名]]` / 台账 value / 形状白名单 / 同行 sha 上下文）。

本仓 STATE 按旧判据（黑名单式）写了 **239 个 ≥100 的手抄实测数字**（144 个不同值），
全是历史实测记录（`6,757,104 B`、`218 字符`、`1525 PASS`…）。它们**不是错误**，
但**未按新规范写**。

**★ 当前处置的真实作用域（2026-11-07 子代理 review 实测纠正）**：
`REFLECT_NAKED_MIN=99999999` 是**两条判据共用的阈值**（`problems()` 把 `bm` 同时传给
`_copied_fact_problems(f, nlines, bm)` 与 `_unaccounted_numbers(f, bm, nlines)`）：
- `_unaccounted_numbers`（反向判据）被短路 ← 本意
- **`_copied_fact_problems`（旧黑名单：抄了台账值却没写 `[[键名]]`）也被一并短路** ← 非本意
- 块一致性 / 坏引用照跑。

**⇒ 之前写的「其余判据全部照跑」是假描述，已改正。** 当前真实 STATE 239 条全是
`bare_number_unaccounted`，没有 `copied_value` 命中，所以**此刻无实际漏报**；
但判据确实被关了一道，直到待办 A 结案。

**复跑（作用域证据）**：在 STATE 正文注入一句含台账值 `34693729` 的裸抄：
```
REFLECT_NAKED_MIN=100       python3 zreflect/check_facts.py STATE.md  ⇒ facts.copied_value
REFLECT_NAKED_MIN=99999999  python3 zreflect/check_facts.py STATE.md  ⇒ 0 条（判据被关）
```

**Settling:** `set -a; source reflect-hooks/Einfacht.env; set +a; env -u REFLECT_NAKED_MIN python3 zreflect/check_facts.py STATE.md` —— 逐段把 239 个数字改成 `[[键名]]` 或行内代码、删掉 `REFLECT_NAKED_MIN` 行后跑：rc=0 且 0 问题 ⇒ 结案（**两条判据一并恢复**）；仍有 `bare_number_unaccounted` ⇒ 未结案。⚠️ 命令必须先 `source` 才有 `REFLECT_FACTS=build/FACTS.json`，否则 `facts.ledger_missing` rc=2。
⚠️ 机械转换不可行：逐 token 包反引号会破坏 `bridge/assets-loader.js:`731`-737`
这类嵌套（`/tmp/lobotomy` 试验场实测，已放弃该路径）。**必须人工逐段判断**，
或给每个数字补 `[[键名]]`。

## 待办 B：上游 `check_facts` 把千分位逗号数字切成假 token（上游缺陷，已报）

**复现**（上游 `zreflect/check_facts.py`）：

```python
line = "（实测 pyodide：release  6,757,104 B vs"
# _SHAPE_PATTERNS 剥不掉 "6,757,104"
# re.findall(r"(?<![\w.])\d+(?![\w.])", line) ⇒ ['6', '757', '104']
# ⇒ '757' / '104' 被当成「无出处裸数字」报出来
```

`_SHAPE_PATTERNS` 不含 `\d{1,3}(,\d{3})+`，上游 18 条自证**没有覆盖带逗号的数字**
（`--selftest` 18 PASS / 0 FAIL）。这是「判据比它声称的窄」，与本仓 #22 同族。

**处置**：已报告 **Einfacht issue #27 ①**，不代修（vendored）。

**Settling:** `python3 zreflect/check_facts.py --selftest` —— 上游把 `\d{1,3}(,\d{3})+`
加进 `_SHAPE_PATTERNS` **并补一条带逗号数字的自证**后：`6,757,104` 被整段剥掉
（`re.findall` 不再返回 `['6','757','104']`）且该新用例 PASS ⇒ rc=0 结案；
仍切成三段 ⇒ 未结案。**这条独立于待办 A**：A 结案（数字被行内代码豁免）后
逗号切分就再也测不出，所以 B 必须靠上游自证单独结算，不能被 A 吞掉。

## 待办 C：上游 `facts --check` 无条件要 `PRINCIPLES.md`，而 opt-out 对它无效（上游不一致，已报）

**事实**（已报 **Einfacht issue #27 ②**）：
- `doc.accepts_principles()` 认 `REFLECT_NO_PRINCIPLES=1`（实测 `_has_principles_doc()` 返回 False）；
- 但 `cmd_check()` 调 `_doc_names()`，后者**无条件**返回 `('STATE.md', 'PRINCIPLES.md')`，
  **没走 `_has_principles_doc()`** ⇒ 不建 `PRINCIPLES.md` 就 FATAL。

**本仓立场**：**不造 `PRINCIPLES.md` 占位文件**——那是「为了让判据绿而造一份自己不用的东西」，
正是本仓反复反对的。改用的是**本仓 pre-push 兼容层**（`reflect-hooks/push_gate.py`），
复用上游全部 push 判据，只把 `--check` 换成官方支持的单文档形式 `--check STATE.md`。

**Settling:** `python3 zreflect/facts.py --check` —— 上游让 `cmd_check` 尊重
`REFLECT_NO_PRINCIPLES` 后，删 `reflect-hooks/push_gate.py` 且 pre-push 恢复
`exec gate.py push`；rc=0 ⇒ 结案。
**反向判据（上游未改时必须红）**：`REFLECT_NO_PRINCIPLES=1 python3 zreflect/facts.py --check`
当前实测 `rc=2` + `facts.doc_missing_check(path=…/PRINCIPLES.md)`；若上游没改而它
变 rc=0，说明有人造了占位文件或改了判据 —— 那不算结案，要查。

## 附：上游 `gates-selftest.sh` 的两套失败（2026-11-07 子代理 review 后重测纠正）

**★ 之前把两套失败混成一套了，实测区分如下：**

**套 1（由本仓迁移期旋钮引起，已用命令隔离）**：`source Einfacht.env` 后直接
`sh gates-selftest.sh` ⇒ `check_facts.py --selftest` 的 4 条反向自证被
`REFLECT_NAKED_MIN=99999999` 短路（14 PASS / 4 FAIL），且 harness 的 `rc or`
让后 4 个 section 不执行（只有 1 个 heading）。**`env -u REFLECT_NAKED_MIN`
后这 4 条全过**（18 PASS / 0 FAIL）。AGENTS.md 已把复跑命令改成隔离形式。

**套 2（上游夹具自身，隔离旋钮后仍在）**：`env -u REFLECT_NAKED_MIN sh gates-selftest.sh`
⇒ rc=1，3 条，**两条成因不同**：
- `facts.fresh_repo_bootstraps_green` / `facts.real_repo_shaped_bootstraps`：
  夹具造 `doc.md`，上游 `_block_homes` 只认 `STATE.md` + `PRINCIPLES.md`
  ⇒ `FATAL: facts.doc_has_no_home`。**上游自己仓 rc=0**（它有 PRINCIPLES.md）。
  ⇒ 隐含依赖「套件仓有原则文档」（已报 **Einfacht issue #27 ③**）。
- `registry.env_hint_fires_with_carrier`：**不是** PRINCIPLES 成因 —— 夹具造临时
  `Einfacht.env` 写 `REFLECT_FACTS=FACTS.json`，却没清掉父进程继承的
  `REFLECT_FACTS=build/FACTS.json`，于是 `env_hint()` 认为旋钮已配、返回 None。
  实测 `env -i PATH="$PATH" HOME="$HOME" GATE_REPO=$PWD python3 zreflect/registry.py --selftest`
  ⇒ rc=0。**这是下游 env 载体耦合**，此前笼统归成「PRINCIPLES」是错的。

**⇒ 两套都不是本仓生产判据红。** 生产判据以 `registry --run commit`
（9 ran / 0 failed）为准。**不为了绿而改 vendored 自证，也不造假 PRINCIPLES.md。**

## 关联

- 机制层上游：`ArchivalEra/Einfacht@b815cd1`（GitRoll 第二轮整改）
- `docs/FACT-SYSTEM.md`、`AGENTS.md` 七条纪律（纪律 2「数字只生产一次」正是待办 A 的源头）
- 我 10-31 反哺的 Einfacht issue #22 被上游实现为 issue #24 的反向判据 —— 待办 A 是它的下游账单
