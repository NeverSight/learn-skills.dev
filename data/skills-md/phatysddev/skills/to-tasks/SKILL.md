---
name: to-tasks
description: "Break a ready feature specification into small, implementation-ready vertical-slice tasks with complete acceptance-criteria coverage, explicit dependencies, session-ready context, and concrete verification. Use when a ready spec is too broad for one focused implementation session or needs durable work items for implementation and review."
---

# To Tasks

Turn one `ready` feature spec into a small dependency graph of implementation-ready tasks.

Each task should deliver a coherent, verifiable behavioral slice and contain enough context to be implemented in a fresh session.

Task files use a minimal checklist contract: after the task title and workflow
metadata, the body contains only `Goal`, `Blocked by`, and `Todo`. Put
acceptance-criteria references, implementation steps, verification, and the
task-scoped commit step in the Todo checklist instead of adding extra sections.

Do not implement code.

Do not change product scope.

Do not invent acceptance criteria.

Do not split work mechanically by technical layer unless that layer produces an independently meaningful outcome.

## Contents

- [Workflow](#workflow)
- [Read before planning](#read-before-planning)
- [Preconditions](#preconditions)
- [Inspect existing tasks first](#inspect-existing-tasks-first)
- [Build the acceptance map first](#build-the-acceptance-map-first)
- [Slice by behavior](#slice-by-behavior)
- [Task sizing](#task-sizing)
- [Dependencies](#dependencies)
- [Task files](#task-files)
- [Task templates and coverage](#task-templates-and-coverage)
- [Quality gate](#quality-gate)
- [Finish](#finish)

## Workflow

Follow this sequence:

```text
Read project context
        ↓
Validate target spec
        ↓
Inspect existing tasks for this spec
        ↓
Map acceptance criteria
        ↓
Design vertical slices
        ↓
Define dependencies
        ↓
Create or update tasks
        ↓
Verify complete coverage
        ↓
Identify first runnable task
        ↓
$implement-task
```

## Read before planning

Read `AGENTS.md` first if it exists.

Then inspect:

* the complete target spec;
* its linked requirement;
* relevant `CONTEXT.md`;
* relevant ADRs;
* `docs/workflow.md` when present;
* existing tasks for the same spec;
* prototype references in the spec and the referenced pages when UI behavior or
  states are part of the contract;
* relevant source structure when needed to understand practical task boundaries;
* repository commands needed for verification.

Read the canonical target spec in full. Do not pass the spec through
`$compact-context` before decomposition; temporary working notes may be
compacted only after the authoritative acceptance criteria remain available.

Do not read unrelated parts of the repository merely to produce a more detailed task list.

Preserve the repository's existing terminology, task format, status convention, and naming when usable.

## Preconditions

The target spec must be `ready`.

When the spec references a prototype, treat the spec and its acceptance
criteria as authoritative. Use the prototype only to understand accepted
visual states, hierarchy, and interaction evidence.

Do not decompose a `draft` spec as if implementation can safely begin.

If the spec contains a material unresolved question that affects:

* scope;
* behavior;
* permissions;
* business rules;
* architecture;
* acceptance criteria;

stop and route back to:

```text
$write-spec
```

when the specification itself is incomplete, or:

```text
$grill-workflow
```

when a new product, domain, or architecture decision is required.

Do not hide a missing decision inside an implementation task.

If an unaccepted proposal or conflict affects the behavior being decomposed,
stop and route to `$spec-with-prototype` or `$grill-workflow`; do not make
prototype interpretation part of a task. Explicitly excluded or non-blocking
proposals outside that behavior do not prevent planning the agreed contract.

## Changes to an existing agreement

Use `$change-scope` when a requested behavioral change requires coordinated
reconciliation of existing requirements, the owning spec, and its task plan.
Ordinary spec clarification or decomposition stays here. When this skill is
already supporting `change-scope` and the changed behavior is settled, complete
its scoped spec/planning work and return to that parent; do not route back to
`change-scope` again. Preserve delivered tasks and evidence, and plan follow-up
work for changed behavior instead of silently reopening completed tasks.

## Inspect existing tasks first

Before allocating new task IDs, inspect `docs/tasks/` for tasks already linked to the target spec.

When `$to-tasks` is rerun:

* preserve completed work;
* preserve valid task IDs;
* preserve evidence already recorded;
* update tasks whose boundaries must change;
* create only genuinely missing tasks;
* avoid duplicate work items.

If an existing task uses the older multi-section format, migrate it in place to
`Goal`, `Blocked by`, and `Todo`. Preserve its status, real blockers, and
completed work by converting relevant acceptance, verification, and evidence
details into checked Todo items; do not create a replacement task.

Do not generate:

```text
TASK-004-booking-form.md
TASK-009-build-booking-form.md
TASK-014-finish-booking-form.md
```

when they represent the same implementation slice.

If existing tasks already provide complete, valid coverage of the spec, leave them unchanged and report that decomposition is already complete.

## Build the acceptance map first

Before creating tasks, identify every active acceptance criterion in the spec.
Keep explicitly retired/superseded criteria as linked history, not new work;
exclude them only when the accepted owning contract says they no longer apply.
A difficult or unimplemented criterion is not implicitly retired.

Construct a working mapping:

```text
AC-01 → ?
AC-02 → ?
AC-03 → ?
```

Every `AC-##` must eventually map to at least one implementation task unless the criterion is already satisfied by existing implementation and that fact is explicitly verified.

Do not create new acceptance criteria in this skill.

Do not silently drop difficult criteria.

If an acceptance criterion cannot be assigned without inventing behavior or scope, stop and return the gap to `$write-spec`.

## Slice by behavior

Prefer the smallest coherent vertical slice that produces behavior which can be tested, demonstrated, or objectively verified.

Prototype creation and visual iteration are upstream workflow work, not
implementation tasks. Do not create tasks for `$to-prototype` or
`$edit-prototype`.

A vertical slice may cross multiple technical layers.

For example:

```text
Good

TASK-012: Customer can submit a booking

May include:
- validation
- application logic
- persistence
- endpoint/action
- UI submission
- tests
```

Avoid:

```text
TASK-012: Create database table
TASK-013: Build backend
TASK-014: Build frontend
```

when none of those tasks independently delivers or verifies the behavior described by the spec.

Technical-only tasks are acceptable when they represent a real independently necessary boundary, such as:

* schema migration required by multiple later slices;
* shared authorization primitive;
* external integration foundation;
* infrastructure prerequisite;
* explicit architecture work required by an ADR.

Do not manufacture technical prerequisites merely to make tasks smaller.

## Task sizing

A task should be small enough for one focused implementation session, but large enough to produce a coherent result.

A good task should usually have:

* one clear goal;
* a bounded behavioral outcome;
* known dependencies;
* a finite set of acceptance criteria;
* concrete verification;
* enough context to resume in a new chat.

Split a task when it contains multiple independently deliverable behaviors.

Merge tasks when splitting them would create artificial handoffs with no independently verifiable result.

Do not optimize for the highest possible task count.

Task count is not a quality metric.

## Dependencies

Express only real implementation dependencies.

Record them in the task's `Blocked by` section:

```markdown
## Blocked by

- None
```

or:

```markdown
## Blocked by

- TASK-###
- TASK-###
```

A blocked-by entry means the current task cannot reasonably reach its definition
of done until the listed task is complete. Do not add a separate `Depends on`
field.

Do not add dependencies merely because another task appears earlier in the list.

Prefer parallel work when tasks are genuinely independent.

The resulting task graph must:

* contain no cycles;
* use existing task IDs exactly;
* contain at least one runnable task when work can begin.

## Task files

Use the repository's existing task convention when one exists.

Otherwise create:

```text
docs/tasks/TASK-###-<short-slug>.md
```

Choose the next unused task ID.

Create `docs/tasks/` only when task files are actually being created.

Keep the task body limited to the three sections defined below. Retain only
the metadata needed for routing, such as `Status` and `Spec`.

## Task templates and coverage

When creating task files or checking decomposition completeness, read [the task templates and coverage reference](references/task-templates-and-coverage.md). It contains the task body contract, session context, verification, spike rules, and exhaustive acceptance/dependency/coverage checks.

## Quality gate

Before marking task decomposition complete, confirm:

* the target spec is `ready`;
* existing tasks were reconciled before new tasks were created;
* all acceptance criteria have task coverage;
* no hidden scope was introduced;
* tasks are appropriately sized;
* vertical slicing was preferred;
* dependencies form a valid DAG;
* at least one runnable task exists when implementation is possible;
* each task is session-ready;
* every task has verification;
* prototype-backed behavior is traceable through the spec rather than directly
  treated as a requirement;
* new Todo items remain unchecked until implementation;
* every task includes a conditional task-scoped commit Todo item;
* rerunning `$to-tasks` would not generate duplicate tasks.

If any check fails, fix the decomposition when possible.

If fixing it requires changing the behavioral contract, return to `$write-spec`.

## Finish

Report:

1. target spec;
2. tasks created;
3. tasks updated;
4. existing tasks left unchanged;
5. acceptance-criteria coverage;
6. dependency order;
7. tasks that can run in parallel, when useful;
8. first runnable task;
9. blockers, if any;
10. next skill.

Use this routing:

```text
spec problem discovered
    → $write-spec

product/domain/architecture decision required
    → $grill-workflow

runnable implementation task exists
    → $implement-task

all linked tasks already reviewed and done
    → report completed coverage and stop; do not request redundant review
```

Do not implement code.

Do not move a task to `in_progress`. When supporting `$change-scope`, return
affected review-readiness evidence to that parent; it owns any invalidation
transition under its scope-change contract.

Do not fabricate evidence.

Do not create additional scope merely to make decomposition look complete.
