# Octave-Forge-Shelf

**Octave-Forge 包的货架**：只存**档案事实**（每包一文件），不存字节。

给 [Octave-Full-Wasm](https://github.com/ArchivalEra/Octave-Full-Wasm) 的**按需拉取**用：
客户端需要一个包时才去上游取，**没用到 = 0 字节下载**。本仓是那次"购物"的**目录**。

## 为什么是独立仓库

用户裁定（2026-10-09）：做成独立仓 ⇒ **复用主仓已有的 fork/lock 管线三件套**，
于是"货架上有什么、哪个版本"由 **submodule commit** 承载，"字节是不是那份"由 **sha256** 承载。
⇒ **能力与包数解耦**：加包 = 加一个 `packages/<name>.json` 文件，
主仓的 provision / witness / 客户端安装器**一行都不用改**。

| 层 | 载体 | 谁核对 |
|---|---|---|
| 货架**内容**（哪些包、什么版本） | 本仓 git 历史 + 主仓的 submodule pin | `witness-upstream-pin.py`（每提交） |
| 货架**字节**（tarball 是不是那份） | 每个版本的 `sha256` | `tools/forge-shelf.py --verify`（每提交） |
| 包**能不能用** | 每版本的 `kinds` + 包级 `verified` | `--probe`（实测，非推断） |

## 布局

```
packages/<包名>.json      每包一个档案（多版本数组；加包只加文件）
tools/forge-shelf.py      取包 / 校验 / 探测 / 出站点目录（纯宿主侧，含 --selftest）
```

## 包档案形状

```json
{ "schema": 1, "name": "quaternion",
  "depends": [],                                  // 包间依赖（闭包由客户端解析）
  "upstream": { "index": "gnu-octave/packages", "description": "…", "links": {…} },
  "verified": { "octave": "11.3.0", "how": "detect_kinds（tar 内容判 m/oct）", "tarball_sha": "…" },
  "versions": [ { "version": "2.4.2", "url": "https://…", "sha256": "…", "size": 47838,
                  "requires": ["octave (>= 4.0.0)"], "date": "…",
                  "kinds": ["m"], "in_index": true } ] }
```

`kinds` **三态**（后果完全不同，实测精化）：
`m` = 纯 `.m`（开箱可用）· `src` = 带 `src/` 源码但**没有**现成 `.oct`（`.m` 照样可用，
只是缺加速件）· `oct` = 随包带预编译 `.oct`（异架构，wasm 里必须重编）。

## 用法

```bash
python3 tools/forge-shelf.py --list
python3 tools/forge-shelf.py --fetch quaternion --cache /path/to/cache
python3 tools/forge-shelf.py --probe quaternion --cache /path/to/cache
python3 tools/forge-shelf.py --verify --cache /path/to/cache
python3 tools/forge-shelf.py --emit out.json --octave 11.3.0
python3 tools/forge-shelf.py --add <包名>            # 从上游索引加新包档案
python3 tools/forge-shelf.py --selftest              # 14 条（三类用例齐备）
```

## 纪律

- **只上验证过的**：`verified: null` 的条目 `--emit` 默认跳过（`--allow-unverified` 才带）。
- **fail-closed**：sha256 不符 ⇒ 拒绝（`--fetch` / `--verify` 都查）。
- **零值守卫**：空货架 / 空缓存 / 空改动集 ⇒ 全部报错，不当"通过"。
- **每个子命令都有判据**，`--selftest` 三档齐备（正常不报 / 该报的必须报 / 空输入必须报）。

## 许可

本仓只含**元数据**（上游索引的公开事实 + sha256）。包本身的许可见各自 `COPYING`；
取包不改变上游许可。本仓自身 AGPL-3.0-or-later。
