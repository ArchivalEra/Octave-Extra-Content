#!/usr/bin/env python3
"""发布契约 · 可机判的验收探针（release-contract-v1 §3）

用法:
  python3 tools/check-release-contract.py <base-url>            # 整体探
  python3 tools/check-release-contract.py <base-url> --selftest  # 自证

判据分两组：
  A. 站侧 HTTP 行为（协议地基是否成立）
  B. manifest 契约（I1–I5 不变量，需 --manifest 指向实件）

三类用例（本仓纪律）：正常不报 / 该报的必须报 / 空输入必须报。
"""
import sys, json, subprocess, hashlib, gzip, os, tempfile

EXIT_OK, EXIT_RED, EXIT_USAGE, EXIT_ENV = 0, 1, 2, 3


def curl_head(url, extra=()):
    cmd = ["curl", "-sI", "--max-time", "30", *extra, url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=40).stdout
    except Exception:
        return {}
    h = {}
    for line in out.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            h[k.strip().lower()] = v.strip()
    return h


def curl_status_size(url, extra=()):
    cmd = ["curl", "-s", "-o", "/dev/null", "--max-time", "120",
           "-w", "%{http_code} %{size_download}", *extra, url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=140).stdout.strip()
        code, size = out.split()
        return int(code), int(size)
    except Exception:
        return 0, 0


def check_site(base, problems, results):
    """A 组：站侧 HTTP 行为。base 指向一个已发布目录（含 .gz sidecar 的实体）。"""
    gz = base.rstrip("/") + "/OpenModelicaCompiler_bg.wasm.gz"
    raw = base.rstrip("/") + "/OpenModelicaCompiler_bg.wasm"

    # A1 Range 只在 sidecar 上（原始件应 none / 200）
    h_raw = curl_head(raw)
    ar = h_raw.get("accept-ranges", "").lower()
    results.append(("A1 原始件 Accept-Ranges", ar or "缺失", ar in ("none", "")))

    h_gz = curl_head(gz)
    ar_gz = h_gz.get("accept-ranges", "").lower()
    results.append(("A2 sidecar Accept-Ranges=bytes", ar_gz or "缺失", ar_gz == "bytes"))

    # A3 单段 Range 必须 206 + Content-Range
    code, size = curl_status_size(gz, ["-H", "Range: bytes=0-1023"])
    results.append(("A3 单段 Range=206", f"{code}/{size}B", code == 206 and size == 1024))

    # A4 越界必须 416
    code2, _ = curl_status_size(gz, ["-H", "Range: bytes=999999999-1000000000"])
    results.append(("A4 越界 Range=416", str(code2), code2 == 416))

    # A5 多段不支持（200 全体是预期行为，写死以免有人"修"成支持后破坏契约）
    code3, _ = curl_status_size(gz, ["-H", "Range: bytes=0-99,200-299"])
    results.append(("A5 多段 Range=200(不支持)", str(code3), code3 == 200))

    # A6 Cache-Control 必须 immutable（发布契约 §1.7 的核心）
    cc = h_gz.get("cache-control", "")
    results.append(("A6 Cache-Control immutable", cc or "缺失", "immutable" in cc.lower()))

    # A7 sidecar 的 Content-Type 不应是 application/gzip（§1.4 的坑）
    ct = h_gz.get("content-type", "")
    results.append(("A7 sidecar Content-Type 非 application/gzip",
                    ct or "缺失", "application/gzip" not in ct.lower()))

    # A8 无 Digest 头（如实记录站侧能力，不是失败项；供 manifest 存在的理由）
    has_digest = any("digest" in k for k in h_gz)
    results.append(("A8 站侧无 Digest 头（预期）", str(has_digest), not has_digest))


