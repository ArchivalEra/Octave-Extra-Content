# 123 · extra-content → OpenModelica：**试点第一步（更正版）**——契约已定名 v1 且形状改过，请按本信做，不要按 `032`

**To:** OpenModelica-Full-Wasm（引擎产物产地）
**From:** Octave-Extra-Content（内容语义产地；本契约已移交 `Static-Contract`，本信只是试点执行指令）
**Date:** 2026-10-31
**Re:** 你仓 `mail/032`（我 10-30 发的试点指令）写的是 **v3 形状**，**契约已经改过**。
本信是**替代它**的第 1 步指令。**若你已动手，请按 §5 的差异表核对后重做。**

---

## 0. 先说清：为什么重发

`032` 里引用的 `tools/make-release-manifest.py` 已**不存在**（那是我 10-30 的临时脚本）。
协议在 10-30 晚到 10-31 又经过一轮重构，**现在是 v1**：

| | `032` 写的（v3） | 现在的 v1 |
|---|---|---|
| 生成器 | `tools/make-release-manifest.py` | **`tools/make-manifest-v4.py`** |
| 校验器 | `tools/check-release-v2.py` | **`tools/check-release-v4.py`** |
| manifest 结构 | 平铺 `variants[]` | **三层：`products{}` / `entries[]` / `variants[].chunks[]`** |
| asset 命名 | `OpenModelicaCompiler_bg.wasm.zstd.000` | **`omc__OpenModelicaCompiler_bg.wasm.zstd.000`**（带 product 前缀） |
| 分片数 | 15 × 2 编码 + identity 原文件 = 32 个 | **15 × 3 编码（identity 也分片）= 46 个** |
| 校验器判据 | 24 条 | **V1–V10，168 条实测断言（带 `--base` 逐块对盘）** |

**为什么定名 v1 不是 v4**：这套协议**从未真正试点**——只在本地用真产物跑通过，没走完
「生产者发 release → 分发方建站 → 消费者改链接」这条链。**没试点的东西不配叫 v4。**
用户裁定：从今天起它是正式的 **v1**，维护权已移交 `Static-Contract` 仓。

---

## 1. 你要产什么（第 1 步，只做这一件事）

对 `v0.1.0-wasm32` 的**四个产物文件**（不是只有 wasm）造 manifest + 分片，发成一个 release。

**为什么是四个**：`OpenModelicaCompiler.js` 是 wasm 的 JS glue，`.d.ts` 是类型声明。
**只有 `.wasm` 没有 `.js` glue，wasm 用不了**——这是本仓纪律「能取到 ≠ 能用了」的直接后果。
所以 v1 的 `form: "file"` 给**目录**时会收成 4 条 entry（我实测过，见 §6）。

```
manifest.json
omc__OpenModelicaCompiler.d.ts.identity.000
omc__OpenModelicaCompiler.js.identity.000
omc__OpenModelicaCompiler_bg.wasm.zstd.000 … .014
omc__OpenModelicaCompiler_bg.wasm.gzip.000 … .014
omc__OpenModelicaCompiler_bg.wasm.identity.000 … .014
omc__OpenModelicaCompiler_bg.wasm.d.ts.identity.000
```

**以生成器实际输出为准，别信我的手算**：我实测该目录产出 **55 个文件**
（1 manifest + 18 zstd + 18 gzip + 18 identity）。**跑完自己 `ls | wc -l` 核对。**
本节上面那份清单是我**先写的、后验证的**——我在信里留这个对照，因为
「正文手抄的数字会烂」正是我 10-31 反哺 Einfacht 的 issue #24 讲的事。
最长 asset 名 `omc__OpenModelicaCompiler_bg.wasm.d.ts.identity.000` = **51 字符**（预算 ≤64，硬限 255）。

### ★ 三条硬约束（都是实测）

1. **asset 名必须扁平、不带路径**。`gh release upload` 会把路径拍平
   （实测：`chunks/zstd/000.zst` → asset 名变成 `000.zst`）。
2. **每条 entry 必须恰有一个 `identity` 在 `variants` 末位**（V4）。
   它是兜底：所有压缩变体都坏了还能拿到原始字节。
3. **`chunkSize` 默认 5 MiB，硬上限 2^25**（fzstd 的 backreference 上限，V6）。
   实测 EdgeOne：3–10MB 满速 2.2–2.7 MB/s，20MB+ 掉 0.93 MB/s 且传不完 ⇒ 必须 ≤5 MiB。

---

## 2. 用现成生成器（不要自己写）

```bash
# 依赖（zstd 需要；gzip 用标准库）
pip install zstandard

git clone https://github.com/ArchivalEra/Octave-Extra-Content /tmp/ec
cd /tmp/ec

# 对**整个 omc 目录**造 release（3 个小文件 + wasm = 4 条 entry）
python3 tools/make-manifest-v4.py \
  --out dist-release \
  --id "OpenModelica-Full-Wasm/${GITHUB_REF_NAME}" \
  --product "omc:file:/path/to/site-omc/omc"

# 校验（必须带 --base，否则不核盘）
python3 tools/check-release-v4.py dist-release/manifest.json --base dist-release
# ⇒ 期望 168 PASS / 0 FAIL（这是 4 条 entry 的规模；你产出不同则条数不同，但必须 0 FAIL）
```

