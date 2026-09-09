---
name: implement-task
description: Execute to-tasks tasks by dependency order, running independent ready tasks in parallel isolated worktrees with one fresh sub-agent per task.
disable-model-invocation: true
---

# Implement Task

Execute the tasks `to-tasks` published. The unit of work is one task in one fresh context: the task file is the whole brief, [`execute.md`](execute.md) is the whole procedure, and the boundary in the task file is the only thing the executor may write inside.

Given one task file, this skill runs `execute.md` itself. Given a ticket or a feature directory, it orchestrates the **frontier**: independent ready tasks run concurrently in separate Git worktrees, each in a fresh sub-agent. The orchestrator owns integration and ticket acceptance.

## 1. Resolve the input

Accept one argument:

- **A task file** (`<issues dir>/<NN>-<ticket-slug>/<MM>-<task-slug>.md`) → single-task mode. Follow `execute.md` directly and stop when it reports.
- **A ticket file or its task directory** → orchestrate that ticket's tasks.
- **A feature directory** → orchestrate every ticket's tasks, in ticket dependency order.

Read the issue tracker convention (`docs/agents/issue-tracker.md` or whatever `/setup-matt-pocock-skills` configured) to locate task files and the `Status:` vocabulary. Tasks not published by `to-tasks` (no Boundary section) are out of scope; say so and name `$to-tasks`.

## 2. Work the frontier

The frontier contains unassigned `ready-for-agent` tasks whose sibling blockers and parent ticket blockers are all `done` on the integration branch. A worker's report alone never clears a blocker: its commit must be integrated and validated first. Parent tickets clear only after all their tasks are integrated and ticket acceptance passes.

Before dispatch, resolve the dependency graph, including blockers outside the requested scope. Stop and identify missing references or cycles; external unfinished blockers remain blocked and do not expand the scope. Confirm pre-existing `done` work is present on the integration branch with passing validation evidence; rerun the relevant checks when resuming an interrupted integration with missing evidence. Keep existing `claimed` work out of dispatch until its owner and outcome are known.

Use the current branch as the integration branch and record its commit as the review base for §3. Inspect the worktree and preserve unrelated changes. Worker inputs (task files, tickets, design, and required code) must be available from the chosen base; surface uncommitted prerequisites rather than silently omitting or committing user changes.

The run ends only when the frontier is empty and no worker remains. Do not ask the user whether to continue; the frontier decides. Everything in scope is already authorized by the invocation.

Loop:

1. Fill available sub-agent slots from the frontier, lowest ticket number then lowest task number first. This is launch priority, not a requirement to wait for earlier tasks. Track assignments so a task is dispatched only once.
2. For each task, create a separate worktree and branch from the latest validated integration commit. Run-created worktrees live only under `<repo>.worktrees/` next to the main checkout — a checkout at `/src/app` puts a task's worktree at `/src/app.worktrees/<NN>-<MM>-<task-slug>`, named by the task's ticket number, task number, and slug — never inside the repository. Give its fresh sub-agent the worktree path, branch and base commit, task path inside that worktree, and the absolute path to this skill's `execute.md`. Tell it to follow the **delegated mode** there and return its report. Keep the brief to these execution coordinates; the worker reads the task, ticket, and design itself. All its edits, tests, staging, and commits run in that worktree.
3. Run independent tasks concurrently up to the environment's available capacity. Sharing a writable project (including `Tests`) alone does not prevent parallelism. Serialize a concrete shared external resource that cannot be isolated, such as tests mutating the same database; explain that restriction. If worktree isolation or parallel sub-agents are unavailable, report the limitation and run `execute.md` in delegated mode yourself, one frontier task at a time, then return to step 4; its closing stop ends that task, not the run.
4. Wait for any worker to finish, then integrate successful reports one at a time. Inspect the task commit for boundary compliance and cherry-pick it onto the integration branch; record both worker and integrated hashes. Resolve routine merge conflicts within the existing task contracts, preserving both tasks' behavior. A conflict requiring a design or boundary change stops the run for triage.
5. On the combined tree, rerun the newly integrated task's Validation command and previously integrated tasks' validation when their shared files or contracts are affected. Keep dispatch paused during integration and validation. Only a passing result makes this commit the new dispatch base and clears its task's blockers.
6. Once every task of a ticket is integrated, run its acceptance criteria on the combined tree, including any task criterion deferred to ticket acceptance. On success, tick the evidenced criteria in the task and ticket files, set the ticket to `done`, and commit these tracker updates before clearing dependent tickets. Ticket completion is a report line, not a stopping point; continue to step 7. On failure, stop and report the failed criterion.
7. Recompute the frontier after each validated integration and ticket completion, and refill available slots without waiting for unrelated running tasks. If the frontier is empty but workers remain, wait for a report. End only when no task can be dispatched and no worker remains; distinguish all-done from work blocked by unfinished prerequisites.

For example, with `01 → 03`, `02 → 04`, and `03 + 04 → 05`, dispatch `03` and `04` together once `01` and `02` are integrated. Dispatch `05` only after both `03` and `04` are integrated and validated.

On `needs-triage`, another unsuccessful report, integration failure, or validation failure, stop new dispatches and integrations. Ask active workers to stop at a safe checkpoint, collect their reports, and retain their worktrees and branches. Report completed-but-unintegrated work separately; it clears no blockers. Preserve the failing evidence and surface the blocker rather than widening a task. Do not end the run with unaccounted workers still writing.

## 3. Review the whole run

When the loop ends normally and changes were integrated, invoke `$code-review` with the commit recorded in §2 as the fixed point. Review the integrated change set against the repository's standards and the spec, after the combined-tree validations.

Carry the review's findings into the report unchanged. Fixing them is a new piece of work: a finding inside one task's boundary becomes a follow-up task under that ticket, and a finding that crosses boundaries goes back to `design.md`. Both are the user's call.

A loop stopped by a worker, integration, or validation failure skips the review; report the incomplete run first.

## 4. Hand back and stop

Report:

- Each task attempted, its worker and integrated commit hashes, and whether it was integrated and validated or remains unintegrated.
- The `$code-review` findings, when §3 ran, and where each would be fixed.
- For a `needs-triage` stop: the task, the project it needed to write to, and the reason, copied from the task's Comments.
- Tickets completed in this run.
- On a normal end nothing remains ready; say all done. List ready or blocked tasks, with their unfinished prerequisites, only when the run stopped for a failure or an external blocker.
- Retained worktree paths, branches, and checkpoints needed to resume.

Remove only run-created worktrees and branches whose work is integrated, validated, and clean. A worktree is run-created only when this run created it under `<repo>.worktrees/`; a worktree anywhere else is pre-existing and stays untouched. Preserve failed, unintegrated, or dirty work; never force cleanup or remove pre-existing worktrees.

Then stop. Do not pick up a task that came back `needs-triage`, and do not widen a boundary to get past it; the fix belongs in `design.md` or in the split, and that is the user's call.
