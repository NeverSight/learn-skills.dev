---
name: groove-utilities-task-create
description: "Create a new task in the configured backend."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-task-create

## Outcome

A task is created in the configured backend with a title, type, status, optional parent, and (for non-trivial tasks) a rich body. The task ID is returned for reference. This command is the single source of truth for how tasks are created — other skills (work compound, daily, etc.) that need to create tasks must follow this spec and call this skill rather than defining their own creation rules.

## Acceptance Criteria

- Task exists in backend with all required fields populated
- Task ID is shown to user after creation
- Non-trivial tasks (feature work, bugs, plans, stage tasks) have a rich body — never create with an empty body when the task represents real work or a stage
- Parent is set when context suggests one (e.g. stage task under a daily or work epic)

## Constraints

- Read `tasks:` from `.groove/index.md` to determine backend
- If `tasks: none`, no-op with friendly message
- If title not provided in arguments, ask user for title and type before proceeding
- Infer parent from current context (open tasks, recent work) and confirm with user if ambiguous
- Default status is `in-progress` (not `todo`) — tasks are created when work is being done
- Do not auto-mark any task as completed during creation
- Backend mappings:
  - `beans`: `beans create "<title>" -t <type> --parent <id> -s in-progress`; body via `beans update <id> -d "<body>"` or by editing the task file under `.groove/tasks/` if the backend is file-based
  - `linear`: create issue via linear CLI or MCP with appropriate team/project
  - `github`: `gh issue create --title "<title>" --body "<body>" --milestone <milestone>`
- **Body (standard):** For any non-trivial task, always supply a body. Use the backend's body/description field (or task file content). Standard body sections: **Context** (what work or session this task belongs to), **Goal** (what "done" means at a high level), **Acceptance Criteria** (checklist of concrete conditions), **Links** (to CHANGELOG, specs, learned files, or other artifacts). Omit a section only if it truly does not apply.
- **Type:** Use the backend's types (e.g. beans: `task`, `bug`, `feature`, `epic`, `milestone`). Stage and bookend tasks (daily Start/End, work stages such as "YYYY-MM-DD, Compound — topic") use type `task` when the backend has no `chore` (e.g. beans).
- **Hierarchy:** Set parent when the task is part of a larger unit (e.g. a daily, an epic). If the caller does not specify a parent, infer from context when possible.
- Always echo the created task ID and title back to the user
