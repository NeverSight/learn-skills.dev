---
name: auto-implement
description: "Implement all existing tasks in an authorized batch through implement-task, in dependency order, after checking every task and requiring all user-action blockers to be resolved first. Use when the user requests automatic multi-task implementation; preserve verification/review policy and stop for new blockers or stalled corrections."
---

# Auto Implement

Own a bounded batch of existing Phat tasks. Scan the entire batch for readiness
before changing implementation, explain every user-action blocker, and start
only after those blockers have been resolved. Then use `$implement-task` one
task at a time and continue automatically within the agreed batch.

## Scope and authorization

Read `AGENTS.md`, project requirements/context, verification and commit policy,
and the task/spec catalog. Resolve installed `implement-task` and the capability
skills it needs; do not assume consumer repositories use this pack's paths.

Use the user's named spec/task set when supplied. Otherwise "all tasks" means
all existing task documents in the current repository at invocation. Record the
exact batch IDs in working notes and report the scope; do not include tasks
created later automatically, reopen done tasks, or invent missing tasks.

Exclude a task from the executable queue only when its repository cancellation
state or `Retired by scope change:` record cites an accepted contract change
and confirms no work remains. Report retired IDs separately from `done`; do not
skip ordinary blocked tasks. Check surviving dependency edges before proceeding.
A retirement does not authorize replacement tasks outside the original batch.

Include upstream dependency closure only when already authorized by the batch.
If a requested subset requires unfinished tasks outside that subset, explain
which prerequisite IDs must be completed or included and obtain that scope
choice before starting. An empty or fully done batch is a no-op.

Invoking this skill authorizes sequential implementation and in-scope review
corrections across this batch without asking permission for each task. It does
not authorize product decisions, verification-policy changes, infrastructure
provisioning, deployment, push, or commits beyond the existing explicit policy.
Preserve unrelated changes and keep each task's diff/evidence distinguishable.

## Whole-batch preflight

Read every selected task and its linked spec in full, plus relevant sources,
recorded blockers, review findings, and known environment/setup instructions.
Apply the `implement-task` readiness and verification-selection contracts to
all unfinished tasks before starting the first one, separating external readiness
from scheduling. Defer the dependency-done gate for dependencies inside the batch
until selecting that task for execution; a task blocked solely by those edges
does not require user remediation. This pass does not execute implementation or
dispatch tests/review.

Check the complete dependency graph for missing IDs, cycles, incompatible
scope, and at least one runnable node. Unfinished dependencies inside a valid
batch are scheduling edges, not requests for the user to implement them.
Dependencies outside the authorized batch, active external blockers, draft or
insufficient specs, missing confirmed policy, unresolved design/behavior
conflicts, and unavailable required capabilities/runners are readiness blockers.

Inspect blockers even if the task status is todo or in_progress: required
credentials, account permissions, services, assets, decisions, runner/delegation
availability, or other known prerequisites may be described in its sources
rather than a Status field. Avoid exhaustive speculative setup checks. A future
module or test file that this batch explicitly implements is not missing
infrastructure; distinguish planned deliverables from external prerequisites.

For secret/environment checks and blocker reporting, read
[blocker readiness and remediation](references/blocker-readiness.md). Explain
all known user-action blockers together with affected tasks, exact evidence,
user steps, expected location, and a safe check/unblock condition. No task may
start while any such blocker remains, even if independent tasks could run.
Do not clear blocked status based only on optimism, replace secrets with fake
values, waive checks, or assume a response/no response means readiness.

Respect review mode. If off/unavailable auto review will leave an unfinished
prerequisite in_review, the batch cannot advance its dependents to done; explain
this manual approval barrier in preflight. Ask the user to arrange review or
explicitly choose a supported policy/override through the owning workflow.
Do not turn review on automatically. Independent tasks may finish implementation
in_review under that policy, but must not be reported as done.

When preflight finds blockers, stop before implementation and task-start status
changes. Report actionable remediation and wait for the user to resolve it.
On resume, re-read changed evidence and recheck the whole batch; preserve already
agreed choices. Mark only demonstrably resolved active blockers as resolved,
using the existing task contract and retaining useful history.

## Changed agreements and optional assessments

