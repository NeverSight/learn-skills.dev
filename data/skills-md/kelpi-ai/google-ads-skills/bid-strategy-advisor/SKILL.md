---
name: bid-strategy-advisor
description: 'Choose a Google Ads bidding approach from trusted goals, observed volume, conversion delay, and business targets, then draft an evaluation plan. Use before changing strategy, CPA, ROAS, or budget settings.'
---

# Bid Strategy Advisor

## Doctrine

The best bidding strategy is the one matched to a trustworthy goal and enough recent evidence to evaluate it. Conversion count matters, but there is no universal magic threshold. Conversion quality, delay, value accuracy, budget pressure, recent changes, and learning status all affect the call. Change one major variable at a time and judge it only after the data has matured.

## When to use

- Before moving between click-based, conversion-based, CPA, or value-based bidding.
- When a campaign is limited by budget, stuck in learning, or missing its target.
- Use a connected Google Ads MCP, or paste the campaign's goal map, bid-strategy report, mature performance, budget, conversion delay, and change history.

## Run it

```
Build a READ-ONLY bid-strategy recommendation. Use live Google Ads data if connected; otherwise use what I paste. Change nothing.

1. Confirm the business objective, trusted primary conversion, value quality, current bid strategy and status, current targets, budget, mature performance window, conversion delay, and major change history.
2. Check the conversion signal with the Conversion Tracking Checker. If the goal or value is contaminated, recommend hold and stop.
3. Compare the strategies that fit the objective:
   - click-based bidding when the real goal is traffic or conversion data is not trustworthy;
   - conversion-based bidding when the goal is reliable but values are not;
   - Target CPA when the business has a defensible CPA target and mature performance to anchor it;
   - value-based bidding only when conversion values reflect real, trusted business value.
4. Do not use a fixed conversion-count gate. Explain whether this campaign's volume, delay, volatility, and learning history are enough for the proposed test.
5. If proposing a target, anchor it to mature trailing actuals and the business limit. Do not invent a precise target from a wide acceptable range or incomplete recent days.
6. Keep a budget change separate from a strategy change unless the user explicitly accepts the confounded test. Being limited by budget does not automatically mean more spend is profitable.
7. Return: current fit, recommendation or hold, evidence, preconditions, tradeoffs, draft target logic, approval required, evaluation window, success measure, and rollback triggers.

Do not apply a strategy, target, bid, or budget change. End with "No changes were made."
```

## Guardrails

- No invented minimum such as 15, 30, or 50 conversions for every account. Use the campaign's evidence and conversion cycle.
- Do not call a recent CPA mature when the latest days are still inside the conversion-delay window.
- No Target ROAS or Maximize conversion value recommendation without trustworthy values.
- Do not choose an arbitrary target between current CPA and the maximum acceptable CPA.
- Wait through learning and at least one full conversion cycle before judging a test. Avoid stacking strategy, target, budget, and goal changes together.

## Good output looks like

One clearly reasoned recommendation or hold, grounded in trusted goals and mature data, with an approval gate and a fair way to tell whether the test worked.
