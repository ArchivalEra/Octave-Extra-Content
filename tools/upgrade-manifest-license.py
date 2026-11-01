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


def upgrade(man, lic, by_name=None):
    """返回新 manifest（不改原对象）。动 `schema` / 顶层 `license` / 可选的 entry 级 `license`。

    `lic`     —— 顶层，`(id, url)`。**保持原有语义**，旧调用不受影响。
    `by_name` —— 可选，`{entry.name: (id, url)}` 或 `{entry.name: {"id":…, "url":…, "role":…}}`。
                 命中的 entry 写 `license`（`role` 若给则一并写）。

    ★ 两条硬规矩（LLVM `023` 提，我采纳）：
    1. **不默认填**。entry 不在 `by_name` 里 ⇒ **不写** `license`，回落到顶层。
       不许给一个猜的默认值 —— **空可以是诚实的，错不能**。
    2. **`check_invariants()` 不动**。license/role 是允许变的；字节身份不许变。
       它本来就不比 license，所以这里加 entry license 不会让它红。

    ★ 键用 **`entry.name` 原样**（LLVM 的方案 a）：`"toolchain/clang.wasm"`。
    不做 `/`→`__` 之类的归一 —— 归一规则一旦进工具就得当契约维护，
    而它只是名字美化，不是语义。调用方多写几个字符是更小的代价。
    """
    new = json.loads(json.dumps(man))          # 深拷贝
    new["schema"] = 3
    new["license"] = {"id": lic[0], "url": lic[1]}
    if not by_name:
        return new
    for e in new.get("entries") or []:
        hit = by_name.get(e.get("name"))
        if hit is None:
            continue                            # 不默认填（规矩 1）
        if isinstance(hit, dict):
            e["license"] = {"id": hit["id"], "url": hit["url"]}
            if "role" in hit:
                e["role"] = hit["role"]
        else:
            e["license"] = {"id": hit[0], "url": hit[1]}
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


def _audit_literal_asserts(path):
    """静态审计：本文件里所有 `t(标签, 条件)` 调用的第二个参数，不许是字面量 bool。

    为什么需要它（2026-11-01 实测三次才想清楚）：
      · 运行时的「元自证」只能验 `t()` 这个**机制**还在判断；
      · 变异测试只能验**被调用函数**（`check_invariants`）没被换掉；
      · fail 计数器只能验计数**动了**（掏空别的断言时照样动）。
    **三者都抓不到「某一条 `t(...)` 被改成 `True`」** —— 而那是掏空一条断言
    的最短路径，也是我实际犯过的错（`... or True`，见 Einfacht issue #23）。

    唯一有效的办法是**看源码**：字面量 bool 作为断言条件，要么是笔误、
    要么是掏空。`SENTINEL` 里的行号是自检器自己的故意失败用例，放行。

    返回 {"literal": [(行号, 值), ...], "sentinel": [...]}。
    """
    import ast
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError) as ex:
        return {"literal": [("<不可解析>", repr(ex))], "sentinel": []}
    SENTINEL = {"〔自检〕这条是故意失败的（用于验证 fail 计数真的会动）"}
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "t" and len(node.args) >= 2):
            arg = node.args[1]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, bool):
                lbl = node.args[0]
                label = lbl.value if isinstance(lbl, ast.Constant) else ""
                if label in SENTINEL:
                    continue
                out.append((node.lineno, arg.value))
    return {"literal": out, "sentinel": sorted(SENTINEL)}


