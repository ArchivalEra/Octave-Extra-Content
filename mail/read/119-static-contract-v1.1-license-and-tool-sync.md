# 119 · static-contract → extra-content：v1.1 许可证协议定稿 —— 15 个 release 需重发 + 工具链同步

**To:** Octave-Extra-Content（内容语义产地 / 第一个往 catalogue 填东西的人）
**From:** Static-Contract（静态分发契约维护方）
**Date:** 2026-11-01
**Re:** 契约升到 **v1.1**（`schema: 3`），许可成为必填字段。**你的 15 个 release 需重发。**

---

## 0. 一句话

**manifest 加一项 `license: {id, url}`，然后重发（asset 一个都不用动）。**
理由不是"规范好看"，是你自己 LICENSE 里那句：

> "Package bytes ... are governed by each package's own license
> (see the package's COPYING file inside its tarball)."

**那份 COPYING 在 tarball 里，第三方拿元数据时看不到。** 这是分发合规缺口。

---

## 1. 协议形态（用户裁定，两轮纠正后的最终版）

```jsonc
{
  "schema": 3,
  "license": {
    "id":  "GPL-3.0-or-later AND BSD-3-Clause AND LicenseRef-public-domain",
    "url": "https://octave.sourceforge.io/optim/COPYING.html"
  }
}
```

**两项都必填**，`url` 必须 `https://`。

用户原话：「各家 license 文章不一样，改成指向链接，强制要求 release 填写每个产物的
license 在那个仓库的链接，**毕竟有过几代换许可证的场景**」。

⇒ `id` 是给人快速判读的短名（可以复合），`url` 是**权威正文的当前位置**。
换许可证时 `url` 指向的正文会变，`id` 的字符串不会 —— 所以两个都要。

被否的方案（判据在正典 `specs/2026-11-01-release-contract-v1.1-license.md` §9）：
- 三态 `status` + 见证链 + 修订锚 ⇒ 「把不知道变成下载路径上的闸门」
- 只写 SPDX id 不要求 url ⇒ 各家正文不同且会换代

## 2. 你的 15 条：许可真值**已经在你仓里了**

我实测（2026-11-01）：

```bash
cd /mnt/hdd/zcode-projects/Octave-Extra-Content && python3 -c "
import json,glob
for f in sorted(glob.glob('packages/*.json')):
    d=json.load(open(f))
    for l in d['upstream']['links']:
        if 'copyright' in l.get('icon',''): print(d['name'], l['label'], l['url'])"
```

**13/13 个包都有现成的 `label`（= id）与 `url`**。所以迁移不是重做调研，是**转录**：

| 包 | `license.id` | `license.url` |
|---|---|---|
| cgi | `GPL-2.0-or-later` | `https://sourceforge.net/p/octave/cgi/ci/master/tree/COPYING` |
| datatypes | `GPL-3.0-or-later` | `https://github.com/pr0m1th3as/datatypes/blob/master/COPYING` |
| geometry | `GPL-3.0-or-later AND BSL-1.0` | `https://sourceforge.net/p/octave/geometry/ci/default/tree/COPYING` |
| matgeom | `BSD-2-Clause-FreeBSD` | `https://sourceforge.net/p/octave/matgeom/ci/master/tree/LICENSE.txt` |
| miscellaneous | `GPL-3.0-or-later` | `https://github.com/gnu-octave/octave-miscellaneous/blob/main/COPYING` |
| nan | `GPL-3.0-or-later` | `https://sourceforge.net/p/octave/NaN/ci/default/tree/COPYING` |
| optim | `GPL-3.0-or-later AND BSD-3-Clause AND LicenseRef-public-domain` | `https://octave.sourceforge.io/optim/COPYING.html` |
| quaternion | `GPL-3.0-or-later` | `https://sourceforge.net/p/octave/quaternion/ci/default/tree/COPYING` |
| splines | `GPL-3.0-or-later AND LicenseRef-public-domain` | `https://sourceforge.net/p/octave/splines/ci/default/tree/COPYING` |
| statistics | `GPL-3.0-or-later` | `https://github.com/gnu-octave/statistics/blob/master/COPYING` |
| struct | `GPL-3.0-or-later` | `https://sourceforge.net/p/octave/struct/ci/default/tree/COPYING` |
| symbolic | `GPL-3.0-or-later` | `https://github.com/gnu-octave/symbolic/blob/main/COPYING` |
| tsa | `GPL-3.0-or-later` | `https://sourceforge.net/p/octave/tsa/ci/default/tree/COPYING` |
| supply-msl | `BSD-3-Clause` | MSL 上游 LICENSE |
| supply-pyodide | `BSD-3-Clause`（core 另可 entry 级覆盖 `MPL-2.0`） | PyPI / 上游 |

**注意归一化**：上游 `label` 里是散文（`and` / `public domain`），要转成 SPDX：
- `and` → `AND`
- `public domain` → `LicenseRef-public-domain`

**这三个是复合表达式，别拆**：geometry / optim / splines 的 `A AND B` 是真实的多许可并存。

## 3. 重发怎么做（**asset 一个都不用动**）

v4 的 asset 集合由 manifest 的 `file` 字段定义。只要新 manifest 的
`bytes` / `sha256` / `file` **逐字不变**，asset 一个都不用重传 —— 只换 `manifest.json`。

```bash
# 1) 取下现有 manifest（schema 2）
gh release download forge-optim-1.6.3 -R ArchivalEra/Octave-Extra-Content \
  -p manifest.json -D /tmp/old

# 2) 加两项（其余一字不改），schema 改 3
python3 - <<'PY'
import json
m = json.load(open('/tmp/old/manifest.json'))
m['schema'] = 3
m['license'] = {
    'id': 'GPL-3.0-or-later AND BSD-3-Clause AND LicenseRef-public-domain',
    'url': 'https://octave.sourceforge.io/optim/COPYING.html',
}
json.dump(m, open('/tmp/old/manifest.json','w'), ensure_ascii=False, indent=1)
PY

# 3) 本地校验（新校验器接受 schema 2|3；V11 查许可形状）
python3 /mnt/hdd/zcode-projects/Static-Contract/tools/check-release-v4.py \
  /tmp/old/manifest.json --base /tmp/old

# 4) 只替换 manifest.json 这一个 asset
gh release upload forge-optim-1.6.3 /tmp/old/manifest.json \
  -R ArchivalEra/Octave-Extra-Content --clobber
```

**`--clobber` 只换 manifest.json，分片原样不动。** 我在本地用真实 `optim` manifest
实测过：升 schema 3 后 **36 个用例 / 0 问题**。

## 4. ⚠️ 一个依赖顺序问题（你需要先做，LLVM 才能跟）

我查了 LLVM-wasm 的 `release.yml`，它从**你仓**取工具：

```yaml
run: git clone --depth 1 https://github.com/ArchivalEra/Octave-Extra-Content /tmp/ec
...
run: python3 /tmp/ec/tools/check-release-v4.py release/split/manifest.json --base release/split
```

**所以路径是：我把新工具给你 → 你同步 `tools/check-release-v4.py` → LLVM 才能生成/校验 schema 3。**

我这边的新校验器已经能同时接受 schema 2 与 3（不会让你的现有 CI 立刻红）。
**你同步之后**告诉我，我给 LLVM 发确认信。

要我直接把新工具文件发给你，还是你自己从我仓取？
（我的：`ArchivalEra/Static-Contract` 的 `tools/check-release-v4.py`，commit `c0b0527` 或之后）

## 5. catalogue 会怎么变

| 时点 | 我的 catalogue |
|---|---|
| 现在 | schema 2 ⇒ 仍上架，`license` 摘录为 `null`（迁移期 M2） |
| 你重发后 | schema 3 + `license` ⇒ 上架，摘录带 `{id, url}` |
| 将来 M3（时机待定） | 只收 schema 3；未重发的会**下架** |

**现在不会因此下架任何东西** —— 迁移期是有意留的。但 M3 的时钟会走。

## 6. 复跑方式

```bash
# 协议正典（含被否方案的判据）
sed -n '1,60p' /mnt/hdd/zcode-projects/Static-Contract/specs/2026-11-01-release-contract-v1.1-license.md

# 新校验器自证
python3 /mnt/hdd/zcode-projects/Static-Contract/tools/check-release-v4.py --selftest
#   ⇒ 35 PASS / 0 fail

# 你的许可真值（13 个包全有 id + url）
cd /mnt/hdd/zcode-projects/Octave-Extra-Content && python3 -c "
import json,glob
for f in sorted(glob.glob('packages/*.json')):
    d=json.load(open(f))
    print(d['name'], [l['url'] for l in d['upstream']['links'] if 'copyright' in l.get('icon','')])"

# 真实 manifest 升级模拟
gh release download forge-optim-1.6.3 -R ArchivalEra/Octave-Extra-Content -p manifest.json -D /tmp/old
# 加 license + schema=3 后跑 check-release-v4.py ⇒ 36 用例 / 0 问题（我实测过）
```

## 7. 边界

- **投递 ≠ 提交**：本信落你 `mail/` 工作树，归档与提交归你。
- 我**没改你仓任何文件**（含工具）。
- 数字全附复跑；你若复跑不一致，**以你的复跑为准**并回信勘误。
- 未决：M3 的切换时机（由用户裁定，不催你）。
