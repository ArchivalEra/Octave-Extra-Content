#!/usr/bin/env python3
"""把已有 release 的 manifest 升到 schema 3（加 license），只替换 manifest.json。

依据 Static-Contract `mail/119`（v1.1 契约）：
  manifest 加一项 `license: {id, url}`，schema 2 → 3。
  **asset 一个都不用动** —— v4 的 asset 集合由 manifest 的 `file` 字段定义，
  只要 `bytes`/`sha256`/`file` 逐字不变，就只换 `manifest.json` 这一个 asset。

许可真值来自本仓 `packages/*.json` 的 `upstream.links` 里 `icon` 含 `copyright` 的那条：
  · `label` → SPDX 归一化后作 `license.id`（`and`→`AND`、`public domain`→`LicenseRef-public-domain`）
  · `url`   → `license.url`（权威正文的当前位置）
能力层（supply-*）的许可在 `recipes/*.md` 里，硬编码在本脚本的 OVERRIDE 中。

用法：
    python3 tools/upgrade-manifest-license.py --dry-run          # 只打印计划
    python3 tools/upgrade-manifest-license.py --out /tmp/upg     # 生成新 manifest 到目录
    python3 tools/upgrade-manifest-license.py --selftest          # 自证（不联网）

⚠️ 本脚本**不上传**。上传是单独一步（`gh release upload --clobber`），
   因为「生成」与「发布」必须能分开验证。
"""
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 能力层的许可不在 packages/ 里（它们是 recipes/ 描述的外部资产）
OVERRIDE = {
    "supply-msl-4.1.0": {
        "id": "BSD-3-Clause",
        "url": "https://github.com/OpenModelica/OpenModelica-ModelicaStandardLibrary/blob/master/LICENSE",
    },
    "supply-pyodide-314.0.7": {
        # Pyodide core 是 MPL-2.0；sympy/mpmath 是 BSD-3-Clause。复合表达式。
        "id": "MPL-2.0 AND BSD-3-Clause",
        "url": "https://github.com/pyodide/pyodide/blob/main/LICENSE",
    },
}


def normalize_spdx(label):
    """把上游散文式 label 归一成 SPDX 表达式。

    实测的上游写法（13 个包里遇到三种）：
      `GPL-3.0-or-later`                          → 原样
      `GPL-3.0-or-later and BSL-1.0`              → `and` 大写
      `GPL-3.0-or-later and public domain`        → `public domain` 是 LicenseRef

    ⚠️ **算符识别必须只在「词与词之间」，不能用 `\\bor\\b`**（2026-11-01 实测踩到）：
    `GPL-3.0-or-later` 里的 `or` 前后都是词边界（连字符是 `\\W`），
    朴素的 `\\bor\\b` 会把它替成 `GPL-3.0-OR-later` —— **一个非法 SPDX**，
    而且它会被 V11 的 parse_spdx 拒掉，13 个包全部炸。
    正确做法：先把 token 切开，**只替换「整个 token 恰好是 and/or」的那些**。
    """
    toks = label.strip().split()
    out = []
    for t in toks:
        low = t.lower()
        if low == "and":
            out.append("AND")
        elif low == "or":
            out.append("OR")
        else:
            out.append(t)
    s = " ".join(out)
    # `public domain` 是 LicenseRef（SPDX 里没有 public domain 这个 id）
    s = re.sub(r"\bpublic[ ]domain\b", "LicenseRef-public-domain", s, flags=re.I)
    return s


def load_pack_licenses():
    """13 个 Forge 包的 (id, url)：从 packages/*.json 的 copyright link 取。"""
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "packages", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        links = (d.get("upstream") or {}).get("links") or []
        lic = [l for l in links if "copyright" in (l.get("icon") or "")]
        if not lic:
            continue
        out[d["name"]] = (normalize_spdx(lic[0]["label"]), lic[0]["url"])
    return out


def license_for(tag, pack_licenses):
    """tag → (id, url)。tag 形如 forge-<包>-<版本> 或 supply-<x>-<版本>。"""
    if tag in OVERRIDE:
        o = OVERRIDE[tag]
        return o["id"], o["url"]
    m = re.match(r"forge-(.+?)-\d", tag)
    if m and m.group(1) in pack_licenses:
        return pack_licenses[m.group(1)]
    return None


def upgrade(man, lic):
    """返回新 manifest（不改原对象）。只动 schema 与 license 两项。"""
    new = json.loads(json.dumps(man))          # 深拷贝
    new["schema"] = 3
    new["license"] = {"id": lic[0], "url": lic[1]}
    return new


