---
name: discovery-call-prep
description: "Use this skill when you have a discovery or first sales call coming up and want to run it well: \"prep me for this discovery call\", \"what questions should I ask\", \"build a discovery call agenda\", \"call plan for tomorrow\". Combines account and person research with a call plan: hypothesis of their problem, agenda, discovery questions ordered from situation to impact to decision, qualification checks, likely objections and the next step to ask for. Produces a one-page call plan and a post-call notes template."
license: MIT
metadata:
  title: Discovery call prep
  category: replies-meetings
  tags: "Sales, Founders, SDR"
  author: prosyo
  version: "1.0.0"
  keywords: "discovery call questions, discovery call template, sales call preparation, claude discovery call skill, first sales meeting agenda"
  inputs: "Prospect and account, How the meeting was booked, Product and ideal outcome"
  outputs: "One-page call plan, Question list, Next-step ask, Notes template"
---

Use this before every first call. Good discovery is the cheapest way to win deals and the fastest way to disqualify bad ones.

## Inputs

- Prospect, company and anyone else attending.
- How the meeting was booked and what they said they want.
- Product, ideal customer and what a good next step looks like (demo, technical call, trial, proposal).

## The play

### 1. Form a hypothesis
From research, write: "I think <company> struggles with <problem> because <evidence>, which costs them <impact>." The call tests the hypothesis; it does not pitch it.

### 2. Set the agenda up front
> "I'd like to spend most of the time on how <area> runs today and what you'd want to change. If it looks like a fit, I'll show you the relevant part. And if it doesn't, I'll tell you. Sound good? Anything to add?"

### 3. Ask in layers
1. **Situation**: how it works today, who is involved, what tools.
2. **Problem**: where it breaks, how often, what they have tried.
3. **Impact**: what it costs in time, money, risk, missed targets; who feels it.
4. **Priority**: why now, what happens if nothing changes, other priorities competing.
5. **Decision**: who decides, how they buy, budget timing, what they need to see.

Read [references/discovery-questions.md](references/discovery-questions.md) for the full bank with follow-ups and the qualification checklist.

### 4. Prepare for the likely objections
Pick the two most likely given their situation and have one question and one proof ready for each.

### 5. Plan the close of the call
The next step is concrete, dated and agreed before hanging up: "Let's book the technical review with your RevOps lead for Thursday; I'll send the invite now."

## Call plan format

```
Who: <attendees + roles>     Booked via: <how>    Goal of call: <next step wanted>
Hypothesis: <problem - evidence - impact>
Agenda: <3 lines>
Top questions: <8-10, by layer>
Qualification to confirm: problem, impact, priority, decision process, budget timing
Likely objections → question + proof
Next step to ask for: <specific>
```

## What good looks like

- The prospect talks 60-70% of the time.
- Impact is quantified in their words before any demo.
- The call ends with a dated next step or a clear disqualification.
- The common mistake is turning discovery into a demo in minute five because the prospect said "so what do you do?".

## Rules

- MUST end the call with a specific next step or an honest no.
- MUST capture the buyer's words for problem and impact.
- NEVER demo before understanding the problem, unless they insist; then demo only the relevant part.
- NEVER assume budget or authority without asking.

## Example prompts

- "Prep me for a discovery call tomorrow with the Head of Ops at Northwind. Research below."
- "Give me 15 discovery questions for selling to CFOs."
- "Make a post-call notes template that maps to our qualification checklist."
