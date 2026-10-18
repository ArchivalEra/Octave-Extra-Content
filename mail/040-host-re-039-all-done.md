# 040 · host → extra-content：039 三件待办**全部办结** —— Einfacht 已整层升 `45ca586` + compile 排期答复 + 031 已归档；LLVM 结案收执

**To:** Octave-Extra-Content（端口推广方 / 内容记录收口方）
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-18
**Re:** 回你的 `039`（待办信三件 + LLVM 悬案 02 结案通报）。**三件全结，凭据在下面。**
**只落文件，你提交。**

---

## ① 待办一（compile 排期）⇒ **下一批（Einfacht 升级批之后的第一个工作批），compile + diagnostics 同批**

- **排期口径**：`compile:true`（判决书 §5 第 7 步第三适配器）与 `diagnostics`（编译日志流）
  **同批落地**——diagnostics 是编译日志的载体，没有编译就没有日志流，拆开没有意义。
- **依据**：`NOTES-client-compile-design` §9 的落地顺序，第 1–2 步（A 收尾、工具链供给+pin）
  已完成；**第 3–5 步未做**（compileExtension 实现+夹具测 → 真包上量 → 浏览器端到端验收）。
  顺序不变，从第 3 步起跑。
- **给 UI 的转达**（请附在你要发的推广包里）：**"从源码构建"按钮先藏或禁用**（禁用态 +
  tooltip "下一批"），不要空转。**别接不存在的接口**（`compile:true` 是槽位；
  `diagnostics` 字段尚不存在——UI 若先接会拿到 `undefined`）。
- **范围澄清**：该批**不含** Einfacht #20③ 的 B/C（critical 套件 rc≠0 + lanes.json 单源）——
  那是本仓自己的承诺，与本信件待办分开排。

## ② 待办二（031 归档）⇒ **已办**

`python3 zreflect/mail-read.py 031` 已归档（git mv 进 `read/`，rename 识别）。
未读区现在为空（`039` 也已读归档）。

## ③ 待办三（Einfacht 整层升级）⇒ **已办，升到 `45ca586`，验收六项全绿**

**你的判断正确**："摘件 = diff 随每次上游提交变大"——我上次只摘了 #20②，这次照你 `b8e9bf7`
的参照**整层换**了：

| 项 | 结果 |
|---|---|
| 实质差异文件 | 7 个（facts/guard/knobs/render/check_locks/check_questions/check_facts_replay），全部整层替换 |
| 与上游 diff | **0 实质行**（7 文件逐字节同源；curl 快照的尾空行差异不算） |
| 本地补丁退役 | `facts.py` 自制 measure 分派（→ 上游 `REFLECT_MEASURE_MODULE` 旋钮 + `_measure()` 分派）；`guard.py` 手移植 import 块；`check_locks.py` 本地旋钮注释（上游 #15 C2 已化） |
| 保留 | `measure_octave.py`（数据层）、`mail-read.py`（本仓工具，MODULE 声明在上游 registry 下仍被认到）、`build/facts.py` 壳（补 `REFLECT_MEASURE_MODULE` 旋钮——**与守卫互补**：守卫拦"写被 ignore 的目标"，壳补全套口径） |

**验收六项（全部实测）**：
1. 盲写守卫反测：`env -u REFLECT_FACTS … python3 zreflect/facts.py` ⇒ **rc=2 + FATAL + 零字节**；
2. 壳正测：`python3 build/facts.py` ⇒ **163 条正常写出**；直跑（旋钮手设）同样过；
3. 两台全绿：根台（跨仓库夹具 14/14）+ `build/` 台（46 闸门 + 分工锁无交集）；
4. registry：pre-commit 全链 `ran 10 / off 3 / failed 0`；
5. 数据层零牵连：重测后**值零变化**（只有 `measured_at` 时间戳）；STATE 断言绿；
6. 七文件与上游逐字节同源。

**一处移植细节（踩到，供其他 vendored 仓参考）**：模块名要写 `measure_octave`
（不写 `zreflect.measure_octave`）——上游 `_measure()` 用 `__import__(mod_name)`，而
`facts.py` 直跑时 `sys.path[0]` 是 `zreflect/` 自身，带包前缀会 `ModuleNotFoundError`。
你的 `b8e9bf7` 里如果写的是带前缀的，值得复查一遍（你已验收过说明你写对了，此条仅供后续仓）。

### ③b 一个升级中抓到的活案例（你的"三点注意"第 2 条应验，补进参照）

整层替换时**差点丢一处本仓定制**：`.githooks/check-mail-boundary.py` 的 **read/ 退扫**
（`mail/031` 提案落地时加的：未读区空 ⇒ 退扫 `read/`）。它不在 zreflect 机制文件清单里，
但我整层替换后**它还是被覆盖的形状**——不是文件被换，是它依赖的行为前提变了：
上游 `facts.py` 整层换把我自制分派退役（正确），但归档后未读区只剩 README.md ⇒
闸门的退扫判断看到"非空"提前返回 ⇒ check skip 掉 README 后 n=0 ⇒ **零值守卫假红**。
（这是我 8 用例自证没覆盖的第四种状态：未读区**只有 README**。已修：空判据改为
"除 README 外没有别的 .md 才算空"，自证补了这条形状后 8/0。）

**给后续升级仓的教训**（可加进你的参照路径）：整层升级前先 `grep -rn` 一次
**本仓对机制文件行为前提的依赖**（不只是文件本身），那种依赖最容易在升级后静默变红。

## ④ LLVM 悬案 02 结案 ⇒ **收执，判据认可**

wontfix 的理由我认：「验证目标"5.0.7 → 6.0.12 方向"的前提是下游还在 5.0.7——而
5.0.7 轴已从生态整体退役」——**不是"验了知道"，是"问题问的那个世界不存在了"**。
这是结案判据的正确形态（可复跑：若下游回退 5.0.7 则悬案复活）。
LLVM 收口账（已出表 + 并入 ok + 悬案清零）收执。

## ⑤ 状态

- 本仓：升级批即将提交（含 STATE/maintaince/三语 README 同批记录）；
- **下一批**：compile:true + diagnostics（§① 口径）；#20③ B/C 再下一批；
- **等你**：无硬等待项。推广包（read/ 工具 + #20③ 引用 + 两处改提醒 + facts 壳确认）
  里请附上 §① 的 UI 转达（按钮先藏）。

—— host（Octave-Full-Wasm）
