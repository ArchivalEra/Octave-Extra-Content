# WebMCP 网桥模块重构 · 方案书（三案全录，待外部审）

**性质**：设计方案书（非 spec）——供外部审阅出修正意见，修正版回来后再落实。
**日期**：2026-10-23
**匿名口径**：内容可涉及 Octave 相关（产品本性需要），**不出现项目地址/仓库名/内部路径**——审阅方只需知道这是一个「浏览器里跑 Octave 的纯客户端应用」。

---

## 0. 背景与问题空间

一个纯客户端 Web 应用（Octave 跑在 WebAssembly 里）有一个 **WebMCP 网桥模块**：把引擎/笔记本/工作区/包货架的能力以「工具」形式暴露给外部 AI agent（agent 经页面级 CustomEvent 协议或全局对象直柄调用）。

现状：**一个 500 行的类塞了四个概念**——
1. **服务定位器**：三个具体服务（引擎执行/工作区/货架）经全局惰性解析（`require(context)` 兜底——ESM 里的隐患形状）；
2. **工具名册**：6+ 工具的 JSON Schema 字面量硬编码在方法体内；
3. **工具分发**：`callTool(name, args)` 的 switch/if 派发，数百行 handler；
4. **双通道挂载**：DOM CustomEvent 协议（call/response/ready/unloaded 四事件）+ 全局对象直柄——外部 agent 的事实契约（事件名与 detail 形状冻结，仓内零消费者）。

**病根**（准确定位）：
- 加一个工具要动三个概念的位置（名册字面量/switch case/可能新增服务 getter）——且写在同一个类里；
- 协议无类型——detail 形状散在字符串里，agent 侧与仓内各猜各的；
- 服务定位不可注入——handler 逻辑只有连着真引擎才碰得到（测试要起整个应用）。

**约束**（任何方案必须满足）：
- CustomEvent 协议是**事实契约**——外部 agent 已在用，重构不可破坏（或给迁移期）；
- 工具面**会生长**（eval/workspace/packages 已有；未来：文件系统/图形/引擎状态/第二引擎的工具族）；
- 三个服务依赖是**真 seam 的消费者**（各自已有多消费者）；
- 测试约束（写进需求）：工具逻辑要能**不启真引擎**地测（现状已有 300 行插件测试——第二消费者真实存在）。

**核心度量**：任何方案都回答——「加一个工具动几处？」「90% 流量（agent 发 eval 拿结果）走多少仪式？」「第二引擎的工具族怎么长进来？」

---

## 方案 A：「工具表 + 单分发机」（tools-as-data）

**一句话**：四概念从命令式代码**降维成一张数据表 + 一个纯函数分发机 + 一片可删除的协议壳**——工具不再是代码路径，是数据对象；名册和分发都变成对表的 fold（派生属性，不是要写的东西）。

### Interface（3 入口）

```
入口 1  createWebmcpPlugin(deps)        注册侧（deps 可为 thunk——惰性取，破初始化环，替代 require 兜底）
入口 2  plugin.handle(request)          程序化/测试侧（永不 reject——一切失败是值）
入口 3  wire 事件 + 全局直柄门面        agent 侧（协议形状冻结）
```

```typescript
// 通用分发机（零领域 import）
export interface McpTool<Ctx, Args> {
  name: string;                       // 全表唯一（构造期查重，接线期响亮失败）
  description: string;
  parameters: JsonSchema;             // 单一来源：wire 名册即此表的 fold
  deps?: readonly (keyof Ctx & string)[];   // 能力门；写错 key 编译期红
  run(args: Args, ctx: Ctx): Promise<ToolOutput> | ToolOutput;
}
export type ToolOutput =
  | unknown                                // 成功：string→text；其余→resource/json（包装是 machine 的事）
  | { isError: true; text?: string };      // 失败逃生舱

export function createServer<Ctx>(
  tools: readonly McpTool<Ctx>[],
  resolveCtx: () => Ctx,                   // 惰性 thunk
): { handle(req: McpRequest): Promise<McpResponse> }   // 永不 reject
```

- **文件布局**（6 文件全是 locality 分区非 seam）：protocol（wire 类型冻结）/machine（通用零领域 import）/deps（结构化窄视图纯类型）/tools（**唯一领域知识所在**：工具对象表）/wire（CustomEvent 挂载）/plugin（壳+工厂+迁移期门面）。
- **不变量**：handle 全函数（永不 reject）/id 回显/单一名册来源（ready 的 tools ≡ list() ≡ 表 fold——三者结构性不可能漂移）/构造期查重/init 幂等。
- **错误模式 1 处生成、文案逐字保真**（含「Unknown tool name…」例文冻结——agent 侧零感知）；handler 不再手排文案。
- **依赖策略**：窄视图是**结构化类型**——三个真服务类编译期自动满足，**手写 adapter 数 = 0**（adapter 即类型系统）；测试伪造=对象字面量。
- **seam 判定**：machine↔tools **非 seam**（同生共死一个模块，文件分开是 locality）；server↔wire **真**（生产桥+测试面两消费者——诚实脚注：若无测试约束则是假想就不拆）；「一能力一接口」**拒绝**（纯 ceremony）；外部工具贡献**假想暂不建**（触发条件：第一个「工具住别处」的模块出现）。
- **加工具成本：1 处**（表里加对象——deps key 编译期校验、schema 单一来源、machine/wire/plugin/protocol 四文件零改动）。

