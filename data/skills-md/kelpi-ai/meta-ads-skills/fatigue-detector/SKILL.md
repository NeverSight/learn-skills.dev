---
name: fatigue-detector
description: Diagnose whether an ad is actually fatigued (two-condition rule) or you are just impatient, and decide refresh vs leave alone. Use when performance dips or a lead cost suddenly multiplies.
---

# Fatigue Detector

## Doctrine
"CTR down, CPM up, must be fatigue" is the most common misdiagnosis in ads. Sometimes it is the auction, the season, or a broken pixel. The two-condition rule cuts false alarms: an ad is fatigued only when frequency > 4.0 AND CTR is down 30%+ from its own baseline. Post-Andromeda, ad lifespans compressed and fatigue scales with spend more than with days, so small budgets fatigue slower than the "20 new ads a month" crowd claims. The owner's version of this pain: "the exact same ads that cost $6.85 a lead now cost $30.90."

## When to use
- A previously-working ad got expensive.
- Before killing anything: impatience kills more winners than fatigue does.
- Needs a Meta Ads MCP, read access.

## Run it

```
Fatigue check, READ-ONLY, change nothing:

1. Pull frequency and CTR by ad for the last 14 days, plus each ad's CTR baseline from its best prior 14-day window.
2. Apply the two-condition rule: flag ONLY ads with frequency > 4.0 AND CTR down 30%+ from their own baseline.
3. For each flagged ad: which angle is it, how much has it spent since the decline started, and is a sibling angle still healthy?
4. For ads that LOOK tired but fail the rule: tell me the likelier cause (auction/CPM shift, seasonality, tracking change, or not enough recent spend to judge).
5. Recommend per flagged ad: refresh the creative (same angle, new execution) or retire the angle (the message is exhausted, not the image). Do not touch anything.
```

## Guardrails
- Read-only. Refresh and retire are human decisions.
- Never judge an ad against another ad's baseline; fatigue is measured against the ad's own history.
- A new execution of a dead angle is still dead. If three executions of one angle all decayed fast, the angle is done: back to Angle Writer.

## Good output looks like
A short list split into "actually fatigued (here is the evidence)" and "leave it alone (here is what is really happening)".
