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
- **角色共识再次确认（2026-10-16，用户原话「内容仓负责推广标准，然后作为 OCTAVE 核心的
  我们做好适配」）**：不是新判决，是对既有分工的**再确认** —— 本仓 = 推广 + 收口 + 档案/配方/
  内容语义；宿主（Octave-Full-Wasm）= 端口产地（**标准由宿主定稿** —— 推广 ≠ 产地方）+
  消费适配（装配/闸门/客户端）；UI 仓 = 两条契约。**实盘已运转**：本仓已推给 LLVM（其表过宿主
  校验器、已并入 `ok`）、OM 缺席（合法）；宿主对一切表 fail-closed 拒收。
  **本仓确认（内容仓的话，回应 host `mail/017` §②）**：无异议。与 2026-10-14「去中间商」
  判决及本仓 `mail/003` A1/A2 的立场一致；宿主直接落本仓 STATE 的**程序问题**已由其
  `mail/017` 自认并补信，此条线闭合。

- **端口推广 + 内容收口**（2026-10-14 起，本仓对外角色）：本仓是 content-list 端口的
  **推广方**（把标准推给各生产者）与**内容记录的收口方**。**平级铁律**（用户点令 2026-10-14）：
  **任何不作为引擎插件的仓库都与引擎同级** ⇒ 本仓与 `LLVM-wasm` / `OpenModelica-Full-Wasm` /
  UI 仓**同级**，推广**不是派活**（唯一约束来自标准）。
  ⚠️ **「收口」的窄定义**（采纳 OpenModelica `mail/002` 的措辞）= **内容记录的单一聚合点
  （记录的生产侧汇总，是"归属"的落地）**，**不是运行期端点** —— UI 读的仍是**宿主站点里
  装配好的表**；别把"收口"读成"UI 直接读本仓"。
  ⚠️ **端口产地仍是宿主**（见上条）—— 推广 ≠ 产地方；本仓推的是**宿主定稿的标准**。
- **收口账**（三家在册，2026-10-17 更新）：本仓 = **已出表 + 边已出 + 候选集已出 +
  包级描述已出**（`--emit` 过宿主校验器 ✔；`symbolic.deps == ["pyodide"]`；
  `versions[]` 52 候选全 staged；`description`/`links` + `optional_keys` 声明）；
  `LLVM-wasm` = **已出表 + 宿主已复跑并入 `ok`**；`OpenModelica-Full-Wasm` =
  **缺席（合法）+ 已发引擎版本**（`v0.1.0-wasm32` first-light，2026-10-17 规范核查**合规**：
  引擎产物/工具链件正确不进表；MSL 出表判据未触发（站点零 `import Modelica.`）⇒ 不出表
  是正确行为；版本身份证键名锚台账。核查信投其仓 `mail/006`）。
  ⚠️ **两档区分**（宿主 §债 的教训）：**「已出表/已出边」≠「宿主 pin 已吃到 / 已并入」** ——
  后者要宿主 **bump submodule pin** 或 `--upstream` 并入，是**它的**判据。
  **`versions[]` 全链已闭环**（五段：schema 三不变量 → 本仓 `--emit` → 宿主 `resolve()` →
  catalog → 浏览器；**宿主三层对账全过**，`mail/019`–`021`）。
- **能力层依赖 = 硬依赖**（2026-10-15 裁决，回应 host `mail/012`）：站点没供能力层 ⇒
  `install` **响亮失败**（`not-found`），**不是软门**。判据：软门无处声明（§2 禁新字段）⇒
  只能藏进适配器（正是刚删掉的形状）；且"装上了却跑不了"的错误信息**指向错方向**。
- **端口三裁决**（宿主 `mail/008`，已同步 `port/README.md`）：①能力层 `content` 留空（不扩枚举）；
  ②加 `consumer` 可选轴（`octave`/`omc`，缺省 octave）；③`pin` 建议前缀形态（不强制）。
- **端口第二批答复**（宿主 `mail/010`）：①`license` 保持自由串/对象；②「普通条目」不限条数；
  ③`--upstream` 并入 `ok`；附 `size` 由 `form` 定。**deps 闭合分域**（本仓部分闭合 + 宿主 R9）。
- **`arch` 轴**（宿主 `mail/017`，已同步 `port/README.md`）：三档语义（纯 `.m` 不带 / 含 `.oct`
  必带 / 能力层不带）；**派生不自写**（从 `.oct` 字节读）。
  **`versions[]` 轴**（`mail/019`–`022`，已同步 `port/README.md`）：三条不变量 +
  **staged 是"字节在谁那"的函数**（生产者态 = 我探过包；装配态 = 字节在站点；两张表各自如实）。
