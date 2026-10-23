# Spec：WebMCP 网桥重构（Claude 审阅修正版——A 为骨 + C 深模块半 + B 两样）

## Problem Statement

WebMCP 网桥（外部 AI agent 经页面事件协议/全局直柄调用引擎与 UI 能力的模块）是一个 500 行单类塞四概念（服务定位器/工具名册/工具分发/双通道挂载）的形状：加一个工具动三处、协议无类型、服务定位不可注入。外部审阅（Claude）对三案（A 工具表/B 工具总线/C 一门一走廊）给出修正主张：**A 为骨、C 只取深模块半、B 只取两样（动态生命周期、通道命名），其余按触发条件延后**——并指出两条三案共同盲区（WebMCP 浏览器标准真实存在、执行模型）与五条共同漏项。本 spec 把修正主张 + 三问实证答案落成可执行方案。

## Solution

把网桥重构为「工具表 + 分发机」骨架（A），配 Claude 修正五件（deps 类型绑死/失败信封取代哨兵/名册=可用性投影/可观测 hook/子集校验）；`octave_eval` 作为深实现工具独立文件（C 的深模块半，接口不对称不进核心）；通道层三 adapter 命名（legacy 事件/全局句柄/原生 modelContext 探测）配 Disposable 生命周期（B 的两样）。行为对旧实现**逐字等价**（golden master 钉死）。

## User Stories

1. As an 外部 AI agent, I want 用现有的页面事件协议调用全部工具, so that 重构对我零迁移成本。
2. As an 外部 AI agent, I want 用全局直柄调用工具（含 eval 快捷方式）, so that 页内调用免事件仪式。
3. As an 外部 AI agent, I want 工具列表反映当前真实可用性（不可用的明示或诚实缺席）, so that 我不会调到静默失败的工具。
4. As an 外部 AI agent, I want 参数校验错误带精确字段消息, so that 我能自纠错重试。
5. As an 外部 AI agent, I want 调用挂起时收到 isError 信封而非无限等待, so that 我的流程不悬挂。
6. As an 工具维护者, I want 加一个新工具只动一处（表里加对象+同目录测试）, so that 无须触碰分发/协议/装配代码。
7. As an 工具维护者, I want 写错依赖名在编译期报错, so that 依赖漂移不可能进运行期。
8. As an 工具维护者, I want 不启动真引擎测试工具逻辑, so that 测试快且不需要完整应用。
9. As an 架构维护者, I want 网桥目录零 import 具体服务, so that 服务依赖全部显式注入可审计。
10. As an 架构维护者, I want 协议形状冻结在单一文件且有快照测试, so that agent 侧契约不漂移。
11. As an 架构维护者, I want 每次调用有 no-op 默认的观测 hook, so that 流量分布（90% 赌注）有可证伪数据。
12. As an 架构维护者, I want 未来第二引擎的工具族按窄视图加前缀自然生长, so that 不需要预建 pack 机制。
13. As an 架构维护者, I want 未来接入原生 modelContext 标准时只加一个通道 adapter, so that 标准漂移被隔离在 wire 层。
14. As an 架构维护者, I want 工具注册带 Disposable 生命周期（与标准 signal 形状对齐）, so that 动态工具集有承接机制。
15. As an 架构维护者, I want「能否被 eval 表达」成为新工具的剪枝审查判据, so that 工具面不无谓生长。

## Implementation Decisions

（Claude 审阅意见全文采纳 + 三问实证答案——实证细节见 Further Notes）

