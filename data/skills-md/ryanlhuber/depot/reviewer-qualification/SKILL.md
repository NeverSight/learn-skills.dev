---
name: reviewer-qualification
description: "Qualifies a reviewer, human or model, for one technical domain by running it on a seeded change with known defects and scoring the result against fixed thresholds. Use when deciding whether a reviewer can be trusted with the review role in a domain, or when a model version changed. Not for reviewing real changes."
disable-model-invocation: true
---

# Reviewer Qualification

## Purpose
Decide, from evidence, whether a candidate reviewer reliably finds real defects in one domain without inventing unsupported ones. Qualification is per domain and per version; it does not transfer.

## When to use
- Use when: a reviewer is about to receive a review role in a domain, a qualified reviewer's underlying model changed materially, or a new technical domain is introduced.
- Do not use when: reviewing an actual change (use a review skill) or when the question is how well someone builds.

## Inputs
- Required: the candidate reviewer, the domain, and the review skill the candidate will use.
- Optional: an existing seeded change for the domain (specification, diff, tests) with its private answer key, and prior qualification results.
- Assumptions: the answer key is never shown to a candidate; a candidate gets no hints beyond what a real review would receive.

## Process
1. Prepare a seeded change for the domain: a small real or sample change with a written specification and four real defects. One is a logic bug. One is an unmet acceptance criterion detectable only by reading the specification, not the code alone. One is an edge case or validation gap. One is a security or accessibility issue.
2. Add one harmless stylistic nit that must not be reported as a defect. Write a private answer key listing each seeded defect (file, line, description) and the nit.
3. Give the candidate the specification, diff, repository context, test results, and the review skill. Run each candidate once per seeded change.
4. Save each candidate's report as a file named for the candidate and date.
5. Score with the [scoring sheet](templates/scoring-sheet.md): real defects found of four, defects missed, unsupported findings (claims with no reproducible evidence), whether the report format was followed, quality of evidence, and whether severity was classified correctly. The human decides what counts as unsupported.
6. Apply the qualification rule and record the result with its date and the candidate's version.

## Rules and heuristics
- Required: a candidate qualifies when it finds at least three of the four defects, produces no unsupported finding, and follows the report format. Reporting the harmless nit as a defect counts as an unsupported finding.
- Required: a borderline result (three of four with exactly one unsupported finding, or two of four) is rerun once on a different seeded change. The candidate qualifies only if the rerun qualifies by the rule above; otherwise it does not qualify. Any other result is not qualified without a rerun.
- Required: qualification applies only to the tested domain and the tested version. Requalify when the version changes materially.
- Required: never lower the bar to fill a role. If too few candidates qualify for what a process requires, report the shortfall and stop.
- Required: the thresholds are screening criteria, not a guarantee of review quality.
- Recommended: reuse a seeded change only for candidates who have not seen its answer key; build a new one when a key may have leaked.

## Checks
- Every seeded defect is real, and the answer key was withheld.
- Each candidate was given the same inputs and no hints.
- The scoring sheet is complete and the decision follows the rule, including any rerun.
- The result records the domain, the candidate's version, and the date.

## Output
Return the completed scoring sheet for each candidate, the qualification decision with its basis, the qualified pool for the domain, and any shortfall or rerun needed. Use the [scoring sheet](templates/scoring-sheet.md).

## Completion criteria
- Each candidate has a recorded decision: qualified, not qualified, or rerun pending.
- The decision is traceable to the score and the rule.
- Limits are stated: one domain, one version, a screening measure.