- **一处已报的宿主缺口**（`mail/022`，本仓实证）：`optim` 的 `url` 带 query
  （`…download.php?package=optim-1.6.3.tar.gz`）⇒ 宿主 `--upstream-bytes` 的 `basename`
  映射命中不了缓存名。今天货架路径不经过它，**一旦走 `--upstream` 即变真问题**。
  宿主已判 **(a)** 并加 `byte_name_candidates()`（判序按"末段像不像归档名" —— 比"query 优先"
  更稳：`download.php` 是脚本名，先试它会**找错**文件；**"找错"比"找不到"更坏**）。
- **"文件里对、装配态才见真章" 六类**（跨仓最稳定的一类坑，每条都有实测出处）：
  ① 假引用（`R-002` `needs`）② 硬编码边（宿主适配器藏实现）③ pin 未 bump（文件对、submodule 旧）
  ④ 声明不消费（宿主 `resolve()` 不吃 `versions`）⑤ 绝对 URL vs 相对落点（`site/https:/…` 假目录树）
  ⑥ 规则只做在一条路径（同源改写漏在 `--upstream`）。**共同点 = "某处的声明"与"某处的消费"
  之间没有对账器** ⇒ 跨仓纪律再加一档：**"我这侧对" ≠ "你那侧吃到"**（收口账按两档记）。
- **UI 仓已建箱并推广内容契约**（2026-10-16，用户点令）：`Octave-UI/mail/{README.md,001-…}`
  + `.gitignore` 白名单放行；首封 = 信件概念 + 内容契约（四态/`content` 诚实/`consumer`/
  `versions` 语义 + 「归属 ≠ 投送」）。**可达性**：本仓 private、UI 仓 public ⇒ 它能读本仓？
  **不能**；回信三条路（投本仓 / 放它仓 `To: extra-content` / 宿主转达）。
  ⚠️ **投递规则的一致例外**（两边 `mail/README.md` 同款）：**`To:` 指名本仓的信若落在对方仓
  （因本仓 private 推不进来），读它是收信不是越界** —— 判据极窄（`To:` 指名才算）。
- **★ UI 已接纳内容契约**（2026-10-16，`mail/024`）：UI 回信逐题答（A1 今日无商店面、
  规划已列 / A2 **加了** `CONTEXT.md` §五——五条语义逐字对齐本仓 `001`（我复核）/ A3 读表
  = 站点装配态 `assets/forge-catalog.json`，`upstream-lock.json` 只锁引擎产物）。
  **它还自己跑了台账放行与 13 道闸门（我复核全绿），并双投回信（它仓 `002` + 本仓 `024`
  副本，只有信头编号不同 —— 投递副本的正确形状）**。⇒ 内容契约这条边**正式接通**：
  三家消费者态全在册（LLVM 并入 `ok` / OM 缺席合法 / **UI 接纳**）。
- **★ UI 的 `PackageManagerPlugin` 已落地**（2026-10-16，`mail/025`；本仓 `mail/004` 规范的
  消费实现）：命名遵守判决（**不叫 Market**，注册 ID `package-manager`，UI 呈现「包与扩展管理」）；
  字段直读站点表 / 判断走 `IAssetsPort.getStatusOf`（`BrowserAssetsAdapter` 直达宿主
  `statusOf`）/ `withheld` 置灰「此版未上架」/ `content: []` 呈现为运行时徽标（非未知非空包）/
  四态不降级 / 闭包口径已改成精确式（`Σ size of 闭包 ∩ form:"tree"`，真值以 `planOnly` 为准，
  **一致性进了它的单元测试**）。10 项契约测试 + 全仓 209/209 全绿。**我核实**：
  `src/modules/plugins/package/` 五文件在、`CONTEXT.md:61` 口径精确。
  ⇒ **宿主 `browse()` 的"等 UI 真需求"已成真** —— 但 UI 尚未在宿主开 Issue（规范 §6 说开工时提）。
- **跨仓催办已闭环**（收口方职能，2026-10-17）：宿主工单 65 缺口 2（`.oct` 缺 `_ZTIi`
  typeinfo 导出）—— LLVM-wasm 已答（其 `mail/009`，宿主侧 `mail/026`）：**归属 = 宿主的
  ABI 决策**（第三种情况：**两边都未提供、现役零使用** —— 宿主二进制 25 个 `_ZTI*` 全是
  Octave 类；emcc 官方路径同样导入 `_ZTIi` ⇒ 非工具链缺陷；11,663 个现役 `.oct` 零个用
  基本类型 typeinfo）。LLVM 建议宿主支持（keep-list + 终链一行）；**判定权在宿主**。
  其悬案 03（tag 依赖面）同批结案（全量 4084/11663 ≈ 35.0%，稳定）。已回信收线
  （`LLVM-wasm/mail/010`：收口账记法 + 一处数字口径提醒 —— 其信引旧值 3,592/10,246
  而台账已是 4,084/11,663，不影响结论）。
  **宿主已裁决 = A**（`mail/027`，逐条复核 LLVM 证据后接受）：keep 生成器显式追加 7 条
  基本 typeinfo + 容器现役 keep 同步 + 自证（闸门台 46）；**重链留独立批**
  （`ready-for-human` = 产品决定）。⇒ 收口账三态：归属已确认 ✅ / 已裁决 A ✅ /
  **重链待产品决定**。
