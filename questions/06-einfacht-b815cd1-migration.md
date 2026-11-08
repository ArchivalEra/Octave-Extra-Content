# 悬案 06：Einfacht b815cd1→351dc7b 升级账 + STATE 裸数字迁移

**Status:** needs-triage
**Raised:** 2026-11-07（「额叶移除」：机制层整层换成上游 HEAD）
**Updated:** 2026-11-08（再升级 351dc7b：B/C 结案、夹具 3→2、根因定位）

## 背景

2026-11-07 把本仓 `zreflect/`（27 个 py）整层换成上游 `b815cd1`（33 个 py + `lang/` +
9 个新模块），钩子骨架换成上游 `gate.py` 薄壳，**6 处可修不兼容全修**（见下表）。
2026-11-08 再整层升到上游 `351dc7b`（试验场 `/tmp` 先行验证；上游工作区当时有未提交
改动，故用 `git archive 351dc7b` 只取已提交内容）。

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

⚠️ **`gates-selftest.sh` 当前 rc=1（如实记）**，两类失败：
- `source Einfacht.env` 后直接跑 ⇒ `check_facts` 4 条反向自证被 `REFLECT_NAKED_MIN`
  短路，且 harness 的 `rc or` 让后 4 个 section 不执行 ⇒ 只有 1 个 heading。
  修法（AGENTS.md 已改）：`env -u REFLECT_NAKED_MIN sh gates-selftest.sh` 隔离旋钮。
- 即便隔离旋钮，仍有 **2 条上游夹具失败**（vendored env 载体污染，根因已定位，
  见 §附），上游自己仓 rc=0（它没有宿主 env 文件）。
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

## 待办 B：上游 `check_facts` 把千分位逗号数字切成假 token —— **已结案（2026-11-08）**

**结案**：上游 `b580052` 把 `\d{1,3}(,\d{3})+` 加进 `_SHAPE_PATTERNS`（实测
`zreflect/check_facts.py:98`）。升级落地后复跑 Settling：含 `6,757,104` 的正文
`facts.ok` 不再切成三段；`check_facts --selftest` **19 PASS / 0 FAIL**（18→19，
新增的正是带逗号数字的用例）。

**Settling:** `python3 zreflect/check_facts.py --selftest` —— 上游把 `\d{1,3}(,\d{3})+`
加进 `_SHAPE_PATTERNS` **并补一条带逗号数字的自证**后：`6,757,104` 被整段剥掉
（`re.findall` 不再返回 `['6','757','104']`）且该新用例 PASS ⇒ rc=0 结案；
仍切成三段 ⇒ 未结案。**这条独立于待办 A**：A 结案（数字被行内代码豁免）后
逗号切分就再也测不出，所以 B 必须靠上游自证单独结算，不能被 A 吞掉。

## 待办 C：上游 `facts --check` 无条件要 `PRINCIPLES.md` —— **已结案（2026-11-08）**

**结案**：上游 `b580052` 修了 #27②：`_doc_names()` 现在**尊重**
`doc.accepts_principles()`（`REFLECT_NO_PRINCIPLES=1` ⇒ 只查 STATE.md；
docstring 明说连 `gate._prepare(push)` 的 pre-push 恒红一起修）。
升级落地后实测：`python3 zreflect/facts.py --check`（无 PRINCIPLES.md）**rc=0**；
反向判据已失效属预期（判据本身修好了，不存在「没改却变绿」情形——机制读过源码确认）。

**落地动作（按本节原 Settling 执行）**：`reflect-hooks/push_gate.py` **已删**；
`reflect-hooks/pre-push` **恢复上游薄壳** `exec gate.py push "$(git rev-parse --show-toplevel)"`
（上游 run()：env 插件 → `facts --check` → registry → README 同批，与本仓兼容层等价）；
`Einfacht.env` 的 `REFLECT_NO_PRINCIPLES=1` **保留**——它不再是 workaround，
而是「本仓不接纳原则文档」的正式声明输入。

**Settling:** `python3 zreflect/facts.py --check` —— 上游让 `cmd_check` 尊重
`REFLECT_NO_PRINCIPLES` 后，删 `reflect-hooks/push_gate.py` 且 pre-push 恢复
`exec gate.py push`；rc=0 ⇒ 结案。
**反向判据（上游未改时必须红）**：`REFLECT_NO_PRINCIPLES=1 python3 zreflect/facts.py --check`
当前实测 `rc=2` + `facts.doc_missing_check(path=…/PRINCIPLES.md)`；若上游没改而它
变 rc=0，说明有人造了占位文件或改了判据 —— 那不算结案，要查。

## 附：上游 `gates-selftest.sh` 的夹具失败 —— **已清零（2026-11-08）**

**351dc7b 落地后 3 → 2，同日上游 `0040c7e` 修复后 2 → 0**：

- `registry.env_hint_fires_with_carrier`：`b580052` 修掉（env 语境自证）。
- `facts.fresh_repo_bootstraps_green` / `facts.real_repo_shaped_bootstraps`：
  **我 2026-11-08 定位真根因并报 [Einfacht #34]**（vendored 形态特有）：夹具的
  `_copy_suite_into()` 把宿主仓整个 `reflect-hooks/`（含带宿主旋钮的
  `Einfacht.env`）拷进「全新仓」，宿主 env 遮蔽夹具自己的 env ⇒ 夹具里
  `check_facts` / `check_readme_sync` 按宿主的 `REFLECT_DOCS` 跑，全新仓只有
  STATE.md ⇒ 红。
  **实证**：把 `reflect-hooks/Einfacht.env` 临时挪走再跑
  `python3 zreflect/facts.py --selftest` ⇒ **16 PASS / 0 FAIL 全过**（挪回原状）。
  纯上游仓（无该 env 文件）同自证 16/0。b815cd1 基线同样两红 ⇒ 非升级回归。
  **上游同日修复**（`0040c7e`）：夹具按名册拷 `reflect-hooks/` 时
  **排除 `Einfacht.env`**。落地后本仓
  `env -u REFLECT_NAKED_MIN sh gates-selftest.sh` ⇒ **rc=0，35 闸门自证全绿，
  facts.py 自证 17/0**。#34 可关。

⚠️ **复跑判据必须用干净 shell**（AGENTS.md 命令原样单独跑）：把
`source Einfacht.env` 与壳写进同一条命令链，会把宿主旋钮（`REFLECT_NO_PRINCIPLES`
等未被夹具覆写的）泄进 harness 夹具 ⇒ `rename_failed` 假红（2026-11-08 实测踩过：
文件、代码、与上游仓逐字无差，差的只是进程 env）。

**历史记录（b815cd1 时期的三条分类，留痕）**：当时两条 facts bootstrap 失败
被归因为「隐含依赖 PRINCIPLES.md」+ env_hint 载体耦合。2026-11-08 重测：
前者归因不准（真根因是上面的 env 载体污染，与 PRINCIPLES 无关）；
env_hint 那条已被 b580052 修复。

## 关联

- 机制层上游：`ArchivalEra/Einfacht@b815cd1`（GitRoll 第二轮整改）
- `docs/FACT-SYSTEM.md`、`AGENTS.md` 七条纪律（纪律 2「数字只生产一次」正是待办 A 的源头）
- 我 10-31 反哺的 Einfacht issue #22 被上游实现为 issue #24 的反向判据 —— 待办 A 是它的下游账单
