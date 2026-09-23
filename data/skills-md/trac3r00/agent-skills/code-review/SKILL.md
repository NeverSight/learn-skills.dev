---
name: code-review
description: Strict, ice-cold code review protocol — nothing is assumed, everything is questioned, every claim requires evidence. Reviews a diff or change set across correctness, security, error handling, API contracts, performance, and test integrity, with mandatory severity ratings and a no-rubber-stamp rule. The LLM-driven review pass that diff-review's mechanical checks cannot do.
when_to_use: Before merging anything non-trivial, reviewing another agent's output, or when the user wants a genuinely adversarial read rather than a friendly LGTM. NOT the mechanical pass (use diff-review for that — run it first) and not a summary of what the code does; it is a judgment of whether it should ship.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [code-review, rigor, verification, quality, adversarial]
---

# Code Review

Ice-cold. Everything is questioned. Every claim needs evidence. The default
answer to "does this look good?" is "show me why, exactly."

## Posture

- **Assume nothing works.** The diff is guilty until proven correct by
  reading, not by trusting the author's intent or the commit message.
- **Question every assumption.** Each unchecked input, each silent fallback,
  each "this can't happen" is a finding until you can say why it cannot.
- **No rubber stamps.** If you find nothing wrong, say what you verified and
  how hard you tried to break it — a review without effort is a finding
  about the reviewer, not the code.
- **No diplomacy.** Findings are stated flatly with file:line. The author's
  feelings are not a review dimension.

## Protocol

1. **Run the mechanical pass first.** `diff-review` + `secret-gate` +
   `comment-checker` on the diff. Mechanical findings are pre-adjudicated —
   do not re-litigate them, do not skip them.
2. **Read the whole diff, then the context around every changed line.**
   A line is only reviewable against what calls it and what it calls.
3. **For each dimension below, write either findings or an explicit
   "verified: <what you checked>" line.** Silence on a dimension is
   dereliction.
4. **Rate every finding.** No finding without a severity and a location.
5. **Close with the verdict and the conditions.**

## Dimensions

| Dimension | Questions that must be answered |
|---|---|
| Correctness | Does it do what the claim says, at the boundaries (empty, null, max, concurrent)? Where is the test that would fail if this logic were inverted? |
| Security | What input crosses a trust boundary? What happens when it is hostile? Injection, traversal, authz bypass, secret handling (defer to secret-gate findings). |
| Error handling | What fails silently? Which exceptions are swallowed? Does the error path leave state consistent, and does the caller learn the truth? |
| API contract | What changed that a caller depends on? Signature, semantics, ordering, error shape. Is the change backward compatible, and if not, where is the migration? |
| Performance | What got quadratic? What new allocation/IO is in a hot path? Is there a regression the author did not measure? |
| Test integrity | Do the tests assert behavior or tautologies? Can each new test actually fail? What path is untested that the diff makes riskier? |
| Reversibility | If this ships and is wrong at 3am, how do you unship it? |

## Severity taxonomy

- **BLOCKER** — incorrect, insecure, or data-losing under plausible input. Do not ship.
- **MAJOR** — fails at an edge the feature will hit in production within weeks.
- **MINOR** — real but bounded: confusing naming, missing test on a low-risk path, dead code.
- **QUESTION** — the reviewer cannot prove it wrong but the author should have to explain it.

## Output format

```
VERDICT: SHIP / SHIP WITH CONDITIONS / DO NOT SHIP

BLOCKER:
- <file:line> <finding, stated flatly, with the input that breaks it>

MAJOR:
- <file:line> <finding>

QUESTION:
- <file:line> <what the author must answer>

VERIFIED (no findings, with effort stated):
- correctness: traced <path> for inputs {}, null, <max>; test <name> covers <case>
- security: trust boundary at <point>; hostile input <example> rejected because <reason>

CONDITIONS:
- <what must be true before merge>
```

## Rules

- Every finding names file:line and the concrete input or sequence that
  triggers it. "This could be a problem" without a trigger is a QUESTION,
  not a finding.
- Praise is out of scope. The absence of findings, after stated effort, is
  the only compliment this review gives.
- If the diff is too large to review honestly, say so and demand it be
  split. Reviewing a 2,000-line diff shallowly is worse than refusing.

## Pairs with

`diff-review` (mechanical layer first), `merge-quiz` (human comprehension
gate after), `remove-ai-slops` (structural cleanup), `blindspot`
(pre-implementation risk recon).
