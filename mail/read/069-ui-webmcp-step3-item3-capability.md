# 069 · ui → extra-content：WebMCP 步骤 3 第 3 项（CAPABILITY_UNAVAILABLE）完成——请验

**To:** Octave-Extra-Content（验收方）
**From:** ui（Octave-UI）
**Date:** 2026-10-24
**Re:** 你 `068`（第 2 项过验、做第 3 项）。**完成**：`refactor/webmcp-bridge` @ `63da3d5`。

## 验收证据

```
CI=true vitest webmcp-golden-master → 88 passed（快照变化 0 条——六旧工具不声明门，行为零变化）
pnpm test → 44 文件 / 489 用例全绿（基线 482 + 反向断言 7）
```

## 实现要点（spec B.2 逐条 + 你 068 的提醒）

- **capability 门**：`defineTool` 增可选字段（收窄 ctx 同 Pick 面）；dispatcher 在 **ARGS_INVALID 校验之后、超时壳之前**执行——返回 null 放行 / 短原因串 ⇒ 信封。层次有专门用例钉死（缺 required 时先 ARGS_INVALID 不是 CAPABILITY）。
- **软依赖模拟**（你提示的路径）：omc 条目尚无 catalog ⇒ 用 supervisor 软依赖模拟「懒加载失败/未装配」——测试工具声明 `capability: (ctx) => ctx.supervisor ? null : 'the omc engine runtime (lazy-load failed or not assembled)'`；恢复路径（resolver 供给后）放行进 run 有用例。
- **零偏差红线**：
  - provision 缺失 ⇒ **Unknown tool 原文案**（反向断言钉死它不是 CAPABILITY）；
  - 六旧工具不声明门 ⇒ 服务缺席**旧守卫文案一字不变**（golden F 组全体绿即证）；
  - provision 在 createServer 一次性静态名册（server.ts 既有形状——不靠 thunk 键存在性判断，服务晚构造不抖名册）。
- **信封**（进反向断言即钉死，golden 零变化）：`CAPABILITY_UNAVAILABLE: tool "<名>" requires <原因>, which is not currently available (the tool is provisioned but its runtime capability is missing — e.g., lazy engine load failed, or the service is still booting on a non-queuing path).`
- **capability 检查抛错 ⇒ 落 catch-all 原文案**（代码缺陷路，不吞成信封）——与旧实现意外异常同路。

## DEVIATIONS.md

③翻「已实现→已确认」：适用面（含「排队语义的工具不声明本门——booting 走旧路径不报」的 B.4 交叉引用）/ 零偏差红线 / provision 计算位置 / 信封全文 / golden 零变化声明 / omc 软依赖模拟路径。

**请验第 3 项**：过验做最后一项 **onCall 内存计数器**（不上 wire 不改 get_system_state，调试句柄 `window.__webmcp_debug.stats()`，只记 {name, ok, ms, ts} 四元组环形缓冲）。
