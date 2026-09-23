---
name: change-linter
description: "改动 Python / Shell 文件后判定并执行 L1–L4 分级后置校验（ruff / ty / pyrefly / pyright / mypy / bash -n），并如实报告工具缺失导致的未校验缺口。Use after modifying .py or .sh files, before claiming a change is complete or reporting success; also when the user asks to run post-edit checks, lint, type-check, or verify that a change passes L1–L4."
compatibility: "Requires git and uv (which provides Python); ruff required, ty/pyrefly/pyright/mypy optional"
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/verify.py *)
---

# 改动分级后置校验

修改 `.py` / `.sh` 文件后，用本技能完成分级校验，再声称改动完成。

## 分工（别越界）

- **级别判定归你（模型）**：脚本不做级别推断。你必须先判定本次改动适用 L1–L4 中的哪一级，再传给脚本。
- **机械执行归脚本**：改动文件发现、工具探测、并行执行、汇总与退出码全部由 `scripts/verify.py` 负责。
- **不写仓库**：脚本只向 stdout 输出。默认把工具缓存隔离到临时目录（ruff 用 `--no-cache`、mypy 用临时 `--cache-dir`），不往项目里写任何文件；`--fast` 例外，它按你的选择改回项目缓存。
- **不跑测试**：本技能只做静态分级校验，不执行测试套件。测试状态按「汇报契约」处理，不因为要写汇报就把测试重跑一遍。

## 流程

1. **判级** — 按下方速查表判定级别；拿不准时取较高一级。
2. **执行** — 用 uv 跑脚本（uv 自带 Python，一条命令跨全平台，不依赖系统上有没有 `python`）：

   ```bash
   SKILL_DIR="${ZCODE_SKILL_DIR:-${CLAUDE_SKILL_DIR}}"   # 由 harness 展开自己的技能目录变量；都未展开时直接填本技能 base directory
   uv run --no-project "$SKILL_DIR/scripts/verify.py" --level L<N>
   ```

   - `uv` 不可用（报 `command not found`）时**才**退回系统解释器：Windows 用 `py -3`，其他系统用 `python3`；都没有就明确报「无法执行，本次改动未被校验」。注意 Windows 上 `python` 常是 Microsoft Store 的占位程序，命令存在 ≠ 可用。
   - **⚠️ 禁止 `python scripts/verify.py`**（相对路径只在 cwd 恰好是技能目录时才成立）。
   - 脚本靠 git 发现本次改动的 `.py` / `.sh`。**非 git 项目、或改动已提交导致发现不到时，改用 `--files` 显式指定**；不加 `--files` 时脚本会报「未校验」并退 1，不会静默判通过。
   - 自动发现会**排除本技能自身的安装副本**，排除数量会打印出来；确需检查这些文件时用 `--files` 显式指定。已删除的文件不会被送检；改动**仅为**删除文件时脚本空跑并报「无适用校验对象」。
   - 两个可选开关：**`--project-scope`**——判定为 L3/L4 且改动涉及公共接口 / 跨模块时加上，类型工具（ty/pyrefly/pyright/mypy）改扫整个项目；单文件检查抓不到「改签名破坏下游调用方」，此开关补上这个盲区，但会连带暴露项目存量类型错误，汇报时须区分存量与本次引入。**ruff 配置自动让位**——项目根有 `pyproject.toml`（含 `[tool.ruff]`）或 `ruff.toml` 时，脚本不传兜底参数，以项目自己的规则为准。
   - **复杂度随 L1 一起跑**：本次改动碰过的函数卡 8，同一次改动里没碰过的存量函数放宽到 12（8~12 记为「存量容忍」并打印出来）。它独立成一条 `complexity` 记录，与 ruff 风格检查分开；阈值判定在脚本内完成，不交给 ruff 退出码。
3. **处理缺失工具** — 脚本报告工具缺失时，**先问用户一次**是否安装；用户同意才加 `--install-missing` 重跑。
4. **汇报** — 输出 `verify:` 行；未真正校验的部分必须如实标注。

## 级别速查

| Level | 场景 | 校验内容 |
| --- | --- | --- |
| **L1** | 独立脚本（不会被 import / 调用的一次性脚本）；纯文档 / 注释 / 格式 / 空白变更 | ruff check + ruff format --check + C901 复杂度（新代码 >8 / 存量 >12）；Bash 为 `bash -n` |
| **L2** | 包内变更 / 会被 import / 调用的文件（含新增文件） | L1 + ty + pyrefly |
| **L3** | 跨模块交互 / 公共接口或类型签名变更 | L1 + L2 + pyright |
| **L4** | 大规模重构 / 核心模块 / 类型系统大范围变动 | L1 + L2 + L3 + mypy --strict |

裁决规则：取最高适用 Level；判定后打印 `后置校验 L<N>`。逐项命令、安装方式与缺失策略见 `references/lint-levels.md`。

## 缺失工具的处理（重要）

- `ruff` 缺失 → **硬失败**，不得降级放过；此时脚本改用 Python 自带的 `py_compile` 保住语法底线（只查语法，不含 lint 规则）。
- 类型检查器（ty / pyrefly / pyright / mypy）缺失 → 该级**降级并显式标注「该级未真正校验」**。
- `bash` 缺失 → 先回退探测 Git for Windows 的常见安装位置；两处都没有时该级判为未校验并明说「没有任何校验被真实执行」，不会静默跳过 `.sh`。
- `uv` 缺失 → 报告「缺少 uv，无法安装校验工具链」，本机由此无法补齐，交回用户处理。
- **解释器与 uv 都不存在** → 脚本根本无法执行；本次改动即**未被校验**，不得当成通过。
- 只有 `uv` 与缺失工具都存在时，才允许在**用户同意后**执行安装。

**绝不静默安装**：安装会改动用户全局环境，必须经用户明确同意；未被同意时把它作为待办明确交回用户。安装命令见 `references/lint-levels.md`。

## 其他语言的改动

本技能只校验 `.py` 与 `.sh`。修改其他语言（JS/TS/Go/Rust/YAML/JSON 等）时，由你按**项目原生工具链**自行校验（`package.json` 里的 scripts、`Makefile`、`go vet`、`cargo check` 等），并**在汇报里明确说明哪些校验做了、哪些没做**——不得因为本技能没报错就当作整体已通过。

## 汇报契约

最后必须给出可复核结论。全部通过时：

```
后置校验 L2
执行: L1 ✓ | L2 ✓
verify: 全部通过 (L2)
```

存在缺口时：

```
后置校验 L2
执行: L1 ✓ | L2 ⚠ 降级
缺失工具: ty → uv tool install ty --upgrade
verify: 未完全通过 — L2 因 ty 缺失未真正校验，不得视为已通过
```

测试不在本技能范围，**也不重复执行**：改动涉及可运行的测试时——本会话内已真实跑过并拿到结果的，直接引用（写明已跑、范围与结论），**不得重跑**；尚未跑过且改动确需测试验证时，才运行必要用例（优先定向用例，不默认全量）；两者都不成立时如实写明未跑。禁止留白，也禁止为凑汇报重复执行刚跑过的测试。

**严禁把未校验写成已完成**，也严禁省略缺失工具清单。
