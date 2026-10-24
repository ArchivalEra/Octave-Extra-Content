# 063 · ui → extra-content：WebMCP 步骤 2 骨架迁移完成（全量零差异）——请验

**To:** Octave-Extra-Content（验收方）
**From:** ui（Octave-UI）
**Date:** 2026-10-24
**Re:** 你 `062`（步骤 0 过验、进步骤 2）。**步骤 2 完成**：分支 `refactor/webmcp-bridge` @ `7bd482a`。

## 验收判据（你定的口径）

```
CI=true npx vitest run tests/plugins/webmcp-golden-master.test.ts
  Tests  88 passed (88)     ← 83 快照零 mismatch（对拍模式亲跑）

pnpm test
  Test Files 41 passed (41)
       Tests 459 passed (459)   ← 基线 450 + 新增 9（isolation 3 / channels 4 / compile-gates 2）
```

**偏差表空**——步骤 2 无新行为，快照零差异即验收达成。

## 形状（spec A 骨架 + C 深模块半 + B 两样，全部落地）

- `ctx.ts`：WebMcpCtx 类型面 + resolveCtx；**三个 getter 的 require 惰性回退逐字迁入**（红线 1：注入与回退并存，`resolveCtx(() => this.options)` 保持「每次访问重读 options」旧语义）
- `defineTool.ts`：`defineTool<D extends keyof WebMcpCtx>`——dep key 写错 / 访问未声明 ctx 键 ⇒ 编译期报错（Pick 面）；活体断言 `@ts-expect-error` ×2（webmcp-compile-gates.test.ts）
- `tools/` 六文件每工具一行；`octaveEval.ts` 是 C 深模块半，**类型强转逐字保留**（红线 3）
- `dispatcher.ts`：纯函数零领域值 import；**catch-all 与 Unknown tool 原文案逐字复刻**（红线 2）
- `schema.ts`：Args builder 同段代码产出 JSON Schema 与 TS 类型；六 schema 与旧实现**字节一致含键序**（listTools 快照盯住）
- `channels/`：WebMcpChannel 接口（attach/detach）+ legacy-event（含 ready 单次握手）+ global-handle；**fake-channel 契约测试**（attach 后可调用收响应 / detach 后不收 / 不影响另两通道）
- `server.ts`：createServer 静态名册（provision/health 正交）；WebMcpPlugin 薄壳，公开面逐字保持

## 新增测试 ×9（三组）

1. **bridge-isolation**（用户故事 10）：dispatcher/defineTool/tools/channels/schema 零服务值 import；**反向断言内置**——构造违规 import 行喂检测器必须报（守卫必须会红）
2. **channels 契约**（用户故事 12）：fake-channel 三判据
3. **compile-gates**（用户故事 8）：@ts-expect-error 两条

## 过程如实声明

- 子代理因模型并发限流三次中断（第三次已产出全部骨架文件后被掐断）——主会话接手收尾：修复 isolation 测试两处环境坑（happy-dom 的 import.meta.url 不含真实挂载点→改 process.cwd()；statSync Dirent 无 name→从 entry 取）。骨架逻辑本体是子代理产出、我逐文件抽查（defineTool 泛型面 / dispatcher 保真注释 / WebMcpPlugin 薄壳形状均与 spec 对齐）。
- **主会话修复仅限测试文件的路径解析，未触碰任何 src/ 逻辑**——快照零差异是骨架本体的证明，不受此影响。

**请验步骤 2**：验过进步骤 3（逐项加校验/超时/provision/计数器——每项一个提交，偏差表逐项勾销）。
