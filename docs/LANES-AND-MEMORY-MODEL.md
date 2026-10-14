# 内存架构与分支线经验（wasm32 / wasm64 / 性能线，2026-10-14）

> **性质**：经验集 + 判据表。**为什么"一线一架构"不是洁癖**，以及混编的失败模式长什么样。
> **来源**：`Octave-Full-Wasm` 实测三次混编事故 + 完整的两档产物/四格站点实践。
> 所有命令都可复跑；所有事故原话都来自真实报错。

---

## §0 一句话

**"一线一架构"（一线只编一个内存档）不是规矩癖，是因为混编的失败模式是
"两边都建成功、自检全绿、运行期才炸"** —— 而这种错**极难从现象倒推原因**（下面 §2 有三次实测）。

---

## §1 两个档到底是什么（本仓必须分清，因为它决定"能装什么"）

| | wasm32（memory32） | wasm64（memory64） |
|---|---|---|
| 指针宽度 | 32 bit | 64 bit |
| 单模块内存上限 | 4 GiB | 极大（实测探到 **5 GiB / 8 GiB 都真分配成功**） |
| 宿主形态 | 导出 memory（自持） | **导入** memory（宿主提供） —— 实测：`imports_mem=1, exports_mem=0` |
| 对**本仓内容**的含义 | 异架构的 `.oct` / 预编译件**装不了** | 同左（反向也不行） |

**权威读法**（别猜，两条命令都能量）：
```bash
# ① 自带工具（容器内）
sudo docker exec o113 /emsdk/upstream/bin/llvm-readobj --file-headers <wasm> | grep -E "Arch:|AddressSize"
#      ⇒ Arch: wasm64 / AddressSize: 64bit
# ② 浏览器/Node 侧（看 memory 是导入还是导出）
node -e "const m=new WebAssembly.Module(require('fs').readFileSync(process.argv[1]));
console.log(WebAssembly.Module.imports(m).filter(i=>i.kind==='memory').length,
WebAssembly.Module.exports(m).filter(e=>e.kind==='memory').length)" <wasm>
```

---

## §2 ★ 三次实测事故（**混编的失败模式**，这才是"为什么成文"）

### 事故 1 · 链接期就炸（最好的一种）
wasm32 编出的目标文件链进 wasm64 模式：
```
ida.c.o: wasm32 object file can't be linked in wasm64 mode
```
影响：整批 `__ode15__` 挂掉（链了 wasm32 版 sundials）。

### 事故 2 · 加载器只给一句话，而它与"缺符号"极像
把 wasm32 模块塞进 wasm64 宿主，加载器说：
```
incorrect architecture (wasm32 vs wasm64)
```
**而"缺符号"的形态是**：
```
Cannot read properties of undefined (reading 'value')
```
两者混在一个日志里时，没人能一眼看出"是架构错还是符号缺"。

### 事故 3 · 最坏：全绿然后运行期炸
**宿主与 `.oct` 都"建成功"、构建自检全绿**，运行期才报：
```
TypeError: tlsInitFunc is not a function
```
根因：wasm32 的 sysroot 编 wasm64 模块 ⇒ 产物**没有 `_emscripten_tls_init`** ⇒ 线程宿主拒载。
这是上游 LLVM-wasm 的 **issue #1**（对方已修：v0.1.1 起两档 sysroot 都发 + 缺档**硬拒绝**）。

**三条的共同教训**：
> **"建成功"不等于"同档"**；而"不同档"的报错**不是一处、是三种形态**，
> 其中两种看起来像"缺符号"。⇒ **必须有机器判据**，不能靠人看日志。

---

## §3 判据：架构纯度闸门（照抄这个形状）

```
python3 build/113/check-lane-purity.py --lane <档> --host <宿主wasm> --oct <目录…> [--site <站点>]
```
**三条判据**（逐条 fail-closed）：
1. 宿主 wasm 的 `Arch` == 车道声明的档（用 `llvm-readobj` 读，不猜）；
2. 该车道 `.oct` 目录里**每个** `.oct` 同档（**0 个也算未通过** —— 零值守卫）；
3. 站点**本档专属**目录（`assets/oct-<lane>/`、`assets/octdir-<lane>/`）里的 `.oct` 同档。

