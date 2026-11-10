---
name: developing-test-first
description: Drives code changes test-first; a focused test must fail for the intended reason before any production edit, then the smallest change makes it pass. Use before writing any production code for a new app, project, feature, endpoint, behavior change, or bug fix, including greenfield work in an empty repository.
metadata:
  opencode/autoinvoke: true
---

# Developing Test-First

Write a failing executable check before changing production code, then make the smallest change that satisfies it.

## Gate: before the first production edit

A task listing Change before Tests describes deliverables, not work order. Even with a specified design, write each listed test first, see it fail, then implement.

Before any `edit`, `write`, or `patch` to a non-test file, confirm that a focused check has failed in this session for the intended reason, covering the behavior that edit changes. If none has, stop and complete Red first.

Exempt preparation, such as a dependency bump or a configuration-only edit, may land before red, but the first behavior-changing edit after it must still pass the gate.

## Red

1. Choose one externally meaningful behavior, boundary, invariant, transition, or regression.
2. Follow the repository's test conventions: location, naming, framework, and helpers.
3. Add the smallest test that expresses the expected public behavior.
4. Run the focused check and confirm it fails for the intended reason. Syntax errors, missing dependencies, and unrelated failures do not establish red.
5. Note the test name and the failure message for the final report.

For a service needed by the check, start it with `shell` and `background: true`, writing its output to a log file, rather than a detached `nohup` or `&` command. For browser-visible behavior, use the `browser` namespace through `execute` when it is available to establish the failing interaction when an automated test is not the right contract.

### OpenSpec scenarios

An OpenSpec change is active when `openspec list --json` reports a non-null `root` and the current work implements one of the listed changes: the change the user or the `openspec-apply-change` skill named, otherwise the only listed change. If several are listed and the work does not show which one it implements, ask. Without the CLI, a root, or a matching change, skip this section. Find the artifacts with `openspec status --change <name> --json` (`changeRoot`, `artifactPaths`) and open them with `read`.

For an active change, the delta specs define the behaviors for Red. Each `#### Scenario:` with its WHEN and THEN lines becomes one failing test, named after the scenario and written before the `tasks.md` item that implements it. A scenario that cannot be automated gets the validation described under Practical exceptions. When the code shows that a scenario is wrong or missing, correct the delta spec first, then write its test, so the specs and tests do not drift apart.

## Green

1. Make the smallest sufficient production change.
2. For a cross-file symbol change, find every reference with `grep`, update them together, and confirm with the project's type checker or compiler.
3. Run the focused check until it passes.
4. Run broader checks proportional to regression risk.
5. Smoke-test the changed path through the real entry point.

## Refactor

Refactor only while checks remain green. Use the repository's codemod tooling for structural rewrites that would be unsafe as text replacement, and review its diff before keeping it.

Then return to Red for the next behavior until every intended behavior has a passing test.

Tests must be deterministic, isolated, and resistant to implementation-only changes. Prefer real collaborators when cheap and reliable; use fakes or mocks only at slow, unstable, destructive, or external boundaries. Do not add production APIs solely for tests.

## Review

After the Green and Refactor steps, load the `reviewing-local-changes` skill when the change carries meaningful compatibility, security, data-integrity, or operational risk. Keep review optional for small, low-risk changes.

## Practical exceptions

Strict test-first may add little value for documentation, generated artifacts, configuration-only edits, exploratory spikes, UI-only visual changes, or environments without a usable harness. Decide an exception before the first production edit; implementing first and then finding the behavior hard to test does not qualify. Proceed without asking when the exception is clear and record the executable, browser, or artifact validation used instead. For hard-to-isolate legacy code, add the narrowest characterization or integration check that exposes the regression.

Do not delete correct pre-existing work because its tests were written later. Improve its evidence from the current state.

## Report red evidence

The final report names each test observed failing before its production change and the failure reason it showed, and names the substitute validation for each exception. A test first run after the production change is not red evidence: to recover, revert only the production change temporarily (for example `git stash push -- <production paths>`), observe the failure, restore it, and report that order. Load the `verifying-before-completion` skill before claiming the behavior works or the regression is covered.
