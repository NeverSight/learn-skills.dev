---
name: progress
description: "Manage and brief repo-local plans, task queues, continuation, handoffs, status, and durable goal contracts. Explicit invocation or established-goal recovery only."
---

# Progress

Run this skill after the user explicitly invokes `$progress`, or when an
already-established persistent goal contract requires `$progress` recovery at
a continuation, resume, compaction, or handoff. Do not infer the latter from an
ordinary planning request. Treat the planning system as manually selected
project memory: reconcile it with direct instructions and repository evidence
before relying on it. In goal mode, keep two independent truths: the project
queue says what the project should do next, while the goal contract says what
the active run is authorized to execute.

A request may authorize more than one phase. Finish and validate each phase,
then redispatch the next authorized operation through this entry point; recover
goal authority before execution. A planning-only phase never grants implementation
or delivery authority by itself.

## Resolve the Work System

1. Read applicable `AGENTS.md` files and inspect git status.
2. Determine the planning scope before selecting files. Use the user-named
   scope or index. During concurrent worktree work, select the current
   worktree's isolated namespace from the parallel-worktree workflow. Otherwise
   use the ordinary unscoped namespace.
3. Classify the request before selecting work:
   - explicit `goal mode`, a supplied `Goal contract`, or a named goal-state
     path selects goal execution;
   - continuing, resuming, implementing, handing off, starting, or completing
     current work is execution-affecting;
   - briefing or discussing a roadmap, future implementation, or proposed plan
     with the user before implementation selects planning review;
   - orienting, auditing, capturing, reordering, scheduling, or otherwise
     editing only the project queue is project-plane work;
   - an explicit instruction to leave the active goal untouched and perform
     separate project work selects ordinary project mode. Do not infer this
     override from a bare request to continue.
4. Check the resolved scope's conventional `goals/` path for schema-valid goal
   state, not arbitrary project documents named goals. Implicit recovery
   requires `Status: active`, a matching `Planning scope`, and an `Original
   contract` block containing the complete required fields from `Outcome`
   through `Delivery`, including a `Goal state` path that names that file. An
   explicit goal-mode or path invocation with malformed state fails closed;
   otherwise ignore schema-invalid files for dispatch. Activate the goal
   overlay for explicit goal execution or when an execution-affecting request
   has one recoverable active goal. Leave it off for project-plane-only work and
   an explicit separate-work override; those paths may keep the queue truthful
   but cannot silently start goal work. If a planning-only request grows into
   implementation, dispatch again before the first implementation action. In
   goal mode, read both
   [Goal contract](references/goal-contract.md) and
   [Goal execution](workflows/goal.md) before selecting candidate work.
5. Within that scope, use an existing index when it matches the work-queue
   model. Prefer `ROADMAP.md` for ordinary work and the scoped roadmap for
   parallel work. Use `PLAN.md` only when it clearly routes project work. When
   only standalone legacy progress documents exist, report that they need the
   organize branch's explicit migration before another workflow can use them.
6. Read the selected index. In goal mode, recover the goal file and test its
   terminal condition before opening a project item's contents. If work remains,
   choose the goal status's current or next in-scope result, classify it from
   the contract and index metadata, and only then read the allowed work-item
   files needed by the workflow. Project `Current` may help locate or reconcile
   an included result but never selects it. Outside item links need not be
   opened merely to establish that they are outside.
7. Inspect recent history, code, tests, or diffs only far enough to verify
   material status claims. Treat conflicts as staleness to report or repair,
   not as restrictions imposed by the documents.

Resolution is complete when project current/next are identified, goal
current/next are separately known when applicable, and any material conflict
between documentation and repository state is known.

## Separate Authorization from Project Order

- A roadmap, `Current` link, ordered plan, task, branch, PR, review finding, or
  newly written plan never adds work to an active goal.
- In goal mode, check the candidate against the durable goal contract before
  starting every new plan, work branch, PR, review program, or independently
  reviewable outcome.
