---
name: account-scorecard
description: 'Turn a Google Ads account into a short weekly scorecard tied to the business outcome, with clear formulas, targets, and caveats. Use when a dashboard has too many numbers and too little meaning.'
---

# Account Scorecard

## Doctrine

A scorecard is a small set of numbers that makes a decision easier. Start with the business outcome, then include the platform metrics that explain it. Reported conversion value is not profit, a click is not a lead, and an "all conversions" total can be full of actions nobody wants the bidding system to chase.

## When to use

- For a weekly owner or operator update that should fit on one screen.
- Use a connected Google Ads MCP, or paste matched account and CRM exports.
- Bring the primary conversion definition, target CPA or ROAS, and margin or downstream lead data when available.

## Run it

```
Build a READ-ONLY Google Ads scorecard. Use live account data if connected; otherwise use what I paste. Change nothing.

1. Confirm the business objective, primary conversion, value definition, currency, timezone, current period, equal comparison period, and target.
2. Choose 5 to 7 KPIs. Lead with the closest trusted business outcome available, such as purchases, qualified leads, cost per qualified lead, or trusted conversion value.
3. For every KPI show: definition, formula, source, current value, comparison value, target, status, and caveat.
4. Keep reported ROAS labeled as reported conversion value divided by ad spend. Do not call it profit or incrementality. If margin, lead quality, or offline outcomes are missing, say so.
5. Use impressions, clicks, CTR, CPC, impression share, and lost impression share only when they explain movement in a business KPI.
6. End with one plain-language health verdict and the 2 next questions the scorecard cannot answer yet.

Do not add every available metric. Do not recommend a budget or bid change from the scorecard alone. End with "No changes were made."
```

## Guardrails

- Use primary business conversions, not an inflated "all conversions" number, unless the user explicitly asks for the latter.
- No target means no claim that a result is healthy, profitable, or bad. Describe direction instead.
- Reported conversion value is not revenue unless the source and definition confirm it, and revenue is not profit without margin.
- Lost impression share from budget does not prove there is profitable room to spend more.
- Keep the scorecard short. Extra metrics belong in a diagnostic follow-up, not the weekly headline.

## Good output looks like

Five to seven trustworthy numbers, each defined and sourced, followed by a verdict that says what is known, what is missing, and what deserves a deeper look.
