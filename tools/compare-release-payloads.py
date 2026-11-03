#!/usr/bin/env python3
"""release 内容对账：判断两个 release 的**载荷**是否相同（顺序无关）。

★ 为什么存在（2026-11-03 实测打的自己的脸）：
  我对比宿主两个 `octave-11.3.0` release 时，用「按 `(product,name,sha256)` **序列**
  算指纹」，得到两个不同值 ⇒ 报「不是简单重复发布」。
  **宿主指出：差异只是 entry 数组顺序**（`data,js,wasm` vs `wasm,js,data`），
  9/9 条 `(product,name,sha256)` 完全相同。

  我把「顺序」当成了「内容差异」——**指纹对顺序敏感 = 假差异**。

  ⇒ 本工具的判据：**排序后再比**（顺序是契约不要求的东西，校验器里零顺序判据）。

用法：
    python3 tools/compare-release-payloads.py a/manifest.json b/manifest.json
    python3 tools/compare-release-payloads.py --selftest

退出码：0 = 载荷完全相同；1 = 有差异（逐条列出）；2 = 用法/输入错误。
"""
import hashlib
import json
import sys


def payload_set(man):
    """把 manifest 的载荷身份取成**无序集合**：(product, name, bytes, sha256)。

    ★ 刻意不含 variants/chunks —— 那些是「同一份载荷的不同编码/分片」，
    它们的差异**也是**载荷身份的一部分吗？不是：contract V5 要求同 entry 各 codec
    块数相同、V7 要求 identity 拼回 sha == entry.sha256。
    ⇒ **载荷身份 = (product, name, bytes, sha256)**，编码只是它的表示。
    **但本工具同时报告 variants 差异**（作为独立维度），免得"编码变了"被漏掉。
    """
    out = set()
    for e in man.get("entries") or []:
        out.add((e.get("product"), e.get("name"), e.get("bytes"), e.get("sha256")))
    return out


def codec_shape(man):
    """每个 entry 的 codec 列表（不含块内容）。用于单独报告「编码形状变了」。"""
    return {(e.get("product"), e.get("name")):
            tuple(v.get("codec") for v in (e.get("variants") or []))
            for e in man.get("entries") or []}


def compare(a, b):
    """返回 (载荷是否相同, 差异列表)。差异列表空 = 相同。"""
    pa, pb = payload_set(a), payload_set(b)
    probs = []
    if not pa or not pb:
        return False, ["有一侧载荷为空 —— 空不是相同（零值守卫）"], ""

    only_a = sorted(pa - pb)
    only_b = sorted(pb - pa)
    for x in only_a:
        probs.append("只在 A: %s/%s bytes=%s sha=%s" % (x[0], x[1], x[2], (x[3] or "")[:16]))
    for x in only_b:
        probs.append("只在 B: %s/%s bytes=%s sha=%s" % (x[0], x[1], x[2], (x[3] or "")[:16]))

    ca, cb = codec_shape(a), codec_shape(b)
    for k in sorted(set(ca) & set(cb)):
        if ca[k] != cb[k]:
            probs.append("%s/%s 的 codec 形状不同: %r vs %r" % (k[0], k[1], ca[k], cb[k]))

    # 附注（不算差异，但要看得见）：顺序是否不同
    oa = [(e.get("product"), e.get("name")) for e in a.get("entries") or []]
    ob = [(e.get("product"), e.get("name")) for e in b.get("entries") or []]
    order_note = "顺序相同" if oa == ob else "顺序不同（契约不要求顺序，不算差异）"

    return (not probs), probs, order_note


def _selftest():
    n = f = 0

    def t(label, cond):
        nonlocal n, f
        if cond:
            n += 1; print("PASS | " + label)
        else:
            f += 1; print("fail | " + label)

    def man(entries):
        return {"schema": 3, "entries": entries}

    def ent(p, nm, b, s, codecs=("zstd", "gzip", "identity")):
        return {"product": p, "name": nm, "bytes": b, "sha256": s,
                "variants": [{"codec": c, "chunks": []} for c in codecs]}

    A = man([ent("w", "octave.wasm", 100, "a" * 64),
             ent("w", "octave.js", 10, "b" * 64)])
    B = man([ent("w", "octave.js", 10, "b" * 64),        # ← 只是顺序反了
             ent("w", "octave.wasm", 100, "a" * 64)])

    ok, probs, note = compare(A, B)
    t("★ 顺序不同但载荷相同 ⇒ 判为**相同**（不再被顺序骗）", ok)
    t("  且 note 明说顺序不同", "顺序不同" in note)

    # 反向：真的改了 sha ⇒ 必须判不同
    C = man([ent("w", "octave.wasm", 100, "c" * 64), ent("w", "octave.js", 10, "b" * 64)])
    ok2, probs2, _ = compare(A, C)
    t("★ 改了 sha ⇒ 必须判不同", not ok2)
    t("  且逐条列出差异", any("octave.wasm" in x for x in probs2))

    # 反向：少了/多了载荷 ⇒ 必须判不同
    D = man([ent("w", "octave.wasm", 100, "a" * 64)])
    ok3, probs3, _ = compare(A, D)
    t("★ 少一条载荷 ⇒ 必须判不同", not ok3)

    # 反向：codec 形状变了 ⇒ 必须报（载荷相同但编码不同）
    E = man([ent("w", "octave.wasm", 100, "a" * 64, codecs=("identity",)),
             ent("w", "octave.js", 10, "b" * 64)])
    ok4, probs4, _ = compare(A, E)
    t("★ codec 形状变了 ⇒ 必须报（哪怕载荷 sha 相同）", not ok4)
    t("  且说明是 codec 形状", any("codec 形状" in x for x in probs4))

    # 空输入必须报
    ok5, probs5, _ = compare(man([]), A)
    t("★ 一侧为空 ⇒ 必须报（零值守卫）", not ok5)

    print(f"\n=== {n} PASS / {f} fail ===")
    print(f"=== {n} PASS / {f} FAIL ===")
    return 0 if f == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 2:
        print("用法: compare-release-payloads.py <a/manifest.json> <b/manifest.json> | --selftest",
              file=sys.stderr)
        return 2
    try:
        a = json.load(open(argv[0], encoding="utf-8"))
        b = json.load(open(argv[1], encoding="utf-8"))
    except (OSError, ValueError) as ex:
        print("FATAL: %s" % ex, file=sys.stderr)
        return 2
    ok, probs, note = compare(a, b)
    if ok:
        print("载荷对账：相同（%d 条载荷；%s）" % (len(a.get("entries") or []), note))
        return 0
    print("载荷对账：**不同**（%d 处）" % len(probs))
    for x in probs[:20]:
        print("  · " + x)
    print("  （%s）" % note)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