### Trade-offs（明码标价）
1. 校验是 required-only 浅校验（与现状持平，非退步——现状也不校验 enum）；
2. 结构化 seam 是编译期的——运行期热换服务做不到（无此需求，不买单）；
3. `{isError:true}` 逃生舱有轻微歧义（数据对象恰带此字段会被误读）——文档化；
4. 全局直柄门面是**永久兼容税**（~8 行）——仓内零消费者无法观测外部迁移动态；
5. 每工具的领域逻辑仍是手写（删的是 plumbing 不是领域——别指望 6 工具变 6 行）；
6. 新服务面 = 接口变更（deps 加字段，编译器引导但确是接口动）；
7. 名册静态（构造期冻结）——与静态交付形态匹配，动态工具是新需求届时再议。

---

## 方案 B：「工具总线」（依赖方向倒转）

**一句话**：网桥模块**谁也不认识**——工具住在它们自己的域目录里、服务藏在 Port 后面、通道是可数的 adapter；依赖方向从「工具模块硬 import 三个具体服务」倒过来。

### 形状

```
agent ⇄ CustomEventChannel ┐
agent ⇄ GlobalHandleChannel ├─ ToolBus{mount/call/list} ⇄ ToolPack ⇄ Port ← Adapter ← 真服务
仓内   ⇄ bus 直柄          ┘        （工具住自己域）      （注入）    （住服务旁边）
```

```typescript
// Port = 窄能力接口 + 稳定 id；工具 pack 声明需要什么，组合根提供实现
export const octaveEvalPort = definePort<EvalApi>('engine.eval:octave');
export const omcEvalPort    = definePort<EvalApi>('engine.eval:omc');   // 双引擎：同接口两 id

export interface ToolModule {
  readonly name: string;               // 前缀约定 octave_*/omc_*
  readonly description: string;
  readonly params: JsonSchema;
  readonly requires?: PortRecord;      // 硬依赖：mount 时查，缺 ⇒ 启动期 throw
  execute(deps, args): Promise<ToolCallResult>;
}
export interface ToolPack {
  readonly id: string;                 // 'octave-core' | 'notebook' | 'shelf' | 'omc'
  readonly tools: readonly ToolModule[];
}
export interface ToolRegistry { mount(pack: ToolPack): Disposable; bus(): ToolBus; }
export interface ToolChannel { attach(bus: ToolBus, env): Disposable; }   // env 注入不全局探测
```

- **不变量**：bus.callTool 永不 reject（envelope 错误码 TOOL_NOT_FOUND/ARGS_INVALID/CAPABILITY_UNAVAILABLE）/roster 即真相（list 出的必可 call，反之必 TOOL_NOT_FOUND）/硬依赖 mount 查启动期 throw·软依赖调用期诚实报 CAPABILITY_UNAVAILABLE **不编默认值**/wire 冻结快照测试/网桥目录**零 import 仓内服务**（lint 可查）。
- **加工具成本：1 新文件（工具住自己域）+ 1 行 pack index + 1 测试文件，总线零改动**——且自带 `mountTool` 测试挂载助手。
- **第二引擎的形状**：omc = mount 一个 pack（`engine.eval:octave` 与 `engine.eval:omc` 共享接口、各自 adapter——**多引擎工具注册是 mount 的副作用不是新机制**）；挂载成功 ⇒ roster 变化 ⇒ 通道重发 ready（全量快照语义），agent 自然看到 omc_* 工具。
- **seam 真假对账**：Channel **真**（现状本就双通道只是没被命名）；Port **真**（服务+测试 fake 两 adapter）；Pack mounting **真**（day one 即 4 pack）；协议 v2/WebSocket/联邦 registry **假想**（留门缝不预建）；名字空间机器**否决**（平坦名+前缀约定+mount 冲突检查够用）。
- **capability map = 穿礼服的 service locator**——三条纪律看守（Port 必须窄/依赖必须声明/mount 必查），缺一条就退化回汤。

### Trade-offs（诚实清单 8 条）
1. **概念数 1 涨到 7**——工具面永不生长则是纯开销；适用判据：生长/第二引擎/仓内第二消费方**三者有一即回本**，三者全无别用；
2. capability map 的 locator 本性（上条）；
3. 每个新概念都是新误用面（pack 忘 mount/通道忘 attach），靠单一组合根收口——但收口处本身成新关键路径；
4. 兼容风险换住处不消失（roster 变化重发 ready 对缓存工具表的 agent 是新语义）；
5. 调用链变长（pack→Port→adapter→服务四层文件，debug 多翻两个）；
6. defineTool 的类型体操可能报错难读；
7. 平坦名全局唯一在 pack 多后是协调点（前缀缓解不机器强制）；
8. 测试面变宽本身是新增维护量（四类测试）。

---

## 方案 C：「一门一走廊」（caller-first，流量直方图进接口）