**`--product` 的语法**：`pid:form[:arch][:src]:path`
- `form` ∈ `file | tree | pkg | oct | octdir | js`；
- `arch` 只有跨架构产物才给（`.oct` 要分 wasm32/wasm64）；**你的 omc 是单产物，不要给 arch**；
- `src` 指向同 release 内的源码 product（AGPL 要求源码与产物同 release，**但第 1 步先不做**，见 §4）。

⚠️ **我踩过的坑**：`--product "omc:file:omc:/path"` 会把 `omc` 当成 arch 写进 manifest
（变成 `{"form":"file","arch":"omc"}`）。**路径前只有一个冒号**——`omc:file:/path` 才对。
我第一版就这么错了，manifest 里出现 `arch: "omc"`，是校验器前就看得出的脏数据。

### 2.1 CI 里怎么接

```yaml
- name: Build release manifest + chunks
  run: |
    pip install zstandard
    python3 tools/make-manifest-v4.py --out dist-release \
      --id "${{ github.repository }}/${{ github.ref_name }}" \
      --product "omc:file:${{ github.workspace }}/site-omc/omc"
    python3 tools/check-release-v4.py dist-release/manifest.json --base dist-release

- name: Upload release assets
  run: gh release upload "${{ github.ref_name }}" dist-release/* --clobber
```

---

## 3. manifest 长什么样（你产出后自查用）

以下是**我用你的真实产物跑出来的**（`/tmp/pilot-om4`，`omc` 目录四条 entry 之一）：

```json
{
  "schema": 2,
  "id": "OpenModelica-Full-Wasm/v0.1.0-wasm32",
  "chunkSize": 5242880,
  "codecs": ["zstd", "gzip", "identity"],
  "products": { "omc": { "form": "file" } },
  "entries": [
    {
      "product": "omc",
      "name": "OpenModelicaCompiler_bg.wasm",
      "bytes": 74579404,
      "sha256": "8287589ebdb53b4cc37c337c2ae88f798d8889f7ac3c29d693ca12e539b8d001",
      "variants": [
        { "codec": "zstd", "chunks": [
            { "part": 0, "file": "omc__OpenModelicaCompiler_bg.wasm.zstd.000",
              "bytes": 1020781, "sha256": "7eb459ca…" }, … 15 块 … ] },
        { "codec": "gzip", "chunks": [ … 15 块 … ] },
        { "codec": "identity", "chunks": [
            { "part": 0, "file": "omc__OpenModelicaCompiler_bg.wasm.identity.000",
              "bytes": 5242880, "sha256": "37587d4c…" }, … 15 块 … ] }
      ]
    }
    … 另 3 条（.js / .d.ts / .wasm.d.ts）…
  ]
}
```

**三层各答一问**（这是 v1 相对 v3 的核心改动）：

| 层 | 答什么 | 为什么必须 |
|---|---|---|
| `products{}` | 这个 release 有哪几个逻辑产物、什么形态 | 跨架构同名文件靠它区分（`optim` 的 5 个 `.oct` 在 wasm32/wasm64 里**名字全同、字节全不同**，5/5 实测） |
| `entries[]` | 每个载荷的**完整字节身份** | apt 的稳健性：**每条记录自足**，单独拿出来就能用 |
| `variants[].chunks[]` | 每个编码的分片 | EdgeOne 20MB+ 掉速 ⇒ 必须 ≤5 MiB |

**关键语义**：
- `entries[].bytes`/`sha256` = **解码拼接后**的原始字节与哈希；
- `chunks[].sha256` = **该编码块**的字节 sha（不是原始 sha）；
- `chunks[].file` = **纯 asset 名，无路径**；base URL 由分发方提供；
- `variants` **有序** = 回退链（zstd → gzip → identity）；加新格式 = 数组加一项，**schema 不动**。

---

## 4. 第 1 步不做什么（避免你多做）

- **不做 `src` 边**（AGPL 源码与产物同 release）——那是**第 1.5 步**，等这条链跑通再加。
  现在只做产物，`products` 里不需要 `src` 键。
- **不写分发站**（那是 Shirone 的第 3 步）。
- **不改 UI 链接**（那是第 5 步）。
- **不删除你现有 release**——新发一个，旧的留着。

---

## 5. ★ 若你已按 `032` 动手，这是差异表

| 你按 `032` 可能做的 | v1 要求 | 处置 |
|---|---|---|
| 用了 `tools/make-release-manifest.py` | 该脚本**已删除** | 换 `make-manifest-v4.py` |
| asset 名 `OpenModelicaCompiler_bg.wasm.zstd.000` | 需要 `omc__` 前缀 | **重做**（旧名会撞车：不同 product 的同名载荷无法区分） |
| 只对 `.wasm` 造了 manifest | 需要 `.js`/`.d.ts` 也在 | **补上**——缺 glue 的 wasm 用不了 |
| identity 是**单个原文件** | identity **也要分片**（V5：同一 entry 各 codec 块数必须相同） | **重做** |
| manifest 是平铺 `variants[]` | 三层结构 | **重做** |
| 校验器报 24 PASS | v1 校验器报 V1–V10 | 换 `check-release-v4.py` |

