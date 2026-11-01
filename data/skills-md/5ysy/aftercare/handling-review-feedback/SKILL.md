---
name: handling-review-feedback
description: process review feedback — from aftercare skills, other agents, or human reviewers — rigorously instead of blindly accepting or defensively rejecting it. use when review comments arrive and the next step is to decide, for each one, whether to act now, defer, or reject with reasoning.
---

# Handling Review Feedback

Announce at the start: "I'm using handling-review-feedback to triage each comment on its merits, not on its tone."

## Core idea

Technical review is not a performance ritual. Feedback is a claim about the code; the response is an evaluation of that claim. Every comment deserves the same discipline: restate it, classify it, verify the claim, then accept, defer, or reject with a reason. Agreement without verification is as sloppy as rejection without verification.

## Workflow

1. Collect all comments from the round of review in one place.
2. For each comment, restate it in your own words. If you cannot, you have not understood it yet — ask.
3. Classify it: is it about **correctness** (the code is wrong), **structure** (the code is hard to change), or **preference** (the reviewer would have written it differently)?
4. Verify the underlying claim against the code. Do not take correctness claims on faith; do not dismiss structure claims as preference.
5. Decide: accept now, defer with a tracked follow-up, or reject with reasoning.
6. Run the decisions through [`checklist.md`](./checklist.md) to confirm each one is justified, then cross-check against [`anti-patterns.md`](./anti-patterns.md) to catch performative-agreement and reflexive-defense failures.
7. If accepted, convert each into the smallest safe action — do not use "acceptance" as cover for a larger rewrite.

## Heuristics

- A comment you disagree with that you cannot refute is probably right.
- A comment you immediately agree with without reading the code is probably not processed.
- Correctness comments bind you; structure comments inform you; preference comments are optional.
- Unresolved structural blockers never merge silently; either act on them or write down why not.

## Do not

- implement every comment automatically to look agreeable
- reject comments because the current code passes tests (tests prove presence of behavior, not soundness of structure)
- merge with unresolved Critical or High feedback and no written justification
- escalate a preference comment into a structural rewrite to satisfy the reviewer

## Supporting files

- [`checklist.md`](./checklist.md) — per-comment processing steps distinguishing AI-generated from human feedback.
- [`anti-patterns.md`](./anti-patterns.md) — review-handling anti-patterns extending [`../../references/anti-patterns.md`](../../references/anti-patterns.md).

## Output

Summarize each comment with: (a) restatement, (b) classification, (c) verdict (accept now / defer / reject), (d) reasoning, (e) the concrete action or the tracked follow-up. Ship the summary alongside the change.
