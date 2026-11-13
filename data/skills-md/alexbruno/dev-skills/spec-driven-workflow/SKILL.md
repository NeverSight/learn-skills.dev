---
name: spec-driven-workflow
description: >-
  Default software engineering workflow using a `workflow/` directory with
  `SPEC.md`, `PLAN.md`, `TASKS.md`, and `REVIEW.md`. Use this skill as the
  standard process whenever starting a feature, bug fix, refactoring,
  architecture change, or code review—to specify requirements, plan execution,
  coordinate parallel tasks, and track review findings.
---

# Spec-Driven Workflow

Adopt this workflow as the **standard software engineering process** for any non-trivial change. Do not jump straight into writing code; follow the gated lifecycle below using the `workflow/` directory to separate **what** needs to change (`SPEC.md`), **how** it will be built (`PLAN.md`), **who** executes independent pieces (`TASKS.md`), and **what** needs attention after implementation (`REVIEW.md`).

## Standard Operating Flow

Follow these phases in order:

1. **Specify (`SPEC.md`)** — Define the problem, scope, constraints, and acceptance criteria before designing or coding.
2. **Plan (`PLAN.md`)** — Map the technical approach, affected files, ordered steps, and verification strategy.
3. **Shard (`TASKS.md`, conditional)** — Break the plan into trackable tasks only when complexity, multi-scope work, or parallel execution warrants it.
4. **Implement** — Execute against `PLAN.md` (or `TASKS.md`), keeping artifact statuses current as work progresses.
5. **Review (`REVIEW.md`)** — Record code review findings (human or agent) and resolve blockers/major issues before completion.

> **Trivial changes exception**: Skip `workflow/` artifacts only for trivial, self-contained edits (e.g., typo fixes, single-line formatting, or minor comment updates) where specification and planning add no value.

## Directory Layout

By default, create artifacts at the repository root under `workflow/`:

```text
workflow/
├── SPEC.md      # Required for any non-trivial change
├── PLAN.md      # Required before implementation starts
├── TASKS.md     # Optional: only for large plans or parallel/async agent work
└── REVIEW.md    # Created during human or agent code review
```

If multiple independent initiatives run concurrently in the same repository, scope each one under `workflow/<change-slug>/` instead of overwriting root files.

If the `workflow/` directory or any required artifact does not exist yet, **create the directory and initialize the missing files automatically** using the templates in `./resources/`.

### Version Control (`.gitignore`)

The `workflow/` directory contains local process-management and guidance artifacts and **must never be tracked by Git**:

- Ensure `workflow/` is listed in the repository's `.gitignore` (add it automatically when initializing `workflow/` if missing).
- Never stage (`git add`) or commit `workflow/` or any files inside it. If `workflow/` is somehow already tracked, warn the user before untrack/cleanup operations.

## Artifact Lifecycle

### 1. `workflow/SPEC.md` — Define the Change

Create `SPEC.md` first for any new feature, bug fix, or architectural change.

- **Purpose**: Align on scope, behavior, constraints, and acceptance criteria before writing code.
- **Template**: Start from [SPEC.md](./resources/SPEC.md).
- **Rules**:
  - State both **Goals** and **Non-Goals** to prevent scope creep.
  - Write testable **Acceptance Criteria** so completion is objective.
  - For bug fixes, document reproduction steps, expected vs. actual behavior, and root cause (once known).

### 2. `workflow/PLAN.md` — Map Execution Steps

Create `PLAN.md` once `SPEC.md` is clear.

- **Purpose**: Translate the specification into concrete, ordered engineering steps.
- **Template**: Start from [PLAN.md](./resources/PLAN.md).
- **Rules**:
  - Reference `SPEC.md` requirements; do not duplicate the full spec.
  - List affected files/modules, ordered implementation steps, and a concrete verification strategy (tests, linters, manual checks).
  - Highlight risks, migrations, or rollback considerations if applicable.

### 3. `workflow/TASKS.md` — Shard Large or Parallel Work (Conditional)

Create `TASKS.md` **only** when at least one of these conditions holds:

1. The `PLAN.md` is too large or comprehensive to execute cleanly in a single pass.
2. The `PLAN.md` spans two or more distinct project scopes (e.g., frontend, backend, infra, or multiple packages), task types (`feature`, `bugfix`, `refactor`, `docs`), or independent deliverables that benefit from separate tracking.
3. Work can be split into independent units executed **in parallel or asynchronously** by different agents or contributors.

- **Template**: Start from [TASKS.md](./resources/TASKS.md).
- **Rules**:
  - Skip `TASKS.md` for small, linear changes where `PLAN.md` is sufficient.
  - Every task must specify an ID, status (`pending`, `in_progress`, `blocked`, `done`), dependencies, owned files/scope (to avoid merge conflicts between parallel agents), and clear done criteria.
  - Keep task statuses updated as work progresses.

### 4. `workflow/REVIEW.md` — Record Code Review Findings

Create or update `REVIEW.md` when a human or reviewing agent inspects the implemented changes.

- **Purpose**: Centralize actionable review observations that require attention before merging.
- **Template**: Start from [REVIEW.md](./resources/REVIEW.md).
- **Rules**:
  - Categorize every observation by severity (`blocker`, `major`, `minor`, `question`).
  - Point to exact file paths, line ranges, or symbols, and explain *why* the issue matters.
  - Track resolution status (`open`, `resolved`, `wontfix`) so nothing is lost across review rounds.

## Verification & Cleanup

Before considering the workflow complete:

1. Every acceptance criterion in `workflow/SPEC.md` is satisfied and verified by tests or explicit checks.
2. All steps in `workflow/PLAN.md` (and `workflow/TASKS.md`, if used) are completed or explicitly deferred.
3. All `blocker` and `major` items in `workflow/REVIEW.md` are marked `resolved` (or `wontfix` with rationale).
4. **Ask the user for final sign-off and cleanup**: Once the plan, tasks (if any), and review are complete, explicitly ask the user if everything is ready and whether the `workflow/` artifacts can be cleaned up.
   - **Never delete** the root `workflow/` directory or its root files (`SPEC.md`, `PLAN.md`, `TASKS.md`, `REVIEW.md`).
   - When the user confirms cleanup, **clear/reset the contents** of the root files (e.g., emptying them or resetting them to their blank templates) while keeping the directory and files intact.
   - **Exception**: Subdirectories created inside `workflow/` by agents working in parallel on independent executions (e.g., `workflow/<change-slug>/`) **may be deleted** upon user confirmation.