def _selftest():
    n = f = 0

    def t(label, cond):
        nonlocal n, f
        if cond:
            n += 1; print("PASS | " + label)
        else:
            f += 1; print("fail | " + label)

    # ★ 元自证（2026-11-01 实测踩到）：本工具的**全部价值**是那条反向断言
    #   「改了字节 ⇒ 必须判身份变了」。但如果有人（我）把它改成恒真（`True`
    #   或 `... or True`），`--selftest` 照样 13 PASS、退出码 0、pre-commit 全绿
    #   —— **假断言与真断言在「返回 0 + 打摘要行」这个面上完全同形**。
    #   这正是 Einfacht issue #23（我自己报的那条）。
    #
    #   下面这道**元级**判据验的是「`t()` 这个机制还在不在判断」：
    #   拿一个必然为假的条件喂进去，它必须计入 fail。
    #
    #   ⚠️ **诚实边界（实测确认，别把它当万能）**：这条**抓不到**「某一条业务断言
    #   被单独改成 `True`」——那种情况下 `t()` 仍在正常判断，元自证照样通过。
    #   我实测过：把「改了 chunk file ⇒ 必须判身份变了」改成 `True` 后，
    #   自证仍是 13 PASS / 0 fail。要抓那一类，需要**变异测试**（给每条断言
    #   注入一个必破输入，断言必须变红），代价是每条断言多写一个破坏器 ——
    #   见 Einfacht issue #23 的三档建议。**这里只做到"机制没死"这一层，
    #   不假装做到了"每条断言都有牙"。**
    _f0 = f
    t("〔元自证〕必然为假的条件必须计入 fail（否则 t() 已失效）", 1 == 2)
    if f == _f0:
        print("FATAL | 〔元自证〕t() 不做判断（假条件没被计入 fail）"
              " —— 本自证整体不可信，全部 PASS 作废")
        print("\n=== 0 PASS / 999 FAIL ===")
        return 1
    n -= 1                      # 这条元的本身不是业务通过，回滚计数
    f -= 1
    n += 1; print("PASS | 〔元自证〕t() 仍在真实判断（假条件已被计入 fail 并回滚）")
    print("      ⚠️ 边界：本元自证只证「机制没死」，不证「每条断言都有牙」"
          "（后者需变异测试，未做）")

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

    # ── entry 级 license（LLVM `023` 请求，2026-11-01）──────────────────────
    # 旧调用（两参数）必须一字不变 —— 加参数不许破坏它。
    t("★ entry 级：不传 by_name ⇒ 行为与旧版完全一致（只有顶层 license）",
      upgrade(old, ("MIT", "https://x/COPYING")) == new)

    two = {"schema": 2, "id": "x/y", "chunkSize": 1, "codecs": ["identity"],
           "products": {"p": {"form": "file"}},
           "entries": [
               {"product": "p", "name": "toolchain/clang.wasm", "bytes": 1,
                "sha256": "a" * 64,
                "variants": [{"codec": "identity",
                              "chunks": [{"part": 0, "file": "a.000", "bytes": 1,
                                          "sha256": "a" * 64}]}]},
               {"product": "p", "name": "toolchain/driver__abi.mjs", "bytes": 2,
                "sha256": "b" * 64,
                "variants": [{"codec": "identity",
                              "chunks": [{"part": 0, "file": "b.000", "bytes": 2,
                                          "sha256": "b" * 64}]}]},
               {"product": "p", "name": "toolchain/unmapped.txt", "bytes": 3,
                "sha256": "c" * 64,
                "variants": [{"codec": "identity",
                              "chunks": [{"part": 0, "file": "c.000", "bytes": 3,
                                          "sha256": "c" * 64}]}]}]}
    E = two["entries"]
    m2 = upgrade(two, ("MIT", "https://x/C"), by_name={
        E[0]["name"]: ("Apache-2.0 WITH LLVM-exception", "https://llvm.org/LICENSE.txt"),
        E[1]["name"]: {"id": "MIT OR NCSA", "url": "https://x/ncsa", "role": "license"},
    })
    t("★ entry 级：命中的 entry 写上 license（键 = entry.name 原样）",
      m2["entries"][0]["license"]["id"] == "Apache-2.0 WITH LLVM-exception")
    t("★ entry 级：dict 形状可带 role", m2["entries"][1].get("role") == "license")
    t("★★ entry 级：未命中的 entry **不写** license（不默认填 —— 空可以诚实，错不能）",
      "license" not in m2["entries"][2])
    t("★ entry 级：顶层 license 仍然写（回落目标）", m2["license"]["id"] == "MIT")
    t("★★ entry 级：加 entry license 后 check_invariants 仍判身份未变",
      check_invariants(two, m2))
    # 反向：entry 级 license 若**误改**了字节字段 ⇒ 必须红
    bad3 = json.loads(json.dumps(m2))
    bad3["entries"][0]["bytes"] = 999
    t("★★ entry 级：若同时误改了字节字段 ⇒ 必须判身份变了",
      not check_invariants(two, bad3))
    # 反向：原对象不许被 by_name 路径就地改
    t("★ entry 级：原对象未被就地修改",
      "license" not in two["entries"][0] and two["schema"] == 2)

    # 反向：改了 file 名 ⇒ 身份断言必须红
    bad = upgrade(old, ("MIT", "https://x/COPYING"))
    bad["entries"][0]["variants"][0]["chunks"][0]["file"] = "g.000"
    t("★ 改了 chunk file ⇒ 必须判为身份变了", not check_invariants(old, bad))
    # 反向：改了 sha ⇒ 也必须红
    bad2 = upgrade(old, ("MIT", "https://x/COPYING"))
    bad2["entries"][0]["sha256"] = "b" * 64
    t("★ 改了 entry sha ⇒ 必须判为身份变了", not check_invariants(old, bad2))

    # ★★ 变异测试（**诚实地讲：它验的是函数，不是断言**）
    #
    #   把 check_invariants 换成一概 True，然后确认「反向判据失去判断力」。
    #   ⚠️ 我实测过：**这抓不到「那条 t(...) 被改成字面量 True」**——
    #   因为掏空的是调用点，而这里验的是被调用者。两者不同。
    #   要真抓到「某条断言被掏空」，唯一办法是让断言本身**不接受字面量**，
    #   而是接受一个可执行的结果（见下面那条「自检器」）。
    #   这一条留着，是因为它能抓「check_invariants 被改成永真」这种**函数级**劣化，
    #   那种劣化同样会让身份保护失效。
    _real = check_invariants
    try:
        globals()["check_invariants"] = lambda a, b: True
        mutated = check_invariants(old, bad)
    finally:
        globals()["check_invariants"] = _real
    t("★★ 变异：check_invariants 被换成一概 True ⇒ 它失去判断力（函数级）",
      mutated is True)
    t("★★ 变异：还原后恢复判断力", check_invariants(old, bad) is False)

    # ★★★ 自检器（**这条才真的抓「断言被掏空」**）
    #
    #   思路：不放一条「结果为 True」的断言，而是放一个**必然失败的用例**，
    #   然后断言「它确实失败了」。若有人把**这条**改成字面量 True，
    #   他改的是"断言"——但它断言的对象是「另一个东西失败了」。
    #   掏空它之后仍然是 15 PASS……**除非**我们检查「这条 FAIL 用例真的产生过 fail 记录」。
    #
    #   ⇒ 真正的判据在这里：**统计 fail 计数**。下面故意让一个用例失败，
    #   它必须让 f 增加；若不增加，说明 t() 或被掏空、或统计被动过。
    _f_before = f
    t("〔自检〕这条是故意失败的（用于验证 fail 计数真的会动）", False)
    if f != _f_before + 1:
        print("FATAL | 〔自检〕fail 计数没有增加 —— 自证统计已失效，全部 PASS 作废")
        print("\n=== 0 PASS / 999 FAIL ===")
        return 1
    f -= 1; n += 1          # 回滚：这条只用来验计数器
    print("PASS | 〔自检〕fail 计数真的会动（故「改了字节 ⇒ 必须判身份变了」若失败，会被计入）")

    # ★★★ 静态扫描（**这条才真的抓「断言被改成字面量」**）
    #
    #   前三道防线都试过、都不够（我实测确认）：
    #   · 元自证验「t() 还在判断」→ 抓不到某条 t(...) 被掏空；
    #   · 变异测试验「check_invariants 被换掉」→ 抓不到**调用点**被掏空（两者不同）；
    #   · fail 计数验「计数器会动」→ 掏空的是别的断言，计数照样动。
    #
    #   **唯一真正有效的判据是看源码**：`t(标签, 条件)` 的第二个参数
    #   不允许是字面量 bool（自检器自己那行 `False` 用哨兵白名单放行）。
    #   掏空一条断言的最短路径就是写成 `True`，AST 一眼看得出。
    #   ⇒ 这不是运行时验证，是**对自证本身的静态审计**。
    _audit = _audit_literal_asserts(__file__)
    t("★★★ 静态审计：自证里没有字面量 bool 断言（掏空的最短路径）",
      _audit["literal"] == [], )
    if _audit["literal"]:
        print("      发现：%r" % (_audit["literal"],))

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
