#!/usr/bin/env python3
# Octave-Forge-Shelf — 货架工具（取包 / 校验 / 解析 / 出站点目录）
# Copyright (C) 2026 ArchivalEra
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ── 这个仓是什么 ──────────────────────────────────────────────────────────────
# **货架**：一组 Octave-Forge 包的**档案事实**（每包一文件，见 packages/*.json），
# 以及一个**纯宿主侧**工具（本文件）。它**不含包字节**——字节按 catalog 里的
# `url + sha256` 从上游取，落到本地缓存（持久盘），再装配进站点。
#
# 为什么这样切（设计稿 build/113/NOTES-forge-ondemand.md）：
#   · 仓小（KB 级）⇒ **可无限扩展**：加一个包 = 加一个文件，diff 干净、无冲突；
#   · pin 形状与主仓 fork 管线**同构**：本仓被主仓当 submodule 钉住 ⇒ 「货架上有什么、
#     哪个版本」由 **submodule commit** 承载；「字节是不是那份」由 **sha256** 承载；
#   · 因此**能力与包数解耦**：主仓的 provision / witness / 客户端 install 三件套
#     一行都不用改就能吃下任意多个包。
#
# ── 纪律（与主仓一致）────────────────────────────────────────────────────────
#   · **只上验证过的**：`verified` 为 null 的条目 = 还没在本构建里实测过 ⇒
#     `--emit` 默认**跳过**（要带上得显式 `--allow-unverified`）；
#   · **fail-closed**：sha256 不符 ⇒ 拒绝（取包/校验/装配三处都查）；
#   · 每个子命令都有判据，且 `--selftest` 三档齐备（正常 / 该报的必须报 / 空输入必须报）。
#
# 用法：
#   tools/forge-shelf.py --list
#   tools/forge-shelf.py --fetch <包名> [<包名>…] [--cache DIR]
#   tools/forge-shelf.py --verify [--cache DIR]
#   tools/forge-shelf.py --probe <包名> --cache DIR        # 探 kinds + 记录 verified
#   tools/forge-shelf.py --emit <out.json> [--octave 11.3.0] [--allow-unverified]
#   tools/forge-shelf.py --add <包名> [--version V]        # 从上游索引加一个新包档案
#   tools/forge-shelf.py --selftest
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG_DIR = os.path.join(HERE, "packages")
INDEX_URL = "https://gnu-octave.github.io/packages/packages.json"
DEFAULT_CACHE = "/mnt/hdd/octave-wasm-build/third_party/forge"


# ── 纯函数（自证直接喂它们）──────────────────────────────────────────────────
def vtuple(s):
    return tuple(int(x) for x in re.findall(r"\d+", str(s))[:3]) or (0,)


def octave_ok(need, requires):
    """`requires` 形如 ['octave (>= 6.4.0)']；need 形如 '11.3.0'。"""
    for r in requires or []:
        m = re.match(r"octave\s*\(\s*(>=|<=|==|>|<)\s*([\d.]+)\s*\)", r.strip())
        if not m:
            continue
        op, ver = m.group(1), vtuple(m.group(2))
        a = vtuple(need)
        if not {">=": a >= ver, "<=": a <= ver, "==": a == ver,
                ">": a > ver, "<": a < ver}[op]:
            return False
    return True


def pick_version(entry, octave):
    """挑「满足目标 Octave」的最新版；没有 ⇒ None。"""
    ok = [v for v in entry.get("versions", []) if octave_ok(octave, v.get("requires"))]
    if not ok:
        return None
    ok.sort(key=lambda v: vtuple(v["version"]), reverse=True)
    return ok[0]


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def detect_kinds(tar_path):
    """包内含什么——**三态，后果完全不同**（2026-10-09 实测精化）：

      `m`    有 `.m` 源 ⇒ **开箱可用**（客户端按需装的主路）；
      `oct`  **随包带预编译 `.oct`** ⇒ ⚠️ 那是**别的架构**的二进制，在 wasm 构建里必须重编；
      `src`  带 `src/` 源码但**没有**现成 `.oct` ⇒ `.m` 部分照常可用，**只是缺加速件**。

    ⚠️ 为什么不能把 `src` 当 `oct`：实测 10 个包里 `src/` 是**可选加速件源码**、
    包**不带** `.oct`（geometry/statistics/struct 的预编译 `.oct` 数都是 **0**）。
    旧判别会把绝大多数包误判成"需编译"，误导 v1 范围。（纯函数：输入 = tar 路径。）"""
    kinds = set()
    with tarfile.open(tar_path, "r:gz") as tf:
        names = tf.getnames()
    if any(n.endswith(".m") for n in names):
        kinds.add("m")
    if any(n.endswith(".oct") for n in names):
        kinds.add("oct")
    if "oct" not in kinds and any(
            ("/src/" in n and n.endswith((".cc", ".cpp", ".c", ".f", ".f90", ".f95")))
            for n in names):
        kinds.add("src")
    return sorted(kinds)


