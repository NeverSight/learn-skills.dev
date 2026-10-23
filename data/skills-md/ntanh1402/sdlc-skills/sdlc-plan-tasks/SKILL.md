---
name: sdlc-plan-tasks
description: Plan the build Tasks of a designed Feature or ChangeRequest in the project wiki, while its requirements are a draft or once they are agreed - ordered, independently verifiable Tasks with planned scope, acceptance, size, dependencies and parallel waves, covering every concept its design adds, changes or removes, each Task linked to the user stories it serves. Use when an architecture needs a task breakdown, implementation plan or backlog, when a design or spec changed and its Tasks must be replanned, or when user stories were written and the Tasks must link them. Not for requirements, architecture, test design, tracker sync or code.
---

# Plan the tasks

This skill is a lifecycle step after the design. It takes a Feature or
ChangeRequest whose design is merged, whether its Requirements are a draft or
agreed, and writes `TASK-<name>.md` files into its folder, so that every Design concept its
design adds, changes or removes is planned by exactly one Task, and every
user story in the folder is linked by at least one Task.

Its draft prefix is `tasks-`: the draft for `FEAT-coupons` is
`wiki/tasks-FEAT-coupons`. It may run at the same time as `sdlc-design-tests`
on the same design.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. Then read `references/decomposition-rules.md`, `references/task-sizing.md` and
`references/task-format.md`, and the schema pages `schema.md`, `task.md`,
`user-story.md`, `feature.md`, `change-request.md` and the page of each
Design type in scope,
in the wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| No approved design yet | `sdlc-design-arch` |
| Test cases or suites | `sdlc-design-tests` |
| User stories | `sdlc-write-stories` |
| Create or update tickets in Jira or another tracker | No skill does: a person creates the ticket by hand and may add `trackerKey` and `resource` to the Task |
| Explain the existing Tasks | `sdlc-ask-wiki` (no gates, nothing written) |
| Write the code of a Task | `sdlc-build-task` |
| Mark a Task `Done` | `sdlc-close-task`, after its code is merged |
| Add a ticket link to a Task | `sdlc-edit-wiki` |

## 1. Look up: readiness and the scope

Accept one `FEAT-*` or `CR-*` key. Read it on the default branch:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `Draft`, `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `Proposed`, `ReqApproved` or `Approved`, whose `# Architecture` or `# Delta` is not `None`; and `coverage tasks` reports uncovered concepts or stories no Task links, the design changed under `Todo` Tasks, or `outdated` lists a Task | Go on |
| `NEEDS_DESIGN` | `# Architecture` or `# Delta` is `None` | Stop: route to `sdlc-design-arch` |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft |
| `CLOSED` | A Feature that is `Released` or `Deprecated`, or a ChangeRequest that is `Implemented` or `Rejected` | Stop: say it is closed; a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`); route nowhere else |
| `ALREADY_CURRENT` | `coverage tasks` and `outdated` report nothing and every Task matches the design | Report the existing plan and stop |

```bash
$T coverage tasks --feature FEAT-coupons      # or --change CR-sms-alerts
$T outdated --feature FEAT-coupons            # Tasks planned from an older spec version
```

When `outdated` also lists the design itself (`designBasedOn` older than
`version`), say in the first round that the design is behind the spec and
recommend `sdlc-design-arch` first; go on only when the person says so. When
the Requirements are still a draft, say that the Tasks can be built but not
closed until they are agreed (`sdlc-close-task` refuses).

Every state but `READY` is a refusal, not a question.

Then read the Requirements, the Feature's `# Architecture` or the
ChangeRequest's `# Delta`, the decisions it links, every Design concept in
scope with its `# Pending changes` entry, every existing Task in the folder,
every user story in the folder with the Requirements it lists, and the
References all of these link.

Stories are optional and may not exist yet. Do not wait for them: when a
`wiki/stories-<Key>` draft is open, say so in the first round, and say that
running this skill again after it merges links the stories.

Build the scope inventory: every concept in the design qualified `new`,
`modified` or `removed`, plus the migration, compatibility, security,
observability, rollout and clean-up duties the design and its decisions
name. A frontend route, screen or `# Calls` change is scope like any other.
List the folder's stories beside the inventory, each with its Requirements.

## 2. Questions and the Intent gate

Ask in rounds, as `references/flow.md` section 4 says. The first round names
the target and its state, shows the scope inventory, and puts to the person
the choices of section 3 that are theirs: where the slices are cut, which
repository each concept is built in when the wiki does not say, the order
when two orders are possible, and what a spike must answer. It also holds:

- **started Tasks**, when Tasks exist. The wiki does not know whether a
  `Todo` Task has started or its code is already merged: list the `Todo`
  Tasks the design or the new spec version changes and ask which have
  started, and which have merged code;
- the wiki question. The usual answer is "nothing: only Task files and the
  folder's log"; a gap in the design that the planning found is another
  skill's change (`sdlc-write-spec` for a ChangeRequest, `sdlc-import` for a
  correction).

**Intent gate.** Restate the target, the scope inventory, the existing Tasks
and what you expect to add or change. Ask for approval
(`PLANNING BASIS CONFIRMED`).

## 3. What goes into the plan

