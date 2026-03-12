---
name: infinite-dev
description: Infinite-running AI development system that builds complete software projects across unlimited context windows. Use this skill when the user wants to build a large project autonomously, run a long-running coding agent, set up an auto-dev loop, implement a complex app feature-by-feature, or mentions "infinite dev", "autonomous coding", "auto dev", "long-running agent", or wants Claude to keep building across sessions. Also use when the user has a feature_list.json or claude-progress.txt in their project, or mentions wanting to break a big project into incremental features.
---

# Infinite Dev: Long-Running Autonomous Development System

Build complete software projects across unlimited context windows using incremental progress, structured state tracking, and a Python CLI tool that drives the workflow.

Based on Anthropic's research on [effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## Architecture

```
状态持久化（跨所有上下文窗口）：
  • feature_list.json  — feature 清单，只改 passes 字段
  • claude-progress.txt — 结构化进度笔记（What was done / Testing / Notes）
  • Git history         — 代码变更记录

执行方式（用户二选一）：
  • Mode A (Interactive) — Claude 直接实现，/clear 清上下文
  • Mode B (Autopilot)  — dev-agent.py run 启动 claude -p 子进程循环
```

## Auto Setup

When this skill is triggered, Claude MUST automatically copy the required files to the project root:

1. Copy `dev-agent.py` from this skill's `scripts/` directory to the project root
2. Copy `AGENTS.md` from this skill's `templates/` directory to the project root
3. Then proceed to Initializer Mode or Coding Agent Mode depending on project state

Claude should resolve the skill path dynamically (the skill lives at the path where this SKILL.md is located).

## Initializer Mode — feature_list.json does not exist

Claude performs these steps automatically:

1. Read the project spec (spec.md, app_spec.txt, README, or ask the user)
2. Generate `feature_list.json` (20-200 features, sorted by priority)
3. Create `init.sh` (idempotent environment setup script)
4. Initialize git repo, first commit
5. Scaffold project structure
6. Create `claude-progress.txt`
7. Ask user: Mode A or Mode B? Then start Coding Agent Mode

## Coding Agent Mode A: Interactive

Claude 在当前会话内逐个实现 feature，完成后用 `/clear` 清理上下文。

```
Claude 读 AGENTS.md
  → init.sh → dev-agent.py status → dev-agent.py next
  → 实现 feature → lint → build → 浏览器测试
  → dev-agent.py complete → git commit → dev-agent.py log
  → 做了 2+ 个或上下文长了：
    "✅ 本轮完成。输入 /clear 后发送 go ahead 继续。"
  → 用户 /clear → go ahead
  → Claude 重新读 AGENTS.md → 继续
```

| 优势 | 劣势 |
|------|------|
| 能看到每一步操作 | 需要偶尔 /clear + go ahead |
| MCP / Playwright 正常工作 | |
| 不需要 --dangerously-skip-permissions | |

## Coding Agent Mode B: Autopilot

Claude 运行 `python dev-agent.py run`，脚本为每个 feature 启动独立 `claude -p` 子进程。

```
dev-agent.py run
  ├─ 读 feature_list.json → 找到 #3
  ├─ 启动 claude -p 子进程 → 实现 → 测试 → commit → 退出
  ├─ 读 feature_list.json → 找到 #4
  ├─ 启动 claude -p 子进程 → 实现 → 测试 → commit → 退出
  └─ 全部完成或达到限制 → 输出报告
```

| 优势 | 劣势 |
|------|------|
| 完全无人值守 | 需要 --dangerously-skip-permissions |
| 每个 feature 天然干净上下文 | MCP 可能不可用 |
| 不会上下文溢出 | 看不到实现过程 |

### Autopilot 参数

| Flag | Default | Description |
|------|---------|-------------|
| `--model <name>` | CLI 默认模型 | 覆盖模型 |
| `--max-features N` | 0（不限） | 最多做 N 个 feature |
| `--max-turns N` | 150 | 每个 feature 最大工具调用轮数 |
| `--timeout N` | 1800 (30min) | 每个 feature 超时秒数 |
| `--delay N` | 3 | feature 之间间隔秒数 |

## dev-agent.py Commands

