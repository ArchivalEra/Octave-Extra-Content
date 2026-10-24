# Spec 定稿：WebMCP 网桥重构（三轮外部审终版——开工前钉 5 + 小项 4 全落）

## Problem Statement

WebMCP 网桥（外部 AI agent 经页面事件协议/全局直柄调用引擎与 UI 能力的模块）是一个 500 行单类塞四概念（服务定位器/工具名册/工具分发/双通道挂载）的形状。三轮外部审（三案设计 → 修正版 → 终版）后**通过可开工**，但开工步骤 0/1 前要先钉死 5 个实现级缺口（前两轮矛盾已收干净，剩余是落成实现细节时才暴露的——其中 1-3 会改动偏差表或 golden master）。本定稿把 5 缺口 + 4 小项全部落定。

## Solution

A 骨架（工具表 + 分发机 + deps 能力门）+ C 深模块半（eval 深实现但表里一行）+ B 两样（Disposable 仅通道/插件生命周期、三通道命名含 fake-channel 契约测试）。核心不变量：**provision/health 正交**（名册稳定/ready 单次）、**旧路径逐字透传**、**有意偏差表限定新行为**、**超时首版含排队且只兜不经 supervisor 的路径**。

## User Stories

1. As an 外部 AI agent, I want 用现有页面事件协议调用全部工具, so that 重构零迁移成本（golden master 在偏差表外零差异）。
2. As an 外部 AI agent, I want 用全局直柄调用工具（含 eval 快捷方式）, so that 页内调用免事件仪式。
3. As an 外部 AI agent, I want 工具列表稳定且反映本构建是否提供该能力（provision 静态）, so that 工具发现不因引擎健康态抖动。
4. As an 外部 AI agent, I want crashed/failed 时收到既有错误文案（原文逐字不变）、booting 时调用排队等引擎就绪后执行（旧行为不变）, so that 重构不改变我对引擎状态的理解模型。
5. As an 外部 AI agent, I want 参数明确违规（缺 required / 类型错 / enum 越界）时收到带字段名的 ARGS_INVALID, so that 我能自纠错；未知字段与可强转值被放行, so that 旧调用不被新校验误杀。
6. As an 外部 AI agent, I want 调用超时时信封明示「仍在排队或执行中，勿盲目重试」, so that 我不造成重复执行。
7. As an 工具维护者, I want 加一个新工具只动一处（表里加对象+同目录测试）, so that 无须触碰分发/协议/装配代码。
8. As an 工具维护者, I want 写错 dep key 或访问未声明 ctx 键在编译期报错, so that 依赖漂移不可能进运行期。
9. As an 工具维护者, I want 不启动真引擎测试工具逻辑, so that 测试快且不需要完整应用。
10. As an 架构维护者, I want 网桥目录零 import 具体服务且该规则有 lint/依赖检查钉住, so that 服务依赖全部显式注入可审计。
11. As an 架构维护者, I want 每次调用被内存计数器记录（环形缓冲，经调试句柄读取，不联网、不改已有工具输出）, so that 流量分布有真实数据。
12. As an 架构维护者, I want 新增 Channel 只需实现既有 Channel 接口（fake-channel 契约测试证明）, so that 原生标准稳定后可增量接入。
13. As an 架构维护者, I want 未来第二引擎工具按 provision 加前缀自然生长、EvalPort 待两族落地后再抽象, so that 不预猜泛化。
14. As a 贡献者, I want「新工具能否被 eval 一行表达」作为剪枝审查判据（写在贡献文档）, so that 工具面不无谓生长。

## Implementation Decisions

### A. 三轮审定的基础架构（不变，摘要重述）

- **A 骨架**：数据表（name/description/params schema/deps/run）+ 纯函数分发机（零领域 import）+ 协议壳 + 插件壳工厂。`defineTool<D extends keyof Ctx>` 绑死 deps 与 ctx（`Pick<Ctx, D>`）。
- **C 深模块半**：`octave_eval` 独立深实现文件（可用性守卫+输出规范化+工作区同步）但表里一行；`.eval()` 只挂全局直柄（legacy 门面）。
- **B 两样**：Disposable（仅通道 attach/卸载+插件生命周期）；三通道命名（legacy 事件/全局直柄/fake-channel 契约测试）。
- **provision / health 正交**：provision 静态决定名册、health 动态只影响调用结果且不进 list wire。
- **守卫优先级**：旧路径（6 个既有工具）遇 crashed/failed ⇒ supervisor 原文案逐字透传；`CAPABILITY_UNAVAILABLE` 只用于新路径（见 B.2）。
- **升级触发条件**：「工具住别处」的贡献方出现 / 引擎运行期自报能力导致工具集依赖运行时数据。触发前不建 pack/registry/工具级 dispose。