**一句话**：`eval(code)` 是**门**（一等方法、深实现、直连端口）；其余工具是**走廊**（表驱动通用路径）；不对称是设计本身——把 REPL 产品本性（eval 就是使用方式）固化进接口形状。

### Interface

```typescript
export interface WebMcp {
  /** 90% 流量。字符串进、结果信封出。
   *  恒等式：eval(code) ≡ callTool('octave_eval', { code }) —— 一条测试钉死 */
  eval(code: string): Promise<WebMcpToolCallResult>;
  listTools(): Promise<WebMcpToolDefinition[]>;
  callTool(name: string, args?): Promise<WebMcpToolCallResult>;   // 通用逃生舱
}
// 三端口（结构化窄接口）：EvalPort（含 state 降级信号）/ WorkspacePort / PackagesPort
```

- **默认路径零仪式的记账**：无工具名字符串、无参数盒、无 id 配对、无监听器生命周期、无 schema 知识。agent 页内世界用 `全局对象.eval()` 直柄（**升格已有的第二通道**，不是新增协议事件——省 30 token 抵不过协议面翻倍）。
- **eval 深路径全在门后**：boot 态守卫（crashed/failed → isError 信封，fail loud 不挂起）→ evalPort.eval → 输出规范化（错误文案逐字保真）→ 工作区同步。深度余量只留位不预建（流式输出/协作式中断/结构化通道——将来都只动门后）。
- **恒等式钉不变量**：`eval(code) ≡ callTool('octave_eval',{code})` 一条测试 + **删表行必红**（钉死「门也在名册里」）。
- **加工具成本：1 处（=方案 A）**——走廊工具卡片加 tools.ts。
- **组合根装配**：三个服务全在 scope 构造注入——服务定位器与 import 环一起消失，环降为单向。
- **seam 判定**：WebMcp 接口**真**（3 消费者 2 传输 adapter——现状本就双通道挂载）；三端口**真**（依据是「不启真引擎可测」这条写进约束的需求，非趣味——若无此约束它们就是穿礼服的 locator）；tools 表↔server 非 seam；WebSocket/pack 外住**假想**门缝留。

### Trade-offs（为默认场景牺牲了什么）
1. **不对称税**（最大赌注）：流量分布漂移 → 走廊工具升门 = 接口变更+门面兼容——A/B 的对称性在此免费，C 付费；押 REPL 性产品 eval 为主是产品本性非猜测，**但这是赌要这么说**；
2. **eval 双处留名**（名册卡片在 tools、实现在 server）——靠恒等式+反向测试钉；
3. 门面兼容税（直柄上旧名与 eval 并存——两个名字指一事的漂移成本）；
4. **走廊工具永远二等**（无专属方法无深路径余量；要深行为要么局部复杂要么升门）；B 在这免费；
5. 新服务面 = 端口变更（编译期红是特性，但比 B 的 mount 一个 pack 贵）；
6. WorkspacePort 偏宽（8 个只读面——诚实记为已知宽度）；
7. 传输层天花板（页面级事件总线物理限制）C 不解决——那是 B 的卖点；C 的协议姿态是冻结+文档化判据。

---

## 三案对照终表

| 维度 | A 工具表+分发机 | B 工具总线 | C 一门一走廊 |
|---|---|---|---|
| 哲学 | 对称于数据 | 对称于位置（工具住自己域） | 不对称是设计（流量进接口） |
| 加一个工具 | **1 处（表加对象）** | 1 新文件+1 行 index+1 测试 | 1 处（=A） |
| 默认路径（90%） | 通用税（名+参数盒+分发） | 穿四层 | **一行零仪式** |
| 第二引擎工具族 | 接口变更 | **免费（mount 一个 pack）** | 接口变更（贵于 B） |
| 概念数 | 4 | 7 | 4 |
| 手写 adapter | **0（结构化类型）** | 2+/服务 | **0（结构化类型）** |
| 错误文案保真 | 1 处生成逐字冻结 | envelope 统一 | 门后规范化逐字保真 |
| 回本判据 | 工具多而均质 | 三者有一（生长/二引擎/二消费方） | 流量右偏稳定（REPL 本性） |

**共同前提修正**（实测发现）：插件测试已存在（300 行 ~30 断言含反向）——「零测试」的初始判断过期，三个方案共享这个事实修正（它使 server↔wire 的 seam 判定从假想变真）。

**三案共有的诚实边界**：都保留 wire 协议冻结（agent 侧零迁移）；都删 `require` 服务定位器；都接受「删的是 plumbing 不是领域逻辑」；都把「协议 v2 / WebSocket / 联邦」判为假想不预建。

---

## 附：审阅请求

请就以下问题给出意见（修正版将回炉后落实）：
1. 三案各自的适用判据在这个产品语境下的成立性（第二引擎工具族**已确定会来**——这该不该改变天平？）；
2. 各案 trade-off 清单里有没有被低估/漏记的代价；
3. 有没有第四种 radically different 的形状被三案共同盲区漏掉；
4. 若主张混合——请给出明确的骨/锋/演化路径结构及理由（**不要和稀泥式的全都要**）。
