---
name: code-review
description: >-
  Perform structured, multi-dimensional code reviews aligned with the
  `spec-driven-workflow` (`workflow/SPEC.md`, `workflow/PLAN.md`,
  `workflow/REVIEW.md`). Use this skill after implementing a feature or bug fix,
  before merging a PR, or when reviewing changes written by another agent or
  human.
---

# Code Review

Review code changes against both **engineering quality** and **specification intent**, recording every actionable finding in `workflow/REVIEW.md`.

## Review Philosophy

- **Net improvement over perfection**: Approve changes that clearly improve overall code health and satisfy `workflow/SPEC.md`, even if minor stylistic preferences differ.
- **Evidence over opinion**: Ground every finding in a concrete file path, line range or symbol, and explain *why* it matters.
- **Zero silent passes**: Do not approve or finish work while any `blocker` or `major` finding remains `open`.

## 1. Load Workflow Context First

Before inspecting the diff, read the active `workflow/` artifacts (or `workflow/<change-slug>/` for scoped parallel work):

1. **`workflow/SPEC.md`** — Verify goals, non-goals, constraints, and acceptance criteria.
2. **`workflow/PLAN.md`** (and **`workflow/TASKS.md`**, if present) — Understand the intended technical approach and module scope.
3. **`workflow/REVIEW.md`** — Check prior review rounds so resolved items are not re-reported and open items are re-verified.

If `workflow/REVIEW.md` does not exist yet, create it (using the `spec-driven-workflow` `REVIEW.md` template if installed).

## 2. Five-Axis Review Framework

Evaluate the diff (e.g., `git diff`, staged changes, or target PR) across all five dimensions:

1. **Correctness & Spec Alignment**
   - Does the implementation satisfy every acceptance criterion in `workflow/SPEC.md`?
   - Does it stay within scope (no unintended changes outside `SPEC.md` / `PLAN.md`)?
   - Are edge cases (null/empty values, boundaries, concurrency) and error paths handled?
   - Do tests verify the new behavior and guard against regressions?
2. **Readability & Simplicity**
   - Are names clear and consistent with the codebase?
   - Is control flow shallow and easy to follow without dead code or over-engineering?
3. **Architecture & Maintainability**
   - Does the change follow existing codebase patterns and respect module boundaries?
   - Does it avoid duplicated logic or unnecessary coupling?
4. **Security**
   - Is untrusted input validated and sanitized at system boundaries?
   - Are secrets, tokens, and sensitive data kept out of code, configs, and logs?
   - Are queries parameterized and auth/authorization checks enforced?
5. **Performance**
   - Are there obvious N+1 queries, unbounded loops/fetches, memory leaks, or blocking I/O on hot paths?

## 3. Record Findings in `workflow/REVIEW.md`

Log every finding in `workflow/REVIEW.md` using consistent severity tiers and resolution statuses:

- **Severities**:
  - `blocker`: Must be fixed before completion (broken spec requirement, security flaw, data-loss risk, failing build/tests).
  - `major`: Must be addressed before completion (edge-case bug, weak error handling, architectural violation, missing test coverage).
  - `minor`: Optional improvement or nit (naming, minor readability cleanup); never blocks approval.
  - `question`: Clarification needed from the author or implementing agent.
- **Statuses**: `open` | `resolved` | `wontfix` (with brief rationale).

Each finding entry must include:
- A unique ID (e.g., `[R1]`, `[Q1]`), exact file path and line/symbol reference, severity, status, **Issue**, and **Action**.

## 4. Verification & Sign-Off

1. Run the project's verification commands (`test`, `lint`, `typecheck`, `build` as applicable) rather than relying on inspection alone.
2. Update `workflow/REVIEW.md` status (`Open` | `Changes Requested` | `Approved`):
   - **Approved**: All `SPEC.md` acceptance criteria are met, checks pass, and zero `blocker` or `major` items remain `open`.
   - **Changes Requested**: One or more `blocker` or `major` items remain `open`.
3. Follow the `spec-driven-workflow` cleanup rule: **never delete** `workflow/REVIEW.md`; only clear/reset its contents after the user confirms everything is ready.