### B. 开工前钉的 5 缺口

#### B.1 超时计时（选第三条路：首版承认含排队）

- **首版采用**：承认计时**含排队时间**（machine 在 supervisor 之上看不到「开始执行」时刻），阈值定高，信封措辞改为「**仍在排队或执行中，勿盲目重试**」——精确覆盖「尚未开始」的情况。**不碰 supervisor**（实施仓归属纪律）。
- **默认阈值**：`120_000`（120 秒）——大于 Kill Ladder 最终决议阈值，只兜不经 supervisor 的慢路径。覆盖范围明示：eval 挂起由 Kill Ladder 先决议（超时几乎不触发）；**超时真正兜住的** = 懒加载引擎装载 / 装包下载 / UI 类工具读大量文件系统。
- **表项支持 `timeoutMs` 覆盖**——OMC 仿真分钟级场景将来按需设。
- **后续升级路径**（记入贡献文档但不本轮实现）：若将来需要「从开始执行计时」，走端口 adapter 暴露「已开始」回调（动 adapter 不动 supervisor）。
- 超时后底层任务仍在跑/排着——信封明示勿盲目重试（上条措辞已含）。

#### B.2 「provision 缺失」的返回值（消除自相矛盾）

- **未提供的工具不在名册**：调用它 ⇒ 返回**旧的 `Unknown tool name: "x". Use listTools() to see available tools.` 原文案**（旧路径，零偏差，golden master 覆盖）。
- **`CAPABILITY_UNAVAILABLE` 只用于**「已提供（provision 在册）但引擎/服务当前不可得」——如懒加载 omc 引擎装载失败、服务 boot 中且该工具不排队（如果排队则走旧路径不报）。
- **偏差表第 3 项改写**：`CAPABILITY_UNAVAILABLE` 的触发面从「provision 缺失或懒加载不可得」缩为「provision 在册但运行期不可得（懒加载失败/boot 中不排队路径）」。
- **反向断言改写**：删「provision 缺失调 CAPABILITY_UNAVAILABLE」，改为「调用未在名册中的工具返回 Unknown tool 原文案」。
- **provision 在哪算**：**装配根在 `createServer` 时一次性给定**（静态数组），**不能**靠 thunk 里 key 是否存在判断——否则服务晚构造时 provision 抖动。`resolveCtx` 的 thunk 只服务已 provision 工具的运行期依赖解析。

#### B.3 新增 wire 面：不上 wire

- **`effects` 只做表内元数据**，**不进 `list()` 返回也不进 `ready` 载荷**——它没有消费者；等第一个消费者（权限机制）出现再暴露上 wire。偏差表第 5 项据此**从偏差表删除**（因为不上 wire 就没有 wire 字节差异）。
- **onCall 计数器只走调试句柄**（如 `window.__webmcp_debug.stats()`），**不塞进 `octave_get_system_state` 的返回**——那是已有工具，改它的输出就是 golden master 偏差（偏差表没列，也不该列）。
- **计数器只记 `{name, ok, ms, ts}` 四元组**，**不记 args**（args 里是用户代码，隐私/体积双重理由）。

#### B.4 用户故事 4 改写（booting = 旧行为排队，非错误信封）

- **实证**（本轮补查）：supervisor 的 eval 守卫只拦 `crashed/failed`——**booting 时不拦、直接入 `_enqueueTask` 排队**，boot 完成后执行返回结果。
- **改写后**：crashed/failed ⇒ 原文案不变（零偏差）；**booting ⇒ 旧行为不变（排队等就绪再执行）**——不是新行为不进偏差表。步骤 0 对 booting 路径也录 golden master（实证旧行为是排队返回结果）。若旧实现在 booting 下长时间无响应，由超时兜底（B.1 措辞已覆盖）。

#### B.5 不变量测试与旧行为等价

- **步骤 0 对下列项也录旧实现行为**（不确定旧实现是否满足这些不变量）：
  - throw 非 Error（`throw 'string'`）/ throw undefined / run 返回 undefined / 返回不可序列化值（含循环引用对象）——各工具的 catch-all 输出形状。
  - `ready.detail.tools` 与 `listTools()` 返回的逐字一致性（含键序）。
  - 两条通道（legacy 事件 + 全局直柄）调用同一工具的响应一致性。
- **不一致的项进偏差表**（新行为是有意的 ⇒ 列入、确认、勾销），**一致的项留在保真清单**。不让新测试悄悄定义什么是「正确」。

### C. 小项 4

