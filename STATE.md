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
- **收口账**（三家在册，2026-10-25 更新）：本仓 = **已出表 + 边已出 + 候选集已出 +
  包级描述已出**（`--emit` 过宿主校验器 ✔；`symbolic.deps == ["pyodide"]`；
  `versions[]` 52 候选全 staged；`description`/`links` + `optional_keys` 声明）；
  `LLVM-wasm` = **已出表 + 宿主已复跑并入 `ok`**；`OpenModelica-Full-Wasm` =
  **出表中（MSL 一条）+ 已发引擎版本**（2026-10-25 更新：MSL 站内资产落地〔OM
  `mail/016`〕⇒ 出表判据触发，我方字节对账一致 + 条目指导已发〔当日 ★ 条目 +
  `recipes/msl.md`〕，OM 按指导出 content-list；引擎条目另线 = 宿主 `mail/056`
  提单在途 + `057` 扩展。〔2026-10-17 时：缺席合法、引擎产物/工具链件正确不进表、
  MSL 判据未触发〔站点零 `import Modelica.`〕⇒ 不出表是正确行为；核查信投其仓
  `mail/006`〕。版本身份证键名锚台账）。
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
- **★ "输入消失"病根已有上游编号**（host `mail/034` 转达；**Einfacht #20 第③条**，
  2026-10-18）：宿主删 `threads` 档时漏改三张登记表之一 ⇒ 核心闸门 `probe-lane`
  被 sweep 按"缺输入跳过"**永久假绿**（94 套 / 1525 PASS / 0 FAIL —— 全绿，核心闸门
  一次没跑）。**三种形态同根**（闸门没考虑"空"是谁造成的）：
  假红（本仓 mail 归档清空 ⇒ 零值守卫红，host 已修）/
  假绿·跳过（缺输入 ⇒ 跳过不计 FAIL，host 实例）/
  假绿·默认值（裸跑写根、钩子读 build/ ⇒ 改口不生效）。
  **本仓自查（2026-10-18 host `mail/035` 更正后修正）**：形态二不适用（无 sweep/manifest
  机制）；**形态三未防——曾误记"已防"**（"没写盘"是执行顺序的巧合：先 `--render-doc`
  ⇒ `_load_or_die` 读失败先退出；**先量测裸跑必写根**——worktree 实测写出根
  `FACTS.json` 4161 字节/13 条的第二真值，且无任何 warn；`_load_or_die` 的提示
  "先在仓库根跑一遍量测"还在教人踩坑，host 实测同款并已报 Einfacht #20 评论区）。
  **本仓已修**：加 `build/facts.py` 兼容壳（宿主同款形状）—— 不带旋钮直跑壳 ⇒
  写 `build/FACTS.json`（实测 ✓ 根无野文件）；`zreflect/facts.py` 直跑仍会写根
  （上游机制，归 B4/#20 上游化）。形态一由 registry 的 OFF: 聚合防（C2）。
  **推广提醒已记**：read/ 附带给 LLVM/OM/UI 时带上 #20③ + **#20②**（默认值形态：
  先确认有没有 facts.py 仓内壳；OM/UI 更可能撞 ②，LLVM 撞 ③——一个包盖两形态）。
- **★ 纯下载模块设计已定稿**（2026-10-18，design-it-twice 四子代理 A/B/C/D + 用户四裁决；
  规格信投宿主/UI `mail/037`）：
  - **判决**：骨架取 C（常见调用者优先：download/index/unit 三入口、裸参数、拉取式状态）
    + 接缝哲学取 D（**下载/装载之间的接缝长在记录上**——OPFS 里的已核验字节 +
    manifest 记录 schema:1 + provenance 回显 url+sha256，与 content-list 端口同构）
    + 三收紧（A 的 url/sha 只从目录解析调用方给不了；B 的 remove 吸收取消；A 的
    目录漂移对账——记录 sha vs 当日目录 sha 失配自动重下）。
  - **用户四裁决**：① 同包多档并存允许（硬闸门在装载期 ARCH_MISMATCH，下载层只记账）；
    ② **引擎纳入同一解耦**（kind:'engine'，arch=lane；换引擎=下载另一档+装载界面
    重新拉起，零特殊代码路径。**sha 源更正（host `mail/038`，已核实）**：不是 UI 的
    `upstream-lock.json`（那是第三方源码锁，9 条无引擎条目）——是
    **`<站点>/<lane>/octave.build.json` 的 `measured.files`**（每档一份的产物身份证，
    三件套逐件 sha 实测在；与 src/pre 同构：核验依据 = 部署产物自证，不为 engine
    开特例、不造第二产地）；
    ③ 删除走 Octave 文件树（下载产物是 OPFS 普通文件，用户自己管理——不做下载管理面板，
    DownloadStore 无 remove 方法）；④ **自编产物不留存**（compile:true 编完即装载进 MEMFS、
    不写 OPFS 不产生记录；无目录事实 ⇒ 不校验——'不许编'纪律的反面应用）。
  - **三类生命周期**：持久层（OPFS）= 源码/预编译/引擎，全带 sha 验证才算已下载；
    会话层（MEMFS）= 装载态 + 自编产物，关网页即没。
  - **★ OPFS 布局（原生 Octave 实测定稿，11.3.0 本机）**：
    `downloads/{src,pre,engine}/` + manifest.json。核心判据 = **src/ 用上提布局**
    （inst/ 内容提到包根 + packinfo/DESCRIPTION）—— 实测：上提布局原生 Octave
    `pkg rebuild → pkg list → pkg load` 三连全通、与原生安装包共存 load 成功；
    可见性三要素 = 目录名 `<name>-<version>` + `packinfo/DESCRIPTION` + 一次 rebuild
    （pkg list 走缓存清单不扫盘）；`.m` 必须在包根（多套一层子目录 ⇒ pkg load 无报错
    但类 undefined——静默失败）。pre/ 存逐文件 .oct 字节（装载期按 manifest files[].path
    摆位，.oct 的家 = getarchdir 公式 archprefix/<name>-<version>/<arch>/）。
    **兼容判据写死：布局正确 = 原生 Octave 对它跑三连全通**（实测脚本即验收脚本雏形）。
- **★ 用户裁决⑤：源码包装载的必要条件 = LLVM 工具链已下载**（2026-10-18，
  端到端实测后落规）：**含 `src` 的源码包** ⇒ 现场编译 ⇒ **LLVM 能力层在场是必要条件**
  （未下载 ⇒ 装载界面拒绝并提示预下载）；**预编译包随便装载**（不受此约束，arch 闸门
  照旧）；**纯 `.m` 包不受此约束**（无 src 无可编译件——宿主验收 C5 实证 m-only 明说）。
  **端到端证据链**（全部真跑）：① 前置检查判据模拟 4 正例 + 3 反向（LLVM 未下载 +
  含 src ⇒ BLOCKED / 已下载 ⇒ OK / 纯 .m 无需 / 预编译不受限；不存在包/版本/非法 kind 必拒）；
  ② 宿主 `accept-compile-extension` **11/0**（真字节：cell2cell.cc → 真 .oct 13405B →
  `exist=3` dlopen 识别 → 真调用；C1b 证明编译路径消费四件供给 llvm/worker/headers/config
  ——LLVM 在场**事实上**就是必要条件；C6 坏源响亮报错）。**规格缺口顺带暴露**：
  站点 forge-catalog 的 packs 里**没有 llvm-wasm 能力层条目**（只有 pyodide）——
  下载模块按表现表读不到它 ⇒ 宿主装配器需把 llvm-wasm 作为 form:tree 条目进表
  （其逐件 sha 在宿主处，与 artifacts 同判据）——已并入给宿主的待办。
- **★ compile:true + diagnostics 已落地（host `mail/041`，我核过）**：
  `OctaveAssets.compileExtension(name,{onProgress,onDiagnostic})` 返回 Verdict
  （compiled/m-only 两态）+ diagnostics 日志流（实测 20 条）。**分段懒加载**（用户点令）：
  三段切——init 拉 sysroot(19.7MB)+clang(45.8MB)，**lld(31.8MB) 首次链接才拉**
  ⇒ 首编峰值 66MB 原始（gzip ≈25MB）非 81MB；编排仍 import 生产者 compile-core.mjs
  （不复制）。~~**已知边界（如实）**：现编产物**识别但不可调**~~（**已翻案，见下条
  「实测第二轮」**：C2c 现编语义正确，与预编同值）。裁决⑤的 **compiled / callable
  分开记**口径**保留**（"能不能编"≠"编出来能不能跑"仍是正确判据形状，只是两者现都为真）。
  验收 11/0 我独立复跑确认；宿主下一批：多 TU 包 + 工单 65 重链。
- **★ host 039 三件待办全部办结（`mail/040`，我核实过）**：① compile 排期已兑现
  （041 落地）；② 031 归档✓；③ **Einfacht 整层升 45ca586**——7 文件与上游
  **实质差异 0 行**（我收紧判据复验：`diff -q` 会被尾空行骗，须用实质行判据
  `[<>] [^ ]`）；本地自制分派/手植 import/旋钮注释全退役；盲写守卫反测 rc=2+零字节。
  **③b 活案例**（宿主抓的）：升级改了行为前提 ⇒ 不在机制清单里的本地闸门
  （check-mail-boundary 退扫）遇"未读区只剩 README"第四种状态假红——修法 = 空判据
  改"除 README 外无别的 .md" + 自证补形状。**收口方注记**：升级参照加一步
  `grep -rn "mail/\|zreflect/" .githooks/`（前提依赖的便宜登记位）。
  **宿主移植细节**：模块名不带 zreflect. 前缀（__import__ + sys.path[0] 形状）——
  本仓壳没踩（写对了）。
- **★ 追问闭环（host `mail/042` 答 (a) + 我逐条复核成立）**：宿主认账——"已上报"
  写在 STATE/脚本 say 行/设计稿**三处**时**信确实没发**（真假混句：provision 兜底
  拷贝真做了、"上报"半句没发生）。**更深一层（宿主自查 + 我复核）**：发布的
  v0.1.2 bundle 里**也没有** compile-core.mjs（tar tzf 逐条核：driver/ 4 件无它；
  manifest 13 条；**工作树 14 条含它**）——根因 = 时序：修复提交 14:47 晚于
  bundle 生成 14:31 / release 发布 14:39 **8~16 分钟** ⇒ **"修复 ≠ 发布"**，
  生产者 `mail/007` §⑤ 那句"v0.1.2 已 13→14 条"与发布资产不符（同一形状在生产者仓
  又演一遍）。宿主已补发正式信（宿主仓 045 = LLVM 仓 `mail/013`，我核实信在），
  请生产者二选一（重发 v0.1.3 推荐 / 同 tag 换包不推荐——check_locks 会撞），
  并建议其 check-release.mjs 加"tar tzf 已发布包 ↔ manifest 对账"（声明 vs 消费
  之间没有对账器——本生态反复踩的形状）。**追问抓对了一处真病**：三处不实断言
  已由宿主改为可复跑事实；退出条件写死（对方重发 ⇒ 换 pin + 删兜底 + 自证翻面）。
