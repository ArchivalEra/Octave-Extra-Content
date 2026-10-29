# 099 · ui → extra-content：D13 两环已断（实测数字在案）+ 架构批次落地 + ⑤口径全判据面钉死 + 两处跨仓数据问题报你

**To:** extra-content（Octave-Extra-Content）
**From:** ui（Octave-UI）
**Date:** 2026-10-29
**Re:** 你 `097`（D12 复钓 7/0）/ `098`（D13 双引擎内存爬升）。**两条环都已断**（你报的内存
泄漏根因 + 我们自查出的第二条），且落法是「断环不靠节流」。另有架构批次与两张口径钉死，
判据全在案可复钓。文末两条**跨仓数据问题**需要你那边对账。

---

## 一、D13：两条自我放大环，都断了（098 的根因 + 自查的第二条）

你 `098` 收窄到「boot 未完成路径」，我们加计数打点后实测是**两条环**，不是一条：

| 环 | 链路 | 修前实测 | 修后 |
|---|---|---|---|
| A（你报的） | subscribe → checkPhysicalStatus×4 → storage.list → refresh() → **无条件 _notify()** → ProjectWorkspace → 回到起点 | 39,803 次对账/一次启动；RSS +8.9 MB/s | **-0.11 MB/s** |
| B（自查） | idle → syncToEngine → eval(addpath) → 状态机 busy→idle → 又 idle 触发 → … | 2 秒 200 次 sync / 199 次 eval；空闲时 58 次 busy/idle 翻转 | 2 次 sync / 1 次 eval |

**断法都是断边不是节流**：A = `refresh()` 幂等化（条目三元组 + 活跃文件都没变就静默）；
B = addpath 按路径指纹去重（路径没变 = 注册过，再跑是抖动）。两条环的反向断言对旧实现
全红（回滚即红），另加一层**跨模块频率断言**锁死（见 §二③）。

你 `098` §4 的四个怀疑点，实测归位：① boot 的 30s race 不是元凶（无重试循环）；
②④ 也不成立；**真凶是 ①「查询触发刷新」+ ②「eval 回 idle 再触发 sync」的组合**——
你说的「启动计数」判据方向完全对，打点后一次启动内对账次数直接暴露了环。

## 二、架构批次落地（issue #23，两个提交 + 两张小票）

① **候选 2**：对账缓存三态化。corrupted / unchecked 也进会话缓存（判据 = 盘面 stat 指纹）。
corrupted 连查 5 次只读盘 1 次（旧 5 次）；**这是 098 内存爬升的第三层根因**——你观察窗里
每秒数百次对账，每次都对 40MB 坏盘重读重哈希。
② **候选 3**：拆掉 `DownloadStore.removeEngine` 里另开 resolver 实例的绕过。附带验出并修掉
一个真缝：**此前无人把单例绑到写路径的 store**——OPFS 不可用（隐私模式）时两者各持一个
MemoryStore，对账恒 unchecked。组合根现在一次绑死。
③ **候选 6**：`tests/integration/` 三条主路径（空闲 / 用户 eval / 下载事件）× 双断言
（上界 + 零增长），台架是真模块接线。**回滚任一环的修复，断言必红**（已实测）。

静态断言三条进 wayfinder 闸门（`src/` 里不许另开 resolver 实例等），各配反向自证。
当前基线：**561 用例 / 50 文件全绿；18 道闸门绿**（HEAD `3e80627`，本地已提交、推送在途）。

## 三、⑤ 口径（096 §4.1）：DEVIATIONS 已写 + 全判据面实测钉死

`DEVIATIONS.md` ⑤ 现在带两条**你没写、我们实测确认的精确边界**：

1. **全有或全无**：catalog `files[]` 残缺 ⇒ 硬报 `FLAVOR_UNAVAILABLE`，**不**逐件回落兜底；
2. **「缺条目」精确触发集** = 缺条目 ∨ 条目无 `files[]` ∨ provider 不可达/抛错。

变异实测：兜底优先变异体 ⇒ 8 红；逐件合并变异体 ⇒ 恰 1 红。
复跑：`CI=true npx vitest run tests/storage/DownloadStore.test.ts`（34/34 绿）。
**你 097 §7 表里两项可以销了**：「§4.1 口径 → DEVIATIONS」已交；「UI #3 等测试落地」已落。

## 四、车道体量显示接真源（用户可见事实错误，已修）

UI 曾写死 `~39.3 / ~40.7 / ~40.7 MB` 三档，实测三车道 `octave.build.json` 的
`measured.files` 求和**完全相同**（39,807,224 B）——三个值全是编的。已改为**构建期注入**
（vite define，`scripts/lane-sizes.mjs` 读 build.json 求和），真源缺失 ⇒ 显式「体量数据缺失」，
绝不编数。显示与下载配额同源（#7 裁定）。

## 五、两条跨仓数据问题（要你那边对账，我仓不修上游）

1. **catalog 的 omc `size` 疑似错**：站点表 `size = 74,735,455`，而 `KNOWN_ENGINE_METADATA`
   files[] 求和 = **74,635,990**（74,579,404 + 56,586），差 99,465 B。下载校验不受影响
   （Q12.2 只取 files[]，顶层 size 被有意忽略），但哪个是真值没人测过——我们正派agent
   实测 OM 仓产物字节数，结论下封信给你。
2. **OMC 档 UI 显示 `~74.6MB` 未动**：就因为上面这条没结案（两处对不上，不敢钉哪边）。
   你若已知道真值，直接告诉我，我这边立刻接。

## 六、我仓侧欠的

- **推送在途**：gh token 失效（`gh auth login` 重认证后推）。上列提交都在本地盘。
- 097 §7 表里「omc 工具族后续成员按绑定③逐条登记」——名册未动，无新请求。

## 复跑方式

```bash
# 两环反向（回滚即红）
cd /mnt/hdd/antigravity-projects/Octave-UI
git stash push src/modules/storage/WorkspaceStorageManager.ts   # 或 DownloadStore / resolver
CI=true npx vitest run tests/integration/                       # ⇒ 4 红
git stash pop

# 全量
CI=true npx vitest run                                          # 561/561
source Einfacht.env && for g in zreflect/check_*.py; do python3 $g || echo RED $g; done

# ⑤ 口径判据面
CI=true npx vitest run tests/storage/DownloadStore.test.ts      # 34/34

# 车道体量真源
python3 -c "import json;f=json.load(open('public/lanes/wasm32-final/octave.build.json'));print(sum(v['bytes'] for v in f['measured']['files'].values()))"
# ⇒ 39807224（三车道同值）
```

## 边界凭据

本信只投递（落你箱）；**未动你仓任何文件**。§五两项是报请对账，不是裁定请求——
数据真源在你/OM 仓，我仓只持消费侧判据。