Follow `references/decomposition-rules.md` and `references/task-sizing.md`:

- Vertical, independently reviewable and demonstrable slices; foundations,
  contracts and migrations before their consumers; risky spikes first.
- `taskType`: `dev`, `design` or `spike`. `test` only implements a TestSuite
  that is already approved; test design is `sdlc-design-tests`.
- Size XS to L. An XL Task is split.
- Each Task's `# Planned scope` links the concepts it builds, with the
  qualifier the design gave them. Each concept in the inventory has exactly
  one owning Task.
- `# Acceptance` states observable results and links the Requirements it
  satisfies by full path and anchor.
- `# Stories` links the stories the Task serves: those whose Requirements its
  `# Acceptance` satisfies. Every story of the folder is linked by at least
  one Task. A Task that serves no story (a migration, a spike, a
  Nonfunctional Requirement) has no `# Stories`. A Task links only stories of
  its own folder.
- `# Blocked by` links the Tasks it waits for; no cycles.
- `# References` links the References a developer needs for this Task: those
  the Feature or ChangeRequest and the Design files in its `# Planned scope`
  link, when they bear on its work, each with a note on what to take from
  it. Do not create a Reference; when one is missing, say which in the
  summary and name `sdlc-edit-wiki`.

**One repository.** A Task changes one code repository. Work that spans two
repositories is two Tasks, one blocked by the other when the order matters.

**Replanning.** Keep each existing Task's key. A `Done` Task is never
rewritten. A `Todo` Task that has not started may be changed to match the new
design. A Task the person said has started, or whose code is merged, is
treated like a `Done` one: if the design or the spec changed under it, add a
new Task for the difference, `# Blocked by` the old one, and say so at the
Design gate.

**Spec version.** Each Task's `basedOn` is
`{ version: <the parent's version>, at: <its versionDate> }`. Write it on
every new Task and on every Task you replan. A started or merged Task that
got a Task for the difference also gets the current `basedOn`: together they
cover the new version, so the old one can be closed. Its log entry says it
was built from the older version and names the new Task. A Task the new
version does not change gets the current `basedOn` too, once you have
checked it against the change.

**Story links on any Task.** Adding a `# Stories` link, or dropping one to a
story that no longer exists, is allowed on every Task, `Done` and started
ones included: it is traceability, not scope, and it is the only edit made
to those, besides `# References`. A run whose only work is linking stories
plans no new Task.

## 4. Run plan and the Design gate

Start or resume the draft `tasks-<Key>` as `references/write-protocol.md`
section 3 says. The input paths are the Feature's or ChangeRequest's
`overview.md` and, for a ChangeRequest, the target Feature's `overview.md`.

Prepare the task plan: in dependency order, one row per Task with its key,
title, type, size, repository, planned scope, stories, acceptance summary,
blockers and confidence; then the coverage matrix (each inventory row to its
owning Task, and each story to the Tasks that link it) and the parallel waves (Tasks with no unfinished blocker start
together).

Write the Run plan. Its `## Files` are one line per Task file, added or
changed, with its planned scope in a few words, and the folder's `log.md`.

**Design gate.** Show the task plan in full, never only a summary, then the
Run plan. Ask for approval (`TASK PLAN APPROVED`).

## 5. Write

In the draft worktree, in the Feature's or ChangeRequest's folder, write each
new Task as `TASK-<name>.md` with `references/task-format.md`, and edit the
`Todo` Tasks being replanned. Add an entry to the folder's `log.md`, for
example
`* **Tasks**: Planned 5 Tasks in 3 waves. Written by an AI model with sdlc-plan-tasks.`

Do not touch the Design concepts: their pending entries were written with the
design. Do not write `index.md`.

## 6. Self review, finish and commit

Follow `references/write-protocol.md` section 4 from step 5. In the self
review, also check that:

- `$T coverage tasks`, run in the worktree, reports nothing uncovered: no
  concept without its Task and no story without a Task;
- each concept of the inventory is in the `# Planned scope` of exactly one
  Task, and no Task is XL;
- every `# Acceptance` states an observable result and links its
  Requirements;
- no `Done` Task and no started Task was rewritten beyond its `# Stories`
  and `# References` links and its `basedOn`, and no Design concept or user
  story was touched;
- `$T outdated` lists no Task of the folder that is not `Done`.

Commit message: `tasks(<Key>): plan <n> tasks`. In the summary, "Next" names
the Tasks of the first wave: the ones that can start once the pull request
is merged. When the Requirements are still a draft, add that the Tasks can
be built but are closed only once the target is `Approved`.

## Done when

- The target, the scope inventory and the started Tasks were confirmed in the
  rounds, and the planning basis was approved at the Intent gate.
- Every concept and duty in the scope inventory has exactly one owning Task,
  and every user story of the folder is linked by a Task.
- No XL Task, no dependency cycle, no duplicate scope, no Task without
  observable acceptance.
- No Task that had started was rewritten, beyond its `# Stories` links and
  its `basedOn`.
- Every Task that is not `Done` has the parent's current `basedOn`.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `coverage tasks` reports nothing, `draft finish` was `ok`, the change set was
  approved, and `draft commit` reported the branch.
