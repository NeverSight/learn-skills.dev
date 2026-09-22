---
name: repoledger
description: "Create, execute, inspect, complete, or abandon explicitly opted-in repository tasks through Repoledger. Ordinary implementation requests remain task-free."
argument-hint: "<new [--language <tag>] [context]|exec [task]|status [task]|complete [task]|abandon [task]>"
user-invocable: true
---

# Repoledger

Manage explicitly opted-in implementation work as stable repository state on a
shared primary branch. Repoledger validates and publishes lifecycle facts; it
does not decide intent, semantic overlap, human approval, or code correctness.

## Route The Request

For an explicit `/repoledger` invocation, route by the first argument. Treat it
as a verb, not as free-form task context:

- `new [--language <tag>] [context]`: admit one accepted implementation
  outcome and register it in backlog. `--language` overrides the project
  default and user preference for this task only. Stop after registration; do
  not start or implement it.
- `exec [task]`: resolve one existing task, start or resume it, and follow the
  lifecycle until it is terminal or genuinely blocked.
- `status [task]`: list tasks when no task is supplied, or report and remotely
  check one resolved task. Do not mutate task state or implementation files.
- `complete [task]`: resume one ongoing task at the delivery boundary. Verify
  all completion requirements and request approval for the exact current
  primary commit. The invocation itself is not delivery approval and must not
  call `task complete` directly.
- `abandon [task]`: resolve one nonterminal task and require an explicit human
  decision to abandon that outcome before changing its state.

For a missing or unknown verb, show the supported forms and stop without
changing task or implementation state. Repository instructions may also load
this skill for an explicit request to manage an existing registered task; route
that request as `exec`. Never infer `new` from an ordinary implementation
request, task size, duration, or a suggestion from the agent.

## Admit Work

- Create a task only after the user explicitly invokes `/repoledger new`.
- Admit only an accepted outcome expected to change at least one tracked path
  outside the configured `tasksDirectory`. Source, tests, docs, configuration,
  workflows, scripts, instructions, and skills all count.
- Do not admit questions, read-only investigation, planning or review without
  implementation, validation-only work, external-only work, or changes confined
  to the task directory.
- Once registered, manage the task until it becomes `completed` or `abandoned`.

For cross-repository work, the repository owning the primary implementation
owns the source task. Create a linked task only when another repository owns an
independent implementation outcome.

## Task Language

Every registered task has one stable language track recorded in `Task.md` as
`Language: <canonical-tag>`. The tag is canonical BCP 47, such as `en` or
`zh-CN`. It controls narrative prose, not machine protocol.

For `/repoledger new`, run
`repoledger config resolve task-language [--language <tag>] --json`
before preparing `Task.md`. Pass `--language` only when the invocation includes
the one-task override. Resolution is deterministic: invocation override, then
the project default in `repoledger.yaml`, then the user preference, then `en`.
Use the returned value for agent-authored user-facing narrative replies during
task creation and record it in `Task.md`; never record the resolution source or
configuration paths. The project default is optional shared repository state.
Manage the persistent user fallback with
`repoledger config get --global task-language` and
`repoledger config set --global task-language <tag>`. User preferences stay
outside repositories and never modify `repoledger.yaml`. Use
`repoledger config resolve --global task-language` only when resolving outside
a repository and intentionally skipping the project default.

For every existing task, read its recorded `Language` from the authoritative
`Task.md` or `repoledger status`; do not re-resolve the current user's
preference. A legacy task without `Language` uses `en`. Never infer language
from prose, translate existing artifacts, or change a task's language during
resume or handoff. During `/repoledger exec` and `/repoledger complete`, use
the task's recorded language for agent-authored user-facing narrative replies,
even when the current project default or user preference differs.

Write narrative titles, goals, context, scope, criteria, decisions, validation,
blockers, evidence, and user instructions in the task language. Keep required
Markdown headings, checkpoint names, applicability and approval values,
outcomes, acceptance statuses, commands, identifiers, and other validated
protocol markers in English exactly as the templates define them. Preserve
quoted tool output in its original form.

## Prepare Task Work

1. Read repository instructions and the repository task profile.
2. Run `repoledger task list` to inventory current primary state and read only
   plausible overlaps.
3. Run `repoledger status <task-name>` and
   `repoledger check <task-name> --remote` before resuming one task.
4. Read its stable `Task.md`, task language, and any existing `Progress.md`
  from primary.
5. Preserve unrelated work and stop on semantic overlap or same-task conflicts.

The configured primary repository and branch are authoritative. Their
credential-free HTTPS URL and branch name are shared state, while local Git
remote names, credentials, and URL rewrites are not. Every ongoing task
advertises one source repository and branch so work can continue from another
clone. The source ref is mutable collaboration state, not accepted history;
accepted work must return to primary.

## Create And Start

After `/repoledger new` admission:

1. Resolve the task language as described above.
2. Prepare `<tasksDirectory>/<task-name>/Task.md` from the task template and
  record the resolved canonical `Language`.
3. Run `repoledger task register <task-name>`. It snapshots that local task
   directory and publishes the backlog record and artifacts to primary.
4. Synchronize the caller's local primary checkout as described below, then
  stop without starting or implementing the task. A later `/repoledger exec`
  invocation owns that transition.

