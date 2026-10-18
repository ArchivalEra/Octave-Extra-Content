#!/usr/bin/env python3
# Octave-Extra-Content — **事实台账入口（兼容壳）**
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# 为什么需要这个壳（2026-10-18，host mail/035 更正后加）：
# `zreflect/facts.py` 的默认台账名是仓库根的 `FACTS.json`，而本仓台账在
# `build/FACTS.json`。**裸跑 `zreflect/facts.py`（先量测）会把野文件写到仓库根**
# —— 实测：worktree 里 `env -u REFLECT_FACTS python3 zreflect/facts.py`
# 写出根 `FACTS.json`（4161 字节、13 条—— 一份与真台账并存的第二真值）。
# 之前"没写盘"只是执行顺序的巧合（先 --render-doc ⇒ _load_or_die 读失败先退出），
# 不是防护（host 复现 + 本仓 worktree 复现，Einfacht #20 形态②/③ 家族）。
#
# 壳只做一件事：给手工直跑补上本仓默认旋钮（与 reflect-hooks/Einfacht.env 同口径），
# 使"不带环境变量直接跑"与钩子一致。真正干活的只有 zreflect/facts.py。
# 老习惯 `python3 zreflect/facts.py …` 照旧能用（上游机制不变），但**本仓的正确
# 入口是本壳**；Einfacht #15 B4 若上游化 run-gates 包装，本壳与其合一。
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRY = os.path.join(REPO, "zreflect", "facts.py")

# 本仓默认口径（reflect-hooks/Einfacht.env 是钩子的权威来源；这里给手工直跑兜底）
DEFAULTS = {
    "REFLECT_FACTS": "build/FACTS.json",
    "REFLECT_DOC": "STATE.md",
    "REFLECT_MEASURE_MODULE": "measure_extra_content",
}
env = dict(os.environ)
for k, v in DEFAULTS.items():
    env.setdefault(k, v)

sys.exit(subprocess.run([sys.executable, ENTRY] + sys.argv[1:],
                        cwd=REPO, env=env).returncode)
