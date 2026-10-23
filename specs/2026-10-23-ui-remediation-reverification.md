# Spec：UI 掀翻式重构的复钓验收（fix/integrity-reconciliation 分支）

**提案人**：Octave-Extra-Content（钓鱼判据产地与验收方）
**日期**：2026-10-23
**状态**：待用户审阅（同意后才 implement）
**对象**：UI `mail/055` 声明的 12/12 全量整改（分支 `fix/integrity-reconciliation`，20 提交，未合并——等复钓结果定合并）

---

## 0. 背景与立场

用户裁定（mail/055 §四1 引述）：**本仓自造钓鱼脚本永远不得作为 UI 的收口证据——渔具与钓权归验收方**；UI 自己的 346/346 单测只覆盖逻辑形状，不冒充复跑判据。因此本 spec 的全部判据由**我方真浏览器复钓**产出，UI 听判。

## 1. 目标（deliverable）

一份**复钓验收报告**（投 UI `mail/056`），逐判据给 PASS/FAIL + 证据 + 复跑命令，附「留痕裁量点」踩中清单（UI §四2 声明的 6 条——踩到任何一条都如实报，因为它说「都是留过痕的」）。验收结果直接决定 UI 是否合并分支。

## 2. 测试环境

- UI dev server：`pnpm dev`（http://localhost:4321/repo/Octave/，分支工作树已在其上——已勘察确认）
- 判据不采信 dev 边界内的假阴性：vite public js import 500 等 4 条已知白名单（钓鱼全程在案）
- harness：/mnt/hdd/octave-wasm-build/harness/（playwright-core + 系统 chromium，宿主同款起法保 COI）；脚本用完即删（惯例）
- OPFS 检查：`navigator.storage.getDirectory()` 递归列 `octave_workspace/downloads/`（实测根，非 OPFS 根）

## 3. 四判据（UI 原样奉还的复跑 + 我补的两个）

### 判据 A（P0-1）：Plots 面板复活
- 步骤：boot → 终端 `h=1:10; plot(h);` → 激活 Plots tab
- PASS：图真显示（Plots 面板内可见 img/canvas，非 staging 藏匿）；console 无 `graphicsSink.onFigure` TypeError
- FAIL 附加观察：Notebook 路径回归确认（原侥幸通道不许被新接线弄坏）

### 判据 B（P0-2）：离线零流量（五件套）
- 步骤：下载引擎（wasm32-final）→ 等徽标 ✓ → `setOffline(true)` → reload → 启动
- PASS：到 idle 且 `/octave\.(js|wasm|data)|build\.json|assets\/manifest/` 网络请求**= 0**（五件全拦）
- 附加钓点：断网启动后**资产可用性**（idle 但 dldfcn 全灭的「降级假绿」不许复发——跑一条 `exist('gzip')` 或 plot 验资产链）
- 边界如实记：真断网下页面文档本身能否 load（dev 无缓存头）——记观察不判 FAIL

### 判据 C（P0-3 + 增补 3）：完整性闸门（两个钩子）
- C1 截断：OPFS wasm 截 1 字节 → 启动 → PASS = 报 `ENGINE_CORRUPTED`（或等义校验错）+ **零网络重下** + 徽标「⚠ 已损坏」
- C2 XOR：wasm 首字节 xor 0xFF（大小不变）→ reload → PASS = 徽标「⚠ 已损坏」非「✓」；启动 → PASS = 校验错非静默喂坏字节
- 附加：`size===expectedBytes` + sha 重算的实测时长（五件全验的性能面——74MB wasm 重算 sha 会不会卡 UI，记录数字）

### 判据 D（P0-5）：生产 Mock 回退根除
- 步骤：page.route 拦 `octave-core.js` 返回 404 → 生产路径 boot
- PASS：状态 failed（非 idle）+ 错误含 BOOT_UNAVAILABLE（或等义）+ **绝不出现 `ans = 42`**

### 我补的判据 E：getAssetsPort 复活（增补 1 的行为面——UI 只给了 tsc 死缝证据）
- 步骤：page.evaluate 复刻 `plugin.getAssetsPort().fetchCatalog()` 调用（原实测 THROW 的同款闭包路径）
- PASS：返回 15 packs（catalog 真读到——动态防线活）；`typeof plugin.getAssetsPort === 'function'` = true

### 我补的判据 F：假 seam 清扫回归（架构 Strong③ 的行为面抽查）
- `src/lib/engine/` 目录不存在（已勘察 ✓——判据写入报告）；`unit()` grep 零消费者；OMC 桥独立后**双引擎回归**（勾 OM → boot → FLAVOR_UNAVAILABLE 上报链仍工作 + toast 经组合根不倒挂）
- R1 回归：终端 `1+` → 错误文本**无中文噪音**（ErrorSanitizer 接通终端通道）

## 4. 执行方式

- 我方真浏览器逐判据跑（每判据独立 fresh context，OPFS 起始干净或按判据需要预置）
- 每判据：PASS/FAIL + 证据（网络请求清单/徽标截图/console 全文/OPFS 字节）+ 复跑命令
- **不修任何 UI 文件**（只报；留痕裁量点踩中如实报）
- 产出落我仓 STATE + 投 UI mail/056；全过 ⇒ 建议合并；有红 ⇒ 红项 + 裁量点对照表

## 5. 明确不做

- 不重跑 UI 的 346 单测（它自己跑过；单测面不是复钓面）
- 不验 UI 仓 Einfacht×wayfinder 联动（它仓内机制，非本 seam 契约面——只在报告里记录其存在）
- 不做第三批 UI 全插件回归（本轮只验 054/055 指名缺陷的修复面；全回归待分支合并后另行规划）
- 不碰「宿主侧 omc 进表」提单进度（host mail/056 在途，另行跟踪）

## 6. 风险与边界（如实）

- dev server 需重启在分支上（已确认工作树在分支；服务当前停着，implement 时起）
- chromium 下载期高频 evaluate 会触发 SIGTRAP（055 环境坑在案）——脚本改只轮询 OPFS stat
- UI §四2 的 6 条留痕裁量点（#6/#9/#10/#12/#14/#15）——踩中任何一条不算它撒谎（留痕公开），但如实进报告
- 分支未合并：复钓全过前，main 上一切如旧（本验收不改变 main 现状）

**等你批准后 implement。**
