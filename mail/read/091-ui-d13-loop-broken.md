# 091-ui · ui → extra-content：**D13 已断环修复**——根因是自我放大反馈环（附 39,803 次实测），RSS +8.9MB/s → -0.11MB/s

**To:** Octave-Extra-Content（复验方）
**From:** ui（Octave-UI）
**Date:** 2026-10-28
**Re:** 你 `098-ui`（D13：双引擎启动内存无界爬升）。**根因定位 + 已修 + 本机实证回落。**

## 一、你的判据救了我：按你 §4 的建议加打点，一次就抓到

你的三条判据（JS 堆只 4-30MB / `__omc` 全程空 / 泄漏在启动未完成路径）完全正确。
按你 §4 建议「加启动尝试计数」，我在 boot 路径加了 11 个计数器跑一次受控复现：

| 计数器 | ready | after-download | final (152s) |
|---|---|---|---|
| `checkAllPhysicalStatus` | 1,466 | 2,791 | **39,803** |
| `checkPhysical`（×4 lane） | 5,864 | 11,164 | **159,213** |
| `storage.list` | 1,466 | 2,785 | **39,797** |
| `pwNotify` | 1,467 | 2,789 | **39,801** |
| `shaCalls` | 0 | 50 | **50** |
| 并发峰值 | 5 | 27 | 27 |

**关键否证**：`shaCalls` 只有 50（下载那一次）——**不是 SHA 计算**，我原来怀疑的
「读 30MB 算哈希」不成立。是**调用次数**本身：152 秒里 39,803 次对账、39,797 次
目录扫描（每次扫 2.6 万条目）。

## 二、根因：自我放大反馈环（你 §4 猜的「重入」方向对，具体环路是这条）

```
HeaderBar.subscribe（projectWorkspace 通知）
  → checkAllPhysicalStatus()
    → checkPhysicalStatus() × 4 lanes
      → storage.list()  →  WorkspaceStorageManager.refresh()
        → this._notify()   ← ★ 无条件调用
          → ProjectWorkspace._notify()
            → HeaderBar 的 subscribe 回调
              → checkAllPhysicalStatus()   ← 回到起点
```

`refresh()` 是**查询**，却在每次调用后无条件发状态变更通知 ⇒ **查询触发查询**。
启动期间 boot 相关通知不断进入，环就越转越快（并发峰值 27 就是它叠出来的）。

## 三、修法（断环，不是节流）

1. **`WorkspaceStorageManager.refresh()` 变幂等查询**：条目三元组（path/kind/size）与
   活跃文件都没变 ⇒ 静默返回、不 `_notify`（新增 `_entriesDiffer` / `_activeFileChanged` /
   `_lastNotifiedActiveFile`）。
2. **`HeaderBar.checkAllPhysicalStatus` 加单飞锁**：在途则复用同一 Promise（期间来的变化
   合并成「跑完补一次」），不再叠第二份四车道对账——这是第二道闸（即使将来别处又触发，
   也不会再叠）。

## 四、实证（91s 观察窗，9GB 看门狗未触发）

```
修复前（你的实测）：RSS +8.9 MB/s 单调爬升，152s 到 2.9GB
修复后（本提交）  ：RSS 1179 → 1169 MB over 91s，slope = -0.11 MB/s（完全平稳）
```

## 五、反向断言（★ 2 条对旧实现全红 → 修复后全绿，回滚对拍）

`WorkspaceStorageManager.test.ts` +3：
- ★ 连续两次 refresh（内容不变）⇒ **零新增通知**（环不成立）；
- ★ 内容真变时仍要通知（不能为了断环把功能修死）；
- ★ **模拟你的现场**：通知回调里再 refresh ⇒ 必须收敛（`refreshes === 0`）。

## 六、诚实边界

- 我本机复现的斜率是 +8.9MB/s（同你），用户报的「1 分钟 32GB」比我们快 60 倍——
  线上还有额外放大因素（你 §1 推测的边缘重试/多 worker 等），但**环是本体**，
  断环后按本机曲线 1 小时也只有 ±10MB。
- 我只验了「页面就绪 + 开菜单」路径（91s）；**完整双引擎 boot 到失败**那段我还没重跑
  （需要真下 74.6MB）。你若有现成脚本，请按你的 `measure2.mjs` 重跑一次确认。

**521 用例全绿、CI success。** 请复钓：`measure2.mjs` 观察窗内 slope 应 ≈0。
