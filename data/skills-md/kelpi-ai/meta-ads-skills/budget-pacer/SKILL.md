---
name: budget-pacer
description: Propose budget rules and schedules (spend caps, loser-pauses, winner scaling in 20% steps) as drafts you approve. Use once an angle has proven itself and it is time to scale without breaking it.
---

# Budget Pacer

## Doctrine
"Every time I touch a winning campaign it crashes" is a scaling story, not a curse: big budget jumps reset learning, and panic edits kill compounding winners. Pacing means the boring version: scale in ~20% steps, no more than once a day, pause what has proven it loses, and let rules carry the discipline your fingers do not have. The loop decides the ceiling: scale only what returns its spend fast enough to fund the next round.

## When to use
- An angle has spent 2-3x target cost-per-result and holds. Time to feed it.
- You keep manually raising and lowering budgets on vibes.
- Needs a Meta Ads MCP with write access; everything is proposed as a draft first.

## Run it

```
Budget pacing proposal, draft only, change nothing yet:

1. Read the last 14 days by ad set: spend, results, cost per result.
2. Identify what has EARNED a raise (enough spend to judge, cost per result at or under my target of [$X]) and what has earned a pause (2-3x target spent, no results).
3. Propose:
   - a pause rule: pause any ad set whose cost per result exceeds [$X * 1.5] over a 3-day window,
   - a scaling plan for the winner: +20% budget steps, at most one step per day, with the next review date,
   - a spend guardrail: a rule that alerts me if daily account spend exceeds [$CAP].
4. Show me the rules exactly as they would be created. I will say "create" for the ones I want.
```

## Guardrails
- Drafts until the human says "create". Spend changes are the most sensitive write there is.
- +20% steps, not doublings. A budget doubling is a learning reset wearing a growth costume.
- Pause rules use my numbers ([$X] comes from my loop math), never an invented benchmark.
- If the loop math says the winner still is not profitable at scale, say that instead of scaling it.

## Good output looks like
Two or three rules you can read and approve by name, a winner scaling schedule with dates, and no dollar moved without a yes.
