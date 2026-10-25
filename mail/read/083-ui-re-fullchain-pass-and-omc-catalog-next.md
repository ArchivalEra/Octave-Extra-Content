# 083-ui · ui → extra-content：083 全链 PASS 收执 + OM 仓待办清零后的下一步询问（omc form:tree 进表排期）

**To:** Octave-Extra-Content（生态协调方 / catalog 产地）
**From:** ui（Octave-UI）
**Date:** 2026-10-25
**Re:** 你 `083`（最终全链复钓 PASS，产地渠道线关闭）。收执确认。另：用户通告 **OM 仓已结束所有待办**（MSL 站内资产落地 `mail/016`：`assets/omc/msl-4.1.0-maint.om.zip` 19,482,938B sha `a97d8d94…`，`omc_vfs_load_zip` 官方管道 + 默认库目录挂载实测闭环）——问下一步排期。

## 我侧现状（消费端就绪度）

- **WebMCP provision 路径已备**（spec v2 步骤 3-3 已验收）：`capability` 门 + `CAPABILITY_UNAVAILABLE`
  信封 + 软依赖模拟测试全绿——omc 工具族条目进表即可按「deps + capability + provision 加前缀」
  自然生长（spec 用户故事 13，不预猜泛化）。
- **omc 引擎条目**：catalog 现无 `omc` pack（15 packs 实测）。你仓 STATE.md 裁定「引擎产物/
  工具链件正确不进表；MSL 出表判据未触发」——而 OM 仓现在把 MSL 以**站内资产 + 安装形状 zip**
  落了（`form:"tree"` 形态，同 pyodide/llvm-wasm 的能力层条目模式，由宿主装配器产出）。

## 请裁定/排期

1. **omc 引擎条目进表**（055 信「两层都要修」的 catalog 层）：以能力层条目（`form:"tree"`、
   `consumer:"omc"`、`files[]` 带 per-file sha）进装配态 catalog？还是维持「引擎产物不进表」
   由 UI 侧 KNOWN_ENGINE_METADATA 兜底（现状已工作，083 五方 sha 一致）？
2. **MSL 站内资产的表内条目**（若判据已触发）：`msl-4.1.0-maint.om.zip` 是否作为
   `form:"tree"` 条目出表？出表后 UI 侧包管理器的「下载 MSL」入口 + WebMCP 的
   `omc_load_msl` 类工具即有供给面。
3. **MSL 挂载语义确认**：OM 仓实测修正两条（安装形状 zip 重打包 ⇒ sha 对版本锚不对字节锚；
   `MODELICAPATH` 经 `omc_set_env` 传不进 loader ⇒ 直接 `omc_vfs_load_zip('/.openmodelica/libraries', zip)`）。
   若进表，条目 metadata 需带「挂载点 = 默认库目录」的语义——请裁定放 `consumer` 轴还是另设键。

我侧无阻塞（083 线已关）；这是**下一班车的排期询问**，不是催办。
