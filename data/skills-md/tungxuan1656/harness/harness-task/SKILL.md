---
name: harness-task
description: >-
  Assess incoming work in repositories governed by Harness and choose no
  task record, an inline task plan, or a separate linked plan. Use for code,
  documentation, bugs, migrations, reviews, and investigations under that
  harness. Do not impose Harness artifacts outside it or orchestrate skills.
---

# Harness Task

Choose the smallest artifact level that keeps approved work safe and resumable.
A task can be a feature, fix, investigation, or documentation change; its label
and file count do not determine planning cost.

## Assess

1. Read applicable instructions and the requested outcome.
2. Inspect the relevant tracker or task only when work needs or affects tracked state.
3. Inspect the affected slice for risk, execution horizon, dependencies, and ownership.
4. Use the [routing matrix](references/task-routing-matrix.md).
5. Reuse sufficient canonical tracking before creating a task.
6. State the choice and strongest reason in one sentence; continue the work.

Do not run broad verification just to classify a request. Ask only about facts
that materially change scope, artifact level, or safe execution. When choosing next work
or coordinating local tasks, run `node <path-to-harness>/scripts/task-ready.mjs [tasks-dir]`
to find unblocked candidates without reading every task into context.

## Apply

- **No task record**: default for questions, reviews, lookups, and small clear,
  reversible work that safely fits one session. Create no plan or progress log.
- **Task with inline plan**: preserve scope, acceptance, evidence, and handoff
  when persistence is useful but execution remains one bounded unit.
- **Task with separate plan**: link the canonical plan only when dependent
  phases, coordination, recovery, or high-impact controls require durable sequencing.

Reuse accessible external tracking that owns the required truth; do not mirror
its status locally. Otherwise use `tasks/task-<slug>.md` or the repository's
native task path. Use tracker IDs or descriptive slugs, not global counters.
Each local task owns its status, owner, evidence, blockers, and next action.
Independent tasks can be active concurrently. Coordinate overlapping files;
a task document does not reserve them.

## Decompose an approved spec

When asked to turn a spec into tasks, map observable acceptance to the smallest
independently verifiable deliverables. Link the canonical spec, name non-goals,
and include necessary tests/docs with the implementation rather than creating
artificial analysis/design/test phases. Do not fabricate missing product rules.

Use an epic or subtasks only for a real coordination boundary. Put shared scope
in the parent and specific acceptance/dependencies in each child; no mirrored
child status. Distinguish dependencies needed to start from integration/release
gates. A vertical slice is a useful deliverable, not a rule that every task
must finish before another starts. State which work can safely proceed in parallel.

Update the roadmap links only when task membership changes. At closure, extract
durable knowledge and check incoming references before removing disposable tasks.

## Boundaries

- Repository scale modifies risk and discovery cost; it does not mandate a plan.
- A small security or destructive-data change can need durable safeguards.
- Reuse in-scope tasks; never fold unrelated work into them.
- Honor explicit artifact requests and repository-native paths.
- A requested index is navigation/roadmap, not duplicated status or dependencies.
- Do not create root progress logs or records just for this assessment.
- Do not invoke or replace other design, implementation, review, or verification skills.
