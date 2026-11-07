---
name: daily-auditor
description: "The read-only morning audit: last 7 complete days vs the prior 7, wasted budget, fading ads, starved tests, pixel problems, one next test. Max 5 recommendations, changes nothing. Use every morning, or right now on any account you suspect is leaking."
---

# Daily Auditor

## Doctrine
Nobody looks at your ad account every day. Not the agency (check the activity history), not Meta (its recommendations optimize Meta's revenue), usually not even you. Meanwhile the best community advice is "stop touching your campaigns", which only works if something is still watching. The resolution: read daily, act rarely. A read-only audit is what lets you keep your hands off without flying blind.

## When to use
- Every morning, same time, whether things feel fine or not. Quiet failures are the expensive ones.
- Also: on any account managed by someone else, as an accountability check.
- Needs a Meta Ads MCP, read access only.

## Run it

```
Run a READ-ONLY audit of my ad account. Change nothing. Compare the last 7 complete days against the prior 7, at campaign, ad set, and ad level, and give me at most 5 findings, ranked by dollars at stake:

1. Wasted budget: spend with zero results, and where it is pooling.
2. Fading ads: flag ONLY if frequency > 4.0 AND CTR is down 30%+ vs the prior window. Name the ad.
3. Starved tests: ads that never got enough spend to be judged (Meta picked a favorite early and starved the rest). Tell me which ads never got a real test.
4. Pixel and conversion health: events that stopped firing, double-fires, or a mismatch that makes the numbers lie.
5. The one next test worth running, based on what the winners share.

For every finding: the numbers behind it, from the account. If a number is not in the account, say "no data", never estimate. If nothing is wrong in a category, say so in one line. End with: "No changes were made."
```

## Guardrails
- Read-only is the identity of this skill. It proposes; a human disposes.
- Max 5 findings. A 50-row dashboard dump is not an audit, it is homework.
- Week-over-week complete days only: partial days and lifetime views both lie.
- The fatigue rule (frequency > 4.0 AND CTR -30%) is a deliberate two-condition heuristic to avoid false alarms. It is falsifiable; if your data disagrees, tighten or loosen it and write down why.

## Good output looks like
Five bullets you can read before coffee, each with real account numbers, ending in "No changes were made."
