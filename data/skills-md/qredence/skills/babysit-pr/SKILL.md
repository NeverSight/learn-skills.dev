---
name: babysit-pr
description: Babysits a GitHub pull request by continuously polling CI checks, review comments, and mergeability state until the PR is ready to merge or closed. Diagnoses failures, retries flaky failures up to 3 times, auto-fixes branch-related issues, and stops only when user help is required. Use when asked to monitor a PR, watch CI, handle review comments, or track failures on an open PR.
---

# PR Babysitter

## Objective

Babysit a PR persistently until one of these terminal outcomes:

- PR is merged or closed.
- CI succeeded, no unaddressed review comments, not blocked on review approval, and mergeable.
- A situation requires user help (infra issues, exhausted flaky retries, permissions, or ambiguity).

Do not stop merely because a single snapshot returns `idle` while checks are still pending.

## Inputs

- No PR argument: infer from the current branch (`--pr auto`)
- PR number or PR URL

## Commands

```bash
# One-shot snapshot
python3 scripts/gh_pr_watch.py --pr auto --once

# Continuous watch (JSONL)
python3 scripts/gh_pr_watch.py --pr auto --watch

# Trigger flaky retry cycle
python3 scripts/gh_pr_watch.py --pr auto --retry-failed-now

# Explicit PR target
python3 scripts/gh_pr_watch.py --pr <number-or-url> --once
```

## Core Workflow

1. Start with `--watch` for monitoring requests; use `--once` only for one-shot diagnostics.
2. Inspect `actions` in the JSON response and act accordingly:
   - `diagnose_ci_failure` → inspect logs, classify as branch-related or flaky.
   - `process_review_comment` → address actionable feedback, commit and push.
   - `retry_failed_checks` → rerun flaky jobs (prioritize review fixes first).
3. After any push or rerun, immediately resume polling on the updated SHA.
4. Repeat until a stop condition is met.

For detailed workflow steps, CI classification, review handling, git safety rules, polling cadence, and output expectations, see `references/workflow.md`.

## Stop Conditions

Stop only when:
- PR merged or closed.
- PR is ready: CI green, no unaddressed reviews, mergeable, not blocked on approval.
- User intervention required and cannot safely proceed alone.

Keep polling when:
- Checks are still pending or running.
- CI is green but mergeability is unknown/pending.
- CI is green but blocked on review approval — continue on green-state cadence.

## Final Summary

Include: final PR SHA, CI status, mergeability, fixes pushed, flaky retry cycles used, remaining unresolved items.

## References

- Detailed workflow and patterns: `references/workflow.md`
- Heuristics and decision tree: `references/heuristics.md`
- GitHub CLI/API details: `references/github-api-notes.md`
