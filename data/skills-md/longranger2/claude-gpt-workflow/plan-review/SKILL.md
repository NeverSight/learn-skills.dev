---
name: plan-review
description: Use when the user says "/plan-review", "plan review", or "PRD review" and provides a plan file path that needs critical review and iterative refinement with Codex.
---

# Plan Review Skill

## Purpose

When the user runs `/plan-review {plan-file-path}`, start the "adversarial plan iteration" workflow:
1. I (Claude Code) ask Codex to perform a critical review of the specified plan.
2. I read the review produced by Codex and evaluate whether its suggestions are sound.
3. I revise the plan based on valid suggestions and write changes back to the original plan file.
4. If the review status is `NEEDS_REVISION`, I automatically ask Codex to review again.
5. Repeat until consensus is reached as `MOSTLY_GOOD` or `APPROVED`.

## Usage

```
/plan-review plans/my-feature-plan.md
```

## Session Reuse

After each Codex invocation, extract `session_id=xxx` from the script output and save it as the session ID for the current task. In later Codex calls for the same task, pass `--session <id>` to reuse context so Codex remembers prior review history and can stay consistent across multiple rounds.

## My Workflow (Claude Code)

### Step 1: Determine the Review File

Derive the review file path from the plan file name:
- `plans/auth-refactor.md` → `reviews/auth-refactor-review.md`
- Rule: `reviews/{plan-file-name-without-.md}-review.md`

If the review file already exists, this is not the first round, so Codex must track the resolution status of issues from the previous round.

### Step 2: Ask Codex to Review the Plan

Use the `/codex` skill and give Codex the following instruction:

```
Read the contents of {plan-file-path} and review it critically as an independent third-party reviewer.

Requirements:
- Raise at least 10 concrete and actionable improvement points
- Each issue must include: issue description + exact location/reference in the plan + improvement suggestion
- Use severity levels: Critical > High > Medium > Low > Suggestion
- If {review-file-path} already exists, read it first and track the resolution status of previous issues in the new round

Analysis dimensions, choosing the relevant ones based on the plan type:
- Architectural soundness: overdesign vs underdesign, module boundaries, single responsibility
- Technology choices: rationale, alternatives, compatibility with the existing project stack
- Completeness: missing scenarios, overlooked edge cases, dependency and impact scope
- Feasibility: implementation complexity, performance risks, migration and compatibility concerns
- Engineering quality: whether it follows the Code Quality Hard Limits in `CLAUDE.md`
- User experience: interaction flow, error/loading states, i18n when relevant
- Security: authentication, authorization, data validation when relevant

Append the current review round to {review-file-path}, creating the file if it does not exist.
Separate rounds with `---` and append new rounds at the end of the file. Use this format:

---

## Round {N} — {YYYY-MM-DD}

### Overall Assessment
{2-3 sentence overall assessment}
**Rating**: {X}/10

### Previous Round Tracking (R2+ only)
| # | Issue | Status | Notes |
|---|-------|--------|-------|

### Issues
#### Issue 1 ({severity}): {title}
**Location**: {location in the plan}
{issue description}
**Suggestion**: {improvement suggestion}
... (at least 10 issues)

### Positive Aspects
- ...

### Summary
{Top 3 key issues}
**Consensus Status**: NEEDS_REVISION / MOSTLY_GOOD / APPROVED

Key principle: be a critical reviewer, not a yes-man. Every issue must be specific enough that someone knows how to revise the plan.
```

When the review file is created for the first time, add this header at the top:

```markdown
# Plan Review: {plan title}

**Plan File**: {plan-file-path}
**Reviewer**: Codex
```

### Step 3: Read the Review and Revise the Plan

After Codex finishes, I read the latest review round in the review file:

1. **Evaluate each issue** raised by Codex one by one.
2. **Adopt valid suggestions** and revise the plan file.
3. If rejecting an unreasonable suggestion, optionally note the reason briefly in the plan.
4. **Update the original plan file directly** instead of creating a new file.

### Step 4: Decide Whether to Continue Iterating

Use the `Consensus Status` provided by Codex:

| Status | My Action |
|--------|---------|
| `NEEDS_REVISION` | Revise the plan, then automatically ask Codex to review again and return to Step 2 |
| `MOSTLY_GOOD` | Revise the plan, then tell the user the plan is mostly mature and ask whether another review round is needed |
| `APPROVED` | Tell the user the plan has passed review and is ready for implementation |

### Step 5: Wrap Up

After the iteration is complete, report the following to the user:
- How many review rounds were completed
- Which major areas were improved
- The final plan file path
- The review log file path

## File Convention

- One review file per plan: `reviews/{topic}-review.md`
- `{topic}` is the plan file name without `.md`
- Append all rounds to the same file and separate them with `---`
- Example: `plans/auth-refactor.md` -> `reviews/auth-refactor-review.md`
