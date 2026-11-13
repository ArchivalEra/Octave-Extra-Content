# shellcheck allowlist（2026-11-12 首扫 13 条 finding 的逐条裁定）

> 工具：shellcheck 0.11.0（`shellcheck -x`）。扫描面 = 本仓全部 5 个 shell 文件
> （`reflect-hooks/einfacht-env.sh` / `pre-commit` / `pre-push` / `gates-selftest.sh`
> / `.kimi-code/hooks/kimi-hook`）。**真代码零 finding**——13 条全部落入下表 4 条
> 惯用形规则，逐条核源码定性误报；CI 用 `-e` 排除（quality-assessment.yml ⑦ 步）。

| 规则 | 条数 | 定性 | 判据 |
|---|---|---|---|
| SC1007（`=` 后空格） | 8 | **POSIX 惯用法误报** | `CDPATH= cd -- "$dir"` 是「清空 CDPATH 再 cd」的标准惯用法——那个空格是环境变量赋值的分隔，不是赋值语句的空格。行为实测正确（`sh -c 'CDPATH= cd -- /tmp'` → `/tmp`）。预提交/pre-push/gates-selftest/einfacht-env 共 4 个文件的同款行 |
| SC1090（non-constant source） | 3 | **插件契约本体** | `einfacht-env.sh` 的 env 文件位置在运行时解析（钩子目录优先/仓根回落）——这正是 issue #8 的「可拔插件」设计；静态化路径反而破坏契约。kimi-hook 的 `EINFACHT_PLUGIN_DIR=… . …` 同理 |
| SC1091（not following） | 1（info，`-x` 下出现） | 同上 | 跨文件 follow 在插件契约下不可静态解析 |
| SC2016（single-quote no-expand） | 1 | **自证夹具故意不展开** | `einfacht-env.sh:58` 的 printf 写假钩子 fixture——`$0` 必须以字面量进文件（fixture 在 `--selftest` 的临时目录里自建 `$0` 语境），展开反而破坏自证 |

## 复跑

```bash
# 全量（13 finding，与本表对账）
shellcheck -x reflect-hooks/einfacht-env.sh reflect-hooks/pre-commit \
  reflect-hooks/pre-push gates-selftest.sh .kimi-code/hooks/kimi-hook
# allowlist 后（应 rc=0 = 真代码零 finding）
shellcheck -e SC1007,SC1090,SC1091,SC2016 reflect-hooks/einfacht-env.sh \
  reflect-hooks/pre-commit reflect-hooks/pre-push gates-selftest.sh \
  .kimi-code/hooks/kimi-hook
```

## CI 收录

`quality-assessment.yml` ⑦ 步（`shellcheck-gates`）：pip 装 `shellcheck-py`，
同 `-e` allowlist，rc 如实进 results.tsv。规则语义：**外部验证既有壳，不是新 lint**
——allowlist 变更须过本表（每条给判据），不许静默加 `-e`。