- **★ UI 咨询答复已收（`mail/039`，A1–A5 定稿意见）**：A1 三入口足够（离散事件点拉取
  index，非 rAF 轮询；建议 manifest 写入后发 `octave:download-changed` CustomEvent——
  零订阅成本，采纳）；A2 onProgress 契约完备（total 缺失走波浪动画**不伪造百分比**；
  phase 映射状态胶囊）；A3 other-arch **如实展示角标+置灰+tooltip，绝不隐藏**
  （OPFS 占用户真实配额，隐藏 = 空间被占却在界面找不到）；A4 引擎下载**必须
  planOnly 式预演确认弹窗**（逐件列体积+车道特性，严禁静默下载 30-45MB）；
  A5 **新增存储配额预检**（download 前 navigator.storage.estimate() 探测，
  (quota-usage) < expected+5MB ⇒ 前置拒绝而非 99% 时 STORAGE_WRITE_FAILED——
  采纳，新错误码 STORAGE_QUOTA_EXHAUSTED 一并登记，总 7 码）。
- **★ Einfacht 机制层升级至上游 `45ca586`（2026-10-18）**：机制 9 文件换新版
  （facts/guard/knobs/render/check_locks/check_questions/check_facts_replay/
  pre-commit/pre-push），**本仓 3 块本地补丁全部退役**（render 多 AUTO 块 / REFLECT_LOCKS
  旋钮 / MEASURE_MODULE 分派——上游 #15 上游化后逐字节同源）。**上游新件**：
  #14 修复（prose_of 剥全部 AUTO 块）、#20② 盲写守卫（write_target_problems：目标被
  gitignore 覆盖 ⇒ FATAL 拒写 + 载体在而旋钮未设 ⇒ warn + _load_or_die 提示改写）、
  #15 B1（Settling 续行支持）、回落占位**响亮警告**。**验收**（实测）：盲写守卫
  真拦（worktree 旧版误判排除后，主仓裸跑 rc=2 + FATAL + 零写出 + 回落警告响）；
  壳路径正常（build/facts.py 写 build/ 不受影响——**壳保留**：守卫拦"写被 ignore 的
  目标"，壳补全套旋钮，互补不冗余）；全套自证台 24 件全绿（check_questions 10→11、
  guard 16→20）；commit 相位 ran 8/off 5/failed 0；本地补丁与上游逐字节同源 ×6；
  数据层零牵连（台账 13 条、复跑全绿）。AGENTS 复跑命令补 REFLECT_FACTS 前缀。
- **★ 下载规格宿主批复（`mail/038`，三项确认 + 一处产地更正）**：
  ① engine sha 源 = `octave.build.json` 的 `measured.files`（每档一份，产物自证 ——
  I1 因此更干净：src/pre/engine 三者核验依据同构）；② `ARCH_MISMATCH` 口径确认
  （宿主现役实现 `assets-loader.js:678`：装载期 plan 阶段、hostArch 不读引擎、
  能力层 form:tree 豁免 —— 与裁决①"下载层只记账"完全一致，两层判断对象不同不塌陷）；
  ③ **`install()` 暂不收敛 DownloadStore**（宿主判决：install 是同步原子链无时间 gap，
  切两段只多一次 OPFS 往返无收益；两套 staged 语义不同——"字节在站点" vs
  "字节在 OPFS 且与今日目录对上账"——收敛 = 同一事实两产地（#20③ 形状）；
  新 6 码在一步到位的 install 里不该出现。**两条链并存各管各的**：
  install=站点随附即时装载 / DownloadStore=市场先下后装。将来若收敛由宿主发起走 mail，
  判据 = 两套 staged 语义能合并成一个）；④ 6 个新错误码按 `[state,cause]` 预填表
  （NOT_DOWNLOADED/VERSION_WITHHELD/FLAVOR_UNAVAILABLE=not-found 档；
  STORAGE_WRITE_FAILED/DOWNLOAD_ABORTED=failed 档；INDEX_UNREADABLE=cannot-know 档
  —— 该档只留"连目录都读不到"，与宿主 CATALOG_UNREADABLE 同级）。
- **★ LLVM 悬案 02 结案（wontfix，用户点令 5.0.7 一切不碰）**：验证目标"5.0.7→6.0.12
  方向"的前提（下游还在 5.0.7）已不成立——宿主 2026-10-11 三线全面切 6.0.12 并发运，
  5.0.7 轴整体退役。"不是验了知道，是问题问的那个世界不存在了"；单向证据留档、
  结案判据可复跑（下游回退 5.0.7 则复活）。⇒ **LLVM 悬案 3/3 全部关闭**，
  收口账：LLVM = 已出表 + 并入 ok + 悬案清零。
- **★ 给宿主的待办信已投（`mail/039` 宿主仓，2026-10-18，压缩上下文前的钉纸）**：
  ① compile:true + diagnostics 排期问询（下载功能的宿主侧关键路径——UI 的
  "从源码构建"按钮会等它）；② 它未读区 mail/031 该归档（已处理未归档）；
  ③ **Einfacht 整层升级提醒**（它只摘了盲写守卫单件，上游已到 45ca586——
  #14 修复/#15 三块上游化/#20② 全套；建议整层换而非继续摘件，参照本仓 b8e9bf7
  路径与三点注意）；④ LLVM 悬案 02 结案通报。
- **★ 全 coalition 盘点（2026-10-19）：宿主 compile 线五连发收线 + 我仓一处滞后落账**
  （信 `mail/015` → host）：
  - **宿主五连发全部实测成立**（我独立复核，不抄信）：① pin v0.1.1→v0.1.3（upstream-lock
    亲验）；② 兜底退役（provision 正向断言）；③ v0.1.3 发布件 18 件含 `driver/compile-core.mjs`
    （tar tzf 亲数）+ 部署盘 manifest **14 条**含 compile-core（generated 10-18T23:17）；
    ④ forge-catalog **15 条**（llvm-wasm 能力层 form:tree 进表——**我 039 待办① 的裁决⑤
    数据源请求已兑现**）；⑤ 多 TU 编译落地（cc8e47f + 8991f5d promote/回归/部署三层）。
    ⇒ **compile 线全收**：v0.1.2 缺口 → v0.1.3 结案 → pin 换 → 站点供给 → 目录进表，链条闭合。
  - **同一轮盘点抓出宿主两处勘误级问题**（`mail/015` B1/B2，只报不动）：
    **B1** 宿主仓 mail/read/ 有 gitignore 洞——6 封已读归档信盘上有、git 里没有、
    status 假干净（`!mail/` 放行了未读区、`!mail/read/` 漏放行——白名单"看不见"失败模式
    在传播目标仓首次实测现身；我仓自查 36=36 全跟踪无洞）；**B2** 宿主投 UI 的两封信
    （下载规格三项确认 + compile 落地通报）落错工作树——落在 zcode 侧 UI 工作树
    （untracked），UI 真实活动树在 antigravity 侧 ⇒ UI 看不到这两封（引擎 sha 口径
    009 勘误的根源）。
  - **我仓滞后落账（C1）→ 当场已修**（2026-10-19，盘点同批）：`measure_extra_content.py`
    的 LLVM_BUNDLE 默认路径 v0.1.1→v0.1.3（路径写死 = "量的是哪份字节"这个事实本身，
    换版必改此处并逐条放行改口）；台账重测
    `--accept-changes=llvm_bundle_sha,llvm_bundle_bytes`（两键改口放行；v0.1.1 旧值
    随改口退役，现值 = [[llvm_bundle_bytes]] / [[llvm_bundle_sha]]）。
    **独立对账**：我复算的 v0.1.3 sha 与宿主 `upstream-lock.json` 的 llvm-wasm 条
    **逐字一致**（对账命令见 `mail/015` §D）。⇒ compile 线在本仓侧**全清**。
  - **UI 勘误信已投**（`mail/016` → ui）：其 009 规格副本两处旧口径——engine sha 源
    仍写 `upstream-lock.json`（宿主已更正为 octave.build.json measured.files）+
    裁决⑤"别接不存在的接口"已被 014 时效更新（compile 已落地）。
  - **Einfacht #15 仍 OPEN**（上游 issue 列表亲验，#14–#20 全开）——反哺线不动，等上游。
- **★ OM 首次肉眼验收（2026-10-19，用户点令「验收几乎空白」后的补课）**：v0.1.0-wasm32
  全过——四套脚本断言 **43/0**（omc-page 10 / samepage 8 / mat-handshake 14 / omc-bridge 11，
  判据原样跑零漂移）+ 四个交互面真浏览器亲验（omc-bridge 演示页 / samepage 双引擎同页握手
  闭环 / 站点首页 7 客户端路由 / **OMShell 终端**：页面自装 MSL 4.1.0 后真敲
  `simulate(ChuaCircuit, stopTime=100)` → LOG_SUCCESS、timeTotal 0.741s、产出 .mat）。
  **OMShell 是全新覆盖**——四套脚本无一碰它，它是站点侧栏用户第一站，此前零验收。
  两个自动化验收方法坑记档（已投 OM `mail/007`）：①终端 Enter 走 form submit，
  CUA keypress 打不进去（人类无影响）；②外壳 iframe 动态 src 卡 frameLocator
  （直开子页 URL 正常）。**验收环境可复跑**：`serve-coi.py 8765 site-omc` + 四个
  `test/browser/run-*.sh`。收口账：OM = 规范合规 + 脚本 43/0 + 肉眼四面全过。
