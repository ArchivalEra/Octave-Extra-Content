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
| `docs_count` | **3** | 2026-10-18T15:45:56+0800 | `ls docs/*.md | wc -l` |
| `llvm_bundle_bytes` | **34679853** | 2026-10-18T15:45:56+0800 | `stat -c%s /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz` |
| `llvm_bundle_sha` | `a9ba3b41e5fa8e74…` | 2026-10-18T15:45:56+0800 | `sha256sum /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz | cut -d' ' -f1` |
| `port_docs_count` | **1** | 2026-10-18T15:45:56+0800 | `ls port/*.md | wc -l` |
| `pyodide_core_bytes` | **6757104** | 2026-10-18T15:45:56+0800 | `stat -c%s /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2` |
| `pyodide_core_sha` | `2abdcc2e35208af4…` | 2026-10-18T15:45:56+0800 | `sha256sum /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2 | cut -d' ' -f1` |
| `recipes_count` | **2** | 2026-10-18T15:45:56+0800 | `ls recipes/*.md | wc -l` |
| `shelf_needs_capability` | **1** | 2026-10-18T15:45:56+0800 | `grep -l '能力层需求' packages/*.json | wc -l` |
| `shelf_oct_packs` | **0** | 2026-10-18T15:45:56+0800 | `python3 -c "import json,glob;print(sum(1 for f in glob.glob('packages/*.json') if any('oct' in (v.get('kinds') or []) for v in json.load(open(f))['versions'])))"` |
| `shelf_packs` | **13** | 2026-10-18T15:45:55+0800 | `ls packages/*.json | wc -l` |
| `shelf_verified` | **13** | 2026-10-18T15:45:55+0800 | `grep -l '"verified": {' packages/*.json | wc -l` |
| `shelf_versions` | **52** | 2026-10-18T15:45:56+0800 | `python3 -c "import json,glob;print(sum(len(json.load(open(f))['versions']) for f in glob.glob('packages/*.json')))"` |
| `tool_selftest_pass` | **45** | 2026-10-18T15:45:56+0800 | `python3 tools/forge-shelf.py --selftest 2>/dev/null | grep -c '^PASS'` |

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
