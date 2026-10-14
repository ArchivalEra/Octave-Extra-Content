# 供给配方 · Pyodide + SymPy（符号计算的共享能力层）

> **性质**：**配方**（从哪取 + 什么 sha + 体积），**不是字节**。字节由宿主 provision 到站点
> （同源硬约束）。**上游 = [pyodide/pyodide](https://github.com/pyodide/pyodide)（BSD-3-Clause）+ SymPy（BSD-3-Clause）**。
>
> **为什么它在"额外内容"里**：Forge 的 `symbolic` 包是**纯 `.m`** 却全靠 Python/SymPy 干活，
> 而本构建 wasm 里 `pyexec`/`pyeval`/`pycall` 字节数**全 = 0**、也无 shell ⇒
> **包原样跑不了**，必须有一个真 Python 运行时。它不是"某个包的字节"，是**多个包共用的能力层**
> （另一个同类 = clang 工具链）。

## 上游身份

| 项 | 值 | 出处 |
|---|---|---|
| Pyodide | **314.0.7** | `gh release list -R pyodide/pyodide` |
| Python | 3.14（Pyodide 内建） | 浏览器实测 `pyodide.version` |
| SymPy | **1.14.0**（PyPI 官方字节） | `https://pypi.org/pypi/sympy/1.14.0/json` |
| mpmath | **1.4.1**（SymPy 依赖） | `https://pypi.org/pypi/mpmath/1.4.1/json` |
| 许可 | Pyodide = MPL-2.0（`pyodide` 仓 LICENSE）；SymPy/mpmath = BSD-3-Clause | 各自仓 |

## 资产清单（三分件，逐件 sha256）

| 资产 | 来源 URL | 字节 | sha256 |
|---|---|---|---|
| `pyodide-core-314.0.7.tar.bz2` | `https://github.com/pyodide/pyodide/releases/download/314.0.7/pyodide-core-314.0.7.tar.bz2` | **6,757,104** | `2abdcc2e35208af406e07724cffa85bc582ced97e9028383ecf5462541393f95` |
| `sympy-1.14.0-py3-none-any.whl` | PyPI（经 JSON API 解析实际文件 URL） | **6,299,353** | `e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5` |
| `mpmath-1.4.1-py3-none-any.whl` | PyPI（同上） | **567,787** | `dc4f0ea2304480d4a9a48a94c1020571558ade522b44a6912efac63a586e140f` |

**解包后**：`pyodide/` 目录 ≈ **20.99 MB**；站点新增（解包 + 轮子）≈ **27.54 MB**。

## ★ 一个身份坑（实测抓到，别改回去）

**PyPI 的 sympy 轮子 ≠ pyodide-core 自带 lock 里记的字节** —— pyodide 对纯 Python 包会
**去掉测试再打包**（lock 里 `unvendored_tests: true` 就是这个意思），所以两边 sha 不同：

| 包 | pyodide lock 里记的 sha（前 16） | PyPI 官方字节的 sha（前 16） |
|---|---|---|
| sympy 1.14.0 | `61ea8bb98049ba1c` | `e091cc3e99d2141a` |
| mpmath 1.4.1 | `e5ebd537e74b9066` | `dc4f0ea2304480d4` |

而 pyodide 的标准 CDN（`cdn.jsdelivr.net/pyodide/...`）在部分网络**连不通**（实测 `curl http=000`）。
⇒ **供给走 PyPI 官方字节，并把托管副本的 `pyodide-lock.json` 里这两条的 sha 改写成实际字节的 sha**
（我们才是供给方 —— pin 的必须是"我们放上去的字节"）。宿主侧已有 `overlayLock` 实现与记录
（`test/browser/probe-pyodide-sympy.mjs`）。

## 实测性能（决定"要不要用它"，出处 = 宿主台账 `sympy_*` 键）

| 项 | 值 | 说明 |
|---|---|---|
| 冷启动 | Pyodide 装载 ~1.7 s + 装 sympy 包 ~0.5 s | 懒加载即可，**不进开机路径** |
| 稳态（vs 原生 CPython） | **2.01×** | 15 个 CAS op 几何均值；逐项 1.6–3.2× |
| vs 原生 Octave + `symbolic` | 浏览器档**快 3.69×** | 后者每 op 要过管道做变量编组 |
| `.pyc` 预编译 | `import sympy` **7.4×**（2.71→0.37 s）、稳态 **0.99×（不变）** | 收益集中在冷启动；代价 = 字节 3.28× |
| 浏览器无隐式字节码缓存 | 源码档**二次 import 仍 2.73 s** | ⇒ 每次冷启动重编 472 个模块（原生有 `__pycache__`，浏览器 site-packages 只读） |

## pin 载体

| 层 | 载体 | 谁核对 |
|---|---|---|
| 运行时身份 + 字节 | `URL + sha256`（宿主 `build/upstream-lock.json` 一组） | 宿主 `zreflect/check_locks.py` |
| 站点副本 | **provision 产物**（可删可重建 = 缓存） | provision 脚本逐件核 sha |

## 复跑命令

```bash
gh release list -R pyodide/pyodide
python3 -c "import json,urllib.request;d=json.loads(urllib.request.urlopen('https://pypi.org/pypi/sympy/1.14.0/json').read());print(d['urls'][0]['digests']['sha256'])"
sha256sum /mnt/hdd/octave-wasm-build/symprobe/cache/pyodide-core-314.0.7.tar.bz2 \
          /mnt/hdd/octave-wasm-build/symprobe/cache/sympy-1.14.0-py3-none-any.whl \
          /mnt/hdd/octave-wasm-build/symprobe/cache/mpmath-1.4.1-py3-none-any.whl
# 浏览器侧前提实测（5/0）：sh test/browser/run.sh test/browser/probe-pyodide-sympy.mjs   [宿主仓内跑]
```

## 待办（本仓视角）

- [ ] 宿主 `build/upstream-lock.json` 加这一组（三条）；`provision-pyodide.sh`（宿主侧动作）
- [ ] `packages/symbolic.json` 建档时标**能力层需求**（`needs: ["pyodide"]`，见仓根 README 的诚实说明）
- [ ] 许可台账：把 Pyodide/SymPy/mpmath 三条写进宿主 `THIRD-PARTY-NOTICES.md`（宿主侧动作）
