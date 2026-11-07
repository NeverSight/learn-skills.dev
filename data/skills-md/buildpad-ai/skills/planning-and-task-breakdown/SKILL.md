---
name: planning-and-task-breakdown
description: Decomposes specs into implementable tasks. Use when you have a spec or feature description and need to break it into small, verifiable tasks with acceptance criteria and dependency ordering.
---

# Planning and Task Breakdown

## Overview

Decompose specifications into small, verifiable tasks with clear acceptance criteria and dependency ordering. Good planning prevents the "implement everything at once" anti-pattern and enables incremental delivery with verification at each step.

## When to Use

- You have a spec or feature description and need implementable units
- A feature is too large to build in one pass
- Multiple agents or developers will work in parallel
- You need to estimate effort or report progress

## Task Decomposition Process

### Step 1: Identify the Deliverables

From the spec, list every concrete deliverable:

```
Feature: Task Management

Deliverables:
1. Tasks collection, defined through `create-collection`
2. API route for CRUD operations
3. TypeScript interfaces
4. List page with CollectionList
5. Create/Edit form with CollectionForm
6. RBAC permissions (roles, policies)
7. Tests (API, page, E2E)
8. Documentation
```

### Step 2: Order by Dependencies

```
                ┌─── 3. Types ───────┐
1. Collection ──┤                    ├─── 5. Form ──┐
                └─── 2. API Route ───┤              ├─── 7. Tests
                                     └─── 4. List ──┘       │
                     6. RBAC ────────────────────────────────┘
                                                             │
                                                        8. Docs
```

### Step 3: Write Tasks with Acceptance Criteria

Each task should be:
- **Small** — completable in one sitting (~100 lines)
- **Verifiable** — has clear pass/fail criteria
- **Independent** — can be tested without other unfinished tasks
- **Committed separately** — each task = one commit

```markdown
### Task 1: Define the tasks collection
**Depends on:** Nothing
**Files:** the collection definition that the `create-collection` skill writes (a migration file on a Supabase project; calls to the Engine's API on an Engine project)
**Acceptance criteria:**
- [ ] The tasks collection has fields: id, title, status, date_created, date_updated
- [ ] Standard audit fields included (user_created, user_updated)
- [ ] Access for authenticated users: RLS policies on a Supabase project; roles, policies and permissions on an Engine project
- [ ] The definition applies without errors

### Task 2: Create tasks API route
**Depends on:** Task 1 (collection)
**Files:** app/api/items/tasks/route.ts
**Acceptance criteria:**
- [ ] GET returns paginated task list
- [ ] POST creates a task with validation
- [ ] Proxy pattern used (calls DaaS backend)
- [ ] API tests pass
```

## DaaS Layer Ordering

This skill feeds the `tasks.md` stage of spec-driven development (`/buildpad-spec-tasks`, or Kiro's native specs). Order tasks along DaaS dependency layers — each layer builds on the one before:

| Layer | Task Types |
|-------|-----------|
| Data | Collections (`create-collection`), API routes, types, API tests |
| UI | List pages, form pages, navigation, page tests |
| Logic | Validation hooks, RBAC setup, workflow definitions |
| Relations | Junction tables, relational fields, file uploads |
| Hardening | Error handling, performance, a11y, docs, E2E tests |

## Task Size Guidelines

```
~30 min  → Single change (collection definition, type definition)
~1 hour  → Small feature slice (API route + test)
~2 hours → Moderate slice (page + form + tests)
~4 hours → MAXIMUM for a single task — split further if larger
```

## Output Format

```markdown
## Implementation Plan: [Feature Name]

### Data Foundation
- [ ] Task 1.1: Define the collection (`create-collection`) — [acceptance criteria]
- [ ] Task 1.2: Create API route — [acceptance criteria]
- [ ] Task 1.3: Define TypeScript types — [acceptance criteria]
- [ ] Task 1.4: Write API tests — [acceptance criteria]

### Core UI
- [ ] Task 2.1: Create list page — [acceptance criteria]
- [ ] Task 2.2: Create form page — [acceptance criteria]
- [ ] Task 2.3: Add navigation — [acceptance criteria]
- [ ] Task 2.4: Write page tests — [acceptance criteria]

### Risks & Dependencies
- [Known risk 1 and mitigation]
- [External dependency and fallback]
```

## Parallelization with Subagents

Once tasks are ordered, independent branches of the dependency graph can run as parallel subagents (see `subagent-delegation`). Define any shared contract (API types, DaaS collection schema) as a first task, then fan out.

- **Safe to parallelize:** independent feature slices, read-only research, per-module reviews.
- **Keep sequential:** collection definitions (migrations on a Supabase project), shared-state changes, and anything on one dependency chain.
- Integrate and verify each subagent's result on the main thread before marking a task done.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Planning takes too long" | Debugging an unplanned implementation takes longer. |
| "I'll figure out the order as I go" | Dependency loops discovered mid-implementation cause rework. |
| "These tasks are too granular" | Granular tasks are verifiable. Vague tasks hide unknowns. |
| "We can parallelize everything" | Dependencies exist. Ignoring them causes integration failures. |

## Red Flags

- Tasks without acceptance criteria
- Tasks estimated at more than 4 hours
- No dependency ordering (just a flat list)
- Tasks that can't be independently tested
- Mixing different layers in a single task
- No risk identification

## Verification

After planning:

- [ ] Every spec requirement maps to at least one task
- [ ] Every task has acceptance criteria
- [ ] Dependencies are identified and ordered
- [ ] No task exceeds ~4 hours of estimated work
- [ ] Each task can be independently verified
- [ ] Tasks follow DaaS layer ordering and land in the spec's `tasks.md`
