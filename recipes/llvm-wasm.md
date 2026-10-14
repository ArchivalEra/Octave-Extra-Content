# 供给配方 · LLVM-wasm 工具链（浏览器内编 `.oct` 用）

> **性质**：**配方**（从哪取 + 什么 sha + 预算），**不是字节**。字节由宿主 provision 到
> 站点（同源是 COEP 下的硬约束）。**生产者 = 邻仓 [ArchivalEra/LLVM-wasm](https://github.com/ArchivalEra/LLVM-wasm)**。
>
> **权威事实在生产者那边**（`release/out/manifest.json`，逐资产 name/bytes/sha256/license）——
> 本文件是**消费侧的摘录**，带出处；两侧不一致时**以生产者的 manifest 为准**，并回来更新本文件。

## 上游身份

| 项 | 值 | 出处 |
|---|---|---|
| 仓 | `https://github.com/ArchivalEra/LLVM-wasm` | — |
| 发布 tag | **v0.1.1** | `gh release list -R ArchivalEra/LLVM-wasm` |
| 发布资产 | `llvm-wasm-bundle-v0.1.1.tar.gz`（**34,679,853 B**）/ `manifest.json` | 同上（本轮实测） |
| bundle sha256 | `a9ba3b41e5fa8e7445e9b8ffaf32ca73e10ae9285bc1afc5327d0f549c84f733` | `sha256sum release/llvm-wasm-bundle-v0.1.1.tar.gz`（本机实测） |
| clang 版本 | `clang version 24.0.0git (llvm-project 55ea1f4e…)` | `release/out/manifest.json` 的 `toolchain.clang` |
| emsdk 版本 | `6.0.12 (5488e087…)` | 同上 `toolchain.emcc` |
| 许可 | `Apache-2.0 WITH LLVM-exception`（clang/lld）；`LICENSE-LLVM.txt`/`LICENSE-EMSCRIPTEN.txt` 随包 | manifest `assets[].license` |

## 逐资产（**从生产者 manifest 摘录**，非手写）

| 资产 | bytes | sha256（前 16） | brotli bytes |
|---|---|---|---|
| `clang.wasm` | 48,069,274 | `198e84c4baeb3ce4` | 12,614,129 |
| `lld-wasm-only.wasm` | 33,358,910 | `8d3b6a2dcca07f07` | 8,495,303 |
| `sysroot-headers.tar`（wasm32） | 20,623,360 | `441e0ee555cb9ee9` | 1,675,293 |
| `sysroot-headers.wasm64.tar`（**wasm64 档专用**） | 20,623,360 | `f64833f92cb4c978` | 1,675,769 |
| `clang.js` | 76,240 | `2871ad1c25ddd163` | — |
| `lld-wasm-only.js` | 72,686 | `2813588e461162e2` | — |
| `driver/toolchain.mjs` | 13,092 | `0d3559e96e77ad3c` | — |
| `driver/abi.mjs` | 7,209 | `dd9a76ef660b901c` | — |
| `driver/tar-reader.mjs` | 1,782 | `3e6a7f25fef18c3b` | — |
| `driver/sysroot-bundle.mjs` | 2,621 | `ad7649a73d9d91c4` | — |

**两条与我们的档结构直接相关的实测事实**：
- **两档 sysroot 必须都发**（`sysroot-headers.tar` = wasm32 / `sysroot-headers.wasm64.tar` = wasm64）：
  拿 wasm32 的 sysroot 编 wasm64 模块 ⇒ 缺 `lib/wasm64-emscripten/pic/crtbegin-mt.o` ⇒
  产物没有 `_emscripten_tls_init` ⇒ 线程宿主拒载（`tlsInitFunc is not a function`）。
  这是**上游 issue #1**，v0.1.1 已修（缺档时**硬拒绝**而非静默降级）。
- **首拉预算**（`first_load`）：brotli **≤ 15 MB**（`per_arch`: wasm32 14,365,662 / wasm64 14,366,138）；
  **lld 首次链接才拉**（`plus_lld_brotli_bytes` 22,860,965）。⇒ 宿主侧懒加载策略照抄这个预算。

## pin 载体（本仓不含字节；这正是"不维护字节"的形状）

| 层 | 载体 | 谁核对 |
|---|---|---|
| 工具链身份 + 字节 | `URL + sha256`（宿主 `build/upstream-lock.json` 一条） | 宿主 `zreflect/check_locks.py` |
| 工具链树（可选树级见证） | `upstream/llvm-wasm` submodule | 宿主 `witness-upstream-pin.py` 的 crosscheck（release manifest 的 `llvm_source_commit` == submodule pin） |
| 站点副本 | **provision 产物**（可删可重建 = 缓存，不是维护对象） | provision 脚本逐件核 sha |

## 复跑命令（本文件每个数字的出处）

```bash
# 生产者身份与发布
gh release list -R ArchivalEra/LLVM-wasm
gh release view v0.1.1 -R ArchivalEra/LLVM-wasm --json tagName,assets

# 逐资产事实（权威出处）
python3 -c "import json;d=json.load(open('/mnt/hdd/zcode-projects/LLVM-wasm/release/out/manifest.json'));
[print(a['name'], a['bytes'], a['sha256'][:16], a.get('brotli_bytes')) for a in d['assets']]"
python3 -c "import json;d=json.load(open('/mnt/hdd/zcode-projects/LLVM-wasm/release/out/manifest.json'));print(d['first_load'])"

# bundle sha（发布件）
sha256sum /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz
```

## 待办（本仓视角）

- [ ] 宿主 `build/upstream-lock.json` 加一条 `{name:'llvm-wasm', version:'v0.1.1', url, sha256}`（宿主侧动作）
- [ ] 建档后再跑一次上游 release 核对（防"发布件被替换"——上游 Release 非持久制品）
