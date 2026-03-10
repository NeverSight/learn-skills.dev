---
name: ai-todo
description: "Manage tasks, track progress, and log daily updates via the ai-todo CLI. Triggers: 1) EXPLICIT — user mentions tasks, todos, progress tracking, standup, sprint planning, project management, or work logs. 2) POST-ACTION — after git commit/push, deploy, merge PR, release, or any milestone, proactively log progress and update/complete related tasks. When git-tools or vercel:deploy finishes, ALWAYS trigger this skill. 3) PRE-ACTION — when user discusses implementation plans, architecture design, feature breakdown, or sprint planning, suggest creating tasks. When brainstorming completes, convert outcomes into tasks. 4) SESSION-END — after substantial code changes, suggest a progress summary."
---

# AI Todo - Task Management for AI Agents

Manage tasks, track progress, and maintain daily work logs through the `ai-todo` CLI. This tool connects to ai-todo (https://ai-todo.stringzhao.life) for persistent, cross-session task management.

## Prerequisites

The `ai-todo` CLI must be installed and authenticated. Before running any command, check if credentials exist:

```bash
cat ~/.config/ai-todo/credentials.json 2>/dev/null
```

If not authenticated, run `ai-todo login` first.

If the `ai-todo` command is not found, install it:

```bash
npm install -g ai-todo-cli
```

## Command Discovery

Commands are **dynamically loaded from the server**. Do NOT memorize or hardcode commands. Always discover them at runtime:

```bash
# Step 1: Discover all available commands
ai-todo --help

# Step 2: View usage and options for a specific command
ai-todo <command> --help
# Example: ai-todo tasks:create --help
```

Key conventions:
- All commands output **JSON** — parse responses accordingly
- Parameters use `--key <value>` format
- Commands are namespaced: `tasks:*` for task operations, `spaces:*` for space operations
- Exit codes: 0=success, 1=error, 2=not authenticated (run `ai-todo login`)

## Workflow Patterns

### 了解任务结构（首要步骤）

在创建、更新或关联任务前，**必须先了解现有任务层级**：

```bash
ai-todo tasks:tree
```

输出树形文本，📌 标记项目空间，缩进显示父子关系。用于：
- 找到新任务应归属的项目空间或父任务
- 避免创建重复任务
- 理解当前任务拆分再添加子任务

**重要**：把任务放到正确的项目和父任务下，是保持任务系统可用的关键。不要在顶层随意创建任务。

### Starting a work session

Check existing tasks to understand priorities:
```bash
ai-todo tasks:tree
ai-todo tasks:list --filter today
ai-todo tasks:list --filter assigned
```

### Task creation from development context

When the user describes work or you identify actionable items:
1. Run `ai-todo tasks:tree` to see existing task structure
2. Find the correct parent task or project space for the new task
3. Create a parent task for the overall objective (or use an existing one)
4. Break it into subtasks using `--parent_id`
5. Set priorities based on dependencies and urgency
6. Use `ai-todo tasks:create --help` to see all available options

### Progress tracking during development

As you complete work, update tasks incrementally:
1. Starting a task: update progress to 10-20%
2. At checkpoints: increment progress
3. When done: complete the task
4. Always add a log entry describing what was accomplished

Use `ai-todo tasks:update --help` and `ai-todo tasks:add-log --help` for available options.

### Post-action workflow (after commit/deploy)

When a git commit, push, or deployment completes:
1. List tasks to find related ones
2. If related task exists: update progress, add a log, mark complete if done
3. If no related task: suggest creating one to record the completed work
4. Keep it lightweight — one log entry summarizing what was done

### Pre-action workflow (during planning/design)

When the user discusses implementation plans or feature breakdown:
1. Identify actionable items from the discussion
2. Create a task hierarchy to track planned work
3. Set priorities based on dependencies

### Cross-skill collaboration

- **After git-tools**: Log progress on related tasks
- **After vercel:deploy**: Log deployment and update/complete related tasks
- **After brainstorming**: Convert action plan into a task hierarchy

## Best Practices

- Write task titles as clear, actionable statements ("Implement X" not "X stuff")
- Use subtasks to break complex work into manageable pieces
- Update progress incrementally, not just at 0% and 100%
- Add log entries with specific details: "what was done" and "what's next"
- Use tags to categorize tasks by area (frontend, backend, infra, docs)
- Set realistic priorities — not everything is P0
