---
name: ticktick
description: >
  Manage TickTick tasks and projects for JMO. Use when the user asks to add,
  create, or capture a task or todo; list, show, or review pending tasks;
  complete or check off a task; update a task's priority, due date, notes, or
  tags; delete a task or list; create or manage a project/list; or see what's
  due today or overdue. Also handles quick captures like "remind me to..." or
  "don't let me forget...".
metadata:
  author: 0juano
  version: "1.1.0"
---

# TickTick

Manage tasks and projects via `scripts/tt.sh`. Full API reference in `references/api.md`.

**Auth:** `TICKTICK_TOKEN` env var (set in shell from Infisical).
**Timezone:** All dates in ART (America/Buenos_Aires, UTC-3). Script appends `-03:00` automatically.
**Inbox ID:** `inbox131039472`

## Quick Reference

```bash
# Load token (if not already in env)
export TICKTICK_TOKEN=$(infisical secrets get TICKTICK_TOKEN \
  --token="$INFISICAL_TOKEN" --projectId="$INFISICAL_PROJECT_ID" \
  --env=prod --plain 2>/dev/null | tail -1)

TT="bash /root/.openclaw/workspace/skills/ticktick/scripts/tt.sh"
```

## Commands

### List projects
```bash
$TT projects
```

### List tasks
```bash
$TT tasks                          # inbox (default)
$TT tasks --project "Work"         # by name
$TT tasks --project <projectId>    # by ID
```

### Add a task
```bash
$TT add "Buy tennis grip"
$TT add "Call accountant" --priority high --due "2026-02-20T10:00:00"
$TT add "Draft email" --project "Work" --priority med --notes "Reply to Yarilin"
$TT add "Review PR" --tag "work,code"
```
Priority values: `none` | `low` | `med` | `high`

### Complete a task
```bash
$TT complete <taskId> --project <projectId>
# Inbox tasks: --project flag optional (defaults to inbox)
```

### Update a task
```bash
$TT update <taskId> --project <projectId> --priority high
$TT update <taskId> --title "New title" --due "2026-02-25T09:00:00"
```

### Delete a task
```bash
$TT delete <taskId> --project <projectId>
```

### Manage projects
```bash
$TT add-project "Tennis"           # creates new list
$TT add-project "Work" --color "#FF5733"
$TT delete-project <projectId>
```

## Workflow

1. **Quick capture** — if no project specified, task lands in Inbox
2. **Find taskId** — run `$TT tasks` or `$TT tasks --project X`, copy the id from output
3. **Find projectId** — run `$TT projects`, copy the id

## Display Format

When showing tasks to JMO, format like this:
```
📋 Inbox — 3 pending

  ○ [HIGH]  Call accountant            — due Feb 20
  ○ [MED]   Review BT analytics
  ○         Buy tennis racket grip
```
Sort by: priority (high first), then due date. Hide completed tasks unless asked.