- **★ 钓鱼执法第一轮（2026-10-19，用户点令「各种插件都用用，出问题发信不修」）**：
  对两站点全部插件面故意使坏式验收。**发信级缺陷 ×1，全绿 ×5，环境澄清 ×2**：
  - **★ 缺陷（已投宿主 `mail/045`）：音频播放链断** —— `sound/audioplayer/audiorecorder`
    全部 `__player_audiorecorder__`/`__player_audioplayer__` undefined（wasm 产物 exist=0
    **vs 原生 11.3.0 exist=3**，原生对照拿下；`.m` 面在 FS、`.oct` 面不在产物也不在资产
    目录；宿主 accept-dldfcn 验过 audioread 读文件但**从未测播放链**——「文件里对、
    装配态才见真章」又一例）。JS 侧 webaudio 桥本身是好的。
  - **全绿**：p5canvas（plot→drawnow→560x420 真图、单例替换、close all 生效）/ webnet
    （懒加载后 urlread 全链通、坏 URL 4ms 明确失败）/ worker 模式（eval、长算不冻主线程、
    `while(1)` 可 interrupt、terminate 无僵尸 promise）/ **omc_* MATLAB 兼容桥**
    （并发 3 提交 seq 单调且应答不串、`\n` 转义命令 ok、collect 不存在 seq=99999
    **明说 pending**、同 seq 幂等取回——协议自洽，E 线「为 Octave 服务」链成立）/
    资产车道（catalog 35 资产名与货架对得上）。
  - **环境澄清**：audioread 在无 COI 页 dlopen 必死（LinkError shared=1 vs imported=0）
    ——嵌入式浏览器首测撞的是这个；宿主同款 headless（COI=true）下 audioread 系 4 个
    .oct 全部 dlopen 成功。**非缺陷**；lane 无 COI⇒w64-base / COI⇒w64 与声明一致。
  - **OM Simulator 钓**：坏模型 → `Simulation failed after 6 ms` + 解析器原文上屏
    （错误可见带定位，不静默）。OMShell 首开自动装 MSL（三包 SHA 同源、装完 Ready）。
  - **UI 体量信已投**（`mail/016` → ui 仓）：OM 站 162MB（引擎单体 71.1MB vs Octave
    28.3MB）、8 客户端形态、MSL 运行时装载、omc_* 接口跨引擎工作流入口——
    DownloadStore/PackageManager 的设计输入（不改已定规格）。
  - **★ 子代理三路战果（全收，2026-10-19）**：
    - **★ OM 发信级缺陷（已亲验复现 + 投 OM `mail/008`）：Export FMU 全挂** ——
      simulator 默认 BouncingBall → Export FMU → `fmu_link.rs: unrecognized dylink.0
      subsection: 6`（klu 库链接元数据解析失败，~170ms 响亮红错、页面不挂死、两次独立
      复现）。**连锁**：FMI Simulator 页在纯浏览器环境拿不到任何可加载 FMU（站点无示例
      FMU + 自产通道断）⇒ 该客户端对普通访客完全不可用。报错形态是好的（红错+rust 栈），
      坏在链接器功能。
    - **OM 其余全绿**：OMPlot 真画图（7 变量 → svg 出图）+ 反钓（假/空 .mat 红错
      `Corrupt header (1)` 且再喂真件恢复）；FMI 假 .fmu 红错且 Simulate 保持禁用、
      状态机回位；egui/dioxus 双变体真起真交互（`getVersion()="-rust"`、`2+3`=5；
      资源链逐件 HEAD 无一 404 无一空）。
    - **OM UX 事实（建议级）**：MSL 首启 ~2 分钟不可交互（egui/dioxus 默认
      `installMsl=true` 拉 19MB zip，worker 支持 `installMsl:false` 未用）；
      FMI 页缺示例 FMU 出路（缺陷修复前的过渡）。
    - **Octave 站剩余桥四点全过（无发信级）**：webfilepick（裸调如实报 fltk 门禁；
      装资产后两步协议跑通；**0 字节/255B/300B 超长名/Unicode+emoji 名全扛住**）；
      webaudiorec（空队列 drain 无异常；无麦克风 → 明确 error 三态 + Octave 侧清晰
      报错，不用空矩阵假成功；recordblocking 如实报 T10 边界）；lane 反钓（`?lane=不存在`
      静默当无覆盖回落 w64，与 lane.js 声明一致）；embed 模式正常（evalJSON ok）。
      轻微观察（不发信）：拼错 lane 名无 console 告警；裸 uigetfile 未提示可懒装载资产。
  - **钓鱼执法第一轮总结：发信级缺陷 ×2**（宿主音频播放链 / OM Export FMU），
    其余 **15 项全绿**，环境澄清 ×2。两封信均已投，等修复回执后复验。
- **★ 钓鱼缺陷 1（OM Export FMU）修复复验结案（2026-10-19，om `mail/009` 修复 → 我
  `mail/010` 复验收执）**：OM 根因 = **自家 clang24（wasm-ld）给 dylink.0 写子段 6**
  （target-features 声明，合法 wasm）而上游 wit-component 0.259 白名单只认子段 1–5 ⇒
  14 个 blob 全带 6 ⇒ FMU 链接必炸；上游 CI 的 clang 旧不写 ⇒ 上游无感。修法 = 产物侧
  剥离（`strip-dylink-features.py`，语义无损，挂进构建两处防回归）。**我独立复验全过**：
  剥离器自证 10/0；全树 215 wasm 干净；新产物 sha `8287589e…` 构建产物=站点副本=信中
  口供三层逐字一致（74,579,404B）；`run-export-fmu.sh` 6/0（含反向断言）；**FMI Simulator
  全链闭环**——simulator 自产 FMU（下载截获）→ fmi-simulator 装载（1232ms 识别 FMI 3.0、
  13 变量 2 连续态）→ Simulate 真跑（**1695 采样 / 51ms / Co-Simulation 1597 步 97 事件**）；
  回归抽查 omc-page 10/0。⇒ **「Open FMU 死胡同」从报告到全链恢复 <1 天**。收口账：
  OM 发信级缺陷 1/1 = 已修 + 已复验 + 结案。**根因沉淀**（「文件里对、装配态才见真章」
  新形态）：我方工具链比上游新 ⇒ 产物带合法新子段 ⇒ 上游白名单解析器不认 —— 构建自检绿
  ≠ 消费端绿，与 compile-core「修复≠发布」、v0.1.2 manifest 缺件同族：声明侧与消费侧
  之间没有对账器的地方就会在第一次真用时穿帮。
- **★ UI 071/072 WebMCP 重构终验通过（2026-10-24；`mail/072`）——全链收官**：
  - **第 4 项 onCall 计数器亲验**：CI 88/88 快照 0 变化（不上 wire 兑现）+
    全量 45 文件 499 全绿（+反向断言 10）+ callStats 四元组环形缓冲（容量 512
    溢出丢最旧/浅拷贝/setEnabled 观测暂停）+ **不记 args 红线亲验**
    （callStats.ts:9/28——args 是用户代码）+ 调试句柄挂/卸且不误删后来者 +
    server.callTool 终态后记录（默认零行为）。
  - **步骤 3 总账**：四项 × 独立提交——ARGS_INVALID 3 条快照变化 / TIMEOUT 0 /
    CAPABILITY 0 / onCall 0——**偏差表精确预测每项影响面**（068 评语模式延续生效）。
    DEVIATIONS.md 3/3 勾销 + 计数器入「观测面记录」（非偏差）+ 保真清单不变。
  - **终验总表**：步骤 0/2/3-1/3-2/3-3/3-4 + 两红修复（独立线）全 PASS。
  - **合并建议**：`refactor/webmcp-bridge` → main；合并后建议一次合并后回归
    （main 全量+关键行为抽查——合并冲突解决可能引入意外）。
  - **升级触发条件在案**（spec 决策 11）；下一步队列：OM MSL 站内化批次落地后
    form:tree 进表 + 第二引擎工具族按 provision 自然生长（Q2 裁定形状）。
  - **全链轨迹**：一轮三案 → 二轮修正版 → 三轮钉 5 → 实施（0/2/3-1/3-2/3-3/3-4
    六次验收）→ 终验。全程偏差表精确预测影响面、零 golden 意外漂移、纪律零违例。
- **★ OM JS 键上账复验 + UI wire 面裁定 A（2026-10-25；OM `021` + UI `086-ui` → 我 `093`→UI〔其槽 `087`〕/ `094`→OM〔其槽 `022`〕）**：
  - **OM `021` 复验 ✓**：`omc_web_js_sha`/`omc_web_js_bytes` 在账（部署盘现役件
    路径——files[] = 下发闭包，取下发面正确）；**我亲跑其 30 条复跑闸门 OK**；
    值与我亲测、UI 硬编码三方逐字一致（孤儿事实有产地了）。OM 侧链条闭环。
  - **UI #4 抽验 ✓**：`DownloadStore` 的 `form:"file"` 分支 + 缺件响亮拒在码
    （我抽验）；供给面 `consumer:'omc'` 筛选两条正确。工具面现 6 条（工具体
    移出名册暂存——等 wire 裁定，纪律正确）。
  - **★ wire 面裁定：A（provision 自然生长）**。判据：①能力门是诚实降级
    （三道反向断言 ⇒ `CAPABILITY_UNAVAILABLE` 响亮不冒充——比藏名册诚实，spec
    3-3 capability 信封的设计意图）；②B 名册随构建变 = wire 面成构建函数，恰是
    spec「provision 静态」要防的漂移，且藏了能力发现；③生长条件真实成立（表里
    MSL 条目已落地，非预猜）。**四条绑定**：golden 更新与注册同提交；DEVIATIONS ④
    引用我 `093` 勾销；本确认只覆盖 `omc_load_msl`（后续名册变仍逐条登记，A 不是
    免确认通行证）；能力门不许退化成静默缺席。
  - **UI 落地后我复钓两分支**：无 omc 会话（7 条 + `CAPABILITY_UNAVAILABLE` 信封）
    / 有 omc 会话（真装 MSL + 装后自检三条 + 返回体带自检）。
  - **剩余链条**：宿主 schema/投影/rebake（我 `090` 在途）→ UI 刷表 → #3。
- **★ 宿主双件落地复验 + UI 抓出 `files[]` 缺口 → 裁定补键（2026-10-25；宿主 `060` + UI `085-ui` → 我 `090`→宿主〔其槽 `061`〕/ `091`→OM〔其槽 `020`〕/ `092`→UI〔其槽 `086`〕）**：
  - **宿主 `060` 复验全过（亲测）**：17 packs（omc `consumer:["omc"]` ✓ + MSL 全字段 ✓）；
    `forge-catalog.py --selftest` 我亲跑 40/0（含 ③ 装配器落位缺陷两修的正反例）；
    **isui.ren 线上表亲验 17 packs**（UI 已刷新部署 + 落位对齐 `assets/msl/`，200）。
    其 ③（`stage_upstream_bytes` 一律铺 `assets/forge/` ⇒ 站内相对 url 改为照 url 铺）
    与 ④（browse Entry 透传 consumer/kind/role）两缺陷修法收下——「同一条交付路径
    两个口径」与 llvm-wasm 那次同族（声明与消费之间没有对账器）。
  - **★ UI `085-ui` 抓出真缺口（挡 #3 删硬编码）**：omc 条目**无逐件 sha**——JS 胶水
    件表里无 sha（UI 硬编码 `56c399bd…` 我亲测逐字一致但**无产地**）、表 `size` =
    目录和（74,735,455，含非下载的 `.d.ts`）≠ 下载闭包（两件和）。宿主「逐件 sha
    走产物自证」在**运行期消费端够不着**——只有表能带过去。
  - **裁定：采 UI 方案 A——表补可选键 `files[]`，五条绑定**：①可选、`form:"tree"`
    专属（`form:"file"` 条目 sha 即文件 sha，MSL 无缺口——UI #4/#5 **即刻解锁**）；
    ②值 = **下发闭包清单**（消费者要拉的文件；`.d.ts` 等非下发件不列 ⇒ files-sum
    ≠ size，两者语义不同且都有用）；③**产地纪律**：逐件 sha 唯一产地 = 生产者台账
    （OM `omc_web_wasm_sha` + 待补 JS 键），宿主装配**投影**进表、不另算——我 `056`
    「逐件 sha 从产物自证」的运行期形态；④`size` 语义不变（目录和，R14 不变量），
    下载预算 = Σ files[].bytes 消费端自算；⑤缺省兼容（无 files[] 的 tree 条目合法，
    llvm-wasm/pyodide 现状不动）。方案 B（硬编码长期持有）**否**——D1 线数周灭的
    例外不能制度化。schema 产地 = 宿主落地，本仓随后同步 `port/README.md` 副本。
  - **OM 待补一件**：台账加 JS 胶水件键（sha + bytes，fail-closed cmd）——files[]
    投影的产地（我已亲测值：`56c399bd…` / 56,586B）。
  - **落位教训收编（recipes/msl.md）**：**落位以表 `url` 为准，示例不是规范**——
    我的示例「如 `msl/`」被读成路径规格，UI 首镜像 `public/msl/` 与表 url 错位。
