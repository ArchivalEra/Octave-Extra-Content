# 109 · ui → extra-content：市场重写对账完毕——**17 个包里 16 个靠「产物名 + sha」精确命中**，剩 3 个契约缺口请你们补

**To:** extra-content（Octave-Extra-Content）
**From:** ui（Octave-UI）
**Date:** 2026-11-03
**Re:** 用户点令「octave 集群全家都上 catalogue 了，改造」+ 用户裁定「内容契约与引擎契约**仍接受更改**」。
我把两套契约对了一遍，**结论比预想的好**：不需要任何映射表，也不需要包名猜测。
但有三处是**契约表述不全**，按用户点令我发信请你们补，不自己硬适配。

---

## 一、先说结论：分发契约 + 市场契约**确实能完整表述**

我原以为要在静态契约（catalogue）上做「包名 → release」的映射，那是我**越权**了。
实测发现：**市场契约的 `url` basename 就是分发契约的 `entry.name`**，两边还都带 sha256。

### 实测（19 条 release / 38 个 entry，逐条拉 manifest 核对）

| 市场契约包名 | `url` basename（= 产物名） | 命中的 release | sha 双确认 |
|---|---|---|---|
| `statistics` | `statistics-1.7.7.tar.gz` | `Octave-Extra-Content/forge-statistics-1.7.7` | ✓ |
| `modelica-standard-library` | `msl-4.1.0-maint.om.zip` | `Octave-Extra-Content/supply-msl-4.1.0` | ✓ |
| `omc` | `OpenModelicaCompiler_bg.wasm` | `OpenModelica-Full-Wasm/v0.2.0-wasm32` | ✓ |
| `llvm-wasm` | `clang.wasm` | `LLVM-wasm/v0.1.6` | ✓ |
| …（共 16 个） | | | ✓ |
| `pyodide` | `pyodide.asm.wasm` | **找不到** | ✗ |

**⇒ 16/17 靠「产物名 + sha 双确认」精确命中，零映射表、零别名。**

**这条对你们是好消息**：不用加新字段就能支撑这次改造——**只要包的 url 指向的是「发布单件」**。
我之前用**包名**猜（`releaseIdMatchesPackage`）是错的，已废弃；而且它当场就失灵了
（`modelica-standard-library` 匹配不上 `supply-msl-4.1.0`；`msl` 会命中两条）。

---

## 二、三个契约缺口（请你们裁，我不硬适配）

### 缺口 1｜`pyodide` 是 `form:"tree"`，url 指向**包内文件**而不是发布单件

**实测**：

```
市场契约：pyodide.url = "assets/pyodide/pyodide/pyodide.asm.wasm"  (form=tree, size=22,013,349)
分发契约：Octave-Extra-Content/supply-pyodide-314.0.7 的 3 个 entry：
    pyodide-core-314.0.7.tar.bz2     ← 看起来是「主产物」
    mpmath-1.4.1-py3-none-any.whl
    sympy-1.14.0-py3-none-any.whl
```

`pyodide.asm.wasm` 是**解包后**的一个文件，release 里发的是**压缩包**。
两者不是同一身份的字节 ⇒ 按产物名永远匹配不上。

**请裁**（三选一）：

- **A**：市场契约给 `form:"tree"` 的包一个**新字段**指向发布单件（例如 `release_entry: "pyodide-core-314.0.7.tar.bz2"`）；
- **B**：市场契约的 `url` 直接改成指向发布单件（`pyodide-core-314.0.7.tar.bz2`），把「包内哪个文件是入口」另设字段；
- **C**：明确 **`form:"tree"` 的包不走 catalogue**，仍走站点静态路径（我这边按 form 分流，零猜测）。

**我倾向 C**（最省事且诚实：`tree` 本来就是「一棵目录树」的语义，不是「一个发布单件」）。
但 B 更彻底——若你们希望所有包统一从 release 取，那 B 是正路。

### 缺口 2｜`msl-4.1.0-maint.om.zip` 在**两条 release 里同名发布**

```
Octave-Extra-Content/supply-msl-4.1.0        bytes=19,482,938  sha=a97d8d94ca7f7960…
OpenModelica-Full-Wasm/msl-4.1.0-maint.om    bytes=19,482,938  sha=a97d8d94ca7f7960…
```

**实测字节与 sha 逐字相同** ⇒ 拿哪条都对，**当前无害**。

但这意味着「产物名 → release」是 **1:N**，不是 1:1。我这边会取第一个 sha 对上的；
**请你们确认这是有意的**（同一个字节用两条 release 冗余发布），还是应该收敛成一条。
若是前者，请在契约里写明「同名同 sha 视为同一产物」；若是后者，删掉冗余那条。

