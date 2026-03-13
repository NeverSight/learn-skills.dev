---
name: bugfix
description: "Use when given a bug report, failing test, stack trace, or CI failure that needs diagnosis and repair. Autonomously diagnoses root cause, implements minimal fix, verifies correctness, and commits. Keywords: fix bug, failing test, stack trace, CI failure, debug error, broken test."
---

# Bugfix

Autonomous end-to-end bug fix: diagnose from evidence, find root cause, minimal fix, verify, commit.

## NEVER

- Never ask the user for more information unless the bug description is completely ambiguous — use tools to find it.
- Never refactor unrelated code while fixing a bug — scope creep breaks regression isolation.
- Never fix other bugs you notice while fixing the target — create a new task instead.
- Never `git add -A` — stage only the files you changed.
- Never skip running the full workspace test suite after a fix — targeted test passing doesn't mean no regression.
- Never commit until typecheck passes on the affected workspace.

## Root Cause Classification (decide before writing any code)

| Type | Signal | Fix approach |
|------|--------|--------------|
| Code bug | Logic error, wrong query, bad comparison | Fix implementation |
| Test bug | Expectation contradicts documented contract | Fix the test — explain why it was wrong |
| Mock wiring | `mockReset: true` pattern not followed, stale mock state | Use correct mock pattern from CLAUDE.md |
| Type error | TypeScript compilation failure | Fix types, not tests |
| Import error | Wrong package path, missing export | Fix import resolution |

**If it's a mock wiring issue:** read the mock patterns in CLAUDE.md before writing anything — there are three distinct patterns (forwarding, object-bag, counter-based sequencing).

## Evidence-First Thinking

Collect before hypothesizing:
1. Run the failing test — see the exact error output, not just the description
2. Read the failing test — understand what it expects
3. Read the source under test
4. `git log --oneline -10 -- <file>` — was this recently changed?
5. For runtime errors: check logs, route/plugin/service code

State hypothesis explicitly before writing code: "The test fails because X, caused by Y."

## Abort Conditions (stop and ask user)

- Bug is in security-sensitive area (auth, RBAC, IDOR) — confirm fix approach first
- Fix requires changing more than 5 files — may be an architectural issue
- Root cause requires changing the mock strategy for an entire test suite

## Scripts

```bash
bash scripts/collect-bugfix-context.sh apps/api/src/tests/routes/auth.test.ts
bash scripts/run-targeted-test.sh apps/api/src/tests/routes/auth.test.ts
bash scripts/run-targeted-test.sh apps/api/src/tests/routes/auth.test.ts "returns 500"
```

## Verification Sequence

1. Run the specific failing test — must pass
2. Run the full workspace suite — no new failures
3. Run typecheck on the affected workspace (`npx tsc --noEmit`)
4. `git diff --name-only` — verify every changed file relates to the bug; revert anything that doesn't

## Commit Format

```
fix(scope): what was broken and how it was fixed

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## Arguments

`$ARGUMENTS`: Error message, failing test path, CI log URL, or reproduction steps. If empty, ask for the error or failing test name.
