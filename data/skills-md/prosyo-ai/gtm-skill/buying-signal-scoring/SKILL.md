---
name: buying-signal-scoring
description: "Use this skill when you track buying signals and need to decide which ones deserve outreach today: \"which accounts are in market\", \"prioritise these signals\", \"build a signal-based selling system\". Catalogues the signals that matter for your offer (hiring, funding, leadership changes, intent, website visits, engagement, tech changes), scores them on strength and freshness, stacks multiple signals per account, and outputs a daily ranked action list with the play to run for each. The core of signal-based outbound."
license: MIT
metadata:
  title: Buying signal scoring
  category: signals
  tags: "SDR, Sales, RevOps, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "buying signals, signal based selling, intent signals scoring, claude buying signals skill, in-market accounts"
  inputs: "Signal feed or list of events, ICP and account tiers, Your offer"
  outputs: "Signal catalogue with weights, Daily ranked action list, Play per signal"
---

Use this to turn a noisy stream of events into a short list of accounts to contact today, with a reason and a play for each.

## Inputs

- The signals available: job listings, leadership changes, funding, web visits, content engagement, third-party intent, technology changes, product usage for existing users.
- The ICP and account tiers.
- The offer, so each signal can be tied to a reason to talk.

## The play

### 1. Build the signal catalogue
List every signal you can detect. For each, write the "so what": why this event makes your offer more relevant now. Signals without a clear "so what" are noise, however easy they are to collect.

### 2. Weight by strength and freshness
Strength reflects how often the signal precedes a real opportunity. Freshness reflects how fast it decays. Read [references/signal-weights.md](references/signal-weights.md) for the starter weights, decay curves and the stacking rules.

### 3. Stack signals per account
One signal is a hint; two or three on the same account in the same month is a pattern. Score = sum of decayed signal weights × fit multiplier (Tier 1: 1.0, Tier 2: 0.7, Tier 3: 0.4). Accounts outside the ICP get no multiplier and do not make the list, however loud their signals.

### 4. Pick the play
Each signal type maps to a play: who to contact, the angle, the channel and the timing. A new VP gets a "first 90 days" angle; a pricing-page visit gets a fast, low-pressure helpful touch; a hiring wave gets a "before your new team starts" angle.

### 5. Produce the daily list
Rank by score, cap at the team's capacity (typically 15-30 signal-led touches per rep per day), and include the evidence so reps can write in seconds.

## Output format

```
rank | account | score | signals (type - date - source) | contact | play | suggested opener
```

Plus: signals that fired on accounts outside the ICP (for review), and signals that decayed without action this week.

## What good looks like

- Every row has evidence a rep can check in one click.
- The list is short enough to finish. A 300-row "hot list" is a cold list.
- Plays reference the situation, never the surveillance: "teams that just raised often..." not "I saw you were on our pricing page".
- Stacked signals beat single loud ones. One webinar attendance is weaker than a new VP plus two relevant job listings.
- The common mistake is treating every signal as equal and blasting the same template the moment anything fires.

## Rules

- MUST apply the ICP filter before ranking.
- MUST decay signals over time.
- NEVER reveal in outreach that you tracked someone's website visit or profile view.
- NEVER contact the same person on more than one signal in the same week.

## Example prompts

- "Here are this week's signals across our 800 target accounts. Who should we contact today?"
- "Design a signal catalogue and weights for our HR software."
- "Turn these funding and hiring alerts into a ranked list with openers."
