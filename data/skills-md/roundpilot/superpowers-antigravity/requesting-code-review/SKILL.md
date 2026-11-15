---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs** — run each on its own and copy the SHA it prints:
- `BASE_SHA`: `git rev-parse HEAD~1` — or: `git merge-base origin/main HEAD`
- `HEAD_SHA`: `git rev-parse HEAD`

**2. Dispatch code reviewer subagent:**

Use `invoke_subagent` with `Workspace: "inherit"` — reviewers only need read access. For a whole-branch review — after completing a major feature, before merge — use `TypeName: "final-reviewer"`; for one task's diff or a small range (when stuck, before refactoring, after fixing a complex bug), use `TypeName: "code-reviewer"`. Both are bundled with this plugin. Fill the base template in [code-reviewer.md](code-reviewer.md) and append its `## Whole-Branch and Ad-Hoc Reviews` block inside the Prompt. If the TypeName is rejected, retry once with the prefixed name (`superpowers:final-reviewer` or `superpowers:code-reviewer`). If that is rejected too, read the agent's file — `agents/<name>.md`, two directories above this skill — and dispatch `TypeName: "self"` with that file's body (everything after its frontmatter) ahead of the filled template. Say which fallback ran when you report the review.

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{REVIEW_FOCUS}` - The plan's Review Focus section, if the work has a plan with one (whole-branch block; omit when absent)

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)
- Rule on every "Declined to judge" line the reviewer returns — leave it out of scope or take it up as a finding — and say which, with the reason, when you report the review.
- To push back or ask for clarification, `send_message` to that reviewer — its conversation id is in the dispatch result — and it answers with the diff still in context. If it is no longer available, dispatch a fresh reviewer with your question and the same range.

Use GitHub-style alerts in review output for severity classification:
- `> [!CAUTION]` for Critical issues
- `> [!WARNING]` for Important issues
- `> [!NOTE]` for Minor observations

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

[Run `git log --oneline`: Task 1's commit is a7981ec]
[Run `git rev-parse HEAD`: 3df7661]

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: requesting-code-review/code-reviewer.md
