---
name: groove-utilities-task-archive
description: "Archive a completed task in the configured backend."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-task-archive

## Outcome

All completed and scrapped tasks are archived in the configured backend. The count of archived tasks is reported to the user.

## Acceptance Criteria

- All completed/scrapped tasks are moved to archived state in backend
- User is shown the scope of what will be archived and confirms before running
- Count of archived tasks is reported after completion

## Constraints

- Read `tasks:` from `.groove/index.md` to determine backend
- If `tasks: none`, no-op with friendly message
- Always show user what will be archived and ask for confirmation before proceeding
- Never run automatically during daily end — only when user explicitly requests
- Backend mappings:
  - `beans`: `beans archive` (archives all completed/scrapped — no single-task option)
  - `linear`: mark filtered issues as archived via linear CLI or MCP
  - `github`: close resolved issues via `gh issue close`
- Report count of archived tasks after completion
