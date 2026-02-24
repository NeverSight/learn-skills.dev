---
name: refining
description: Refines code changes for better reviewability. Validates change cohesion (no mixed concerns), generates clear commit messages, creates PR/MR with reviewer-focused descriptions. Use when committing, reviewing, creating PR/MR, or mentions "commit", "review", "PR", "MR", "pull request", "merge request", "refine", "提交", "审查".
---

# Refining

Refine code changes to make them easy to review.

## Philosophy

### Why Refine?

Refining exists because **reviewers are humans with limited attention**.

The core question isn't "what checks should I run?" but "would I want to review this?"

```
The Reviewer's Reality:
├── Context loading takes mental effort
├── Large changes exhaust attention
├── Mixed concerns require mental switching
└── Unclear changes create uncertainty
```

### The Reviewer's Burden

Every code review requires:
- **Context loading** - Understanding what the change is about
- **Verification** - Checking if it's correct
- **Risk assessment** - What could this break?

Small, focused changes make this tractable. Large, mixed changes make it exhausting.

### Cohesion Over Size

A 500-line focused change is often easier to review than a 200-line mixed change.

Why?
- Focused changes have one mental model
- Mixed changes require context switching for each concern
- Each concern should be independently verifiable

The "lines changed" heuristic is about cognitive load, not absolute limits. Ask: **Could a reviewer hold this entire change in their head?**

### The Refining Mindset

Before committing or creating a PR, ask:
1. Would I want to review this?
2. Can I explain this in one sentence?
3. If this breaks, is the blast radius obvious?

If yes to all → proceed.
If no → refine further.

## Core Concepts

### Reviewability Factors

| Factor | What it measures | Why it matters |
|--------|------------------|----------------|
| **Cohesion** | Single purpose? | Mental model simplicity |
| **Size** | Cognitive load | Reviewer attention span |
| **Clarity** | Is intent obvious? | Time to understand |
| **Noise** | Distractions present? | Focus degradation |

These aren't gates to pass. They're lenses to evaluate through.

### When to Split

Not "must split" - but "consider splitting":

- Feature + refactor → Refactor can be reviewed independently
- Bug fix + new feature → Fix is urgent, feature can wait
- Multiple unrelated changes → Each deserves its own commit

The question: Would reviewing these separately produce better feedback?

### Noise Detection

Noise makes reviewers work harder without adding value:

- `console.log`, `print`, `debugger` → Should these be here?
- `TODO`/`FIXME` in new code → Is this intentional?
- Commented-out code → Dead code or notes?

Note these to the user. Let them decide if intentional.

## Three Modes

### Commit

Validate staged changes, create commit.

```
1. Check staged:     git diff --cached --stat
2. Assess:           Cohesion? Size? Noise?
3. Generate message: Conventional Commits format
4. Commit:           git commit -m "type(scope): description"
```

**Never push** unless explicitly requested.

### Review

Assess a PR/MR or branch comparison.

```
1. Identify target:  PR URL, branch, or current changes
2. Quick assessment: Cohesion, size, obvious issues
3. Detailed review:  Focus on what linters miss
4. Report:           Severity-based (🔴 Critical, 🟡 Important, 🔵 Suggestion)
```

Focus your attention where it matters most. Skip what automated tools catch.

See [reference/review-strategies.md](reference/review-strategies.md) for project-specific approaches.

### Create PR/MR

Generate reviewer-focused description.

```
1. Gather changes:   git log --oneline main..HEAD
2. Assess:           Is this PR-ready?
3. Generate:         Title + description + context
4. Create:           gh pr create / glab mr create
```

**Description structure:**
```markdown
## Summary
[What and why in 1-2 sentences]

## Changes
[Key changes as bullet points]

## Testing
[How to verify this works]

## Reviewer Notes
[What to focus on, known risks, trade-offs]
```

See [reference/description-guide.md](reference/description-guide.md) for examples.

## Understanding, Not Rules

Instead of memorizing thresholds, understand the underlying tensions:

| Tension | Resolution |
|---------|------------|
| Speed vs Quality | Quick changes need less refinement. Critical paths need more. |
| Completeness vs Focus | Better to have multiple focused PRs than one sprawling one. |
| Description Detail vs Reader Time | Enough to understand, not encyclopedic. |
| Stopping Early vs Proceeding | When in doubt, ask. User decides. |

### On Line Counts

"400 lines" isn't a magic number. It's a heuristic for "about the limit of focused review."

- Simple rename across many files? 1000 lines might be fine.
- Complex algorithm change? 100 lines needs careful review.

**Match review depth to change complexity, not line count.**

## Reference

Load these **as needed**, not upfront:

- [reference/reviewability.md](reference/reviewability.md) - Detailed criteria
- [reference/description-guide.md](reference/description-guide.md) - PR/MR examples
- [reference/review-strategies.md](reference/review-strategies.md) - Approaches by context
- [reference/review-checklist.md](reference/review-checklist.md) - Language-specific checks
- [reference/impact-analysis.md](reference/impact-analysis.md) - Blast radius techniques

## The Goal

The goal isn't to follow a checklist. It's to create changes that **reviewers can understand quickly and review confidently**.

Reviewability is empathy. Put yourself in the reviewer's shoes.
