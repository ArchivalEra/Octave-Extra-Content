#!/usr/bin/env python3
"""分发协议 ↔ 市场协议 的**解耦闸门**（2026-11-02 用户裁定「两种协议完全不相干」）。

判据只有一句话：

> **市场表里的任何字段都不许取自分发侧的唯一标识；
> 分发契约也不许引用市场语义字段。**

这条不是"风格偏好"，是**方向性错误**：一旦市场表引用 `release tag` / `release base` /
`manifest_sha256`，换分发方（GitHub → CF → 对象存储 → …）时市场表就得跟着改。
反之，分发契约若引用 `name`/`version`/`deps`/`consumer`，它就变成了半个市场契约。

用法：
    python3 tools/check-contract-decoupling.py --market <content-list.json>
    python3 tools/check-contract-decoupling.py --selftest

退出码：0 = 解耦成立；1 = 发现耦合；2 = 用法/输入错误。
"""
import json
import re
import sys

# ── 分发侧的唯一标识（市场表里出现这些形状 ⇒ 耦合）──────────────────────────
#   `releases/download/<tag>/` 是最硬的信号：它就是 release 直链的路径形状。
RELEASE_PATH = re.compile(r"/releases/download/")
#   catalogue 侧字段名：市场表不该有这些**字段名**（值是别的也说明在抄分发侧）
DIST_KEYS = {"base", "manifest_sha256", "verified_at", "manifest_url"}

# ── 市场侧语义字段（分发契约里不该出现）──────────────────────────────────────
MARKET_KEYS = {"name", "version", "deps", "consumer", "role", "form", "content",
               "versions", "upstream_url", "description", "links"}


def audit_market(entries):
    """市场表里有没有取自分发侧的标识。返回问题清单（空 = 解耦）。"""
    if not entries:
        # 零值守卫：空表不是「没有耦合」，是「什么都没有」——那就是通过不了。
        return ["市场表为空 —— 空不是通过（零值守卫）：先确认真的是零条还是读错了"]
    probs = []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            probs.append("[%d] 不是对象" % i)
            continue
        for k in sorted(DIST_KEYS & set(e)):
            probs.append("[%d] %r 含分发侧字段 %r —— 市场表不许有它"
                         % (i, e.get("name"), k))
        url = e.get("url") or ""
        if isinstance(url, str) and RELEASE_PATH.search(url):
            probs.append("[%d] %r 的 url 指向 release 直链（%s）—— "
                         "市场表要取址就用自己语义下的站内同源 url"
                         % (i, e.get("name"), url[:70]))
    return probs


def audit_release(man):
    """分发契约（manifest）顶层有没有引用市场语义。返回问题清单。"""
    probs = []
    if not isinstance(man, dict):
        return ["manifest 不是对象"]
    for k in sorted(MARKET_KEYS & set(man)):
        probs.append("manifest 顶层含市场语义字段 %r —— 分发契约不许引用它" % k)
    # entries[] 里的 product/form 是**分发侧自己的判别符**（跨 arch 去重需要），
    # 与市场语义的 form/content 同名但不同义 —— 明确豁免并写进注释，避免误判。
    return probs


def _selftest():
    n = f = 0

    def t(label, cond):
        nonlocal n, f
        if cond:
            n += 1; print("PASS | " + label)
        else:
            f += 1; print("fail | " + label)

    # ① 正常：解耦成立 ⇒ 不报
    good = [{"name": "cgi", "version": "0.1.2", "url": "assets/forge/cgi-0.1.2.tar.gz",
             "sha256": "a" * 64}]
    t("正常：市场表用站内同源 url ⇒ 不报", audit_market(good) == [])

    # ② 该报：url 指向 release 直链
    bad1 = [{"name": "cgi", "url": "https://github.com/o/r/releases/download/t/cgi.tar.gz"}]
    t("★ 该报：url 指向 release 直链 ⇒ 必报",
      any("release 直链" in x for x in audit_market(bad1)))

    # ③ 该报：市场表含分发侧字段
    bad2 = [{"name": "cgi", "base": "https://github.com/o/r/releases/download/t/",
             "manifest_sha256": "b" * 64}]
    t("★ 该报：市场表含 base ⇒ 必报", any("base" in x for x in audit_market(bad2)))
    t("★ 该报：市场表含 manifest_sha256 ⇒ 必报",
      any("manifest_sha256" in x for x in audit_market(bad2)))

    # ④ 该报：分发契约引用市场语义
    badm = {"schema": 3, "deps": {"cgi": []}, "entries": []}
    t("★ 该报：manifest 顶层含 deps ⇒ 必报",
      any("deps" in x for x in audit_release(badm)))

    # ⑤ 正常：分发契约自己的 form/product 不该被误判
    okm = {"schema": 3, "products": {"omc": {"form": "file"}, "wasm32": {"form": "octdir"}},
           "entries": [{"product": "omc", "name": "x.wasm", "bytes": 1, "sha256": "c" * 64}]}
    t("正常：manifest 的 products.form / entries.product ⇒ 不报（分发侧自己的判别符）",
      audit_release(okm) == [])

    # ⑥ 空输入必须报（零值守卫）
    t("★ 空输入：空市场表 ⇒ 必报（空不是通过）", audit_market([]) != [])

    # ⑦ 静态审计：本自证里不许有字面量 bool 断言（掏空的最短路径）
    #   写这个工具的同一天我又差点写成 `!= [] or True` —— 那是恒真。
    #   静态扫描是唯一有效抓法（元自证 / 变异测试 / fail 计数都抓不到，见本仓经验集）。
    import ast as _ast
    _src = open(__file__, encoding="utf-8").read()
    _lit = []
    for node in _ast.walk(_ast.parse(_src)):
        if (isinstance(node, _ast.Call) and isinstance(node.func, _ast.Name)
                and node.func.id == "t" and len(node.args) >= 2):
            a = node.args[1]
            if isinstance(a, _ast.Constant) and isinstance(a.value, bool):
                _lit.append(node.lineno)
    t("★★ 静态审计：本自证里没有字面量 bool 断言", _lit == [])

    print(f"\n=== {n} PASS / {f} fail ===")
    print(f"=== {n} PASS / {f} FAIL ===")
    return 0 if f == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if "--market" in argv:
        p = argv[argv.index("--market") + 1]
        try:
            d = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError) as ex:
            print("FATAL: 读不了 %s：%s" % (p, ex), file=sys.stderr)
            return 2
        entries = d.get("entries") or d.get("packs") or []
        probs = audit_market(entries)
        if probs:
            print("解耦闸门：发现 %d 处耦合" % len(probs))
            for x in probs[:20]:
                print("  · " + x)
            return 1
        print("解耦闸门：OK（市场表 %d 条，无分发侧标识）" % len(entries))
        return 0
    if "--manifest" in argv:
        p = argv[argv.index("--manifest") + 1]
        try:
            man = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError) as ex:
            print("FATAL: 读不了 %s：%s" % (p, ex), file=sys.stderr)
            return 2
        probs = audit_release(man)
        if probs:
            print("解耦闸门：发现 %d 处耦合" % len(probs))
            for x in probs[:20]:
                print("  · " + x)
            return 1
        print("解耦闸门：OK（manifest 未引用市场语义）")
        return 0
    print("用法: --market <content-list.json> | --manifest <manifest.json> | --selftest",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