# ── 端口 schema 2 的两个轴（接缝 §2；port/README.md 的命名纪律）───────────────
#   `kind` 与 `kinds` 同名两义（实测缺陷：manifest 的 kind = 投送形态，catalog 的
#   kinds = 内容构成）⇒ 收编成两个正交轴，名字不再撞：
#     · form    = **投送形态**（供给期从字节派生：pkg | tree | oct | octdir | file | js）
#     · content = **内容构成**（今天的 kinds：m | src | oct）
#   本仓出的包条目都是「一个 tarball 整包投送」⇒ form 恒为 "pkg"（从 kinds 派生规则：
#   本仓不产 tree/oct/octdir/file/js —— 那些是能力层 / 编译件 / 单文件的形态，
#   由各自的生产者出，不是本仓货架的活）。`content` 就是 kinds 本身。
def derive_form(kinds):
    """投送形态（本仓只有 pkg 一种：每包一个 tarball 整包投送）。"""
    return "pkg"


def derive_axes(kinds):
    """(form, content) —— 端口 schema 2 的两轴。`content` = 今天的 kinds。"""
    return derive_form(kinds), list(kinds or [])


# ── producer 自述（接缝 §4「生产者必做第 3 条：pin 自述」）────────────────────
#   端口把 `producer` 列为**可选顶层块** `{id, pin}`：写了才能过宿主的
#   `validate-content-list.py --producer <id>` 那条**针对性校验**（不写不算错）。
#   本仓的身份 = **submodule commit**（宿主 pin 的就是它）⇒ `pin` 读当前 HEAD。
#   ⚠️ `pin` 每提交都变 ⇒ **绝不进事实台账**（同 R-001）；它只活在**出表**里，
#   出表不是渲染进 STATE.md 的机器块 ⇒ 不破坏 `--check` 收敛。
PRODUCER_ID = "octave-extra-content"


