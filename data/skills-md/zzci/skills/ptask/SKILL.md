---
name: ptask
description: Manage project tasks with docs/task/index.md and docs/task/PREFIX-NNN.md, including claim-before-work multi-agent coordination and immediate status sync. Use when users ask to create tasks, track progress, update task status, or coordinate implementation work. Supports English and Chinese content.
---

# Project Task

Maintain a compact task system in `docs/task/` with deterministic status updates.

## Hard Rules

1. Use English filenames only, even for Chinese content.
2. Keep one language per project/task file (follow user preference, otherwise follow existing project language).
3. Task index uses one-line entries only; all details go to detail files.
4. Claim before work; do not implement code before claim is complete.
5. Write status changes immediately; never defer.

## Language Mode

- Content can be English or Chinese.
- Filenames stay English in all cases (`index.md`, `PREFIX-NNN.md`).
- Keep one language per project unless the user explicitly asks to switch.

## Canonical Structure

```
docs/task/
├── index.md
└── PREFIX-NNN.md
```

- `index.md`: one-line status entries
- `PREFIX-NNN.md`: detail files (description, owner, dependencies, notes)

## Task Formats

### Index Entry

```markdown
- [ ] [**PREFIX-001 Short imperative title**](PREFIX-001.md) `P1`
```

### Index Entry (Chinese Content)

```markdown
- [ ] [**PREFIX-001 简短祈使句标题**](PREFIX-001.md) `P1`
```

### Detail File Template

```markdown
# PREFIX-001 Short imperative title

- **status**: pending
- **priority**: P1
- **owner**: (unassigned)
- **createdAt**: YYYY-MM-DD HH:mm

## Description

What needs to be done, with context and acceptance criteria.

## ActiveForm

Present-continuous description for spinner display.

## Dependencies

- **blocked by**: (none)
- **blocks**: (none)

## Notes

(Implementation notes, progress logs, or related links.)
```

### Detail File Template (Chinese Content)

```markdown
# PREFIX-001 简短祈使句标题

- **status**: pending
- **priority**: P1
- **owner**: (未分配)
- **createdAt**: YYYY-MM-DD HH:mm

## 描述

需要做什么，包含上下文和验收标准。

## 进行时描述

进行中的现在进行时描述（用于 spinner 显示）。

## 依赖

- **blocked by**: (无)
- **blocks**: (无)

## 笔记

（实现笔记、进度日志或相关链接。）
```

## ID, Marker, and Status Rules

### Task ID

- Format: `PREFIX-NNN` (uppercase prefix + zero-padded 3 digits)
- Sequence per prefix starts from `001`
- Never reuse or renumber IDs

### Status Markers

| Marker | Meaning | TaskUpdate status |
|--------|---------|-------------------|
| `[ ]`  | Pending | `pending` |
| `[-]`  | In progress | `in_progress` |
| `[x]`  | Completed | `completed` |
| `[~]`  | Closed / Won't do | `deleted` |

### Allowed detail `status` values

- `pending`
- `in_progress`
- `completed`
- `closed`

### Priority

- `P0`: blocking
- `P1`: high
- `P2`: medium
- `P3`: low

## Claim-Before-Work (Multi-Agent Safety)

Before writing any implementation code:

1. Read `docs/task/index.md`.
2. If marker is `[-]`, open detail file and check `owner`.
3. If owned by another agent, skip and pick another task.
4. Claim atomically:
   - Update index marker `[ ] -> [-]`
   - Update detail `status -> in_progress` and set `owner`
   - Call `TaskUpdate(status: "in_progress", owner: "<agent>")` if task tools are available
5. Start implementation only after all claim writes succeed.

On completion:

- Update index `[-] -> [x]`
- Update detail `status -> completed`
- Call `TaskUpdate(status: "completed")` if task tools are available

On close/won't do:

- Update index to `[~]`
- Update detail `status -> closed` and add reason in notes
- Call `TaskUpdate(status: "deleted")` if task tools are available

## Sync Rules

Primary source is `docs/task/` files.

- If `TaskCreate`/`TaskUpdate` tools are available, keep tool state synced with file state.
- If tools are unavailable, continue with file-only sync and mention that in updates.

Session checklist:

1. Session start: read `docs/task/index.md` and active detail files.
2. New task: create detail file first, then append index line.
3. Before work: complete Claim-Before-Work.
4. Session end: verify all statuses are persisted and update index header date.

## Project Initialization

On first use in a repository:

1. Ensure `CLAUDE.md` has a `## Project Task` section that references `/ptask` and claim-before-work.
2. Ensure `AGENTS.md` has the same section.
3. Ensure `docs/task/index.md` exists; initialize it if missing.

Recommended `CLAUDE.md` / `AGENTS.md` block:

```markdown
## Project Task

Use the /ptask skill to manage all tasks.
- Read `docs/task/index.md` before starting work.
- Every feature/fix has a task entry.
- Use `PREFIX-NNN` IDs; never reuse IDs.
- Claim task before implementation: index + detail + task tool sync.
- Update status markers in place after progress/completion.
```

Chinese content version (filenames still English):

```markdown
## Project Task

使用 /ptask 管理所有任务。
- 开始工作前先读 `docs/task/index.md`。
- 每个功能或修复都要有对应任务条目。
- 任务编号使用 `PREFIX-NNN`，禁止复用。
- 实现前必须先认领：索引 + 详情 + 任务工具状态同步。
- 进度和完成后原地更新状态标记。
```

## Update Rules

- In `index.md`, only update checkbox markers; never delete historical lines.
- In detail files, update fields in place; do not delete existing sections.
- Append new tasks at the end of `index.md`.

## Output Behavior

When reporting progress:

1. Summarize index changes.
2. List `[-]` and `[ ]` tasks.
3. List newly completed `[x]` tasks.

Keep updates concise and aligned with actual repository changes.
