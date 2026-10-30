#!/usr/bin/env python3
"""发布契约 v2 校验器：I1–I7 不变量。fail-closed。

用法:
  python3 tools/check-release-v2.py <manifest.json>             # 校验实件
  python3 tools/check-release-v2.py --selftest                   # 三类用例自证
"""
import sys, json, os, hashlib, gzip, tempfile

EXIT_OK, EXIT_RED, EXIT_USAGE = 0, 1, 2
MAX_CHUNK = 2**25          # I6: fzstd backreference 上限 32MiB
HEX = set("0123456789abcdef")

def is_hex64(s):
    return isinstance(s, str) and len(s) == 64 and set(s) <= HEX

def check(man, base_dir=None):
    """返回 (results, problems)。results = [(label, detail, ok)]"""
    R, P = [], []
    def ok(label, detail, cond, why=None):
        R.append((label, detail, cond))
        if not cond:
            P.append(f"{label}: {detail}" + (f" —— {why}" if why else ""))

    if not isinstance(man, dict):
        P.append("I0: manifest 必须是对象"); return R, P

    # 顶层
    ok("I1 顶层 sha256 形状", str(man.get("sha256"))[:8], is_hex64(man.get("sha256")))
    ok("I1 顶层 bytes 正整数", str(man.get("bytes")), isinstance(man.get("bytes"), int) and man["bytes"] > 0)

    vs = man.get("variants")
    ok("I4 variants 非空数组", f"{type(vs).__name__}", isinstance(vs, list) and len(vs) > 0)
    if not isinstance(vs, list) or not vs:
        return R, P

    # I4: 恰有一个 identity 且在末位
    idcs = [i for i, v in enumerate(vs) if isinstance(v, dict) and v.get("codec") == "identity"]
    ok("I4 恰有一个 identity 兜底", f"位置={idcs}", len(idcs) == 1)
    ok("I4 identity 在末位", f"末位={len(vs)-1}", idcs and idcs[0] == len(vs) - 1)

    # I7: codec 是开放字符串（不是枚举）——这里只能检查"不是空/不是数字"
    for i, v in enumerate(vs):
        c = v.get("codec") if isinstance(v, dict) else None
        ok(f"I7 variants[{i}] codec 是非空字符串", repr(c), isinstance(c, str) and c != "")

    # 逐变体
    for i, v in enumerate(vs):
        if not isinstance(v, dict):
            P.append(f"I5: variants[{i}] 不是对象"); continue
        codec = v.get("codec"); chunked = v.get("chunked")
        tb = v.get("totalBytes")
        ok(f"I3 variants[{i}] totalBytes 正整数", str(tb), isinstance(tb, int) and tb > 0)

        if chunked is True:
            cs = v.get("chunkSize")
            ok(f"I5 variants[{i}] chunked⇒chunkSize 必填", str(cs), isinstance(cs, int) and cs > 0)
            if isinstance(cs, int) and cs > 0:
                ok(f"I6 variants[{i}] chunkSize ≤ 2^25", f"{cs} vs {MAX_CHUNK}", cs <= MAX_CHUNK)
            chs = v.get("chunks")
            ok(f"I5 variants[{i}] chunked⇒chunks 非空", f"{type(chs).__name__}", isinstance(chs, list) and len(chs) > 0)
            if isinstance(chs, list):
                tot = 0; allok = True
                for j, c in enumerate(chs):
                    if not isinstance(c, dict): allok = False; P.append(f"I5: variants[{i}].chunks[{j}] 非对象"); continue
                    if not is_hex64(c.get("sha256")):
                        allok = False; P.append(f"I2: variants[{i}].chunks[{j}] sha256 非 64hex")
                    if not (isinstance(c.get("bytes"), int) and c["bytes"] > 0):
                        allok = False; P.append(f"I5: variants[{i}].chunks[{j}] bytes 非法")
                    if not isinstance(c.get("file"), str):
                        allok = False; P.append(f"I5: variants[{i}].chunks[{j}] file 缺失")
                    tot += c.get("bytes", 0) if isinstance(c.get("bytes"), int) else 0
                ok(f"I2 variants[{i}] chunks sha 形状齐", f"{len(chs)} 块", allok)
                ok(f"I3 variants[{i}] Σchunks.bytes == totalBytes", f"{tot} vs {tb}", tot == tb)
        elif chunked is False:
            ok(f"I5 variants[{i}] 非分片⇒有 file 无 chunks",
               str(v.get("file")), isinstance(v.get("file"), str) and "chunks" not in v)
        else:
            P.append(f"I5: variants[{i}] chunked 必须是 true/false")

    # 若给了 base_dir 且有 identity 单文件：实件核对 I1
    if base_dir:
        for v in vs:
            if v.get("codec") == "identity" and isinstance(v.get("file"), str):
                f = os.path.join(base_dir, v["file"])
                if os.path.exists(f):
                    b = open(f, "rb").read()
                    ok("I1 identity 实件 bytes 一致", f"{len(b)}", len(b) == man.get("bytes"))
                    ok("I1 identity 实件 sha 一致", hashlib.sha256(b).hexdigest()[:8],
                       hashlib.sha256(b).hexdigest() == man.get("sha256"))
    return R, P