- **偏差表第 4 项（空 code 守卫不变）移入「保真清单」**——它是保真不是偏差。偏差表只列**有意新增的拒绝/错误码/wire 形状变化**。
- **Args 类型派生机制明示**：**用一个小 builder（同一段代码同时产出 JSON Schema 和 TS 类型）**——不引 json-schema-to-ts（外部依赖太重），不自写类型体操。builder 生成的 schema **与旧实现的 JSON Schema 字节一致（含键序）**，golden master 盯这一点。
- **步骤 2 验收收紧**：骨架迁移阶段（步骤 2）**全量零差异**（不是「偏差表外零差异」——步骤 2 还没加新行为，偏差表应该是空的）。偏差项的 golden 更新**只允许出现在步骤 3 对应的提交里**。
- **Out of Scope 里「#15」改称「同会话缓存盲区（上一轮复钓观察项）」**——避免与用户故事 14（原编号 15）撞号。

## Testing Decisions

- **最高位 seam = 分发机 `handle()`**：全部行为测试直调（DOM-free、引擎-free）。协议层归一化快照。
- **步骤 0 golden master 覆盖面**（对旧实现录制）：
  - 每工具 × { 成功 / 失败（含工具内异常 throw Error / throw 非 Error / throw undefined / 返回 undefined / 不可序列化值） / 边界（缺参 / 空参 / 非法类型 / crashed / booting）} × 两通道（legacy 事件 + 全局直柄）；
  - `ready.detail.tools ≡ listTools()`（含键序）逐字一致；
  - 「同一 tick 发两个 call」并发用例；
  - Unknown tool 原文案；
  - 归一化规则：比较前屏蔽耗时、关联 id、时间戳。
- **步骤 2 验收**：全量零差异（偏差表空）。步骤 3 每项一个提交，偏差表逐项从「未实现」→「已确认→已勾销」。
- **反向断言清单**（更新后）：空 code 必报 / unknown tool 返回原文案 / provision 在册但引擎不可得报 CAPABILITY_UNAVAILABLE / 删 octave_eval 表行必红 / 恒等式 `eval(code) ≡ callTool('octave_eval',{code})`。
- **类型层**：`@ts-expect-error` 两条（dep key 写错、访问未声明 ctx 键）。
- **网桥零 import 服务**：lint/依赖检查规则钉住。
- **fake-channel 契约测试**：假 Channel 实现 attach/detach/投递全过。
- **计数器测试**：只记四元组不记 args、环形缓冲覆盖、调试句柄可读。

## Out of Scope

- ready 重发 / 动态工具集（归升级触发条件）；
- 原生 modelContext 通道实现（fake-channel 契约测试替代骨架）；
- pack/registry/工具级 dispose（升级触发条件）；
- EvalPort 双引擎共享抽象（两族落地后再看）；
- 权限机制（effects 留表内元数据不上 wire，等消费者出现）；
- 两红修复（已验收完毕，独立线）；
- 同会话缓存盲区（上一轮复钓观察项——UI 已留痕、跨会话兜住；方向 size+mtime 或抽样哈希，不进本轮）。

## Further Notes

**三轮审定轨迹**：一轮三案（A 表/B 总线/C 门）→ 二轮修正（A 骨五修正+C 深模块半+B 两样 + provision/health 正交 + 守卫优先级 + 偏差表 + 超时闭合）→ **三轮钉 5**（超时首版含排队不碰 supervisor / provision 缺失返回 Unknown tool 原文案 / effects 与 onCall 不上 wire / booting 旧行为排队不改 / 不变量测试先录旧行为再定偏差）。

**本轮新实证两项**：① supervisor 的 eval 守卫只拦 crashed/failed，**booting 不拦直接入队**（B.4 依据）；② ready.detail.tools 与 listTools() 从同一 listTools 调用产生（:459 `void this.listTools().then(...)` 构造 ready 载荷）——结构上一致但键序与形状仍需步骤 0 快照确认（B.5 覆盖）。

**落实顺序**（三轮审定后不变，验收语义收紧）：
0. 单独提交：对**旧实现**录 golden master（含 B.5 补录项 + 并发用例 + booting 路径），全绿。
1. 偏差表定稿（本轮已定稿：ARGS_INVALID / TIMEOUT / CAPABILITY_UNAVAILABLE 三项，每项标注适用面）。
2. 骨架迁移——验收 = **全量零差异**（偏差表空、此步没有新行为）。
3. 在骨架上逐项加校验/超时/provision/计数器——每项一个提交，偏差表逐项勾销，golden 更新只在本步出现。
4. omc 到来时走升级路径（provision 在册+懒加载+CAPABILITY_UNAVAILABLE 新路径）。
