---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Dispatch superpowers-bd:code-reviewer subagent to catch issues before they cascade.

## Quick Access

For ad-hoc review outside SDD: /superpowers-bd:cr — interactive flow supporting local changes and GitHub PRs. Supports single or multi-reviewer (N independent reviewers, aggregated, max 10).

## When to Request Review

**Mandatory:** After each task in SDD, after completing major feature, before merge to main.

**Optional:** When stuck, before refactoring, after fixing complex bug.

## How to Request

1. Get git SHAs: run `git rev-parse HEAD~1` for BASE_SHA and `git rev-parse HEAD` for HEAD_SHA
2. Dispatch code-reviewer subagent using template at `code-reviewer.md`
   - `{PLAN_OR_REQUIREMENTS}` -- plan file path, bd show output, or spec
   - `{BASE_SHA}` / `{HEAD_SHA}` -- commit range
3. Act on feedback: fix Critical immediately, fix Important before proceeding, note Minor for later, push back if wrong

## Multi-Review Mode

For critical changes, dispatch N=3 independent reviews and aggregate per `superpowers-bd:multi-review-aggregation` (118% recall improvement per SWR-Bench).

**When:** Changes >200 lines, security-sensitive, pre-merge to main, complex refactoring.

**How:** 3 independent code-reviewer subagents with `run_in_background: true`, each with `"You are Reviewer {i} of 3. Review independently."` Single review is default for ad-hoc; multi-review is automatic in SDD for max-20x and max-5x tiers.

## Example

```
git log --oneline -10   # find the commit for Task 1, note the SHA
BASE_SHA=<sha-from-above>
HEAD_SHA=<from git rev-parse HEAD>
[Dispatch superpowers-bd:code-reviewer with plan context + SHAs]
[Subagent returns: 4/4 requirements mapped, Important: missing progress indicators]
[Fix -> Continue to next task]
```

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:** Push back with technical reasoning, show code/tests, request clarification.

See template at: requesting-code-review/code-reviewer.md

<!-- compressed: 2026-02-11, original: 449 words, compressed: 272 words -->
