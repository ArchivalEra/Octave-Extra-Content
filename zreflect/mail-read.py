#!/usr/bin/env python3
# mail-read.py —— 读信入口（2026-10-17，用户点令「read 文件夹」第三版定稿）
#
# ## 这份代码被分发给所有带 `mail/` 的仓（2026-10-31）
#
# 它**自包含**：只用标准库（os / sys / subprocess / tempfile / shutil），
# 不 import 任何仓内模块，不假设仓库结构 —— 唯一的前提是**存在 `mail/` 目录**
# （未读 = `mail/*.md`，已读 = `mail/read/*.md`，位置即状态）。
#
# 所以：换任何仓都能直接 `python3 zreflect/mail-read.py` 跑；`--selftest`
# 会在临时目录里造夹具、不碰真 `mail/`，9 条用例自证。
#
# 分发规矩（四仓已在用的同一套）：投递 = 落文件到收信方 `mail/`；
# 提交 = 收信方自己做（每仓闸门不同，发信方不代提交）。
#
# 为什么是这个形状（前两版被否的教训）：
#   v1 闸门化（凭据推断 + pre-commit --check）✘ —— 违反信任边界：mail 不进断言面
#      （mail/README.md 明写"本目录不进任何闸门的断言面"；闲散往来不可信是刻意的）。
#   v2 会话注入（SessionStart hook）✘ —— 剥夺选择权：信硬塞上下文，人不能选择不读。
#   v3 本版：**读信入口命令**。像 `git log` 一样——你决定读（选择权），读 = 打印全文
#      并自动 git mv 进 read/（零手动搬运）。
#
# 为什么不是内核级读取检测（实测矩阵，2026-10-17 本机）：
#   atime     ✘ /mnt/hdd 挂 noatime（cat 后实测纹丝不动）；根分区仅 relatime
#   inotify   △ 免 root 可用但无历史（监听进程不在场的事件永久丢失）
#   fanotify  ✘ 实测 EPERM（需 CAP_SYS_ADMIN）
#   auditd    ✘ auditctl 不可用（需 root）
#   ⇒ 内核层没有"免 root + 有历史 + 覆盖一切读取"的机制；入口命令是工程最优解。
#
# 用法：
#   python3 zreflect/mail-read.py                 # 列未读信（一屏速览，不动文件）
#   python3 zreflect/mail-read.py 030             # 读信：打印全文 + git mv 进 read/
#   python3 zreflect/mail-read.py 030 --keep      # 读但留在原处（回头再读/对照）
#   python3 zreflect/mail-read.py --all           # 依次读全部未读信（逐封确认）
#
# ⚠️ 有意不做的事（信任边界）：
#   · 不进任何闸门 / 不产 rc 语义 / 不写 FACTS —— 信件内容永远不是机器可信输入；
#   · 不自动拉取/推送 —— 读信是本地动作；
#   · read/ 里的信只进不出（git mv 保留 --follow 历史；"不删"本意 = 内容不可消失）。
import os
import re
import subprocess
import sys

# ⚠️ 真自包含（2026-10-31 修）：原来这里无条件 `from gate import module_meta`，
# 于是这份脚本**离开 Einfacht 就跑不起来**（`gate.py` 是 Einfacht 的模块）。
# 但这份代码要分发给所有带 `mail/` 的仓，其中有的仓没有 Einfacht —— 那种情形下
# 一个 ImportError 就把「读信」这个最基本的动作废掉了，而读信本来只需要标准库。
#
# 形状：**先定义本地等价实现，再尝试用真的覆盖它**。
# ⚠️ 别把 `MODULE = module_meta(...)` 写进 try 块里 —— `registry.py` 的名录对账是
#     **AST 扫模块顶层**（`_declaration()` 只走 `tree.body`），写进 try 就扫不到，
#     本仓会以「平台模块必须声明自己」红掉（2026-10-31 实测踩到）。
#     所以声明必须在**顶层、无条件**出现；「有没有真 gate」是调用期的事。
class _Meta:
    """`gate.module_meta` 的最小等价物（无 Einfacht 时的退化）。"""
    def __init__(self, name, summary, selftest=False):
        self.name, self.summary, self.selftest = name, summary, selftest