- **三线模型终版**（宿主 `mail/027` 转达用户点令纠偏，2026-10-17）：**wasm32**（32 单线程、
  无 `-pthread`、无 COI）/ **master**（wasm64 多线程、COI）/ **IllegalPerformance**
  （64 多线程 + Rust 补丁、**non-free**）。**分档 = 用户可达性 + 许可线，与性能无关**；
  "其他仓库也只会有这三种线"。`arch` 轴天然两值（wasm32/wasm64）、与 `consumer` 正交
  ⇒ 本仓零改动；`wasm64-NEXT` 分支已删（本仓查无引用，无需清）。
- **宿主预编译预告**（`mail/027` §⑤）：下一批按三线口径只编两份（wasm32 无 pthread /
  wasm64 + MEMORY64）⇒ 站点将出现**带 `arch` 的包条目**（含 `oct` 必带 `arch`，
  三档语义不变）；`versions[].stage` 判定不变。本仓待那批上线后同步 `port/README.md`
  实例描述。宿主 `browse()`（读面）优先级**已上调**（UI 已真实消费引擎契约面 ⇒
  "等真需求"成真）；本仓已请求其返回带**包级 `description`/`links`**（见下条）。
- **★ UI 四问已逐答**（2026-10-17，UI `mail/028` 问、本仓回信投其仓 `mail/006`）：
  - **Q1 错误码**（引擎契约 ⇒ 转呈宿主）：UI 截到的 `Module.FS 尚未就绪` 是宿主
    cause 闭集（`bridge/assets-loader.js:731-737` 六码）的**漏网之鱼**（该 throw 不在表内）；
    诉求 = 闭集补全 + cause 升为错误一等字段；根因形状 = "用 regex 匹配中文当协议"。
  - **Q2 版本描述接口**（内容契约 ⇒ **本仓裁：方案 A 分两层**）：**包级 `description` +
    `links` 进表**（数据有货：上游索引包级一条；**已落地** —— `--emit` 出这两字段 +
    表顶层 `optional_keys: ["description","links"]` 协商声明；宿主校验器实测：
    不声明 ⇒ fail-closed 撤下条目（协商规则第一次拦住合法新字段，证明其工作），
    声明 ⇒ `ok`；`--selftest` 41→45）；**逐版 description/release_notes 不做**
    （上游无此数据，**不编** —— 同 kinds 的"许编"病）；
    方案 B（异步接口）不需要（browse() 透传静态字段即可）。
    样件已投 UI（其仓 `mail/007`）+ 宿主（其仓 `mail/029`，请其装配器透传 + browse 带出）。
    **终裁（`mail/030`，回应宿主拆分文件建议）**：**内联维持**（实测 description 13 包
    合计仅 865 字节——"几十 KB"担忧来自逐版假设，已裁不做；links ~9 KB 是大头 ⇒
    **下一批瘦身去 icon**，留 label+url）；**`desc_url` 拆分文件不采**（规模不够 +
    按需第二 catalog = 第二内容通道风险；将来"单包描述 > 若干 KB"再启，判据写明）。
  - **Q3 双模式**（判决已定 + 本仓补三档语义）：`ways` 是派生不是记录；UI 不做"每包切换"
    （多数包无选择：纯 m 不存在编译、src 是可选加速件）；**不引入 `flavor`**（预编译与否
    是同一版的两种取得路径，不是版本的味道）；推荐交互 = "默认安装 / 高级：从源码构建"。
  - **Q4 LLVM 前置**（引擎契约 ⇒ 转呈宿主 + 本仓裁 deps 语义）：**`deps` 不含编译器**
    （deps 只装运行时硬依赖；编译器是 `compile:true` 路径的闭包语义，宿主实现）——
    否则"装 statistics 必拉 48MB 编译器"。源码构建的档可用性判据在宿主；`arch` 轴
    已覆盖预编译件档匹配。
