---
name: dev
description: "Ad-hoc development workflow for implementing features, fixing bugs, and making code changes outside a formal plan. Use when asked to implement, add, fix, build, or create something in the codebase. Routes to domain skills (postgres-expert, server-action-builder, react-form-builder, service-builder, playwright-e2e), enforces task tracking for context-compact recovery, and follows a reference-grounded build-test-verify loop. Do NOT use for large multi-phase features — use /create-plan + /implement instead."
argument-hint: "[task description]"
agent: general-purpose
model: sonnet
compatibility: "Claude Code only. Requires Task, Skill, TaskCreate, TaskUpdate, TaskList, and TaskGet tools."
allowed-tools: "Read Write Edit Grep Glob Bash Skill Task TaskCreate TaskUpdate TaskList TaskGet"
metadata:
  version: 1.1.0
---

# Dev

**YOUR TASK: `$ARGUMENTS`**

## Critical

- **Check TaskList FIRST** before doing anything else — tasks may already exist from a previous session or compact
- **Find a reference implementation** before writing code — never guess at patterns
- **Invoke the right domain skill** for each piece of work — skills embed project-specific conventions
- **Run verification** (tests, typecheck) before reporting done — unverified code breaks downstream work
- Do NOT create plan files, phase files, or documentation — this skill implements directly

## Task Tracking

Tasks survive context compacts — skipping this check causes lost progress and repeated work.

**Before starting work, run `TaskList`** to check if tasks already exist from a previous session or before a compact. If tasks exist:

1. Read existing tasks with `TaskGet` for each task ID
2. Find the first task with status `pending` or `in_progress`
3. Resume from that task — do NOT recreate the task list

If no tasks exist, create them in Step 2 after scoping the work.

Mark each task `in_progress` when starting and `completed` when done.

## Workflow

### Step 1: Understand the Task

Read any files the user referenced or that are clearly relevant. If the task mentions an existing file, read it. If it mentions a feature area, Glob for related files.

Extract:

- **What needs to change** — new files, modified files, or both
- **What domain(s) are involved** — database, server actions, services, UI, forms, tests
- **What already exists** — don't rebuild what's already there

### Step 2: Create Task List

Break the task into concrete sub-tasks. Each task should be a single, completable unit of work.

```
TaskCreate({ subject: "...", description: "...", activeForm: "..." })
```

**Task descriptions must be self-contained** — include file paths, function signatures, and acceptance criteria. If your context gets compacted, the task description is all you'll have.

**Order tasks by dependency:**

1. Schema/database changes first (if any)
2. Service layer
3. Server actions
4. UI components and forms
5. Tests (or interleave with TDD — Step 0 pattern)
6. Verification

### Step 3: Identify Domain Skills and References

For each task, determine the right domain skill and find a reference implementation:

| Work Type                                 | Domain Skill                   | Reference Glob                              |
| ----------------------------------------- | ------------------------------ | ------------------------------------------- |
| Database schema, migrations, RLS policies | `/postgres-expert`             | `supabase/migrations/*.sql`                 |
| Service layer (business logic, CRUD)      | `/service-builder`             | `app/home/[account]/**/*service*.ts`        |
| Server actions (mutations, auth + Zod)    | `/server-action-builder`       | `app/home/[account]/**/*server-actions*.ts` |
| React forms with validation               | `/react-form-builder`          | `app/home/[account]/**/_components/*.tsx`   |
| React components, pages, layouts          | `/vercel-react-best-practices` | `app/home/[account]/**/_components/*.tsx`   |
| E2E tests                                 | `/playwright-e2e`              | `e2e/tests/**/*.spec.ts`                    |
| UI/UX review                              | `/web-design-guidelines`       | N/A (guideline check, not reference-based)  |

**For each domain involved:**

1. **Glob** the reference pattern — read ONE file of the matching type
2. **Extract key patterns**: function signatures, imports, naming, error handling
3. **Invoke the domain skill** before implementing that type of work:

   ```
   Skill({ skill: "postgres-expert" })
   ```

   The skill loads project-specific conventions. Follow them.

**Reference is ground truth.** If the codebase does something differently from what you'd expect, match the codebase.

### Step 4: Implement

Work through your task list sequentially. For each task:

1. `TaskUpdate` — mark `in_progress`
2. Invoke the domain skill (if not already loaded for this type)
3. Read the reference file (if not already read for this type)
4. Implement the change
5. Run quick verification (tests for that area if they exist)
6. `TaskUpdate` — mark `completed`

**Key project patterns to follow:**

- Server actions: validate with Zod, verify auth before processing
- Services: `createXxxService(client)` factory wrapping private class, `import 'server-only'`
- Imports: path aliases, ordering: React > third-party > internal > local
- After mutations: `revalidatePath('/home/[account]/...')`

**Scope boundary — implement ONLY what was asked:**

- Do NOT add improvements not specified in the task
- Do NOT refactor adjacent code
- Do NOT create documentation files

**IMPORTANT:** Before using the Write tool on any existing file, you MUST Read it first or the write will silently fail. Prefer Edit for modifying existing files.

### Step 5: Verify

Run the verification suite:

```bash
pnpm test
pnpm run typecheck
```

Both must pass. If either fails, fix the issues before proceeding.

If the project doesn't have these commands, check `package.json` scripts for alternatives.

### Step 6: Summary

Report what was done:

- **Files created/modified** (list with brief description of each change)
- **Domain skills used** (which skills were invoked)
- **Verification result** (tests passing, typecheck clean)
- **Anything left for the user** (manual steps, env vars to set, etc.)

---

## Resuming After Context Compact

If you notice context was compacted or you're unsure of current progress:

1. Run `TaskList` to see all tasks and their status
2. Find the `in_progress` task — that's where you were
3. Run `TaskGet {id}` on that task to read full details
4. Continue from that task — don't restart from the beginning

Tasks persist across compacts. The task list is your source of truth for progress, not your memory.

**Pattern for every work session:**

```
TaskList → find in_progress or first pending → TaskGet → continue work → TaskUpdate (completed) → next task
```

---

## Troubleshooting

### Domain skill not found or not relevant

**Cause:** The task doesn't fit neatly into one domain skill.

**Fix:** Skip skill invocation for that piece of work. Find a reference file of the same type in the codebase and follow its patterns directly. The reference is more important than the skill.

### Tests fail but code looks correct

**Cause:** Reference patterns may have changed, or existing tests have assumptions your change breaks.

**Fix:** Re-read the failing test file. Understand what it expects. If your change intentionally alters behavior, update the test. If not, your implementation has a bug — fix it.

### Task is too large for a single session

**Cause:** The task scope exceeds what can be done before context fills up.

**Fix:** This is exactly why task tracking exists. Your tasks will survive compaction. If the task is truly massive (10+ files, multiple domains), suggest the user create a plan with `/create-plan` instead.

## Constraints

- Do NOT create plan files, phase files, or review files — this is for direct implementation
- Do NOT skip the reference read — guessing at patterns causes review failures
- Do NOT skip verification — unverified code is incomplete work
- Auto-invoke domain skills for matching work types — they embed conventions you'll miss otherwise
- Keep task descriptions self-contained — they're your lifeline after compaction
