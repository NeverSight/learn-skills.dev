---
name: pixel-conversions
description: "Verify the tracking is telling the truth: which events fire, which double-fire or died, and whether Meta's numbers can be reconciled with your store's. Use before launch, after any site change, and whenever dashboards disagree."
---

# Pixel & Conversions

## Doctrine
If the pixel is broken, every other number is a lie, and the algorithm optimizes toward the lie. The most common ownerside symptom is "Meta says my ads are fine, Shopify says sales are down": that is either attribution's normal flattery or a real tracking break, and knowing which is worth more than any optimization. Measurement integrity precedes optimization, always.

## When to use
- Before the first campaign, after every site or checkout change, and monthly regardless.
- Whenever Meta's dashboard and your store/CRM disagree hard.
- Needs a Meta Ads MCP, read access.

## Run it

```
Tracking truth check, READ-ONLY:

1. List the pixels on my account and which one my active campaigns optimize toward.
2. For the last 7 days: which conversion events fired, at what volume? Flag anything that looks broken: purchase events at zero while traffic flows, events double-firing, or a custom event that silently replaced a standard one.
3. Compare Meta's reported conversions for the period against my store's number: [MY STORE'S COUNT]. State the gap as a percentage and explain the plausible causes in plain language (attribution windows, view-through, genuine breakage), ranked by likelihood.
4. Tell me the ONE fix worth doing first if anything is broken, and what it would confirm.
5. Change nothing.
```

## Guardrails
- Read-only; fixes happen on the site or in Events Manager by a human.
- Never explain a gap away: "a 15% gap is normal attribution behavior" and "your purchase event died Tuesday" are different findings; say which one the data shows.
- If store numbers are unavailable, say the reconciliation is incomplete rather than trusting Meta's side alone.

## Good output looks like
A verdict in one line ("your tracking is telling the truth" or "purchase events died on [date]"), the evidence, and one prioritized fix.