- **★ 三方回信全到 + 复验 + 两裁定（2026-10-25；宿主 `058` / UI `084-ui` / OM `018` → 我 `087`→OM〔其槽 `019`〕/ `088`→宿主〔其槽 `059`〕/ `089`→UI〔其槽 `085`〕）**：
  - **复验全过（亲测，非采信口供）**：①OM 三件——兄弟目录迁移（`assets/omc/` 已删、
    `assets/msl/` 落位、迁移后 sha 复测一致）/ 出表（字段逐项符合指导，**我亲跑宿主
    校验器双模式均 `ok`**）/ release 双资产（`gh api` 核 digest，GitHub 算的 = 第三方
    复核）；②宿主——omc 条目上表（16 packs，字段如提单，`version:"unversioned"`
    诚实占位）+ **R14 我亲跑自证 40/0**（正反两例）+ `provision-omc.sh` 自证 4/0
    （含入口侧兄弟目录拒收反例）；③UI——isui.ren 用户路径 MSL 镜像 200 /
    字节精确 / sha **六方逐字一致**（OM 台账 / 盘前后 / GitHub digest / 线上）。
  - **裁定一（命名申辩：采）**：MSL 条目 `name` = **`modelica-standard-library`**
    （OM `mail/018` §4 申辩成立）。判据：catalog 名携带上游身份是既有先例
    （llvm-wasm / pyodide / octave-forge 包名）；表是公开机器产物，通用缩写不可检索；
    名字将成 deps 边目标与安装键——现在改一个串，将来改不动。OM 表已按全称写，
    无需改动。
  - **裁定二（omc 引擎条目 consumer）：`["octave"]` → `["omc"]`**。宿主条目按缺省
    走了 octave——缺口在我 `056` 提单漏指定 consumer。判据：**consumer = 条目服务的
    引擎车道**——omc 引擎是 omc 车道的运行时（与 MSL 同栈 `["omc"]`）；llvm-wasm /
    pyodide 是 octave 车道栈（`["octave"]`）不变；omc 车道栈统一 `["omc"]` 让缺省
    octave 市场面不被第二引擎条目污染。今日零破坏（UI 筛选缺省 `'all'`、
    EngineAssetResolver 按 lane 读不经 consumer——亲查其源码）。已请宿主改装配器
    一个数组 + rebake（`088`）。
  - **切换条件修正（给 UI）**：isui.ren 镜像表**仍 15 packs**（omc/MSL 条目未到——
    宿主 rebake 的是自己三站，UI 的表要它自己刷新部署）。UI #3（删硬编码）的生效
    条件 = **其站镜像表里出现 omc 条目**，不是「宿主装配完」。
  - **剩余链条**：宿主改 consumer + 并入 OM 表（校验器我已亲跑 ok）+ rebake →
    UI 刷新镜像 → UI #3/#4/#5。
- **★ MSL 收口两件闭环 + UI 三问裁定（2026-10-25；OM `mail/016` 收执 → 我 `mail/084`→OM〔其槽 `017`〕/ `085`→宿主〔其槽 `057`〕/ `086`→UI〔其槽 `084`〕）**：
  - **字节对账 ✓**（收口件一）：本机实测 OM 部署盘站内 zip 的字节数 + sha256 与其
    `mail/016` 资产身份**逐字一致**（fail-closed 锚 = 站内 zip 自身字节；复跑命令在
    `recipes/msl.md`）。
  - **对在档口径的两处修正**（判据跟着实测走，出处 OM `mail/016`）：①对账口径 =
    **版本锚 + 站内字节**（安装形状重打包 ⇒ 与 GitHub 源字节必不等——修正 2026-10-21
    在档的「认字节」表述）；②条目形态 = **`form:"file"`**（单 zip 交付、解压在运行期，
    非当时推断的 `form:"tree"`）。
  - **UI 三问裁定**（UI `083-ui` → 我 `086`）：**A1** omc 引擎条目**进表已裁**
    （宿主 `056` 提单、llvm-wasm 同款 `kind:"engine"`+`role:"toolchain"`；UI 删
    硬编码的生效条件 = 条目落地）；**A2** MSL **出表**（出表方 = OM，字段级指导
    已发；UI 预备 `consumer:"omc"` 供给面读取 + 下载入口 + WebMCP 工具族）；
    **A3** 挂载语义**不入 `consumer` 轴、不加 schema 键**——归消费端车道适配器的
    操作知识，载体 = `recipes/msl.md`（权威配方，含 `MODELICAPATH` 反例）+ 条目
    `note` 指路。判据：轴语义 = 「哪面可用」（包含），不是「怎么装」；§2 判决
    不引入新字段；挂载事实已被实测翻案过一次（`.d.ts` 契约不成立），焊进 schema
    会让下次翻案变成 schema 变更。
  - **★ 站点落位硬约束**（新裁定）：MSL zip **不许落引擎条目的树目录**（引擎
    `form:"tree"` 的 size = 该目录字节和，混入即虚胀引擎闭包预算）——落**兄弟目录**。
  - **配方落地**：`recipes/msl.md`（llvm-wasm 同款消费侧摘录 + 挂载语义权威载体 +
    字段级出表指导 + 渠道待办）。
  - **渠道待办**：OM 挂 release asset（引擎产地渠道线同模式）→ 宿主装配进
    forge-catalog → UI 镜像 + fail-loud（期望值 = OM 台账键）。
- **★ 最终全链复钓 PASS + Einfacht 同步（2026-10-25；`mail/083` + knobs/registry 升级）**：
  - **全链 PASS**（isui.ren 用户路径，单次浏览器会话）：菜单第 2 次尝试 ALIVE
    （冷节点长尾=平台物理）/ URL 单前缀 ✓ / 200 + gzip 20.3MB 传输 /
    OPFS 74,579,404B 精确 / **sha 五者逐字一致**（线上字节/METADATA/OM产物/
    CI 锚/OPFS 落盘字节）/ manifest 在。**产地渠道线 056→083 完整闭环**。
  - **Einfacht 更新同步**（用户点令）：上游 tip `1b753f3`（issue #21 相位旋钮）——
    `knobs.py` 新增 REFLECT_PHASES + `registry.py` PHASES 焊死改为 BUILTIN_PHASES
    + 可扩展 phases()/phases_problems()。两文件已拷贝同步，全套闸门 pre-commit
    路径 ran 7/0/0 全绿。其余 7 个机制文件逐字节一致（无需同步）。
    **本仓暂无自定义相位需求**（commit/start-of-work 够用），旋钮已可用但不启用。
- **★ UI 079/080 + 复钓（2026-10-25；`mail/081`）——边缘修好 + 新根因：URL 双重前缀**：
  - **边缘修复确认有效**：curl HTML 15/15 全 200（前 2/15 挂起→零挂起）；浏览器菜单
    第 1 次尝试即活（前 0/3）；长尾仍在（10.7s/22.4s 各 1 次——多节点缓存冷启差异，
    EdgeOne Age 序列互异吻合）。
  - **★ OMC 下载线上 404——根因 = base path 双重前缀**：浏览器实测请求 URL
    `https://isui.ren/repo/Octave/repo/Octave/omc/OpenModelicaCompiler_bg.wasm`
    （双重 `/repo/Octave/`）→ 404；正确路径亲验 200 + application/wasm。
    根因方向：Astro base = `/repo/Octave/` + DownloadStore.resolveUrl 叠加了一层。
    dev 没踩到因为 dev base = `/`。修法：resolveUrl 感知 BASE_URL 或读
    `<meta name="site-base">`（UI 仓已有此 meta）。
  - **.gz 传输面确认**（用户纠正口径）：用户路径走 gzip → Content-Encoding: gzip /
    21,333,875B（≈20.3MB）✓；heart 083 的 .gz + Range 旁路上线（20,895,435B
    预压缩件 206 Partial Content 格式亲验）——DownloadStore 将来可改分片下载。
  - `mail/081` 已投 UI（紧急修复信）。
- **★ UI 077 最终复验（2026-10-24；`mail/078`）——sha 逐字一致 + 新发现线上弹窗不弹**：
  - **通过面**：isui.ren 用户路径 omc wasm 200 + Content-Type: application/wasm ✓
    + 74,579,404B 完整下载 ✓ + **sha 四者逐字一致**（线上字节 / KNOWN_ENGINE_METADATA / OM 产物 / CI
    校验锚——完整指纹见 UI 仓 `077`/`078` 信，非本仓台账面）+ .gz 预压缩对上站 ✓。
  - **★ 新发现（发信级）**：**线上 More Options 菜单弹窗不弹**——三组独立浏览器
    测试一致（isui.ren + GitHub Pages 直链）：节点数不变/零 console error/零弹层
    DOM / lane-choice-group 不存在 ⇒ **引擎架构选择和下载入口对线上用户不可达**。
    排除面：同一 App.D7owsQ-e.js 产物本地 preview 弹窗正常 / dev main 正常 /
    JS 产物有引擎菜单代码 / 无 404 chunk。诊断方向：CORS/CSP/COI 差异或
    条件渲染分支。**比 OMC 200 更紧急**。
  - 用户纠正两轮：最终用户走 isui.ren 反代（不是 GitHub Pages 直链）+ gzip——
    sha 亲验按正确路径完成。
- **★ UI 073/074 处理（2026-10-24；`mail/075` → ui + `mail/014` → om）**：
  - **073**：WebMCP 重构合并 main（ebb9f7b）+ 合并后回归绿（499/88/17 闸门）——
    **线正式关闭**。
  - **074**：线上 OMC wasm 404 根因链我亲验（404 ✓ / OM PRIVATE ✓ / asset 在
    v0.1.0-wasm32 ✓）。**产地渠道三选一已投 OM mail/014**（附我的裁定：①
    public release asset 最优——产物身份已在只是可见性问题）。
  - **UI 越界处置**：上传 wasm 为 OM release asset **保留**（产地正确、是方案①
    雏形）但纪律裁定「跨仓动作须先走信请求授权——结果对了程序错了记档不追
    下不为例」；试图转挂 UI 仓 public release 被用户当场制止（定性「造假
    seam」正确）——记档不追。
  - **断言不降级**（CI 红着比绿着缺件诚实——b6b44d5 改进不撤）。
  - **球在 OM**：裁决三选一。
- **★ Claude 二轮复审的两处实证补查（2026-10-24，支撑终版 spec 应改项）**：
  ① `getWorkspace` 亦经 `_enqueueTask`（`ws_` 前缀任务，EngineSupervisor:580）——
  并发安全覆盖 workspace 读；`executeCell` 有独立 `_isRunning` 互斥（另一层守卫）
  ——「同一 tick 两 call」golden 用例有据。② **eval 可经 `pkg install`/`urlread`
  走到 install 同等效应**（宿主 pkg shim `__web_pkg_fire__` → `OctaveAssets.install`
  + webnet 桥出网）——故 eval 的 effects 必须保守标 `sandbox-escape`，「装包不该
  被 eval 表达」的剪枝论据需保留但承认 eval 本身有该效应面（终版 spec 已写）。
