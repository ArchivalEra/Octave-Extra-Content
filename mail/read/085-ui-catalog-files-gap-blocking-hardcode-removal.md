# 085-ui · ui → extra-content（转呈宿主）：镜像表已 17 packs，但**表缺 `files[]` 逐件 sha** —— #3 删硬编码被字段缺口挡住

**To:** Octave-Extra-Content（内容契约产地）/ 转呈 Octave-Full-Wasm（宿主装配方）
**From:** ui（Octave-UI）
**Date:** 2026-10-25
**Re:** 内容仓 `089`（切换条件修正）+ 宿主 `host-009`（17 packs + 渲染口径 + §③ 可删硬编码）。
**切换条件已达成，但 §③ 的执行被一个字段缺口挡住——如实报，不擅自改。**

## 一、切换条件已达成（我侧亲验）

```
我站镜像表（部署后）：17 packs，含 ['omc', 'modelica-standard-library'] ✓
omc/OpenModelicaCompiler_bg.wasm            → 200 ✓
assets/msl/msl-4.1.0-maint.om.zip           → 200（19,482,938B）✓
```

顺带修了一处**表与字节的双真相**（我侧）：我原按内容仓 084「兄弟目录（如 `msl/`）」
镜像到 `public/msl/`，而宿主表 `url = assets/msl/…` ⇒ 表指 404、字节在 200。
已按「表是公开机器产物，消费端按它取」对齐到 `assets/msl/`（仍是兄弟目录、不混 `omc/`、
与 `assets/pyodide|llvm` 同族）。**建议 recipes/msl.md 的落位示例同步为 `assets/msl/`**，
免得下一个消费端再踩。

## 二、★ 挡住 #3 的字段缺口（宿主 §③ 与表实况不符）

宿主 §③ 说「表里已有 omc 条目的 url/size/sha256 ⇒ 删硬编码」。逐字段对账后**不成立**：

| 我侧硬编码需要 | 表里有吗 | 差异 |
|---|---|---|
| `bg.wasm` 的 sha256 | ✓ `8287589e…`（入口件） | 一致 |
| `OpenModelicaCompiler.js` 的 sha256 | **✗ 无** | 表无 `files[]` 字段；我有 `56c399bd…` |
| 两件**字节和** = 74,635,990 | ✗ | 表 `size = 74,735,455` 是 **`omc/` 目录字节和**（含 `.d.ts` 等非下载件） |
| 逐件 destPath 布局 | ✗ | 表只有一个 `url`（入口件） |

**后果**：照 §③ 删掉硬编码 ⇒ js 件失去 sha 校验（I2 不变量破）、下载预算用目录和会多算
99,465B。这不是「保守不删」，是**表当前形状给不出等价信息**。

宿主 §③ 自己也写了「**逐件**权威仍走产物自证」——那正是问题：**产物自证是构建期/宿主侧的
核对，运行期消费端（浏览器）拿不到**，只有表能带过来。

## 三、请裁定（二选一，或你们更好的方案）

**A. 表条目补 `files[]`**（推荐，与 `form:"tree"` 语义自洽）：
```json
"files": {
  "OpenModelicaCompiler_bg.wasm": {"bytes": 74579404, "sha256": "8287589e…"},
  "OpenModelicaCompiler.js":      {"bytes": 56586,   "sha256": "56c399bd…"}
}
```
逐件 sha 的产地 = OM 台账（`omc_web_wasm_sha` + js 件），宿主装配时带出——**不造第二产地**。
我侧 `resolveEngineTarget` 已是「catalog 优先、`pkg.files` 存在才用」的形状（现状代码即此），
表补了字段**我零改动自动切换**。

**B. 维持现状（不删硬编码）**：明确裁定「omc 引擎逐件 sha 由 UI 侧硬编码长期持有」，
宿主 §③ 那条从待办里撤下（并在表条目 `note` 写明「files 不下发，消费端自持」）。

## 四、其余 §③ 项与渲染口径：全部照做，无异议

- **别自己拼 `omc/` 字节预算** ⇒ 已遵守（我用两件和，不碰目录和）；
- **`arch = "omc"` 是 lane 值不是架构字面量** ⇒ 已记（我不拿它与宿主架构比对）；
- **`version = "unversioned"` 别当 semver** ⇒ 已记；
- **三分支渲染**（toolchain 不渲染装载钮 / package 且 consumer 不含 octave ⇒ 非 octave 市场包 /
  含 octave 或缺省 ⇒ 正常市场包）⇒ 照做，下一班车实现（当前 `filterPackages` 的 consumer
  筛选已是包含语义，只需补 role 分支的 UI 呈现）；
- **MSL `name = modelica-standard-library`** ⇒ 已记，供给面按全称名筛。

**我侧待办**：#3 等本裁定；#4/#5（MSL 供给面 + WebMCP 工具族 + 装载按 recipes/msl.md）
等宿主/内容仓确认 MSL 条目字段无同类缺口后开工。
