# 活状态（Octave-Extra-Content）

这个文件是**活状态文档**：正文只写「现在是什么」，**数字一律引用台账键**（`[[键名]]`），
不手抄。机器维护的块（事实台账 + 闸门名录）在文件末尾，由
`python3 zreflect/facts.py --render-doc STATE.md` 渲染，**不要手改**。

> ⚠️ 正确写法示范：本仓的包档案数是 [[shelf_packs]]。若写成「本仓有 13 个包」，
> `check_facts.py` 会报**正文裸数字** —— 那个数字从写下的一刻就开始腐烂（加一个包
> 它就成了假话，而没人记得回来改）。引用键名则永不过期。

## 本仓在管线里的角色

**生产适配器**：出**档案事实**（`packages/`）、**供给配方**（`recipes/`）、
**端口规范副本**（`port/`）、**事实系统运维**（`zreflect/` + `build/` + `questions/`），
并接**「内容契约」面向 UI 的那条边**（治理面：字段 / 四态语义 / 版本策略 / 许可台账）。
**不含字节、不装配站点、不运行服务**。字节同源由宿主 `Octave-Full-Wasm` 装配
（COEP 下同源是硬约束）。完整分工见 `docs/FORK-PIPELINE.md`。

- **两条契约**（接缝 §8.1）：**引擎契约**（宿主 ↔ UI）本仓**不碰**；
  **内容契约**（本仓 ↔ UI）本仓**接**（**内容语义**：四态含义 / `content` 诚实 / 版本策略 / 许可台账）。
- **端口产地 = 宿主**（2026-10-14 宿主裁决，见 `mail/004`）：schema + 校验器归宿主
  `build/extra-content/`，本仓**符合**它并共发布副本（`port/README.md`）。
- **归属 ≠ 投送**（同一裁决）：**归属**（谁定语义、负内容契约的责）= **本仓**；
  **投送**（UI 实际拿到什么）= **宿主**（站点里的表）；**对话**（深语义）= 经 `mail/`
  （本仓 private、UI 仓 public ⇒ UI 无直接通道，必要时宿主转达）。
  运行期唯一同源端点 = **宿主站点**；本仓是**治理面**的对话对象，**不是数据通道**。
- **端口推广 + 内容收口**（2026-10-14 起，本仓对外角色）：本仓是 content-list 端口的
  **推广方**（把标准推给各生产者）与**内容记录的收口方**。**平级铁律**（用户点令 2026-10-14）：
  **任何不作为引擎插件的仓库都与引擎同级** ⇒ 本仓与 `LLVM-wasm` / `OpenModelica-Full-Wasm` /
  UI 仓**同级**，推广**不是派活**（唯一约束来自标准）。
  ⚠️ **「收口」的窄定义**（采纳 OpenModelica `mail/002` 的措辞）= **内容记录的单一聚合点
  （记录的生产侧汇总，是"归属"的落地）**，**不是运行期端点** —— UI 读的仍是**宿主站点里
  装配好的表**；别把"收口"读成"UI 直接读本仓"。
  ⚠️ **端口产地仍是宿主**（见上条）—— 推广 ≠ 产地方；本仓推的是**宿主定稿的标准**。
- **收口账**（三家在册，2026-10-15 更新）：本仓 = **已出表**（`--emit`，过宿主校验器 ✔）；
  `LLVM-wasm` = **已出表、两处必修已修**（`content: []` + id 小写 + `upstream_url`；
  我复核 `--producer`/`--site` 均 `ok`，v0.1.2 已发布）；`OpenModelica-Full-Wasm` =
  **缺席（合法）**（判据：其发运模型集出现 `import Modelica.` 时出表）。
- **端口三裁决**（宿主 `mail/008`，已同步 `port/README.md`）：①能力层 `content` 留空（不扩枚举）；
  ②加 `consumer` 可选轴（`octave`/`omc`，缺省 octave）；③`pin` 建议前缀形态（不强制）。
- **跨 agent 通信**：`mail/`（收件箱，只追加）；由信催生的角色/契约结论落进本文件。

## 事实系统（Einfacht）接入状态

