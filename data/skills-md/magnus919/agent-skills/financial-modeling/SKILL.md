---
name: financial-modeling
description: >-
  Build and review assumptions-led financial models, unit economics, pricing, fundraising
  scenarios, and SaaS operating metrics. Use when calculating CAC, LTV, payback, runway,
  ARR, churn, NDR, Rule of 40, or sales efficiency; when modeling revenue, costs, cash
  flow, pricing, cap tables, or financing. Do not use this skill for unrelated requests;
  route to the nearest named specialist.
license: MIT
metadata:
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: 867a555
---

# Financial Modeling

Use transparent assumptions, clearly labeled periods and units, and base/upside/downside scenarios. A model is a tool for exploring the implications of assumptions, not a prediction.

**Analytical-aid boundary:** This skill provides analytical frameworks, not financial, investment, tax, accounting, or legal advice. Verify inputs and calculations, and consult qualified professionals for decisions that require them.

## When to Use

Load this skill when the task involves:

- Building or reviewing a P&L, balance sheet, cash-flow, revenue, cost, or runway model
- Calculating CAC, LTV, contribution margin, CAC payback, or segment-level unit economics
- Evaluating pricing, packaging, price changes, or monetization
- Preparing fundraising scenarios, a cap table, valuation analysis, or term-sheet questions
- Analyzing SaaS ARR/MRR, churn, retention, NDR, Rule of 40, Magic Number, or burn multiple
- Running sensitivity analysis or comparing base, upside, and downside cases

## When Not to Use

- For statistical inference, experiment design, causal analysis, or general model selection, use `data-scientist`.
- For insurance, actuarial, claims, reserving, solvency, credibility, tail-risk, or financial-risk statistical models, use `actuarial-risk-modeling`.
- For the narrow question of whether a startup reaches profitability before cash runs out, use `yc-default-alive-calculator`.
- Do not use this skill as a substitute for licensed financial, investment, tax, accounting, or legal advice.
- Enterprise pricing negotiations, jurisdiction-specific securities rules, and tax/accounting treatment need specialist review beyond this skill.

## Reference Guide

Load only the reference relevant to the task:

| Reference | Load when |
|---|---|
| [Unit economics](references/unit-economics.md) | Calculating CAC, LTV, payback, gross margin, or contribution margin |
| [Financial modeling](references/financial-modeling.md) | Building linked statements, revenue and cost models, scenarios, or runway |
| [Pricing strategy](references/pricing-strategy.md) | Evaluating value, packaging, tiers, price changes, or elasticity |
| [Fundraising](references/fundraising.md) | Reviewing valuation methods, cap tables, term sheets, or fundraising process |
| [SaaS metrics](references/saas-metrics.md) | Defining and interpreting ARR, churn, NDR, Rule of 40, Magic Number, or burn multiple |
| [Source index](references/source-index.md) | Reviewing provenance, porting scope, source URLs, and currency boundaries |

## Templates

| Template | When to use |
|---|---|
| [Unit economics record](templates/unit-economics-record.md) | Recording segment- or channel-level CAC, LTV, payback, and contribution margin with stated definitions |
| [Pricing decision record](templates/pricing-decision-record.md) | Structuring a pricing or price-change decision: options, unit-economics trade-offs, test plan, and decision |
| [Fundraising scenario](templates/fundraising-scenario.md) | Preparing a raise: size from the cash model, runway per case, fully diluted cap-table impact, and diligence prep |
| [Model sanity checklist](templates/model-sanity-checklist.md) | Cross-checking a model for structure, linkage, driver consistency, and scenario coverage before sharing it |

## Scripts

| Script | When to use |
|---|---|
| [saas-metrics.py](scripts/saas-metrics.py) | Computing ARR, monthly and annualized logo churn, NDR, and Rule of 40 from stated inputs; `--json` for machine-readable output |

## Evals

`evals/evals.json` — output-quality eval manifest for this skill: unit-economics review, pricing decision, fundraising scenario, SaaS metrics interpretation, model sanity check, and runway and burn analysis.

## Working Method

1. Define the decision, audience, currency, time period, and accounting basis before calculating anything.
2. List input sources and assumptions separately from calculated outputs. Keep monthly, quarterly, and annual figures distinct.
3. Build from operational drivers, then use market-level estimates only as a reasonableness check.
4. Show base, upside, and downside cases; vary the assumptions that materially change cash, growth, or profitability.
5. Segment customers, channels, and products when their economics differ. Do not let an average conceal a loss-making segment.
6. Treat benchmarks and thresholds as context-dependent heuristics, not pass/fail rules. Compare against stage, customer segment, contract cadence, business model, and current market conditions.
7. State limitations, reconcile model outputs to the relevant statements where possible, and identify inputs that need professional review.

## Portability

This skill is intentionally host-neutral. Use the host agent's normal mechanisms to load the references listed above. It requires no profile system, task orchestrator, output format, scripts, or external services.
