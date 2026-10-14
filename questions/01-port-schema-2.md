# 01: `--emit` 是否已对齐端口 schema 2（`form`/`content` 两轴）？

**Status:** ready-for-agent

**Settling:** `tools/forge-shelf.py` —— 跑 `tools/forge-shelf.py --emit /tmp/emit-probe.json --allow-unverified` 后读输出的 `"schema"`：rc=0 且 schema=2 ⇒ 已对齐（结案）；rc=0 且 schema=1 ⇒ 未对齐（本单第一交付物 = 给 `--emit` 加两轴）。

## 背景

`port/README.md`（宿主 `build/extra-content/` 的消费侧副本）写的是 `schema: 2`，
带两条命名纪律：`form` = 投送形态（供给期从字节派生）、`content` = 内容构成（今天的
`kinds`）。而本仓 `tools/forge-shelf.py --emit` 目前出的是 `schema: 1` + `kinds`。
`port/README.md` 的「待办」里也列了这条。**未对齐是已知状态，不是意外** —— 本单的作用
是给它一个**能跑的结算件**，而不是留在散文里。

## 结案判据

- 跑上面那条命令，读输出里的 `"schema"` 值；
- `2` ⇒ 结案（把本文件 `Status` 改 `resolved`，别删）；
- `1` ⇒ 维持未结案，本单第一交付物 = 加 `form`/`content` 两轴。
