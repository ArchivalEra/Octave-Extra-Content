#!/usr/bin/env python3
"""Octave-Extra-Content — **本仓的数据层**（Einfacht 机制层之上的"你的部分"）。

Einfacht 的 `zreflect/facts.py` 只提供**机制**（守卫 / 渲染 / 收尾），
`measure_example()` 是占位。这里放本仓真正要量的东西：**货架档案的规模事实**、
**工具自证通过数**、**供给配方引用的上游字节身份**。全部照旧：每条带复跑命令 + 出处。

⚠️ 本模块**自包含**：不 import 宿主仓的任何东西（那是另一棵仓）。
⚠️ 采集器纪律（`zreflect/collect.py` 五条原则）逐条遵守：
   · 只读**持久盘**产物，不跑服务、不碰网络（pre-commit 里不该依赖"某个东西正在跑"）；
   · **不引入会自己在变的输入** —— 本仓 tip（`git rev-parse HEAD`）**故意不进台账**：
     它每提交都变，进了 ⇒ 同一个提交里 `--check` 永不收敛、复跑闸门永远红
     （FACT-SYSTEM.md §4 建议表里那条 `content_pin` 与 collect.py 原则 2 冲突，
      按机制纪律取后者；要引用 tip 就在正文写命令，不写台账）；
   · **读不到就明说**：上游字节不在本机（换机器 / 没挂盘）⇒ 那条事实**不写**，
     不许用 0 冒充"已量"（0 是一个数字，会被人当结果引用）；
   · 贵的测量有缓存：本仓事实都是廉价磁盘读，无此需要。
"""
import glob
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ledger import fact                                    # noqa: E402
from gate import module_meta                               # noqa: E402

# ★ C5：本仓数据层也必须在平台名册里声明自己，否则 registry 报 undeclared。
#   selftest=False：它是**数据**（量什么、怎么量），机制的自证在 zreflect/ 那批。
MODULE = module_meta("本仓数据层", "量本仓的货架/工具/配方上游字节（数据 vs 机制分离）",
                     selftest=False)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配方引用的上游字节（**持久盘**上的 provision 产物；权威事实在生产者的 manifest）。
# 可用环境变量覆盖（换机器）；读不到就**不写**那条事实（宁缺勿假）。
LLVM_BUNDLE = os.environ.get(
    "LLVM_BUNDLE", "/mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz")
PYODIDE_CORE = os.environ.get(
    "PYODIDE_CORE", "/mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2")


def _one(cmd):
    """跑一条裸值命令，返回 stdout.strip()（读不到 ⇒ None，调用方决定写不写）。"""
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           cwd=REPO, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if p.returncode != 0:
        return None
    return p.stdout.strip()


