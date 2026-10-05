---
name: bitrix24-tasks
description: 'Bitrix24 on-premise tasks in PHP: V2 commands (AddTaskCommand), TaskProvider, CTaskItem compat, responsible and accomplices, checklist, templates, TaskAccessController, OnTaskAdd events. Use when creating, reading, securing or hooking tasks.'
---

# Bitrix24 tasks (server side)

Scope: Bitrix24 on-premise · Verified: tasks 26.300.100, main 26.800.0

| Task | Read |
| --- | --- |
| Pick the API layer; create, update, complete, delete; errors | `rules/writing.md` |
| One task or lists: filters, sort, paging, dates | `rules/reading.md` |
| Members, deadlines and time zones, checklists, tags, projects, templates, comments | `rules/details.md` |
| Access actions, events and their arguments, REST mapping | `rules/access-events.md` |

## Invariants

- Write through the V2 commands (`AddTaskCommand`, `UpdateTaskCommand` …; legacy `CTaskItem`/`CTasks` end in the same V2 services). Never write `TaskTable` or member/checklist tables: counters, chat, search, events and recycle bin are skipped.
- Commands do not check rights. Check `TaskAccessService`/`TaskAccessController` for the acting user before `run()`.
- Pass the acting user id explicitly (`userId` in configs). Agents and CLI have no `$USER`; `CTasks::Add` without `USER_ID` acts as user 1.
- Dates in V2 entities are Unix timestamps (`deadlineTs`). Never pass site-format strings from background code.
- Keep V2 calls in one `/local` gateway class: commands take `V2\Internal\…` entities and configs that may change between releases. The V2 layer is verified in tasks 26.300.100 only; if `class_exists(AddTaskCommand::class)` is false, use `CTaskItem`.
- New task card: comments are messages in the task chat (see `rules/details.md`, `bitrix24-im`).