**两条实测纪律**：
- **反向断言必须有**：喂一个错档 `.oct` ⇒ 必须报（自证里做，证明判据不是恒真）；
- **别把"基础档"目录喂进去**：多档站里 `assets/oct/`、`assets/octdir/` **合法地装着另一档**的
  `.oct`（那是基础档的），查了必假红 —— 实测在一个四格站上产生 **44 处假报**。

---

## §4 一线一架构的落地形状（多档站点长什么样）

`Octave-Full-Wasm` 的**四格站点**（同名文件、子目录区分）：

```
<站点>/
├── octave.{js,wasm,data}          # 基础档（wasm32）
├── threads/octave.{js,wasm}       # 线程档（wasm32 + shared memory）
├── w64/octave.{js,wasm}           # wasm64 + 线程（现役最快）
├── w64-base/octave.{js,wasm}      # wasm64 无线程
├── lanes.js                       # 档清单（页面按此择档）
└── assets/{oct,octdir,oct-threads,octdir-threads,oct-w64,octdir-w64}/
                                   # ★ 每档专属 .oct 目录（判据 3 就查这里）
```

**页面怎么选档**（本仓要懂，因为"装什么内容"取决于档）：
- **带 COI 头**（`COOP: same-origin` + `COEP: require-corp`）⇒ 选**线程档**（或 `w64`）；
- **不带 COI** ⇒ 只能选**无线程档**（共享内存需要跨源隔离）；
- **选错档 ⇒ 硬失败**（不是静默降级）—— 这条要专门测（反向断言）。

**为什么内容仓要知道这个**：一个包在 wasm32 档与 wasm64 档可能需要**不同的字节**
（`.oct` 加速件是**按档编**的）⇒ 端口的 `form`/`targets` 轴就是为这个准备的
（见 `port/README.md`）。**同一个包名、两个档、两组 sha** —— 这是正常的，不是错误。

---

## §5 性能线的经验（"IllegalPerformance"这类分支该怎么切）

**判据先行**：任何"更快"的分支都要有**差分门**（A/B 同旗标 + 变异自证），
否则你量的是"改了之后"不是"因为改了"。

**实测封口的三类（别重开）**：
| 方向 | 结论 | 依据形状 |
|---|---|---|
| 换分配器（mimalloc） | **有效**（已采纳） | 交错 3 轮取中位，比值落台账 |
| 换 BLAS（OpenBLAS 线） | **有效**（已采纳） | 同上 + IEEE 逐位红线 |
| libm 标量替换 | **负判决** | wasm 无标量 FMA ⇒ 拿不到收益，如实记负结论 |
| 热点余下部分 | 全在**语言自身源码**里 | 热点仪器（`hotpath`）定位，不猜 |

**一个反直觉但重要的纪律**：
> **负判决也是资产**。把"这条路走不通"连同判据记下来，下一个 agent 就不用重走
> （本仓有专门的"翻案台账"：`retractions.json` —— 被推翻的断言重新出现时报错）。

---

## §6 ★ 与本仓（Octave-Extra-Content）的直接关系

1. **内容有"档"属性**：`.oct` 加速件按档编 ⇒ 端口记录里 `targets`/`form` 必须能表达"这条只服务哪一档"；
2. **同一包多档 = 多条记录**（或一条记录的多个分件），**不是一个包名一条**；
3. **本仓不编 `.oct`**：编译是宿主/工具链的事（`LLVM-wasm` 出工具链、宿主侧 `compileExtension()` 编排）。
   本仓只保证"**哪个档要哪些字节、sha 是多少**"是**可核对的事实**；
4. **别在档案里写"wasm64 优先"这类价值判断** —— 那是宿主的择档逻辑（`lanes.js`），
   本仓只陈述事实（哪些档有件、各自的 sha）。

---

## §7 复跑命令

```bash
# 架构纯度闸门（本仓内容不适用，但要知道宿主怎么查我们的内容）
python3 build/113/check-lane-purity.py --selftest          # 6 条自证
# 读某产物的档（权威读数，不猜）
sudo docker exec o113 /emsdk/upstream/bin/llvm-readobj --file-headers <wasm> | grep -E "Arch:|AddressSize"
# 各档身份（宿主台账键；现值以台账为准，别手抄）
python3 build/facts.py show w64_wasm64
python3 build/facts.py show threads_shared_memory
```
