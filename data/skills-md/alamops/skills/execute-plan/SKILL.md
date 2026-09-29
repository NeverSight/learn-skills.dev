---
name: execute-plan
description: (alamops) Executes only the coding work of an approved implementation plan, with parallel sub-agents that never collide. Cuts a branch and records the base SHA, checks no two tasks in a wave own the same file, gives each task's agent a self-contained brief with a no-TODO completeness clause, holds wave barriers, isolates unavoidable shared files in worktrees, routes reported remainder into the next wave, and commits a checkpoint per wave. Use when the user hands over a plan (`docs/plans/<slug>.md`, a `write-plan` output, or a task breakdown with file ownership) and limits the job to writing code — just the code and I'll review and test it myself, only run the coding waves, fan these tasks out with no tests — or asks for this skill by name. A plain "execute this plan" with no such limit belongs to `implement`, which carries the plan through review and tests to green. Phase 4 of `implement`, runnable alone. Not for writing the plan (write-plan) or a single pinpointed edit.
---

# Execute plan — collision-free parallel coding from a plan

Your job is to turn an approved plan's work breakdown into code, fanning tasks out to parallel agents wave by wave, so that the result is the plan — complete, on a branch, in resumable commits — and nobody's work got overwritten along the way.

You're the coordinator. Agents write the code; you own the decisions that keep the fleet safe: whether a wave is valid, what each brief says, when to move to the next wave, what to do with the remainder agents report, and how to recover when a task fails.

## Where this sits

