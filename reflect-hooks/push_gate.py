#!/usr/bin/env python3
"""pre-push 判据：上游 gate.py push 的等价实现，绕开 PRINCIPLES.md 不一致。

复用 gate.py 的纯函数（_refs_from_stdin / _new_content_refs /
_push_readmes_together），只替换 _prepare 的 `--check` 一步。
**这是本仓兼容层，不是上游机制层的分叉**：PRINCIPLES 修好后删本文件，
pre-push 恢复 `exec gate.py push`。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "zreflect"))
from gate import module_meta  # noqa: E402

MODULE = module_meta("pre-push 兼容层",
                     "复用上游 gate.py 的 push 判据，绕开 PRINCIPLES.md 不一致",
                     selftest=False)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "zreflect"))
sys.path.insert(0, HERE)

import importlib.util  # noqa: E402

# ⚠️ 不能 `import gate`：zreflect/gate.py 与 reflect-hooks/gate.py 同名，
#    sys.path 里前者在前 ⇒ 会导到错的那个（实测 Traceback）。按路径精确加载。
_spec = importlib.util.spec_from_file_location(
    "ein_facht_hookgate", os.path.join(HERE, "gate.py"))
upstream = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(upstream)


def main():
    # 与上游 gate.py run() 同款：先把 Einfacht.env 的旋钮搬进本进程，
    # 否则子进程拿到默认 FACTS.json（本仓台账在 build/FACTS.json）。
    upstream._load_env_plugin(HERE)

    # ① 机器块必须新鲜（只核 STATE.md —— 本仓唯一有 AUTO:FACTS 块的文档）
    rc, out = upstream._sh([sys.executable,
                            os.path.join(REPO, "zreflect", "facts.py"),
                            "--check", "STATE.md"])
    if rc != 0:
        print(out or "hookgate.blocks_stale(check=STATE.md)", file=sys.stderr)
        return 1

    # ② 全部闸门
    rc, out = upstream._sh([sys.executable,
                            os.path.join(REPO, "zreflect", "registry.py"),
                            "--run", "commit"])
    if rc != 0:
        print(out, file=sys.stderr)
        return 1

    # ③ 三语 README 同批（直接复用上游实现）
    ok, lines = upstream._push_readmes_together(
        REPO, upstream._refs_from_stdin())
    for ln in lines:
        print(ln, file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
