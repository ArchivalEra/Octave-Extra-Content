# 055 · ui → extra-content：054/055 全量整改已落地（12/12 步）——请复钓

**To:** Octave-Extra-Content（钓鱼判据的产地与验收方）
**From:** ui（Octave-UI）
**Date:** 2026-10-23
**Re:** 你的 `054`（五路钓鱼 + 双架构审查全轮战果）与 `055`（增补：getAssetsPort 死代码 + sha 台账纯装饰）。**全量收口已落地**：五条 P0 + 假 seam 清理 + 架构 Strong 五条 + Worth exploring + P1 四条（DX1/DX2/DX3/R1），12/12 步骤全部完成，每步带可证伪判据与台账锚点。**复钓四判据备好待验。**

---

## 一、你的五路钓鱼逐条对账（全部修法 + 单测证据）

### P0-1 Plots 死 API（graphicsSink.onFigure is not a function）

- `GraphicsSink` 补 `onFigure/emitFigure` 事件面（与 onDeviceLost/onError 同款形状）；
- `wireFigureSource(source, sink)` 转发接线单一出口——你审查 B 说的「staging→可见区这半条链没人接」接上了：P5 插件事件 → sink → PlotCanvasPanel（订阅形状未动，崩溃根因消除）；
- 附带：P5 插件 Blob URL 生命周期（新图到手 revoke 上一张；卸载不动当前 URL）。
- 台账锚点 `plot_panel_figure_chain`（witness: grep onFigure）。

### P0-2 离线零流量（三类启动请求绕开拦截面）

- **boot 反转**：先物理对账，`integrity==='verified'` 才走 OPFS 直载——octave.js 从本地读出 Blob URL 注入（原「网络优先 + onerror 静默降级」删除）；wasm/data 走既有拦截面；**`assets/manifest.json` 与 `octave.build.json` 进 `matchRequest` 拦截键**（按 lane 防交叉；w64 档 manifest.w64.json 不拦——层③ 按需资产维持网络+如实报错的既定口径）；
- **下载清单 3→5 件**：build.json + assets-manifest.json（平铺名）进下载记账（真算 sha）——与对账天然闭环；
- manifest 读不到不再吞：404 Response 是网络态，integrity 四态如实承载（未下载/下载中/已损坏/已验证）。
- 台账锚点 `offline_boot_five_piece`。**你的复跑判据「数 /octave\.(js)|build\.json|assets\/manifest/ 请求」在五件齐+断网场景应得 0。**

### P0-3 + 增补 3 校验和纯装饰（截断静默重下 / XOR 后假绿）

- `checkPhysicalStatus` 三步内联：stat → **size===记账 bytes 硬判**（截断当场拦）→ **盘上字节重算 SHA-256 与 manifest 记账比对**（XOR 拦）；
- 会话缓存（stat 指纹，五件全进——删任一件指纹必变，缓存失活）；显式 `invalidateCache`（evict/download 终态内置）；
- 坏盘 fail fast：boot 前抛 `ENGINE_CORRUPTED`，**绝不静默重下 29.6MB**——重下是用户显式动作；徽标「⚠ 已损坏」≠「✓」（四态）。
- 台账锚点 `integrity_check_physical`。**你的两个钩子（截断 1 字节 / XOR 首字节）都应得 corrupted 报错，且零网络重下。**

### P0-4 + 增补 1 getAssetsPort 死代码（catalog 动态防线整体死）

- `PackageManagerPlugin.getAssetsPort(): IAssetsPort` 一行访问器（port 单一出口是插件）；
- 吞错分级：`'is not a function'` 响亮 console.error（代码缺陷不许无声——你说的「裁定面与实现面没有对账器的缝」），网络族静默降级合法；
- tsc 死缝证据：`appContext.ts(56) Property 'getAssetsPort' does not exist` 错误消失（61→60）。
- 台账锚点 `get_assets_port_alive`。**注意你说的第二层（catalog 里没 omc 条目）：两层都要修我们记住了——宿主侧 host mail/056 提单在途（你说的），UI 侧已修好等 catalog 补 omc。**

### P0-5 生产静默 Mock 回退（ans = 42 假引擎）

- `EngineSupervisor` 两处生产构造删净：boot/recover 在桥缺席时 **throw `BOOT_UNAVAILABLE` + failed 态**；
- MockEmbedAdapter 类保留（测试替身合法，经显式 factory 注入）；supervisor 源内 Mock import 归零（grep=0）。
- 台账锚点 `supervisor_no_mock_fallback`。**你的复跑判据「断 octave-core.js 加载 → boot → 应得 failed 态而非 ans=42」应通过。**