def measure():
    """量一遍全部事实（本仓的策略/数据）。守卫与写盘由 zreflect/facts.py 的平台负责。"""
    facts = {}

    # ── 货架档案规模（**目录侧**事实，从磁盘量，不猜）────────────────────────────
    #   每包一文件（packages/<名>.json）；规模 = 包数 / 已验证数 / 版本条目总数 /
    #   含异架构预编译 .oct 的包数（那是"装上必须重编"的那一档，见 README 的 kinds 三态）。
    n_packs = len(glob.glob(os.path.join(REPO, "packages", "*.json")))
    if n_packs:
        facts["shelf_packs"] = fact(n_packs, "ls packages/*.json | wc -l",
                                    "packages/", "货架上的包档案数（每包一文件）")
    n_ver = _one("grep -l '\"verified\": {' packages/*.json | wc -l")
    if n_ver is not None:
        facts["shelf_verified"] = fact(int(n_ver),
                                       "grep -l '\"verified\": {' packages/*.json | wc -l",
                                       "packages/",
                                       "已验证（--probe 实测过）的包数；未验证的默认不上架")
    n_versions = _one("python3 -c \"import json,glob;print(sum(len(json.load(open(f))"
                      "['versions']) for f in glob.glob('packages/*.json')))\"")
    if n_versions is not None:
        facts["shelf_versions"] = fact(int(n_versions),
                                       "python3 -c \"import json,glob;print(sum(len("
                                       "json.load(open(f))['versions']) for f in "
                                       "glob.glob('packages/*.json')))\"",
                                       "packages/", "全部包档案里的版本条目总数")
    n_oct = _one("python3 -c \"import json,glob;print(sum(1 for f in glob.glob("
                 "'packages/*.json') if any('oct' in (v.get('kinds') or []) for v in "
                 "json.load(open(f))['versions'])))\"")
    if n_oct is not None:
        facts["shelf_oct_packs"] = fact(int(n_oct),
                                        "python3 -c \"import json,glob;print(sum(1 for f in "
                                        "glob.glob('packages/*.json') if any('oct' in "
                                        "(v.get('kinds') or []) for v in json.load(open(f))"
                                        "['versions'])))\"",
                                        "packages/",
                                        "含**异架构预编译 .oct** 的包数（wasm 里必须重编）")

    # ── 能力层需求（`kinds` 会说谎的那一类：纯 .m 却要 Python 运行时）──────────────
    #   判据 = 档案 `note` 里有没有写能力层需求（`DESCRIPTION` 的 SystemRequirements）。
    #   这条数的不是"能不能装"，是"装上了跑不跑得动"——见 README 的已知角落与 R-002。
    n_needs = _one("grep -l '能力层需求' packages/*.json | wc -l")
    if n_needs is not None:
        facts["shelf_needs_capability"] = fact(
            int(n_needs), "grep -l '能力层需求' packages/*.json | wc -l", "packages/",
            "标了**能力层需求**的包数（纯 .m 却要 Python/SymPy ⇒ kinds 对它们会说谎）")

    # ── 工具自证通过数（本仓工具的判据强度）──────────────────────────────────────
    n_pass = _one("python3 tools/forge-shelf.py --selftest 2>/dev/null | grep -c '^PASS'")
    if n_pass is not None:
        facts["tool_selftest_pass"] = fact(int(n_pass),
                                           "python3 tools/forge-shelf.py --selftest "
                                           "2>/dev/null | grep -c '^PASS'",
                                           "tools/forge-shelf.py",
                                           "取包工具自证通过数（三类用例齐备）")

    # ── 内容面规模（文档/配方/端口）────────────────────────────────────────────
    for key, d, what in (("recipes_count", "recipes", "供给配方数"),
                         ("docs_count", "docs", "经验集文档数"),
                         ("port_docs_count", "port", "端口规范副本数")):
        n = len(glob.glob(os.path.join(REPO, d, "*.md")))
        if n:
            facts[key] = fact(n, "ls %s/*.md | wc -l" % d, "%s/" % d, what)

    # ── 供给配方引用的**上游字节**（URL + sha256 的身份；配方是"重取入口"）────────
    #   ⚠️ 字节不在本机 ⇒ 这条事实**不写**（宁缺勿假，collect.py 原则 3）。
    #   权威事实在生产者的 manifest（LLVM-wasm release/out/manifest.json）；本仓是消费侧摘录。
    if os.path.isfile(LLVM_BUNDLE):
        facts["llvm_bundle_sha"] = fact(
            _one("sha256sum %s | cut -d' ' -f1" % LLVM_BUNDLE),
            "sha256sum %s | cut -d' ' -f1" % LLVM_BUNDLE,
            "recipes/llvm-wasm.md", "LLVM-wasm 工具链 bundle 的 sha（发布件身份）")
        facts["llvm_bundle_bytes"] = fact(
            int(_one("stat -c%%s %s" % LLVM_BUNDLE)),
            "stat -c%%s %s" % LLVM_BUNDLE,
            "recipes/llvm-wasm.md", "LLVM-wasm 工具链 bundle 的字节数")
    if os.path.isfile(PYODIDE_CORE):
        facts["pyodide_core_sha"] = fact(
            _one("sha256sum %s | cut -d' ' -f1" % PYODIDE_CORE),
            "sha256sum %s | cut -d' ' -f1" % PYODIDE_CORE,
            "recipes/pyodide.md", "Pyodide 运行时 core 的 sha（符号计算能力层的底座）")
        facts["pyodide_core_bytes"] = fact(
            int(_one("stat -c%%s %s" % PYODIDE_CORE)),
            "stat -c%%s %s" % PYODIDE_CORE,
            "recipes/pyodide.md", "Pyodide 运行时 core 的字节数")

    return facts


if __name__ == "__main__":
    print(json.dumps(measure(), ensure_ascii=False, indent=1))
