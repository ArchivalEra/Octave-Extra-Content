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

表的 schema 与校验器产地是宿主仓 `build/extra-content/`，本仓持有副本（`port/README.md`）。内容语义（四态含义、版本策略、许可台账）归本仓。

## 供给配方（recipes/）

每个能力层一份配方：从哪拉字节、用什么 sha 钉版本、部署到站点哪里。

- `recipes/llvm-wasm.md` — 浏览器内 C++ 编译工具链（clang/lld/sysroot，73MB bundle）
- `recipes/pyodide.md` — Python 运行时（SymPy 等给 symbolic 包用）
- `recipes/msl.md` — Modelica 标准库（omc 车道能力层；含挂载语义权威配方）

## 与宿主的分工

| 谁 | 管什么 |
|---|---|
| 本仓 | 包档案事实（`packages/`）、供给配方（`recipes/`）、content-list 语义、端口副本 |
| 宿主 | 引擎、站点、装配（按本仓的表从上游拉字节、部署到同源站点） |
| UI | 消费面（包管理器界面、下载管理） |

上游来源：gnu-octave（Octave Forge）、LLVM-wasm、Pyodide。本仓只存元数据（URL + sha256），不存字节。

## 事实系统（Einfacht）

本仓用 [Einfacht](https://github.com/ArchivalEra/Einfacht) 管理事实：每个数字有出处（`build/FACTS.json` 台账 + 复跑命令）、活状态文档（`STATE.md`）与台账对账、翻案检测（`build/retractions.json`）、悬案管理（`questions/`）。

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
docs/         经验集（管线 / 事实系统 / 内存架构）
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