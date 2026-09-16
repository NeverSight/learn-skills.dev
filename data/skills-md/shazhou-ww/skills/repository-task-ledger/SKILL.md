---
name: repository-task-ledger
description: "Authoritative lifecycle for user-invoked task-new and task-exec flows and existing repository tasks. Ordinary implementation requests remain task-free."
user-invocable: false
---

# Repository Task Ledger

Manage explicitly opted-in implementation work as versioned repository state
that can move across devices, people, agents, and worktrees. This is a
coordination protocol, not a distributed lock.

## Admit Work

- Create a new task only after the user invokes `task-new`. Ordinary requests
  remain task-free regardless of size, duration, or changed paths. An agent may
  suggest `task-new`, but must not invoke it or make it a prerequisite.
- After opt-in, admit only accepted outcomes that will change at least one file
  outside the owning repository's `tasks/**`. Source, tests, docs, config,
  workflows, scripts, instructions, skills, and new tracked files all count.
- Do not admit read-only work, planning, review, validation-only work,
  external-only operations, or task-ledger maintenance.
- Once a task exists, manage it until completion, abandonment, or explicit
  handoff. The opt-in rule does not release existing ownership.

For cross-repository work, the repository owning the primary design and
implementation owns the source task. Generated files, installed copies, and
lockfile refreshes remain part of that task. Create linked tasks only where
another repository owns independent design, adaptation, tests, or config;
never copy one task between repositories.

## Prepare Task Work

1. Read the repository's agent instructions and `tasks/README.md`; local policy
   may refine this skill.
2. Run `repoledger doctor` before claiming or resuming when the repository has
   adopted the CLI. It must refresh the shared branch, validate full history,
   and validate the worktree identity; `--offline` is insufficient.
3. Inspect all backlog and ongoing tasks for duplicates, overlap, and ownership.
4. Preserve unrelated changes and never move another identity's task to clear
   a conflict.

The authoritative identity is the lowercase kebab-case value of
`task-ledger.identity` in worktree-scoped Git config. It requires
`extensions.worktreeConfig=true` and a matching
`tasks/ongoing/<identity>/.gitkeep` on the refreshed shared primary branch.
Never infer it or fall back to `task-ledger.defaultIdentity`; that global value
is only an initialization suggestion. If setup is missing, follow the
[adoption guide](./references/adoption.md) before task work.

Run `repoledger check` after task-artifact changes and in CI. The CLI validates
facts but never decides admission, ownership, acceptance, or lifecycle state,
and it never mutates task state. Without the CLI, apply the same checks in this
skill and the repository profile.

## Publish Milestones

The repository profile names the shared remote, primary branch, and normal
direct-push, merge, or pull-request path. Accepted task work authorizes routine
non-force commits and publication through that path; do not ask permission
solely for those steps.

Before each publication, refresh the remote, reconcile concurrent work without
discarding it, run focused checks, publish, and verify the commit is reachable
from the refreshed remote primary branch. Local commits, side branches, and
unmerged pull requests are not published milestones.

Authentication, branch protection, required review, failed validation, push
rejection, and conflicts remain real blockers. Never force-push around them.
Record the blocker and exact next action in `Progress.md`, then ask only for the
required user action.

Every completed task has at least three distinct integrations:

1. **Claim:** task moved to the current identity before implementation.
2. **Implementation complete:** implementation and evidence published while
   the task is still ongoing.
3. **Archive:** completed task moved to `tasks/archived/` as a separate final
   integration.

Never combine claim with implementation completion or implementation
completion with archive publication.

## Create And Claim

After `task-new` intake and admission:

1. Create `tasks/backlog/<task-name>/Task.md` from the
   [task template](./assets/Task.md). Record the accepted goal, scope,
   constraints, observable acceptance criteria, and task-specific human review
   plan rather than a transcript. Task creation plans approval gates; it does
   not satisfy them.
2. Keep Issues or another external tracker available for open intake and link
   it bidirectionally when possible.
3. Refresh the shared branch and recheck all backlog and ongoing tasks.
4. Move the whole folder with `git mv` to
   `tasks/ongoing/<identity>/<task-name>`.
5. Create `Progress.md` from the [progress template](./assets/Progress.md),
   copy the planned human checkpoints and their current status, record current
   state and next action, and apply the move checks below.
6. Commit only the claim artifacts, publish them, and verify the claim before
   substantive implementation.

## Work And Coordinate

- Keep `Task.md` durable; put chronology, current state, decisions, validation,
   human approval evidence, blockers, checklist state, and the next concrete
   action in `Progress.md`.
- Publish meaningful validated checkpoints with current progress evidence. Do
   not publish known-broken work merely to create a checkpoint.
- Keep task-specific research with the task. Put only stable project consensus
   in `docs/`.
- Never store credentials, tokens, private keys, private customer data, or
   machine-local secrets in task artifacts.

A claim advertises intent but is not a lock. If another task overlaps, stop
before expanding the implementation, refresh the shared branch, compare scope
and state, coordinate ownership or sequencing, record the resolution, and
preserve both actors' work.

## Pass Human Review Checkpoints

Every new task plans five checkpoint categories in `Task.md`. Scope alignment
and delivery acceptance are required for completed work. Interface, business
and data model, and architecture checkpoints are required when the task affects
those surfaces; otherwise record a reason they do not apply or the concrete
trigger that will decide during execution. The middle checkpoints may be
reordered to follow task dependencies.

