---
name: writing-plans
description: Create implementation plans with tasks grouped by subsystem. Related tasks share agent context; groups parallelize across subsystems.
---

# Writing Plans

Write step-by-step implementation plans for agentic execution. Each task should be a **complete unit of work** that one agent handles entirely.

**Clarify ambiguity upfront:** If the plan has unclear requirements or meaningful tradeoffs, use `AskUserQuestion` before writing the plan. Present options with descriptions explaining the tradeoffs. Use `multiSelect: true` for independent features that can be combined; use single-select for mutually exclusive choices. Don't guess when the user can clarify in 10 seconds.

**Save to:** `**/plans/YYYY-MM-DD-<feature-name>.md`

## Plan Template

````markdown
# [Feature Name] Implementation Plan

> **Status:** DRAFT | APPROVED | IN_PROGRESS | COMPLETED

## Specification

**Problem:** [What's broken, missing, or needed. Describe the current state and why it's insufficient. Be specific enough that someone unfamiliar with the codebase understands the issue.]

**Goal:** [What the end state looks like after this work is done. Describe the user/developer experience, not the implementation.]

**Scope:** [What's in and what's out. Explicit boundaries prevent scope creep.]

**Success Criteria:**

- [ ] Criterion 1 (measurable/verifiable)
- [ ] Criterion 2

## Context Loading

_Run before starting:_

```bash
read src/relevant/file.ts
glob src/feature/**/*.ts
```

## Tasks

### Task 1: [Complete Feature Unit]

**Context:** `src/auth/`, `tests/auth/`

**Steps:**

1. [ ] Create `src/auth/login.ts` with authentication logic
2. [ ] Add tests in `tests/auth/login.test.ts`
3. [ ] Export from `src/auth/index.ts`

**Verify:** `npm test -- tests/auth/`

---

### Task 2: [Another Complete Unit]

**Context:** `src/billing/`

**Steps:**

1. [ ] ...

**Verify:** `npm test -- tests/billing/`
````

## Task Sizing

A task includes **everything** to complete one logical unit:

- Implementation + tests + types + exports
- All steps a single agent should do together

**Right-sized:** "Add user authentication" - one agent does model, service, tests, types
**Wrong:** Separate tasks for model, service, tests - these should be one task

**Bundle trivial items:** Group small related changes (add export, update config, rename) into one task.

## Parallelization & Grouping

During execution, tasks are **grouped by subsystem** to share agent context. Structure your plan to make grouping clear:

```markdown
## Authentication Tasks ← These will run in one agent

### Task 1: Add login

### Task 2: Add logout

## Billing Tasks ← These will run in another agent (parallel)

### Task 3: Add billing API

### Task 4: Add webhooks

## Integration Tasks ← Sequential (depends on above)

### Task 5: Wire auth + billing
```

**Execution model:**

- Tasks under same `##` heading → grouped into one agent
- Groups touching different subsystems → run in parallel
- Max 3-4 tasks per group (split larger sections)

Tasks in the **same subsystem** should be sequential or combined into one task.

## Rules

1. **Explicit paths:** Say "create `src/utils/helpers.ts`" not "create a utility"
2. **Context per task:** List files the agent should read first
3. **Verify every task:** End with a command that proves it works
4. **One agent per task:** All steps in a task are handled by the same agent

## Before Presenting

Before presenting the plan to the user, dispatch the `ce:devils-advocate` agent via Task tool to review it:

- Pass the full drafted plan text to the agent
- Load relevant domain skills based on what the plan involves. Evaluate which of these apply and include them in the agent prompt:
  - `Skill(ce:architecting-systems)` - system design, module boundaries, dependencies
  - `Skill(ce:managing-databases)` - database schemas, queries, migrations
  - `Skill(ce:handling-errors)` - error handling patterns
  - `Skill(ce:writing-tests)` - test strategy and quality
  - `Skill(ce:migrating-code)` - code migrations, API versioning
  - `Skill(ce:optimizing-performance)` - performance-sensitive work
  - `Skill(ce:refactoring-code)` - structural refactoring
- The agent will look for: unstated assumptions, missing edge cases, tasks that are too vague, missing dependencies between tasks, verification gaps
- Incorporate valid feedback into the plan
- Note what the review caught in a brief "Review notes" comment at the bottom of the plan

Skip this step only if the plan is trivial (< 3 tasks, single subsystem, no architectural decisions).

## Large Plans

For plans over ~500 lines, split into phases in a folder:

```
**/plans/YYYY-MM-DD-feature/
├── README.md           # Overview + phase tracking
├── phase-1-setup.md
└── phase-2-feature.md
```