def module_meta(name, summary, selftest=False):
    return _Meta(name, summary, selftest)


try:                                    # 有 Einfacht ⇒ 用真实现（同名字段同语义）
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from gate import module_meta
except ImportError as _e:               # 没有 ⇒ 留在上面的本地实现，且**退化要可闻**
    print("note: 本仓无 zreflect/gate.py（非 Einfacht 仓）—— mail-read 以自包含模式运行：%s"
          % _e, file=sys.stderr)

MODULE = module_meta("mail 读信入口",
                     "读 = 打印 + 自动归档 read/（纯工具，不进断言面）",
                     selftest=True)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL = os.path.join(HERE, "mail")
READ = os.path.join(MAIL, "read")


def unread():
    """未读区（mail/ 直下）的信，按编号序。read/ 里的 = 已读，不列。"""
    try:
        names = sorted(os.listdir(MAIL))
    except OSError:
        return []
    return [n for n in names if n.endswith(".md") and n != "README.md"]


def _match(query):
    """把用户输入（030 / 030-host… / 完整名）匹配到未读信文件名。"""
    if query in unread():
        return query
    hits = [n for n in unread() if n.startswith(query) or query in n]
    return hits[0] if len(hits) == 1 else None


def _archive(name):
    """读过了 ⇒ git mv 进 read/（未跟踪文件退普通 rename）。返回是否成功。

    ⚠️ 同名冲突拒覆盖（试验场实测 bug#1，2026-10-18）：read/ 已有同名信时，
    git mv 本身会拒，但 rename 兜底会**静默覆盖** ⇒ 旧信丢失（违反"内容不可消失"）。
    修法：目标已存在 ⇒ 不动，报错让人处理（重投同名信本身可疑——编号就该唯一）。
    """
    os.makedirs(READ, exist_ok=True)
    dst = os.path.join(READ, name)
    if os.path.exists(dst):
        print("FATAL: mail/read/%s 已存在 —— 同名重投？编号应唯一；"
              "不覆盖旧信（内容不可消失）。新信留在未读区，先人工处置。"
              % name, file=sys.stderr)
        return False
    r = subprocess.run(["git", "-C", HERE, "mv", os.path.join("mail", name),
                        os.path.join("mail", "read", name)],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return True
    src = os.path.join(MAIL, name)
    if os.path.isfile(src):
        os.rename(src, dst)
        return True
    return False


def cmd_list():
    names = unread()
    if not names:
        print("未读区：空（mail/read/ 里的是已读存档）")
        return 0
    print("未读区 %d 封（读完自动进 read/）：" % len(names))
    for n in names:
        # 一行速览：编号 + 标题行
        try:
            head = open(os.path.join(MAIL, n), encoding="utf-8",
                        errors="replace").readline().lstrip("# ").strip()
        except OSError:
            head = "（读不了）"
        print("  %-46s %s" % (n, head[:60]))
    print("\n读：python3 zreflect/mail-read.py <编号或文件名>")
    return 0


def cmd_read(query, keep=False):
    name = _match(query)
    if not name:
        print("FATAL: 未读区里没有（或不止一封）匹配 %r 的信 —— 先跑无参数列清单" % query,
              file=sys.stderr)
        return 2
    text = open(os.path.join(MAIL, name), encoding="utf-8", errors="replace").read()
    print(text)
    if keep:
        print("\n── --keep：留在未读区（read/ 未动）", file=sys.stderr)
        return 0
    if _archive(name):
        print("\n── 已读，归档 mail/read/%s" % name, file=sys.stderr)
        return 0
    # 归档失败的两形（_archive 已打 FATAL 细节）：同名冲突拒覆盖 / git 异常。
    # 信留在未读区、内容已读 —— fail-open（工具坏了不拦人读信）。
    print("\n── ⚠️ 归档失败 —— 信留在未读区（内容已读；这不是断言面，不拦你）",
          file=sys.stderr)
    return 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if argv and argv[0] == "--all":
        names = unread()
        if not names:
            return cmd_list()
        for i, n in enumerate(names):
            print("══ [%d/%d] %s ══" % (i + 1, len(names), n))
            cmd_read(n)
        return 0
    if not argv:
        return cmd_list()
    keep = "--keep" in argv
    query = [a for a in argv if not a.startswith("--")][0]
    return cmd_read(query, keep)


# ── 自证（纯函数档：列/匹配/归档的判据；不碰真 mail/）─────────────────────────
def _selftest():
    import tempfile, shutil                                     # noqa: E401
    global HERE, MAIL, READ
    t = tempfile.mkdtemp()
    os.makedirs(os.path.join(t, "mail"))
    saved = (HERE, MAIL, READ)
    HERE, MAIL, READ = t, os.path.join(t, "mail"), os.path.join(t, "mail", "read")
    open(os.path.join(MAIL, "001-a.md"), "w").write("# 001 · x\n")
    open(os.path.join(MAIL, "002-b.md"), "w").write("# 002 · y\n")
    cases = [
        ("列清单：未读区 2 封", lambda: len(unread()) == 2),
        ("匹配：完整名", lambda: _match("001-a.md") == "001-a.md"),
        ("匹配：编号前缀", lambda: _match("002") == "002-b.md"),
        ("匹配：无命中 ⇒ None", lambda: _match("999") is None),
        ("归档：git mv（无 git 时退 rename）后从未读区消失",
         lambda: (_archive("001-a.md") or True) and not os.path.exists(
             os.path.join(MAIL, "001-a.md"))),
        ("归档后 read/ 里有它", lambda: os.path.exists(os.path.join(READ, "001-a.md"))),
        ("★ 归档不改变内容（逐字节）",
         lambda: open(os.path.join(READ, "001-a.md"), encoding="utf-8").read() == "# 001 · x\n"),
        ("★ 未读区剩下的是没读的那封（002 还在）",
         lambda: "002-b.md" in unread()),
        ("★ 同名冲突拒覆盖（试验场 bug#1）：read/ 已有同名 ⇒ _archive 拒 + 新信留未读区",
         lambda: (
             # 再投一封同名 001-a，归档必须拒
             open(os.path.join(MAIL, "001-a.md"), "w").write("# 001 · 冲突版\n"),
             not _archive("001-a.md"),
             # 旧信（read/ 里的）内容未被覆盖
             open(os.path.join(READ, "001-a.md"), encoding="utf-8").read() == "# 001 · x\n",
             # 新信留在未读区
             "001-a.md" in unread(),
         )[1] and (open(os.path.join(READ, "001-a.md"), encoding="utf-8").read() == "# 001 · x\n")
         and "001-a.md" in unread()),
    ]
    # ⚠️ 顺序（本文件第一版的真实 bug）：lambda 在执行时才读全局 MAIL/READ ——
    #    恢复 saved 必须在**全部用例跑完之后**，否则夹具变量被换回真仓路径，
    #    用例全跑在真 mail/ 上（26 封 ⇒ "未读区 2 封"必 fail）。
    bad = 0
    for label, fn in cases:
        try:
            ok = bool(fn())
        except Exception as e:                                  # noqa: BLE001
            ok, label = False, "%s（异常 %r）" % (label, e)
        print("%s | %s" % ("PASS" if ok else "fail", label))
        bad += 0 if ok else 1
    HERE, MAIL, READ = saved
    shutil.rmtree(t, True)
    # ⚠️ 两行汇总都**不能删**（2026-10-31 实测踩到）：人读行 + 机器摘要行是
    # Einfacht 的平台约定（issue #3 ③）。我一度以为第二行是"完全同义的冗余"删掉了，
    # `gates-selftest.sh` 立刻报「自证缺机器摘要行」—— 它 grep 的就是 `=== N PASS / M FAIL ===`
    # 这个与检查器名无关的固定格式，人读行它不认。
    print("=== mail-read 自证：%d PASS / %d fail ===" % (len(cases) - bad, bad))
    print("=== %d PASS / %d FAIL ===" % (len(cases) - bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