机制层 vendored 自上游 [Einfacht](https://github.com/ArchivalEra/Einfacht)，
**数据层是本仓唯一自己写的那个文件**（`zreflect/measure_extra_content.py`）。

- **两道守卫生效中**：重测时掉条（键没了）与改口（值换了）都会拒绝写盘，除非显式
  `--allow-drop` / `--accept-changes`（后者支持逐条：`--accept-changes=k1,k2`）。
- **闸门在线**：清单见文末闸门名录机器块（发现式名录从各闸门的**声明行**渲染 ——
  手写清单会漂）。执行面读声明不读文件名（`registry --run <相位>`）；off 态与
  「跑过且通过」可区分（`OFF:` 标记 ⇒ 聚合 `ran / off / failed`）。
- **复跑闸门**：台账每条 `cmd` 逐字复跑（裸值契约：stdout 必须等于值）。
- **钩子有持久的旋钮载体**：`reflect-hooks/Einfacht.env`，经可拔插件
  `einfacht-env.sh` 加载（删掉插件 ⇒ 回落纯环境变量）。

### 本仓的采集器纪律（两条刻意的取舍）

- **本仓 tip 故意不进台账**（`git rev-parse HEAD` 每提交都变 ⇒ `--check` 永不收敛）。
  这条已被翻案：见 `build/retractions.json` 的 `R-001`。要引用 tip 就在正文写命令。
- **上游字节不在本机就不写那条事实**（`recipes/*.md` 引用的 bundle / 运行时）：
  读不到就明说，不许用 0 冒充「已量」（采集器原则 3，宁缺勿假）。

### 上游字节身份（供给配方的「重取入口」）

配方引用的工具链与运行时字节，其身份（URL + sha256）落成**可核对**的清单
`build/upstream-lock.json`（`check_locks.py` 经旋钮 `REFLECT_LOCKS` 内联指向它）。

- LLVM-wasm 工具链 bundle 的 sha：[[llvm_bundle_sha]]（字节 [[llvm_bundle_bytes]]）。
- Pyodide 运行时 core 的 sha：[[pyodide_core_sha]]（字节 [[pyodide_core_bytes]]）。

> 硬纪律：**URL 是「重取入口」，不是运行时依赖**。上游删/换 URL 不影响已装配的站点，
> 只影响重取 —— 这正是 sha256 fail-closed 的用处（见 `docs/FORK-PIPELINE.md` §3）。

## 已知缺口（如实写，不假装查过）

- **端口 schema 2 本仓侧已完成**（2026-10-14）：`--emit` 现在出 `schema: 2`，每条带
  `form`（投送形态，本仓恒为 `pkg`）与 `content`（内容构成 = 旧的 `kinds`），`kinds`
  保留为兼容视图。**宿主侧**的校验器与端口产地（`build/extra-content/`）仍是待落地
  （宿主侧动作，本仓不改宿主仓）—— 见 `port/README.md` 待办。
- **能力层的表示法未定**：`symbolic` 已建档（[[shelf_needs_capability]] 个包标了能力层
  需求），但「怎么表达这条需求」还没定 —— 本文与 `recipes/pyodide.md` 曾错引成
  「接缝 §2 的 `needs` 轴」（**已翻案，见 R-002**），**实测接缝 §2 没有 `needs` 这个轴**
  （§2 判决：能力层 = `form:"tree"` 普通条目、进同一张 `deps` 图、不引入新字段）。
  表示法见悬案 `questions/02-capability-layer-axis.md`。
- **`verified` 只标了 `kinds`**：档案里的 `verified` 来自 `--probe`（tar 内容判 m/oct），
  **不等于「真跑通」**；「能不能真用」这一层还没有独立证据链（`docs/FACT-SYSTEM.md` §2 C4
  点名的缺口）—— `symbolic` 正是这条缺口的活例子（探出 `['m']` 却要 Python 运行时）。

<!-- AUTO:FACTS -->
> 本区块由 `zreflect/facts.py --render-doc` 从 `FACTS.json` 渲染，**不要手改**（pre-commit 会重算并 `git add`）。
> 正文里的「测出来的数字」只在这里生产：要引用就写 `[[键名]]`，不要手抄数字。

| 键 | 值 | 测于 | 复跑命令 |
|---|---|---|---|
| `docs_count` | **3** | 2026-10-15T21:01:39+0800 | `ls docs/*.md | wc -l` |
| `llvm_bundle_bytes` | **34679853** | 2026-10-15T21:01:39+0800 | `stat -c%s /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz` |
| `llvm_bundle_sha` | `a9ba3b41e5fa8e74…` | 2026-10-15T21:01:39+0800 | `sha256sum /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz | cut -d' ' -f1` |
| `port_docs_count` | **1** | 2026-10-15T21:01:39+0800 | `ls port/*.md | wc -l` |
| `pyodide_core_bytes` | **6757104** | 2026-10-15T21:01:39+0800 | `stat -c%s /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2` |
| `pyodide_core_sha` | `2abdcc2e35208af4…` | 2026-10-15T21:01:39+0800 | `sha256sum /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2 | cut -d' ' -f1` |
| `recipes_count` | **2** | 2026-10-15T21:01:39+0800 | `ls recipes/*.md | wc -l` |
| `shelf_needs_capability` | **1** | 2026-10-15T21:01:39+0800 | `grep -l '能力层需求' packages/*.json | wc -l` |
| `shelf_oct_packs` | **1** | 2026-10-15T21:01:39+0800 | `python3 -c "import json,glob;print(sum(1 for f in glob.glob('packages/*.json') if any('oct' in (v.get('kinds') or []) for v in json.load(open(f))['versions'])))"` |
| `shelf_packs` | **13** | 2026-10-15T21:01:39+0800 | `ls packages/*.json | wc -l` |
| `shelf_verified` | **13** | 2026-10-15T21:01:39+0800 | `grep -l '"verified": {' packages/*.json | wc -l` |
| `shelf_versions` | **52** | 2026-10-15T21:01:39+0800 | `python3 -c "import json,glob;print(sum(len(json.load(open(f))['versions']) for f in glob.glob('packages/*.json')))"` |
| `tool_selftest_pass` | **27** | 2026-10-15T21:01:39+0800 | `python3 tools/forge-shelf.py --selftest 2>/dev/null | grep -c '^PASS'` |

13 条事实。
<!-- /AUTO:FACTS -->

<!-- AUTO:GATES -->
> 本区块由 `zreflect/facts.py --render-doc` 从发现式名录（zreflect/registry.py 的声明行）渲染，**不要手改**。
> 执行面（hooks / CI）读 `registry --run <相位>` —— 相位是声明字段（`runs_at`），不是文件名。

| 闸门 | 相位 | 它挡住什么 | 消费的旋钮 |
|---|---|---|---|
| `check_ab.py`（A/B 闸门） | commit | A/B 同旗标不变式（非 allow 轴差异 = 混淆变量，A/B 作废） | `REFLECT_AB` |
| `check_envfile.py`（env 文件闸门） | commit | 守钩子的 REFLECT_* 载体（旋钮 typo / 指向缺失 / 空值） | `REFLECT_ENV_FILE` |
| `check_facts.py`（事实闸门） | commit | 块一致性 / 裸数字 / 坏引用 | `REFLECT_FACTS`, `REFLECT_DOC`, `REFLECT_NAKED_MIN` |
| `check_facts_replay.py`（复跑闸门） | commit | 台账 cmd 逐字复跑（裸值契约：stdout 必须等于值） | `REFLECT_FACTS`, `REFLECT_REPLAY`, `REFLECT_REPLAY_TIMEOUT` |
| `check_instruments.py`（仪器生命周期闸门） | commit | 恒常检测（first_seen）+ 被证伪量法登记 | `REFLECT_INSTRUMENTS`, `REFLECT_INSTRUMENT_DAYS`, `REFLECT_FACTS` |
| `check_invariants.py`（不变量闸门） | commit | 声明式不变量：仓库文件必须/不得含某片段（grep 级） | `REFLECT_INVARIANTS` |
| `check_locks.py`（锁定源闸门） | commit | 锁定源清单（URL + 文件 + sha256 的内容指纹） | `REFLECT_LOCKS` |
| `check_pins.py`（pin 闸门） | commit | 派生树 pin 一致性（stamp commit / dirty / 版本串对读） | `REFLECT_PINS` |
| `check_questions.py`（悬案闸门） | commit | 未结案的问题必须挂一个能跑的结算件 | `REFLECT_QUESTIONS` |
| `check_readme_sync.py`（三语 README 闸门） | commit | 语言版本是同一条断言的三份拷贝：结构互链 + 每次推送同批 | `REFLECT_READMES` |
| `check_retractions.py`（翻案重现检测） | commit | 被推翻的断言不许悄悄回来当现状 | `REFLECT_RETRACTIONS`, `REFLECT_DOCS`, `REFLECT_HISTORY_SECS` |
| `check_stale.py`（陈旧断言检测） | commit | sha 出处 / 退役名 / 测龄 | `REFLECT_DOCS`, `REFLECT_FACTS`, `REFLECT_HISTORY_SECS`, `REFLECT_RETIRED`, `REFLECT_STALE_DAYS` |
| `check_world.py`（world 闸门） | commit | 声明式验证对象：多线仓库共享验证环境的世界对账 | `REFLECT_WORLD`, `REFLECT_WORLD_LINE` |
| `doctor.py`（开工预检 doctor） | start-of-work | 进程 / 端口活性（查会死的东西 ⇒ runs_at=start-of-work，不进 pre-commit） | `REFLECT_DOCTOR`, `REFLECT_DOCTOR_TIMEOUT` |

14 道闸门（发现式名录派生 —— 手写清单会漂，加闸门 = 落一个声明行，这里自动长出来）。
<!-- /AUTO:GATES -->