def check_invariants(old, new):
    """★ 升级绝不能改字节身份 —— 这是「asset 不用动」的前提。

    逐字比对：id / chunkSize / codecs / products / 全部 entry 的
    (product, name, bytes, sha256) 与每个 chunk 的 (part, file, bytes, sha256)。
    """
    def core(m):
        return {
            "id": m.get("id"), "chunkSize": m.get("chunkSize"),
            "codecs": m.get("codecs"), "products": m.get("products"),
            "entries": [
                {"product": e.get("product"), "name": e.get("name"),
                 "bytes": e.get("bytes"), "sha256": e.get("sha256"),
                 "variants": [
                     {"codec": v.get("codec"),
                      "chunks": [{"part": c.get("part"), "file": c.get("file"),
                                  "bytes": c.get("bytes"), "sha256": c.get("sha256")}
                                 for c in v.get("chunks") or []]}
                     for v in e.get("variants") or []]}
                for e in m.get("entries") or []],
        }
    return core(old) == core(new)


def _selftest():
    n = f = 0

    def t(label, cond):
        nonlocal n, f
        if cond:
            n += 1; print("PASS | " + label)
        else:
            f += 1; print("fail | " + label)

    t("归一：and → AND", normalize_spdx("A and B") == "A AND B")
    t("归一：public domain → LicenseRef",
      normalize_spdx("GPL-3.0-or-later and public domain")
      == "GPL-3.0-or-later AND LicenseRef-public-domain")
    t("归一：单个 SPDX 原样", normalize_spdx("MIT") == "MIT")

    old = {"schema": 2, "id": "x/y", "chunkSize": 1, "codecs": ["identity"],
           "products": {"p": {"form": "file"}},
           "entries": [{"product": "p", "name": "a", "bytes": 3, "sha256": "a" * 64,
                        "variants": [{"codec": "identity",
                                      "chunks": [{"part": 0, "file": "f.000",
                                                  "bytes": 3, "sha256": "a" * 64}]}]}]}
    new = upgrade(old, ("MIT", "https://x/COPYING"))
    t("升级：schema → 3", new["schema"] == 3)
    t("升级：license 写入", new["license"] == {"id": "MIT", "url": "https://x/COPYING"})
    t("★ 升级不改字节身份（core 逐字相同）", check_invariants(old, new))
    t("★ 原对象未被就地修改（深拷贝）", old["schema"] == 2 and "license" not in old)

    # 反向：改了 file 名 ⇒ 身份断言必须红
    bad = upgrade(old, ("MIT", "https://x/COPYING"))
    bad["entries"][0]["variants"][0]["chunks"][0]["file"] = "g.000"
    t("★ 改了 chunk file ⇒ 必须判为身份变了", not check_invariants(old, bad))
    # 反向：改了 sha ⇒ 也必须红
    bad2 = upgrade(old, ("MIT", "https://x/COPYING"))
    bad2["entries"][0]["sha256"] = "b" * 64
    t("★ 改了 entry sha ⇒ 必须判为身份变了", not check_invariants(old, bad2))

    pl = load_pack_licenses()
    t("包许可：13 个包全解析到", len(pl) == 13)
    t("tag 解析：forge-optim-1.6.3", license_for("forge-optim-1.6.3", pl) is not None)
    t("tag 解析：supply-msl-4.1.0 走 OVERRIDE",
      license_for("supply-msl-4.1.0", pl) == (OVERRIDE["supply-msl-4.1.0"]["id"],
                                              OVERRIDE["supply-msl-4.1.0"]["url"]))
    t("tag 解析：未知 tag ⇒ None", license_for("nope-1.0", pl) is None)

    print(f"\n=== {n} PASS / {f} fail ===")
    print(f"=== {n} PASS / {f} FAIL ===")
    return 0 if f == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    dry = "--dry-run" in argv
    outdir = None
    if "--out" in argv:
        outdir = argv[argv.index("--out") + 1]
        os.makedirs(outdir, exist_ok=True)

    pl = load_pack_licenses()
    tags = json.loads(subprocess.run(
        ["gh", "api", "repos/ArchivalEra/Octave-Extra-Content/releases?per_page=100",
         "--jq", "[.[]|select(.draft==false)|.tag_name]"],
        capture_output=True, text=True).stdout)
    ok = bad = 0
    for tag in sorted(tags):
        lic = license_for(tag, pl)
        if not lic:
            print(f"SKIP {tag}（找不到许可真值）"); bad += 1; continue
        d = os.path.join(outdir or "/tmp", tag)
        os.makedirs(d, exist_ok=True)
        subprocess.run(["gh", "release", "download", tag,
                        "-R", "ArchivalEra/Octave-Extra-Content",
                        "-p", "manifest.json", "-D", d], check=True)
        old = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
        new = upgrade(old, lic)
        if not check_invariants(old, new):
            print(f"FAIL {tag}：升级改了字节身份（不该发生）"); bad += 1; continue
        if dry:
            print(f"PLAN {tag}: schema {old['schema']}→3  {lic[0]}")
        else:
            json.dump(new, open(os.path.join(d, "manifest.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print(f"OK   {tag}: {lic[0]}")
        ok += 1
    print(f"\n{ok} 完成 / {bad} 失败")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
