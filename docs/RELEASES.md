# 发布清单 · Forge 包与能力层（产地 = 本仓）

> **状态**：2026-11-01 首次发布，15 个 release 全部在线且**下载回验通过**。
> **复跑方式在文末**。本文是**人读索引**——字节身份的唯一权威是每个 release 里的
> `manifest.json`，本文不复制 sha 值（避免第二个产地）。

---

## 1. 这是什么

本仓作为**产地**，把 Forge 包与能力层资产的字节钉在**不可变 tag** 上。
在此之前链条是「上游 SourceForge → 宿主装配 → 站点」，**中间没有稳定产地**：

- 上游挂过（SourceForge 多次故障）；
- 上游改过 URL（`optim` 至今是 `download.php?package=` 重定向形式）；
- 上游一旦变，手里那份 sha 就变成**无法验证的历史断言**。

release 解决这件事：**同一个 tag 永远是同一份字节**。

---

## 2. 命名约定

```
forge-<包名>-<版本>            例：forge-cgi-0.1.2
supply-pyodide-<pyodide版本>   例：supply-pyodide-314.0.7
```

**MSL 没有 `supply-msl-*` 约定**（2026-11-03 撤除）：MSL 归 OM 发（其 tag 是
`msl-4.1.0-maint.om`，不带 `supply-` 前缀）。**本仓不产 MSL release。**

**一个包一个 release**（用户 2026-11-01 裁定）。理由：增量最小——某个包更新只重发那一个，
不牵动其它 12 个。

### 2.1 manifest 版本：`schema: 3`（v1.1 契约，许可必填）

2026-11-01 起，所有 manifest 是 **`schema: 3`**，带一项必填的许可声明：

```jsonc
{
  "schema": 3,
  "license": {
    "id":  "GPL-3.0-or-later AND BSD-3-Clause AND LicenseRef-public-domain",
    "url": "https://octave.sourceforge.io/optim/COPYING.html"
  }
}
```

- `id` = SPDX 表达式（给人快速判读，可复合）；`url` = **权威正文的当前位置**（必填，https）。
- **为什么两项都要**：`url` 指向的正文会随换许可证而变，`id` 的字符串不会。
- **合规缺口是真缺口**：包内的 `COPYING` 在 tarball 里，第三方拿元数据时看不到。

**升级既有 release 不用重传字节**：asset 集合由 manifest 的 `file` 字段定义，
只要 `bytes`/`sha256`/`file` 逐字不变，就只换 `manifest.json` 这一个 asset。
本仓的做法是 `tools/upgrade-manifest-license.py`（自证 13/13）——它**强制断言升级不改字节身份**。

⚠️ **归一化的坑**（本仓实测踩到，下游 13 个产物会一起中招）：把散文 `and`/`or` 转 SPDX 算符时，
**不能用 `\bor\b`** ——`GPL-3.0-or-later` 里的 `or` 前后都是词边界，会被替成
`GPL-3.0-OR-later`（非法 SPDX），而 `-only` 的包看不出来。**正确做法**：先切 token，
只替换「整个 token 恰好是 and/or」的。

---

## 3. 当前发布面

**13 个 Forge 包**（每个 1 条 entry / 2 个 asset：1 个 identity 分片 + `manifest.json`）：

`cgi` 0.1.2 · `datatypes` 1.4.2 · `geometry` 4.1.0 · `matgeom` 1.2.4 ·
`miscellaneous` 1.3.3 · `nan` 3.7.2 · `optim` 1.6.3 · `quaternion` 2.4.2 ·
`splines` 1.3.5 · `statistics` 1.7.7 · `struct` 1.0.18 · `symbolic` 3.2.2 · `tsa` 4.6.3

**1 个能力层 release**：

| tag | 内容 | entry / asset |
|---|---|---|
| `supply-pyodide-314.0.7` | Pyodide core + SymPy + mpmath（`symbolic` 的运行期依赖） | 3 / 10 |

**合计 14 个 release**（台账键 `releases_published`）。

**★ MSL 不在本仓发布（2026-11-03 已撤）**：我曾发过 `supply-msl-4.1.0`，与 OM 的
`msl-4.1.0-maint.om` **逐字相同**（`a97d8d94ca7f…`）。那是**冗余发布**，而且
**MSL 的产地是 OM 不是我**（红线：不许以产地为由改别人的产物归属）。
已删除本仓那条；OM 那条经我核验完好（47 PASS / 0 FAIL，5 asset）。
**为什么删不违反「release 不可变」**：那条原则防的是**改写已发布字节**；
这里撤的是**我自己发的重复件**，权威件（OM 的）仍在，字节从未消失。

---

## 4. 为什么全是 identity（没有 zstd/gzip 变体）

13 个 Forge 包全是 `.tar.gz`，Pyodide 三件是 `.tar.bz2` / `.whl`，MSL 是 `.zip`
——**全部是已压格式**。生成器的 `PRECOMPRESSED` 判定只给它们出 identity。

