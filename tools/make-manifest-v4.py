#!/usr/bin/env python3
"""发布契约 v4 · manifest 生成器

v4 相对 v3 的核心变化：
  1. 名字字符白名单（实测 GitHub 静默改写面 → 只允许不会被改写的字符）
  2. products{} 分组解决「跨 arch 同名不同字节」（optim 5/5 撞车，实测）
  3. 每条 entry 自足（apt 稳健性：不靠 blob 间接，重复写 sha 换"单条可用"）
  4. file 字段 == asset 名（白名单保证 GitHub 逐字保留 ⇒ 不需要映射表）

用法:
  python3 tools/make-manifest-v4.py --out DIR --id ID \
      --product src:tmpl:--:file.tar.gz \
      --product wasm32:octdir:wasm32:dir/ \
      --selftest
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import sys
import tempfile

CHUNK = 5 * 1024 * 1024
MAX_CHUNK_HARD = 2 ** 25

# ★ 实测得到的白名单（GitHub 逐字保留）：
#   OK:      a.b_c-D9.zstd.000 / UPPER.Mixed.Case.000 / under_score / hy-phen / -leading
#   CHANGED: dots...many.000 → dots.many.000（连续点折叠）
#            .leading-dot    → default.leading-dot
#            trailing-dot.   → default.trailing-dot
NAME_RE = re.compile(r"^[A-Za-z0-9_-][A-Za-z0-9._-]*$")

PRECOMPRESSED = (".zip", ".gz", ".br", ".zst", ".xz", ".whl", ".7z", ".rar", ".tgz",
                 ".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".webm", ".woff2")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def name_ok(n):
    """名字能否通过 GitHub 逐字保留。返回 (ok, reason)。"""
    if len(n) > 255:
        return False, "长度 > 255"
    if not NAME_RE.match(n):
        return False, "不符合白名单 ^[A-Za-z0-9_-][A-Za-z0-9._-]*$"
    if ".." in n:
        return False, "含连续点（会被折叠）"
    if n.endswith("."):
        return False, "以点结尾（会被加前缀）"
    return True, ""


def compress_blocks(blocks, codec):
    if codec == "gzip":
        return [gzip.compress(b, 9) for b in blocks]
    if codec == "zstd":
        import zstandard as zstd
        c = zstd.ZstdCompressor(level=19)
        return [c.compress(b) for b in blocks]
    if codec == "identity":
        return list(blocks)
    raise ValueError(codec)


def build_variants(raw, prefix, codecs, outdir, name_ctx):
    """为一个载荷产出 variants[]（每块独立压缩）。name_ctx = 名字前缀（不含 codec/序号）。"""
    blocks = [raw[i:i + CHUNK] for i in range(0, len(raw), CHUNK)]
    variants = []
    for codec, pfx in codecs:
        parts = compress_blocks(blocks, codec)
        chunks = []
        for i, p in enumerate(parts):
            fn = f"{name_ctx}.{codec}.{i:03d}"
            ok, why = name_ok(fn)
            if not ok:
                raise SystemExit(f"FATAL: 名字不合法 {fn!r}: {why}")
            with open(os.path.join(outdir, fn), "wb") as f:
                f.write(p)
            chunks.append({"part": i, "file": fn, "bytes": len(p), "sha256": sha256(p)})
        variants.append({"codec": codec, "chunks": chunks})
    return variants, len(blocks)


def make(spec, outdir, relid, codecs=(("zstd", "z"), ("gzip", "g"), ("identity", "i")),
         chunk=CHUNK):
    """spec = [ {product, form, arch, src, files:[path,...]} ]"""
    if chunk > MAX_CHUNK_HARD:
        raise SystemExit(f"chunkSize {chunk} > 2^25")
    os.makedirs(outdir, exist_ok=True)

    products = {}
    entries = []
    for p in spec:
        pid = p["product"]
        products[pid] = {"form": p["form"]}
        if p.get("arch"):
            products[pid]["arch"] = p["arch"]
        if "src" in p:
            products[pid]["src"] = p["src"]

        for fp in p["files"]:
            raw = open(fp, "rb").read()
            base = os.path.basename(fp)
            tag = p.get("arch") or "src"
            name_ctx = f"{tag}__{base}"
            # 已压格式：只出 identity（实测 zip 再压只省 4.6%，白花 CPU）
            is_pre = base.lower().endswith(PRECOMPRESSED)
            use = [("identity", "i")] if is_pre else list(codecs)
            variants, nchunks = build_variants(raw, None, use, outdir, name_ctx)
            entries.append({
                "product": pid, "name": base,
                "bytes": len(raw), "sha256": sha256(raw),
                "variants": variants,
            })
            print(f"  {pid}/{base}: {len(raw):,} B → {nchunks} 块 × {len(variants)} 编码"
                  + ("  [已压格式只出 identity]" if is_pre else ""))

    if not entries:
        raise SystemExit("FATAL: 没有条目")

    man = {"schema": 2, "id": relid, "chunkSize": chunk,
           "codecs": [{"codec": c, "prefix": p} for c, p in codecs],
           "products": products, "entries": entries}
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1)
    return man


def selftest():
    n = f = 0

    def t(label, cond):
        nonlocal n, f
        if cond:
            n += 1; print(f"PASS | {label}")
        else:
            f += 1; print(f"fail | {label}")

    # ① 白名单：实测的三个改写案例必须被拦
    t("白名单：正常名通过", name_ok("w32__a.oct.zstd.000")[0])
    t("白名单：大写通过（实测 OK）", name_ok("UPPER.Mixed.Case.000")[0])
    t("白名单：下划线/连字符通过", name_ok("a_b-c.000")[0])
    t("★ 白名单：连续点必须拒（实测 dots...many → dots.many）",
      not name_ok("dots...many.000")[0])
    t("★ 白名单：前导点必须拒（实测 .x → default.x）",
      not name_ok(".leading-dot")[0])
    t("★ 白名单：尾点必须拒（实测 x. → default.x）",
      not name_ok("trailing-dot.")[0])
    t("白名单：含空格必须拒", not name_ok("sp ace.bin")[0])
    t("白名单：含斜杠必须拒", not name_ok("a/b.bin")[0])
    t("白名单：含中文必须拒", not name_ok("a中b.bin")[0])
    t("白名单：含百分号必须拒", not name_ok("pct%41.bin")[0])

    with tempfile.TemporaryDirectory() as d:
        # ② 造两个跨 arch 同名不同字节的载荷（复刻 optim 真实形状）
        for arch, size in (("wasm32", 11 * 1024 * 1024), ("wasm64", 12 * 1024 * 1024)):
            sub = os.path.join(d, arch)
            os.makedirs(sub)
            open(os.path.join(sub, "numgradient.oct"), "wb").write(os.urandom(size))
        src = os.path.join(d, "optim-1.6.3.tar.gz")
        open(src, "wb").write(os.urandom(300 * 1024))

        out = os.path.join(d, "out")
        man = make([
            {"product": "src", "form": "pkg", "files": [src]},
            {"product": "wasm32", "form": "octdir", "arch": "wasm32", "src": "src",
             "files": [os.path.join(d, "wasm32", "numgradient.oct")]},
            {"product": "wasm64", "form": "octdir", "arch": "wasm64", "src": "src",
             "files": [os.path.join(d, "wasm64", "numgradient.oct")]},
        ], out, "test/optim-1.6.3", chunk=5 * 1024 * 1024, codecs=(("gzip", "g"), ("identity", "i")))

        t("v4：products 有 3 个（src + 两 arch）", len(man["products"]) == 3)
        t("v4：src 边存在", man["products"]["wasm32"].get("src") == "src")
        t("★ v4：跨 arch 同名不同字节 = 2 条独立 entry（不塌陷）",
          sum(1 for e in man["entries"] if e["name"] == "numgradient.oct") == 2)
        t("★ v4：两条 entry 的 sha 不同（真不同字节）",
          len({e["sha256"] for e in man["entries"] if e["name"] == "numgradient.oct"}) == 2)
        t("v4：已压格式只出 identity",
          [v["codec"] for v in next(e for e in man["entries"]
                                    if e["name"].endswith(".tar.gz"))["variants"]] == ["identity"])
        t("★ v4：11MiB 载荷被切成 3 块（5MiB×2 + 余）",
          len(man["entries"][1]["variants"][0]["chunks"]) == 3)
        t("★ v4：所有 file 名通过白名单",
          all(name_ok(c["file"])[0] for e in man["entries"]
              for v in e["variants"] for c in v["chunks"]))
        t("★ v4：所有 file 名全局唯一",
          len({c["file"] for e in man["entries"] for v in e["variants"]
               for c in v["chunks"]}) == sum(len(v["chunks"]) for e in man["entries"]
                                             for v in e["variants"]))
        # 块能独立解回
        import gzip as gz
        e = man["entries"][1]
        c = e["variants"][0]["chunks"][0]
        blob = open(os.path.join(out, c["file"]), "rb").read()
        t("I2：块能独立解压（gzip）", gz.decompress(blob) ==
          open(os.path.join(d, "wasm32", "numgradient.oct"), "rb").read()[:5 * 1024 * 1024])
        # 超界必拒
        try:
            make([{"product": "x", "form": "file", "files": [src]}],
                 os.path.join(d, "o2"), "t/x", chunk=2 ** 26)
            t("该报（chunkSize > 2^25）⇒ 必拒", False)
        except SystemExit:
            t("该报（chunkSize > 2^25）⇒ 必拒", True)
        # 空输入必拒
        try:
            make([], os.path.join(d, "o3"), "t/e")
            t("空输入（无条目）⇒ 必拒", False)
        except SystemExit:
            t("空输入（无条目）⇒ 必拒", True)

    print(f"\n=== {n} PASS / {f} fail ===")
    return 0 if f == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--id", dest="relid")
    ap.add_argument("--product", action="append", default=[],
                    help="pid:form[:arch][:src]:path  （path 是文件或目录）")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.out and a.relid and a.product):
        ap.print_help(); return 2

    spec = []
    for ps in a.product:
        parts = ps.rsplit(":", 1)
        meta, path = parts[0].split(":"), parts[1]
        pid, form = meta[0], meta[1]
        arch = meta[2] if len(meta) > 2 and meta[2] else None
        srcp = meta[3] if len(meta) > 3 else None
        files = ([os.path.join(path, x) for x in sorted(os.listdir(path))]
                 if os.path.isdir(path) else [path])
        d = {"product": pid, "form": form, "files": files}
        if arch: d["arch"] = arch
        if srcp: d["src"] = srcp
        spec.append(d)

    man = make(spec, a.out, a.relid)
    print(f"\n✅ {os.path.join(a.out, 'manifest.json')}")
    print(f"   id={man['id']}  products={list(man['products'])}  entries={len(man['entries'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