This is Phase 4 of the `implement` delivery loop, packaged to run on its own. It executes a plan from `write-plan` (or `implement`'s Phase 3, or any breakdown with equivalent structure). It stops when the code is written: code review, tests, and the test/fix loop are separate steps (`code-review`, `write-tests`, `test-loop`) — or use `implement` to run all of it.

## 1. Load and check the plan

Find the plan — usually `docs/plans/<slug>.md`. Before anyone writes code, confirm it's executable:

- **Tasks own files.** Every task lists the exact files it creates or edits, and waves say what runs in parallel. If the breakdown lacks file ownership (it's a ticket list or a PRD), derive the partition yourself from the code, show the user the tasks-and-waves table, and get a quick yes before spawning — you just changed the plan, and they should see it.
- **Open questions.** If §8 holds an unresolved question a task depends on, raise it now. A premise that's wrong costs a sentence to fix today and a rewrite after the wave lands.
- **Approval.** A plan the user handed you with "execute this" is approved. A plan marked self-approved under `--auto` is approved for an unattended run.

If the input is really a feature request with no plan behind it, say so and point to `write-plan` (or `implement`) instead of improvising a breakdown on the fly — the plan is where file ownership gets thought through, and skipping it is what makes parallel agents collide.

## 2. Baseline before anything writes

- **Branch.** Never let a fan-out write to the default branch. If you're on `main`/`master` or no target branch was named, create one from the plan slug (`implement/<slug>`) and announce it.
- **Record the base.** Capture `git rev-parse HEAD` as the base SHA and note whether the tree was already dirty (`git status --porcelain`). Fill the plan's `Branch` and `Base SHA` rows — a metadata-only edit, not a scope change. Review and the final diff are measured against exactly this ref, so pre-existing edits aren't mistaken for this build's.

## 3. Run each wave

For every wave in the plan, in order:

1. **Validate it.** Cross-check the owned-files lists of the tasks you're about to launch together. If any path appears in two of them, the wave isn't valid — re-partition or split it before spawning. It's a thirty-second check and the cheapest place a collision will ever be caught.
2. **Brief each task** (see below).
3. **Spawn one agent per task in a single message**, so they run concurrently — when the tasks are substantial enough for parallel wall-clock to matter. A wave of a few small, single-file tasks is often faster done by one agent carrying them all, or by you directly; each agent costs a full context, so match the fleet to the work rather than to the task count. On Claude Code, use `general-purpose` agents; leave the model unset so they inherit the session's model unless the user asked for another. If your harness has no sub-agent tool, execute the tasks yourself one at a time in wave order — the partition still keeps each change clean.
4. **Hold the barrier.** Wait for every agent in the wave before starting the next; later waves depend on earlier ones.
5. **Read what came back** — each agent's summary, deviations, and remainder.
6. **Checkpoint.** Run a quick sanity pass if it's cheap (build, typecheck, lint on changed files), then commit the wave: `wave N: <summary>`. These commits are resume points: if a later wave fails, you pick up from the last green one instead of starting over.

### The brief

An agent can't pause to ask what you meant, so its one instruction must carry everything. Vague briefs are the biggest single cause of overlapping work and rework. Every brief nails:

- **Objective** — the task's goal, in a sentence.
- **Owned files** — exactly the plan's list, with a firm "touch nothing else — other files belong to other agents".
- **Context** — the relevant findings and file:line anchors from the plan, and the sibling code to mirror.
- **Acceptance** — the plan's criteria for this task.
- **Conventions** — match the surrounding code: naming, error handling, logging, idiom.
- **Completeness clause** — finish the task's whole scope, with no `TODO`/`FIXME`/stub/`NotImplementedError` standing in for in-scope work. If you find remainder *outside* your owned files — a caller on the old path, a validator that needs the new enum value — don't reach across the boundary (that collides) and don't leave a marker (that's a silent deferral): report it back.
- **Shared-tooling limits** — run formatters and linters on your owned files only, not the whole repo; don't install or upgrade dependencies unless you own the manifest and lockfile; don't regenerate shared code. File-disjoint tasks still collide through tools that rewrite files nobody assigned.
- **Output** — a summary of files changed, any deviation from the plan and why, and any remainder found outside the owned files. Same format for every sibling so you can merge them.

Example: *"**Objective:** add a `TransactionHistory` class. **Owned files:** create `wallet/history.py` — do not edit `account.py`, the tests, or config; a later task wires it in. **Context:** mirror the style of `wallet/account.py:1-40`; no new deps. **Acceptance:** `TransactionHistory.append()` and `.since(ts)` behave as in plan §4 T3. **Completeness:** no stubs or TODOs; report anything outside `history.py` that needs changing. **Output:** files changed, deviations, remainder."*

## 4. When files can't be partitioned

If two tasks genuinely must edit one central file (a registry, a routes table), prefer, in order:

1. **Sequence them** into different waves.
2. **Carve out a wiring task** — one small task in a later wave owns the shared file and makes all the one-line registrations.
3. **Isolate them** — run the colliding agents in separate worktrees (on Claude Code, `isolation: "worktree"`), then **you** merge each worktree branch into the working branch one at a time and resolve conflicts yourself. Merging is the step most likely to strand or clobber work, so it's the last resort, not the default.

## 5. Handle the remainder

Agents following the completeness clause will report remainder they weren't allowed to touch — that's the clause working, not a failure. For each item:

- **It's part of finishing the feature** → schedule it as a task in the next wave (or a final sweep wave), with its own owned files.
- **It's genuinely a different ticket** → add it to the plan's completeness ledger (§9) as *out of scope*, with the reason.

What it never becomes is a `TODO` in the code or a "later" line in your report. Before you finish, grep the diff against the base for added `TODO|FIXME|XXX|HACK` and placeholder throws — it catches the obvious half in seconds.

## 6. When a wave fails

- **Never discard completed work** because something downstream failed. Fix forward from the last green checkpoint.
- **An agent's task failed on its own terms** (compile error, missed acceptance) → re-brief that task with the failure output, same owned files.
- **The plan's premise was wrong** (the API doesn't exist, the "two callers" are twelve) → stop and surface it. That's a plan change the owner should see, not something an agent improvises around mid-wave.

## 7. Report

- **Branch and base SHA**, and the wave commits.
- **What each task changed**, which agent did it, and any deviations from the plan.
- **Remainder**: what got swept into later waves, and what went to the ledger as out of scope (and why).
- **Sanity checks** run and their results.
- **Not done by this skill**: review and tests. Suggest the next steps — `code-review` on the diff since the base SHA, `write-tests` for the plan's §5 test tasks, then `test-loop` to run the suite to green — or `implement` next time to run the whole loop.
