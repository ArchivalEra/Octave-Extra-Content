# 01: `--emit` 是否已对齐端口 schema 2（`form`/`content` 两轴）？

**Status:** resolved

**Settling:** `tools/forge-shelf.py` —— 跑 `tools/forge-shelf.py --emit /tmp/emit-probe.json --allow-unverified` 后读输出的 `"schema"`：rc=0 且 schema=2 ⇒ 已对齐（结案）；rc=0 且 schema=1 ⇒ 未对齐。

## 结论（2026-10-14 结案）

**本仓侧已对齐**：`--emit` 现在出 `schema: 2`，每条带 `form`（投送形态，本仓恒为 `pkg`）
与 `content`（内容构成 = 旧的 `kinds`），`kinds` **保留为兼容视图**（旧消费者照读）。
`--selftest` 加 3 条断言覆盖两轴（含一条反向：`kinds` 空 ⇒ `content` 也空，不许把空说成有内容）。

**未闭合的**是**宿主侧**：端口产地 `build/extra-content/{content-list.schema.json,
validate-content-list.py, golden/, bad/}` 仍未落地（宿主侧动作，本仓不改宿主仓）——
那不是本单的对象，见 `port/README.md` 待办。

## 背景

`port/README.md`（宿主 `build/extra-content/` 的消费侧副本）写的是 `schema: 2`，
带两条命名纪律：`form` = 投送形态（供给期从字节派生）、`content` = 内容构成（今天的
`kinds`）。而本仓 `tools/forge-shelf.py --emit` 原先出的是 `schema: 1` + `kinds`。

## 结案判据（复跑）

- `python3 tools/forge-shelf.py --emit /tmp/emit-probe.json` ⇒ 输出 `"schema": 2`；
- `python3 tools/forge-shelf.py --selftest` ⇒ 17 PASS（含两轴的正/反/空三类断言）。
