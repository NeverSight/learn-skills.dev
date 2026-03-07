---
name: groove-utilities-task-analyse
description: "Analyse task status and distribution across the configured backend."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-task-analyse

## Outcome

Tasks are summarised by status. Milestones and epics are summarised. Completed tasks include enough resolution detail for memory population bullets. Output is suitable for daily end and daily memory.

## Acceptance Criteria

- Tasks grouped by status: in-progress, todo/ready, blocked, completed, scrapped
- Milestones/epics show progress (X of Y tasks done)
- Completed tasks include resolution summary (not just title)
- Output contains enough detail to write meaningful daily memory bullets without re-reading tasks

## Constraints

- Read `tasks:` and `task.analyse_limit` (optional; default 30) from `.groove/index.md`
- If `tasks: none`, no-op with friendly message
- Backend mappings:
  - `beans`: (1) run `skills/groove-utilities-task-list/scripts/list-tasks-by-priority.sh [LIMIT]` for active tasks (LIMIT from `task.analyse_limit` or 30); (2) run `beans list --json --status completed` and `beans list --json --status scrapped` for completed/scrapped; merge, group by status, then summarise (milestones/epics and resolution detail as per acceptance criteria)
  - `linear`: fetch all assigned issues via linear CLI or MCP, group by state
  - `github`: `gh issue list --state all --assignee @me`, group by label/state
- For completed tasks: include the body's "Summary of Changes" section if present
- If a completed task has no resolution, note that it is missing — do not omit the task
- Output format should be scannable markdown (headers per status group, bullet per task)
