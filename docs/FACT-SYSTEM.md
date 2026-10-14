# 事实系统（Einfacht）与它的用法（2026-10-14）

> **性质**：操作手册。**为什么一个"档案仓"需要事实系统**、怎么接、踩过哪些坑。
> **来源**：`Octave-Full-Wasm` 的实际接入（2026-10-09 采纳，2026-10-10 追平上游 C1–C5），
> 本文按**本仓（Octave-Extra-Content）的角色**裁剪。所有"坑"都是实测的。

---

## §0 为什么本仓需要它（这不是"给别人看的花架子"）

**本仓的产品就是一堆"断言"**：
"这个包的这个版本 sha 是 X"、"这个包装得上（`verified`）"、"这个配方的 URL 取回来是 Y 字节"。
一条断言没了"谁能复跑"，它就**只是印象** —— 而印象会被照抄，照抄是说假话的唯一来源
（宿主仓一天内抓到过 5 处照抄出的假话）。

**Einfacht 做的事一句话**：**让每句「现在如此」都能被一条命令复跑证明**。三块：

| 块 | 作用 | 本仓对应 |
|---|---|---|
| **事实台账** | 数字/断言 + **每条旁写复跑命令**，闸门每次提交逐字执行 | `build/FACTS.json`（**已建立**，2026-10-14 接入完成） |
| **翻案台账** | 被推翻的断言登记在册；它**重新出现**时报错 | `build/retractions.json` |
| **悬案台账** | 未结案的问题，每条挂**可跑的结算件** | `.scratch/open-questions/issues/` |

**机制层从上游 vendored**（`zreflect/` 机制 + `reflect-hooks/` 钩子 + `gates-selftest.sh`），
**数据层是本仓唯一要写的文件**（`zreflect/measure_extra_content.py`）—— 换仓库只换那个文件。

---

## §1 接入六步（照抄，逐步可验）

