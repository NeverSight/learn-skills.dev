---
name: think-decision-option-review
description: Produces a criteria-weighted option matrix by comparing a set of options against weighted criteria, scoring each, surfacing the explicit tradeoffs, and recommending one while flagging where the scoring is soft. Use when choosing among several real options, or when a decision needs its tradeoffs made explicit rather than left to intuition.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.decision-option-review
  family: decision-and-option-evaluation
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Decision Option Review

When several real options compete, intuition compares them on shifting, unstated criteria that nobody can inspect. This skill makes the comparison explicit: list the options, define and weight the criteria that actually matter, score each option, surface the tradeoffs, and recommend. The output is a **criteria-weighted option matrix**. It is a lightweight multi-criteria review, not academic MCDA, and it deliberately shows the tradeoffs rather than hiding behind a single total: weighted scores can manufacture false precision, so soft scores are flagged and the recommendation states what would flip it.

## When to Use

- Choosing among several real, distinct options.
- Objectives conflict and the tradeoffs are currently implicit.
- The decision needs to be explained or defended to others.

## When NOT to Use

- Trivial or obvious choices, or one-way doors needing deeper analysis than a matrix.
- To generate options (use an ideation skill); this compares options that already exist.
- When the criteria genuinely cannot be articulated.
- As a way to make a single weighted total settle a close call (false precision).

## Instructions

When asked to review options, follow these steps:

1. **List the options** being compared (the real, distinct ones).
2. **Define the criteria** that actually matter for this decision, and weight them (high / medium / low is enough). State why each criterion is in.
3. **Score each option** against each criterion. Use a small scale and say what a high score means. Flag any score you are not confident in.
4. **Surface the tradeoffs.** For each leading option, state plainly what it gives up. Note factors that resist scoring rather than dropping them.
5. **Recommend** one option, with a confidence note and the conditions under which the recommendation would flip.
6. **Emit the matrix** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the matrix plus the tradeoffs and a recommendation, not prose and not a bare total.

## Quality Checklist

Before finalizing, verify:

- [ ] Criteria and weights are explicit, with a reason each is included.
- [ ] Soft or low-confidence scores are flagged, not presented as exact.
- [ ] The tradeoffs each leading option makes are stated.
- [ ] Factors that resist quantification are noted, not dropped.
- [ ] The recommendation states what would flip it.
- [ ] The output is the matrix artifact, not a single total treated as the answer.

## Evidence

Tier **P** (flagged). Structured multi-criteria comparison is a long-standing, government-endorsed decision aid (UK Government MCDA guidance), which stresses it should support judgment, not replace it. Making criteria and weights explicit improves transparency, but a weighted total does not produce a correct decision, and over-trusting the arithmetic (false precision) is a known failure. Evidence is transferred from human practice, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed option matrix.
