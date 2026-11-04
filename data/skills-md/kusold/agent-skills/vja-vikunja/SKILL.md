---
name: vja-vikunja
description: Manage Vikunja tasks, projects, labels, and buckets using the vja CLI. Use for "add a task", "list my tasks", "mark task done", "edit task", "create a project", or "what's due" when Vikunja or vja is named or established as the task system.
metadata:
  author: mikekusold
  version: "1.0.0"
---

# Vja - Vikunja CLI Task Manager

Manage tasks on a Vikunja server using the `vja` command-line interface. `vja` is a CLI client for [Vikunja](https://vikunja.io), the open-source self-hosted task manager.

## Prerequisites

Check the installed version, then run a read-only command to check access:

```bash
vja --version
vja ls
```

Do not hide errors: distinguish a missing executable, incompatible API URL, authentication failure, and connection failure before suggesting a fix. These examples were checked against `vja 6.0.3`, which requires Vikunja >= 2.5.0 and an API URL ending in `/api/v2`. For other versions, consult `vja <command> --help` and the [upstream documentation](https://github.com/cernst72/vja). Do not change server configuration or install software unless the user requests it.

Configuration lookup order:

1. `$VJA_CONFIGDIR/config.rc`
2. `$XDG_CONFIG_HOME/vja/config.rc`
3. `~/.config/vja/config.rc`
4. `~/.vjacli/vja.rc` (legacy fallback)

Use the existing configuration location. Do not print credentials or token files.

## Resolve requests and verify changes

Use this skill when Vikunja or `vja` is the requested or established task system. A task in a code change, another task service, or a general project plan does not by itself select Vikunja.

- Use a task ID supplied by the user. For a title-based request, search with `vja ls --json --title="pattern"` and inspect IDs, titles, and projects before editing. Title, project, and label list filters use regular expressions; escape metacharacters for literal searches and check returned values. If several tasks fit and context does not resolve the target, ask which one.
- `vja ls` excludes completed tasks. Include `--include-completed` when looking for completed tasks, reopening a task, or checking whether an apparently missing task was already finished. Use `vja show ID --json` for a known task's current state.
- Apply the requested state: `--done=true` completes and `--done=false` reopens. Label edits toggle membership; inspect current labels and only toggle when the requested add/remove requires a change. Do not add `--force` unless creating the missing label is within the user's request.
- After adding or editing a task, read it with `vja show ID --json` and report the ID and resulting change. In vja 6.0.3, label edits return a task object captured before the label toggle, so that output alone does not verify label membership. If a request times out or a batch partly fails, inspect the affected state before retrying: adds and clones can duplicate tasks, while label toggles and deferrals can undo or repeat changes. Report unresolved outcomes instead of claiming success.

## Commands Reference

All task commands work as both `vja <command>` and `vja task <command>`.

### Adding Tasks

```bash
# Quick add to default project
vja add "Task title"

# Full options
vja add "Task title" \
  --note="Description text" \
  --priority=3 \
  --favorite \
  --due="tomorrow at 11:00" \
  --reminder \
  --label=@work \
  --project=1
```

Short flags: `-n` note, `-p` priority, `-f` favorite, `-d` due date, `-r` reminder, `-l` label, `-o` project

```bash
# Clone an existing task
vja clone 1 "Copy of task with this new title"
```

### Listing Tasks

```bash
# All active tasks
vja ls

# JSON output
vja ls --json

# Include completed tasks
vja ls --include-completed --json

# Specific tasks by ID
vja ls 10 13 14
```

**Sorting:**

```bash
vja ls --sort=id
vja ls --sort=-id          # reverse
vja ls --sort='due_date, -priority'
```

Default sort: `'done, -urgency, due_date, -priority, project.title, title'`

**Filtering:**

```bash
vja ls --project=1                          # by project ID
vja ls --project=projec                            # project name (regex)
vja ls --base-project=myproject             # base project
vja ls --label="^@work$"                    # exact label title
vja ls -l work                              # label (regex)
vja ls --due-date="before today"            # overdue
vja ls --filter="due_date ge today" --filter="due_date before in 5 days"  # due within range
vja ls --favorite=True                      # favorites only
vja ls --priority="gt 3"                    # priority greater than 3
vja ls --title=ask                          # title matches regex
vja ls -u                                   # urgency >= 4
vja ls --urgency=8                          # urgency >= 8
```

**Advanced filters:**

```bash
vja ls --filter="created after 2 days ago"
vja ls --filter="due_date before today in 7 days"
vja ls --filter="labels contains @work"
vja ls --filter="labels ne @work"
vja ls --filter="priority gt 2"
vja ls --filter="title contains clean up"
```

Filters can be combined:

```bash
vja ls --filter="labels ne @work" --project=1 --urgent
```

### Showing a Task

```bash
vja show 1
vja show 1 --json
vja show 1 2 3
```

### Editing Tasks

```bash
# Update properties
vja edit 1 --title="new title" --due-date="friday" --priority=1 --star
vja edit 1 --no-star

# Set due date with reminder
vja edit 1 --due="in 4 days at 15:00" -r

# Toggle label after checking current membership; --force creates a missing label
vja edit 1 -l @work

# Mark as done
vja edit 1 --done="true"

# Reopen a task
vja edit 1 --done=false

# Shortcut to toggle done
vja check 1

# Batch edit
vja edit 1 5 8 --due="next monday 14:00"
```

For "mark done" requests, use `--done=true`, which leaves an already completed task completed. `vja check` toggles a single task and can reopen it; use it only when toggling is requested.

### Deferring Tasks

```bash
# Defer by timedelta
vja defer 1 1d
vja defer 1 2w

# Batch defer
vja defer 1 2 3 1d
```

Moves a future due date forward by the given timedelta; for an overdue task, sets the due date to now plus that timedelta. Moves the first absolute reminder forward by the timedelta. Relative reminders stay relative to their configured date.

### Reminders

```bash
# Absolute time
vja edit 1 -r "next sunday at 11:00"

# Relative to due date
vja edit 1 -r "1h before due_date"
vja edit 1 -r "10m before due"

# Set reminder equal to due date
vja edit 1 -r

# Remove reminder
vja edit 1 -r ""
```

### Deleting Tasks

```bash
vja delete 1
vja delete 1 2 3
```

**Note:** No confirmation prompt — use carefully.

### Opening in Browser

```bash
# Open Vikunja starting page
vja open

# Open specific tasks in browser
vja open 42 43
```

### Managing Projects

```bash
# Add project
vja project add "New Project"

# Add subproject
vja project add "Subproject" -o 2
vja project add "Subproject" -o "parent-title"

# List projects
vja project ls

# Show project details
vja project show 1

# Open in browser
vja project open 1
```

### Managing Kanban Buckets

```bash
vja bucket add "Doing" --project=1
vja bucket ls --project-id=1
```

### Managing Labels

```bash
vja label add "Next action"
vja label ls
```

### Session

```bash
# Logout (removes local token)
vja logout
```

## Urgency

Tasks have an urgency score (displayed in the last column) calculated from:

- Due date proximity
- Priority
- Favorite status
- Keyword matches in project title
- Keyword matches in label titles

Weights and keywords are configurable in the active configuration file (normally `~/.config/vja/config.rc`) under `[urgency_coefficients]` and `[urgency_keywords]`.

## Priority Values

| Value | Meaning |
|-------|---------|
| 0     | Unset   |
| 1     | Low     |
| 2     | Medium  |
| 3     | High    |
| 4     | Urgent  |
| 5     | Do now  |

## Common Workflows

### Quick task capture
```bash
vja add "Fix the login bug" -p 2 -d "tomorrow" -l @work -r
```

### Daily review
```bash
vja ls --sort='-urgency' -u
vja ls --due-date="before tomorrow"
```

### Get things done
```bash
vja edit 1 --done=true
vja edit 2 3 --done=true
```

### Reschedule
```bash
vja defer 5 2d
vja edit 8 9 --due="next monday"
```
