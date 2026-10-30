#!/usr/bin/env python3
"""发布契约 v3 · manifest 生成器（试点用）

把产物文件 → 分块压缩 → 算 sha → 写 manifest.json。
这是「落地顺序第 2 步」缺的那件工具：没有它，试点要手工拼 manifest（易错且不可复现）。

用法:
  python3 tools/make-release-manifest.py --out <dir> --id <repo/tag> <file> [<file>...]
  python3 tools/make-release-manifest.py --selftest

判据（每条都可复跑）:
  · 每块 sha256 = 该编码块**字节**的 sha（I2）
  · Σchunks.bytes == variants[].totalBytes（I3）
  · 恰有一个 identity 在末位（I4）
  · chunkSize ≤ 2^25 且 ≤ 10 MiB（I6，默认 5 MiB）
  · 生成后用 tools/check-release-v2.py 校验应全绿

依赖: zstandard (pip install zstandard)。gzip 用标准库。
"""
import argparse
import gzip
import hashlib
import json
import os
import sys
import tempfile

MAX_CHUNK_HARD = 2 ** 25      # fzstd backreference 上限
MAX_CHUNK_SOFT = 10 * 1024 * 1024   # 实测降速点在 10–20MB，超此落进降速区
DEFAULT_CHUNK = 5 * 1024 * 1024     # 5 MiB（用户定的上限值）


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def compress_blocks(blocks, codec):
    """每块**独立**压缩（I6 要求；且分块压缩本就没有跨块 backreference）。"""
    if codec == "gzip":
        return [gzip.compress(b, 9) for b in blocks]
    if codec == "zstd":
        import zstandard as zstd
        c = zstd.ZstdCompressor(level=19)
        return [c.compress(b) for b in blocks]
    raise ValueError(codec)


def build_variant(blocks, codec, chunk_size, outdir, asset_name):
    """产一个变体：压缩 + 落盘 + 收集身份。"""
    parts = compress_blocks(blocks, codec)
    d = os.path.join(outdir, "chunks", codec)
    os.makedirs(d, exist_ok=True)
    ext = {"gzip": "gzip", "zstd": "zstd"}[codec]
    chunks = []
    for i, p in enumerate(parts):
        name = f"{i:03d}.{ext}"
        with open(os.path.join(d, name), "wb") as f:
            f.write(p)
        chunks.append({"i": i, "file": f"chunks/{codec}/{name}",
                       "bytes": len(p), "sha256": sha256(p)})
    v = {"codec": codec, "totalBytes": sum(len(p) for p in parts),
         "chunked": True, "chunkSize": chunk_size, "chunks": chunks}
    if codec == "zstd":
        # ESM 实际负担 6,840 B（gzip 后）——不是 UMD 的 3,860 B（Shirone mail/117 纠）
        v["decoder"] = "fzstd@0.1.1"
        v["decoderBytes"] = 6840
        v["decoderForm"] = "esm"
    return v


def make(files, outdir, relid, chunk_size=DEFAULT_CHUNK, codecs=("zstd", "gzip")):
    """为**单个**主资产生成 manifest（试点只做单资产；多资产留待后续）。"""
    if chunk_size > MAX_CHUNK_HARD:
        raise SystemExit(f"chunkSize {chunk_size} > 2^25 (fzstd 上限)")
    if chunk_size > MAX_CHUNK_SOFT:
        print(f"⚠️ chunkSize {chunk_size} > 10 MiB —— 实测降速点在 10–20MB，可能落进降速区",
              file=sys.stderr)

    os.makedirs(outdir, exist_ok=True)
    total_bytes = 0
    variants = []
    primary = None

    for f in files:
        raw = open(f, "rb").read()
        name = os.path.basename(f)
        if len(raw) > chunk_size:
            if primary is None:
                primary = name
                total_bytes = len(raw)
                # identity 兜底：原样拷进 outdir（I4：末位必须有）
                with open(os.path.join(outdir, name), "wb") as o:
                    o.write(raw)
                blocks = [raw[i:i + chunk_size] for i in range(0, len(raw), chunk_size)]
                for c in codecs:
                    variants.append(build_variant(blocks, c, chunk_size, outdir, name))
                print(f"  {name}: {len(raw):,} B → {len(blocks)} 块 × {len(codecs)} 编码")
            else:
                print(f"  ⚠️ 跳过 {name}（试点只做单个主资产；多资产待后续）", file=sys.stderr)
        else:
            print(f"  ⚠️ 跳过 {name}（{len(raw):,} B < chunkSize，小件不分片）", file=sys.stderr)

    if primary is None:
        raise SystemExit("FATAL: 没有大于 chunkSize 的资产 —— 无需分片")

    raw = open(os.path.join(outdir, primary), "rb").read()
    variants.append({"codec": "identity", "totalBytes": len(raw),
                     "chunked": False, "file": primary})

    man = {"schema": 1, "id": relid, "bytes": total_bytes,
           "sha256": sha256(raw), "variants": variants}
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1)
    return man


