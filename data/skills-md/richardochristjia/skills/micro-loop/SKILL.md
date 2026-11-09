---
name: micro-loop
user-invocable: false
description: Execute a simple, low-risk phased plan from `.plans/{task}/` straight through with no builds, tests, or commits between phases; verify, lint, and commit once at the end. Use when the plan is straightforward and rebuilding per phase would only waste time.
argument-hint: "<.plans/task or slug>"
---

# Micro Task Loop

A fast path for simple phased plans. Trades per-phase safety checkpoints for wall-clock time: no builds, tests, or commits until every phase is done, then one verification pass and one commit. `tasks.md` tracks progress in real time.

**Arguments:** `$ARGUMENTS` — the plan (a `.plans/<task>/` path or slug). Always run the whole plan.

Picked by pick-tier when the tier is S or M.

**Read `task-loop-rules.md` in this skill's folder first.** It holds the project commands, constraints, concepts, task-list discipline, and finishing steps all three task loops share. This file adds only what is specific to this loop.

## Constraints (on top of the shared ones)

- **Edit-only until the end.** During phases, only edit files; `check` and `test` wait for **Final verification** — not per-package, not per-module, not "just this once." Avoiding rebuild-thrash is the entire point of this skill. Exception: an environment or toolchain failure that blocks editing itself.

---

## The Loop

**Repeat until every task is complete.** Work per phase, top to bottom.

1.  **Check status.** `Read` `tasks.md`. Every task `[x]` → go to **Final verification**. Otherwise start at the next task.

2.  **Gather** what the current task needs: the spec section it implements and the code it touches.

3.  **Implement, one task at a time:**

    a. **Restate** the current task in one sentence.

    b. **Do the work** — edits only (Constraint 2).

    c. **Tick it** in `tasks.md`.

    d. **Pick the next task** under the current phase header and repeat from (a). When the phase has no `- [ ]` left, go to 3.5.

3.5. **Audit.** Re-read `tasks.md`. Any task in this phase not `[x]` means you drifted: return to step 3 with it. The list must be clean before you move to the next phase.

4.  **Go to step 1.**

---

## Final verification

All phases are done and the list is clean. Run these in order without stopping, unless an unrecoverable error blocks progress:

1.  **Check.** Run `check` and fix until it passes. Failures can point at any phase — fix forward.

2.  **Test.** Run `test`; all tests pass.

3.  **Lint and format** as in **Finishing** step 1 of the rules file.

4.  **Commit once** with a Conventional Commit message, `<type>(<scope>): <summary>` (lowercase, imperative, 72 characters or fewer), only after check, tests and lints pass. If an unrecoverable failure blocks verification, stop and report instead of committing.

5.  **Sync.** Run `sync` once (resolve conflicts, re-test, commit the merge).

6.  **Hand back** as in **Finishing** step 2 of the rules file.
