---
name: onepatch
description: Take an unplanned fix or change from report to delivery — diagnose, confirm with the author, run test-fail-fix-reflect, and deliver to the working tree or as a PR.
---

# One Patch

Given a problem description, a failing test, or a failed GitHub Actions job, diagnose it, confirm the remedy with the author, fix it, and deliver — either to the working tree or as a pull request with every blocking check green.

## Input

The input is one of:

- a **description** of the problem;
- a **failing test**;
- a failed GitHub Actions **job**: a job id, run id, or run/job URL.

A failing test is run first, before any diagnosis, to confirm what fails. For CI input, read [ci.md](ci.md) for job resolution and triage.

## Fix or change

Say which one this is. A **fix** repairs a defect and runs the full test-fail-fix-reflect cycle below. A **change** alters intended behavior and skips reflect: there is no defect the process should have caught.

## Delivery

CI input defaults to PR delivery; anything else defaults to the working tree. The author may override either way.

Work starts in a clean tree unless the author says to add to dirty work. PR delivery works in its own worktree; see [pr.md](pr.md). Working-tree delivery ends uncommitted, with a proposed commit message under the rules below.

## Diagnose

Investigate with the project's tools — read the relevant code, search the codebase, inspect logs, run the code. Where the failure maps to a local command, reproduce it locally first. Present the diagnosis concisely, leading with the conclusion:

- **Root cause** (or **design**, for a change) — the specific mechanism, or the intended behavior and where it lands;
- **Evidence** — the code, log output, or behavior supporting it;
- **Scope** — what is and isn't affected;
- **Remedy** — the approach (not yet implemented).

## Confirmation gate

Ask the author before implementing, unless the remedy is simple and obvious. Small, localized remedies with clear evidence — a wrong flag, a null check, a test expectation, an obvious bug — may proceed. Anything the author would reasonably want to design first stops for approval: architecture changes, large cross-cutting refactors, behavior beyond the reported scope, deleting or rewriting substantial modules. When stopping, present the diagnosis with the remedy, the files touched, and the risks, and offer:

- **Full cycle** — test-fail-fix-reflect (a change skips reflect);
- **Quick fix** — implement directly: no new test, no reflect;
- **Another direction** — the author's text becomes the new framing; go back to Diagnose with it and do not reuse the previous diagnosis unless it still applies.

Ask with the host's question tool where it has one; otherwise ask in prose.

## Fix

Run test-fail-fix-reflect strictly:

1. Write a test reproducing the defect. Run it and confirm it fails. A change starts here instead with the new behavior's test, or with the existing tests where they cover it.
2. Implement the remedy. Run the test and confirm it passes.
3. Run the full test suite to check for regressions.
4. Reflect: why wasn't this caught earlier? Name the spec or process change that would have caught this kind of problem.

A quick fix implements directly, runs the directly related existing tests, and writes no new test and no reflect.

## Patch checks

The same patch checks as `onebuild` apply to everything landed here:

2. **Verify** the patch demonstrates its planned change: where test-coverable, its test fails before the patch and passes after. The full test suite must be green — the project must be clean for a patch to commit. Green is necessary but not sufficient: if the patch claims a live or external effect (a provider calls us, a platform capability enabled, a credential provisioned), verify by observing that real effect — a synthetic stand-in proves the handler, not the claim. This holds equally when the patch depends on anything the repository does not control, for example another tool's logs or an API's responses: verify against the real thing in this patch, and build fixtures from captured real samples. Judge against the planned claim, not a narrowed post-hoc claim. If the real effect cannot be observed as true (never attempted, inconclusive, or denied), stop before commit — missing proof is a block, not a skip.
3. **Pre-commit checks**:
   - Confirm the worktree contains only the intended patch scope.
   - Every changed line traces to the patch's stated invariant or to machinery that invariant requires (imports, type plumbing, test setup). A line that traces to neither belongs to another patch: move it out, or report it to the author before committing.
   - Stop for blocking problems or unspecified UI/interaction surfaced by a dependency.
   - A live/external step that comes back denied, unavailable, or not-authorized — or whose claimed effect cannot be observed — is a blocker even with a green suite. Report it to the author verbatim and stop: do not commit this patch, do not start later patches — that report is the deliverable. Don't route around it: no silent continue, no "pending"/"skipped" status, no marking the patch done, no synthetic proof. Blocked ≠ done; the author decides next.
   - For user-facing work: check against mature desktop software quality, treat library defaults as implementation details, verify new limits at the limit, map tests across affected workflows and failure paths, and document non-default product choices in the change spec.

## Working-tree delivery

Leave the tree uncommitted and propose a commit message instead. The message accounts for every changed file:

- one bullet per feature, not per file;
- product impact over mechanics;
- no file names and no test report, unless the author asked;
- a split across commits is listed by file;
- never stage or commit unless the author asks.
