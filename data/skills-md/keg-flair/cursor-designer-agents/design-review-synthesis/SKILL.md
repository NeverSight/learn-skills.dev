---
name: design-review-synthesis
description: Synthesizes competing design review inputs into one prioritized recommendation with conflicts, trade-offs, rationale, measurement, and a test plan. Use when UX, accessibility, analytics, research, or stakeholder signals disagree.
---

# Design Review Synthesis

See shared conventions in `docs/HOUSE_STYLE.md` (priority, confidence, evidence labels, and verification).

## Defaults

- **Decision-first**: give one recommended path with an escape hatch.
- **Evidence-weighted**: prioritize direct user behavior, observed user evidence, and must-fix accessibility risk over unverified preference.
- **Conflict-aware**: name disagreements instead of smoothing them away.

## Constraints

- **Do not invent** metrics, research findings, visual details, or stakeholder intent.
- **Ask at most 3 clarifying questions**; if context is thin, proceed with assumptions and low confidence.
- **Preserve trade-offs** between usability, accessibility, metrics, implementation cost, and business constraints.

## Inputs to request (only if missing)

- Review findings or agent outputs
- Metrics/funnel data and definitions
- Research snippets or usability observations
- Accessibility constraints
- Business/product constraints
- Decision needed

## Output template

```markdown
#### Recommendation
- **Recommended path**:
- **User goal**:
- **What changes**:
- **Why it helps**:
- **Confidence**:

#### Conflicts / trade-offs
- **Conflict**:
  - **Resolution**:
  - **Risk**:

#### Rationale
- **Strongest evidence**:
- **Supporting evidence**:
- **Unknowns**:

#### What to measure
- **Primary metric**:
- **Guardrails**:
- **Qualitative checks**:

#### Test plan / validation
- …

#### Open questions
- …
```

## Quality bar

- Do not average conflicting recommendations into generic compromise.
- State which signal gets priority and why.
- Include what would change the recommendation.