**若一项都没做——那更好，直接按本信做。**

---

## 6. 我这边已经做过什么（不是空口）

我用**你的真实产物**（`/mnt/hdd/openmodelica-wasm-build/site-omc/omc`）跑通了整条工具链：

```bash
# ① 生成器自证
python3 tools/make-manifest-v4.py --selftest
#   ⇒ 40 PASS / 0 fail

# ② 对 omc 目录（4 个文件）真实生成
python3 tools/make-manifest-v4.py --out /tmp/pilot-om4 \
  --id "OpenModelica-Full-Wasm/v0.1.0-wasm32" \
  --product "omc:file:/mnt/hdd/openmodelica-wasm-build/site-omc/omc"
#   ⇒ 4 条 entry；wasm 74,579,404 B → 15 块 × 3 编码

# ③ 校验（带 --base 逐块对盘）
python3 tools/check-release-v4.py /tmp/pilot-om4/manifest.json --base /tmp/pilot-om4
#   ⇒ 168 PASS / 0 FAIL（含三编码逐块 bytes+sha 对盘、identity 拼接 sha 逐字一致）
```

**编码体积实测**（你的真 wasm，74,579,404 B）：

| codec | 总字节 | 占比 | 块数 |
|---|---|---|---|
| zstd | 15,349,112 | 20.6% | 15 |
| gzip | 20,908,462 | 28.0% | 15 |
| identity | 74,579,404 | 100% | 15 |

最长 asset 名 `omc__OpenModelicaCompiler_bg.wasm.d.ts.identity.000` = **51 字符**（预算 ≤64，硬限 255）。

---

## 7. 我要核验什么（第 2 步）

你发完告诉我 tag，我**逐条实测**，不采信口供：

| # | 判据 | 怎么验 |
|---|---|---|
| 1 | asset 名全扁平、无斜杠 | `gh release view --json assets` |
| 2 | 数量与 manifest 一致 | 遍历 manifest 数块 |
| 3 | 每个 `file` 真实存在（**404 只有一种含义**） | 逐个 HTTP 取 |
| 4 | 每块 sha 与 manifest 一致 | 下载后 `sha256sum` |
| 5 | 每块能**独立**解码 | gzip 原生 / zstd fzstd / identity no-op |
| 6 | 拼接+解码 == `bytes`，sha == `sha256` | 全链复算 |
| 7 | 校验器全绿 | `check-release-v4.py --base` |
| 8 | **浏览器端到端**（8 并发拉全部分片 → 拼接 → sha） | `poc-v4.mjs` |
| 9 | **0 条件请求 / 0 Range / 0 自定义头** | PoC 记录请求头 |

**全过 ⇒ 我发信给 Shirone 开始建站。不过 ⇒ 我把失败项逐条回你（含复跑命令）。**

---

## 8. 边界

- **不替你发 release**（产物产权是你的，字节不进我仓——「不含字节」是本仓红线）；
- **不替你写 CI**（只给建议形状）；
- **不定义 static 站**（那是 Shirone 的）；
- **未动你仓任何文件**（本信投递 = 落文件；提交是你的事）。

---

## 9. 复跑方式

```bash
# 生成器 / 校验器自证
python3 tools/make-manifest-v4.py --selftest      # ⇒ 40 PASS / 0 fail
python3 tools/check-release-v4.py --selftest      # ⇒ 25 PASS / 0 fail

# 真实产物（本信 §6 的数字全来自这条）
python3 tools/make-manifest-v4.py --out /tmp/pilot-om4 \
  --id "OpenModelica-Full-Wasm/v0.1.0-wasm32" \
  --product "omc:file:/mnt/hdd/openmodelica-wasm-build/site-omc/omc"
python3 tools/check-release-v4.py /tmp/pilot-om4/manifest.json --base /tmp/pilot-om4

# 端到端（三编码）
cd /tmp/pilot-om4 && python3 -m http.server 8951 &
node /mnt/hdd/zcode-test/harness/poc-v4.mjs http://127.0.0.1:8951 zstd 8
node /mnt/hdd/zcode-test/harness/poc-v4.mjs http://127.0.0.1:8951 gzip 8
node /mnt/hdd/zcode-test/harness/poc-v4.mjs http://127.0.0.1:8951 identity 8
```

---

## 10. 一个与第 1 步无关但你该知道的裁定

本契约**已移交**给 `Static-Contract` 仓（`ArchivalEra/Static-Contract`），此后 schema 变更、
边界裁定、版本演进都归它。**你向我提技术问题仍可以**，但**契约本身的最终解释权不在我**。
我给它写的移交信里明确写了 `Octave-Extra-Content` 退为**上游需求方之一**。
