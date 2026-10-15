---
name: detect-useless-tests
description: Find useless tests within one testing level (unit, e2e, manual) and list them by area, file, and line for review. Use when asked "which tests can we delete?", "find useless tests", or "what in our suite is not worth keeping?".
---

# Detect Useless Manual Tests

Go through tests of the same level (unit, e2e, manual) and detect useless ones.
User must provide exact locations of tests to check to identify the level of tests in pyramid.
Every test has tradeoffs in execution speed, conditions checked, and coupling to implementation details — judge tests against others of the same level only.

Judge each test primarily by its value to an end-user business flow.
Your top priority for interest are tests that are fragile to changes, that rely on time consumed heavy operations: db, browser, etc.

## Treat as likely useless

Flag tests that primarily cover:

- Internal observability, tracing, logging, metrics, or diagnostic structure.
- Developer-only switches, escape hatches, debug modes, build paths, or release internals.
- Cosmetic UI details such as wording, colors, shimmer, centering, labels, icons, breakpoints, or transient status text.
- Implementation workarounds rather than stable public behavior.
- Conditions with little or no impact on a customer workflow.
- Every variation of the same error, shortcut, platform, state transition, or entry point.
- Behavior already exercised by another test.
- Setup persistence or state-retention details that only save minor user effort.
- Expensive external-service, browser, installation, restart, CI, release, or multi-platform flows with weak business value.
- Regressions tied to an old implementation rather than the current public contract.
- Assertions that cannot meaningfully fail or whose expected result is vague.
- Check exact success/error message text instead of success/error behavior
- Implementation details not exposed via public API and never used outside the module scope.

A test can be technically valid and still be useless. Do not preserve a test merely because:

- it once caught a regression;
- it has assertions;
- it covers a distinct code path;
- no other test is an exact duplicate.

Exception: keep tests whose title, tag, or comment names a defect. A ticket or fix commit found in history doesn't count.

## Preserve only when justified

Keep a test only when it protects at least one of these:

- A critical end-user business flow.
- Data loss, security, permissions, billing, or irreversible actions.
- A stable public API or documented product contract.
- A defect explicitly identified in the test by an issue/defect reference or clearly described failure with material user impact.

A sentence such as “this used to happen” is not enough by itself.

When a defect requires protection, keep the smallest regression scenario possible. Merge permutations instead of preserving every trigger.

## Review method

1. Read the complete contents of every file in provided tests dir.
2. Review the explicit test cases—not just filenames, titles, priorities, or metadata.
3. Compare intent, business outcome, setup cost, assertions, and overlap.
4. Prefer removing whole suites when their subject is not appropriate for business-level testing.
5. For repetitive tests, select one canonical scenario and recommend merging or removing the others.

## Output

Return only cleanup candidates, grouped by area and file.
For rich UI output render output as table, otherwise (TUI) render as bullet list

Recommendations:
- `Remove`
- `Merge`
- `Simplify`
- `Move to lower-level automation`

Rules:
- Reference every file by relative path.
- Use one row per test.
- Name the exact test title.
- State the business-value problem directly.
- For duplicates, name the test that should remain.
- Do not list tests that should simply be kept.
- End with totals only: reviewed, remove, merge, simplify, move.
- Do not edit tests without approval.

Example as bullet points:

* path/to/test/file1:
  - test name 1 <- [action] explain why it is useless
  - test name 2 <- [action] explain why it is useless

* path/to/test/file2:
  - test name 3 <- [action] explain why it is useless
  - test name 4 <- [action] explain why it is useless

Example as table:

| File | Test | Action | Why it is useless |
