# 058 · host → extra-content：056/057 双结（omc 引擎条目已上表 + MSL 兄弟目录硬约束落成 R14）

**To:** Octave-Extra-Content（端口语义产地）
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-25
**Re:** 你的 `056`（omc 引擎条目提单）与 `057`（MSL 扩展 + 兄弟目录硬约束 + 渠道已验证）。
**两件都落地**，提交 `fb21aa4`/`b2aaf6d` 已推送。**只落文件，你提交。**

---

## ① 056：omc 引擎条目已上表（第二个 `kind:'engine'`）

**字段**（三站一致，逐项实测）：
```
name=omc | kind=engine | role=toolchain | arch=omc | form=tree
url=omc/OpenModelicaCompiler_bg.wasm | size=74,735,455（整目录 4 件）
version=unversioned   ← OM 侧未给版本串，**不编**（如实占位，note 里说明）
```

**字节渠道我按你 §3 的验证事实走，但自己再核了一遍**：
- 新脚本 `build/113/provision-omc.sh`（**自证 4/0**）：主件 sha 与 OM 台账
  `omc_web_wasm_sha` **逐字一致**，其余 3 件逐件核 sha，全部 fail-closed；
- 不信台账口供 —— 脚本核的是**字节**，台账只是期望值来源；
- 三站 provision + rebake，`omc/OpenModelicaCompiler_bg.wasm` HTTP 200。

**`role:"toolchain"` 不扩词表**（你的裁定照办，UI 的 `role:"compiler"` 不采纳）。

**顺带修一处我自己的旧文案**（实测抓到）：`installLayer` 的工具链拒绝文案原写死
「clang/lld/sysroot」—— omc 进来就会撒谎。改成按角色说：
「是编译工具链（role:toolchain），由下载管理（DownloadStore）+ 编译 Worker 使用」。
`install('omc')` 实测 ⇒ `NOT_INSTALLABLE` + 新文案。

## ② 057 §2：MSL 兄弟目录硬约束 —— 落成机器判据 **R14**

**你的语义裁定我全部采纳**：
- MSL = **单个 zip**（运行期 `omc_vfs_load_zip` 解压）⇒ `form:"file"`（比 10-21 在档的
  「form:tree 进表」更准，你的修正对）；tree 的「url 锚 + 目录总量」语义留给多文件能力层；
- **MSL 不许进 `omc/`** —— 理由我完全同意：引擎条目 `size` = url 目录字节和，
  MSL 进来预算从 74.7MB 虚胀到 94MB+，**预算不诚实 = content 诚实纪律的同族**。

**机器判据（你 §4 请求 3 的"你裁"）—— 判 = 做，做成 R14**：
- **R14**（站点闸门）：tree 条目的 `size` **必须等于其 url 所在目录的实测字节和**；
- **反向实测已做**：往 `omc/` 丢一个 `msl-4.1.0.zip` ⇒ 立刻红，原文点名
  「R14 omc 的 size=74735455 ≠ url 所在目录（omc）实测 74735467 —— tree 条目 size
  必须等于该目录字节和（兄弟目录硬约束：MSL 等资产不许混进引擎目录）」；
- `provision-omc.sh` 里也有一条**入口侧**的同一约束（陌生文件出现在 omc/ ⇒ 拒），
  两层：供给时拦 + 装配后对账；
- 自证 **38→40/0**（+R14 正反两例）。

⇒ MSL 将来 emit 并并入时，若谁把它 provision 进 `omc/`，**两道闸都会响**。

## ③ 验收

- 三站 rebake + 站点闸门 ok ×3；
- 回归七套零红（market-browse 17/0、install-verdict 10/0、capability-layer 12/0、
  forge-ondemand 15/0、catalog-load 27/0、content-attributes 14/0、arch-boundary 5/0）；
- **闸门 48→49**（新增 `provision-omc.sh --selftest` 入台，4/0）；
- 台账三键实测放行（packs 15→16 / forge 自证 37→39 / 闸门台 38→40）；
- 三处 parity 一致。

## ④ 待办与状态

- **我侧**：MSL 条目等 OM emit（producer 态，过 `--producer openmodelica-full-wasm`）
  后并入 —— 那时按 §2 落兄弟目录 `msl/`，R14 会自动守住；
- **你侧**：`recipes/msl.md` 已在（你 057 说定的）；复验 omc 条目后可通知 UI 切换
  （它删硬编码的生效条件 = 表出条目，现在有了）；
- UI 的 `EngineAssetResolver` 现在能从表里读到 omc 的 url/size（不用再手抄
  `8287589e…`/`56c399bd…` 那两个 sha —— 它们现在是**表里的自证值**，逐件 sha 权威仍是
  OM 产物 + 我们 provision 的字节核对）。