def _git_head(short=12):
    """本仓 HEAD（producer.pin 用）。读不到 ⇒ None（宁缺勿假，不编一个假 sha）。"""
    try:
        r = subprocess.run(["git", "-C", HERE, "rev-parse", "--short=%d" % short, "HEAD"],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() or None if r.returncode == 0 else None


def producer_block():
    """`{id, pin}`；pin 读不到 ⇒ 只给 id（不编假 sha）。"""
    pin = _git_head()
    blk = {"id": PRODUCER_ID}
    if pin:
        blk["pin"] = "submodule:%s" % pin
    return blk


def producer_ok(doc, want_id):
    """纯判据（自证用）：表里的 producer.id == want_id。空/缺 ⇒ False（零值守卫）。"""
    p = (doc or {}).get("producer")
    return bool(isinstance(p, dict) and p.get("id") == want_id)


def load_shelf(pkg_dir=None):
    """读全部包档案 → {name: entry}。目录缺失/为空 ⇒ 调用方按零值守卫报。"""
    d = pkg_dir if pkg_dir is not None else PKG_DIR
    out = {}
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return out
    for n in names:
        if not n.endswith(".json"):
            continue
        try:
            with open(os.path.join(d, n), encoding="utf-8") as fh:
                e = json.load(fh)
        except (OSError, ValueError):
            continue
        if isinstance(e, dict) and e.get("name"):
            out[e["name"]] = e
    return out


# ── 子命令 ──────────────────────────────────────────────────────────────────
def cmd_list(shelf):
    if not shelf:
        return fatal("货架是空的（packages/ 里一个档案都没有）——空输入不是通过")
    for name in sorted(shelf):
        e = shelf[name]
        vs = ", ".join(v["version"] for v in e.get("versions", []))
        kinds = e["versions"][0].get("kinds", []) if e.get("versions") else []
        ver = "verified" if e.get("verified") else "UNVERIFIED"
        print("%-14s %-16s %-8s deps=%s" % (name, vs, ver,
                                            ",".join(e.get("depends") or []) or "-"))
    print("共 %d 个包（%d 个已验证）" % (len(shelf),
                                     sum(1 for e in shelf.values() if e.get("verified"))))
    return 0


def tarball_path(entry, ver, cache):
    return os.path.join(cache, "%s-%s.tar.gz" % (entry["name"], ver["version"]))


def cmd_fetch(shelf, names, cache):
    os.makedirs(cache, exist_ok=True)
    bad = 0
    for name in names:
        e = shelf.get(name)
        if not e:
            print("  ! 货架上没有包: %s" % name, file=sys.stderr)
            bad += 1
            continue
        for v in e.get("versions", []):
            dest = tarball_path(e, v, cache)
            if os.path.isfile(dest) and sha256_file(dest) == v["sha256"]:
                print("  %-14s %-8s cached（sha 相符）" % (name, v["version"]))
                continue
            url = v.get("url") or ""
            if not url:
                print("  ! %s %s 没有 url（档案缺）" % (name, v["version"]), file=sys.stderr)
                bad += 1
                continue
            r = subprocess.run(["curl", "-sSL", "--max-time", "600", "-o", dest, url])
            if r.returncode != 0 or not os.path.isfile(dest):
                print("  ! 取包失败: %s" % url, file=sys.stderr)
                bad += 1
                continue
            got = sha256_file(dest)
            if got != v["sha256"]:
                print("  ! CHECKSUM-MISMATCH %s %s: 期望 %s… 实得 %s…"
                      % (name, v["version"], v["sha256"][:12], got[:12]), file=sys.stderr)
                bad += 1
                continue
            print("  %-14s %-8s ok %9d 字节" % (name, v["version"], v["size"]))
    if bad:
        return fatal("取包有 %d 个问题（见上）" % bad)
    return 0


def cmd_verify(shelf, cache):
    if not shelf:
        return fatal("货架是空的 —— 空输入不是通过")
    bad, checked = 0, 0
    for name in sorted(shelf):
        for v in shelf[name].get("versions", []):
            dest = tarball_path(shelf[name], v, cache)
            if not os.path.isfile(dest):
                print("  - %s %s 本地缓存没有（未取）" % (name, v["version"]))
                continue
            checked += 1
            got = sha256_file(dest)
            if got != v["sha256"]:
                print("  ! %s %s sha 不符：档案 %s… 本地 %s…"
                      % (name, v["version"], v["sha256"][:12], got[:12]), file=sys.stderr)
                bad += 1
            else:
                print("  ✓ %s %s" % (name, v["version"]))
    if checked == 0:
        return fatal("缓存里一个包都没有 ⇒ 没查到东西（空输入不是通过）")
    if bad:
        return fatal("%d 个包的字节与档案不符" % bad)
    print("校验 %d 个 tarball，全部与档案 sha 相符" % checked)
    return 0


def cmd_probe(shelf, name, cache, octave):
    """探包：kinds 探测 + 记录 verified（**只记量到的事实**：kinds 来自 tar 内容）。"""
    e = shelf.get(name)
    if not e:
        return fatal("货架上没有包: %s" % name)
    v = pick_version(e, octave)
    if not v:
        return fatal("%s 没有满足 Octave %s 的版本" % (name, octave))
    p = tarball_path(e, v, cache)
    if not os.path.isfile(p):
        return fatal("先取包：tools/forge-shelf.py --fetch %s" % name)
    if sha256_file(p) != v["sha256"]:
        return fatal("本地 tarball 与档案 sha 不符")
    kinds = detect_kinds(p)
    v["kinds"] = kinds
    e["verified"] = {"octave": octave, "how": "detect_kinds（tar 内容判 m/oct）",
                     "tarball_sha": v["sha256"][:16]}
    write_entry(e)
    verdict = {"m": "纯 .m ⇒ v1 按需装可行",
               "m+src": ".m 开箱可用；src/ 是可选加速件（不编也能用）⇒ v1 可行",
               "m+oct": "⚠️ 随包带预编译 .oct（异架构）⇒ 必须重编，见设计稿 §6A",
               "oct": "只有 .oct ⇒ 必须重编",
               "src": "只有 src/（无 .m）⇒ 必须编译"}.get("+".join(kinds), "见 kinds")
    print("%s %s：kinds=%s ⇒ %s" % (name, v["version"], kinds, verdict))
    return 0


def write_entry(e):
    p = os.path.join(PKG_DIR, e["name"] + ".json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(e, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def cmd_emit(shelf, out, octave, allow_unverified):
    """出**站点目录**（客户端读的那份）：按目标 Octave 解析版本 + 只带已验证的。

    ⚠️ schema 2（2026-10-14，接缝 §2 / port/README.md）：每条加 `form`（投送形态，
    供给期从字节派生）与 `content`（内容构成 = 今天的 kinds）两轴；`kinds` **保留为
    兼容视图**。

    ★ `producer` 自述（2026-10-14，接缝 §4「生产者必做第 3 条：pin 自述」）：
    顶层带 `{id, pin}`（pin = 本仓 submodule commit）⇒ 能过宿主
    `validate-content-list.py --producer octave-extra-content` 的针对性校验。

    ★ URL 两段式（接缝 §4）：**生产者态**的 `url` 是**上游绝对 URL**（"重取入口"，
    `docs/FORK-PIPELINE.md` §3）；宿主装配时改写为站点态同源相对，并把上游 URL 记进
    `upstream_url`。本仓出表时**两者都给**（`url` = 上游；`upstream_url` 同值）——
    宿主装配时 `url` 被改写、`upstream_url` 保留，本仓这一侧不必猜宿主怎么改写。
    """
    if not shelf:
        return fatal("货架是空的 —— 空输入不是通过")
    packs, skipped = [], []
    for name in sorted(shelf):
        e = shelf[name]
        if not e.get("verified") and not allow_unverified:
            skipped.append(name + "（UNVERIFIED）")
            continue
        v = pick_version(e, octave)
        if not v:
            skipped.append(name + "（无兼容 %s 的版本）" % octave)
            continue
        form, content = derive_axes(v.get("kinds"))
        packs.append({
            "name": name, "version": v["version"], "size": v["size"],
            "sha256": v["sha256"], "url": v["url"],
            "upstream_url": v["url"],               # 重取入口（宿主装配时 url 被改写为同源）
            "deps": e.get("depends") or [],
            "form": form, "content": content,
            "kinds": content,                       # 兼容视图（旧消费者照读）
        })
    doc = {"schema": 2, "octave": octave, "producer": producer_block(), "packs": packs}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    pin = doc["producer"].get("pin", "(pin 读不到)")
    print("已写出 %s（%d 个包，schema 2，producer=%s %s）"
          % (out, len(packs), PRODUCER_ID, pin))
    if skipped:
        print("  跳过 %d 个：%s" % (len(skipped), "; ".join(skipped)))
    return 0


def cmd_add(shelf, name, version, cache):
    """从上游索引加一个新包档案（**只写档案，不取字节**）。"""
    if name in shelf:
        return fatal("货架上已有 %s（要换版本请手改 packages/%s.json）" % (name, name))
    idx = load_index()
    e = idx.get(name)
    if not e:
        return fatal("上游索引里没有包: %s" % name)
    vers = e.get("versions", [])
    if not vers:
        return fatal("%s 在上游索引里没有版本" % name)
    if version:
        vers = [v for v in vers if v["id"] == version]
        if not vers:
            return fatal("%s 没有版本 %s" % (name, version))
    out_vers = []
    for v in vers:
        out_vers.append({
            "version": v["id"], "url": v.get("url", ""),
            "sha256": v.get("sha256", ""), "size": v.get("size") or 0,
            "requires": [d for d in v.get("depends", []) if d.startswith("octave")],
            "date": v.get("date"), "kinds": [], "in_index": True,
        })
    entry = {"schema": 1, "name": name,
             "depends": sorted({d.split()[0] for v in vers
                                for d in v.get("depends", [])
                                if d.split()[0] not in ("octave", "pkg")}),
             "upstream": {"index": "gnu-octave/packages",
                          "description": (e.get("description") or "")[:300],
                          "links": e.get("links") or {}},
             "verified": None, "note": "", "versions": out_vers}
    write_entry(entry)
    print("已加 %s（%d 个版本）；下一步： --fetch %s && --probe %s --cache %s"
          % (name, len(out_vers), name, name, cache))
    return 0


# ── 基础设施 ────────────────────────────────────────────────────────────────
def fatal(msg):
    print("FATAL: %s" % msg, file=sys.stderr)
    return 2


def load_index(cache=None):
    c = os.path.join(cache or DEFAULT_CACHE, "packages.json")
    if os.path.isfile(c) and os.path.getsize(c) > 10000:
        with open(c, encoding="utf-8") as fh:
            return json.load(fh)
    import urllib.request
    with urllib.request.urlopen(INDEX_URL, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    os.makedirs(os.path.dirname(c), exist_ok=True)
    with open(c, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    return data


# ── 三档自证（本仓纪律：正常不报 / 该报的必须报 / 空输入必须报）──────────────
def _selftest():
    import tempfile
    cases = []

    def ck(label, fn):
        cases.append((label, fn))

    # ① 正常不报（阳性对照）
    ck("octave_ok：'11.3.0' 满足 '>= 6.4.0'",
       lambda: octave_ok("11.3.0", ["octave (>= 6.4.0)"]) is True)
    ck("octave_ok：无 requires ⇒ 满足（不拦）",
       lambda: octave_ok("11.3.0", []) is True)
    ck("pick_version：挑最新满足的",
       lambda: pick_version({"versions": [
           {"version": "1.0.0", "requires": []},
           {"version": "2.0.0", "requires": ["octave (>= 99.0.0)"]}]}, "11.3.0")["version"] == "1.0.0")
    ck("vtuple 排序正确（1.10.0 > 1.9.0）", lambda: vtuple("1.10.0") > vtuple("1.9.0"))
    ck("load_shelf 读空目录 ⇒ {}（不炸）",
       lambda: load_shelf(tempfile.mkdtemp()) == {})

    # ② 该报的必须报（反向断言）
    ck("★ octave_ok：'7.2.0' 不满足 '>= 8.1.0'（必须报 False）",
       lambda: octave_ok("7.2.0", ["octave (>= 8.1.0)"]) is False)
    ck("★ pick_version：没有兼容版本 ⇒ None（不是硬塞一个）",
       lambda: pick_version({"versions": [
           {"version": "2.0.0", "requires": ["octave (>= 99.0.0)"]}]}, "11.3.0") is None)
    ck("★ fetch：货架上没有的包必须报错（fatal 退 2）",
       lambda: cmd_fetch({}, ["no_such_pkg"], tempfile.mkdtemp()) == 2)
    ck("★ probe：货架上没有的包必须报错",
       lambda: cmd_probe({}, "nope", tempfile.mkdtemp(), "11.3.0") == 2)
    ck("★ add：货架上已有同名 ⇒ 必须报错（不静默覆盖）",
       lambda: cmd_add({"x": {"name": "x"}}, "x", "", tempfile.mkdtemp()) == 2)

    # ③ 空输入必须报（零值守卫）
    ck("★ list：空货架必须报（空输入不是通过）", lambda: cmd_list({}) == 2)
    ck("★ verify：空货架必须报", lambda: cmd_verify({}, tempfile.mkdtemp()) == 2)
    ck("★ verify：缓存全空必须报（没查到东西 ≠ 通过）",
       lambda: cmd_verify({"a": {"name": "a", "versions": [{"version": "1", "sha256": "x"}]}},
                          tempfile.mkdtemp()) == 2)
    ck("★ emit：空货架必须报", lambda: cmd_emit({}, tempfile.mkdtemp() + "/o.json",
                                                "11.3.0", False) == 2)

    # ④ 端口 schema 2 两轴（form / content；接缝 §2）
    def _emit_doc(kinds):
        d = tempfile.mkdtemp()
        sh = {"p": {"name": "p", "depends": [], "verified": {"octave": "11.3.0"},
                    "versions": [{"version": "1.0", "sha256": "a" * 64, "size": 1,
                                  "url": "u", "requires": [], "kinds": kinds}]}}
        cmd_emit(sh, d + "/o.json", "11.3.0", False)
        with open(d + "/o.json", encoding="utf-8") as fh:
            return json.load(fh)

    ck("schema 2：form 派生为 pkg，content = kinds",
       lambda: (lambda doc: doc["schema"] == 2 and doc["packs"][0]["form"] == "pkg"
                and doc["packs"][0]["content"] == ["m", "src"])(
           _emit_doc(["m", "src"])))
    ck("schema 2：kinds 保留为兼容视图（= content，旧消费者照读）",
       lambda: (lambda p: p["kinds"] == p["content"] == ["m", "oct"])(
           _emit_doc(["m", "oct"])["packs"][0]))
    ck("★ schema 2：kinds 空 ⇒ content 也是空（不许把空说成有内容）",
       lambda: (lambda p: p["content"] == [] and p["form"] == "pkg")(
           _emit_doc([])["packs"][0]))

    # ⑤ producer 自述（接缝 §4「pin 自述」；producer.id 是宿主的 --producer 判据）
    ck("producer：--emit 顶层带 producer.id（= octave-extra-content）",
       lambda: _emit_doc(["m"]).get("producer", {}).get("id") == PRODUCER_ID)
    ck("producer：pin 是 submodule:<sha>（本仓身份 = submodule commit）",
       lambda: str(_emit_doc(["m"])["producer"].get("pin", "")).startswith("submodule:"))
    ck("producer_ok：id 相符 ⇒ True",
       lambda: producer_ok({"producer": {"id": PRODUCER_ID}}, PRODUCER_ID) is True)
    ck("★ producer_ok：id 不符 ⇒ 必须 False（宿主的 --producer 判据形状）",
       lambda: producer_ok({"producer": {"id": "someone-else"}}, PRODUCER_ID) is False)
    ck("★ producer_ok：缺 producer 块 ⇒ 必须 False（零值守卫，不是通过）",
       lambda: producer_ok({}, PRODUCER_ID) is False)
    ck("★ producer_ok：producer 是 None ⇒ 必须 False（不许 AttributeError）",
       lambda: producer_ok({"producer": None}, PRODUCER_ID) is False)
    ck("emit：每条带 upstream_url（重取入口；两段式的生产者态）",
       lambda: _emit_doc(["m"])["packs"][0].get("upstream_url") == "u")

    # ⑥ 能力层边（接缝 §2 落法：deps 指向 form:"tree" 的能力层条目，不加 needs 字段）
    #    本仓的活：`symbolic` 要 Python/SymPy ⇒ depends 带 "pyodide"（宿主 mail/010 给的字面量）。
    def _emit_with_dep():
        d = tempfile.mkdtemp()
        sh = {"symbolic": {"name": "symbolic", "depends": ["pyodide"],
                           "verified": {"octave": "11.3.0"},
                           "versions": [{"version": "1.0", "sha256": "a" * 64, "size": 1,
                                         "url": "u", "requires": [], "kinds": ["m"]}]}}
        cmd_emit(sh, d + "/o.json", "11.3.0", False)
        with open(d + "/o.json", encoding="utf-8") as fh:
            return json.load(fh)

    ck("能力层边：档案 depends 里的 pyodide 出现在 emit 的 deps 里（§2 落法）",
       lambda: _emit_with_dep()["packs"][0]["deps"] == ["pyodide"])
    ck("★ 能力层边：档案 depends 为空 ⇒ deps 也是空（不臆造边）",
       lambda: _emit_doc(["m"])["packs"][0]["deps"] == [])
    ck("★ 能力层边：emit 里不出现 needs 字段（§2：不加新字段）",
       lambda: "needs" not in _emit_with_dep()["packs"][0])

    bad = 0
    for label, fn in cases:
        try:
            ok = bool(fn())
        except Exception as e:                              # noqa: BLE001
            ok, label = False, "%s（异常 %r）" % (label, e)
        print("%s | %s" % ("PASS" if ok else "fail", label))
        bad += 0 if ok else 1
    print("=== forge-shelf 自证：%d PASS / %d fail ===" % (len(cases) - bad, bad))
    print("=== %d PASS / %d FAIL ===" % (len(cases) - bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--fetch", nargs="+", metavar="PKG")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--probe", metavar="PKG")
    ap.add_argument("--emit", metavar="OUT")
    ap.add_argument("--add", metavar="PKG")
    ap.add_argument("--version", default="")
    ap.add_argument("--cache", default=DEFAULT_CACHE)
    ap.add_argument("--octave", default="11.3.0")
    ap.add_argument("--allow-unverified", action="store_true")
    a = ap.parse_args(argv)

    shelf = load_shelf()
    if a.list:
        return cmd_list(shelf)
    if a.fetch:
        return cmd_fetch(shelf, a.fetch, a.cache)
    if a.verify:
        return cmd_verify(shelf, a.cache)
    if a.probe:
        return cmd_probe(shelf, a.probe, a.cache, a.octave)
    if a.emit:
        return cmd_emit(shelf, a.emit, a.octave, a.allow_unverified)
    if a.add:
        return cmd_add(shelf, a.add, a.version, a.cache)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
