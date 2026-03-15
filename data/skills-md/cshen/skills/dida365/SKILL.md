---
name: dida365
slug: dida365
version: 1.0.0
description: Manage TickTick/Dida365 tasks and projects from the terminal. List, create, complete, update, and delete tasks and projects via the Dida365 Open API.
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":["python3","curl"]},"os":["linux","darwin"]}}
---

# Dida365 — TickTick Task Manager ✅

Manage your [TickTick](https://ticktick.com) / [Dida365](https://dida365.com) tasks and projects directly from the CLI. Pure Python, zero external dependencies.

## Prerequisites

- `TICKTICK_TOKEN` environment variable must be set with a valid Dida365/TickTick Open API bearer token
- If the token is missing, **stop and tell the user** to set it: `export TICKTICK_TOKEN="..."`
- Token can be obtained at https://developer.dida365.com/manage

## Tool Location

The CLI script is bundled with this skill:

```
{baseDir}/tt.py
```

All commands follow the pattern:

```bash
python3 {baseDir}/tt.py <command> [options]
```

## When to Use This Skill

Activate when the user wants to:
- List, view, or check their tasks or to-do items
- Add, create, or schedule a new task
- Complete, finish, or check off a task
- Delete or remove a task
- Update, edit, reschedule, or reprioritize a task
- List, create, or delete projects (task lists/folders)
- Anything related to TickTick, Dida365, their calendar tasks, or daily planning

**Trigger phrases:** "add a task", "what are my tasks", "mark it done", "show my to-dos", "create a project", "schedule", "my dida365", "ticktick", "what's on my plate", "to-do list", "任务" (Chinese for task), "待办" (to-do)

## Commands Reference

### List Projects

```bash
python3 {baseDir}/tt.py projects
```

Returns all projects with their IDs and names. Use project IDs or names in other commands.

### List Tasks

```bash
# Inbox (default)
python3 {baseDir}/tt.py tasks

# Specific project (by name or ID)
python3 {baseDir}/tt.py tasks --project "Work"
python3 {baseDir}/tt.py tasks --project 6478a1b2c3d4e5f6a7b8c9d0
```

Shows pending (incomplete) tasks sorted by priority then start date.

### Add a Task

```bash
python3 {baseDir}/tt.py add "Task title" [options]
```

| Option | Description | Default |
|---|---|---|
| `--project <name\|id>` | Target project | inbox |
| `--priority <none\|low\|med\|high>` | Priority level | none |
| `--start <YYYY-MM-DDTHH:MM:SS>` | Start date (timezone auto-appended) | — |
| `--notes <text>` | Description body | — |
| `--tag <tag1,tag2>` | Comma-separated tags | — |

**Examples:**

```bash
# Simple task
python3 {baseDir}/tt.py add "Buy groceries"

# Full options
python3 {baseDir}/tt.py add "Deploy v2.0" \
  --project Work \
  --priority high \
  --start 2026-03-20T18:00:00 \
  --notes "Run regression suite first" \
  --tag "release,urgent"
```

Returns the created task's ID — save it for complete/update/delete operations.

### Complete a Task

```bash
python3 {baseDir}/tt.py complete <taskId> [--project <name|id>]
```

If `--project` is omitted, inbox is assumed.

### Update a Task

```bash
python3 {baseDir}/tt.py update <taskId> [options]
```

| Option | Description |
|---|---|
| `--project <name\|id>` | Project the task belongs to (default: inbox) |
| `--title <text>` | New title |
| `--priority <none\|low\|med\|high>` | New priority |
| `--start <YYYY-MM-DDTHH:MM:SS>` | New start date |

### Delete a Task

```bash
python3 {baseDir}/tt.py delete <taskId> [--project <name|id>]
```

### Add a Project

```bash
python3 {baseDir}/tt.py add-project "Project Name" [--color "#FF6B6B"]
```

### Delete a Project

```bash
python3 {baseDir}/tt.py delete-project <projectId>
```

## Important Details

### Date Format
- User provides: `YYYY-MM-DDTHH:MM:SS` (e.g., `2026-03-20T18:00:00`)
- The script auto-appends `+0800` (Asia/Shanghai timezone)
- The API requires RFC 822 offset format (`+0800`, **not** `+08:00`)

### Priority Mapping
| User says | Flag value | API value |
|---|---|---|
| none | `none` | 0 |
| low | `low` | 1 |
| medium | `med` or `medium` | 3 |
| high | `high` | 5 |

### Project Resolution
- `inbox` → built-in inbox project
- A 24-char hex string → used as-is (it's already an ID)
- Anything else → case-insensitive name lookup via the API

### Error Handling
All errors print to stderr and exit code 1. Common issues:
- `TICKTICK_TOKEN not set` — user needs to export the token
- `Project 'X' not found` — check project name with `projects` command
- API errors — token may be expired or invalid

## Behavioral Rules

1. **Always run commands with `python3`** — the script has no shebang-based auto-execution guarantee.
2. **When the user asks to add a task**, ask for the brief task description at minimum, which is the notes for the command line.  Infer priority/project/date from context if the user provides them naturally. Summarize the task details using no more than 10 words in ENGLISH and use that as the task title.
3. **When the user says "my tasks" or "what's on my plate"**, default to listing inbox tasks. Ask which project if they have context suggesting a specific one.
4. **After creating a task**, report the task ID back to the user — they'll need it for complete/update/delete.
5. **After completing or deleting**, confirm the action with the task ID.
6. **If a command fails**, read stderr output and explain the issue to the user in plain language.
7. **Never hardcode task IDs** — always get them from `tasks` output or `add` output first.
8. **Quote titles and notes** that contain spaces when building the command.
