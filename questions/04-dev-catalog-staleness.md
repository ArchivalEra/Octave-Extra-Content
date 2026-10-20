# 悬案 04：dev 形态下 catalog 陈旧无对账（C-3）+ 顶层 version 指向 withheld 的呈现判据（C-4）

**Status:** needs-triage

**Raised:** 2026-10-20（UI 钓鱼 D7/U-4/C-4 收编）

## 事实

- UI dev/自有部署读自己 `public/assets/forge-catalog.json` 静态副本（shelf `922736a`），
  落后 8761 现役（`285af2f`）两代——无 llvm-wasm、无 description 新字段，**无任何陈旧告警**。
- 契约「唯一同源端点 = 宿主站点」在 dev 形态下被架空。
- 顶层 `version` 若指向 withheld 候选时 UI 应如何呈现（置灰？回退最新 staged？），
  契约未写判据；当前 8761 无此形态未测。

## 结算实验（可区分两种结论）

两问各自可独立结案：

- **C-3 判据**：三方（host/UI/本仓）对「dev 取数路径约定」回执一致（env var 指 8761
  **或** 同步脚本带 `shelf_commit` 新鲜度检查，二选一或都拒）。
  - 三方书面一致 ⇒ 按裁定的路径写进 `port/README.md`（结案 rc=0）；
  - 任一方反对且无替代方案 ⇒ 约定不成，dev 陈旧记为**已知边界**进 STATE（结案 rc=1）。
- **C-4 判据**：`page.route` 注入「顶层 version = withheld 候选」catalog 变体，开 UI
  实测现行为并截图归档：
  - UI 现行为已是「顶层置灰 + 提示可用版本」⇒ 判据照现行为写进 port/README.md（rc=0）；
  - 现行为是别的（如照常可装/静默）⇒ 记缺陷投 UI，判据定为「顶层置灰 + 提示」
    并等它修后复验（rc=2）。

**Settling**: `sh settle-04.sh` —— C-3 段 grep 三方信箱回执的一致性（rc=0/1），
C-4 段跑注入变体实验出截图（rc=0/2）；两段都出结论本悬案才结。

（结算件 `settle-04.sh` 尚未落盘——本悬案挂出时实验未启动；落盘与启动一并做，
不提前声明已存在的东西。）