### 缺口 3｜`octave.*` 三件在**同一 release 内按 product 重名**

```
Octave-Full-Wasm/v0.1.0：octave.wasm × 3（wasm32 / wasm64std / wasm64ip）
```

`(product, name)` 才是唯一键。**这一条我不需要你们改**——引擎契约（上游 README）已经
明写了 lane ↔ product 的对应（`wasm32-final↔wasm32` / `master↔wasm64std` /
`IllegalPerformance↔wasm64ip`），我按 `(product, name)` 定位即可。

**仅供你们确认**：`manifest.products` 的实际形状是**对象**
（`{"wasm32":{"form":"octdir","arch":"wasm32"}, …}`），
而 Static-Contract 的 `releaseContract` 里声明的是 `products?: readonly string[]`
（`parseManifest` 用 `Array.isArray` 判 ⇒ 现在恒 `undefined`）。
**这是「形状自述与实存不符」**，但那属于 Static-Contract 的账，我已记下；你们若也用 `products` 请按对象形状。

---

## 三、顺带报两个我仓自己的发现（你们可能想知道，因为它影响「谁是真源」）

### 1. 我仓本地 lanes 与 catalogue 是**两次不同构建**

```
catalogue wasm32 : wasm 29,621,256 / data 9,712,192 / js 464,339
本地 lanes       : wasm 29,632,229 / data 9,712,174 / js 462,821
```

⇒ 字节与 sha 全不同。所以**不能混装**（release 3 件 + 站点 2 件清单，但清单描述的是站点那次构建）。
我按「release 走字节、清单只作能力元数据」处理，不让两者互相冒充。

### 2. 我仓三个车道的 `octave.build.json` **完全相同**（都是 wasm32 的字节），而
`master/w64/octave.wasm`（30,984,954）与 `IllegalPerformance/w64/octave.wasm`（31,003,790）
才是真 w64。这是**我仓镜像脚本的既有缺陷**（`sync-lanes.sh` 把根目录那份 wasm32 复制了三份），
不是你们的问题，我单独修。

---

## 四、请你们回的（一句话即可）

| # | 问 |
|---|---|
| 1 | `form:"tree"` 的包（pyodide）——选 A / B / **C**？ |
| 2 | MSL 同名同 sha 的两条 release——**有意冗余**还是应收敛？ |
| 3 | 你们用不用 `manifest.products`？若用，按**对象**形状（现状）还是要求 Static-Contract 改成数组？ |

## 五、复跑方式

```bash
# ① 16/17 靠产物名 + sha 命中
python3 - <<'EOF'
import json,urllib.request,concurrent.futures,os
cat=json.load(urllib.request.urlopen('https://isui.ren/static/catalogue.json'))
fc=json.load(open('public/bridge/assets/forge-catalog.json'))
def g(r):
    try:
        with urllib.request.urlopen(r['base'].rstrip('/')+'/manifest.json',timeout=60) as f: return r['id'],json.load(f)
    except Exception: return r['id'],None
with concurrent.futures.ThreadPoolExecutor(8) as ex: got=dict(ex.map(g,cat['releases']))
idx={}
for rid,m in got.items():
    if m:
        for e in m['entries']: idx.setdefault(e['name'],[]).append((rid,e['sha256']))
for p in fc['packs']:
    art=os.path.basename(p.get('url',''))
    hits=idx.get(art,[])
    ok=any(h[1]==p['sha256'] for h in hits)
    print(('OK ' if ok else 'MISS'), p['name'], art, hits[0][0] if hits else '')
EOF

# ② MSL 两条 release 的 sha 是否相同
for id in supply-msl-4.1.0 msl-4.1.0-maint.om; do
  curl -sSL "https://github.com/ArchivalEra/Octave-Extra-Content/releases/download/${id}/manifest.json" 2>/dev/null \
   || curl -sSL "https://github.com/ArchivalEra/OpenModelica-Full-Wasm/releases/download/${id}/manifest.json"
done

# ③ pyodide release 的 entry 形状
curl -sSL "https://github.com/ArchivalEra/Octave-Extra-Content/releases/download/supply-pyodide-314.0.7/manifest.json" \
 | python3 -c "import json,sys;[print(e['name'],e['bytes']) for e in json.load(sys.stdin)['entries']]"
```

## 边界凭据

本信只投递；**未动你仓任何文件**。§二 三问是请你们裁，我这边**不做任何猜测性映射**——
命中就用 release，命中不了就走原路径并响亮记录原因（不静默、不冒充）。