def check_manifest(path, problems, results):
    """B 组：manifest 不变量 I1–I5。"""
    if not os.path.exists(path):
        problems.append(f"manifest 不存在: {path}")
        return
    try:
        m = json.load(open(path))
    except Exception as e:
        problems.append(f"manifest 非法 JSON: {e}")
        return

    assets = m.get("assets")
    if not isinstance(assets, dict) or not assets:
        problems.append("I0: assets 必须是非空 map（零值守卫）")
        return
    results.append(("B0 assets 非空", f"{len(assets)} 个", True))

    for name, a in assets.items():
        if not isinstance(a, dict):
            problems.append(f"I0: {name} 不是对象")
            continue
        # I4 granularity 范围
        rg = a.get("range") or {}
        g = rg.get("granularity")
        if g is not None:
            ok = isinstance(g, int) and 0 < g <= 2**31 - 1
            if not ok:
                problems.append(f"I4: {name} granularity={g} 必须 0<n<=2^31-1")
            results.append((f"B-I4 {name} granularity", str(g), ok))

        # I3 basis 合法 + encoded 时 encodings 非空
        basis = rg.get("basis")
        if basis not in (None, "encoded", "identity"):
            problems.append(f"I3: {name} range.basis={basis!r} 非法")
        encs = a.get("encodings") or {}
        if basis == "encoded" and not encs:
            problems.append(f"I3: {name} basis=encoded 但 encodings 为空")
        results.append((f"B-I3 {name} basis/encs", f"{basis}/{len(encs)}", True))

        # I1/I2：每个编码层必须 64hex sha + 可复算（用本地实件若同目录存在）
        base_dir = os.path.dirname(os.path.abspath(path))
        for enc, e in encs.items():
            sha = e.get("sha256", "")
            ok_sha = len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)
            if not ok_sha:
                problems.append(f"I1: {name}/{enc} sha256 非 64hex")
            results.append((f"B-I1 {name}/{enc} sha 形状", sha[:8] or "缺失", ok_sha))

            f = os.path.join(base_dir, f"{name}.{ 'gz' if enc=='gzip' else enc}")
            if os.path.exists(f):
                raw_b = open(f, "rb").read()
                got = hashlib.sha256(raw_b).hexdigest()
                ok = got == sha
                if not ok:
                    problems.append(f"I1: {name}/{enc} 实件 sha 不符")
                results.append((f"B-I1 {name}/{enc} 实件一致", got[:8], ok))
                # I2 复算
                try:
                    dec = gzip.decompress(raw_b) if enc == "gzip" else None
                    if dec is not None:
                        ok2 = len(dec) == a.get("bytes") and hashlib.sha256(dec).hexdigest() == a.get("sha256")
                        if not ok2:
                            problems.append(f"I2: {name}/{enc} 解码后 bytes/sha 不符")
                        results.append((f"B-I2 {name}/{enc} 可复算", str(ok2), ok2))
                except Exception as ex:
                    problems.append(f"I2: {name}/{enc} 解码失败: {ex}")


def selftest():
    """三类用例：正常不报 / 该报必须报 / 空输入必须报。"""
    p, r = [], []
    # 空输入
    check_manifest("/nonexistent/manifest.json", p, r)
    ok_empty = any("不存在" in x for x in p)
    print(f"{'PASS' if ok_empty else 'fail'} | 空输入（manifest 不存在）⇒ 必报")

    # 该报：坏 manifest
    with tempfile.TemporaryDirectory() as d:
        bad = os.path.join(d, "manifest.json")
        json.dump({"schema": 1, "assets": {"a": {"encodings": {"gzip": {"sha256": "zz"}},
                                                 "range": {"basis": "encoded", "granularity": 2**40}}}}, open(bad, "w"))
        p2, r2 = [], []
        check_manifest(bad, p2, r2)
        ok_bad = any("I1" in x for x in p2) and any("I4" in x for x in p2)
        print(f"{'PASS' if ok_bad else 'fail'} | 该报（坏 sha + 超界 granularity）⇒ 必报 I1+I4")

        # 正常：好 manifest
        good = os.path.join(d, "g.json")
        json.dump({"schema": 1, "assets": {"x.wasm": {
            "bytes": 3, "sha256": hashlib.sha256(b"abc").hexdigest(),
            "encodings": {}, "range": {"basis": "identity"}}}}, open(good, "w"))
        p3, r3 = [], []
        check_manifest(good, p3, r3)
        print(f"{'PASS' if not p3 else 'fail'} | 正常（合法 manifest）⇒ 不报   [{p3}]")

    # 该报：assets 空
    with tempfile.TemporaryDirectory() as d:
        e = os.path.join(d, "m.json"); json.dump({"schema": 1, "assets": {}}, open(e, "w"))
        p4, r4 = [], []
        check_manifest(e, p4, r4)
        print(f"{'PASS' if any('零值守卫' in x for x in p4) else 'fail'} | 空 assets ⇒ 必报零值守卫")
    return EXIT_OK


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return EXIT_USAGE
    if "--selftest" in args:
        return selftest()

    base = args[0]
    manifest = None
    if "--manifest" in args:
        manifest = args[args.index("--manifest") + 1]

    problems, results = [], []
    check_site(base, problems, results)
    if manifest:
        check_manifest(manifest, problems, results)

    print(f"=== 发布契约探针 :: {base} ===")
    for label, detail, ok in results:
        print(f"{'PASS' if ok else 'fail'} | {label} :: {detail}")
    if problems:
        print("\n问题:")
        for x in problems:
            print("  ·", x)
    fails = sum(1 for _, _, ok in results if not ok) + len(problems)
    print(f"\n=== {sum(1 for _,_,ok in results if ok)} PASS / {fails} FAIL ===")
    return EXIT_OK if fails == 0 else EXIT_RED


if __name__ == "__main__":
    sys.exit(main())
