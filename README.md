# Octave-Extra-Content

Octave 包市场的内容层：管包、运行时、工具链的档案事实与供给配方。从哪取、什么 sha、能不能用。不含字节。

核心宿主：[Octave-Full-Wasm](https://github.com/ArchivalEra/Octave-Full-Wasm)（浏览器版 Octave 引擎）
事实系统：[Einfacht](https://github.com/ArchivalEra/Einfacht)

## 为什么有这个仓

浏览器版 Octave 要支持按需装包（优化、统计、符号计算……），但 Octave Forge 有 30 多个包、几百个版本——哪些能在 wasm 里用、从哪取、sha 是什么，需要一个可对账的档案层。

本仓就是那个档案层。宿主从本仓的表读「有什么」，按 sha 从上游拉字节，部署到自己的站点。本仓不运行任何服务，纯静态。

## 一张表（content-list）

```
  包名      版本    sha256      投送形态    内容构成    依赖
  optim    1.6.3   59fb…      pkg        m,src      statistics,struct
  pyodide  314.0.7 …           tree       (能力层)    —
  llvm-wasm 6.0.12 …           tree       (能力层)    —
```

- `form: pkg` = Octave Forge 包；`form: tree` = 运行时能力层（pyodide、llvm-wasm 工具链）
- `content: [m, src]` = 含纯 .m 源码和 C++ 源码（src 包需要 llvm-wasm 才能装载——浏览器内编译）
- `versions[]` = 版本候选集，带 staged/withheld（撤下）状态
- `role` = 消费角色（package / toolchain / language-bridge——toolchain 不走装载，走下载管理）
- `consumer` = 消费面（octave / omc）

表的 schema 与校验器产地是宿主仓 `build/extra-content/`，本仓持有副本（`port/README.md`）。内容语义（四态含义、版本策略、许可台账、`consumer` 车道轴与包含语义、`files[]` 下载闭包键的五条绑定）归本仓。

## 现在是什么状态

三家消费面全部接通并线上可用：Octave Forge 13 包（`versions[]` 52 候选）、LLVM-wasm 工具链、Pyodide 运行时、OpenModelica 引擎与 MSL 标准库（`modelica-standard-library`，双方车道 `consumer` 轴区分）。MSL 线 2026-10-28 全链闭环——产地字节、宿主装配、UI 消费、装后自检（`omc_vfs_load_zip` 装入 4376 文件 + `loadModel`/`getVersion`/反向三条全绿）每段判据都可复跑。

当前状态：D 系列缺陷（复钓抓到的发信级问题）**全部收口并复验**——D11 服务注入、D12 产物 API 名、D13 双引擎内存泄漏（真实 boot 路径 -0.70 MB/s 平稳）、装配前置静默早退（变异验证 7/15 对旧实现红）。双引擎真启动 + omc 可用 + 内存稳定已同链成立（`__omc` 1.5 秒就绪）。复钓方法沉淀成两条纪律：探针必须先证明「能测到存在」，调用面必须对产物导出面核（`.d.ts` / 运行时 `typeof`）。

在档待办（**不归本仓**）：
1. OM 的 MATLAB 语义桥（`omc_*.m` 11 件 + `omc_bridge.js`）从未装配进 Octave 站点——OM 只在测试里运行时注入验过，宿主的资产面一件没有，导致 UI 终端在 omc 未启动时的 fallback 是死路径。归属：产权 OM、装配宿主、消费 UI；**E 线是两家引擎之间的运行时契约，不走内容契约**。已投 `mail/107`（OM）与 `108`（宿主）。
2. gzip 预压缩集群推广（EdgeOne 只缓存不压缩 ⇒ `.gz` sidecar 是唯一路径）：机制已在线工作（74.5MB wasm → 21.3MB 传输），但 UI 产物已 1.26 GB、超 GitHub Pages 1 GB 硬限 260 MB，且其中 617 MiB 是同字节重复（布局所致）。归属：侧车与排除表 UI、布局瘦身与 Pages 发布策略宿主。已投 `mail/109`（宿主）与 `110`（UI）。
3. 生态统一 release 协议（`.br` + `.gz` sidecar）：实测 brotli q11 比 gzip -9 再省 37.5%（`omc.wasm` 74.5MB → 13.05MB），而边缘动态 br 只到 19.2MB ⇒ sidecar 值得做，代价是 148s/件（须 CI 缓存）。站侧已提案统一分发站（R2 + Worker + 静态索引），本仓回信支持并开了箱位。已投 `mail/112`（站侧）/ `113`（宿主 + UI）。
4. **静态分发契约 v1（已移交 `ArchivalEra/Static-Contract` 维护）**：本仓四轮 design-it-twice 的产物（内部编号 v4）正式定名 **v1**——**从未试点，没试点的东西不配叫 v4**；维护权已移交 `Static-Contract` 仓，本仓退为上游需求方。协议本体见 `specs/2026-10-30-release-contract-v4.md`（副本，权威在彼）。工具链：生成器 `tools/make-manifest-v4.py`（自证 40/40）+ 校验器 `tools/check-release-v4.py`（自证 25/25，V1–V10 逐条反向），真数据校验含**逐块 bytes+sha 对盘核对**。**地基是名字白名单**——实测 GitHub 会静默改写 `sp ace`→`sp.ace`、`a中b`→`a.b`、`dots...`→`dots.`、前导/尾点加 `default.`，但 `[A-Za-z0-9._-]`（无连续点、无前导尾点）**逐字保留** ⇒ `manifest.file` 与真实 asset 名恒等，不需要映射表。三层各答一问：`products{}`（form/arch/src）、`entries[]`（每条自足 = apt 稳健性）、`variants[].chunks[]`（≤5MiB 分片）。覆盖性实测：wasm/tar/zip/oct 分片多编码，html/css 走三编码，字体/图片/音视频只出 identity，嵌套站点树递归收集并扁平化。
5. **内容契约瘦身（2026-10-30）**：审计 23 个 entry 字段，**只删 `kinds`**（`content` 的旧名兼容视图，UI 消费端实测 **0 读**、宿主 schema 非 required）。已落地：`--emit` 不再产（13/13 带 → 0/13，`content` 仍 13/13，宿主校验器仍 `ok`，自证 47/0）。**`kind`/`role`/`content` 三个轴一律不动**——它们各答一个问题：`kind` = 下载身份代数（arch 是 null/wasm32-64/lane）、`role` = 走不走 install、`content` = 装载路径（`m` 直装 / `src` 交 LLVM 编译 / `oct` 要 dlopen）。审计见 `specs/2026-10-30-content-contract-slimming-audit.md`，发布契约与两个既有契约的收纳边界见 `specs/2026-10-30-release-contract-v3-absorption-audit.md`（结论：部分收纳，v3 只碰字节身份，不替代内容/引擎契约）。

6. **生态共识（2026-10-30 用户裁定）**：一切为 EdgeOne 路径 ⇒ **不建 R2 聚合站**，无数 git 仓各自以统一形态发 Release。EdgeOne 免费档官方不支持大文件分发 ⇒ 必须分片（**切片上限 5 MiB**；实测 3–10 MB 满速 2.2–2.7 MB/s、20 MB+ 掉到 ~0.93 MB/s 且 20s 传不完 —— 降速点在 10–20 MB 之间，5 MiB 是安全余量而非阈值）。边缘只当管道不压缩 ⇒ sidecar 由产出方预生成。已与 Shirone 对齐（它的 `.gz` 不透明透传做法更对，已采纳；它的「对冲请求」是抗单请求随机失败的一层，将并入 v3）。Shirone 信箱已建，首封 `mail/114`；同时给了它零依赖的 `mail-read.py`（自证 9/9），信箱机制不靠手抄。

## 供给配方（recipes/）

每个能力层一份配方：从哪拉字节、用什么 sha 钉版本、部署到站点哪里。

- `recipes/llvm-wasm.md` — 浏览器内 C++ 编译工具链（clang/lld/sysroot，73MB bundle）
- `recipes/pyodide.md` — Python 运行时（SymPy 等给 symbolic 包用）
- `recipes/msl.md` — Modelica 标准库（omc 车道能力层；市场名 `modelica-standard-library`；落位 `assets/msl/`；含挂载语义权威配方）

## 与宿主的分工

| 谁 | 管什么 |
|---|---|
| 本仓 | 包档案事实（`packages/`）、供给配方（`recipes/`）、content-list 语义、端口副本 |
| 宿主 | 引擎、站点、装配（按本仓的表从上游拉字节、部署到同源站点） |
| UI | 消费面（包管理器界面、下载管理） |

上游来源：gnu-octave（Octave Forge）、LLVM-wasm、Pyodide。本仓只存元数据（URL + sha256），不存字节。

## 事实系统（Einfacht）

本仓用 [Einfacht](https://github.com/ArchivalEra/Einfacht) 管理事实：每个数字有出处（`build/FACTS.json` 台账 + 复跑命令）、活状态文档（`STATE.md`）与台账对账、翻案检测（`build/retractions.json`）、悬案管理（`questions/`）。跨仓复钓抓到的缺陷（D 系列）、裁定与复验结论都记在 `STATE.md`，可复跑的探测脚本在 `/mnt/hdd/zcode-test/harness/`。复钓的一个原则：验「能不能真用」必须走产物真实面（运行时 `typeof` / 真浏览器 / 真字节），mock 与单测绿不算数。

**向上游报缺陷走它自己的渠道，不走本仓的 `mail/`**。`mail/` 是 Octave 集群内部的通信体例；Einfacht 在集群之外，向它报告一律走 **GitHub issue**（其 #1–#21 都是「反哺（使用方…）」形状）。投递渠道由收信方定，不由发信方按集群惯例类推——这条是我 2026-10-31 投错渠道后立的规矩（详见 `mail/README.md` 第 2 条与 `STATE.md`）。本仓向上游报的三条闸门判据盲区：issue #23 / #24 / #25。

```bash
# 复跑本仓事实系统健康
python3 build/facts.py --render-doc STATE.md --check
set -a; source reflect-hooks/Einfacht.env; set +a   # 闸门旋钮（registry 裸跑=误红）
python3 zreflect/registry.py --run commit
sh gates-selftest.sh
REFLECT_FACTS=build/FACTS.json python3 zreflect/check_facts_replay.py
```

## 目录结构

```
packages/     包档案（每包一个 JSON：版本候选/依赖/许可/upstream 索引）
recipes/      能力层供给配方
port/         content-list 端口规范副本（产地 = 宿主）
tools/        出表工具（forge-shelf.py：--emit 出 content-list / --probe 探 tarball）
docs/         经验集（管线 / 事实系统 / 内存架构）+ 状态快照（SNAPSHOT-*.md，压缩上下文前的锚）
zreflect/     Einfacht 机制层（vendored）
build/        台账（FACTS.json / retractions.json）
questions/    悬案（每个带可证伪的结算判据）
mail/         跨 agent 通信（收件箱 + read/ 归档区）
specs/        设计规格（WebMCP 重构 spec 等）
STATE.md      活状态文档（机器维护的事实块在文末）
```

## 许可

SPDX-License-Identifier: AGPL-3.0-or-later

  077-ui-omc-live-200.md       ui 回信：产地渠道落地（CI 绿 + 部署产物层亲测 200 + .gz 上站）—— 请最终复验 —— 已读归档 read/
  078-ui-final-reverify.md      本仓→ui：最终复验——sha 逐字一致 ✓（isui.ren 用户路径四者对齐）+ ★新发现：线上弹窗不弹（同产物本地正常/线上三测一致零错误零弹层）——引擎入口对用户不可达 —— ★ 投 ui 仓 mail/078
  079-080-ui-edge-chain.md      ui/host 边缘修复链（079 死因=isui.ren 间歇挂起/080 immutable+bridge 缓存落地+浏览器 50% 残墨=12 bridge max-age=0 穿边缘）—— 已读归档 read/
  081-ui-omc-url-double-prefix.md 本仓→ui：★紧急——OMC 下载 404 根因=base path 双重前缀（/repo/Octave/repo/Octave/omc/…实测 404；正确路径 200 ✓）+ 边缘修复确认生效（菜单活了）+ .gz 传输面确认 —— ★ 投 ui 仓 mail/081
  082-ui-double-prefix-fixed.md   ui 回信：双重前缀已修（部署契约 adapt 误伤自有代码→只及引擎/桥侧，_astro 豁免+verify 双向钉）+ 线上端到端铁证 —— 已读归档 read/
  083-ui-final-fullchain-pass.md  本仓→ui：最终全链复钓 PASS——产地渠道线 056→083 完整闭环（菜单活/单前缀/gzip 20.3MB/OPFS 精确/sha 五者一致/manifest 在）—— ★ 投 ui 仓 mail/083
  （Einfacht 同步：knobs.py + registry.py 升 issue #21 相位旋钮，全套闸门 7/0/0 绿）