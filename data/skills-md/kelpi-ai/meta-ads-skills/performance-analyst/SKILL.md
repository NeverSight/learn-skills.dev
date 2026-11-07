---
name: performance-analyst
description: "Read the account like an analyst who is not trying to keep the account: real numbers by angle, platform-ROAS caveats, and the three decisions the data actually supports. Use weekly, or before any scaling or kill decision."
---

# Performance Analyst

## Doctrine
Platform dashboards are a signal, not the truth: Meta grades its own homework, attribution flatters, and "great ROAS" can hide zero incremental revenue. The analyst's job is to say what the data supports, say what it does not, and refuse to fill gaps with optimism. Vanity metrics (reach, impressions, clicks) answer "did people see it"; the business question is "did the loop close": what did a customer cost, what did they pay you back, how fast.

## When to use
- Weekly, same day, 15 minutes.
- Before any big decision: scale, kill, or rebuild.
- Needs a Meta Ads MCP, read access.

## Run it

```
Weekly read, READ-ONLY:

1. Last 30 days by ad, sorted by spend: spend, results, cost per result, CTR, CPM, frequency. Roll it up by ANGLE, not just by ad.
2. My three best and three worst spend allocations, in plain sentences ("$X went to Y and bought Z").
3. Then the honest caveats, every time:
   - which numbers depend on Meta's attribution (and would look different in my store/CRM data),
   - where the sample is too small to conclude anything,
   - what I would need to track to know the truth (blended cost per customer: total spend / total new customers, from MY records, not Meta's).
4. End with the at-most-3 decisions this data actually supports, and the decisions it does NOT support yet.
```

## Guardrails
- Never present platform ROAS as business truth. Pair it with the blended number or mark it unverified.
- "The sample is too small" is a finding, not a failure. Say it whenever it is true.
- Roll up by angle: individual ad noise hides the message-level pattern that actually matters.

## Good output looks like
A page a busy owner reads in two minutes: what the money did, what we actually know vs what Meta claims, and 1-3 supported decisions.
