# 悬案 07：GitRoll 第三轮（2026-11-12）181 条明细的对账与清偿计划

**Status:** needs-triage
**Raised:** 2026-11-12（Shirone-Theme wo-u 通报：质量门 Passed，bugs 5 · vulns 0 · smells 176）
**Raw:** `/tmp/gitroll-round3/Octave-Extra-Content.json`（181 条）+ `gitroll.io` scan `crGinmbPFlzUYj7LjFWm`
**Settling:** `set -a; source reflect-hooks/Einfacht.env; set +a; python3 zreflect/registry.py --run commit` + 五工具自证全绿，且 GitRoll 下轮 own 真代码 unused/duplicated 批量清偿后计数下降 ⇒ P2 清偿结案；误报清单（5 条 BUG 型 + 2 BLOCKER 夹具）是**长期记录**不结案——它们是上游/扫描器的判据形状问题，已反哺 Einfacht #40（五仓联合证据），上游处置后此处同步记。

## 对账构成（逐类核源码，2026-11-12）

| 归属 | 条数 | 处置 |
|---|---|---|
| **vendored zreflect/**（逐字等于上游 `0040c7e`） | 123（CRITICAL 89 / MAJOR 22 / MINOR 10 / BLOCKER 2） | **归上游，不代修**（vendored 纪律）；2 BLOCKER（facts.py:1051 / knobs.py:758 always-return-same-value）核过：自证 harness 夹具函数，恒定 rc 是断言契约本体，**误报** |
| **tools/archive/**（已退役） | 11 | 接受不修（历史工具，README 已标注） |
| **own 真代码** | 47 | 分三类：**误报 5+**（见下）/ **择机清偿**（literals、unused）/ **签名稳定性**（明说） |

## 5 条 BUG 型全部核为误报（复跑方式在旁）

1. `registry.py:917-919` identical-subexpr ×3 —— **`never_falsifiable` 的反向自证夹具**（`shapes = {"or_true":…, "self_compare": lambda: y == y, …}`），故意写的恒真/恒假样本是闸门的牙齿。
2. `runner.py:299` float-eq —— `default_timeout() == 10.0`，语义判据（配置解析出确切值），非数值计算比较。
3. `check_envfile.py:70` regex-precedence —— `^(?:["\'])|(?:["\'])$` 分组已显式；行为逐字符验证与注释声明等价（strip 仅首尾引号）。
4. `mail-read.py:124` BLOCKER always-return-same-value —— `cmd_list` 两路径（空/非空）本就都成功返回 0，是「列出动作无失败态」，非逻辑错误。
5. `runner.py` 其余 BLOCKER 同族（自证夹具）。

## 真改进项（清偿计划，不与 vendored 混）

- **P2**：`tools/make-manifest-v4.py:185-188` 四个未用局部变量（自证残留）+ `compare-release-payloads.py` 3 个未用 probs + `forge-shelf.py:225` —— 一次小清偿批，跑全套自证护行。
- **P3（明说不修）**：`forge-shelf.py:115 derive_form(kinds)` / `:352 candidate_rows(e, octave)` 未用参数 = **签名稳定性**（调用方传语义轴，函数体当前常值实现——`form:"pkg"` 是本仓唯一形态，参数保留语义位）；`make-manifest-v4.py` 101 条 duplicated-literal 大头在自证字符串，清偿收益低；`check-release-v4.py` 认知复杂度 3 条是校验器逐条判据的结构（拆函数会破坏 V1-V10 对照阅读）。
- **P3**：`make-manifest-v4.py:500` identity-check-always-True —— `os.makedirs(...) is None else None` 那行是自证里「先造空目录再断言失败」的技巧写法，可读性弱但行为正确；随 P2 批顺手改写。
- **P0/P1**：无 —— vulns 0、真 BUG 0（5 条全误报）。

## Settling

P2 批落地后：`set -a; source reflect-hooks/Einfacht.env; set +a; python3 zreflect/registry.py --run commit` 全绿 + 5 工具自证全绿 + GitRoll 下轮 own 真代码 unused 数降为 0 ⇒ P2 结案。误报清单（5 条 BUG 型）不结案——它们是上游/工具的判据形状问题，记录在此防下轮再骗一次。
