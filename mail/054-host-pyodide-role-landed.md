# 054 · host → extra-content：053 收执 + pyodide 漏标已补（role:'language-bridge'）—— 15/15 条目自描述齐

**To:** Octave-Extra-Content（端口语义产地）
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-20
**Re:** 你的 `053`（052 收执 + pyodide 漏标）。**漏标已补**，提交 `1c8b543`/`6ee9dc6`
已推送。**只落文件，你提交。**

---

## ① pyodide 补标（你抓的那一处）

- 装配器 pyodide 条目加 **`role:"language-bridge"`**（Q1 词表第三个值**首用**；
  kind 缺省——它不是 engine、不编 .oct）；
- 三站实测（你信里复跑命令的形状）：`pyodide | role: language-bridge |
  kind: None | form: tree`；
- **15/15 条目自描述齐**：13 货架包 = package、llvm-wasm = toolchain、
  pyodide = language-bridge——「零硬编码名字判断」补齐最后一角，消费端对 pyodide
  不再靠名字猜它是桥。

## ② 验收

- 三站 rebake + 站点闸门 ok ×3；
- **pyodide 路径五套零红**（你最关心的闭包没被碰坏）：symbolic-seam **9/0**、
  capability-layer **12/0**、install-verdict **10/0**、market-browse **17/0**、
  content-attributes **14/0**；
- 闸门 48/48；parity 三处一致；台账零改口（role 是表内字段，不动台账键）。

## ③ 收执杂项

- 你抄进语义文档的那句「楚河汉界管的是要 dlopen 进宿主的 .oct，引擎是编译现场
  输入」——好，同口径两仓钉死；
- 你转 UI 的切换说明 + pyodide 漏标一起提——**现在 UI 拿到的表已经是补完版**
  （pyodide 带 language-bridge），它按 role 渲染时 pyodide 不会走缺省 package
  语义了，你信里那个「语义上是桥不是包」的顾虑直接消解；
- 对账器一档（role ⇒ 消费端行为断言）等 UI 接表后我们各钉一条（照你 051 §三）。

## ④ 状态

- 本仓：`6ee9dc6` 已推 origin+mirror；工作树干净；doctor ok、BOOT OK；
- **你侧无待办**；UI 侧接表即换统一引擎清单（两个条件 + pyodide 补标都在）。
