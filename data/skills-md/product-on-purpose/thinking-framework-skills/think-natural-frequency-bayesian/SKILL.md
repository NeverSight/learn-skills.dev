---
name: think-natural-frequency-bayesian
description: Converts a conditional-probability or base-rate question into natural frequencies over a concrete population (for example 9 of 1000) to compute the correct posterior and expose base-rate neglect, and refuses to proceed without real input rates. Use when interpreting a test result, screening signal, or any "given a positive, what is the real probability" question.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.natural-frequency-bayesian
  family: reasoning-clarity
  evidence-tier: "S"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Natural-Frequency Bayesian Framing

People - including experts - reason badly about conditional probabilities stated as percentages, because they neglect the base rate. Re-expressing the same facts as natural frequencies over a concrete population makes the correct answer nearly visible: "Out of 1,000, 10 have it; 9 of those test positive; of the 990 without it, ~89 also test positive; so of ~98 positives, only 9 truly have it - about 9%." The format does the work by keeping the base rate in the counts. The output is a **natural-frequency breakdown**. Honest constraint: the base rate and hit rates must be real - the format makes correct reasoning tractable, it does not invent the inputs.

## When to Use

- Interpreting a test or screening result (medical, fraud, security, lead-scoring, A/B).
- Any "given a positive signal, what is the actual probability the thing is true?" question.
- Communicating risk to others so they do not over-read a positive.

## When NOT to Use

- When you do not have real input rates and would have to invent them.
- When there is no conditional-probability structure to the question.
- For general project forecasting (use reference-class forecasting).
- When a single point estimate is wanted and the base-rate structure is irrelevant.

## Instructions

When asked to reason about a conditional probability, follow these steps:

1. **State the question precisely.** What posterior is being asked - usually P(condition | positive signal). Distinguish it from P(positive | condition), which people confuse it with.
2. **Gather the real inputs.** The base rate, the true-positive (hit) rate, and the false-positive rate. If any is unknown, say so and stop or clearly flag the estimate as illustrative - do not fabricate numbers.
3. **Build a frequency tree over a concrete population.** Pick a round number (e.g., 1,000). Work out: how many have the condition; of those, how many test positive; of those without, how many also test positive.
4. **Compute the posterior** as true positives / all positives, and state it plainly.
5. **Name the wrong intuition it corrects.** State the answer most people give (usually near the hit rate) and why it is wrong (base-rate neglect).
6. **Emit the natural-frequency breakdown** per `references/TEMPLATE.md`.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the frequency tree, the posterior, and the plain-language meaning, not a bare percentage.

## Quality Checklist

Before finalizing, verify:

- [ ] The question distinguishes P(condition | positive) from P(positive | condition).
- [ ] The base rate, true-positive rate, and false-positive rate are real (or missing data is flagged, not invented).
- [ ] A frequency tree over a concrete population is shown.
- [ ] The posterior is computed as true positives / all positives.
- [ ] The common wrong intuition (base-rate neglect) is named.
- [ ] The output is the breakdown artifact, not a bare number.

## Evidence

Tier **S**. Presenting conditional-probability information as natural frequencies substantially improves Bayesian-inference accuracy - accuracy on these problems rises from roughly 10% to 50-90% with the same facts in frequency format (Gigerenzer & Hoffrage 1995; Sedlmeier & Gigerenzer 2001), replicated across populations including physicians. The format does not supply the inputs; real rates are required. Evidence is from human reasoners, transferred to AI use, not AI-validated. Full grading: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed breakdown.
