---
name: outbound-math
description: "Use this skill when you need to turn a revenue or pipeline target into outbound activity: \"how many emails to hit quota\", \"reverse funnel calculator\", \"how many SDRs do we need\", \"what activity does our pipeline target require\". Works backwards from revenue through win rate, deal size, opportunity rate, meeting rate and reply rate to contacts, touches and daily activity per rep, shows the levers that change the answer most, and checks it against team capacity and market size."
license: MIT
metadata:
  title: Outbound math
  category: revops
  tags: "Sales Leaders, Founders, RevOps, SDR"
  author: prosyo
  version: "1.0.0"
  keywords: "reverse funnel calculator, sales activity calculator, how many sdrs do i need, claude outbound math skill, pipeline target to activity"
  inputs: "Revenue or pipeline target, Conversion rates, Team size and capacity"
  outputs: "Reverse funnel, Activity per rep per day, Headcount need, Lever analysis"
---

Use this when setting targets or headcount. It shows what a number actually requires, and which conversion rate to improve before adding people.

## Inputs

- Target: new revenue (or pipeline) for the period, and how much should come from outbound.
- Rates: win rate, average deal size, held meeting to opportunity, booked to held, positive reply to booked, positive reply rate per contact. Measured if possible; otherwise labelled assumptions.
- Team: SDRs and AEs, and their realistic capacity.

## The play

### 1. Run the reverse funnel
```
Outbound revenue target              $600,000 per quarter
÷ average deal size ($20,000)        = 30 deals won
÷ win rate (25%)                     = 120 opportunities
÷ meeting → opportunity (50%)        = 240 meetings held
÷ show rate (80%)                    = 300 meetings booked
÷ positive reply → booked (60%)      = 500 positive replies
÷ positive reply rate (1.5%)         = 33,333 contacts per quarter
÷ 13 weeks                           = 2,564 new contacts per week
```

### 2. Convert to daily activity
Contacts per week × touches per contact ÷ 5 = touches per day across the team. Divide by reps for activity per rep, and compare with what one rep can do well (for example 50-80 new contacts a week with personalization).

### 3. Check headcount and capacity
Reps needed = contacts per week ÷ realistic contacts per rep per week. AEs needed = meetings per week ÷ meetings one AE can hold well (typically 8-15).

### 4. Check market size
Contacts per year vs reachable contacts in the ICP. If the plan needs 130,000 contacts a year and the ICP has 25,000, the plan is impossible as written.

### 5. Show the levers
Recalculate with each rate improved by a realistic step. Usually positive reply rate and meeting-to-opportunity rate change the answer most. Example: 1.5% → 2.5% positive replies cuts required contacts by 40%.

## Output format

```
Target → deals → opportunities → meetings held → booked → positive replies → contacts
Per week: contacts N | touches N | per rep N
Headcount: SDRs N (have N) | AEs N (have N)
Market check: N contacts/year vs N reachable → OK / exhausts in N months
Levers: <rate change → contacts needed>
Assumptions: <which rates are measured vs assumed>
```

## What good looks like

- Every rate is labelled measured or assumed.
- The plan is checked against both capacity and market size.
- The answer recommends the lever to improve before the hire to make.
- The common mistake is solving a target with activity alone ("send 3x more"), which burns the market and the domains.

## Rules

- MUST label assumed rates and use conservative ones.
- MUST check the plan against the reachable market.
- NEVER present the output as a forecast; it is a requirement model.

## Example prompts

- "We need $1.2M in new ARR from outbound this year. What activity does that take?"
- "How many SDRs do we need for 200 meetings a quarter?"
- "Which conversion rate should we improve first to hit target without hiring?"
