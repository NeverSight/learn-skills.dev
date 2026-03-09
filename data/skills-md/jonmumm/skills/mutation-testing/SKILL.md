---
name: mutation-testing
description: Run and interpret Stryker mutation testing; kill survivors to reach ≥95% score. Use when running mutation tests, setting up Stryker, interpreting survivors, or verifying test quality after TDD.
---

# Mutation Testing Quality Gate

Use Stryker Mutator to verify that tests actually catch breakage — not just that they pass. Often used after TDD (e.g. in Ralph’s quality gate).

## What It Does

Stryker modifies your source code (mutates it) and checks if your tests catch the change. If a mutation survives (tests still pass), there's a gap in your test coverage.

Examples of mutations:
- `> 0` → `>= 0` (boundary condition)
- `a + b` → `a - b` (arithmetic operator)
- `if (condition)` → `if (true)` (removed conditional)
- `return value` → `return ""` (string literal)
- `{ ...body }` → `{}` (removed block)

If your tests don't catch these, they're not testing real behavior.

## Setup (one-time per project)

See [references/setup.md](references/setup.md): install Stryker packages, add `stryker.config.mjs`, npm scripts (`test:mutate`, `test:mutate:incremental`), and `.gitignore` entries.

## The Quality Gate Workflow

Run **after all unit tests pass**:

1. **Run Stryker**: `npm run test:mutate:incremental` (first run 10–60 min; incremental 2–5 min).
2. **Read survivors**: Clear-text output shows file, line, and what was changed.
3. **Kill survivors** on files you touched: understand the mutation → write a targeted test that would fail with the mutation → re-run incremental.
4. **Repeat** until mutation score ≥ 95% on touched files. Use `thresholds.break: 90` in config to fail the build if you regress.

## Survivor table and tips

| Mutation | What It Means | How to Kill |
|----------|--------------|-------------|
| `> 0` → `>= 0` | No test with zero value | Add test with `amount = 0`, assert rejection |
| `a + b` → `a - b` | No test verifying arithmetic result | Assert exact computed values |
| `if (x)` → `if (true)` | Condition not tested as false | Add test where condition is false |
| `return value` → `return ""` | Return value not asserted | Assert the specific return value |
| `{ ...body }` → `{}` | Block removal not detected | Assert side effects of the block |
| `a.filter(fn)` → `a` | Filter not tested | Add test with mixed data, assert filtered result |
| `a === b` → `a !== b` | Only testing the happy path | Test both matching and non-matching cases |

- **Run incremental, not full**: After the first baseline, use `npm run test:mutate:incremental`. Much faster.
- **Focus on your changes**: Kill survivors only in code you touched.
- **NoCoverage / CompileError**: NoCoverage = add tests later; CompileError = no action.
- **Don't chase 100%**: 95% on covered code is excellent.