def selftest():
    n_pass = n_fail = 0
    def t(label, cond):
        nonlocal n_pass, n_fail
        if cond: n_pass += 1; print(f"PASS | {label}")
        else: n_fail += 1; print(f"fail | {label}")

    # ① 正常：合法 manifest 不报
    good = {"schema":1,"id":"x/y","bytes":100,"sha256":"a"*64,"variants":[
        {"codec":"zstd","totalBytes":60,"chunked":True,"chunkSize":5*1024*1024,
         "chunks":[{"i":0,"file":"chunks/zstd/000.zst","bytes":60,"sha256":"b"*64}]},
        {"codec":"identity","totalBytes":100,"chunked":False,"file":"a.wasm"}]}
    _, P = check(good); t("正常（合法 manifest）⇒ 不报", not P)

    # ② 该报：缺 identity 兜底
    bad1 = json.loads(json.dumps(good)); bad1["variants"] = bad1["variants"][:1]
    _, P = check(bad1); t("该报（无 identity 兜底）⇒ 必报 I4", any("I4" in x for x in P))

    # ③ 该报：chunkSize 超 2^25
    bad2 = json.loads(json.dumps(good)); bad2["variants"][0]["chunkSize"] = 2**26
    _, P = check(bad2); t("该报（chunkSize > 2^25）⇒ 必报 I6", any("I6" in x for x in P))

    # ④ 该报：Σchunks != totalBytes
    bad3 = json.loads(json.dumps(good)); bad3["variants"][0]["chunks"][0]["bytes"] = 1
    _, P = check(bad3); t("该报（Σchunks ≠ totalBytes）⇒ 必报 I3", any("I3" in x for x in P))

    # ⑤ 该报：块 sha 非 hex
    bad4 = json.loads(json.dumps(good)); bad4["variants"][0]["chunks"][0]["sha256"] = "zz"
    _, P = check(bad4); t("该报（块 sha 非 64hex）⇒ 必报 I2", any("I2" in x for x in P))

    # ⑥ 空输入：变体为空
    _, P = check({"schema":1,"bytes":1,"sha256":"a"*64,"variants":[]})
    t("空输入（variants 空）⇒ 必报 I4", any("I4" in x for x in P))

    # ⑦ 空输入：非对象
    _, P = check([]); t("空输入（根非对象）⇒ 必报 I0", any("I0" in x for x in P))

    print(f"\n=== {n_pass} PASS / {n_fail} fail ===")
    return EXIT_OK if n_fail == 0 else EXIT_RED


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return EXIT_USAGE
    if "--selftest" in a: return selftest()
    f = a[0]
    if not os.path.exists(f): print(f"FATAL: 不存在 {f}"); return EXIT_RED
    try: man = json.load(open(f))
    except Exception as e: print(f"FATAL: 非法 JSON {e}"); return EXIT_RED
    R, P = check(man, base_dir=os.path.dirname(os.path.abspath(f)))
    for label, detail, ok in R:
        print(f"{'PASS' if ok else 'fail'} | {label} :: {detail}")
    if P:
        print("\n问题:")
        for x in P: print("  ·", x)
    fails = sum(1 for _,_,ok in R if not ok) + len(P)
    print(f"\n=== {sum(1 for _,_,ok in R if ok)} PASS / {fails} FAIL ===")
    return EXIT_OK if fails == 0 else EXIT_RED

if __name__ == "__main__":
    sys.exit(main())