1. **骨 = A 骨架**：数据表（工具对象：name/description/params schema/deps/run）+ 纯函数分发机（零领域 import）+ 协议壳 + 插件壳工厂。名册与分发是表的派生（fold）。
2. **Claude 修正五件全采纳**：① `defineTool<D extends keyof Ctx>`——deps 与 run 的 ctx 类型绑死（`Pick<Ctx, D>`），消灭「类型化 locator」漂移面；② `fail()`/`ToolError` 取代 `{isError:true}` 哨兵——成功值保留类型；③ 子集校验（type/enum/required/items，30-50 行自写不引 ajv）带精确字段消息——调用方是 LLM，ARGS_INVALID 消息是它自纠错的关键；④ **名册 = 表在当前可用性下的投影**（不是静态 fold）——`list()` 过滤不可用工具，可用性变化触发 ready 重发（legacy 通道）；⑤ 可观测 hook `onCall(name, ok, ms)` 默认 no-op。
3. **可用性是一等值**（Claude 共同漏项 2）：`absent / booting / ready / crashed + reason` 四态同时服务 call 门禁（不可用时 fail loud 信封）、roster 过滤、ready 重发。数据源 = 引擎 supervisor 的 state（**实证：supervisor.eval 已有 crashed/failed fail-loud 守卫 + 完整 Kill Ladder 挂起决议——可用性透传即可，不在 machine 重建执行模型**）。
4. **执行模型不重建**（三问 Q1 实证）：supervisor 层已有串行队列（`_enqueueTask`——并发 call 天然排队、无撕裂）、crashed/failed 守卫（fail loud）、Kill Ladder（死循环挂起→abort→pending 决议）；webmcp 的 catch-all 把决议后的错误转 isError 信封——**agent 端 response 不悬挂已闭环**。machine 只补：调用超时（防 queue 前面任务永久占位）+ 透传 state。
5. **C 的深模块半**：`octave_eval` 独立文件、深实现（可用性守卫上提为通用门 + 输出规范化 + 工作区同步）——但**在表里仍只是一行**，接口不对称不进核心；`.eval()` 快捷方式只挂在全局直柄（legacy 门面本来要保留）。恒等式测试钉死 `eval(code) ≡ callTool('octave_eval', {code})` + 删表行必红。
6. **B 取两样**：① Disposable 生命周期（mount 返回注销函数，与标准 AbortSignal 形状对齐）；② 通道层三 adapter 命名——legacy 页面事件（改名「页面事件协议（legacy）」防与 W3C WebMCP 标准撞名）/ 全局直柄 / 原生 modelContext（`document.modelContext ?? navigator.modelContext` 探测，标准稳定前默认不开）。**不取** pack mount/Port 注册表/名字空间机器。
7. **第二引擎生长路径**（三问 Q2 裁定）：omc 工具先按自己的窄视图加 `omc_` 前缀长进表（**懒加载语义：总是列出 + 调用时驱动 + 不可得时诚实报 CAPABILITY_UNAVAILABLE**——roster 是可调用性上界非保证，明文进不变量）；EvalPort 等两族都落地、真出现两个生产 adapter 时才抽象（不在一个例子上预猜泛化——Claude 意见采纳）。
8. **第四形状的裁决**（三问 Q3 实证）：6 工具逐个判定——5 个是「eval 表达不了（UI/服务态）或不该表达（装包有下载/磁盘效应）」的结构化工具，**消灭工具形状对本仓不成立**；但「能否 eval 一行表达」永久保留为新工具剪枝审查判据。
9. **effects 字段预留**（Claude 共同漏项 4）：表项带 `effects: 'readonly' | 'workspace' | 'sandbox-escape'` 元数据（eval 沙箱内=readonly；装包=sandbox-escape 正例）——不建权限机制，先让标注在。
10. **协议文档改名**：仓内文档与代码注释统一称「页面事件协议（legacy）」，WebMCP 一词保留给 W3C 标准语境。
11. **升级到 B 全案的触发条件**（明文）：出现「工具住别处」的贡献方模块；或引擎运行期自报能力导致工具集依赖运行时数据（过滤已不够用）。触发前不建 pack/registry。

## Testing Decisions

- **最高位 seam = 分发机的 handle()**：全部行为测试走 `handle({kind:'call'|'list'})` 直调（DOM-free、引擎-free——注入对象字面量 deps）。协议层单独快照测试（事件名/detail 形状/ready 单次/卸载干净）。
- **golden master 先行**（Claude 共同漏项 3——重构前对旧实现录制）：每工具 × 成功/失败/边界 × 两通道（legacy 事件 + 直柄）的 wire 响应字节级快照；「unknown → resource/json」的包装规则是最易漂移点，重点钉。
- 先行测试锚点（现 300 行插件测试）：断言面在 additive 接口下基本保形迁移（它已经在直调 callTool 注入 fake——正是本 seam 的既有消费者）。
- 反向断言必备（仓纪律）：空 code 必报/unknown tool 必报/不可用工具调用必报 CAPABILITY_UNAVAILABLE/删 octave_eval 表行必红（钉「门也在名册里」）/恒等式必过。
- onCall hook 测试：no-op 默认零影响 + 注入收集器可数调用。

## Out of Scope

- 原生 modelContext 标准通道的实现（只留探测 adapter 骨架 + 触发条件「标准稳定」）；
- pack/registry 升级（触发条件见决策 11）；
- EvalPort 双引擎共享抽象（两族落地后再看）；
- 权限机制（只留 effects 标注）；
- 现有两红的修复（Plots 接线/徽标态——已在另一条修复线单独跟踪，与本 spec 无关）；
- 修 bug 纪律不变：本 spec 实施方 = UI 仓（它修复、我复钓）；本仓只出方案与验收判据。

## Further Notes

**三问实证答案**（spec 决策的依据，全部源码级）：
- **Q1**：引擎页面主线程（非独立 worker）但 supervisor 有完整执行模型——eval 入 `_enqueueTask` 串行链（并发不撕裂）、crashed/failed fail-loud 守卫、Kill Ladder 挂起决议；webmcp catch-all 把决议错误转 isError 信封——response 不悬挂闭环。
- **Q2**：裁定懒加载语义（总是列出+调用驱动+诚实报不可用）——与宿主 forge-catalog 能力层语义同构；可用性模型因此进核心。
- **Q3**：6 工具中 5 个是结构化工具（run_cell=UI 状态/get_workspace=结构化读取不污染/list_packages=catalog 域/install=有效应/get_system_state=UI 八面）——第四形状对本仓不成立，剪枝判据保留。

**Claude 审阅的撤回与警示照单全收**：「协议 v2 = 假想」撤回（原生通道是真实第三通道）；平台工具生命周期是动态的（Disposable 同构）；平台在漂移必须隔离（wire 三 adapter）；命名撞车改口（页面事件协议 legacy）。