Registration publishes from an isolated worktree and deliberately leaves the
caller's checkout unchanged. After successful publication, use the returned
`primaryAfter` commit to fast-forward the caller's checked-out primary branch
to the exact published commit. First verify that the current branch is the
configured primary branch. Temporarily move the local task directory outside
the worktree, fast-forward to `primaryAfter`, compare the restored tracked task
directory with the saved input, and remove the saved copy only when they are
identical. Preserve unrelated index and worktree changes. If the branch cannot
fast-forward or the directories differ, restore or retain the saved input and
report the blocker; never reset, silently switch branches, or discard content.
Do not finish `/repoledger new` with remote primary ahead of the checked-out
local primary branch.

When execution begins, run `repoledger task start <task-name>`. The source
defaults to `task/<task-name>` in the primary repository; use
`--source-repository` for a fork or `--source-branch` for an intentional
override. Repoledger publishes `backlog -> ongoing` and creates the shared
source ref without changing the caller's checkout or creating `Progress.md`.

## Work And Progress

`Task.md` is the durable outcome contract. `Progress.md` is an implementation
journal, not a transcript or a mirror of Git.

- Create or update `Progress.md` only in a publication that also creates,
  modifies, renames, or deletes at least one path outside `tasksDirectory`.
- In that same commit, record only outcome-relevant implementation changes,
  material decisions, validation, blockers, and the next action.
- Write narrative Progress content in the task's recorded language while
  preserving the template's English headings and canonical review values.
- Never create a standalone Progress commit for fetches, checks, pushes, commit
  hashes, reachability, status transitions, resumes, handoffs, review requests,
  approvals without implementation, or task-only document edits.
- Git already records exact commit identity, chronology, and publication.
- Publish validated implementation non-force to the exact source ref reported
  by `repoledger status`, then integrate it through the repository's normal
  primary path. Never force-push, silently switch repositories or branches, or
  discard concurrent work.

If work becomes blocked and there is no implementation delta to publish, report
the blocker to the user without manufacturing a Progress update.

## Human Review

Every new task plans scope and delivery review. Interface, business/data model,
and architecture review apply when those surfaces change.

- Scope and interface review requests link the canonical `Task.md` on primary
  so the user can open the review artifact directly. Do not require the user to
  provide or repeat a commit ID; associate the explicit decision with the
  refreshed authoritative revision internally.
- Other review requests identify their published artifact clearly. Delivery
  approval remains bound to the exact primary commit passed to
  `repoledger task complete --approved-commit`.
- Task-only review artifacts may be published without editing `Progress.md`.
- Approval is an explicit human decision; Git activity and silence are not
  approval.
- Approval alone does not create a metadata commit. If the decision materially
  affects later implementation, summarize it in the next implementation-linked
  Progress update.
- Reopen a checkpoint when later changes materially alter the reviewed result.

Do not cross a protected implementation gate until its required decision is
explicit. Routine non-force publication needs no separate permission.

## Resume And Handoff

A receiving agent fetches primary, runs status and remote check, reads the
stable artifacts, then fetches and continues from the advertised source ref.
Handoff changes no lifecycle field or source locator and does not update
`Progress.md`. Concurrent source or primary publication is resolved by normal
non-force Git integration, never by silent overwrite.

## User Acceptance

Create `UserAcceptance.md` only when a criterion requires user-only access,
physical interaction, or subjective judgment that the agent cannot verify.
Publish it with an implementation delta. Record only the result the user
reports, and require explicit delivery approval separately unless one response
clearly supplies both decisions.
Write its narrative instructions in the task language while preserving the
English headings and canonical acceptance statuses.

## Complete Or Abandon

To complete:

1. Finish acceptance criteria and agent-verifiable checks.
2. Publish the final implementation and its concise Progress update together.
3. Complete required manual acceptance.
4. Ask the user to approve the exact current primary commit for delivery.
5. Run `repoledger task complete <task-name> --approved-commit <commit>`.
  Repoledger requires that commit to equal fetched primary and contain the
  fetched source tip, removes the source locator from status, publishes the
  completed record, and verifies it. It does not delete the source branch. Do
  not add a completion-only Progress commit.

To abandon, obtain an explicit human or accountable-owner decision and run
`repoledger task abandon <task-name>`. Repoledger removes the source locator
from status but does not delete the source branch. Existing findings remain in
the latest implementation-linked Progress entry. Do not create
abandonment-only progress.

Terminal task directories remain at the same stable path. There is no archive
move, delete, rename, reopen, handoff, takeover, identity, or generic set-state
operation.

## Links And Layout

Use file-relative links for targets inside one task directory. Use the
repository profile's declared convention for targets elsewhere. Stable task
paths eliminate lifecycle link rewrites.

```text
repoledger.yaml
tasks/
|-- status.yaml
|-- <task-name>/
|   |-- Task.md
|   |-- Progress.md       # only after implementation publication
|   `-- UserAcceptance.md # only when required
`-- <another-task>/
    `-- Task.md
```

Run local `repoledger check` after task artifact changes, `repoledger check
--staged` for the index candidate, and `repoledger check --commit HEAD` for CI
on the checked-out commit. Use `repoledger check --remote` when CI or a human
must also validate refreshed primary and ongoing source refs. Follow the
[adoption guide](./references/adoption.md) for setup and legacy migration.