- Allow explicitly included work and the smallest bounded work necessary for
  an included completion condition. Honor decision authority explicitly
  persisted in the effective contract. Record useful outside work for later.
  Ask before ambiguous work not covered by that authority or materially
  expansive work.
- When the final included condition is satisfied, update both truth planes,
  complete the goal, and return before consulting the next project item.
- If the goal contract cannot be recovered exactly, fail closed. Do not infer
  scope from the project queue or reconstruct authority from conversation
  fragments.

## Keep Plans Coherent at Write Time

Whenever any `progress` workflow creates a plan or materially revises its
intended outcome, behavior, architecture, compatibility, migration, rollout, or
acceptance conditions, read
[End-state planning](references/end-state-planning.md) and apply it before
writing. Reconstruct the settled target, remove historical residue, preserve
real obligations and their exit conditions, and write one coherent plan in the
same operation. Do not require a separate review command or a second user
invocation after the edit.

This gate does not apply to a routine evidence update, next-action refresh,
queue reorder, lifecycle transition, or typo fix that leaves the planned end
state unchanged. When it does apply, ask only for a load-bearing product or
external-contract decision that the user's instructions and repository evidence
cannot resolve. Respect the selected workflow's existing mutation and goal
authority; coherence review never expands what may be edited or implemented.

## Keep One Work Queue per Scope

- Keep each index compact: a `Current` slot, an ordered `Plans` queue, and an
  unordered `Tasks` pool.
- For ordinary work, store the index at `ROADMAP.md`, scheduled work at
  `plans/<stable-slug>.md`, and unscheduled work at
  `tasks/<stable-slug>.md`. Preserve an established `todo/` or `todos/`
  directory as the task pool instead of creating a duplicate convention.
- During concurrent worktree work, give every concurrently edited worktree a
  distinct roadmap and distinct plan and task subdirectories. Apply the naming
  and ownership rules in the parallel-worktree workflow.
- Persist plan order only in the selected index. Keep sequence numbers out of
  filenames and item files.
- List every active item in a scope exactly once: current, queued, or pooled.
  An item in `Current` is absent from its former list until it stops being
  current.
- Make each item file the source of truth for its `Outcome`, `Current state`,
  and `Next action`. Add scope, checklist, decisions, or validation only when
  they carry continuation value.
- On completion, record the result in the item, remove it from the active
  index, and retain the unlisted file as concise history.

## Select a Workflow

Goal execution is a conditional authorization overlay, not a replacement for
project work management. When goal mode is active and the request reviews,
changes, or implements project work, read exactly one primary workflow below
in addition to the goal resources. When the request only initializes,
recovers, amends, or completes goal state, the goal workflow is sufficient.

- [Organize work](workflows/organize.md) — initialize the system; capture,
  start, reorder, schedule, unschedule, or complete items.
- [Orient to work](workflows/orient.md) — report current, next, blocked, or
  stale work without modifying the repository.
- [Brief planned work](workflows/review.md) — explain what comes next and how
  the plan is written so the user can judge whether it matches their intent;
  surface consequential review notes and apply only explicitly approved
  planning changes.
- [Continue work](workflows/continue.md) — select and implement one substantial
  coherent slice while keeping its item current.
- [Hand off work](workflows/handoff.md) — compress the present session into a
  durable item and next action without implementing.

When the user is actually coordinating multiple git worktrees, also read
[Parallel worktrees](workflows/parallel-worktrees.md). Keep that exception out
of ordinary runs.

## Finish Coherently

Before ending a mutating workflow, verify that every path in each touched index
exists, each active item appears exactly once within its scope, plan numbering
is continuous, and every touched item states an evidence-backed current state
and concrete next action. For every new or materially revised plan, also verify
that the written target passed the end-state planning gate without requiring a
follow-up review invocation. During parallel work, also verify that the current
worktree changed only its own planning namespace. Keep transcripts and routine
session logs out of the files. In goal mode, also verify that the original
contract remains unchanged except for explicit recorded amendments, status
names only in-scope next work, and completion does not start the project queue's
next item. Report changed planning files, validation performed, and the next
in-scope action, completion, or blocker.
