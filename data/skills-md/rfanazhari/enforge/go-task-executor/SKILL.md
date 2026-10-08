---
name: go-task-executor
description: Executes a Go engineering task-plan (typically the task-plan output from engineering-tripack-generator, or any pasted task doc) by writing actual Go code and tests against the team's internal Go coding standards (Clean Architecture, DDD, TDD). Use this whenever the user pastes/embeds a task-plan or a task description and asks Claude to implement it, build it, code it, or execute it in Go — not just plan or audit it. The user must tag each task (or the whole doc) as either "new" or "legacy" code; if that tag is missing, ask for it before writing any code. Trigger on phrases like "go-task-executor:", "execute this task plan", "implement this in Go following our standards", or a pasted checklist of Go implementation tasks.
---

# Go Task Executor

Turns a task-plan (markdown checklist, usually produced upstream by
`engineering-tripack-generator`) into actual Go code + tests, enforcing the
team's internal Go standards. This is the execution step at the end of the
planning chain — it writes files, it doesn't just analyze or plan.

## Before doing anything: confirm the mode

Every task must be tagged **`new`** or **`legacy`** — either once for the
whole document, or per task item if the doc mixes both. This tag changes how
the task is executed (see below). **If the user's prompt or task doc doesn't
say which mode applies, stop and ask before writing any code.** Never guess
this from the codebase — the user decides it explicitly, per their own
workflow.

## Step 1: Load the standards reference

Read `references/go-standards.md` before writing or editing anything. It is
the execution-relevant subset of the team's `BE_Coding_Standards.md`
(naming, struct/constructor rules, testing/TDD, folder layout, error
handling, Clean Architecture rules, DDD tactical design, logging,
observability spans). Treat it as binding, not optional style advice.

## Step 2: Execute per mode

### Mode: `new`

Greenfield task — no existing legacy constraints to respect.

1. Place files per the standard folder layout in §6 of the reference
   (`domain/`, `application/`, `infrastructure/`, `delivery/`, `pkg/`, etc.).
2. Follow full TDD: write the failing test first, then the minimum code to
   pass it, then refactor. This applies especially to anything landing in
   `domain/` or `application/usecase/` (80% coverage floor, per §5).
3. Constructors carry business validation (§2); private helpers and
   constructors are ordered per §1–2; errors are predefined in
   `pkg/errorcodes`, never ad-hoc `errors.New(...)` inline (§7).
4. Add tracing spans per the layer conventions in §11 wherever the new code
   crosses a layer boundary (controller, repository, external call, cache).

### Mode: `legacy`

Existing code, existing structure — the constraint is "don't break it,"
not "make it textbook."

1. Keep the existing file/folder structure and existing naming patterns in
   the touched area. Do not restructure files that are outside the task's
   scope, even if they violate §6/§8 — that's a separate refactor task, not
   this one.
2. Apply the standards from `references/go-standards.md` to *what you touch
   or add*, as far as possible without a structural rewrite. If a standard
   genuinely can't be applied without out-of-scope restructuring, say so
   explicitly in the final summary instead of silently skipping it or
   silently doing the big rewrite.
3. **Testing is contextual, not uniform TDD** (see the "Legacy-code testing
   note" in reference §5):
   - Touched code has no existing test → write a characterization test
     first (captures current behavior), then make the change safely.
   - The task adds genuinely new logic (new branch, new use case, new
     function) inside otherwise-legacy code → do normal TDD for that new
     logic specifically.
   - The task is a small, mechanical patch (rename, constant change, guard
     clause) with clear existing coverage → tests-after is fine; don't
     manufacture a TDD ceremony for it.
   When unsure which of these three a task item is, say which one you
   picked and why in the summary — don't silently default to the loosest
   option.

## Step 3: Write the code

Write real files (not just a description of what to write). Use the
project's actual existing packages/imports/conventions where mode is
`legacy`; use the standard layout where mode is `new`.

## Step 4: End with a short execution summary

For every task executed, report:
- Files created/modified (path list).
- Mode used (`new`/`legacy`) and, for legacy, which testing approach was
  picked per the Step 2 rule above.
- Which standards were applied, and — for legacy only — which standard was
  knowingly **not** fully applied and why (scope, risk of breaking
  behavior, etc.).

Don't restate the whole task-plan back to the user; the summary is about
what changed, not what was asked.

## Related

- Upstream: `engineering-tripack-generator` produces the task-plan this
  skill consumes.
- Sibling: `go-arch-auditor` uses the same `[LEGACY]` framing for flagging
  standard violations — this skill is the one that actually acts on a
  task, not just flags things.
