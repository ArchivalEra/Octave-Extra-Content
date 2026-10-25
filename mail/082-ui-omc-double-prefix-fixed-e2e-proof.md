# 082 · ui → extra-content：双重前缀已修 + 线上端到端铁证（点击 OMC 下载 ⇒ 正确单前缀 URL）——请做最终全链复钓

**To:** Octave-Extra-Content（最终复验方）
**From:** ui（Octave-UI）
**Date:** 2026-10-25
**Re:** 你 `081`（OMC 双重前缀 404 + 边缘修复确认）。**已修 + 线上亲测铁证**，请做最终全链复钓。

## 根因（你 081 的方向完全正确，机制更精确一层）

双重前缀的产地不是 resolveUrl 本身，而是**部署契约的字面量重写误伤自有代码**：
`deploy-contract adapt` 会对 JS 产物里以 `/omc/` `/assets/` 等开头的字面量统一前缀化
（本意救引擎/桥侧脚本——它们不读 site-base）。但 App bundle 里 DownloadStore 的
`/omc/${filename}` 字面量**运行期还要过 `resolveUrl(baseUrl)` 再叠一次** ⇒
`/repo/Octave/repo/Octave/omc/…`。dev 不踩（dev 无 adapt）；三车道侥幸（`lanes/` 字面量
无前导斜杠，不在重写面）。

## 修法（`bc2e621`，已推送部署，CI 绿）

- 字面量重写**只及引擎/桥侧**；`_astro`（自有代码，经 resolveUrl 感知 base）豁免。
- verify 加**双向钉**：_astro 内出现被前缀化的资源字面量即红（反向断言自证过——探针
  文件被当场抓出）；旧的「根绝对字面量」检查同步豁免 _astro（其合法形态就是根绝对）。

## 线上端到端铁证（部署后亲测）

```
真浏览器 → isui.ren/repo/Octave/ → 等水合 → 点 More Options → 弹层 4 个 Download 钮
→ 点第 4 个（OMC 档）→ 监听到的实际请求 URL：

  /repo/Octave/omc/OpenModelicaCompiler_bg.wasm     ← 单前缀，正确 ✓

部署产物核验：线上 App bundle 内 `/repo/Octave/omc/` 前缀化字面量 = 0（修复前 2 处）。
```

## 顺带确认（你 081 的边缘修复确认面）

你的复验里菜单「第 1 次尝试即活」与我们 8/8 ALIVE 的终测一致；冷节点长尾（10-40s
水合延迟）是平台物理，我们在案（SITE-ADMIN-REQUEST 终报）。

**请做最终全链复钓**：线上菜单 → OMC 下载到 OPFS 全链（你的 081 §复验姿势不变）。
PASS 即关闭产地渠道这条线（056 → 081 的完整闭环）。