- **★ UI 069 步骤 3 第 3 项 CAPABILITY_UNAVAILABLE 验收通过（2026-10-24；`mail/070`）**：
  分支 @ `63da3d5`。亲验：CI 88/88 **快照变化 0 条**（六旧工具不声明门 ⇒ 零偏差
  红线守住——golden F 组全绿即证）+ 全量 44 文件 489 全绿（+反向断言 7）+
  capability 门位置（ARGS_INVALID 后/超时前，层次专门用例钉死）+ 软依赖模拟
  路径（omc 无 catalog ⇒ supervisor 软依赖模拟懒加载失败/恢复放行）+ 零偏差
  红线三条全过（provision 缺失 Unknown tool 原文案/旧守卫一字不变/静态名册）+
  信封形状亲验 + capability 抛错落 catch-all 不吞。**进步骤 3 最后一项 onCall
  内存计数器**（不上 wire/不改 get_system_state/四元组环形缓冲/调试句柄/
  默认零行为）。
- **★ UI 067 步骤 3 第 2 项 TIMEOUT 验收通过（2026-10-24；`mail/068`）**：
  分支 @ `35530cf`。亲验：CI 88/88 **快照变化 0 条**（066 预告「120s 内不触发」
  精确兑现——各偏差项影响面差异被偏差表精确预测）+ 全量 43 文件 482 全绿
  （+超时反向断言 9）+ raceTimeout 在 machine 层（dispatcher:31，supervisor
  一行未碰）+ 计时含排队（B.1 第三条路如实首版）+ 缺省 120_000/timeoutMs
  覆盖（defineTool:32-36）+ **信封措辞 spec B.1 原文逐字** + 超时不取消底层
  反向断言实测 + DEVIATIONS ②确认。**进步骤 3 第 3 项 CAPABILITY_UNAVAILABLE**。
- **★ UI 065 步骤 3 第 1 项 ARGS_INVALID 验收通过（2026-10-24；`mail/066`）**：
  分支 @ `47b09c8`。亲验：CI 88/88（快照变化 **3 条全部缺 required 面**——
  `git diff` 亲核 6 行 = 3 对与偏差表精确吻合）+ 全量 42 文件 473 全绿（+
  反向断言 14）+ 强转放行面守住（code:42 旧快照绿/consumer:5 透传）+ 空串
  两道守卫并存（旧守卫原文案非 ARGS_INVALID）+ DEVIATIONS.md 建表+保真清单
  单列。类型关放行可强转/enum 非串放行——spec「校验器宽松只拒明确违规」
  精确落地。**进步骤 3 第 2 项 TIMEOUT**（120s 含排队/timeoutMs 覆盖/
  「仍在排队或执行中勿盲目重试」措辞/偏差表第 2 项）。
- **★ UI 063 步骤 2 骨架迁移验收通过（2026-10-24；`mail/064` 已投）**：
  分支 `refactor/webmcp-bridge` @ `7bd482a`。亲验：CI 对拍 88/88（83 快照零
  mismatch）+ 全量 41 文件 459 全绿（基线 450 + 新增 9 = isolation/channels/
  compile-gates）+ Unknown tool/catch-all 原文案逐字复刻（dispatcher:52/:60
  亲验）+ require 惰性回退保留（ctx.ts 7 处）+ 骨架布局（Plugin 薄壳 75 行 /
  server 31 / dispatcher 63 / defineTool 36 / tools 六文件 / channels 三文件）+
  @ts-expect-error 8 处 + fake-channel 契约测试 + isolation 反向断言。
  **偏差表空、全量零差异——步骤 2 验收达成**。UI 如实声明子代理三断+主会话
  收尾只改测试路径——采信。**进步骤 3**（四项新行为逐个提交：ARGS_INVALID →
  TIMEOUT → CAPABILITY_UNAVAILABLE → onCall 计数器，每项偏差表勾销）。
- **★ UI 060/061 回信 + 步骤 0 验收（2026-10-24；`mail/062` 已投）**：
  - **060**：fix/integrity-reconciliation 已合并 main（`64dd4ef`/`a498292`），分支
    已删，wayfinder map #4 与 spec #19 关闭——**两红线终结**。
  - **061 步骤 0 golden master 录完**：分支 `refactor/webmcp-bridge` @ `969f81a`，
    88 用例 / 83 快照条目对旧实现录制（CI 对拍两遍绿）。**亲验通过**：CI 模式
    88/88 全绿；快照关键面抽查——crashed 走 catch-all（原文案）/ run_cell 吞
    异常为 resource / booting 排队后返回 / unknown tool 原文案两通道一致 / 
    A/B/C/D/F 全覆盖。**键序方法论认可**（JSON.stringify 载体绕 vitest 排序）。
  - **UI 录的「旧实现意外行为 10 条」极有价值**——尤其 #2（callTool 无 crashed/
    failed 前置守卫，靠 catch-all 兜）和 #6（非法类型大量被强转放行=ARGS_INVALID
    偏差面）。步骤 2 骨架迁移不改任何旧行为（全量零差异）；`require` 惰性回退
    语义逐字不动（UI 建议正确、我采纳）。
  - **进步骤 2**（骨架迁移 A+C 半+B 两样，验收 = 全量零差异、偏差表空）。
- **★ 两红复钓全绿（2026-10-23；`mail/059` 已投）——UI 055 全量整改整体通过**：
  - **红 1 Plots 接线 PASS**：主钩（终端真实通道 plot → 面板内 img 可见 + 零
    TypeError）+ **反向铁证严格版**（先激活 tab 再画两张 → blob src 两次不同
    `dff96c…`→`8dee50…`——事件真到面板非时序运气）。UI 058 根因修正采信（断点①
    URL 读取时机/img 未挂 DOM 读空串；断点② `p5canvas.js` 重赋值 window.OctaveP5
    致对象级标记失效——比我的候选更底层；页面级总线+函数级标记是正解）。
  - **红 2 徽标 PASS（两姿势）**：截断→重开菜单 = ⚠ Corrupted（✓ 消失）；
    XOR+reload 新会话 = ⚠ Corrupted + integrity 真值 `{corrupted, downloaded:true}`
    ——「只看 integrity 不叠 downloaded」口径正确。
  - **观察（#15 留痕）**：同会话 XOR 不 reload 仍 ✓（缓存指纹只含 size）——UI 已
    留痕，跨会话兜住；本轮按 057 不要求修，方向（size,mtime 或抽样哈希）记档。
  - **六判据终表：A/B/C/D/E/F 全 PASS ⇒ 建议合并 fix/integrity-reconciliation**。
  - **工装教训**：后台长测试无输出（10 分钟无 stdout）→ 用户点令改前台直测，20 秒
    出结果；前台脚本带步骤日志+硬上限。另：`getDirectoryHandle` 不接受多级路径
    （逐级取）；astro-dev-toolbar 拦物理点击（走合成输入/force）。
- **★ 修两红开工信 + WebMCP 方案书（2026-10-23，用户点令；294a1a1）**：
  - **mail/057 已投 UI**：先修两红（现成 bug，与 MCP 重构无关可立即动工）——
    红 1 断点定位（接线代码在/断点在源头不发事件，两候选：p5.show 钩子链断/
    两实例不同源）+ 红 2 修法方向（HeaderBar 消费 integrity 三态）；修完只复钓
    两钩子（其余四判据无需重跑）即合并。
  - **WebMCP 重构方案书已出**（specs/2026-10-23-webmcp-redesign-proposal.md）：
    **三案全录不混合**（用户裁定：不按我的混合推荐，三个平等呈外部 Claude 审，
    修正版回来再落实）；**匿名口径**（可含 Octave 相关、无项目地址/仓库名/内部
    路径——自查 grep 干净）；含三案 Interface/不变量/seam 判定/trade-off 全文 +
    对照终表 + 共同前提修正（插件测试已存在 300 行——「零测试」过期）+
    四问审阅请求（含第二引擎已确定会来是否改变天平）。
- **★ 复钓验收终判（2026-10-23；`mail/056` 已投）——4 PASS + 1 FAIL + 1 部分**：
  六判据 A-F 三路并行真浏览器复钓完毕。**硬面全兑现**（离线五件套请求 0 /
  完整性闸门 ENGINE_CORRUPTED+零重下+fail fast / Mock 根除 Failed 态零 42 /
  getAssetsPort 复活 15 packs 含反向断言 / 假 seam 清扫全过 + R1 中文噪音根除）；
  **两红线挡合并**：① **A=Plots 接线「代码在、行为断」**（三测一致图困死
  staging；反向验证坐实非时序——先激活 tab 再画仍空；接线代码亲验在
  appContext:79+GraphicsSink:147——断点在源头不发事件；Notebook 走 lastFigure
  拉取与 sink 事件流不同源）② **C 徽标子项**（「⚠ 已损坏」渲染态不存在——
  HeaderBar:40 只取 downloaded 布尔，integrity 三态引擎层正确产出被 UI 面丢弃）。
  两红均不在六条留痕裁量点内（新缺陷）。裁量踩中 #6/#15 与留痕一致。
  性能面：五件 sha 复验 603-659ms UI 不卡（rAF 31 帧）+ 断网冷启 1.2-1.35s。
  **合并建议：修两红后复钓两钩子（现成）即可合并，其余六判据无需重跑**。
- **★ 复钓验收执行中 + MCP 重构方案排队（2026-10-23，用户点令）**：
  - **复钓 spec 已获批执行**（specs/2026-10-23-ui-remediation-reverification.md，37a98ca）：
    三子代理并行（A+F 终端面 / B+C 离线完整性 / D+E 防线面）——**D+E 已双 PASS**
    （Mock 回退根除 Failed 态零 42 + getAssetsPort 复活 15 packs + 反向断言复刻死缝
    验证分级吞错语义 + 裁量点 #6 踩中与留痕一致）；A/B 两路在跑。
  - **MCP 重构方案（用户点令，两轮 design-it-twice）**：三路审计回归后用
    codebase-design skill 出 MCP 重构方案——**第一轮**：三路复钓回来后一次；
    **第二轮**：等那轮所有子代理回来后再一次（用户原话「很繁琐但 UI 的屎山
    真的太多了，不好好设计永远是大便上堆砌大便」）。对象：webmcp 插件
    （547 行——WebMcpPlugin 500 行单类塞双通道挂载/静默握手/工具调度/services
    四概念）+ MCP 面（工具暴露/agent 桥/上下文 API）的 seam 设计。
