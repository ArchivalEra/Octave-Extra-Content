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

# 已压缩格式：再压零收益（实测 MSL zip 19,482,938 → zstd 18,584,076，只省 4.6%，白花 20s CPU）
PRECOMPRESSED_EXT = (".zip", ".gz", ".br", ".zst", ".xz", ".whl", ".7z", ".rar",
                     ".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".webm",
                     ".woff2", ".tar.gz", ".tgz")


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
    """产一个变体：压缩 + 落盘 + 收集身份。

    ★ 命名约定（2026-10-30 实测硬约束）：GitHub Release 的 asset 名**会被拍平**
      （`gh release upload .../chunks/zstd/000.zst` 落成 `000.zst`，路径丢失）。
      所以分片用**扁平名 + 命名约定**：`<asset名>.<codec>.<序号>`，
      点号是合法分隔符，消费端按 `<name>.<codec>.<i>` 解析。
      `chunks[].file` 就是**纯 asset 名**（无路径）；base URL 由分发方提供。
    """
    parts = compress_blocks(blocks, codec)
    os.makedirs(outdir, exist_ok=True)
    chunks = []
    for i, p in enumerate(parts):
        name = f"{asset_name}.{codec}.{i:03d}"      # ← 扁平，无斜杠
        with open(os.path.join(outdir, name), "wb") as f:
            f.write(p)
        chunks.append({"i": i, "file": name,
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
    """为**多个**资产生成 manifest（v3 multi-asset：`assets` 是 map）。

    每个资产独立处理：> chunkSize 的分片 + 多编码；<= chunkSize 的只做 identity。
    """
    if chunk_size > MAX_CHUNK_HARD:
        raise SystemExit(f"chunkSize {chunk_size} > 2^25 (fzstd 上限)")
    if chunk_size > MAX_CHUNK_SOFT:
        print(f"⚠️ chunkSize {chunk_size} > 10 MiB —— 实测降速点在 10–20MB，可能落进降速区",
              file=sys.stderr)

    os.makedirs(outdir, exist_ok=True)
    assets = {}

    for f in files:
        raw = open(f, "rb").read()
        name = os.path.basename(f)
        # identity 兜底：原样拷进 outdir（I4：末位必须有）
        with open(os.path.join(outdir, name), "wb") as o:
            o.write(raw)
        variants = []
        is_pre = name.lower().endswith(PRECOMPRESSED_EXT)
        if is_pre:
            print(f"  {name}: 已压格式 ⇒ 只做 identity（分片仍做，但不重复压缩）")
            # 已压格式仍**分片**（为了走 5MB 快速通道），但不做 zstd/gzip 变体
            if len(raw) > chunk_size:
                # 分片 identity：直接用原字节切片，名 <name>.identity.<i>
                blocks = [raw[i:i + chunk_size] for i in range(0, len(raw), chunk_size)]
                chunks = []
                for i, b in enumerate(blocks):
                    fn = f"{name}.identity.{i:03d}"
                    open(os.path.join(outdir, fn), "wb").write(b)
                    chunks.append({"i": i, "file": fn, "bytes": len(b), "sha256": sha256(b)})
                variants.append({"codec": "identity-chunked",
                                 "totalBytes": len(raw), "chunked": True,
                                 "chunkSize": chunk_size, "chunks": chunks})
                print(f"     → identity 分片 {len(blocks)} 块")
        elif len(raw) > chunk_size:
            blocks = [raw[i:i + chunk_size] for i in range(0, len(raw), chunk_size)]
            for c in codecs:
                variants.append(build_variant(blocks, c, chunk_size, outdir, name))
            print(f"  {name}: {len(raw):,} B → {len(blocks)} 块 × {len(codecs)} 编码")
        elif len(raw) <= chunk_size:
            print(f"  {name}: {len(raw):,} B < chunkSize ⇒ 只做 identity（不分片）")
        variants.append({"codec": "identity", "totalBytes": len(raw),
                         "chunked": False, "file": name})
        assets[name] = {"bytes": len(raw), "sha256": sha256(raw), "variants": variants}

    if not assets:
        raise SystemExit("FATAL: 没有资产")

    man = {"schema": 1, "id": relid, "assets": assets}
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
        small2 = os.path.join(d, "side.zip")
        open(small2, "wb").write(b"PK fake zip content" * 100)   # < chunkSize
        out = os.path.join(d, "out")
        man = make([src, small2], out, "test/rel", chunk_size=5 * 1024 * 1024)
        A = man["assets"]["big.bin"]
        B = man["assets"]["side.zip"]
        t("正常：manifest 生成", os.path.exists(os.path.join(out, "manifest.json")))
        t("★ 多资产：assets 是 map 且有 2 项", isinstance(man["assets"], dict) and len(man["assets"]) == 2)
        t("正常：大资产 variants 有 zstd/gzip/identity",
          [v["codec"] for v in A["variants"]] == ["zstd", "gzip", "identity"])
        t("正常：小资产只有 identity", [v["codec"] for v in B["variants"]] == ["identity"])
        t("正常：每个资产 identity 都在末位",
          A["variants"][-1]["codec"] == "identity" and B["variants"][-1]["codec"] == "identity")
        t("正常：资产 sha 正确", A["sha256"] == sha256(data))
        t("正常：zstd 块数 = ceil(11MiB/5MiB) = 3", len(A["variants"][0]["chunks"]) == 3)
        t("I3：Σchunks == totalBytes（zstd）",
          sum(c["bytes"] for c in A["variants"][0]["chunks"]) == A["variants"][0]["totalBytes"])
        c0 = A["variants"][0]["chunks"][0]
        p0 = os.path.join(out, c0["file"])
        t("I2：块 sha 与落盘实件一致", sha256(open(p0, "rb").read()) == c0["sha256"])
        t("★ Release 兼容：asset 名扁平（无斜杠）", "/" not in c0["file"])
        t("★ 命名约定可解析（<name>.<codec>.<i>）",
          c0["file"].endswith(".zstd.000") and c0["file"].startswith("big.bin"))
        t("I2：块能解回原文（zstd）",
          __import__("zstandard").ZstdDecompressor()
             .decompress(open(p0, "rb").read(),
                         max_output_size=5 * 1024 * 1024) == data[:5 * 1024 * 1024])
        t("decoderBytes 是 ESM 的 6840（不是 UMD 的 3860）",
          A["variants"][0].get("decoderBytes") == 6840)

        # 该报：chunkSize 超 2^25
        try:
            make([src], os.path.join(d, "o2"), "t/r2", chunk_size=2 ** 26)
            t("该报（chunkSize > 2^25）⇒ 必拒", False)
        except SystemExit:
            t("该报（chunkSize > 2^25）⇒ 必拒", True)

        # 空输入：一个文件都没有 ⇒ 必拒
        try:
            make([], os.path.join(d, "o3"), "t/r3")
            t("空输入（无资产）⇒ 必拒", False)
        except SystemExit:
            t("空输入（无资产）⇒ 必拒", True)

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
    print(f"   id={man['id']}  assets={len(man['assets'])}")
    for an, av in man["assets"].items():
        print(f"     {an}: {av['bytes']:,} B  variants={[v['codec'] for v in av['variants']]}")
    print(f"\n校验: python3 tools/check-release-v2.py {os.path.join(a.out, 'manifest.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
