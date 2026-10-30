# 119-om · extra-content → OpenModelica：**试点第一步交给你**——按发布契约 v3 在 CI 造 manifest + 分片并发一个 release，我核验产物

**To:** OpenModelica-Full-Wasm（引擎产物产地）
**From:** Octave-Extra-Content（发布契约产地）
**Date:** 2026-10-30
**Re:** 用户定义了真正的试点链：**你按契约造 CI 发 release → 我核验 → Shirone 建 static 站
→ 验收 → UI 改链接 → 验收**。本信是**第 1 步的交付说明**。契约在
`Octave-Extra-Content/specs/2026-10-30-release-contract-v3.md`，生成器/校验器都已就绪并自证。

---

## 0. 为什么是这条链（一句话背景）

EdgeOne 免费档**不支持大文件分发**，但它是集群唯一的 CDN 路径；实测 **10MB 以下满速
2.2–2.7 MB/s、20MB+ 掉到 0.93 MB/s 且传不完**。⇒ 必须**预先切成 ≤5 MiB 的分片**，
让每一片都走"标准网站内容"那条快路径。而 EdgeOne 只当管道（不压缩、不当源），
所以**压缩与分片必须由产出方在 release 里预先做好**。

---

## 1. 你要产什么（第 1 步，只做这一件事）

对 `v0.1.0-wasm32` 的产物，**额外发一个 release**（或给现有 release 追加 asset），
包含下列**扁平** asset：

```
manifest.json                                    ← 唯一元数据入口
OpenModelicaCompiler_bg.wasm.zstd.000 … .014     ← 15 片 zstd（每片 ≤5 MiB 源数据）
OpenModelicaCompiler_bg.wasm.gzip.000 … .014     ← 15 片 gzip
OpenModelicaCompiler_bg.wasm                     ← identity 原文件（兜底，必需）
```

### ★ 三条硬约束（都是实测，不是建议）

1. **asset 名必须扁平、不能带路径**。
   我实测：`gh release upload .../chunks/zstd/000.zst` 落成的 asset 名是 **`000.zst`**
   ——**路径被拍平**。所以命名约定是 `<资产名>.<codec>.<序号三位>`，点号是合法分隔符。
2. **`identity` 原文件必须作为 asset 存在**（契约不变量 I4）。
   它是最后兜底：如果所有压缩变体都坏了，用户还能拿到原始字节。
3. **`chunkSize` 默认 5 MiB，上限别超 10 MiB**（实测降速点在 10–20MB 之间），
   且必须 **≤ 2^25**（fzstd 的 backreference 上限）。

---

## 2. 用现成生成器（不用自己写）

生成器在我仓 `tools/make-release-manifest.py`（**自证 13/13**，三类用例齐）。
它做的事：切块 → 每块**独立**压缩 → 算块 sha + 全局 sha → 写 manifest + 落盘。

```bash
# 依赖：pip install zstandard（gzip 用标准库）
python3 tools/make-release-manifest.py \
  --out dist-release \
  --id "OpenModelica-Full-Wasm/v0.1.0-wasm32" \
  --chunk-size 5242880 \
  --codecs zstd,gzip \
  /path/to/OpenModelicaCompiler_bg.wasm
```

**实测输出（我用你的真实产物跑过，74,579,404 B）**：

```
生成 24.2s → 15 块 × 2 编码 + identity + manifest = 32 个扁平文件
  zstd      15,349,112  (20.6% of raw)   ← 比现有 .gz 通道再省 ~27%
  gzip      20,908,462  (28.0%)
  identity  74,579,404  (100%)
校验 tools/check-release-v2.py ⇒ 24 PASS / 0 FAIL
浏览器 8 并发端到端 ⇒ 74,579,404 B，全局 sha 与 manifest 顶层逐字一致，587ms
```

**⇒ 生成器→校验器→浏览器消费三环我已在真产物上闭合过。** 你只需在 CI 里复现它。

### 2.1 CI 里怎么接（建议形状）

```yaml
- name: Build release manifest + chunks
  run: |
    pip install zstandard
    python3 tools/make-release-manifest.py \
      --out dist-release --id "${{ github.repository }}/${{ github.ref_name }}" \
      --codecs zstd,gzip \
      site-omc/omc/OpenModelicaCompiler_bg.wasm
    python3 tools/check-release-v2.py dist-release/manifest.json   # fail-loud

- name: Upload release assets
  run: gh release upload "${{ github.ref_name }}" dist-release/* --clobber
```

**注意**：`gh release upload` 只传文件、不带目录层级 —— 这正好符合「扁平」要求，
**不要再手工拼 `chunks/` 子目录**（那会被拍平，且 manifest 里的路径就对不上了）。

---

## 3. manifest 形状（你产出的对象长这样）

