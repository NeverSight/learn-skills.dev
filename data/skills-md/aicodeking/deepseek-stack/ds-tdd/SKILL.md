---
name: ds-tdd
description: "Fix a bug by first writing a focused test that fails for the right reason, then making the smallest change that makes it pass. Use when the user asks for TDD or a regression test, when a bug has a cheap local test target, or for /ds-tdd."
---

# ds-tdd

Make the bug executable before touching production code, so the fix is proven, not claimed.

## Steps

1. Pin down the bug: expected behavior, actual behavior, the code path, and the smallest way to reproduce it.
2. Find the nearest existing test style for that code path. Use it. Do not build a new harness just for this.
3. Write the smallest test that would have caught the bug. It checks intended behavior, not the current implementation.
4. Run it. Show the output. It must fail, and fail for the bug, not for a typo or missing import. If not, fix the test first.
5. Make the smallest production change that gives the intended behavior without breaking nearby contracts.
6. Run the new test and the surrounding suite. Show the output.
7. If a clean test is impractical (heavy setup, brittle mocks, production-only state), use the closest runnable check instead: a script, a repro command or a log check. Say why you skipped the test.

## Stop when

- The new test failed before the fix and passes after it, both shown with output, and the surrounding suite passes.
- Or after three fix attempts the test still fails. Stop, report what you learned and run /ds-unstick.

## Rules

- Never edit a test to match a wrong implementation.
- Do not weaken existing assertions without a clear, stated reason.
- No test beats a bad test: one that mostly tests mocks, depends on timing, or would be deleted right after.
