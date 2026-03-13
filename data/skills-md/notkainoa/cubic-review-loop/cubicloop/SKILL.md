---
name: cubicloop
description: >
  Iteratively improves local code changes by repeatedly running cubic CLI review,
  fixing actionable findings, and rerunning until no actionable issues remain (or
  an iteration cap is reached). Use when the user wants a local pre-flight quality
  loop before push/PR using cubic review on uncommitted changes, base-branch diffs,
  specific commits, or focused prompt-based checks.
---

# Cubicloop

Iteratively run `cubic review`, fix actionable issues, and rerun until the review is clean.

## Inputs

- Review target:
  - Current branch against `main`: `cubic review --base main`
  - Uncommitted changes: `cubic review`
  - Specific commit: `cubic review --commit <ref>`
- Custom focus (optional): `cubic review --prompt "<instructions>"`
- Max iterations (optional): default `5`

## Workflow

### 1. Preflight

1. Confirm `cubic` is available and authenticated.
2. Confirm current workspace is a git repo.
3. If the user did not specify a review target, ask a simple choice question:

   Do you want to:
   - review the current branch against `main`
   - review uncommitted changes
   - review a specific commit
   - focus on a specific area or problem

4. Pick a single review mode based on the user's answer.

Use exactly one of:
- `--base main` or another explicit base branch
- uncommitted changes
- `--commit <ref>`
- `--prompt "<instructions>"`

`--base`, `--commit`, and `--prompt` are mutually exclusive. See [CLI JSON reference](references/cli-json.md).

### 2. Iteration Loop (Max 5)

For iteration `N` from 1 to max:

1. Run review and store JSON output:
   ```bash
   mkdir -p .cubicloop
   cubic review --json > ".cubicloop/iteration-${N}.json"
   ```
   If using a mode, include it before `--json` (for example `cubic review --base main --json`).
2. Parse issue totals and priority counts directly from the JSON output.
   `jq` is optional; use it only if available. See [CLI JSON reference](references/cli-json.md).
3. Exit early if issue count is `0`.
4. Fix actionable issues in priority order: `P0`, `P1`, then the rest.
5. For each issue:
   - Read the file and line context.
   - Decide if actionable or likely false positive.
   - Apply a fix for actionable items.
   - Record non-actionable items in the report with rationale.
6. Run relevant validation (tests/lint/typecheck) when available.
7. Continue to next iteration.

### 3. Exit Conditions

Stop when either condition is true:
- No remaining actionable issues in Cubic output.
- Max iterations reached.

### 4. Report

After exiting, summarize:

| Field | Value |
|-------|-------|
| Iterations | N |
| Target mode | uncommitted / base / commit / prompt |
| Issues fixed | N |
| Remaining issues | N |
| Highest remaining priority | P0/P1/P2/P3 or none |

If max iterations are reached, include a short list of remaining issues with file and line.

## Output Format

If fully resolved:

```text
Cubicloop complete.
  Iterations:    2
  Target:        --base main
  Fixed:         6 issues
  Remaining:     0
```

If not fully resolved:

```text
Cubicloop stopped after 5 iterations.
  Target:        uncommitted
  Fixed:         11 issues
  Remaining:     2
  Highest left:  P1

Remaining issues:
  - src/auth.ts:45 [P1] SQL injection vulnerability in user lookup
  - src/db.ts:112 [P2] Missing index on user_id column
```
