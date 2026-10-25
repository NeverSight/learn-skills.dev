---
name: media-buyer
description: Build the whole campaign (objective, one broad ad set, a $20/day test, one ad per angle) as a PAUSED draft for review. Use when angles and creatives are approved and it is time to go live.
---

# Media Buyer

## Doctrine
Simple structure wins at small budgets: one campaign, one broad ad set, 3-5 genuinely different angles as separate ads. Fragmenting budget across many ad sets starves the algorithm of signal; low budgets get killed by too much structure, not too little. Targeting stays broad on purpose: post-Andromeda, the ad content is the targeting, and the $20/day test exists to find the angle that closes the loop before real money goes in.

## When to use
- After Creative Director; you have approved ads and image hashes.
- Needs a Meta Ads MCP with write access. Everything is built paused; nothing spends until you publish.

## Run it

```
Build me a test campaign, everything PAUSED until I review it:

1. Campaign: sales objective (or leads, if my offer is lead-gen), one campaign only.
2. Ad set: one, broad targeting (country + broad age range only, no interest stacks), $20/day budget.
3. Ads: one ad per approved angle, using these creatives: [IMAGE HASHES + COPY]. Do not blend angles.
4. Confirm the pixel/conversion event it optimizes toward, and flag if the pixel looks dead or misconfigured BEFORE anything else.
5. Show me the full structure as a table (campaign > ad set > ads with their angles) and wait. I will say "publish" when I have reviewed it.

Do not enable any Advantage+ creative enhancements. I want the creatives to run exactly as approved.
```

## Guardrails
- Paused draft first, always. The human says "publish", the skill never assumes it.
- $20/day until an angle has proven itself with 2-3x target cost-per-result of spend. Scaling before signal is donating to Meta.
- One campaign. If you feel the urge to add a second ad set, you probably need a different angle instead.
- After publishing: hands off for a week. Daily edits reset learning. Reading daily is what the Daily Auditor is for.

## Good output looks like
A paused campaign whose structure you can read in ten seconds, optimizing toward a verified conversion event, with each ad mapped to a named angle.