- **★ UI 四问已闭环**（2026-10-17，宿主 `mail/029` 答集 + 本仓转达）：Q1 **宿主已落地**
  （17 处 throw 全带 `err.code`、14 码闭集、四态分类改读 code —— 我逐条核实；
  本仓发现：`_byCode` 映射表只收 7 码，其余只带 code 不进 Verdict 分类 —— 已提醒宿主
  补全或写明边界）；Q2 终裁内联（见上）；Q3 宿主口径（默认路径即预编译优先按档自动，
  UI 不做选择器；compile:true 未实现）；Q4 宿主口径（planOnly 把工具链算进闭包 =
  规划拦截；wasm32 置灰是产品决定；LAYER_UNREACHABLE 已进词表；diagnostics 未实现）。
  答集已转达 UI（其仓 `mail/008`，含"能接 vs 要等"对照表）。
- **★ 发版模型判决已收**（host `mail/031`，判决书在其 `build/113/NOTES-release-model.md`）：
  **发布单位 = `(name, version, arch)` 三元组**；**架构做索引键不做版本轴**（不造
  `optim-1.6.3-wasm32` 这种上游不存在的版本）；源码包 A1–A6（本仓已产）/ 预编译件
  B1–B7（宿主新立）两套判据各自可机器验。**本仓不用改档案**：`artifacts[]` 归宿主
  装配补（"你不构建就量不出 sha" —— 与 staged 语义同一条纪律）。
  边界（如实记）：`control`（9 `.oct` 随站资产）不在本仓档案 ⇒ 今天无发布身份；
  **若将来进市场 = 本仓先把它加进货架档案**（宿主不替它编假身份）。
  现役实测：5 包 × 2 架构 = 10 artifact 全 staged、逐文件 sha 与站点相符。
- **★ read/ 读信规则已被宿主采纳**（host `mail/032`）：其仓已移植 `mail-read.py`
  （自证 10/0，含 bug#1 反向断言）+ 归档 16 封历史信（`git mv` 全部识别为 rename，
  `--follow` 可追）。**它抓出并修了本仓提案漏掉的一个真坑**：`check-mail-boundary.py`
  的零值守卫 vs 合法清空 —— 信全部归档 ⇒ `mail/*.md` 空 ⇒ 闸门假红。修法 = 未读区空时
  **退扫 `read/`**（`To:` 不变量照样成立）+ **两处都空仍必红**（防"归档绕过的恒绿"，
  闸门自证 5→8/0）。本仓照收该修法思路（本仓无 boundary 闸门，无直接动作）；
  其指出的 `--all` 死分支已清（纯整洁，语义不变）。
- **跨 agent 通信**：`mail/`（收件箱，只追加）；**投递落点 = 收信方 `mail/`**（写给宿主投宿主仓）；
  **投递 ≠ 提交**（落文件 = 发信方；提交推送 = 收信方）；由信催生的角色/契约结论落进本文件。

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
| `docs_count` | **3** | 2026-10-18T10:10:22+0800 | `ls docs/*.md | wc -l` |
| `llvm_bundle_bytes` | **34679853** | 2026-10-18T10:10:22+0800 | `stat -c%s /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz` |
| `llvm_bundle_sha` | `a9ba3b41e5fa8e74…` | 2026-10-18T10:10:22+0800 | `sha256sum /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz | cut -d' ' -f1` |
| `port_docs_count` | **1** | 2026-10-18T10:10:22+0800 | `ls port/*.md | wc -l` |
| `pyodide_core_bytes` | **6757104** | 2026-10-18T10:10:22+0800 | `stat -c%s /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2` |
| `pyodide_core_sha` | `2abdcc2e35208af4…` | 2026-10-18T10:10:22+0800 | `sha256sum /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2 | cut -d' ' -f1` |
| `recipes_count` | **2** | 2026-10-18T10:10:22+0800 | `ls recipes/*.md | wc -l` |
| `shelf_needs_capability` | **1** | 2026-10-18T10:10:22+0800 | `grep -l '能力层需求' packages/*.json | wc -l` |
| `shelf_oct_packs` | **0** | 2026-10-18T10:10:22+0800 | `python3 -c "import json,glob;print(sum(1 for f in glob.glob('packages/*.json') if any('oct' in (v.get('kinds') or []) for v in json.load(open(f))['versions'])))"` |
| `shelf_packs` | **13** | 2026-10-18T10:10:22+0800 | `ls packages/*.json | wc -l` |
| `shelf_verified` | **13** | 2026-10-18T10:10:22+0800 | `grep -l '"verified": {' packages/*.json | wc -l` |
| `shelf_versions` | **52** | 2026-10-18T10:10:22+0800 | `python3 -c "import json,glob;print(sum(len(json.load(open(f))['versions']) for f in glob.glob('packages/*.json')))"` |
| `tool_selftest_pass` | **45** | 2026-10-18T10:10:22+0800 | `python3 tools/forge-shelf.py --selftest 2>/dev/null | grep -c '^PASS'` |

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
