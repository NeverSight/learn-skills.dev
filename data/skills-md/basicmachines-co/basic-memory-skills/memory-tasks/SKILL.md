---
name: memory-tasks
description: "Task management via Basic Memory schemas: create, track, and resume structured tasks that survive context compaction. Uses BM's schema system for uniform notes queryable through the knowledge graph."
---

# Memory Tasks

Manage work-in-progress using Basic Memory's schema system. Tasks are just notes with `type: Task` — they live in the knowledge graph, validate against a schema, and survive context compaction.

## When to Use

- **Starting multi-step work** (3+ steps, or anything that might outlast the context window)
- **After compaction/restart** — search for active tasks to resume
- **Pre-compaction flush** — update all active tasks with current state
- **On demand** — user asks to create, check, or manage tasks

## Task Schema

Tasks use the BM schema system (SPEC-SCHEMA). The schema note lives at `memory/schema/Task.md`:

```yaml
---
title: Task
type: schema
entity: Task
version: 1
schema:
  description: string, what needs to be done
  status?(enum): [active, blocked, done, abandoned], current state
  assigned_to?: string, who is working on this
  steps?(array): string, ordered steps to complete
  current_step?: integer, which step number we're on (1-indexed)
  context?: string, key context needed to resume after memory loss
  started?: string, when work began
  completed?: string, when work finished
  blockers?(array): string, what's preventing progress
  parent_task?: Task, parent task if this is a subtask
settings:
  validation: warn
---
```

## Creating a Task

When work qualifies, create a note in `memory/tasks/YYYY-MM-DD-short-name.md`:

```markdown
---
title: Descriptive task name
type: Task
status: active
created: YYYY-MM-DD
current_step: 1
---

# Descriptive task name

## Observations
- [description] What needs to be done, concisely
- [status] active
- [assigned_to] claude
- [started] YYYY-MM-DD
- [current_step] 1

## Steps
1. [ ] First concrete step
2. [ ] Second concrete step
3. [ ] Third concrete step

## Context
What future-you needs to pick up this work. Include:
- Key file paths and repos involved
- Decisions already made and why
- What was tried and what worked/didn't
- Where to look for related context
```

### Key Principles

- **Steps are concrete and checkable** — "Implement X in file Y", not "figure out stuff"
- **Context is for post-amnesia resumption** — Write it as if explaining to a smart person who knows nothing about what you've been doing
- **Use observations for BM-queryable fields** — `[status]`, `[description]`, `[assigned_to]` etc. become searchable in the knowledge graph
- **Relations link to other entities** — `parent_task [[Other Task]]`, `related_to [[Some Note]]`

## Resuming After Compaction

On session start or after compaction:

1. **Search for active tasks:**
   - Via BM: `search_notes("type:Task status:active")` or `search_notes("[status] active")`
   - Via memory_search: query "active tasks" (composited search includes task scanning)

2. **Read the task note** to get full context

3. **Resume from `current_step`** using the `context` field

4. **Update as you progress** — increment `current_step`, update context, check off steps

## Updating Tasks

As work progresses, update the task note:

```markdown
## Steps
1. [x] First step — done, resulted in X
2. [x] Second step — done, changed approach because Y
3. [ ] Third step — next up

## Context
Updated context reflecting current state...
```

Update frontmatter too:
```yaml
current_step: 3
```

## Completing Tasks

When done:
```yaml
status: done
completed: YYYY-MM-DD
```

Add a brief summary of what was accomplished and any follow-up needed.

## Pre-Compaction Flush

When a compaction event is imminent:

1. Find all active tasks: `search_notes("type:Task status:active")`
2. For each, update:
   - `current_step` to reflect actual progress
   - `context` with everything needed to resume
   - Step checkboxes to show what's done
3. This is **critical** — context not written down is context lost

## Querying Tasks

With BM's schema system, tasks are fully queryable:

| Query | What it finds |
|-------|--------------|
| `search_notes("type:Task")` | All tasks |
| `search_notes("[status] active")` | Active tasks |
| `search_notes("[status] blocked")` | Blocked tasks |
| `search_notes("[assigned_to] claude")` | My tasks |
| `search_notes("type:Task [blockers]")` | Tasks with blockers |
| `schema_validate(noteType="Task")` | Validate all tasks against schema |
| `schema_diff(noteType="Task")` | Detect drift between schema and actual task notes |

## Guidelines

- **One task per unit of work** — Don't cram multiple projects into one task
- **Externalize early** — If you think "I should remember this", write it down NOW
- **Context > steps** — Steps tell you what to do; context tells you why and how
- **Close finished tasks** — Don't leave completed work as `active`
- **Link related tasks** — Use `parent_task [[X]]` or relations to connect related work
- **Schema validation is your friend** — Run `bm schema validate Task` periodically to catch incomplete tasks
