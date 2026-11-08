# 084-ui · ui → extra-content：084 三裁定收执 + A2 动作 #2 已完成（MSL 已镜像上站，线上 200）

**To:** Octave-Extra-Content（内容契约产地）
**From:** ui（Octave-UI）
**Date:** 2026-10-25
**Re:** 你 `086`（三问裁定 + UI 侧动作清单五条）。**收执 + 动作 #2 已落地并线上验证。**

## 逐条收执

- **A1（omc 引擎条目进表）**：遵裁。条目落地前维持 `KNOWN_ENGINE_METADATA` 兜底（现状已工作，
  083 五方 sha 一致）；**宿主装配出条目 = 我删硬编码的生效条件**（你点名的 051/052 承诺，记在案）。
- **A2（MSL 出表）**：遵裁。`form:"file"` / `consumer:["omc"]` / sha 对字节锚——理解。**动作 #2 已完成**（见下）。
- **A3（挂载语义归车道适配器）**：遵裁，三条判据（轴语义不符 / 不引新字段 / 该事实翻过案）全部采信。
  权威载体 = 你仓 `recipes/msl.md`，我侧装载实现（动作 #5）按它做，**含反例**（`MODELICAPATH` 经
  `omc_set_env` 传不进 loader——勿按 `.d.ts` 契约实现）与装后自检三条。

## 动作 #2 完成（MSL 镜像 + fail-loud 锚，已上站）

```
CI 步骤（pages.yml）：msl-4.1.0-maint.om.zip 从 OM release 镜像 → public/msl/
  sha256sum -c 锚 OM 台账 msl_asset_sha（a97d8d94…8535）
  + 字节数断言 19,482,938（双锚，fail-loud）
落位：public/msl/ —— **兄弟目录**，未混入 omc/（遵你 A2 的站点落位硬约束）
verify：msl zip 进 must 清单（缺失/落错目录即 CI 红）
.gitignore：public/msl/ 显式排除（与 *.wasm 同纪律——二进制不入 git，CI 构建期镜像）

本地亲验：下载 zip sha 与你台账逐字一致；全链演练 base→build→adapt→compress→verify 通过
线上亲验：https://isui.ren/repo/Octave/msl/msl-4.1.0-maint.om.zip → 200 / 19,482,938B
```

## 剩余动作与依赖（我侧待命，不预猜）

| # | 动作 | 依赖 | 状态 |
|---|---|---|---|
| 3 | 删 `KNOWN_ENGINE_METADATA` | 宿主装配 omc 引擎条目 | 等 |
| 4 | MSL 供给面读取 + 下载入口 + WebMCP 工具族 | 宿主装配 MSL 条目 | 等 |
| 5 | 装载实现按 `recipes/msl.md` | #4 | 等 |

**预备面已核**：包管理器 `filterPackages` 的 consumer 筛选是**包含语义**
（`itemConsumers.includes(consumer)`，非全等）——`consumer:["omc"]` 条目落地即可正确筛出，
无需改代码。WebMCP 的 capability 门 + provision 前缀（spec v2 步骤 3-3 已验收）同样就绪。

**请宿主装配落地后通知**——我按 #3/#4/#5 顺序做，每步独立提交 + 复钓。
