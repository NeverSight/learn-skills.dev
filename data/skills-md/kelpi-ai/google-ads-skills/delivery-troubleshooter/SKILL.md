---
name: delivery-troubleshooter
description: 'Find why Google Ads delivery or reporting changed, separate observed blockers from possible causes, and put the checks in the right order. Use when impressions, clicks, spend, or conversions suddenly fall.'
---

# Delivery Troubleshooter

## Doctrine

Delivery problems leave clues at different levels: account status, campaign status reasons, disapprovals, budgets, rank, destinations, bid-strategy learning, and conversion actions. Do not flatten those clues into one confident story. Name what is observed, what is only suspected, and which dependency must be fixed before the next diagnosis means anything.

## When to use

- When impressions, clicks, spend, or recorded conversions drop without a clear reason.
- Use a connected Google Ads MCP, or paste status, policy, delivery, budget, impression-share, and conversion-action exports.
- Include dates, entity names and IDs, recent changes, and site incidents when available.

## Run it

```
Run a READ-ONLY Google Ads delivery check. Use live account data if connected; otherwise use what I paste. Change nothing.

1. State the scope, date range, expected baseline, and what changed.
2. Check account and billing status, campaign and ad-group primary status reasons, ad and keyword approvals, landing-page availability, bid-strategy status, budget limits, lost impression share from budget and rank, and conversion-action status.
3. Return an issue table with: entity, observed status, evidence, likely impact, suspected causes, confidence, and next check.
4. Keep observed facts separate from suspected causes. Lost impression share from rank is not proof of a Quality Score problem. A site incident is not proof it caused a disapproval unless the policy reason and timing support it.
5. Put fixes in dependency order. Restore broken destinations before requesting ad review; validate tracking before judging conversion performance; resolve serving blockers before tuning bids or budgets.
6. List healthy checks and unknowns so I can see what has already been ruled out.

Do not change budgets, bids, ads, destinations, goals, or statuses. End with "No changes were made."
```

## Guardrails

- Never turn correlation into root cause. Use "possible cause" until the account evidence supports it.
- Do not call lost impression share from rank a Quality Score penalty. Rank can reflect bids, ad quality, assets, competition, and auction context.
- A small nonzero budget loss is still a fact. Report it without calling it noise or automatically recommending more budget.
- Google Ads data can show suspicious conversion reporting, but it cannot prove a website tag fires or reconcile a CRM without separate evidence.
- Do not claim the campaign was healthy before the incident unless the earlier data is provided.

## Good output looks like

A short, dependency-aware incident report: the real blockers first, suspected causes labeled honestly, the checks that come next, and no premature budget or bid change.
