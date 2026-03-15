---
name: eng-agent-task-breakdown
description: This skill should be used when the user asks to "break down tasks", "create a task list", "plan implementation", "decompose architecture", "create agent tasks", "plan MVP build", "break down feature", "create execution plan", or mentions task breakdown, agent development workflow, or implementation planning. Two-phase workflow for AI agent development with granular, testable tasks.
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# Agent Task Breakdown

Break architecture into executable tasks. Build them one at a time with AI agents.

---

## Phase 1: Task Decomposition

### Task Format

```markdown
## Task [N]: [Title]

**Depends on:** [Task numbers this requires, or "None"]

**Outcome:** [What exists when done - one sentence]

**Why:** [What this unblocks]

**Acceptance:** [How to verify - specific test, expected result]

**Human action:** [External setup needed, if any]
```

### Sizing Rules

Right size:
- Changes ONE testable thing
- 5-30 min agent implementation time
- Failure cause is obvious and isolated

Split if:
- Multiple independent things to test
- Multiple files for different reasons
- Acceptance has multiple unrelated conditions

### Content Rules

**Outcomes, not implementation.**

Bad: "Create users table with id, email, created_at using Prisma"
Good: "Database stores user records with unique emails and timestamps"

Bad: "Install React Query and create useUser hook"
Good: "User data fetches efficiently with caching"

The agent knows their tools. Define success, not steps.

**Risk-first ordering.**

Put uncertain/complex tasks early. Fail fast on hard problems. Don't save integrations and edge cases for the end.

Typical flow: setup > risky core logic > database > API > UI > integration

**Dependencies explicit.**

Every task lists what it needs. Enables parallel work and failure impact analysis.

### Output Structure

```markdown
# [Project] Tasks

## Prerequisites
[External setup: accounts, keys, env vars]

## Tasks
[Ordered task list with dependencies]

## Out of Scope
[What's NOT in this MVP]
```

### Validation Checklist

Before starting execution, verify:

- [ ] Every task has exactly ONE acceptance test
- [ ] No task depends on something not yet defined
- [ ] Risky/uncertain work is front-loaded
- [ ] All external config is in Prerequisites, not buried in tasks
- [ ] A junior dev could verify each acceptance criteria
- [ ] No task requires unstated knowledge to complete

### Anti-Patterns

**Too big:** "Build the auth system" - This is 5+ tasks disguised as one.

**Too small:** "Create the Button component" then "Add onClick to Button" - Combine unless genuinely separate concerns.

**Hidden dependency:** Task 8 needs an API key not mentioned until Task 8. Put it in Prerequisites.

**Vague acceptance:** "User flow works correctly" - Works how? What's the test?

**Implementation-as-outcome:** "Use Redux for state management" - That's a how, not a what.

---

## Phase 2: Task Execution

### Before Starting

1. Read architecture doc fully
2. Read task list fully
3. Understand the end state before writing code
4. If ANYTHING is ambiguous, ask. Don't assume.

### Per-Task Protocol

1. State which task you're starting
2. Write minimum code to pass acceptance
3. State exactly what to test and expected result
4. STOP. Wait for confirmation.
5. Pass → commit, announce next task
6. Fail → fix the specific issue only, don't expand scope

### Coding Rules

```
DO:
- Write absolute minimum code required
- Focus only on current task
- Keep code modular and testable
- Preserve existing functionality

DO NOT:
- Make sweeping changes
- Touch unrelated code
- Refactor unless task requires it
- Add features not in current task
- Optimize prematurely
- Assume - ask instead

WHEN HUMAN ACTION NEEDED:
- State exactly what to do
- State which file/value to update
- Wait for confirmation before continuing
```

### When Stuck

1. State what's blocking
2. Propose smallest modification to unblock
3. Wait for approval

Never silently skip acceptance criteria. Never reinterpret the task.

### Scope Change Protocol

If you discover a missing requirement:

1. STOP current task
2. State what's missing and why it's needed
3. Propose where it fits in task order
4. Wait for PM to update task list
5. Resume only after task list is updated

Don't improvise new requirements into existing tasks.

---

## PM Feedback Format

When reporting test results:

```
Task [N]: PASS | FAIL | BLOCKED

[If FAIL]: What broke, error message, steps to reproduce
[If BLOCKED]: What's preventing test
```

Keep it tight. Agent needs signal, not narrative.

---

## Example

```markdown
# Todo App Tasks

## Prerequisites
- Supabase project with URL + anon key in .env.local
- Resend API key in .env.local

## Tasks

## Task 1: Scaffold
**Depends on:** None
**Outcome:** Next.js app runs with Supabase client configured
**Why:** Foundation for all features
**Acceptance:** `npm run dev` shows page, console logs "Supabase connected"

## Task 2: Signup
**Depends on:** 1
**Outcome:** Users create accounts via email/password
**Why:** Unblocks all authenticated features
**Acceptance:** Submit signup form → user appears in Supabase Auth → confirmation email sent

## Task 3: Login + Protected Routes
**Depends on:** 2
**Outcome:** Users log in and access protected pages
**Why:** Unblocks task management UI
**Acceptance:** Login → redirect to /dashboard. Visit /dashboard logged out → redirect to /login

## Task 4: Tasks Table + RLS
**Depends on:** 1
**Outcome:** Database stores tasks per user
**Why:** Unblocks task CRUD
**Acceptance:** Insert task via Supabase dashboard with user_id, title, due_date, completed. Query as different user returns empty.

## Task 5: Create Task
**Depends on:** 3, 4
**Outcome:** Users create tasks from UI
**Why:** Core feature
**Acceptance:** Submit form → task in DB → appears in list without refresh

## Out of Scope
- Social auth
- Task sharing
- Mobile app
```
