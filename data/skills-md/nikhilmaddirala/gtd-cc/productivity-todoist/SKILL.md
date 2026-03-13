---
name: productivity-todoist
description: Fetch and manage Todoist tasks. Use when the user asks about "todoist tasks", "show my tasks", "what's due", "overdue tasks", "triage tasks", or when another skill needs Todoist task context.
---

# Todoist

## Overview

Read Todoist tasks from synced markdown files and manage them via the Python SDK. Provides task context to other skills (e.g., life-coach planning) and allows direct task management from the CLI.

## Context

- Tasks are synced to `todoist-sync/tasks/` as markdown files with YAML frontmatter
- Sync freshness is tracked in `todoist-sync/sync-status.yml`
- Token stored at `~/.config/todoist-cli/config.json` (set up via `npx @doist/todoist-cli auth token`)
- Triage script uses `uv run --script` so dependencies are handled automatically
- For project structure, labels, priorities, and collaboration model, see the "Todoist organization reference" appendix in `todoist-sync/README.md`

## Process

### Step 1: Sync (always do this first)

Run the sync script to refresh local markdown files from Todoist:

```bash
./todoist-sync/scripts/sync.py
```

Or via justfile:

```bash
just todoist-sync
```

Check `todoist-sync/sync-status.yml` for last sync time. If the sync is recent (within the last hour), you can skip this step.

### Step 2: Read tasks from synced files

Tasks live at `todoist-sync/tasks/{project-slug}/{section-slug}/{task-slug}.md`.

Each file has YAML frontmatter:
```yaml
---
title: "Review Q1 invoices"
id: "6VpWpv2qfH9pm7fG"
project: "Work"
section: "Business ops"
priority: "p2"
labels: ["30-min", "admin"]
due: "2026-02-15"
recurring: false
created: "2026-02-01T12:00:00+05:30"
updated: "2026-02-08T12:00:00+05:30"
url: "https://app.todoist.com/app/task/..."
parent_id: null
---
```

To answer common queries, read the frontmatter:
- Today's tasks: find files where `due` is today or earlier
- Tasks by project: read from the project's subdirectory
- High priority: find files where `priority` is p1
- Tasks with label: find files where `labels` contains the label
- All tasks: read all `.md` files under `todoist-sync/tasks/`

### Step 3: Triage (write operations)

For modifying tasks (close, reschedule, label), use `scripts/todoist-triage.py`:

```bash
echo '[{"action": "drop", "task_name": "old task"}, {"action": "reschedule", "task_name": "deferred", "due_date": "2026-04-01"}]' | \
  ./scripts/todoist-triage.py
```

Actions: `drop` (add "dropped" label + close), `complete` (close), `reschedule` (update date), `someday` (add "someday" label + remove date)

After triage, run sync again to update the local files.

## Resources

- **todoist-sync/scripts/sync.py**: One-way sync from Todoist to markdown (run first)
- **todoist-sync/tasks/**: Synced task files (read these for current state)
- **todoist-sync/sync-status.yml**: Sync metadata (last sync time, counts)
- **scripts/todoist-triage.py**: Batch triage via Todoist API (drop/complete/reschedule/someday)

## Guidelines

- Always sync before reading tasks to ensure freshness
- Priority mapping: p1 (urgent/important), p2 (important), p3 (urgent, not important), p4 (neither). Todoist API inverts these: API priority 4 = p1, API priority 1 = p4.
- When reviewing tasks during planning: overdue tasks need a decision (reschedule, do today, or drop). Tasks with no due date need `--all` during weekly review.
- After any triage action, re-run sync to update the local markdown files