- **★ UI 双引擎深挖增补（2026-10-22；`mail/055`）——三个新实锤**：
  - **★ `getAssetsPort` 方法不存在**（亲验：appContext:56 调用、Plugin 0 处定义）⇒
    catalog 动态路径**整条死代码**（TypeError 被 catch 吞、零网络请求零报错、永远
    fallback 手抄坏串侧）——**我 053 裁定的「优先 catalog 动态」从未生效：裁定面
    与实现面之间又一条无对账器的缝**（且两层都要修：方法缺失 + catalog 无 omc 条目）。
  - **拼接 sha 定性修正**：校验被绕过、下载照样成功（per-file 真值恰好过检）——
    manifest 顶层 integrity 字段 = 永远不可能被真实哈希命中的谎言值，无闸门会发现。
  - **★ sha 台账纯装饰**（实测：wasm 首字节 xor 0xFF → reload 徽标仍 ✓）——
    checkPhysicalStatus 只查 size>0，manifest 里正确的 per-file sha 无任何启动对账
    消费者；与 054 P0-3 同根（修法同一个钩子：对账升级为 size===expected + sha 复验）。
  - **修正我 054 一处**：假版本号 1.25.0 **DOM 不可见**（用户可见面干净）——只撒进
    机器面（manifest 键 + 代码常量五处）。正面：OMC 下载 5 秒稳定精确 / 物理 reload
    对账正确（stale manifest 延迟收敛 5 秒自愈非漂移）。环境坑备忘：chromium 下载期
    高频 evaluate 轮询 DOM 触发 SIGTRAP（两枚 coredump 在案）——改轮询 OPFS 即稳。
- **★ UI 重构验收全轮（2026-10-22；五路钓鱼 + 双架构审查；`mail/054` 已投）**：
  - **★ P0×3**：① Plots 面板死 API（`PlotCanvasPanel:8` 调 `graphicsSink.onFigure`
    不存在——两路独立实锤+亲验；引擎真出 PNG 断在 UI 消费端，D10 修复半态）；
    ② **spec②离线零流量不成立**（octave.js 先打网络再降级 / assets-manifest 永走
    网络且吞错照常 idle——「引擎能起 ≠ 引擎完整」/ build.json 同状；页面级断网
    本身开不了）③ **截断反钓失败**（1 字节 wasm 无校验静默重下覆盖，sha 记了
    从不复验——半截契约）。
  - **★ 架构审查「重构半真」**（两路独立）：删 StorageService 当场造 lib/ 两个
    重导出壳（新假 seam，亲验）+ DownloadStore 40% 死接口（unit() 零消费者亲验）+
    **聚合 sha 三产地**（128hex 坏串只是其一）+ 手抄表无对账（omc 缺席 catalog
    ⇒ 手抄侧单边）+ 双真相无收敛器（removeEngine 双边暴力删自证分裂）；
    **★ 生产静默 Mock 回退**（EngineSupervisor:235-238 亲验——bridge 失败生产
    boot Mock 引擎永远 ans=42 无告警，吞 404 同类）；OMC 桥 90 行走私进
    WasmEmbedAdapter + engine→ui 倒挂（toastService）；ProjectWorkspace 透传层
    转世 + adapter.fs 穿透（亲验）；OmcShellPanel 读无主 `window.__omc`（D9 同构）。
  - **PASS 面存档**：P1 下载校验链成立 / **P3 物理对账兑现（spec③）** / D6
    browse() 合流闭环（13/13 描述真渲染）/ U-3 includes / role 渲染 / 三语主体 /
    265 测试亲跑。**spec 四不变量对账：2/4 成立 + ④ 半成立**。
  - P1 级：DX1 错误无 Toast 无机器码 / DX2 坏 catalog 永转 / DX3 dev lane 资产
    三缺（双源不一致）/ R1 终端中文噪音旁路 i18n / 手钓两尾巴（128hex 入
    manifest + 1.25.0 假版本号持久化显示）。
  - Deepening 建议 Strong×5 已随信（删手抄表+intake 断言 / 聚合 sha 语义 /
    删壳+死接口 / 删 Mock 回退 / OMC 桥抽离）。修好后复钓三钩子（离线/截断/Plots）。
- **★ UI 重构言行复核 + 手钓（2026-10-21，四轮子代理模型侧连挂改前台亲钓）**：
  - **言行一致性**：重构主体真落（EngineAssetResolver 接入 WasmEmbedAdapter:99 的
    withLocalAssets / StorageService 物理删除 / browse() 合流 / 占位符清）；**两个尾巴**：
    ① `KNOWN_RUNTIME_METADATA` 的 `omc@1.25.0` **顶层 sha256 = 两 sha 拼接的 128hex
    坏串**（`DownloadStore.ts:57`——files 里 wasm/js 两 sha 是官方真值，wasm
    `8287589e…` = OM 10-19 新产物亲验同源）；② **1.25.0 是编造版本号**（omc 真返回
    "-rust"，D8 假历史同族）。
  - **手钓行为面（真浏览器三连）**：**OMC 下载链真通**（选 OMC → Download → OPFS
    `downloads/engine/omc/w32/` 两文件字节精确：wasm 74,579,404B + js 56,586B）；
    **manifest 记账正常**（`engine:omc@1.25.0:wasm32` + files 明细）——但 ★★
    **manifest 顶层 sha256 = 128hex 拼接坏串原样入库**（未来任何用 manifest.sha
    对账/重验的面全踩坏串 = sha 语义污染，发信级）；★ **冷启动状态徽标 ✓ 来自
    物理 stat 而非 manifest**（manifest 空时徽标已绿 = EngineAssetResolver 物理探针
    真落 = spec 不变量③兑现，正面）；★ **假版本号 1.25.0 持久化进 manifest 键 +
    UI 显示**（发信级）。
  - **拼接坏串的触发路径精确化**：omc 下载走 downloadEngine（engine 路径）成功——
    KNOWN_RUNTIME_METADATA 的 :586 兜底分支（omc 不在 catalog 时）未被主路径踩到，
    但 manifest 记账取了 known 顶层坏串 ⇒ 污染入口是**记账**而非下载校验
    （校验比对用 files 真值）。
- **★ UI 051/052 合答（2026-10-21；我回信 `mail/053` + 宿主提单 `mail/056`）**：
  - **UI 051（OMC 线上 404 + 硬编码 sha 自首）**：404 根因 = gitignore `*.wasm` 漏杀 +
    部署流水线没拉 OM 产物；DownloadStore 两个手抄 sha（`8287589e…`/`56c399bd…`
    = D1 第四层，自首）。**Q1 裁定**：OMC 产物**产地 = OM 仓部署盘**（同源托管，
    与 llvm-wasm 供给同款——lock 记 URL+sha、站点副本可重建）；UI 部署流从产地同步，
    绝不进 git 树。**Q2 裁定**：omc 进 forge-catalog 走 llvm-wasm 同款
    **kind:'engine' + role:'toolchain'（不加新值——UI 想要 role:"compiler" 已回绝）**；
    出表方 = 宿主装配器，字节从 OM 产物自证——**提单已投宿主 mail/056**。
  - **UI 052（spec.md 全站重构规范审阅）**：四不变量（上游只读/离线零流量/物理 stat
    唯一事实/深模块）**全对**；EngineAssetResolver（Scoped Fetch Proxy 瞬态拦截）
    方向对——**三点技术确认**（并发代理栈防覆盖/Content-Length 别省/import.meta.url
    绝对 URL 匹配）；两处修正（OMC 产地 = OM 盘非「内容仓 public/」；octave.build.json
    **顶层不拆**——arch 是条目级字段，variant 是 lane 内部署事实不进表）。
    **结论：无阻断级异议可进实施**；Phase 2 断网实测（网络请求严格 0）通过后我复钓
    （离线零流量 + 物理 stat 两个钩子）。
  - UI 的假状态自曝（「下载了 master 仍全量走网络」/「32 位下载 64 位启动」）= spec
    §1 缺陷全景——钓鱼 D2/U-5 的深化版，它的自诊准确。
- **★ UI 049 全量结案收执（2026-10-21；我回执 `mail/050`）——U/D 全表 + 025 三层闭环**：
  - **静态三验全成立**：①官方字节——llvm tar sha 与上游 lock **逐字一致**
    （[[llvm_bundle_sha]]），symlink/19.1.0 已删；②假 sha 根除——占位符无痕，
    KNOWN_RUNTIME_METADATA + 无权威指纹响亮抛 FLAVOR_UNAVAILABLE；③role 三层拦截
    （Plugin/Adapter/Modal 源码亲读）+ browse() 正门对接（mail/030 出口）。
    **265/265 亲跑**（31 套件）。
  - **双引擎复钓两轮（八次工装迭代点中 menu-item-choice）**：D5「不再静默」
    **在 dev 真环境兑现**——console 双 warn（OMC import failed / bridge failed in
    dual engine mode）亲收；omc_getVersion undefined（OM 半未起）但上报链在。
    **★ dev 边界记档**：`import(public/omc/…js)` 在 vite dev 下 HTTP 500
    （vite 明文 public 文件不能被源码 import）——dev-only，preview 形态 import 走
    原生 ESM 直 GET 能过（其 E2E 即此理）；修法方向两选（URL 参数绕缓存 / 胶水进
    src 打包）或 README 明说「测双引擎用 preview」。
  - **收口账翻面**：UI 从「缺陷大户」（D1-D10 + U1-U7）到「修复标杆」（全表闭环 +
    27 封历史信主动归档审计 + 假 sha 根治）——一轮钓鱼一轮修复一轮复验的完整生态循环。
  - MSL 预备登记 + 不私造条目（纪律正确）；OM 落 zip 后经我收口进表。
- **★ OM 012 两问答复收执（2026-10-21；我回执 `mail/013` + 转呈 UI `mail/026`）**：
  - **A1 MSL 会站内化**（OM 下个产物批次，判据先行）：`site-omc/assets/omc/
    msl-4.1.0-maint.om-<上游版本串>.zip`，**字节指纹我从 GitHub 源复算与 OM 口供
    逐字一致**（20,362,007B；完整 sha 见 `mail/012` §A1——**上游字节不在本仓台账
    面**，站内化落地后若要进事实再量产）；OM 口供里的短 sha 是版本串非字节 sha
    ——站内化对账认字节。官方管道 `omc_vfs_load_zip` 现成（一次 fetch + 调用 =
    离线装库）。落地后 OM 回信 ⇒ 我做收口两件（字节对账 + form:tree 条目指导，
    与 llvm-wasm 同判据）。
  - **A2 进度钩子「半只」**（源码级如实）：`omc_enable_progress_sink()` +
    `__omcReportProgress(permille, phase)` 在产物（亲验 .d.ts 导出面）；装库/
    编译阶段有真 permille（`permille=-1=不定`——上游自带「不伪造百分比」语义）；
    **simulate 主链 0 上报点**（`simulate_fn.rs` grep 亲跑 0 命中；PHASE_SIMULATE
    常量在、无调用点——上游缺口，OM 不动上游源的边界正确）。⇒ **UI 的不定进度胶囊
    对 simulate 是终局形态不是过渡**。我 018 Q3 的 CustomEvent 裁定按在役形态
    修正为 **SAB 控制块 + 宿主 timer**——判据跟着实测走。
  - **答复已转呈 UI**（026，含亲验注记）；010 复验收执 OM 收讫（双侧收口账对齐）。
- **★ 宿主 054 pyodide 补标（我回执 `mail/055`）——kind/role 线终局**：15/15 条目
  role 齐（13 package + llvm-wasm toolchain + **pyodide language-bridge（Q1 词表
  三值首用）**）——亲验分布成立；pyodide 五套零红（闭包未碰坏）。**四天闭环**
  （047 提单→050 schema→052 引擎上表→053 漏标→054 补齐）：schema 产地 + 语义
  副本 + 表数据 + 装载器判据四方对齐，零硬编码名字判断。我 024 给 UI 的
  「pyodide 过渡期提醒」作废——它接表直接按 role 渲染即可。
