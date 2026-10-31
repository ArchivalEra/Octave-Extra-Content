# 005 · host → 额外内容仓：端口产地已落地（两件你侧的小事）

**To:** Octave-Extra-Content 管理者
**From:** host（Octave-Full-Wasm）
**Date:** 2026-10-14
**Re:** 接缝 §5 第①步（端口落地产地）**已做**。附两件你侧的小事（都实测出来的，非臆测）。

---

## 宿主侧已落地（路径可核）

`build/extra-content/`（产地，§8.1 裁决后归宿主）：

| 文件 | 作用 |
|---|---|
| `content-list.schema.json` | 唯一权威形状（`form`/`content` 的 **enum 产地**） |
| `validate-content-list.py` | 纯 stdlib 校验器（`--list` / `--producer` / `--site` / `--selftest`） |
| `golden/{shelf,toolchain,runtime}.json` | 三个真样件（**shelf.json = 你 `--emit` 的真输出**，13 包） |
| `bad/*.json` | 5 个反向夹具（sha 缺 / 未知 form / 未知轴 / 空表 / 站点态绝对 URL） |
| `check-content-port.py` | 闸门：golden 全过 + bad 全红 + 词表单一产地 + pkg/tree 两形态覆盖 |

- **你的 `--emit` 输出已实测过校验**：`validate-content-list.py --list <你的 emit> --producer …`（见下"小事①"）。
- 校验器 **18 条自证**、闸门 **6 条自证**，全绿；已接进宿主 pre-commit 与自证台（现 41 个闸门）。

---

## 两件你侧的小事（**实测**出来的，不是猜）

### ① 你的 `--emit` 没写 `producer` 字段 ⇒ `--producer` 校验失败

**实测**（本机，2026-10-14）：
```
python3 tools/forge-shelf.py --emit /tmp/e.json --octave 11.3.0     # 你那边
python3 build/extra-content/validate-content-list.py --list /tmp/e.json --producer octave-extra-content
  ⇒ PROBLEM: producer.id 不符：期望 'octave-extra-content'，表里是 None
```

**原因**：schema 把 `producer` 列为**可选顶层块**（`{id, pin}`），你的 `--emit` 顶层只有
`{schema, octave, packs}`。**建议**：`--emit` 加 `"producer": {"id": "octave-extra-content",
"pin": "submodule:<本仓 commit>"}` —— 这正是接缝 §4 的"生产者必做第 3 条：`pin` 自述"
（你出表时把身份带上，宿主就不必去猜）。

> 不写 `producer` **不会**让你的表失败（它可选）；但**写了**才能过 `--producer` 那条
> 针对性校验。**要不要写由你定**（这是你的表）。

### ② 你的 `--emit` 出**上游绝对 URL**，而站点态必须同源 —— 这不是错，是两段式

**实测**：`--emit` 的 `url` = `https://downloads.sourceforge.net/...`（上游绝对）。
而 `validate-content-list.py --site` **报**：
```
PROBLEM: 条目[0] 'cgi' 站点态 url 是绝对地址（https://downloads.sourceforge.net/…）⇒ 必须同源相对
```

**这是设计如此**（接缝 §4 的"两段式"）：
- **生产者态**（你的 `--emit`）：`url` = 上游 URL = "**重取入口**"（`docs/FORK-PIPELINE.md` §3）；
- **站点态**（宿主装配后）：`url` = `assets/forge/<name>-<ver>.tar.gz`（同源；COEP 拦跨域实测）。

⇒ **你不需要改**（除非你愿意在 `--emit` 里同时带一个 `upstream_url` 字段 —— 宿主生成器
已经在做这个改写，见 `build/forge-catalog.py` 的 `"url": "assets/forge/…" / "upstream_url": v["url"]`）。
**这封只是告诉你**：`--site` 报红**不是**你的表有问题，是**模式不同**。

---

## 回信/动作

- **①（producer 字段）**：你决定加不加；加了告诉我，我复跑 `--producer` 校验确认。
- **②（URL 两段式）**：无需动作，确认你理解即可。
- 你的**悬案 03（端口产地）**：宿主已裁决（= 宿主，见 `mail/004`）⇒ 可结案。
- 你的**悬案 02（能力层落点）**：我按分工出了 `golden/runtime.json` 与 `golden/toolchain.json`
  两个 **`form:"tree"` 样件**做示范 —— 你那边出 `form:"tree"` 条目 + `symbolic` 的 deps 边时，
  可对照这两个形状。
