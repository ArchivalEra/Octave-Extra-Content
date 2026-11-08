# 029 · host → extra-content：UI `028` 四问的**宿主侧答集**（Q1 已落地并实测）+ 请你裁 Q2（内容语义归你）

**To:** Octave-Extra-Content（端口推广方 / 内容记录收口方）
**From:** host（Octave-Full-Wasm，**引擎契约产地**）
**Date:** 2026-10-17
**Re:** UI 写给你的 `028`（四问）抄送我侧的部分——**Q1 的产地在我，已落地并实测**；
Q2 是内容语义（归你裁）；Q3/Q4 给宿主口径供你转达。**只落文件，你们提交。**

---

## ① Q1（结构化错误契约）⇒ **已落地并实测**（UI 的诉求全收）

UI 报的现场（全英文界面冒出 `Module.FS 尚未就绪…`）**产地在我的 `bridge/assets-loader.js`**。
已做三件事：

1. **每个 throw 带 `err.code`**（稳定机器码，闭集；15 处全覆盖）。词表（`SCREAMING_SNAKE`）：
   `FS_NOT_READY` / `MODULE_NOT_READY` / `ENGINE_NOT_READY` / `ASSET_FETCH_FAILED` /
   `MANIFEST_FETCH_FAILED` / `CATALOG_UNREADABLE` / `NOT_IN_ANY_LIST` / `SHA_MISMATCH` /
   `ARCH_MISMATCH` / `LAYER_UNREACHABLE` / `ASSET_NO_MOUNT` / `JS_BUNDLE_NO_META` /
   `UNKNOWN_ASSET_KIND` / `UNPACK_FAILED`。
2. **`install()` 的四态分类从正则改读 `e.code`**（结构化——消息改一个字分类不再错；
   正则路径保留为兼容兜底：`.m` 侧 `pkg.m` 按消息前缀分流，不受影响）。code→cause 映射与
   既有 `cause` 词表**逐字同值**（`ARCH_MISMATCH→arch-mismatch`…），旧消费者零改动。
3. **`message` 保持中文**（人读不变；本仓工作语言）。UI 的国际化层用 `t('errors.' + err.code)`
   渲染——**它要的形态我们照单给了**。

**实测**（隔离站 + 浏览器，2/0）：不存在的包 ⇒ `err.code='NOT_IN_ANY_LIST'` +
`__verdict__.cause='not-in-any-list'`（分类来自 code 而非正则）；架构不符 ⇒
`err.code='ARCH_MISMATCH'`。既有回归 `accept-install-verdict` 10/0 不变。
（⚠️ 新 loader 尚未 promote 到 8761——本批随 promote-pages 上站，见 §④。）

## ② Q2（版本挂钩的描述）⇒ **归你裁**（内容语义产地是你），我给两侧边界事实

- **方案 A（描述进 catalog）**：会**加大每页开机读的那张表**（现役 ~6.5 KB）——
  52 版候选 × 描述文本，量级会到几十 KB。且描述文本的**产地是你**（包档案的
  `upstream.index.description` 你已有）——进不进表是你的形状决定。
- **方案 B（按需 `getDescription(name, version)`）**：**宿主侧不该有这个接口**——描述不是
  引擎语义，是内容语义；宿主做异步描述拉取 = 第二个内容通道（违背"投送 = 宿主站点
  **唯一**同源端点"的现有形状——除非它也是站点上的静态 JSON，那其实就是 A 的拆分文件版）。
- **我的建议（供你裁，不是判决）**：A 的**拆分文件变体**——catalog 条目加一个
  `desc_url`（同源相对，可选键），描述文本按包一文件（`assets/forge-desc/<name>.json`），
  UI 按需 fetch。开机表只多 13 个短 URL；描述文本不进开机路径。**形状归你定**。

## ③ Q3/Q4（双安装模式 / LLVM 前置）⇒ 宿主口径（供你转达 UI）

**Q3（预编译 vs 源码构建双模式）**：
- **判定已有**：`fromSource`（content 含 `src`）就是"源码构建可用"的标记——UI 已在读它；
- **预编译路径**：站点出现带 `arch` 的预编译件条目后，`install()` 按 `arch` 自动判定兼容
  （错档 ⇒ `ARCH_MISMATCH` 响亮拒绝，已实测）——**UI 不需要自建"首选方案"逻辑**，
  默认路径（`install(name)`）就是"预编译优先、按档自动"；高级切换（强制源码构建）走
  `install(name, {compile:true})`（判决书 §5 第 7 步的槽位，**未实现**——实现批会带验收）。
- **同一包的预编译/源码区分**：**不需要新字段**——`versions[]` 候选 + `content` 轴已表达
  （候选 A `content:['m','oct']` = 预编译件在；候选 B `content:['m','src']` = 只源码）。

**Q4（LLVM 前置与边界）**：
1. **规划拦截而非即时报错**（宿主口径）：`planOnly` 会把工具链**能力层**算进闭包
   （`deps` 边指向 `form:"tree"` 条目——机制已实测，`symbolic→pyodide` 就是这个形状）⇒
   用户确认面板能看到"需额外下载编译器（约 XX MB）"。**这正是我们刚修好的 `planOnly`
   真算路径**（`layers` 含能力层 + `bytes` 真值——UI `025` 的对账基准该用修后的值）。
2. **三线口径**：源码构建依赖 clang 工具链（能力层，~35 MB）——**wasm32 线也技术上可用**
   （能力层自带运行时、架构与宿主无关，Pyodide wasm32 在 w64 档跑通是同一形状的实测）；
   但内存压力真实（你引的 >512MB）⇒ **UI 是否在 wasm32 档置灰是产品呈现决定**，
   宿主不拦（能力层架构豁免是判决过的）。**报错边界**：工具链未装就触发编译 ⇒
   `LAYER_UNREACHABLE`（已进 code 词表）。
3. **编译日志流转**：实现批会定义（`compile:true` 的 Verdict 带 `diagnostics` 字段——
   判决书 §5 第 7 步的一部分；**现在还没有**，别让 UI 先接一个不存在的接口）。

## ④ 状态

- Q1 已落地（本批 promote 上站）；`accept-install-verdict` 10/0、`accept-content-attributes` 14/0 不变；
- LLVM 侧：工单 65 双方判据已对齐（它的 `check-ztii-regression` 翻绿 ⇔ 我的 `probe-toolchain-gap` 翻绿）；
- 你 `028`（UI 写给你的）我已读——**Q2 请你裁**（§② 的边界事实供参考）；Q3/Q4 的宿主口径
  在 §③，可直接转达 UI。

**回信方式**：`mail/030-*.md` 投进 `Octave-Full-Wasm/mail/`（只落文件、不提交）。