- **★ UI runtime bundle 取证（2026-10-20，我 `mail/025`）——三层问题，最重 = 假 sha**：
  UI 45d9850 补投送面（D3/U-4 方向正确：public/omc 引擎字节 + forge tarball + runtimes）
  但取证发现：① **DownloadStore 对 toolchain 运行时的 sha256 是占位符字符串**
  （`${ref.name}-${ref.version}-sha`——下载核验在该路径被自废，字节换了也不红；
  bytes 也是粗略常量 36700160 vs 实际 34,694,190 = D1 第三层）；② **双版本名 symlink
  指向同一字节**（6.0.12 → 19.1.0——版本语义不可辨；19.1.0 是上游 LLVM 版本串，
  现役契约不存在，其 048 引用失真的根源即此）；③ **字节非官方发布件**
  （UI 仓 tar 实测 sha ≠ 官方 v0.1.3 [[llvm_bundle_sha]]；20 件 vs 18；manifest
  generated 时间戳与宿主部署盘同——疑似重打包）。修法方向信里给了（真 sha 从
  tar 内 manifest/文件实测；一个版本一个文件；字节对齐或定新号）。
- **★ 宿主 052 引擎条目上表（我回信 `mail/053` + 转 UI `mail/024`）——统一引擎清单
  两条件齐**：站点表 llvm-wasm = `kind:"engine"` + `role:"toolchain"` +
  `arch:"w64"`（lane 值，从 lanes.js 读非手抄——亲验逐字段成立）；13 包带
  `role:"package"`；`install('llvm-wasm')` NOT_INSTALLABLE 新文案亲测；pyodide 经
  symbolic 闭包装载不受影响。**arch 豁免三处判据配套**（宿主九套零红）：端口校验器
  词表补站点档名 / R10 豁免 engine / loader arch 硬闸门豁免——**w64（lane）vs
  wasm64（架构）两词表的坑**，宿主裁得准：「楚河汉界管的是要 dlopen 进宿主的 .oct，
  引擎是编译现场输入」——我已抄同款口径进语义文档。**★ 一处漏标（我报宿主 053）**：
  **pyodide 条目 role/kind 均为 None**（装配器透传只盖了货架包+llvm，漏了 pyodide
  tree 条目）——行为面无恙但「表上自描述」少一角，应补 `role:"language-bridge"`
  （Q1 裁定归属）。已提醒 UI 过渡期按 form=tree+installLayer 判断（024 信）。
  **UI 切换说明已转**（024：引擎条目形状/逐件 sha 从 build.json/role:toolchain 不渲染
  装载钮/NOT_INSTALLABLE 两码接 D4/pyodide 过渡处理）。
- **★ 宿主 050 三结收执（2026-10-20；我回信 `mail/051`）——047/048/049 全闭环**：
  - **亲验全成立**：schema 新键 **kind**（src/pre/engine，engine 的 arch=lane）+
    **role**（package/toolchain/language-bridge）双键落地（entry properties 亲读、
    enum 钉死）；校验器自证 **57/0** 亲跑；installLayer 两路文案（NOT_INSTALLABLE /
    LAYER_NOT_IMPLEMENTED）+ 8761 亲测新文案原文；C-2 勘误标记在其 STATE 亲见。
    「表未升级按 name 兜底」两层设计——UI 不等 emit 就能拿正确文案。
  - **我侧待办全清**：① **--emit 出 role**（13 包恒 `role:"package"`，自证 45→47/0，
    +2 正反断言）；② port/README 副本同步 kind/role 语义与记录形状示例；
    ③ 勘误宿主 §⑥「llvm 台账指 v0.1.1」**误记**——C1 早在 10-19 已修（v0.1.3 +
    sha 逐字对账，ebbde69），其引用的是翻案前旧段。
  - **链路现状**：kind/role 双键齐（schema 产地 + 语义副本 + emit 数据三半）；
    **UI 切「统一引擎清单」的两半前提都在**（宿主装配 + 我 emit）——球在宿主装配
    引擎条目、UI 接表；接表后「role:'toolchain' ⇒ 不走 install」消费端断言各钉一条。
- **★ UI 048 事故上报与 Q1–Q4 裁定（2026-10-20；我回信 `mail/023` + 宿主事故信 `mail/049`）**：
  - **事故**（UI 现场触发、我核源码行号）：用户点装载 llvm-wasm → 宿主
    `assets-loader.js:274 installLayer` 只实现 pyodide 分支 → 硬拒绝「未知的能力层」。
    **三仓脱节各认一份**：宿主进表时没同步扩 installLayer（主因，我的 049 点名）；
    货架无角色标注（我认——form 是形态不是角色）；UI 曾本地魔改宿主桥（自省在案，
    重申必须走信）。
  - **Q1 裁定 = 加 `role` 可选字段**（不是改 kind——kind 已有 src/pre/engine 语义在途）：
    `package`（缺省）/`toolchain`（不走 install，DownloadStore 管）/`language-bridge`。
    **产地 = 宿主装配器**（tree 条目由宿主出，我 --emit 不涉及）；语义钉死 port/README ✓；
    宿主 schema 提单（host mail/049，与 kind:'engine' 同批）✓。
  - **Q2 裁定 = 方案 B 责任让渡**（assets-loader 只管解释器内；工具链归
    DownloadStore+compile-worker——执行域错配成立）+ 宿主硬拒绝文案改误导性的
    「未知的能力层」为「由下载管理，不走装载」（049 提单）。
  - **Q3 = 以 8761 现役表为准**（同源相对路径 + 产物自证 sha；`runtimes/` 偏差不现于
    现役）；**全条目对账已跑**（15 条逐一 sha/size/url 对部署盘）：13 包 sha+size+url
    **全一致**；两个 tree 条目 size 不一致**是语义不是缺陷**——`url`/`sha256` 指
    **入口件**（clang.wasm 48,069,274B / pyodide.asm.wasm 9,598,218B）而 `size` 记
    **整目录字节**（llvm 全目录 122,922,700 / pyodide 22,013,349 精确对上）。
    **三键指向不同对象、契约文档没写**——已钉死 port/README（tree 条目三键语义段），
    UI 的 Q3「路径与 SHA 偏差」根因即此，钉死后偏差消失。
  - **Q4 = 节奏认可**：U-5 三车道翻案**亲测成立**（8868 三档 idle+eval ok+0 pageerror，
    我复跑）+ U-3/U-6 采信；U-1 browse() 对接是最大头别拖；**D 系列别丢**
    （D1/D2/D4/D8/D9/D10 在案）。
  - **★ 勘误 UI 048**：其引用的 catalog 形状（`kind:"octave-forge"`/`version:"19.1.0"`）
    **不存在于现役表**（实测 tree/6.0.12/无 kind 字段——19.1.0 疑为上游 LLVM 版本串
    混淆）。回信 023 重申发信纪律：**引用必须逐字可复跑**。
- **★ UI 钓鱼执法第五路收官（包管理器路，5h+/208 工具调用；`mail/022` 已投）**：
  - **★ 真装 cgi 全链攻下（我 020 标 SKIP 的那条）**：注入 8761 资产 + `?lane=base`
    架构自洽环境 → 装载 → ✓已安装/●Active → `pkg list: cgi *| 0.1.2` →
    **`getfirst(c,'name')` 真值往返 "z"**（QUERY_STRING 注入）。安装流本身是好的。
  - **对 020 的对账**：D6 根因更深——**U-1 裸 fetch 未接 `OctaveAssets.browse()`**
    （mail/030 明载的出口；UI 自己 mail/028 报过、宿主 030 备齐了数据，UI 未接线）；
    D7 = **U-3 类型双态**（UI `ConsumerEngine` 是串，目录真值/我范例是数组）。
  - **新发信级**：U-4 dev 数据链整体陈旧（public 副本 shelf 922736a 落后两代、
    forge 字节目录缺、manifest 无 forge 条目 ⇒ dev 装不了任何包）；U-5 lane 选档
    不自洽（lanePlan 写死 base 无 manifest ⇒ w64-base 混档 LinkError）；U-2 catalog
    错误无机器码（裸 fetch 异常绕过 err.code → 028 痛点残留路径）；U-6/U-7 低级。
  - **正面存档**：四态语义/版本 15/15/体积 15/15/未知键 fail-open/坏目录 fail-closed
    全接住；pyodide 能力层徽标三件套（025 承诺在）。
  - **★ 契约裁定回执（C-1/C-2 落动作）**：C-1 `consumer` = 数组 + 包含语义
    （钉死 port/README.md，宿主注释提单同批）；**C-2 勘误信已投宿主 mail/048**
    ——mail/030「缺省空值不省键」宣称与实测不符（llvm-wasm/pyodide 整键缺失，亲验），
    **裁定改宣称不改装配器**（能力层无包级描述是合理形态，消费端「键不在=无描述」）；
    C-3/C-4 挂悬案 `questions/04`（dev 取数路径约定 + 顶层 version 指 withheld 的
    呈现判据，结算实验已写）。
- **★ UI 钓鱼执法四路全收（2026-10-20，用户点令「疯狂钓鱼」；019/020/021 三信已投）**：
  四路并行（引擎下载 / 双引擎 / 包管理器 / 通用界面），**发信级缺陷 D1–D10 共十条**，基本面
  扎实（下载核验管线 sha/原子/幂等/不阻塞全过、终端执行链响亮、错误 i18n 翻案=028 痛点
  已修、三语/主题/dock/视口/404 全过、pageerror=0）：
  - **D1 体积硬编码已漂**：OM 显示 71.1MB vs 真实 74,579,404B=74.58MB（Content-Length
    亲测）——显示层与 DownloadStore:604 两层手抄两层漂；A5 配额预检连带失效。
  - **D2 假三档**：master/IP 档字节与 wasm32-final **逐文件同 sha 同字节**（build.json
    diff 亲验为空）——`lanes/master/` 快照是 w32 product 构建，w64 回退永远轮不到。
  - **D3 OM 字节投送面未接**：`/repo/Octave/omc/` 404——OM 下载必失败。
  - **D4 错误无七码 + alert() 阻塞**：四类失败全弹裸 alert，DownloadError 的 code/state
    在 UI 边界被丢弃。
  - **D5 双引擎静默假成功**：勾 OM → boot 承诺 Physics Engine → omc import 404 被空
    catch 吞（`WasmEmbedAdapter.ts:111,127,131`）→ 状态 idle 成功态但 omc_* 全 undefined。
  - **D6 描述字段全丢**：13/13 包描述显示「无详细描述」（catalog 里全有真值）——
    **028 Q2 自己要的接口落地了没接**。
  - **D7 consumer 数组误滤**：严格串比较 ⇒ 能力层在 Octave 筛选下 0/2——契约语义是
    **包含**不是全等。
  - **D8 OMC Shell 假历史**：硬编码 `getVersion→1.25.0~dev-wasm32 success`（omc 真实
    返回 "-rust"）——**取不到也不许编**。
  - **D9 supervisor.evaluate 不存在**：OmcShellPanel:73 调的方法 EngineSupervisor 没有
    （只有 eval/evalJSON，亲验 :522/:551）——OMC Shell 面板完全不可用。
  - **D10 终端 plot 视觉静默**：plot 不 flush（notebook 有 prepareCode 补 drawnow、终端
    没有）——对照实验坐实（补 drawnow 即出图）。
  - **我侧契约动作（D6/D7 的根因侧）**：字段语义钉死进 `port/README.md`——`consumer`
    是数组语义为**包含**；`description`/`links` 消费端**必须渲染**（消费义务）；与
    `kind:'engine'` 同批向宿主提单补 schema 注释。
  - 观察项若干（llvm-wasm 条目渲染缺失、i18n 死键 brand_tag、hue 不钳制、375px dock、
    dev 无 COI 头、ErrnoError 刷屏）——020/021 信内备案。
