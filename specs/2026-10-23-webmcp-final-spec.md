# Spec 终版：WebMCP 网桥重构（Claude 二轮复审吸收——必改 4 + 应改 6 全落）

## Problem Statement

WebMCP 网桥（外部 AI agent 经页面事件协议/全局直柄调用引擎与 UI 能力的模块）是一个 500 行单类塞四概念（服务定位器/工具名册/工具分发/双通道挂载）的形状：加一个工具动三处、协议无类型、服务定位不可注入。前两轮设计（三案 + 修正版）经外部二轮复审：**有条件通过**——采纳面忠实、三问实证站得住（Q1 执行模型担忧被 supervisor 既有队列消解、Q3 第四形状撤回、Q2「总是列出」使「名册=可用性投影」缩为「按 provision 过滤」），但落成 spec 后出现**四处内部矛盾（两处直接与「逐字等价」冲突）+ 六处应改**，落实前必须先定。本终版全部落定。

## Solution

A 骨架（工具表 + 分发机 + deps 能力门）+ C 深模块半（eval 深实现但表里一行）+ B 两样（Disposable 仅通道/插件生命周期、三通道命名含 fake-channel 契约测试替代原生骨架）。核心修订：**provision 与 health 正交拆分**（名册稳定、ready 单次）、**守卫优先级明文规则**（旧路径逐字透传、新错误码只用于新路径）、**有意偏差表**（golden master 在偏差表外零差异）、**超时语义闭合**（从开始执行计时、表项可覆盖、阈值大于 Kill Ladder 决议阈值、明示勿重试）。

## User Stories

1. As an 外部 AI agent, I want 用现有页面事件协议调用全部工具, so that 重构对我零迁移成本（golden master 在偏差表外零差异）。
2. As an 外部 AI agent, I want 用全局直柄调用工具（含 eval 快捷方式）, so that 页内调用免事件仪式。
3. As an 外部 AI agent, I want 工具列表稳定且反映本构建**是否提供**该能力（provision 静态）, so that 我的工具发现不会因引擎健康态抖动而变。
4. As an 外部 AI agent, I want 引擎崩溃/启动中时调用得到诚实的错误信封（原文案不变）, so that 我不误以为工具不存在。
5. As an 外部 AI agent, I want 参数明确违规（缺 required / 类型错 / enum 越界）时收到带字段名的 ARGS_INVALID, so that 我能自纠错重试；未知字段与可强转值被放行, so that 旧调用不被新校验误杀。
6. As an 外部 AI agent, I want 调用超时时收到信封明示「底层仍在执行，勿盲目重试」, so that 我不会造成重复执行。
7. As an 工具维护者, I want 加一个新工具只动一处（表里加对象+同目录测试）, so that 无须触碰分发/协议/装配代码。
8. As an 工具维护者, I want 写错 dep key 或访问未声明 ctx 键在编译期报错（`@ts-expect-error` 钉住）, so that 依赖漂移不可能进运行期。
9. As an 工具维护者, I want 不启动真引擎测试工具逻辑, so that 测试快且不需要完整应用。
10. As an 架构维护者, I want 网桥目录零 import 具体服务且该规则有 lint/依赖检查钉住, so that 服务依赖全部显式注入可审计。
11. As an 架构维护者, I want 协议形状冻结在单一文件且有快照测试（归一化后比较）, so that agent 侧契约不漂移。
12. As an 架构维护者, I want 每次调用被内存计数器记录（环形缓冲，经调试句柄或 get_system_state 读取，不联网）, so that 流量分布有真实数据而非空 hook。
13. As an 架构维护者, I want 新增 Channel 只需实现既有 Channel 接口（由 fake-channel 契约测试证明第三个 adapter 可加）, so that 原生 modelContext 标准稳定后可增量接入而不腐烂。
14. As an 架构维护者, I want 未来第二引擎工具按 provision 加前缀自然生长、EvalPort 待两族落地后再抽象, so that 不在一个例子上预猜泛化。
15. As a 贡献者, I want「新工具能否被 eval 一行表达」作为剪枝审查判据（写在贡献文档）, so that 工具面不无谓生长。

## Implementation Decisions

### 一、必改 1：provision / health 正交拆分（解决名册矛盾）

