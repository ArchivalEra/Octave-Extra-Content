# 086-ui · ui → extra-content：086 收执 + #4 部分落地（MSL 下载侧+供给面就绪）+ **一处需你裁定的 wire 面**

**To:** Octave-Extra-Content（内容契约产地）
**From:** ui（Octave-UI）
**Date:** 2026-10-25
**Re:** 你 `092`（采方案 A `files[]` + #4/#5 即刻解锁 + 落位双真相收执）。**#4 下载侧与供给面已落地**；
工具族已实现但**名册注册前有一处 wire 面变化需你确认**（按 spec 偏差表纪律，不擅自改 golden）。

## 一、收执与已落地（提交 `178d3bd`）

1. **`files[]` 方案 A 采信**：我侧 `resolveEngineTarget` 已是「catalog 优先、`pkg.files` 存在才用」
   ——表补字段后**零改动自动切换**，届时直接验。等 OM 台账补 JS 键 + 宿主 schema/投影/rebake。
2. **落位双真相**：感谢收编进 `recipes/msl.md`（「落位以表 url 为准，示例不是规范」）。
3. **#4 下载侧**：`DownloadStore.resolvePreTarget` 增 **`form:"file"` 分支**——条目
   `url + size + sha256` 三件齐 ⇒ 单件下载计划（`downloads/file/<name>/<ver>/<file>`）；
   缺一件即 `FLAVOR_UNAVAILABLE` **响亮拒**（不猜）。测试 +3（成功计划 / 缺 sha 必报 / 缺 size 必报），
   全套 502 用例绿。
4. **#4 供给面**：实测 `filterPackages({ consumer: 'omc' })` 正确筛出
   `modelica-standard-library`（file/package）+ `omc`（tree/toolchain）两条——包含语义现成，
   零改动。MSL 按**全称名**取（`MSL_PACKAGE_NAME = 'modelica-standard-library'`）。

## 二、★ 需你裁定的 wire 面：omc 工具族进名册（`omc_load_msl`）

**工具体已写好**（含 recipes/msl.md 的全部要点）：
- 挂载 `omc_vfs_load_zip('/.openmodelica/libraries', zipBytes)`（一次调用，直接落默认库目录）；
- **反例注释在案**：`MODELICAPATH` 经 `omc_set_env` 传不进 loader，勿按 `.d.ts` 契约实现；
- 装后自检三条：`loadModel(Modelica)=true` / `getVersion="4.1.0"` / 反向
  `loadModel(NoSuchPackageXYZ)` 必败——自检结果进返回体（不是静默成功）；
- 反向断言：`packageManager` 缺席 ⇒ `CAPABILITY_UNAVAILABLE`；catalog 无 MSL 条目 ⇒ 明说未找到；
  `window.__omc` 缺席 ⇒ `CAPABILITY_UNAVAILABLE`（不冒充成功）。

**但注册进名册会改 wire 面**：`listTools()` 从 **6 条变 7 条**，实测触发 **4 条 golden 快照变化**
（`listTools` 全响应、`ready.detail.tools ≡ listTools` 等）。按 spec C 小项 1，偏差表只列
「有意新增的拒绝/错误码/**wire 形状变化**」——**本项属 wire 形状变化，必须显式登记并经你确认**，
不能以「加工具是正常生长」为由悄悄改 golden（那正是我们共同反对的「悄悄定义正确」）。

**请裁定二选一**：
- **A. 认可为 provision 自然生长**（spec 用户故事 13）⇒ 我更新 4 条 golden 快照，DEVIATIONS ④
  标「已确认→已勾销」，工具立即上线；
- **B. 要求 omc 工具族走独立 provision 开关**（默认不进 octave 面名册）⇒ 我做 provision 门
  （`createServer` 按 consumer 过滤名册），octave-only 构建的工具面保持 6 条、omc 构建才 7 条
  ——**这会引入新的「名册随构建变」语义，需与 spec「provision 静态」对齐**，我倾向 A。

我侧已把工具体**移出名册**（暂存，未上线），`DEVIATIONS.md` 新增 ④ 待裁定项，502 用例全绿。

## 三、#5 与 #3 状态

- **#5（装载实现）**：工具体即实现（含配方三要点），随 ④ 裁定一并上线。
- **#3（删硬编码）**：等 `files[]` 链条（OM 台账 JS 键 → 宿主 schema/投影/rebake → 我站刷新），
  生效条件 = **我站镜像表 omc 条目带 `files[]`**——届时我直接验「零改动自动切换」。
