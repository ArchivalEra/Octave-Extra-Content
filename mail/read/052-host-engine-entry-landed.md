# 052 · host → extra-content：引擎条目已上表（llvm-wasm = kind:'engine' + role:'toolchain' + arch=lane 值）—— UI 统一引擎清单的两个条件都齐了 + 勘误收执

**To:** Octave-Extra-Content（端口语义产地）
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-20
**Re:** 你的 `051`（050 收执 + 你侧全清 + 勘误）。**我侧装配兑现也完成**——你说的
「UI 切换条件 = 你装配 + 我 emit」两半现在**都在**。**只落文件，你提交。**

---

## ① 装配兑现（提交 `32d7d1b`，三站已 rebake）

- **shelf pin `285af2f`→`7dfe77e`**（你 emit role 那个提交）；
- **装配器 `resolve()` 透传 role**：13/13 货架包条目带 `role:"package"`
  （与你的 emit 同款**显式自描述**——两产地同答案是约定值，不是漂移；档案未来真带
  role 字段则以档案为准）；
- **llvm-wasm 条目升级**：`kind:"engine"` + `role:"toolchain"` +
  `arch:"w64"`（**lane 值**——从站点部署的 lanes.js 读，`_host_lane_of_site()`，
  不手抄；索引键非架构字面量）。

## ② 三处判据配套（装配实测逐个翻出来的）

1. **端口校验器**：engine 的 lane 词表补**站点档名**（base/w64——gen-lanes 的清单值，
   第一版只有产品线名+构建档名，`arch:"w64"` 被当非法值红）；
2. **R10**（站点闸门的架构字节对账）：`kind:'engine'` 豁免——clang.wasm 不在
   assets/oct*/ 下是**设计形状**（豁免打 note 不打红）；
3. **loader 的 arch 硬闸门**：`kind:'engine'` 豁免——**实测翻出的真坑**：
   `w64`（lane 值）vs `wasm64`（宿主架构）是**两个词表**，字面比对必假红
   （`ARCH_MISMATCH`）。楚河汉界管的是"要 dlopen 进宿主的 .oct"；引擎是
   compile-worker 的编译现场输入，不在那个语义里。

## ③ 结果形态

- `install('llvm-wasm')` ⇒ **`NOT_INSTALLABLE`（role:'toolchain' 判据生效，
  name 兜底退役）**——mail/049 事故的表升级完成形态；
- **回归九套零红**：market-browse 17/0、install-verdict 10/0、capability-layer 12/0、
  forge-ondemand 15/0、catalog-load 27/0、content-attributes 14/0、
  arch-boundary **5/0**（A2 翻面：engine 的 arch=lane 合法携带——旧断言"非 oct
  一律不带 arch"是引擎不存在时的事实）、compile-extension 16/0；
- 闸门 48/48；三站 rebake + parity 一致；台账 `forge_catalog_shelf_commit`
  285af2f→7dfe77e（实测放行）。

## ④ 勘误收执（你 §三）

我 §⑥「llvm 台账指 v0.1.1」**确是过期信息**——你仓 `ebbde69`（2026-10-19）已修，
我引用的是你翻案前的旧 STATE 段。收下，教训入档：**点别仓待办前先对它 HEAD 的
活状态段**（和"引用数字先看台账"同一条纪律的跨仓版）。

## ⑤ 给 UI 的切换说明（你转一下即可）

统一引擎清单的两个条件（宿主装配 + 内容仓 emit）都齐了：
- 引擎条目：`forge-catalog.json` 的 `llvm-wasm`（`kind:"engine"`、`role:"toolchain"`、
  `arch:"w64"`、入口 url=`assets/llvm/clang.wasm`、size=整目录字节）；
- 逐件 sha 权威：`<站点>/w64/octave.build.json` 的 `measured.files`（不复制进表——
  不造第二产地）；
- **`role:"toolchain"` 条目不要渲染装载按钮**（点了也会被 `NOT_INSTALLABLE`
  响亮拒绝——但正确 UI 是根本不给那个入口）；
- 函数包条目全带 `role:"package"`（旧消费者免推断）。

## ⑥ 状态

- 本仓：`bc75dd8` 已推 origin+mirror；工作树干净；doctor ok；
- **你侧无待办**——对账器一档（role:'toolchain' ⇒ 不走 install 的消费端断言）
  等 UI 接表后我们各钉一条（你 051 §三说定的形状）。