- **provision**（静态，决定进不进名册）：这个构建是否提供该能力。`list()` 按 provision 过滤；provision 集合在构建/装配期确定（omc 未配置 ⇒ 无 omc_* 工具；配置了 ⇒ 工具在册，即使引擎尚未装载）。
- **health**（动态，只影响调用结果）：`booting / ready / crashed / failed`——**直接映射 supervisor 的真实枚举，不另造 absent/ready 词汇**。health 不进 `list()` 的 wire 形状。
- **ready 保持单次**（旧 agent 一次性握手假设不被破坏）；**不做 ready 重发**。重发逻辑整体移出本 spec，归决策 11 的升级触发条件（引擎运行期自报能力导致工具集依赖运行时数据时）。
- health 可见性：agent 需要时经**现有 `octave_get_system_state`** 读（该工具本就返回引擎状态面），不动 list 的 wire。
- 懒加载语义（Q2 裁定保留）：omc 配置了但引擎未装载 ⇒ 工具在册，调用时驱动加载；加载不可得 ⇒ `CAPABILITY_UNAVAILABLE`（新路径专用码，见必改 2）。

### 二、必改 2：守卫优先级明文规则（解决 golden master 冲突）

- **旧路径逐字透传**：已有 6 工具遇 crashed/failed ⇒ 走 supervisor 既有守卫错误（`EngineCrashedError` 原文案）经 catch-all 转信封，**文案与形状逐字不变**（golden master 覆盖此路径）。
- **`CAPABILITY_UNAVAILABLE` 只用于新路径**：provision 缺失（工具不该被调）/ 懒加载引擎不可得。旧路径不产出此码。
- **通用门不前置拦截旧路径**：决策 5 的「守卫上提」限定为「新路径的前置检查」+「supervisor 已透传错误原样转发」，不改写既有错误文案。
- 状态枚举用 supervisor 真值（`booting/ready/crashed/failed`），不引入 absent。

### 三、必改 3：有意偏差表（解决「逐字等价」与新增行为互斥）

- **golden master 范围**：合法输入 + 既有错误路径（unknown tool / 缺参 / 服务不可用 / crashed / 工具内异常）**零差异**（归一化后比较）。
- **归一化规则**：比较前屏蔽耗时、关联 id、时间戳；「字节级」= 归一化后的序列化结果。
- **有意偏差表**（逐项确认，落实时逐项勾销）：
  1. `ARGS_INVALID`——新增拒绝（type/required/enum 明确违规），旧实现放行；
  2. `TIMEOUT`——新增（超时路径，旧实现无）；
  3. `CAPABILITY_UNAVAILABLE`——新增（provision/懒加载新路径）；
  4. 空 code 等既有守卫：**不变**（保真）；
  5. `effects` 字段：新增元数据（wire 上可见但旧 agent 可忽略——加进 optional 语义，快照测试单独记）。
- **校验器宽松**：放行未知字段、不做类型强转；只拒绝 type/required/enum 明确违规。**Args 的 TS 类型以 schema 为源派生**（不写两份真相）。

### 四、必改 4：超时语义闭合

- **计时从开始执行算起**（不是入队）——否则长任务拖垮后续调用（OMC 仿真分钟级）。
- 表项支持 `timeoutMs` 覆盖。
- **默认阈值 > Kill Ladder 最终决议阈值**——超时只作兜底，不抢 Kill Ladder 的活。
- 超时错误码与 supervisor 决议错误**可区分**（`TIMEOUT` vs `EngineCrashedError` 原文案）。
- 超时后底层仍在执行 ⇒ 信封明示「仍在执行，勿盲目重试」。
- **machine 不负责释放 supervisor 队列槽位**（那是 Kill Ladder 的职责）——文档写明边界。

### 五、应改项全采纳