| Command | Description |
|---------|-------------|
| `python dev-agent.py run` | Autopilot：每个 feature 一个 claude -p 子进程 |
| `python dev-agent.py run --parallel N` | 并行模式：同时跑 N 个 feature（worktree 隔离）|
| `python dev-agent.py status` | 显示进度（passing/total/skipped + 最近笔记）|
| `python dev-agent.py next` | 显示下一个要做的 feature（尊重优先级和依赖）|
| `python dev-agent.py find-parallel` | 显示可并行开发的独立 feature 列表 |
| `python dev-agent.py complete <id>` | 标记 feature 为通过 |
| `python dev-agent.py skip <id> [reason]` | 标记 feature 为跳过（记录原因）|
| `python dev-agent.py regression` | 随机选 1-2 个已通过 feature 做回归检查 |
| `python dev-agent.py log` | 追加进度到 claude-progress.txt（支持结构化格式）|

## Feature List Format

```json
[
  {
    "id": 1,
    "category": "functional",
    "priority": 1,
    "description": "User can open a new chat and send a message",
    "steps": [
      "Navigate to main interface",
      "Click 'New Chat' button",
      "Type a message in the input field",
      "Press Enter or click Send",
      "Verify AI response appears"
    ],
    "depends_on": [],
    "passes": false
  }
]
```

Rules:
- `priority`: 1 = 最高，数字越小越先做
- `category`: `functional` / `style` / `integration` / `performance`
- `depends_on`: 依赖的 feature ID 列表，依赖未通过则跳过
- `passes`: `false` → `true`（通过）/ `"skipped"`（跳过）
- **永远不要**删除、修改描述、修改步骤、合并或重排 feature

## Testing Strategy

### Web Apps
- Playwright MCP: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_take_screenshot`
- 通过真实 UI 测试，不只是 curl 或单元测试
- Run `npm run lint` and `npm run build` before marking pass

### Non-Web Projects
- 对应测试框架：`pytest` / `jest` / `go test` / `cargo test`
- Run linter (ruff/flake8/eslint) before marking pass
- 写集成测试，从用户视角验证

### Both
- 新 feature 开始前回归检查已通过的 feature
- 发现回归先修，再做新功能
- **Fix any errors before proceeding** — 不跳过失败的测试
- 只有 lint + build + 端到端验证全部通过才能标记 passes: true

## Team Mode (Parallel Development)

### 触发时机

在每完成一个 feature 后（Phase 4 结束时），检查是否适合开启并行：

```bash
python dev-agent.py find-parallel --count 3
```

如果满足以下条件，**主动询问用户**是否启用 Team Mode：
- 剩余未完成 feature >= 6
- 可并行的独立 feature >= 2
- 本次会话尚未询问过（避免反复打扰）

提示语：
> "检测到 N 个可并行开发的独立 feature（剩余 M 个），是否启用 Team Mode 并行开发？"

### Mode A 下的 Team Mode

在当前 Claude 会话内使用 Agent tool + worktree 并行开发：

1. 运行 `python dev-agent.py find-parallel --count 3` 找到独立 feature
2. 对每个 feature 用 Agent tool 启动 subagent（设置 `isolation: "worktree"`）
3. 各 subagent 在隔离 worktree 中实现 → 测试 → 提交
4. 合并分支，`python dev-agent.py complete <id>`
5. 清理 worktree

### Mode B 下的 Team Mode

使用 `dev-agent.py run --parallel N`，脚本自动处理 worktree 创建/合并/清理：

```bash
python dev-agent.py run --parallel 3          # 同时跑 3 个 feature
python dev-agent.py run --parallel 2 --max-features 6  # 并行 2，最多 6 个
```

并行执行流程：
1. `find_next_features(N)` 找到 N 个独立 feature
2. 为每个 feature 创建 git worktree（`.worktrees/feature-<id>`）
3. 同时启动 N 个 `claude -p` 子进程（各在自己的 worktree 中）
4. 等待全部完成
5. 逐个合并回主分支（`git merge --no-ff`）
6. 清理 worktree + 删除分支
7. 重新加载 feature_list.json，继续下一批

合并冲突处理：保留主分支，skip 冲突的 feature，记录原因。

适用于：50+ feature 待完成、feature 之间独立、用户要求加速。
