---
name: revenue-model
description: Designs pricing hypotheses, revenue scenarios, and unit-economics checks including CAC, ARPU, churn, LTV, and payback for software ideas. Use when the user asks about pricing, willingness to pay, unit economics, ARR, MRR, or revenue projections.
disable-model-invocation: true
---

# Revenue Model

## Checklist

- [ ] Anchor pricing to competitor bands
- [ ] State the target segment and pricing logic
- [ ] Build base, upside, and downside scenarios
- [ ] Estimate CAC by channel
- [ ] Compute ARPU, churn, LTV, payback, and LTV:CAC
- [ ] Record whether economics support strong go, conditional go, or kill

## Scenario table

| Scenario | Price | Adoption | CAC | Churn | LTV | LTV:CAC | Notes |
| -------- | ----- | -------- | --- | ----- | --- | ------- | ----- |
| Base     |       |          |     |       |     |         |       |
| Upside   |       |          |     |       |     |         |       |
| Downside |       |          |     |       |     |         |       |

Default monthly churn to 5% unless evidence says otherwise.

## LTV:CAC decision bands (canonical)

| LTV:CAC (base case) | Interpretation                                                                  |
| ------------------- | ------------------------------------------------------------------------------- |
| **< 2:1**           | Kill cue — economics do not support the stated goal                             |
| **2:1 to < 3:1**    | Conditional go only — name the gap (price, CAC, churn, segment)                 |
| **≥ 3:1**           | Meets bar for **Strong go** on unit economics (with scorecard and other stages) |

## Willingness to pay

Prefer deposits, LOIs, pre-orders, and paid pilots over compliments or email-only signups.

## Output

Save to `discovery/<topic-slug>/research/YYYY-MM-DD-<topic-slug>-revenue.md`.