When the user intends to change an existing agreed behavior across its spec and
task plan, hand that change to `$change-scope`; do not rewrite the contract as
an implementation fix or review waiver. Unsettled product decisions still
belong to `$grill-workflow`. Resume only after the affected contract and task
readiness are reconciled. Existing batch authorization does not include new
follow-up tasks automatically.

`$verify-feature` can assess a requested cross-task acceptance question and
`$release-check` can assess a requested release candidate. Neither replaces
this skill's task verification/review contract or changes its status authority.
Do not invoke them as extra mandatory completion gates.

## Sequential execution

When preflight passes, keep a dependency-ordered queue (use task-ID order as a
tie-breaker) and a working ledger of statuses, task baselines, checks, and results.
Do not create a new project tracking document merely for this ledger.

For each task:

1. Recheck current task/spec, prerequisites, and relevant environment evidence.
   Only a done dependency unlocks its dependent; in_review is not done.
2. Skip done tasks. Load `$implement-task` inline in the main batch agent for
   one todo/in_progress or valid resolved-blocker/review-correction continuation.
   It retains its single-task scope and owns implementation and task updates.
3. Let `implement-task` dispatch selected tests sequentially and one final
   `code-review` sub-agent per implementation cycle under the effective policy.
   Wait for terminal results and enforce every write boundary. Do not delegate
   an implementation agent that cannot dispatch the required verification agents.
4. Apply supported, in-scope review corrections through a new `implement-task`
   cycle, preserving findings and rerunning affected gates. This batch invocation
   supplies authorization to continue recorded fixable findings; no extra user
   invocation is required for each correction.
5. Record the observed result, then select the next runnable task. Never mark
   done yourself or advance a dependent from a partial/unreviewed result.

For a task already in_review and awaiting approval, do not reimplement it.
Use the canonical final-review dispatch contract when its effective mode permits,
with current task-scoped evidence and an explicit comparison base. With review
off/unavailable, preserve in_review and the reported manual barrier.
Check prior review evidence first: dispatch a pending review only if no terminal
final review exists for that cycle. Recorded fixable findings require a correction
cycle; an external review blocker requires its recorded unblock condition to be
resolved before a new review attempt. Never redispatch a completed review merely
because the task remains in_review.

For each task, distinguish its changes from earlier batch changes and unrelated
work. Supply reviewers the task-owned diff and complete required evidence;
never attribute the accumulated batch diff to the latest task. Follow the
existing commit policy, without staging unrelated or earlier-task files broadly.

## Stop, resume, and finish

If a new external/decision blocker appears, stop the batch immediately, record
it in the owning task within its allowed boundary, and provide the remediation
report. Do not proceed to independent tasks while the user-action blocker is
active. A preflight pass cannot guarantee that no new blocker will emerge.

Resolve ordinary in-scope implementation/test failures autonomously. For an
unclear cause, compose `$debug-task` inline if available and return its evidence
to the current `implement-task` cycle. Diagnostic support cannot provision missing
infrastructure, override a gate, or restart the correction budget. Limit
automatic correction to two additional implementation/verification cycles per
task after the initial attempt; stop earlier if the same failure repeats without
new evidence or meaningful progress. Report the exact unresolved finding and
next action rather than looping, weakening verification, or expanding scope.

On resume, rebuild the queue from actual task status and current evidence.
Reuse credible unchanged evidence; rerun checks affected by new changes. Keep
done tasks done, and never reset the batch or discard prior changes to resume.

At completion or interruption report:

- Batch scope and each task's observed status: done, in_review, unfinished,
  blocked, or demonstrably retired, with task paths and relevant evidence.
- Changed files and commit/uncommitted state under the effective policy.
- Remaining blockers with concrete user actions, and tasks waiting on them.
- The next resume/review/decision action, if needed.

Claim all selected tasks done only when they are actually done. If accepted
scope changes retired selected tasks, report executable work complete only when
all surviving selected tasks are done, and list retired IDs separately. An empty
executable queue is a no-op, not proof that retired tasks were implemented.
If all tasks are implemented but await review, say so. Do not start another
batch, mark a spec done without its owning lifecycle checks, or schedule future
work automatically.
