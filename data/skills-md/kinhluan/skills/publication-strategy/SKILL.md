---
name: publication-strategy
description: Select a legitimate publication venue, verify current submission requirements, plan a submission, write a rebuttal, and manage revision or resubmission. Use for journal/conference selection, deadline planning, peer-review responses, camera-ready preparation, or publication-risk checks.
metadata:
  tags: ["research", "publication", "venue-selection", "submission", "rebuttal", "revision"]
---

# Publication Strategy

Match the paper to its audience and contribution, then verify every time-sensitive fact on official sources. Deadlines, tracks, page limits, review models, fees, indexing, ethics requirements, and policies change; never rely on a static venue table or remembered acceptance rate.

## Venue Selection

1. Summarize the paper's contribution type, maturity, evidence, audience, and constraints.
2. Build a candidate set from papers the target audience actually reads and cites.
3. For each candidate, open the official current call for papers or author instructions and record:
   - scope and track;
   - submission deadline with time zone;
   - page/word and supplementary limits;
   - anonymous/open-review policy;
   - prior-publication, preprint, dual-submission, and artifact rules;
   - required ethics, data, code, AI-use, or conflict disclosures;
   - fees and waiver process;
   - expected review/publication timeline;
   - official indexing evidence if indexing matters.
4. Check publisher identity and editorial board. Use recognized anti-predatory guidance; do not treat an unsolicited email or claimed metric as proof of legitimacy.
5. Rank fit, readiness, timing, policy compatibility, and cost separately. Explain uncertainty.

Do not compare CCF, CORE, quartiles, impact factors, or acceptance rates as if they were one ordinal scale. Historical rates may provide context only when officially published and defined for the same track/year.

## Submission Plan

Create a reverse schedule from the verified deadline:

- internal scientific review;
- missing experiments and analysis freeze;
- authorship/contribution agreement;
- anonymization and artifact review;
- format/policy compliance;
- final author approval;
- submission verification and receipt.

Never submit, agree to terms, or add/remove authors without explicit user authority.

## Rebuttal

1. Extract each reviewer claim and classify it as factual error, clarity issue, missing evidence, scope disagreement, or valid limitation.
2. Prioritize concerns that could change the decision.
3. Answer with evidence already in the paper or analyses permitted by the venue.
4. State exactly what will change. Do not promise experiments that cannot be completed or that policy forbids.
5. Remain factual and respectful; quote minimally and preserve reviewer identifiers.

```markdown
**Concern [R2.3]:** [neutral paraphrase]
**Response:** [direct answer and evidence]
**Revision:** [specific section/table change]
**Limitation:** [remaining boundary, if any]
```

## Revision or Resubmission

Maintain a matrix with reviewer, concern, validity, action, owner, evidence, and due date. On rejection, improve the paper before selecting another venue. Recheck the next venue's policies and tailor scope and format; do not assume a familiar annual deadline pattern.

## Output

```markdown
## Publication Plan — [paper]

**Search/verification date:** [date]
**Recommended venue/track:** [name]
**Fit:** [audience and contribution match]

| Criterion | Official evidence | Assessment | Risk |
|---|---|---|---|

**Alternatives:** [tradeoffs]
**Verified deadline:** [timestamp, timezone, official link]
**Required changes:** [scientific, policy, format, artifact]
**Reverse schedule:** [owners and dates]
**Unknowns:** [items requiring editor/organizer confirmation]
```

Use `internal-critique` before submission, `paper-writing` for scientific revision, and `milestone-tracker` for the verified schedule.