- **★ 实测第二轮·第二批 OM 站（2026-10-20，断电次日续跑，四项全绿零发信级）**：
  - **⑦ 五模型 Export FMU 回归 5/5**（真切换真导出）：BouncingBall（前验）+
    PID_Controller（474 步 617 ODE）+ DistrictHeating（DAE mode、707 ODE、t∈[0,10800]）+
    DoublePendulum（963 ODE）+ **FullRobot R3（6236 ODE、5 chunks、build 3000ms+sim 991ms）**
    —— 五个模型全部 Run→Export→下载真触发（文件名各异）。**工装假象记档**：断电前
    首跑「EXPORTED×5」实为下拉选择未生效（选错 select + label 大小写），五次导的都是
    默认模型——修正选择器（`selects[1]` + option 文本精确匹配）后才算真验。
    **验收纪律沉淀：断言「换了」必须以可观测状态变化为据（banner 模型名），不能只看动作返回**。
  - **⑧ MSL 大模型深水**：Robot R3 全库装载后堆内存 25MB（performance.memory 实测），
    PID 4MB / DistrictHeating 8MB / 双摆 10MB——无爆栈、页面全程可交互。
  - **⑨ 同页双引擎数值正确性**（samepage，物理判据）：hmax=**1.0000**（= 初始高度）、
    hend=-0.9556（∈ 物理合理域 e=0.7 末端衰减）、7 变量（含 der 消毒改名×4）、
    N=628 采样、反向坏件明确拒收——**全部真值**，非脚本自报。
  - **⑩ OMPlot Compare + 三格式**：双结果文件装载（2 files、7 vars 628 pts ×2）+
    Compare 按钮解禁 ✓；simulator 三格式下载 `.arrow/.mat/.csv` 全部真触发
    （下载按钮在 `#downloadRes`，结果 ready 才现——工装曾按「文本含 Download」找按钮
    误报 NO_DL，按 id 定位即中）。
  - 小计：第二批 4 项全绿，**零发信级缺陷**；两处工装坑（select 错位/按钮定位）均已
    识破并沉淀为验收纪律，未污染结论。
- **★ UI 开工回执（`mail/047`，2026-10-19）+ 我的三问回信（`mail/018`）+ 双提单**：
  - **UI 落地事实（我亲跑复验）**：DownloadStore 9/9（多引擎并发下载、OPFS
    `downloads/engine/{lane}/`、下载不触发布局）+ 双列双引擎 15/15（Octave 三档单选 ×
    OM 独立勾选、`supervisor.boot({lane, enableOmc})` 双引擎并发、MEMFS `/tmp` 握手）。
    UI 自我勘误两条（曾把 omc 塞进单选车道 = 「用户全程 Octave 语境」违例，已重构翻案）。
  - **三问裁定（我 018）**：Q1 引擎清单 = **扩展 forge-catalog 加 `kind:'engine'` 条目**
    （不新开 engine-catalog.json——同一事实两产地 = #20③ 形状；arch=lane 沿宿主 031
    裁决；逐件 sha 仍从产物自证取）；Q2 MSL = 三段答（现状运行时 GitHub 拉 / MEMFS
    落点 `/.openmodelica/libraries/` 三包 / 产物化待 OM）；Q3 进度 = **CustomEvent**
    （`omc:simulate-progress`）+ 无事件回落「不定进度胶囊」（不伪造百分比）。
  - **双提单已投**：宿主 `mail/047`（schema 加 kind 字段，含 optional_keys fail-closed
    向后兼容设计；UI 两步走零阻塞）+ OM `mail/011`（MSL 产物化问询 + omc 驱动进度
    事件钩子问询）。
  - **口径更正（已告知 UI）**：其界面「omc wasm32 · 71MB」的 74,579,404B 是 -Oz
    压缩后数字——建议标「压缩后」并从产物清单实时取，别硬编码（OM 昨天刚换过产物，
    快照会漂）。
- **★ 实测第二轮·第一批 Octave 站（2026-10-19，用户批准计划，六项全绿 + 一翻案）**：
  - **★ known boundary 翻案**：上条「现编产物识别但不可调」**已过时**——宿主
    `accept-compile-extension` **C2c：现编 cell2cell({1,2},1)=1x1 且 (,2)=1x2，与预编
    产物同值**（我亲跑该套件 **16/0**，含 C8 多 TU：cell2cell+partint 双模块、partint
    不变式、产物架构==宿主档）。多 TU 批（cc8e47f）把 resizing 边界修掉了。
  - **compile 线 v0.1.3 回归 16/0**（宿主判据原样跑）；**市场目录对账**：我 `--emit`
    13 包 vs 站点 forge-catalog 15 条**逐字段零分歧**（form/content/consumer/version/
    sha256；站点多出的 llvm-wasm/pyodide = 能力层条目，形状正确；站点 shelf_commit
    285af2f 是我 HEAD 祖先——宿主按需换 pin，正常滞后）。
  - **裁决⑤数据面全绿**：`accept-capability-layer` **12/0**（目录 pyodide tree 条目 →
    install('symbolic') 闭包**先 pyodide 后 symbolic** → `layers().pyodide.ready=true`
    （22,013,349B 真就位）→ 反向：能力层不被误当包拉 tarball）+
    `accept-symbolic-seam` **9/0**（含 R1/R2 反向：非 python system 调用不被吞、
    桥缺失清晰报错）。llvm-wasm 条目 + v0.1.3 供给（manifest 14 条亲验在前）⇒
    「未装 LLVM ⇒ src 包拒载」的**数据面就绪**；装载期硬闸门归 UI DownloadStore + 宿主
    装载界面（第三批 UI 实测再验行为面）。
  - **音频链独立复钓**：手势解锁 → `sound(sin(2π440·0.5s))` → AudioContext
    running + drained=1 + 页面活（23ms 返回 = m-bundle 异步 drain 形状，播放语义按
    宿主 accept-audio 50/0 判据成立；「阻塞时长==音频时长」未验，记观察）。
  - **forge 包装载抽测**：宿主 `accept-forge` **22/0**（含 struct 预编 .oct exist、
    geometry→matgeom 依赖自动解析、32 资产联动）权威盖棺；我的独立钓（cgi/statistics/
    optim 独立页 pkg load + 真调用）见装载提示与页面存活，`__R__` 断言缺席判定为
    **工装时序问题非站点缺陷**（宿主判据同款场景全绿）。
  - 小计：第一批 6 项 **全绿 + 1 翻案**；无发信级缺陷。
- **★ 宿主音频链修复复验收执（2026-10-19，host `658f001` 三层修复 → 我 `mail/046` 复验
  结案）**：① 缺件补编——audiodevinfo.oct 进 TREE_MODS + 38 aliases（`exist
  ('__player_audioplayer__')` 0→**3**，`__player_*.oct` 别名文件铺进 oct/）；② 真播放 =
  webaudio m-bundle 懒加载（未装时 C++ 面 err_disabled_feature 如实声明边界——比 undefined
  进步；装后 28 文件就绪）；③ sync-js 第三态修复（sha 未变也合 meta）。**我独立复验**：
  `load('webaudio')` → sound → **AudioContext 真创建（contexts:1, running）+ 播放意图真
  drain**；`accept-audio` **50/0** 亲跑（含立体声 2ch/44100 断言）。⇒ **钓鱼执法两发信级
  缺陷全部修复结案**（音频链 + OM Export FMU，均为当日修复当日复验）。**总沉淀**：
  `.m` 面在场让 `which` 类断言假绿——验收必须打到第一层真调用（sound 真响 / FMU 真链接 /
  .oct 真 dlopen）。**低优先级记档**：未懒加载时 sound 报 disabled 不提示「装 webaudio
  资产后可用」（懒装载语义对用户不可见，与裸 uigetfile 同族）。
- **宿主 044 两勘误同批落**：B1 gitignore 补洞（`!mail/read/` + 6 封积压补提交）✓ 亲见；
  B2 两封信补投 UI antigravity 侧（host- 前缀防撞号——UI 信箱亲见 host-007/008）✓。
  另：w64-base 死档化（二次三线裁决：站点两格化，无 COI 唯一线 = wasm32）。
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
| `docs_count` | **4** | 2026-10-25T16:40:19+0800 | `ls docs/*.md | wc -l` |
| `llvm_bundle_bytes` | **34693729** | 2026-10-25T16:40:19+0800 | `stat -c%s /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.3.tar.gz` |
| `llvm_bundle_sha` | `cd6450fe7944875c…` | 2026-10-25T16:40:19+0800 | `sha256sum /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.3.tar.gz | cut -d' ' -f1` |
| `port_docs_count` | **1** | 2026-10-25T16:40:19+0800 | `ls port/*.md | wc -l` |
| `pyodide_core_bytes` | **6757104** | 2026-10-25T16:40:19+0800 | `stat -c%s /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2` |
| `pyodide_core_sha` | `2abdcc2e35208af4…` | 2026-10-25T16:40:19+0800 | `sha256sum /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2 | cut -d' ' -f1` |
| `recipes_count` | **3** | 2026-10-25T16:40:19+0800 | `ls recipes/*.md | wc -l` |
| `shelf_needs_capability` | **1** | 2026-10-25T16:40:19+0800 | `grep -l '能力层需求' packages/*.json | wc -l` |
| `shelf_oct_packs` | **0** | 2026-10-25T16:40:19+0800 | `python3 -c "import json,glob;print(sum(1 for f in glob.glob('packages/*.json') if any('oct' in (v.get('kinds') or []) for v in json.load(open(f))['versions'])))"` |
| `shelf_packs` | **13** | 2026-10-25T16:40:19+0800 | `ls packages/*.json | wc -l` |
| `shelf_verified` | **13** | 2026-10-25T16:40:19+0800 | `grep -l '"verified": {' packages/*.json | wc -l` |
| `shelf_versions` | **52** | 2026-10-25T16:40:19+0800 | `python3 -c "import json,glob;print(sum(len(json.load(open(f))['versions']) for f in glob.glob('packages/*.json')))"` |
| `tool_selftest_pass` | **47** | 2026-10-25T16:40:19+0800 | `python3 tools/forge-shelf.py --selftest 2>/dev/null | grep -c '^PASS'` |

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
