---
name: vikunja-vja
description: Manage Vikunja tasks via VJA CLI, supporting CRUD operations, assignment, priority, and labeling. Use for task-related requests like creating, listing, updating, or deleting tasks. Always append --json to commands for structured results, and pipe to jq for compact and filtered output where possible.
metadata:
  {
    "author": "akhy",
    "version": "1.0.0",
    "upstream": "https://vikunja.io",
    "openclaw":
      {
        "emoji": "✅",
        "homepage": "https://github.com/cernst72/vja",
        "requires": { "bins": ["vja", "jq"] },
        "install":
          [
            {
              "id": "uv-vja",
              "kind": "uv",
              "package": "vja",
              "bins": ["vja"],
              "label": "Install vja (uv tool install vja)",
            },
            {
              "id": "brew-jq",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Vikunja Tasks Skill

Manage tasks on a [Vikunja](https://vikunja.io) instance using the `vja` CLI.

Always use `--json` and pipe to `jq` for structured output. Title arguments are **positional** (not `--title`).

## Tasks

### Create
```bash
vja add "Task title"
vja add "Task title" -n "Description" -d "tomorrow" -p 3 -l urgent -A alice
vja add "Task title" -d "next monday at 9:00" -r "1h before due_date" -o "My Project"
```

Flags:
- `-n` / `--note` — description
- `-d` / `--due` — due date (natural language: `"in 3 days"`, `"2025-12-31"`)
- `--start` / `--end` — start/end dates
- `-p` / `--prio` — priority (1=low … 4=urgent)
- `-l` / `--label` — label name (repeat for multiple: `-l bug -l backend`)
- `-A` / `--assignee` — username to assign
- `-r` / `--reminder` — reminder (`"in 3 days at 18:00"`, `"1h before due_date"`)
- `-o` / `--project` — project name or id
- `-f` / `--star` — mark as favorite
- `--force-create` — create label if it doesn't exist yet

### List
```bash
vja ls --json | jq '.tasks[] | {id, title, due_date, priority}'

# Filter examples
vja ls --filter "done eq false" --json | jq '.tasks[] | {id, title}'
vja ls --filter "priority ge 3" --json | jq '.tasks[] | {id, title, priority}'
vja ls --filter "due_date before today" --json | jq '.tasks[] | {id, title, due_date}'
vja ls -l urgent --json | jq '.tasks[] | {id, title}'
vja ls -o "My Project" --json | jq '.tasks[] | {id, title}'
vja ls -u 3 --json | jq '.tasks[] | {id, title, urgency}'   # urgency >= 3
vja ls --all --json | jq '.tasks[] | {id, title, done}'     # include completed
vja ls --sort "-priority,due_date" --json | jq '.tasks[] | {id, title}'
```

Filter operators: `eq`, `ne`, `gt`, `lt`, `ge`, `le`, `before`, `after`, `contains`. Multiple `--filter` flags are ANDed.

### Show
```bash
vja show <task_id> --json | jq '{id, title, description, due_date, priority, assignees, labels}'
```

### Edit
```bash
vja edit <task_id> -i "New title"
vja edit <task_id> -n "Updated description"
vja edit <task_id> -a "Appended note"          # append to existing description
vja edit <task_id> -d "next friday" -p 4
vja edit <task_id> -l bug -l backend           # set labels
vja edit <task_id> -A alice                    # toggle assignee (adds if absent, removes if present)
vja edit <task_id> -c true                     # mark completed
vja edit <task_id> -f                          # star; --no-star to unstar
vja edit <task_id> -o "Other Project"          # move to project
```

### Delete
```bash
vja delete <task_id> -q
```

### Toggle done/undone
```bash
vja toggle <task_id>
```

### Defer due date
```bash
vja defer <task_id> 2d      # delay by 2 days (also shifts reminders)
vja defer <task_id> 1h30m
```

### Clone
```bash
vja clone <task_id> "New task title"
```

### Open in browser
```bash
vja open <task_id>
```

## Projects

```bash
vja project ls --json | jq '.[] | {id, title, parent_project_id}'
vja project show <project_id> --json | jq .
vja project add "Project name"
vja project add "Sub-project" -o "Parent Project"
```

## Labels

```bash
vja label ls --json | jq '.[] | {id, title}'
vja label add "new-label"
```

## User

```bash
vja user show --json | jq '{id, username, email}'
```

## Workflows

### Daily review
```bash
# Overdue tasks
vja ls --filter "due_date before today" --filter "done eq false" --json \
  | jq '.tasks[] | {id, title, due_date}'

# High-priority open tasks sorted by urgency
vja ls --filter "priority ge 3" --filter "done eq false" --sort "-urgency" --json \
  | jq '.tasks[] | {id, title, priority, urgency, due_date}'
```

### Create, assign, and label in one step
```bash
vja add "Review PR #42" -p 3 -d "today" -A alice -l review --force-create
```

### Bulk-defer overdue tasks
```bash
vja ls --filter "due_date before today" --filter "done eq false" --json \
  | jq '.tasks[].id' \
  | xargs -I{} vja defer {} 1d -q
```

### Complete a task and log it
```bash
vja toggle <task_id> -v --json | jq '{id, title, done}'
```

## Notes
- Dates support natural language via parsedatetime: `"tomorrow"`, `"next monday"`, `"in 3 days at 9:00"`, `"2025-12-31"`
- `--json` outputs Vikunja API JSON; `--jsonvja` outputs vja's internal representation
- Config is read from `~/.config/vja/config.rc` (or legacy `~/.vjacli/vja.rc`)
