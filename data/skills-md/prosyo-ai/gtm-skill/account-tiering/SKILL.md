---
name: account-tiering
description: "Use this skill when you need to decide which accounts get the most effort: \"tier my account list\", \"which accounts should get 1:1 research\", \"prioritise my territory\", \"score these companies\". Scores every account on ICP fit and timing, assigns Tier 1, 2 or 3 with a clear effort level for each tier, and explains the score so reps trust it. Produces a tiered account list and the operating rules for how much research, personalization and channel effort each tier gets."
license: MIT
metadata:
  title: Account tiering
  category: prospecting
  tags: "Sales, SDR, Sales Leaders, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "account tiering, account prioritization, tier 1 tier 2 tier 3 accounts, claude account scoring skill, territory planning"
  inputs: "Account list, ICP, Signals and CRM history"
  outputs: "Tiered account list, Score breakdown, Effort rules per tier"
---

Use this when there are more accounts than time. It produces tiers that tell every rep how much effort each account deserves, and a score breakdown that makes the tier defensible.

## Inputs

- The account list with whatever firmographics exist.
- The ICP with must-haves, nice-to-haves and disqualifiers.
- Signals and history: intent, website visits, past opportunities, engagement, triggers.

## The play

### 1. Score fit and timing separately
Fit says whether the account could ever buy; timing says whether it might buy now. Keep them as two numbers on a 0-100 scale. Combining them too early hides great-fit accounts that are simply not ready, and they belong in nurture, not the bin.

Read [references/tiering-rubric.md](references/tiering-rubric.md) for the full rubric, the weights and the tie-break rules.

### 2. Place each account on the grid

| | Timing high (60+) | Timing low |
| --- | --- | --- |
| **Fit high (70+)** | Tier 1 | Tier 2 |
| **Fit medium (50-69)** | Tier 2 | Tier 3 |
| **Fit low (under 50)** | Tier 3 or out | Out |

### 3. Cap Tier 1
Tier 1 is limited by research capacity: roughly 20 to 50 accounts per rep at a time. If the scoring puts 400 accounts in Tier 1, raise the thresholds instead of diluting the effort.

### 4. Attach effort rules
| Tier | Research | Personalization | Channels | Contacts per account |
| --- | --- | --- | --- | --- |
| 1 | 20-30 min account + person research | 1:1 opener per person | Email, LinkedIn, phone, video | 3-5 |
| 2 | 5 min trigger check | Segment message plus a personal line | Email and LinkedIn | 2-3 |
| 3 | None | Segment message | Email or LinkedIn | 1-2 |

### 5. Re-tier on a schedule
Timing changes weekly. Re-score monthly, and immediately when a strong signal fires (new leader, funding, high-intent page visit).

## Output format

```
account | fit score | timing score | tier | top 3 score drivers | next action
```

Plus a summary: counts per tier, Tier 1 capacity check, and accounts that moved tiers since the last run.

## What good looks like

- A rep reading the score drivers agrees with the tier more than 8 times out of 10. If they do not, the weights are wrong.
- Tier 1 fits the team's research capacity.
- Great-fit, bad-timing accounts are kept warm, not discarded.
- The common mistake is one blended score where a huge logo with no need outranks a perfect-fit account that just hired for the exact problem.

## Rules

- MUST show the score drivers for every account.
- MUST keep fit and timing as separate scores.
- NEVER let Tier 1 exceed research capacity.
- NEVER tier an account with a disqualifier above "out".

## Example prompts

- "Tier these 600 accounts for my territory. I can research about 40 deeply."
- "Score our target list on fit and timing and show me why each is Tier 1."
- "Re-tier my accounts with this month's intent data."
