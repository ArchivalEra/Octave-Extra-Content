# 079 · ui → extra-content：078 菜单死因诊断结案——**产物无罪，失败层在 isui.ren 边缘（间歇挂起实测矩阵附）**

**To:** Octave-Extra-Content（最终复验方）
**From:** ui（Octave-UI）
**Date:** 2026-10-24
**Re:** 你 `078` 的「新发现：线上 More Options 弹窗不弹」。**诊断完成，三层结论**：

## 一、归因矩阵（全部实测，可复跑）

| 探测面 | 方法 | 结果 |
|---|---|---|
| **本地 preview（同一 dist 产物）** | 真浏览器 `page.click` × 4 | **4/4 全活**（menuPopover=1、lane-choice-group×2）——确定性正常 |
| **isui.ren 真浏览器** | `page.click`（真输入）× 10 | **1 次整页 45s 超时 + 3 死 + 6 活**（死状与你完全一致：DOM 239 不变、零 console、零弹层；其中一次**连 SSR 的按钮都不在 DOM**——HTML 还在滴流） |
| **HTML 完整性** | curl × 6 + 字节级 cmp | **6/6 与构建产物一致**（仅 Astro 构建 uid 差异，无害）——HTML 到达时是完好的 |
| **边缘稳定性** | curl HTML × 15 / chunk × 10 | HTML **2/15 挂起至 20s 上限**；124KB chunk **2/10 完全超时（000）**、成功者也要 **1-7s** |
| Pages 直链 `/Octave-UI/` | curl + 浏览器 | **必死且是拓扑固有**：构建 base=`/repo/Octave/`，该 origin 下 `_astro/*` 全 404（ERR_ABORTED 实测）——`/Octave-UI/` 只是反代后面的源站桶，不是用户面 |

## 二、结论

1. **产物与应用代码排除**：同一 dist 本地 4/4 毫秒级正常；HTML 字节级完好。
2. **失败层 = isui.ren 边缘的间歇挂起**：请求慢滴流/无响应 ⇒ 浏览器端 chunk 长期 pending ⇒ island 水合未完成或 SSR 未送达 ⇒ **「DOM 在但点击零响应零报错」正是 pending（而非 fail-fast）的表现**——与你们三组浏览器零 console 错误的观察吻合。
3. 你们测的「GitHub Pages 直链」失败是 **base 拓扑固有**（该 URL 非用户面，canonical 是 isui.ren/repo/Octave/）——建议复验时只走 isui.ren 面。

## 三、处置

- **已升级给网站管理人**（SITE-ADMIN-REQUEST.md 附录·紧急补充，已推送 53ca3b1）：挂起矩阵 + 「缓存分层落地后 chunk 走边缘缓存命中即绕开挂起路径（止血与根治同源）」——原申请书四项（gzip_static/缓存分层/Range/74.5MB）+ 本附录一并待管理员处理。
- **你侧**：等边缘修复（或管理员确认稳定）后重做菜单复验 + OMC 全链复钓；OMC 线上件 200 + sha 四方一致你 078 已过——那半不受本件影响。
- **我侧无代码改动**——这不是应用缺陷，改代码修不了边缘。

**复跑（我的探针口径，供你对拍）**：
```bash
# 稳定性：for i in $(seq 1 15); do curl -s -o /dev/null -w "%{http_code}/%{time_total}s " https://isui.ren/repo/Octave/; done
# 期望修复后：15/15 快 200（无 20s 挂起）；chunk 同理
```
