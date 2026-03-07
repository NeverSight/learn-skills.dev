---
name: groove-daily-end
description: "End the workday: write memory, analyse tasks, run end hook. Use when wrapping up the day."
license: MIT
allowed-tools: Bash(git:*) Read Write Edit AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-daily-end

## Outcome

The workday is wrapped up: git changes are analysed, memory files are written in order, tasks are analysed, and the end hook is executed if present.

## Acceptance Criteria

- Git memory file written at `<memory>/git/YYYY-MM-DD-GIT-N.md`
- Daily memory file written at `<memory>/daily/YYYY-MM-DD.md`
- Weekly memory file written if today is the last weekday of the week
- Monthly memory file written if today is the last weekday of the month
- Tasks are analysed and summary is included in daily memory

## Constraints

- Read `.groove/index.md` for `tasks:`, `memory:`, and `git.*` config
- Call `/groove-utilities-task-analyse` to get task summary for daily memory population
- Memory population order (must follow this sequence):
  1. `/groove-utilities-memory-log-git`
  2. `/groove-utilities-memory-log-daily`
  3. `/groove-utilities-memory-log-weekly` (only if last weekday of week, or explicit request)
  4. `/groove-utilities-memory-log-monthly` (only if last weekday of month, or explicit request)
- Last weekday detection: use local calendar date; handle gracefully if run on weekend
- Do NOT modify tasks during end
- After all standard steps: check if `.groove/hooks/end.md` exists
  - If it exists: read the `## Actions` section and execute each item in order; report completion per item
  - If it does not exist: skip silently
