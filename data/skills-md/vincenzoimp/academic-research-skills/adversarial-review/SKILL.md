---
name: adversarial-review
description: Use when reviewing the survey, a contribution, or a paper draft as a severe but fair reviewer — claim audit, methodology critique, and venue-reviewer simulation before submission.
license: MIT
---

# Adversarial Review

Find the objections that would block acceptance before external reviewers
do. Review; never fix. Findings go to a report beside the artifact; the
artifact itself is never edited by this skill.

## Read First

- the artifact under review: `survey/survey.tex` + PDF, or a contribution
  README + report, or a manuscript + `framing.md` + `venue.md`
- `references/review-lanes.md`, `references/claim-audit.md`

## Procedure

1. Identify the target and the standard it must meet:
   - survey → coverage vs `sota/index.md`, grouping logic, fairness, and
     the quality of the gaps section
   - contribution → badge-checklist truthfulness, methodology (the
     develop-contribution methodology standard), claim–evidence match
   - paper → venue fit and reviewer simulation per `venue.md`, novelty,
     soundness, clarity
2. Read claim-first: contributions/claims, then the evidence offered.
3. Run the claim audit on every acceptance-critical claim per
   `references/claim-audit.md`: verify each against the cited synthesis,
   contribution output, or PDF.
4. Review through every lane in `references/review-lanes.md`; keep lane
   findings separate until the final synthesis.
5. Write the report to `reviews/<YYYY-MM-DD>-<scope>.md` beside the
   artifact (`survey/reviews/`, `contributions/<slug>/reviews/`,
   `papers/<slug>/reviews/` — create the folder on demand) with: executive
   summary and recommendation; strengths with evidence; weaknesses grouped
   by severity; the claim-audit table; questions the authors must answer;
   a prioritized revision roadmap.

## Criticism Standard

Every major criticism carries: exact claim or location, why it matters,
evidence, what would fix or weaken it, severity (fatal / major / moderate /
minor), and confidence. No performative harshness; no objection without
evidence; polish never excuses methodological weakness.

## Done When

- The report exists with all sections, every fatal/major finding is
  evidence-backed, and no lane finding was dropped during synthesis — if a
  finding is wrong, the report says why
