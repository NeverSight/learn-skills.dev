---
name: spec:implement
description: >
  Execute implementation tasks from an approved plan.json. Use when spec:plan has produced
  approved tasks and the human is ready to start coding. Tracks progress via beads, enforces
  TDD, reports between batches. Trigger when the user says "implement", "go", "start",
  "do it", or after spec:plan completes task creation. Do NOT use without an approved plan —
  invoke spec:plan first.
user-invocable: true
---

# Spec Implement

Pick up tasks. Execute them. Track progress. Report. Stop when blocked.

This skill does not make design decisions or modify the plan. If the plan is wrong, go
back to spec:plan. If the design is wrong, go back to spec:research.

## Prerequisites

Before starting, verify these exist:

1. **Approved spec** — `docs/specs/YYYY-MM-DD-<feature>/spec.md`
2. **Approved plan** — `docs/specs/YYYY-MM-DD-<feature>/plan.json`
3. **Tasks created** — In beads or plan.json task list

If anything is missing, do not proceed. Tell the human what's needed.

---

## Step 1: Review the Plan

Read plan.json critically before writing code. Look for:

- Unclear or ambiguous tasks
- Missing file paths or incomplete code snippets
- Tasks that conflict with each other
- Dependencies that don't match what you see in the codebase

If you find concerns, raise them before starting. Don't guess. Don't assume. Ask.

---

## Step 2: Choose Execution Mode

If the human hasn't specified a mode, ask.

### Autonomous Mode

> "Implement it all. Don't stop until you're done."

- Execute all tasks in dependency order
- Track progress in beads: `bd update <id> --status in_progress` → `bd close <id>`
- Run type checking / linting continuously
- Only stop if blocked

### Batched Mode (default)

> "Do a few tasks at a time."

- Execute 3-5 tasks
- Stop and report: what was done, test output, anything unexpected
- Wait for human feedback before continuing

### Subagent Mode

> "Use subagents."

- Invoke **code:subagents** for dispatch patterns and review cycle
- Fresh subagent per task — no context pollution
- Two-stage review after each: spec compliance, then code quality
- Independent tasks dispatch in parallel, dependent tasks run sequentially

Default to batched if the human hasn't expressed a preference.

---

## Step 3: Execute Tasks

For each task, follow plan.json steps exactly. Find the next ready task:

```bash
bd ready --label <feature> --json
```

Mark it in progress:

```bash
bd update <task-id> --status in_progress
```

### TDD Enforcement

Invoke **oracle:testing** patterns. For every task:

```
1. Write the failing test (from plan.json step)
2. Run it — verify it fails for the RIGHT reason
3. Write minimal code to make it pass (from plan.json step)
4. Run it — verify it passes
5. Refactor if needed (tests stay green)
6. Commit (with message from plan.json step)
```

Do NOT write implementation before tests. Do NOT skip "verify it fails." Do NOT write
more code than needed to pass the test.

### On completion

Mark the task done:

```bash
bd close <task-id> --reason "Implemented with tests"
```

### Referencing existing code

When the plan or human references existing implementations ("make it look like the
users table"), read the referenced code before making changes. A reference communicates
all implicit requirements without spelling them out.

---

## Step 4: Report (Batched Mode)

After each batch:

```
Completed: Tasks T1-T3
- T1: UserEntity with validation ✓
- T2: UserEntity tests (6 passing) ✓
- T3: UserRepository ✓

Test output: 6 passed, 0 failed
Type check: clean

Ready for feedback.
```

Wait. Don't continue until the human responds.

---

## Step 5: Handle Feedback

Expect short, terse corrections:

- "You didn't implement `deduplicateByTitle`."
- "This should be in the admin app. Move it."
- "wider" / "still cropped"

Don't ask for elaboration unless genuinely needed.

### Steering patterns

| Pattern | Example | What to do |
|---------|---------|------------|
| Cherry-pick | "Use X for the first one. Ignore the fourth." | Item-level as directed |
| Trim scope | "Skip task T7." | Mark skipped, move on |
| Protect interfaces | "These signatures must not change." | Adapt callers |
| Override | "Use the library's built-in method." | Direct override |
| Revert | "I reverted. Now just do X." | Respect narrowed scope |

### On revert

If the human reverts git changes and re-scopes, respect the narrowed scope completely.
Don't salvage the previous approach. Don't ask "are you sure?"

---

## When to Stop

**STOP immediately when:**

- A test fails and you can't fix it within 2 attempts
- You hit a dependency not covered in the plan
- An instruction is unclear or ambiguous
- The plan conflicts with the actual codebase
- The design needs to change, not just the implementation
- Verification fails repeatedly

**When you stop:**

1. Explain the blocker clearly
2. Show what you tried
3. Ask for direction

Do not guess. Do not work around it. Stop and ask.

If the plan needs to change:

> "This needs a plan revision. Want me to go back to spec:plan?"

If the design was wrong:

> "This changes design assumptions. Want me to go back to spec:research?"

---

## Completion

When all tasks are done, verify and present the work.

### Verification checklist

1. **Run full test suite** — all tests must pass, not just the new ones
2. **Run type check / lint** — clean output, no new warnings
3. **Verify beads tasks** — `bd list --label <feature> --json` — all tasks must be closed
4. **Diff review** — review the full diff against main/master. Look for:
   - Files that changed but shouldn't have
   - Debug code or temporary hacks left behind
   - Inconsistencies between what was planned and what was built

### Summary report

Present to the human:

```
## Feature Complete: {feature name}

**Tasks:** {completed} / {total}
**Tests:** {new tests added}, {total passing}
**Files:** {created}, {modified}

### What was built
- [concise list of what was implemented]

### Verification
- Test suite: ✓ all passing
- Type check: ✓ clean
- Lint: ✓ clean

### Ready for review
```

### Next steps

Offer the human their options:

> **Merge** — squash and merge into main
> **PR** — create a pull request for team review
> **Keep** — leave the branch for now, come back later
> **Discard** — delete the branch, start over

Don't choose for them. Present options and wait.

If validation finds bugs, loop back to implement. See **spec:orchestrator**
for iteration patterns.
