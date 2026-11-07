---
name: deal-qualification
description: "Use this skill when you need to qualify a B2B deal or check its health: \"qualify this opportunity\", \"MEDDICC this deal\", \"is this deal real\", \"score my opportunity\". Scores the deal on metrics, economic buyer, decision criteria, decision process, paper process, pain, champion and competition, separates what is confirmed from what is assumed, names the biggest gaps, and gives the questions and actions that close them before the forecast call."
license: MIT
metadata:
  title: Deal qualification (MEDDICC)
  category: deals
  tags: "Sales, Sales Leaders, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "meddicc template, deal qualification framework, opportunity scoring, claude meddicc skill, sales qualification checklist"
  inputs: "Deal notes and emails, Stage and amount, Close date"
  outputs: "MEDDICC scorecard, Confirmed vs assumed, Gap list, Questions to ask next"
---

Use this whenever a deal enters a forecast or moves stage. It produces a scorecard that separates evidence from hope.

## Inputs

- Call notes, emails and the deal record.
- Stage, amount and expected close date.
- Who the rep has met and what each said.

## The play

### 1. Score each element 0-3
| Element | Question | 3 means |
| --- | --- | --- |
| **Metrics** | What measurable gain does the buyer expect? | Number agreed with the buyer |
| **Economic buyer** | Who signs and controls the budget? | Met them; they confirmed the priority |
| **Decision criteria** | What will they judge options on? | Written or stated criteria we influenced |
| **Decision process** | What steps lead to a decision? | Steps, people and dates mapped with the champion |
| **Paper process** | What happens from "yes" to signature? | Legal, security, procurement steps and timing known |
| **Identify pain** | What problem, how bad, why now? | Pain with impact in their words and a reason for now |
| **Champion** | Who sells for us internally, with power? | Tested: they took an action that cost them effort |
| **Competition** | What else are they considering, including doing nothing? | Named alternatives and why we win |

0 unknown, 1 assumed, 2 partial evidence, 3 confirmed. Read [references/meddicc-scorecard.md](references/meddicc-scorecard.md) for scoring evidence examples and stage minimums.

### 2. Mark evidence
For each score, note the evidence and the source (call date, email). Anything without evidence is scored 1 at most.

### 3. Check stage minimums
Commit-stage deals usually need 2+ on every element and 3 on pain, champion and economic buyer. A deal below the minimum for its stage should move back a stage or out of the forecast.

### 4. Find the biggest gap
The weakest element on the critical path to signature, usually economic buyer, paper process or champion. One gap, one owner, one date.

### 5. Write the questions
Exact questions to ask next, phrased for the buyer, plus who should ask them.

## Output format

```
Deal: <name> | <amount> | <stage> | close <date>
Scorecard: M x | EB x | DC x | DP x | PP x | IP x | C x | Comp x  (total /24)
Confirmed: <evidence list>   Assumed: <list>
Stage check: meets / below minimum for <stage>
Biggest gap: <element> - risk - action - owner - date
Next questions: <3-5>
Forecast call: commit / best case / pipeline / remove
```

## What good looks like

- Scores tie to evidence a manager can check.
- The champion is tested, not just friendly.
- The close date is backed by a paper process timeline.
- The common mistake is scoring from the rep's optimism: "the economic buyer is the CFO" with no meeting is a 1, not a 3.

## Rules

- MUST cap any element without evidence at 1.
- MUST name one biggest gap with an owner and date.
- NEVER recommend "commit" for a deal without an engaged economic buyer.

## Example prompts

- "MEDDICC this deal from my notes and emails."
- "Score my 6 commit deals and tell me which are really commits."
- "What questions should I ask next week to qualify this opportunity?"