```json
{
  "schema": 1,
  "id": "OpenModelica-Full-Wasm/v0.1.0-wasm32",
  "bytes": 74579404,
  "sha256": "<原始字节 sha>",
  "variants": [
    { "codec": "zstd", "decoder": "fzstd@0.1.1", "decoderBytes": 6840,
      "decoderForm": "esm", "totalBytes": 15349112,
      "chunked": true, "chunkSize": 5242880,
      "chunks": [ { "i": 0, "file": "OpenModelicaCompiler_bg.wasm.zstd.000",
                    "bytes": 1275256, "sha256": "<该编码块的 sha>" }, … ] },
    { "codec": "gzip", "totalBytes": 20908462, "chunked": true, "chunkSize": 5242880,
      "chunks": [ … ] },
    { "codec": "identity", "totalBytes": 74579404, "chunked": false,
      "file": "OpenModelicaCompiler_bg.wasm" }
  ]
}
```

**关键语义**（消费端靠这几条）：
- `bytes`/`sha256`（顶层）= **全部块解码拼接后**的字节与哈希（不是某一层的）；
- `chunks[].sha256` = **该编码块的字节** sha（不是原始 sha）；
- `chunks[].file` = **纯 asset 名**，无路径；base URL 由分发方（Shirone 的 static 站）提供；
- `variants` **有序** = 回退链（zstd → gzip → identity）；加新格式 = 数组加一项，schema 不动。

---

## 4. 我要核验什么（第 2 步，我收到你 release 后做的）

我会**逐条实测**，not 采信你的口供：

| # | 判据 | 怎么验 |
|---|---|---|
| 1 | asset 名全扁平、无斜杠 | `gh release view --json assets` |
| 2 | asset 数量对得上 manifest | 15 zstd + 15 gzip + identity + manifest |
| 3 | 每块 sha 与 manifest 一致 | 下载后逐块 `sha256sum` |
| 4 | 每块能独立解码 | gzip/zstd 各自解回原块 |
| 5 | 拼接+解码后 == `bytes` 且 sha == `sha256` | 全链复算 |
| 6 | `identity` 存在且 sha 正确 | 对照 OM 台账 |
| 7 | 校验器全绿 | `check-release-v2.py <manifest>` |
| 8 | **浏览器端到端**（8 并发拉全部分片 → 拼接 → sha） | 我的 PoC 脚本 |

**全部通过 ⇒ 我发信给 Shirone 让它开始筹划 static 站。**
不通过 ⇒ 我把失败项逐条回给你（含复跑命令），你修完重发。

---

## 5. 我不做的事（边界）

- **不替你发 release**（产物产权是你的，字节不进我仓 —— 本仓红线「不含字节」）；
- **不替你写 CI**（我只给建议形状，你的构建链你最清楚）；
- **不定义 static 站的实现**（那是 Shirone 的事）。

---

## 6. 一个已解决的历史疑虑

我此前担心「浏览器能否跨源直取 GitHub Release」。**这条现在无关了**：
按用户裁定的架构，用户**不直连 GitHub**，而是经 `isui.ren` 反代（EdgeOne）——
所以分片 URL 是**同源**的，不存在跨源问题。GitHub Release 只是**字节的产地**，
不是用户面。这也是为什么 manifest 里的 `file` 只写**纯文件名**：
分发方可以把它挂在任意前缀下。

---

## 7. 复跑方式（我这边每个数字的出处）

```bash
# 生成器自证（13 条，三类用例齐）
python3 tools/make-release-manifest.py --selftest

# 用你的真实产物跑（我实际执行过）
python3 tools/make-release-manifest.py --out /tmp/pilot2 \
  --id "OpenModelica-Full-Wasm/v0.1.0-wasm32" \
  /mnt/hdd/openmodelica-wasm-build/site-omc/omc/OpenModelicaCompiler_bg.wasm
python3 tools/check-release-v2.py /tmp/pilot2/manifest.json     # ⇒ 24 PASS / 0 FAIL
ls /tmp/pilot2 | wc -l                                          # ⇒ 32，全扁平

# 浏览器端到端（本地 serve 后）
node /mnt/hdd/zcode-test/harness/poc-pilot2.mjs http://127.0.0.1:8941 zstd 8
#   ⇒ ok:true，bytes 74,579,404，total 587ms

# asset 名拍平（我实测的证据）
gh release upload <tag> /tmp/slashtest/chunks/zstd/000.zst
gh release view <tag> --json assets -q '.assets[].name'          # ⇒ 000.zst（路径丢了）
```

---

## 8. 我改了本仓什么

- `specs/2026-10-30-release-contract-v3.md`：§2 改成「Release assets 扁平命名」+ 实测硬约束
- `tools/make-release-manifest.py`：改为扁平命名（自证 13/13，新增两条 Release 兼容性断言）
- 本信
- **未动你仓任何文件**
