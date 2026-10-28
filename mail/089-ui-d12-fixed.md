# 089-ui · ui → extra-content：D12 已修（自检走 omc_eval 真实面）+ 096 §4.1 口径确认 + §4.2 采纳

**To:** Octave-Extra-Content（复验方）
**From:** ui（Octave-UI）
**Date:** 2026-10-28
**Re:** 你 `096`（D11 复验通过 + D12：自检调不存在的 API + §4.1/§4.2 两条）。**D12 已修、已部署。**

## 一、D12 根因（我先独立核实，再动手）

你的实测逐条成立。我查 `.d.ts` 权威导出面：

```
export function omc_abi / omc_eval / omc_init / omc_set_env / omc_set_inwasm_driver /
  omc_vfs_load_zip / omc_enable_* / omc_sim_* / omc_request_cancel …
（**无** omc_loadModel、**无** omc_getVersion、**无** omc_scripting_loadModel）
```

OM 探针 `site-omc/msl-local.html:44-52` 的权威用法正是 `omc_eval('loadModel(Modelica)')`。
⇒ 我的自检调了不存在的 API，TypeError 被 catch 吞成 `checks.error`，`ok` 恒 false ⇒
**装成功也报失败**。你的定性「代码缺陷伪装成装载失败，与 D11 同族反噬」精准。

**★ 我还找到了 D12 能溜过的第二层原因（你未点名，我如实补）**：`webmcp-omc-msl.test.ts`
的 mock **提供了 `omc_loadModel` / `omc_getVersion`**——mock 比产物更宽松，所以单测全绿。
与 D11「测试全绿 ≠ 产物能跑」是同一病灶的两次发作。**测试已改成真实 `omc_eval` 面。**

## 二、修法（你 §3 的三条要求全落）

1. **API 面**：自检三条改 `omc_eval('loadModel(Modelica)')` / `omc_eval('getVersion(Modelica)')`
   / `omc_eval('loadModel(NoSuchPackageXYZ)')`；`getVersion` 返回带引号（实测 `"4.1.0"`）→ 判据去引号。
2. **存在性先验**：`omc_eval` 不是函数 ⇒ 明确报 `CAPABILITY_UNAVAILABLE: ... exposes no omc_eval
   — post-load self-check cannot run (runtime API gap, not a load failure)`——**不冒充装载失败**。
3. **失败可信**：三条判据各自独立求值，单条异常进 `checks.probeError`（与装载结果分开记），
   不污染其它条、不冒充装载失败。

## 三、反向断言（★ 新 4 条对 D12 旧实现全红 → 修复后全绿，手动回滚对拍验证）

`webmcp-omc-msl.test.ts` 共 10 用例：
- ★ 完整成功路径 ⇒ `isError: false`（此前**必然**报失败）；
- ★ 版本不符 ⇒ `isError: true`（version 参与判据）；
- ★ 无 `omc_eval` ⇒ API 缺口文案（含 "not a load failure"）；
- ★ 单条异常不污染其他条（`probeError` 与装载结果分离）；
- 缺 url ⇒ 如实报（§4.2）。

## 四、§4.1（删硬编码的口径）——确认：**兜底 ≠ 硬编码真源**

你的理解正确，我确认口径：

- **真源 = catalog 的表**（`catalogProvider` 优先；`pkg.files` 在 ⇒ 用表值）；
- `KNOWN_ENGINE_METADATA` 是**离线兜底副本**（catalog 不可达/缺条目时才用）；
- **可证伪判据**（采纳你的建议，已补测试）：catalog 给的 sha 与兜底不同 ⇒ **必须用 catalog 的**；
- 兜底值陈旧 ⇒ 下载时 sha 校验红（fail fast）——注释里已有。

这条我会写进 `DEVIATIONS.md`（下一步一并提交）。

## 五、§4.2 —— 已采纳

`entry.url` 缺失时**如实报**「catalog entry has no url（cannot locate the asset）」，删掉了猜
文件名的 fallback（`modelica-standard-library.zip` 是编的）。有专门的测试钉住。

## 六、请复钓

D12 修好后，「有 omc 引擎」分支的**成功路径**终于可验（你 096 §2 已用权威用法证明 MSL 真能装
——`vfs_load_zip → 4376 文件 / loadModel=true / "4.1.0" / 反向 false`，6 PASS）。
请线上重打该分支：`omc_load_msl` 现在应当在**真装成功后返回 `isError: false`** 且
`selfCheck` 三条全绿。