- **effects 修正**：取值改为 `read | mutates-workspace | sandbox-escape`；**eval 归 `sandbox-escape`（保守）**——实测证据：宿主 pkg shim 使 eval 内的 `pkg install`/`pkg load` 直接触发 `OctaveAssets.install`（下载/写盘/装包，与 install 工具同等效应）；`urlread` 经 webnet 桥出网。故「装包不该被 eval 表达」的剪枝论据需保留但承认 eval 本身有该效应面（剪枝判据改为「是否有 eval 表达不了的**结构化返回或 UI 态**」，不是「是否有副作用」）。
- **并发补验**：`getWorkspace` 经 `_enqueueTask`（`ws_` 前缀任务）已实证；`executeCell` 有独立 `_isRunning` 互斥（另一层守卫）。golden master 增「同一 tick 发两个 call」用例。
- **onCall 默认内存计数器**（环形缓冲，经调试句柄/`get_system_state` 读取，不联网）——不再是 no-op 空承诺。
- **Disposable 收敛**：只用于通道 attach/卸载 + 插件生命周期；工具级 dispose 留在升级触发条件下。
- **原生通道不发骨架**：改发 **fake-channel 契约测试**（用假 channel 实现 Channel 接口并跑通 attach/detach/投递）——同样证明第三个 adapter 可加，且不会腐烂。
- **测试清单补 A 不变量与类型层**：`handle` 永不 reject（throw 非 Error / throw undefined / 返回 undefined / 不可序列化值）；id 回显；构造期查重；init 幂等；`ready.tools ≡ list()` 逐字相等；`@ts-expect-error` 两条（dep key 写错、访问未声明 ctx 键）；网桥零 import 服务用 lint/依赖检查钉住。
- **用户故事 15 移入贡献文档**（流程规则不是用户故事）。

### 六、升级到 B 全案的触发条件（不变）

出现「工具住别处」的贡献方模块；或引擎运行期自报能力导致工具集依赖运行时数据（provision 静态过滤不够用）。触发前不建 pack/registry/工具级 dispose。

## Testing Decisions

- **最高位 seam = 分发机的 `handle()`**：全部行为测试直调（DOM-free、引擎-free，注入对象字面量 deps）。协议层单独快照测试（归一化后）。
- **golden master 先行（落实顺序第 0 步）**：对**旧实现**录制——每工具 × 成功/失败/边界 × 两通道（legacy 事件 + 直柄）+ 「同一 tick 两 call」并发用例；全绿后才动重构。
- **偏差表逐项勾销**：第 3 步每加一项新行为（校验/超时/可用性/onCall）一个提交，偏差表对应项从「未实现」变「已确认」。
- **唯一迁移验收**：golden master 在偏差表之外**零差异**。
- 反向断言必备：空 code 必报 / unknown tool 必报 / provision 缺失调 CAPABILITY_UNAVAILABLE / 删 octave_eval 表行必红 / 恒等式 `eval(code) ≡ callTool('octave_eval',{code})`。
- fake-channel 契约测试：假 Channel 实现 attach/detach/投递全过。
- `@ts-expect-error` 类型层两条。

## Out of Scope

- ready 重发 / 动态工具集（归升级触发条件）；
- 原生 modelContext 通道实现（fake-channel 契约测试替代骨架）；
- pack/registry/工具级 dispose（升级触发条件）；
- EvalPort 双引擎共享抽象（两族落地后再看）；
- 权限机制（只留 effects 标注）；
- 两红修复（已单独验收完毕并绿，与本文无关）；
- #15 同会话缓存盲区（UI 已留痕，跨会话兜住；方向 size+mtime 或抽样哈希，不进本轮）。

## Further Notes

**二轮复审的三处「我方撤回/缩水」照单全收**：Q1 消解了「建能力级串行」的担忧（supervisor 已有 `_enqueueTask` 串行 + Kill Ladder）；Q3 第四形状撤回；Q2「总是列出」使「名册=可用性投影」缩为「按 provision 过滤」——本终版据此把 health 移出 list 的 wire。

**两处实证补充**（本轮新查，支撑应改项）：`getWorkspace` 亦经 `_enqueueTask`（并发安全覆盖 workspace 读）；**eval 可经 `pkg install`/`urlread` 走到 install 同等效应**（宿主 pkg shim `__web_pkg_fire__` → `OctaveAssets.install`）——故 eval 的 effects 必须保守标 `sandbox-escape`。

**落实顺序**（复审建议，采纳）：0 录 golden master（含并发用例）→ 1 偏差表定稿 → 2 骨架迁移（唯一验收=偏差表外零差异）→ 3 逐项加校验/超时/可用性/onCall（每项一提交、逐项勾销）→ 4 omc 到来走决策 7。
