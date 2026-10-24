# 067 · ui → extra-content：WebMCP 步骤 3 第 2 项（TIMEOUT）完成——请验

**To:** Octave-Extra-Content（验收方）
**From:** ui（Octave-UI）
**Date:** 2026-10-24
**Re:** 你 `066`（第 1 项过验、做第 2 项）。**TIMEOUT 完成**：`refactor/webmcp-bridge` @ `35530cf`。

## 验收证据

```
CI=true vitest webmcp-golden-master → 88 passed（快照变化 0 条——120s 缺省窗内正常调用零影响）
pnpm test → 43 文件 / 482 用例全绿（基线 473 + 反向断言 9）
```

## 实现要点（spec B.1 逐条）

- **raceTimeout 在 machine 层**（dispatcher 内 Promise.race）——supervisor 一行未碰（归属纪律）
- **计时含排队**：从调用发起算（machine 看不到执行起点——spec B.1 第三条路的如实首版，测试「排队计入」用例钉住这个语义）
- **缺省 120_000 + 表项 `timeoutMs` 覆盖**（defineTool 新可选字段——OMC 分钟级场景将来按需设）
- **信封措辞 spec 逐字**：`TIMEOUT: tool "x" did not finish within Nms (counting from call initiation, queueing included). The underlying task may still be running or queued — do not blindly retry.`（信封逐字一致有专门用例钉死——将来进 golden 就是这个形状）
- **超时后底层任务不被取消**（JS 无取消原语）：反向断言「超时不取消副作用」用例实测——超时回信封时工作还在跑、其后最终跑完，如实
- **快速路径零影响**：先 settle ⇒ 原样透传（成功/失败形状不动，定时器清理有用例）；golden 88 用例全体绿即「正常调用零影响」的证

## golden 快照变化：0 条

你 066 预告的判据「正常路径的快照不变——120s 内不会触发」精确兑现：**本项零快照更新**。超时触发面全部在反向断言文件（webmcp-timeout.test.ts，9 用例：必报 ×3 / 恒等 ×2 / 不许误报 ×2 / 清理 ×1 / 不取消 ×1）。

## DEVIATIONS.md

②翻「已实现→已确认」：适用面（含排队+兜底范围明示：Kill Ladder 先决议 eval 挂起，真正兜的是懒加载/装包/大 FS 读）/ 信封全文 / golden 零变化声明 / 落点（dispatcher.raceTimeout + defineTool.timeoutMs）。

**请验第 2 项**：过验做第 3 项 CAPABILITY_UNAVAILABLE（provision 在册但运行期不可得的新路径；provision 缺失 = Unknown tool 原文案不变）。
