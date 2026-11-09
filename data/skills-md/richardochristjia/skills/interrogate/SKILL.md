---
name: interrogate
description: "Has four agents review the same code change independently, each from its own angle (correctness, security, structure, tests), then merges their findings and sorts each into act on, consider, noted, or dismissed. Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", \"tear this apart\", or as the autopilot's review step."
---

# Interrogate

Spawn four reviewers on the same model to adversarially review code changes. Each owns one angle, so they don't all find the same things. A problem raised from two angles independently is the strongest signal. Spawn all four by default, however small the diff: a small diff is cheap to review, and the angles exist so no single reader decides what's worth checking. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

**One-angle mode.** When the caller names a single angle — a small, everyday change where one careful reader is enough — spawn only that reviewer and skip the synthesis across angles. Say in the report that the review was single-angle, and which angle it was.

**The context pack.** When `.plans/<task>/context-pack.md` exists, the reviewers read that instead of re-deriving the repository. It holds the diff, the touched files, the API contracts and the test entry points, each with a `file:line` anchor. A reviewer may open a file when the pack points at it, but must not go hunting: the pack exists so the review costs a fraction of a cold start. If there is no pack, build the diff as in Step 1 and say the pack was missing.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

Prefer the context pack over the diff when it exists: read `.plans/<task>/context-pack.md` and hand that to the reviewers as the code under review.

**Call budget.** A reviewer gets at most 8 tool calls to explore. If it needs more, it must say what it could not check, rather than spend the budget. A reviewer that greps the whole repository has failed the review, not the diff.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, take it from the plan, the PR description, or the commits, and say which. Don't stop to ask.

## Step 3, Spawn Reviewers

Launch the reviewers in a single message with the `Agent` tool, each with one angle:

| Subagent | Angle | Rubric sections it goes deepest on |
|----------|-------|------------------------------------|
| Reviewer A | Correctness | Correctness; Root Causes vs. Symptoms |
| Reviewer B | Security | Security |
| Reviewer C | Structure | Structural Integrity; Complexity Budget; the code-quality lens |
| Reviewer D | Tests | Verification |

In one-angle mode, launch only the reviewer for that angle.

**One reviewer per turn.** The harness takes one subagent call per turn; calls issued in a burst are rejected. Launch the reviewers one per turn, correctness first, and only spend a fan-out token if the harness grants one.

All reviewers run on the model the caller names, or `sonnet` by default: a review is reading and reasoning over a prepared pack, not deciding what to build. Each gets `subagent_type: "general-purpose"` and is told to read only: no edits. If the `Agent` tool rejects the model, use the closest valid one from the error message and say so. Don't block the review on it.

Each reviewer is told to read the context pack first, to stay inside the 8-call budget, and to cite `file:line` for every finding.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with its angle, the stated intent, the context pack or the diff, the rubric from `references/rubric.md`, and the code-quality lens from `references/code-quality-review.md`.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that describe the same issue differently, and note which reviewers raised each one. Findings two or more reviewers raised independently are the highest signal. Read a lone reviewer's finding, but weight it accordingly. Note disagreements. If one reviewer flags something and another explicitly says the opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with the reviewer(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [angle], [N findings] (one bullet per reviewer)

### Act On
[Each: description, which reviewers raised it, why it matters.]

### Consider
[Each: description, which reviewers raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where reviewers agreed and diverged, and what that pattern tells us.]
