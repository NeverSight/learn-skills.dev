---
name: competitor-teardown
description: "Use this skill when you need to understand a competitor well enough to beat them: a deal is going head to head, a new competitor appeared, positioning needs a refresh, or reps keep losing on the same objection. Tears down the competitor's positioning, ideal customer, pricing and packaging, product strengths and gaps, customer complaints, sales motion and recent moves, and produces a teardown with where to compete, where to avoid, and the talk track that wins. Built from public sources and your own win-loss notes."
license: MIT
metadata:
  title: Competitor teardown
  category: research
  tags: "Marketing, Sales Leaders, Founders, Sales"
  author: prosyo
  version: "1.0.0"
  keywords: "competitor analysis template, competitive teardown, competitor research b2b, claude competitor analysis skill, competitive intelligence"
  inputs: "Competitor name or site, Your product and pricing, Win-loss notes"
  outputs: "Competitor teardown, Where to compete and avoid, Win themes, Talk track"
---

Use this when a competitor shows up in deals often enough to matter. It produces a teardown that tells sales where to fight, where to walk away and what to say.

## Inputs

- Competitor name and site.
- Your own positioning, product scope and pricing.
- Win-loss notes or rep anecdotes involving this competitor. Even five are useful.

## The play

### 1. Read their story
Homepage headline, category they claim, the customer logos they lead with, the use cases on their navigation. Write their positioning in one sentence as they would: "For <who>, <product> is the <category> that <benefit>."

### 2. Map pricing and packaging
Plans, price points, what is gated to higher tiers, contract terms, free trial or not. Packaging choices reveal who they want and who they tolerate.

### 3. Mine customer complaints
Read reviews (lowest ratings first), community threads and public support forums. Cluster complaints into themes and count them. Recurring themes with 5+ mentions are real weaknesses; single rants are not.

### 4. Map their sales motion
Self-serve or sales-led, demo gating, typical discount behaviour, implementation time, who they target in the buying committee.

### 5. Read recent moves
Launches, pricing changes, leadership hires, funding, layoffs from the last 12 months. Direction of travel matters more than today's feature list.

### 6. Decide where to compete
Use the matrix in [references/teardown-template.md](references/teardown-template.md): segments where you win, where you tie and where you lose. Losing segments are as valuable as winning ones; they tell reps when to qualify out early.

## Output format

```
Competitor: <name>  |  Their positioning: <one sentence>
Who they win: <segments>         Who they struggle with: <segments>
Pricing: <summary>               Packaging traps: <what is gated>
Strengths (be honest): <3>
Weaknesses (evidence): <3, with count of mentions and source>
Recent moves: <dated>
Where we compete: <segments + win theme>
Where we avoid: <segments + early qualify-out question>
Talk track: <3 lines a rep can say, no trash talk>
Landmines: <questions that expose their weak spots, asked neutrally>
```

## What good looks like

- Honest strengths. A teardown that says the competitor is bad at everything gets ignored by reps who just lost to them.
- Weaknesses come with evidence and counts.
- Landmine questions are neutral and fair: "How long did implementation take for teams your size?" not "Did you know they're terrible at onboarding?"
- It answers when to walk away. The best teams lose fewer deals by qualifying out of the wrong ones faster.

## Rules

- MUST use public sources or your own deal notes, and cite them.
- MUST date pricing; pricing pages change often.
- NEVER disparage the competitor in rep-facing copy.
- NEVER use confidential material obtained from a competitor's employees or customers under NDA.

## Example prompts

- "Do a teardown of Northbeam versus us. We lose to them in mid-market."
- "A new competitor just launched. Tear them down from their site and reviews."
- "Turn these 14 loss notes against Acme into a teardown and talk track."