**这不是偷懒，是实测**：拿 13 个包再压一遍，zstd 合计只省 0.4%，gzip 省 0.3%，
**多数单个文件反而变大**（`cgi` +0.1%、`splines` +0.0%）。

**唯一有压缩分片的是 `supply-pyodide-314.0.7` 里的 `pyodide-core-314.0.7.tar.bz2`**
——它 6.76 MB，超过 5 MiB 分片线，所以切成 2 块并出 zstd/gzip/identity 三编码（6 个 asset）。

---

## 5. 客户端怎么取

```
GET <base>/manifest.json            ← 唯一需要"知道"的 URL
遍历 entries[] → variants[] → chunks[].file   ← 逐字取名字，绝不拼
GET <base>/<file>                   ← 普通 GET
```

**base =** `https://github.com/ArchivalEra/Octave-Extra-Content/releases/download/<tag>/`

例：`.../releases/download/forge-cgi-0.1.2/forge__cgi-0.1.2.tar.gz.identity.000`

**注意**：GitHub Release asset 名会被平台规范化，但本协议的白名单保证**不会被改写**
（实测面见 `specs/2026-10-30-release-contract-v4.md` §1）。

---

## 6. 发布新版本怎么做

```bash
# 1) 确认字节在本地且 sha 与台账一致
python3 tools/forge-shelf.py --verify <包名>

# 2) 生成 manifest + 分片
python3 tools/make-manifest-v4.py --out /tmp/rel-<包>-<版本> \
  --id "Octave-Extra-Content/forge-<包>-<版本>" \
  --product "forge:file:/path/to/<包>-<版本>.tar.gz"

# 3) 校验（带 --base 才逐块对盘）
python3 tools/check-release-v4.py /tmp/rel-<包>-<版本>/manifest.json \
  --base /tmp/rel-<包>-<版本>

# 4) 发（用 gh release create 或 API；asset 必须扁平）
gh release create "forge-<包>-<版本>" --title "<包> <版本>" \
  --notes-file <notes.md> /tmp/rel-<包>-<版本>/*

# 5) ★ 回验（下载回来再核一遍 —— 这一步不能省）
gh release download "forge-<包>-<版本>" -D /tmp/vfy && \
  python3 tools/check-release-v4.py /tmp/vfy/manifest.json --base /tmp/vfy
```

⚠️ **踩过的坑**：`gh release create` 在慢网络下会超时并留下 **draft**。
**发完必须查 `draft=false`**，否则资产在但客户端取不到（draft 不对外）。

---

## 7. 复跑方式（本文所有断言的出处）

```bash
# 发布面规模（台账键 releases_published）
gh api 'repos/ArchivalEra/Octave-Extra-Content/releases?per_page=100' \
  --jq '[.[]|select(.draft==false)]|length'      # ⇒ 15

# 逐 release 检查 draft 与 asset 数
gh api 'repos/ArchivalEra/Octave-Extra-Content/releases?per_page=100' \
  --jq '.[]|"\(.tag_name)\tdraft=\(.draft)\tassets=\(.assets|length)"'

# 全量下载回验（13 forge + 2 supply 各跑一次）
for t in $(gh api 'repos/ArchivalEra/Octave-Extra-Content/releases?per_page=100' \
             --jq '.[]|select(.draft==false)|.tag_name'); do
  mkdir -p /tmp/vfy/$t && gh release download $t -D /tmp/vfy/$t --clobber
  python3 tools/check-release-v4.py /tmp/vfy/$t/manifest.json --base /tmp/vfy/$t
done

# 再压一遍的实测（证明 PRECOMPRESSED 判定正确）
python3 - <<'PY'
import os,gzip
import zstandard as zstd
c=zstd.ZstdCompressor(level=19); tr=tz=tg=0
for f in os.listdir('/mnt/hdd/octave-wasm-build/third_party/forge'):
    b=open('/mnt/hdd/octave-wasm-build/third_party/forge/'+f,'rb').read()
    tr+=len(b); tz+=len(c.compress(b)); tg+=len(gzip.compress(b,9,mtime=0))
print('raw %d / zstd %+d%% / gzip %+d%%' % (tr, 100*(tz-tr)//tr, 100*(tg-tr)//tr))
PY
```

## 8. 首次发布的实测记录（2026-11-01）

- 13 个 Forge release：**13/13 下载回验通过**（每份 `check-release-v4.py --base` 全 PASS）
- `supply-pyodide-314.0.7`：92 PASS / 0 FAIL
- ~~`supply-msl-4.1.0`：39 PASS / 0 FAIL~~（**该 release 已于 2026-11-03 撤除**——与 OM 的
  `msl-4.1.0-maint.om` 逐字重复，MSL 产地归 OM。以上验证记录保留作历史。）
- 13 份的验证条数各自 30 条左右（1 entry / 2 asset 的规模）

**踩坑记录**（写给下次）：`gh release create` 在本机慢网络下会超时并留 draft；
两次重试会产生**同 tag 的重复 draft**，必须按 id 删掉多余那个，不能只按 tag 删。
