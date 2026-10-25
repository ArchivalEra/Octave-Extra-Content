# 供给配方 · MSL（Modelica 标准库，omc 车道能力层）

> **性质**：**配方**（从哪取 + 什么 sha + 怎么挂），**不是字节**。字节产地 = 邻仓
> [ArchivalEra/OpenModelica-Full-Wasm](https://github.com/ArchivalEra/OpenModelica-Full-Wasm)
> 的站内资产（安装形状重打包）。**生产者 = OM 仓**（其 `mail/016` 出资产身份三件套；
> 台账键 `msl_asset_sha` / `msl_asset_bytes`，fail-closed 每提交复跑）。
>
> **权威事实在生产者那边** —— 本文件是**消费侧的摘录**，带出处；两侧不一致时
> **以 OM 仓的台账为准**，并回来更新本文件。

## 上游身份

| 项 | 值 | 出处 |
|---|---|---|
| 仓 | `https://github.com/ArchivalEra/OpenModelica-Full-Wasm` | — |
| 站内资产 | `site-omc/assets/omc/msl-4.1.0-maint.om.zip`（站内相对） | OM `mail/016` |
| bytes | **19,482,938**（本机实测 = OM 口供逐字一致，2026-10-25） | `stat -c%s`（复跑见下） |
| sha256 | `a97d8d94ca7f7960f7f1c209613a35d65bcfa2426660e5052617e71326308535` | 同上 |
| 版本锚 | `8df0769a…`（上游索引版本串，与 GitHub 源 zip 同 commit） | OM `mail/016` |
| 上游源（记账） | `OpenModelica-ModelicaStandardLibrary` @ `8df0769a`（GitHub 源 zip 20,362,007B，sha `ba66dd3a…`） | OM `mail/012` §A1 |
| 打包形状 | **安装形状**（`Modelica/package.mo` 在顶层；5067 zip 条目，解压 48,831,815B）——≠ GitHub 源 zip 的仓库快照形状 | OM `mail/016` 修正① |
| 许可 | **BSD-3-Clause**（Modelica Association，包内顶层 `LICENSE` 亲读）；子库许可在 `Modelica/Resources/Licenses/` | 本机解 zip 实测 |

**对账口径**（OM `mail/016` 修正①收编）：站内 zip 是重打包 ⇒ **sha 对版本锚
（`8df0769a`），不对 GitHub 源字节**（形状不同，字节必不等）。条目 fail-closed 的
sha256 = **站内 zip 自己的字节**（上表 sha256），不是上游源 sha。

## 挂载语义（★ 权威安装配方 —— UI 三问 Q3 的裁定载体）

| 项 | 值 | 判据 |
|---|---|---|
| 挂载点 | `/.openmodelica/libraries`（omc 默认库目录） | OM `mail/016` 修正②实测 |
| 调用形状 | `omc_vfs_load_zip('/.openmodelica/libraries', zipBytes)` —— **一次 fetch + 一个调用** | 同上（浏览器端到端 PASS） |
| ★ 反例 | `MODELICAPATH` 经 `omc_set_env` **传不进 loader**（设了仍用默认目录）——产物 `.d.ts` 契约里的 "point MODELICAPATH at mount" 在本产物上**不成立** | 同上（记档，勿按 `.d.ts` 实现） |
| 装后判据 | `loadModel(Modelica)` = true、版本 `"4.1.0"`；反向：`loadModel(NoSuchPackageXYZ)` 必须失败 | OM `mail/016` 判据（探针 `site/msl-local.html`） |

**归属**（2026-10-25 裁定，回 UI `083-ui` Q3）：挂载语义**不进** `consumer` 轴
（轴语义 = 「哪面可用」，包含语义，不是「怎么装」）、**不加** schema 键（§2 判决
能力层 = 普通条目不引入新字段；且挂载点是 omc 产物实现细节——已被实测翻案过一次，
焊进 schema 会在下次翻案时变成 schema 变更，note/配方可单侧更新）。**载体 =
本配方（权威）+ 条目 `note`（一句话指向）**；实现归 UI 的 omc 车道适配器。

## 条目形状（出表指导，OM 为出表方；宿主装配后进 forge-catalog）

```
name: "modelica-standard-library"   version: "4.1.0+maint.om"     form: "file"
content: []            consumer: ["omc"]             role: "package"
sha256: <站内 zip 字节>  size: 19,482,938             arch: 省略（无 oct 内容）
url: 站内同源相对（装配定）；upstream_url: 上游源 zip（记账）
license: "BSD-3-Clause (Modelica Association); sublibrary licenses in Modelica/Resources/Licenses/"
note:   挂载语义一句话 + 配方指路（本文件）+ 版本锚 8df0769a
```

- **`name` = `modelica-standard-library`**（2026-10-25 裁定：采 OM `mail/018` §4 申辩。
  判据：catalog 名携带上游身份是既有先例〔llvm-wasm / pyodide / octave-forge 包名〕；
  表是公开机器产物，通用缩写 `msl` 不可检索；名字将成 deps 边目标与安装键，现在改
  一个串、将来改不动）。

- **`form:"file"` 不是 `form:"tree"`**（对 2026-10-21 在档推断的修正）：MSL 交付 =
  **单个 zip 文件**（解压发生在运行期 `omc_vfs_load_zip`，不在站点侧）；单文件形态
  size == 字节数，sanity 干净。
- **★ 站点落位硬约束**：MSL zip **不许落进引擎条目的树目录**（UI 站 `omc/`——引擎
  `form:"tree"` 的 size = 该目录字节和；混入 MSL 会把 74.7MB 的引擎预算虚胀成
  94MB+）。落**兄弟目录**——**落定值 = `assets/msl/`（宿主表 url 口径，宿主 `060`
  并入后定，2026-10-25）**。★ 教训（UI `085-ui` §一）：**落位以表 `url` 为准，示例
  不是规范**——本文件早先的示例「如 `msl/`」被读成路径规格，UI 首镜像到
  `public/msl/` 与表 url 错位（表指 404、字节在 200）；已对齐 `assets/msl/`。
- `versions[]` 省略（单版本能力层，与 llvm-wasm/pyodide 同形）；MSL 升级时再启用
  多候选。

## pin 载体（本仓不含字节）

| 层 | 载体 | 谁核对 |
|---|---|---|
| 资产身份 + 字节 | OM 仓台账 `msl_asset_sha` / `msl_asset_bytes`（fail-closed 每提交） | OM `check_facts_replay.py` |
| 投放渠道 | OM release asset →（建议）UI CI 镜像 + fail-loud（期望值 = OM 台账）→ UI 站兄弟目录 | UI CI（引擎同模式，056→083 线已验证） |
| 站点副本 | 宿主装配（同源改写 url + provision） | 宿主 `validate-content-list.py --site` |

## 复跑命令（本文件每个数字的出处）

```bash
# 资产身份（OM 部署盘在本机；与 OM 台账逐字对账）
stat -c%s /mnt/hdd/openmodelica-wasm-build/site-omc/assets/omc/msl-4.1.0-maint.om.zip
sha256sum  /mnt/hdd/openmodelica-wasm-build/site-omc/assets/omc/msl-4.1.0-maint.om.zip
# 打包形状（条目数 / 解压字节）
unzip -l /mnt/hdd/openmodelica-wasm-build/site-omc/assets/omc/msl-4.1.0-maint.om.zip | tail -1
# 许可（顶层 LICENSE 亲读，不引二手）
unzip -p /mnt/hdd/openmodelica-wasm-build/site-omc/assets/omc/msl-4.1.0-maint.om.zip LICENSE | head -3
# 浏览器端到端（OM 侧判据，探针在 site/msl-local.html）
#   起服务 → /msl-local.html → __msl 探针：vfs:4376 / loadModel:true / reverse:fail-ok
```

## 待办（本仓视角）

- [x] OM：MSL zip 挂 release asset（引擎产地渠道线同模式）—— `mail/018` §3 完成，
      GitHub digest 与台账逐字一致（我方 gh api 亲核）。
- [x] OM：按上表形状出 content-list 一条（producer 态，name 用全称），过宿主校验器
      `--producer openmodelica-full-wasm` —— `mail/018` §2 完成；**我方亲跑宿主校验器
      双模式（producer/site）均 ok**（2026-10-25）。
- [x] 宿主：装配进 forge-catalog —— `mail/060` 完成（17 packs；R14 + 装配器落位
      缺陷两修收编；三站 + isui.ren 线上表均 17，我方亲验）。
- [x] UI：镜像刷新 + 落位对齐 `assets/msl/` —— `085-ui` 完成（表 17 packs /
      `assets/msl/` 200，我方线上亲验）。
- [ ] UI #3（删硬编码）：等 `files[]` 逐件 sha 链条（~~OM 台账补 JS 键~~ ✓ `021`
      已上账、我亲跑其 30 条复跑闸门核过 → 宿主 schema + 装配投影〔我 `090` 在途〕
      → 表出现 files[]）—— 裁定见 STATE 当日 ★ 条目与信 `090`/`091`/`092`。
- [x] UI #4/#5（MSL 供给面 + 装载按本配方）：`086-ui` #4 下载侧 + 供给面落地
      （form:file 分支 + 响亮拒；consumer 筛选两条正确筛出——我抽验）；
      #5 工具体随 wire 面裁定（A，我 `093`）上线。
- [x] 字节对账（本机实测 bytes + sha 与 OM `mail/016` 逐字一致，2026-10-25）；
      迁移兄弟目录后**复测一致**；isui.ren 线上字节**六方一致**（OM 台账 / 盘前后
      两次 / GitHub digest / 线上下载）。
