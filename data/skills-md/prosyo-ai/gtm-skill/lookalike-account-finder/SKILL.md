---
name: lookalike-account-finder
description: "Use this skill when you want more accounts like your best customers: \"find companies like our top 10\", \"build a lookalike list\", \"who else looks like Acme\". Profiles your best customers on the traits that predicted the win, searches for companies that share them, scores each match on similarity and timing, and explains why each one made the list. Produces a ranked lookalike account list with match reasons and a suggested reference customer for each, ready for outbound or ABM."
license: MIT
metadata:
  title: Lookalike account finder
  category: prospecting
  tags: "Founders, Sales, Marketing, SDR"
  author: prosyo
  version: "1.0.0"
  keywords: "lookalike accounts, find companies similar to customers, lookalike audience b2b, claude lookalike skill, similar companies finder"
  inputs: "Best customer list, Why they bought, Exclusion list"
  outputs: "Ranked lookalike accounts, Match reasons, Reference customer per account"
---

Use this when your best customers are the clearest definition of your ICP. It produces a ranked list of companies that look like them, each with the reason it matched and the customer story to lead with.

## Inputs

- 5 to 20 best customers, ranked by value and fit.
- Why each one bought, in a line.
- Exclusions: current customers, open deals, competitors, partners.

## The play

### 1. Profile the seeds
For each seed customer, capture the traits that mattered: industry niche (not just industry), business model, headcount band, growth stage, region, technologies, team structure, the trigger that preceded the deal. Look for the 3-5 traits most seeds share; ignore traits only one or two have.

### 2. Weight the traits
Not every shared trait predicts a win. Weight by how specific it is: "sells to restaurants through a field sales team" matters more than "B2B, 50-200 employees".

### 3. Search in widening circles
1. Direct peers: competitors of your customers, members of the same associations, exhibitors at the same niche events.
2. Same model, adjacent niche: a company selling the same way to a neighbouring market.
3. Same stack and stage: companies running the same tools at the same size.

Direct peers convert best because the customer story transfers word for word.

### 4. Score each match
| Component | Points |
| --- | --- |
| Shares the core niche and model | 0-40 |
| Size and stage within seed range | 0-20 |
| Shares stack or team structure | 0-15 |
| Active trigger in last 90 days | 0-25 |

70+ goes to outbound now; 50-69 goes to a nurture or a later wave.

### 5. Attach the reference
For each account, name the seed customer it most resembles. That becomes the proof point in the first message, if the customer is approved for reference.

## Output format

```
Seeds: <list>  |  Shared traits: <3-5 weighted traits>
Lookalikes (ranked):
  <company> - score - match reasons (2-3) - trigger - closest seed - approved to name? y/n
Excluded: <counts by reason>
```

## What good looks like

- Match reasons a rep could say out loud: "Same model as Northwind: field teams selling into independent pharmacies."
- Direct peers of happy customers lead the list.
- Timing is scored, so the top of the list is not just similar but ready.
- The common mistake is matching on industry and size only, which returns hundreds of generic companies and none of the nuance that made the seeds buy.

## Rules

- MUST explain why each account matched.
- MUST only name a reference customer if the user confirms the customer is approved for that.
- NEVER include current customers, competitors or open deals.

## Example prompts

- "Here are our 12 best customers. Find 100 lookalikes and rank them."
- "Find companies like Northwind and Contoso and tell me which customer story to use for each."
- "Build a lookalike list from our top accounts in healthcare only."