def selftest():
    """三类用例：正常 / 该报（超界）/ 空输入。"""
    n_pass = n_fail = 0

    def t(label, cond):
        nonlocal n_pass, n_fail
        if cond:
            n_pass += 1; print(f"PASS | {label}")
        else:
            n_fail += 1; print(f"fail | {label}")

    with tempfile.TemporaryDirectory() as d:
        # 造一个 11 MiB 随机件（> 2×5MiB 块，能分 3 块）
        src = os.path.join(d, "big.bin")
        data = os.urandom(11 * 1024 * 1024)
        open(src, "wb").write(data)
        out = os.path.join(d, "out")
        man = make([src], out, "test/rel", chunk_size=5 * 1024 * 1024)
        t("正常：manifest 生成", os.path.exists(os.path.join(out, "manifest.json")))
        t("正常：variants 有 zstd/gzip/identity",
          [v["codec"] for v in man["variants"]] == ["zstd", "gzip", "identity"])
        t("正常：identity 在末位", man["variants"][-1]["codec"] == "identity")
        t("正常：全局 sha 正确", man["sha256"] == sha256(data))
        t("正常：zstd 块数 = ceil(11MiB/5MiB) = 3",
          len(man["variants"][0]["chunks"]) == 3)
        t("I3：Σchunks == totalBytes（zstd）",
          sum(c["bytes"] for c in man["variants"][0]["chunks"])
          == man["variants"][0]["totalBytes"])
        # 实件核对：块 sha 与落盘一致
        c0 = man["variants"][0]["chunks"][0]
        p0 = os.path.join(out, c0["file"])
        t("I2：块 sha 与落盘实件一致", sha256(open(p0, "rb").read()) == c0["sha256"])
        t("I2：块能解回原文（zstd）",
          (lambda: __import__("zstandard").ZstdDecompressor()
             .decompress(open(p0, "rb").read(),
                         max_output_size=5 * 1024 * 1024) == data[:5 * 1024 * 1024])())
        t("decoderBytes 是 ESM 的 6840（不是 UMD 的 3860）",
          man["variants"][0].get("decoderBytes") == 6840)

        # 该报：chunkSize 超 2^25
        try:
            make([src], os.path.join(d, "o2"), "t/r2", chunk_size=2 ** 26)
            t("该报（chunkSize > 2^25）⇒ 必拒", False)
        except SystemExit:
            t("该报（chunkSize > 2^25）⇒ 必拒", True)

        # 空输入：文件小于 chunkSize ⇒ 无可分片
        small = os.path.join(d, "small.bin")
        open(small, "wb").write(b"tiny")
        try:
            make([small], os.path.join(d, "o3"), "t/r3", chunk_size=5 * 1024 * 1024)
            t("空输入（小件 < chunkSize）⇒ 必拒", False)
        except SystemExit:
            t("空输入（小件 < chunkSize）⇒ 必拒", True)

    print(f"\n=== {n_pass} PASS / {n_fail} fail ===")
    return 0 if n_fail == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="发布契约 v3 manifest 生成器")
    ap.add_argument("--out", help="输出目录")
    ap.add_argument("--id", dest="relid", help="release 身份，如 OpenModelica-Full-Wasm/v0.1.0-wasm32")
    ap.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK,
                    help=f"块大小字节，默认 {DEFAULT_CHUNK}（5 MiB）")
    ap.add_argument("--codecs", default="zstd,gzip", help="逗号分隔，默认 zstd,gzip")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not (a.out and a.relid and a.files):
        ap.print_help()
        return 2
    man = make(a.files, a.out, a.relid, a.chunk_size,
               tuple(x.strip() for x in a.codecs.split(",") if x.strip()))
    print(f"\n✅ {os.path.join(a.out, 'manifest.json')}")
    print(f"   id={man['id']}  bytes={man['bytes']:,}  variants={[v['codec'] for v in man['variants']]}")
    print(f"\n校验: python3 tools/check-release-v2.py {os.path.join(a.out, 'manifest.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
