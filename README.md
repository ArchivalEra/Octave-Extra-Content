# Octave-Extra-Content

**额外内容仓**（extra content）：本仓管**非核心内容**的**档案事实**与**供给配方** ——
包、运行时、工具链的"从哪取、什么 sha、能不能用"。**不含字节**。

给 [Octave-Full-Wasm](https://github.com/ArchivalEra/Octave-Full-Wasm)（浏览器版 Octave，
**核心宿主**）的**按需拉取**供货。宿主是**消费适配器**，本仓是**生产适配器**，
两者之间的接缝定义在宿主仓 `build/113/NOTES-extra-content-seam.md`。**本仓不运行任何服务。**

> 本仓由 `Octave-Forge-Shelf` 升格而来（2026-10-14）。历史保留 ⇒ 原货架的 commit 仍可达
> （宿主 submodule pin `980e093` **不变**，只换了 URL）。

## 组织结构（用户点令 2026-10-14：去中间商）

```
   上游                    ┌────────────────────────────────┐
   gnu-octave ─┐           │  Octave-Full-Wasm（核心宿主）    │ ← UI 仓对它立**引擎契约**
   LLVM-wasm ──┤ 供货      │  引擎 / embed API / 四态 install │   （docs/embed-api.md）
   Pyodide ────┘           └───────────┬────────────────────┘
                                       │ 接缝：content-list（本仓产，宿主消费）
                           ┌───────────▼────────────────────┐
                           │  Octave-Extra-Content（本仓）    │ ← UI 仓对它立**内容契约**
                           │  档案事实 + 供给配方 + 端口      │   （端口 schema + 校验器）
                           └────────────────────────────────┘
```

**本仓负责**：包档案（`packages/`）、供给配方（`recipes/`）、端口规范副本（`port/`）。
**本仓不负责**：运行站点、装配站点字节、定义引擎接口 —— 那些是宿主的事
（字节同源由宿主装配：同源是 COEP 下的硬约束，跨域 fetch 实测被拦）。

## 三层事实（各归谁核对）

| 层 | 载体 | 谁核对 |
|---|---|---|
| 内容**有哪些、哪个版本** | 本仓 git 历史 + 宿主的 submodule pin | 宿主 `witness-upstream-pin.py`（每提交） |
| **字节是不是那份** | 每个版本的 `sha256` | `tools/forge-shelf.py --verify`（每提交） |
| 能不能**真用** | 每版本的 `kinds` + 包级 `verified` | `--probe`（实测，非推断） |

## 布局

```
packages/<包名>.json      每包一个档案（多版本数组；加包只加文件）
tools/forge-shelf.py      取包 / 校验 / 探测 / 出目录（纯宿主侧，含 --selftest 17 条）
recipes/                  ★ 供给配方（非包内容）
  llvm-wasm.md            clang+lld wasm 工具链（URL+sha256+首拉预算；与 LLVM-wasm release 同源事实）
  pyodide.md              Pyodide + SymPy 运行时（符号计算的共享能力层）
port/                     ★ 端口规范副本（权威产地 = 宿主 build/extra-content/）
  README.md               端口是什么、谁产地、怎么自证
docs/                     ★ 经验集（来自姊妹仓的实测，接手先读这三份）
  FORK-PIPELINE.md        供给管线：三件套 + sha256 三关 fail-closed + pin 三形态 + 5 条实测坑
                          + 迁移/改名清点表（本仓 2026-10-14 那次迁徙的流程化）
  FACT-SYSTEM.md          事实系统：为什么档案仓需要它 + 接入六步 + 三纪律 + 5 坑
                          + 本仓第一批事实建议表（6 键，各带裸命令）
  LANES-AND-MEMORY-MODEL.md  内存架构与分支线：两档判据 + 三次混编事故原话
                          + 架构纯度闸门三判据 + 多档站点与择档 + 性能线封口清单
zreflect/                 ★ 事实系统机制层（vendored 自上游 Einfacht）+ 本仓数据层
  measure_extra_content.py  本仓数据层（**唯一自己写的那个文件**：量货架/工具/配方字节）
  check_*.py / facts.py / … 机制层（声明即闸门；执行面读 registry --run <相位>）
reflect-hooks/            git hooks（core.hooksPath 指这里）+ Einfacht.env 旋钮载体
gates-selftest.sh         闸门自证台（每个闸门先证明自己会红）
build/                    ★ 事实台账（FACTS.json）/ 翻案台账（retractions.json）/ 锁定源清单
questions/                ★ 悬案（未结案的问题，每条挂可跑的结算件）
STATE.md / AGENTS.md      活状态文档 + agent 硬规矩（机器块由 facts.py 渲染，不手改）
```

> **接手先读**（按顺序）：① 本 README（角色与边界）→ ② `docs/FORK-PIPELINE.md`（供给纪律）
> → ③ `AGENTS.md`（本仓硬规矩 + 复跑命令）→ ④ `STATE.md`（活状态：现在是什么，数字引用台账键）
> → ⑤ `docs/FACT-SYSTEM.md`（事实系统为什么这样接）→ ⑥ `docs/LANES-AND-MEMORY-MODEL.md`
> （内容有"档"属性，决定档案怎么标）。
> 与宿主的对话面 = 宿主仓 `build/113/NOTES-extra-content-seam.md`（接缝）与其 §8（组织判决）。

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

⚠️ **`kinds` 有一个已知会说谎的角落**（实测，2026-10-14）：`symbolic` 探出 `['m']`
（与真·开箱即用的 `cgi` 判得一模一样），但它的 `DESCRIPTION` 明写
`SystemRequirements: python, sympy (>= 1.5.1), mpmath (>= 1.0)` —— 本构建没有 Python
运行时 ⇒ **装上跑不动**。⇒ 这类包要标**能力层需求**（配方见 `recipes/pyodide.md`）。
规模实测：144 个上游包里只有 **2 个**（`symbolic`、`pythonic`）。

> ⚠️ **表示法尚未定**，且本文曾把它错引成「接缝 §2 的 `needs` 轴」（**已翻案，见 R-002**）
> ——**实测接缝 §2 没有 `needs` 这个轴**（`grep needs` 该文件返回空），宿主侧也无任何代码读它。
> §2 的判决是：能力层 = `form:"tree"` 的普通条目、进同一张 `deps` 图、**不引入新字段**。
> 表示法怎么落见悬案 `questions/02-capability-layer-axis.md`。

## 用法

```bash
python3 tools/forge-shelf.py --list
python3 tools/forge-shelf.py --fetch quaternion --cache /path/to/cache
python3 tools/forge-shelf.py --probe quaternion --cache /path/to/cache
python3 tools/forge-shelf.py --verify --cache /path/to/cache
python3 tools/forge-shelf.py --emit out.json --octave 11.3.0
python3 tools/forge-shelf.py --add <包名>            # 从上游索引加新包档案
python3 tools/forge-shelf.py --selftest              # 17 条（三类用例齐备）
```

## 纪律

- **只上验证过的**：`verified: null` 的条目 `--emit` 默认跳过（`--allow-unverified` 才带）。
- **fail-closed**：sha256 不符 ⇒ 拒绝（`--fetch` / `--verify` 都查）。
- **零值守卫**：空货架 / 空缓存 / 空改动集 ⇒ 全部报错，不当"通过"。
- **每个子命令都有判据**，`--selftest` 三档齐备（正常不报 / 该报的必须报 / 空输入必须报）。
- **诚实优先于好看**：探到什么写什么 —— 上面那个 `['m']` 的谎就是这条纪律发现的。

## 边界（不做什么）

- **不托管站点 / 不装配字节 / 不运行服务**（纯客户端铁律；字节同源由宿主装配）。
- **不定义引擎接口**（引擎契约只能属于引擎 —— 见接缝 §8.1）。
- **不改宿主仓**（路径铁律）；宿主的消费面由宿主维护。

## 许可

本仓只含**元数据与配方**（上游公开事实 + sha256 + URL）。包本身的许可见各自 `COPYING`；
取包不改变上游许可。工具链 / 运行时的许可逐条记在 `recipes/*.md`。本仓自身 AGPL-3.0-or-later。
