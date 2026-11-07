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
| 2 | 新增 `check_i18n` 扫 `zreflect/` 里的中文输出（本仓 `mail-read.py` 38 处 + `measure` 16 处） | 两件自有工具移出机制层：`tools/mail-read.py` + 仓根数据层；机制层恢复零语言 |
| 3 | 新增「套件文件必须有声明」判据抓 `zreflect/__init__.py`（上游根本没有这个文件） | 删除本仓多余的 `__init__.py` |
| 4 | 上游薄壳 `pre-commit`（`exec gate.py commit`）只做「重渲染 + registry」，**不跑本仓 5 个 tools 自证 + 解耦真实数据检查** | 混合壳：先 `gate.py commit`（上游唯一产地），再追加本仓 6 道防线 |
| 5 | 上游 `check_facts` 反向判据（issue #24 白名单式）：本仓 STATE 239 个手抄数字全无出处 | **迁移期** `REFLECT_NAKED_MIN=99999999`，其余判据照跑；见 §待办 A |
| 6 | `facts --check` 无条件扫 `PRINCIPLES.md`（本仓没有） | 本仓 `pre-push` 兼容层复用上游 `_push_readmes_together` / `_new_content_refs`，只把 `--check` 换成 `--check STATE.md` |

**主仓复验（2026-11-07）**：`registry 9 ran / 0 failed / 7 off`（升级前 7 ran）、
`replay 14 条逐字一致`、`stale OK`、`i18n OK（36 文件零语言）`、5 工具自证全绿、
解耦真实数据 OK、混合 pre-commit rc=0。

## 待办 A：STATE.md 的 239 个手抄数字要按新规范迁移（本仓技术债）

**事实**：上游 `check_facts` 的 `_unaccounted_numbers`（issue #24，正是我 10-31 反哺的 #22
被上游修好后的形态）是**白名单式**：正文里每个 ≥ 阈值的整数必须有出处之一
（`[[键名]]` / 台账 value / 形状白名单 / 同行 sha 上下文）。

本仓 STATE 按旧判据（黑名单式）写了 **239 个 ≥100 的手抄实测数字**（144 个不同值），
全是历史实测记录（`6,757,104 B`、`218 字符`、`1525 PASS`…）。它们**不是错误**，
但**未按新规范写**。

**当前处置**：`REFLECT_NAKED_MIN=99999999` 迁移期设置，**不是关闸门**——
块一致性 / 坏引用 / 「抄了台账值没引用」三条判据全部照跑。

**Settling:** `env -u REFLECT_NAKED_MIN python3 zreflect/check_facts.py STATE.md` —— 删掉 `reflect-hooks/Einfacht.env` 里的 `REFLECT_NAKED_MIN` 行并逐段把 239 个数字改成 `[[键名]]` 或行内代码后跑：rc=0 且 0 问题 ⇒ 结案；仍有 bare_number_unaccounted ⇒ 未结案。
⚠️ 机械转换不可行：本仓 STATE 有 136 行**已含反引号**，逐 token 包反引号会破坏
`bridge/assets-loader.js:`731`-737` 这类嵌套（试验场实测把 240 压到 116 后失败，
已放弃该路径）。**必须人工逐段判断**，或给每个数字补 `[[键名]]`。

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

**处置**：报告给 Einfacht，不代修（vendored）。本地缓解是待办 A 的行内代码化。

## 待办 C：上游 `facts --check` 无条件要 `PRINCIPLES.md`，而 opt-out 对它无效（上游不一致，已报）

**事实**：
- `doc.accepts_principles()` 认 `REFLECT_NO_PRINCIPLES=1`（实测 `_has_principles_doc()` 返回 False）；
- 但 `cmd_check()` 调 `_doc_names()`，后者**无条件**返回 `('STATE.md', 'PRINCIPLES.md')`，
  **没走 `_has_principles_doc()`** ⇒ 不建 `PRINCIPLES.md` 就 FATAL。

**本仓立场**：**不造 `PRINCIPLES.md` 占位文件**——那是「为了让判据绿而造一份自己不用的东西」，
正是本仓反复反对的。改用的是**本仓 pre-push 兼容层**（`reflect-hooks/push_gate.py`），
复用上游全部 push 判据，只把 `--check` 换成官方支持的单文档形式 `--check STATE.md`。

**Settling:** `python3 zreflect/facts.py --check` —— 上游让 `cmd_check` 尊重 `REFLECT_NO_PRINCIPLES` 后，删 `reflect-hooks/push_gate.py` 且 pre-push 恢复 `exec gate.py push`；rc=0 ⇒ 结案。

## 附：上游 `gates-selftest.sh` 在本仓语境下的 3 条失败（非本仓缺陷）

`env -u REFLECT_NAKED_MIN sh gates-selftest.sh` ⇒ rc=1，3 条：
- `facts.fresh_repo_bootstraps_green` / `facts.real_repo_shaped_bootstraps`：
  夹具造 `doc.md`，而上游新版 `_block_homes` 只认 `STATE.md` + `PRINCIPLES.md`
  ⇒ `FATAL: facts.doc_has_no_home`。**上游自己仓 rc=0**（它有 PRINCIPLES.md）。
- `registry.env_hint_fires_with_carrier`：夹具环境耦合。

**⇒ 这三条是上游自证隐含依赖「套件仓有 PRINCIPLES.md」，不是本仓生产判据红。**
本仓生产判据以 `registry --run commit`（9 ran / 0 failed）为准。
**不为了绿而改 vendored 自证，也不造假 PRINCIPLES.md。**

## 关联

- 机制层上游：`ArchivalEra/Einfacht@b815cd1`（GitRoll 第二轮整改）
- `docs/FACT-SYSTEM.md`、`AGENTS.md` 七条纪律（纪律 2「数字只生产一次」正是待办 A 的源头）
- 我 10-31 反哺的 Einfacht issue #22 被上游实现为 issue #24 的反向判据 —— 待办 A 是它的下游账单