1. **vendor 机制层**：取上游 [Einfacht](https://github.com/ArchivalEra/Einfacht) 的
   `zreflect/*.py` + `reflect-hooks/*` + `gates-selftest.sh`，**排除上游的 `measure_*.py`**。
2. **写本仓数据层** `zreflect/measure_extra_content.py`：定义 `measure()`，
   把本仓"量到的事实"收成 dict；每条 `fact(value, cmd, …)` 的 **`cmd` 必须是能跑的裸命令**（见 §3 坑 3）。
3. **配旋钮** `reflect-hooks/Einfacht.env`（见 §3 坑 1、坑 2）。
4. **装钩子**：`sh reflect-hooks/install.sh`（= `git config core.hooksPath reflect-hooks`）。
   **不装 = 一套没人执行的闸门，而日志一切正常**（§3 坑 4）。
5. **首台账 + 机器块**：`python3 zreflect/facts.py --render-doc STATE.md`。
6. **自证**：`sh gates-selftest.sh`（平台闸门自证，含"换仓库名字全换"的反向断言）。

---

## §2 三条纪律（上游 C1–C5，本仓照收）

| 纪律 | 含义 | 对本仓的意义 |
|---|---|---|
| **C1 谓词=声明，不是文件名** | 执行面读 `registry --run <相位>`；频率是声明字段 `runs_at`，不是命名 | 本仓将来加闸门（如 `check-recipes.py`）**只需一条声明行**，不用改执行面 |
| **C2 off ≠ 通过** | `gate.off()` 打 `OFF:` 标记（rc 仍 0），执行面聚合 `ran/off/failed` | "全绿"不许把"没跑"算进去（宿主实测过 `ran 8 / off 5` 的假全绿） |
| **C4 "必须一致"要配对账器** | 声明旋钮 ⊆ 实读旋钮、登记表 ⊆ README 表……各配可复跑对账 | **没有对账器的"必须一致" = 迟早不一致**（本仓例：`verified` 标了但从未 `--probe` 过 ⇒ 要有对账） |

---

## §3 ★ 实测踩过的坑（照抄会踩）

### 坑 1 · `Einfacht.env` 行尾 `#` 注释会被并进值里
`export X="v"  # 注释` —— sh **只在单词开头**才把 `#` 当注释 ⇒ 值变成 `v"  # 注释`
⇒ 闸门拿着带注释尾巴的路径去查文件 ⇒ 报"不存在"。**注释只能单独成行。**

### 坑 2 · "配置了就必须存在"的旋钮不能全局配
`REFLECT_LOCKS`/`REFLECT_PINS`/`REFLECT_INSTRUMENTS`/`REFLECT_DOCTOR` 这类：
全局配 ⇒ 自证台的**跨仓库夹具**（临时目录、没有那些文件）里 FATAL
⇒ 误报"名字写死在代码里"（宿主实测）。⇒ **一律内联**传给需要它的那次调用。

### 坑 3 · `cmd` 必须是**裸命令**，且 stdout 只打值
复跑闸门会**逐字执行** `cmd` 并把 stdout 与台账比对。写中文散文 ⇒ rc=127；
输出多于一个值 ⇒ 不符。`sha256sum` 默认带路径列 ⇒ 要 `| cut -d' ' -f1`。

### 坑 4 · hooks 不装 = 从未生效
`git config core.hooksPath` 指向哪，闸门就在哪。**装完用一次真提交验证它拦得住**
（故意放一条错断言 ⇒ 必须红）。CI 是第二保险（pre-push 可被 `--no-verify` 跳过，
但本仓纪律**禁用 `--no-verify`**）。

### 坑 5 · 台账会"改口"，改口要有受管辖的入口
重跑测量 ⇒ 值变了 ⇒ 闸门**拒绝**（"未经接受的改口"）⇒ 用 `--accept-changes` 显式接受。
**这条本身是纪律**：数值变了必须有人点头，不许静默改。

---

## §4 本仓的第一批事实（建议表 → **已落地**，2026-10-14）

> ⚠️ **本表是配方期的建议**；实际落地的键见 `build/FACTS.json`（12 条）。落地时按采集器
> 契约（`zreflect/collect.py` 原则 2）**剔除了 `content_pin` 一条**（见下），并补了几条
> 规模事实（版本条目总数 / 含 `.oct` 的包数 / 配方字节数）。散文里引用一律用 `[[键名]]`。

| 键（建议） | 量什么 | `cmd`（裸命令，自本仓根） |
|---|---|---|
| `shelf_packs` | 包档案数 | `ls packages/*.json \| wc -l` |
| `shelf_verified` | 已实测验证的包数 | `grep -l '"verified": {' packages/*.json \| wc -l` |
| `tool_selftest_pass` | 工具自证通过数 | `python3 tools/forge-shelf.py --selftest \| grep -c '^PASS'` |
| ~~`content_pin`~~ | ~~本仓当前 tip~~ | ~~`git rev-parse HEAD`~~ —— **不采用**：tip 每提交都变 ⇒ 违反采集器原则 2（`--check` 永不收敛）。已进翻案台账 `R-001`；要引用 tip 就在正文写命令 |
| `llvm_bundle_sha` | 配方引用的工具链 bundle sha | `sha256sum /mnt/hdd/zcode-projects/LLVM-wasm/release/llvm-wasm-bundle-v0.1.1.tar.gz \| cut -d' ' -f1` |
| `pyodide_core_sha` | 配方引用的运行时 sha | `sha256sum /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2 \| cut -d' ' -f1` |

**★ 两条规矩**：① 数字**只写进台账**，散文里一律引用键名，**不许手抄**；
② 写不出一条复跑命令的断言 ⇒ 不许进台账（只能进 HISTORY 当历史）。

---

## §5 复跑命令（验证接入成功）

```bash
python3 zreflect/facts.py --render-doc STATE.md --check    # 机器块新鲜
python3 zreflect/registry.py --run commit                  # ran/off/failed 三档
sh gates-selftest.sh                                       # 平台闸门自证
python3 .githooks/check-whitelist.py                       # 白名单覆盖（本仓同样适用）
python3 zreflect/check_facts_replay.py                     # 每条 cmd 逐字复跑
```

---

## §6 与姊妹仓的关系

- **机制层同源**：宿主 `Octave-Full-Wasm`、`OpenModelica-Full-Wasm` 与本仓可用**同一套** `zreflect/`；
- **数据层各写各的**：宿主 = `measure_octave.py`；OM 仓 = `measure_openmodelica.py`；
  本仓 = `measure_extra_content.py`（建议名）。
- ⚠️ 若将来三仓都接了：**升级机制层要三仓同批**（否则闸门口径漂移），
  判据 = 各仓 `sh gates-selftest.sh` 全绿。
