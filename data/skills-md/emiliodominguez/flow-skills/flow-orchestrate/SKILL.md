---
name: flow-orchestrate
description: "Multi-worker execution of a plan with independent acceptance gates. Use for cross-system features or long refactors with dependent phases. Routes to `flow-plan`, `flow-verify`, `flow-review` or `flow-handoff`."
metadata:
  stage: plan
---

# Orchestrate

Own intent, dependencies, acceptance and reporting. Delegate implementation and correction;
write only the plan and run records yourself. A skill is instructions, not a running agent:
use only delegation actually available and authorized in this session.

## Phase 1: Establish an executable contract

1. Read the plan, repository instructions, branch and working-tree state, and task-relevant
   source. Reuse a current repository brief after checking its cited inputs.
2. Identify the outcome, non-goals, task IDs, dependencies, artifacts, write boundaries,
   acceptance criteria, verification profile and attempt budget. Criteria need an observable
   result and evidence, not a command name or "looks good".
3. A task is ready only when its dependencies are accepted at the current revision. Reject
   cycles, missing dependency IDs and assumptions that fork the outcome. Resolve routine detail
   from source; ask one targeted question only for a consequential missing decision. Use
   `flow-plan` when the plan needs substantial repair.
4. Inspect available specialists, tools, concurrency and write isolation. Prefer a relevant
   specialist, otherwise a general worker with a bounded brief. Skills do not register agent
   types; never invent one that is not present. If the plan names models or effort, follow
   [execution profiles](references/run-record.md#execution-profiles) before dispatch.
5. Set a finite budget. Defaults unless the plan says otherwise: at most three execution
   attempts per task (initial plus two corrections), at most two active workers, no new
   dispatch after 30 minutes elapsed. Check the deadline at each dispatch and result; use host
   cancellation when available, otherwise record outstanding work without claiming a hard
   timeout.

For one small task, use `flow-work` directly. If independent delegation is unavailable or
prohibited, say so and offer direct execution with explicit self-checks; never label
role-play in one context as independent verification. An already authorized direct fallback
needs no second confirmation.

## Phase 2: Create the run record

Persist state before dispatch using the [run record layout](references/run-record.md#run-record-layout):
one `state.md` plus separate worker and verifier files per attempt.

States: `pending`, `ready`, `running`, `verifying`, `accepted`, `rejected`, `blocked`. Only
`accepted` releases dependents. A worker returning, a tool exiting zero or a checkbox changing
is not acceptance.

## Phase 3: Dispatch bounded workers

Give each worker only what it needs:

- Task ID, attempt and resolved execution profile (or `inherited`).
- Deliverable and observable acceptance criteria.
- Allowed files and external actions, files owned by others, non-goals.
- Relevant repository instructions, source paths, accepted dependency artifacts, exact
  verification commands and working directory.
- Expected return: changed paths, revision/diff identity, checks with actual results, open
  assumptions and a short downstream handoff.
- Stop conditions: scope mismatch, missing capability, conflicting edits, budget reached, or
  an action outside current authorization. Report evidence instead of guessing.

Workers use `flow-work` in delegated mode and never edit plan checkboxes, run state or criteria.
Reviewers are read-only against deliverables; scratch output goes in their own temp dirs.

Parallelize only dependency-independent tasks with disjoint write sets. Shared files,
lockfiles, generated output or a shared index mean one writer at a time. Use isolated
worktrees when supported; integration is its own bounded task, and the combined result is
verified after integration even if each task passed alone.

## Phase 4: Execute, verify, correct

1. On return, record the artifact and revision, increment the attempt, and run `flow-verify` under
   the resolved verifier profile in a separate agent or fresh context. Pass the contract, raw outputs and source, never an instruction
   to approve or the worker's conclusions as ground truth.
2. Require `ACCEPT`, `REJECT` or `BLOCKED` per criterion with reproducible evidence at the
   inspected revision. Missing or malformed verdicts do not pass.
3. **ACCEPT:** record verifier identity, evidence and revision, mark accepted, release
   dependents. Only now check a checkbox-plan task.
4. **REJECT:** keep the verdict, re-delegate correction with the failing criterion and
   reproduction, keep the contract fixed, re-verify independently.
5. **BLOCKED:** stop that dependency chain. Missing tools, evidence or authorization are not
   failed implementations and never justify blind retries. Continue unrelated ready work
   within scope and budget.
6. Stop a correction loop when the attempt limit is reached, the same rejection returns
   without new evidence, the deadline passes, or the plan is contradicted. Record the reason,
   remaining work and smallest next decision. Never weaken a gate to pass it.

Any change to an input, implementation, contract or accepted dependency invalidates the
affected acceptance; re-evaluate that task and its dependents only. Pragmatic gates can accept
decision analysis; production code needs the production profile, repository checks and
runtime evidence.

## Phase 5: Resume and finish

To resume, follow the [resume procedure](references/run-record.md#resume-procedure): reconcile
recorded revisions and in-flight work before any new write.

Finish only when every requested task and the integrated outcome pass their declared gates.
Report accepted work, evidence, rejected/blocked work, limits consumed and remaining risks.
Quote verdicts accurately; synthesize rather than dumping transcripts. Review, merge, deploy
and publish keep their own authorization boundaries.

## Anti-patterns

- Implementing or silently repairing a worker's deliverable from the orchestrator role.
- Treating worker confidence, green typechecks or an absent verdict as acceptance.
- Resetting retry counts after a context switch, or replaying an unknown external action.
- A swarm for a typo, or requiring a specialist the host does not provide.

## Done when

- Every requested task and the integrated outcome has a recorded independent acceptance, or
  the run is explicitly blocked with remaining work and reason.
- No dependent task consumes rejected, missing or stale evidence.
- Another session can reconstruct what is accepted and why from the run records.

Hand off to `flow-review` when gates pass, or `flow-handoff` for a blocked or interrupted run.
Neither grants permission to ship.