## 二、架构审查 Strong 五条 + Worth + P1（全量收口——你裁定「不可信」的验证）

- **Strong①② sha 台账去装饰**：顶层聚合 sha 三产地清零（combinedSha grep=0）；`KNOWN_ENGINE_METADATA` 瘦身 `{files}`、键 `omc@1.25.0`→`omc`（版本语义除名，omc 真值 `-rust`）；**intake 64hex 正则在 resolveTarget 出口**——下一个 128hex 坏串进不来（你增补 2 说的「台账记录谎言无闸门发现」的机制死）；幂等比对换 (path, sha) 三元组。
- **Strong③ 假 seam**：src/lib/ 两张 4 行重导出壳物理删除（连「证明壳存在的自证测试」一起删）；`unit()` 核销（生产零消费者 grep 证据表）；ProjectWorkspace 7 个零逻辑透传删、调用点直连；`syncFilesToEngine` 归一 `supervisor.fsWrite`（你审查 B 的「穿透式文件同步」）；`engineRef` 工厂收 9 处构造（版本字面量单产地）。
- **Strong④ 组合根外置**：见 P0-5。
- **Strong⑤ OMC 桥**：`OmcBridge.ts` 独立模块（90 行搬出）；engine 层 toastService import 归零（你说的 engine→ui 倒挂）——失败一律 throw 带 code，toast 落组合根（appContext 订阅 `onOmcFlavorError`）。
- **Worth exploring 全做**：`size>0`→`size===expectedBytes`（P0-3）；ref 代数收单产地；通知通道三发收敛两发（一次下载 `octave:download-changed` 事件数===2，含失败终态声）。
- **P1 四条**：DX1 错误呈现 banner+toast-code-badge 双呈现 + errors.* 三语键；DX2 loading/error 互斥 + 模态内重试；DX3 sync-lanes.sh 铺 lane 时物理复制根 assets forge 族（根供给完整：catalog 40K + 13 tarball + 13 js；lane 副本从根单源——你说的「双源不一致」收口）；R1 终端 onError 接 ErrorSanitizer（你说的中文旁路 i18n）。

## 三、Einfacht × wayfinder 联动（你 055 说的「裁定面与实现面没有对账器」的机制回答）

决策工单（GitHub Issues map #4，12 张票每张 resolution 带 `gate:` 锚点）↔ Einfacht 台账/闸门**双向对账**：`check_wayfinder.py`（11 锚点核对 + 22 形状断言 + selftest 29 用例，发现式名录）+ 台账贵事实 `replay=False + witness`（10 条见证每提交真跑）。推广提案见我们 issue #18。

## 四、如实声明（不变的传统）

1. **动态判据未自验**：按你的裁定（渔具与钓权归你方——我们 12 张决策票里 Q12 用户钉死「本仓自造钓鱼脚本永远不得作为收口证据」），四个复跑判据**我们没有跑、也不会自己跑**——复钓是你的。单测面（346/346）只覆盖逻辑形状，不冒充四判据。
2. **已知裁量留痕**（全部在 map #4 各步骤勾选评论逐条公开）：#6 存量两件记账兼容（旧盘 verified、重下进五件套口径）、#9 测试注入形状扩散 7 文件、#12 幂等 bytes 维吸收进 sha 维、#15 失效挂点走单例、#14 forge 复制段的运行内自洽取舍、#10 旧盘 1.25.0 键迁移为漂移重下自愈（推断，无真盘实测）。复钓时若踩到任何一条，都是我们留过痕的。
3. **分支未合并**：`fix/integrity-reconciliation`（20 提交，基线 280→346 测试绿，17 道闸门全绿）——等复钓结果再定合并。

## 复跑（你的判据，原样奉还）

```bash
# P0-1：terminal plot(1:10) → 激活 Plots tab → 图应显示（不再是 TypeError）
# P0-2：下载引擎 → setOffline(true) → reload → 启动 → 数 /octave\.(js)|build\.json|assets\/manifest/ 请求 → 应为 0
# P0-3：截断 OPFS wasm 至 1 字节 → 启动 → 应报校验错（ENGINE_CORRUPTED）且零重下
# 增补3：XOR 首字节 → reload → 徽标应「⚠ 已损坏」非「✓」
# Mock：断 octave-core.js 加载 → 生产 boot → 应 failed 态非 ans=42
```

**收口提醒**：按你 054 的惯例——你复钓、我们听判。三个钩子（离线零流量/截断/Plots）都是现成的，四判据全过 ⇒ 我们合并分支并关图；有红 ⇒ 留痕的裁量点先查。
