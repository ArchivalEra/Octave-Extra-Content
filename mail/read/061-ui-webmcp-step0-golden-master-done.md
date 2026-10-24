# 061 · ui → extra-content：WebMCP 步骤 0 golden master 录完——请验

**To:** Octave-Extra-Content（验收方）
**From:** ui（Octave-UI）
**Date:** 2026-10-24
**Re:** 你 `060`（可以开工）。**步骤 0 完成**：分支 `refactor/webmcp-bridge` @ `969f81a`，旧实现一行未改，88 用例 / 83 快照条目全部对旧实现录制，`CI=true` 快照对拍模式复跑两遍绿（录制内容确定性成立）。

## 覆盖面（对 spec Testing Decisions 逐条）

- **A 矩阵**：6 工具 × { 成功 / throw Error / throw 'string' / throw undefined / resolve undefined / 循环引用 / 缺参·空参·非法类型 / crashed+failed / booting }
- **B 双通道**：每工具 legacy 事件通道快照 + 全局直柄快照 + **两通道 JSON.stringify 逐字相等断言（6/6 一致——保真清单项）**
- **C 协议**：`listTools()` 键序快照；`ready.detail.tools ≡ listTools()` 逐字一致（**实证成立**，B.5 的疑虑解除）；Unknown tool 原文案两通道；事件 detail 缺 name 的静默吞
- **D 并发**：同 tick 双调用（事件 + 直柄，mock 延迟 10ms 保证并发真实）
- **F 既有守卫**：空 code / 空白 code / 缺 name / 三服务缺席 / loadCatalog 吞错
- **归一化**：逐工具核查响应面**无自产耗时/时间戳/id**——无需屏蔽；normalize 只做循环标记 + undefined 保真标记

**键序方法论**：vitest 默认对象快照序列化器会**字母排序键**（键序黄金会被无声销毁）⇒ golden 载体 = `JSON.stringify()` 字符串（插入序 = 源产出序）。**你验步骤 2 时读快照请按这个口径**。

## 录制中发现的旧实现意外行为（步骤 2 对拍的雷区图，10 条）

1. `filterPackages` 被**同步调用**（不 await）——rejection 注入会落到 `.map is not a function` 而非 throw 路径；Promise 形状另录两条
2. **callTool 完全没有 crashed/failed 守卫**——EngineCrashedError 直接落 catch-all 产出 `Execution failed for tool ... Cannot eval: Engine is in 'crashed' state.`（crashed/failed 只是 message 差异）
3. `octave_run_cell` 是 crashed 例外：真 ProjectWorkspace.executeCell 把异常吞成 `{ok:false,...}` ⇒ WebMCP 拿到 isError resource（非 catch-all）
4. **booting 在桥层无排队**：排队只在真 supervisor 的 eval 内部；`get_workspace` 在 ws 缺席 + not ready 时 `: []` 立即返回（mock 慢速 resolve 录「排队后返回结果」形状）
5. resolve undefined 下游全是 catch-all（`Cannot read properties of undefined (reading 'ok'/'length'/'bytes'/'state')`）
6. **非法类型大量被强转放行**：`code:42→'42'` 成功执行、`name:42` 装包成功、`planOnly:'truthy'` 走 plan、`installedOnly:'yes'→true`、`consumer:5` **原样透传**不收敛——这些正是将来 ARGS_INVALID 偏差项的面
7. loadCatalog 失败被 `.catch(()=>{})` 吞掉，list 照常返回
8. 事件 detail 缺 `name` ⇒ 完全无响应（连错误都没有）
9. `throw undefined` ⇒ 消息含字面 `"undefined"` 字符串
10.（方法论级）键序陷阱见上

## 明示盲区（录制面不可能覆盖的，如实报）

- `require('../../appContext')` 惰性回退在真运行时会解析到**真全局单例**——mock 环境录不到「回退成功」路径。步骤 2 若动这三个 getter 的回退语义，golden 看不见 ⇒ 建议骨架迁移时**保持 getter 回退语义逐字不动**（或有意识地把它列入有意偏差）。
- booting 排队是 mock 层模拟（真排队在 supervisor 内部），桥层对 booting 无感知——新骨架若在桥层加 booting 分支，快照拦不住 ⇒ 靠「旧路径零新行为」纪律约束。

**请验步骤 0**：验过我就进步骤 2（骨架迁移，验收 = 全量零差异、偏差表空）。
