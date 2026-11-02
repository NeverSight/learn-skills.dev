---
name: bug-repro-test-first
description: Start bug work by proving the reported bug with a failing regression test before attempting a fix. Use when the user reports a bug, asks to fix a bug, or describes a regression, failing behavior, or reproduction case with a plausible test surface.
created: 2026-05-14
---

# Bug Repro Test First

Use this when the user reports a bug or asks for a bug fix.

## Source

Read `references/tangming2005-test-first-bug-report.md` if you need the source note behind this workflow.

## Rule

Do not start by fixing the code.

First write or adapt a test that fails for the reported bug. The test is the definition of the bug.

If there is no useful test surface, create the narrowest reproducible check available instead, then state why a regression test was not practical before fixing production code.

## Workflow

1. Reproduce or inspect the failure enough to choose the narrowest useful test.
2. Add a failing test that captures the bug, preferably near existing coverage for the same behavior.
3. Run that test and confirm it fails for the expected reason.
4. Only then change production code.
5. Run the same test and confirm it passes.
6. Run the smallest relevant surrounding test/check slice.

## Parallel Fixes

If the user explicitly asks for subagents or the active tool policy permits delegation for this task, spawn fix workers only after the failing test exists. Give each worker the failing test command and a disjoint write scope.

If delegation is not available or not appropriate, fix locally after proving the failing test.

## Done

- The bug has a regression test.
- The regression test, or documented fallback check, failed before the fix.
- The same test or check passes after the fix.
- The final report names the test file and exact command run.
