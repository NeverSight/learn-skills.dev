---
name: win-loss-analysis
description: "Use this skill when you want to learn why deals are won and lost: \"run a win-loss analysis\", \"why are we losing to competitor X\", \"analyse last quarter's closed deals\", \"prepare win-loss interviews\". Analyses closed-won and closed-lost deals and buyer interviews, separates stated reasons from real ones, finds patterns by segment, competitor, deal size and stage, and turns them into specific changes for targeting, messaging, product and sales process."
license: MIT
metadata:
  title: Win-loss analysis
  category: deals
  tags: "Sales Leaders, Marketing, Founders, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "win loss analysis template, why we lose deals, win loss interview questions, claude win loss skill, closed lost analysis"
  inputs: "Closed deals with reasons, Call notes or interviews, Competitor data"
  outputs: "Win and loss patterns, Real vs stated reasons, Recommendations by team, Interview guide"
---

Use this quarterly or after a run of losses. It replaces anecdotes ("we always lose on price") with patterns and specific changes.

## Inputs

- Closed-won and closed-lost deals for the period with stage lost, reason, competitor, amount, segment and cycle length.
- Call notes, emails and, ideally, 5-10 buyer interviews.
- Rep notes on why they think deals went the way they did.

## The play

### 1. Quantify first
Win rate by segment, deal size, lead source, competitor, rep and stage lost. The stage where deals die says more than the reason field: losses after the demo are fit or value problems; losses after the proposal are price, champion or competitor problems.

### 2. Separate stated from real reasons
"Price" is the most common stated reason and often not the real one. Look for evidence: was the economic buyer engaged? Was value quantified? Did the champion go quiet? Real reasons usually fall into: no quantified value, wrong buyer, competitor better fit, poor timing, weak process, product gap.

### 3. Interview buyers
Short calls with won and lost buyers, run by someone other than the rep. Ask about their process and alternatives, not about the rep. A guide:
- What problem were you trying to solve, and why then?
- What alternatives did you consider, including doing nothing?
- What mattered most in the decision?
- Where did we fall short, or stand out?
- What almost made you choose differently?

### 4. Find patterns
A pattern needs 3+ deals pointing the same way. Group into: targeting, messaging, product, pricing, sales process, competition.

### 5. Turn patterns into changes
Each pattern gets one recommended change, an owner and how to measure it next quarter.

## Output format

```
Period: <dates> | Deals: N won, N lost | Win rate: X% (vs X% last period)
Where we win: <segments, use cases, competitors>
Where we lose: <same, with the stage deals die>
Stated vs real reasons: <table>
Patterns (3+ deals each): <pattern - evidence - change - owner - metric>
Quick wins: <changes that can start next week>
```

## What good looks like

- Losses are explained with evidence from the deal, not from the reason picklist.
- Wins are analysed too; knowing why you win tells you where to aim.
- Recommendations name a team and a metric.
- The common mistake is concluding "we need to be cheaper" from picklist data when the losses show no economic buyer was ever met.

## Rules

- MUST quantify before interpreting.
- MUST treat stated reasons as hypotheses until evidence supports them.
- NEVER single out individual reps in a team-wide report; give rep-level findings privately to managers.
- NEVER share interview quotes with identifying details without the buyer's permission.

## Example prompts

- "Here are 80 closed deals from last quarter. Run a win-loss analysis."
- "Why do we keep losing to Acme in mid-market? Notes attached."
- "Write a win-loss interview guide and a request email to lost buyers."