Before resuming a backlog or ongoing task that predates this plan, add and
publish its task-specific checkpoints without claiming that prior discussion
was approval. Do not retrofit archived task history solely for this change.

The checkpoints cover:

1. **Scope alignment:** goal, included and excluded work, constraints, and
   acceptance criteria before substantive implementation.
2. **Interface alignment:** affected GUI flows, CLI commands, MCP tools, or API
   contracts, including compatibility, before implementing that interface.
3. **Business and data model alignment:** concepts, rules, entities,
   relationships, schemas, and migration impact before implementing those
   model or data changes.
4. **Architecture alignment:** affected modules, responsibilities, boundaries,
   dependencies, and any split or combination before structural implementation.
5. **Delivery acceptance:** the integrated revision, validation evidence, and
   any manual test result before marking the task completed and archiving it.

Claim publication and research needed to prepare a review artifact may happen
before approval. At each applicable gate:

1. Prepare the concrete review artifact and summarize it in `Progress.md`, with
   a durable link when available.
2. Publish the artifact and pending gate state to the shared primary branch.
3. Ask the named human reviewer for an explicit decision and stop before the
   work that the gate protects.
4. Record the actual decision, reviewer, date, and concise evidence in
   `Progress.md`; publish that approval before continuing through the gate.

Do not infer approval from task creation, a `task-exec` invocation, silence,
routine Git authorization, or an earlier approval of a materially different
plan. Resolve every `Assess during execution` row before its trigger is crossed.
If implementation changes invalidate an approved artifact or introduce a
previously excluded surface, reopen the affected checkpoint, publish that
state, and obtain fresh approval. An abandoned task may archive with unresolved
checkpoints when `Progress.md` records the reason; do not label it completed.

## Verify Every Move

After a claim, handoff, archive, abandonment, or layout migration:

1. Verify the destination contains every artifact.
2. Verify the source task directory is gone. Remove it only when empty; stop if
    unexpected files remain.
3. Count non-hidden task directories across backlog, every ongoing identity,
    and archive, including empty directories. The task must appear exactly once.

Never copy tasks between positions. Preserve identity `.gitkeep` files.

## Run User Acceptance

Create a manual acceptance procedure only when a criterion depends on user
operation, user-only access, physical interaction, or another result the agent
cannot verify. This procedure tests the delivered behavior; it is distinct
from the required human delivery-acceptance decision. Do not invent manual test
steps for criteria the agent can verify.

When required, create `UserAcceptance.md` from the
[template](./assets/UserAcceptance.md) with exact prerequisites, numbered
actions, expected results, and an unambiguous reporting method. Publish it with
implementation completion and keep the task ongoing. Record only the result
the user reports. On failure, record the observation, fix and republish, then
repeat acceptance. On success, record the test result and continue to the
delivery checkpoint without requesting routine Git confirmation. A single user
response may satisfy both the manual test result and delivery approval only
when it explicitly states both decisions; record them separately.

## Handoff

Update `Progress.md`, verify the destination identity is registered, move the
whole task to `tasks/ongoing/<new-identity>/<task-name>`, apply the move checks,
and publish the handoff before either identity continues.

## Complete Or Abandon

To complete:

1. Finish all agent-verifiable criteria, run focused validation, and update
   `Task.md` and `Progress.md` with actual results.
2. Publish implementation completion while the task remains ongoing and verify
   it on the refreshed remote branch.
3. Complete any required manual user acceptance.
4. Present the delivery checkpoint, obtain explicit human approval, record and
   publish it, and mark `Completed` only after every required criterion and
   review checkpoint passes.
5. Mark archive publication as the final checklist action, move the whole task
   to `tasks/archived/<task-name>`, apply the move checks, then commit, publish,
   and verify this separate final integration.

To abandon, record the reason, useful findings, validation state, and follow-up
in `Progress.md`; set `Abandoned`, archive, and publish. Do not claim
implementation completion for unfinished work.

Archived tasks have no identity layer; Git history preserves prior ownership.

## Link Task Artifacts

Use a file-relative link for every target stored inside the current task
directory, such as `./Progress.md` or `./UserAcceptance.md`. The task directory
moves as a unit, so these links remain valid across lifecycle moves regardless
of renderer behavior.

For repository-local targets outside the task directory, use
`/path/from/repository/root` only when the repository profile declares that all
supported renderers resolve it. Otherwise use portable file-relative links and
update them when tasks move. Preserve external and fragment-only links, and
never couple local links to a machine path, repository owner, remote, or branch.

## Canonical Layout

```text
tasks/
|-- backlog/
|   `-- <task-name>/
|       `-- Task.md
|-- ongoing/
|   `-- <identity>/
|       |-- .gitkeep
|       `-- <task-name>/
|           |-- Task.md
|           |-- Progress.md
|           `-- UserAcceptance.md  # only when manual acceptance is required
`-- archived/
   `-- <task-name>/
      |-- Task.md
      |-- Progress.md
      `-- UserAcceptance.md      # preserved when one was required
```

For project setup, instruction wording, validation invariants, and migration
from a flat `ongoing/`, follow [the adoption guide](./references/adoption.md).