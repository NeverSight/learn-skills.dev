---
name: tam-calculator
description: "Use this skill when you need a credible market size for a B2B product: a board or investor deck, territory planning, deciding which segment to attack, or checking whether outbound has enough accounts to sustain a quota. Builds a bottom-up TAM, SAM and SOM from countable accounts and real prices instead of top-down analyst numbers, shows every assumption, and turns the result into an account count per segment that sales can actually work."
license: MIT
metadata:
  title: TAM, SAM and SOM calculator
  category: research
  tags: "Founders, Sales Leaders, Marketing, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "tam sam som calculator, bottom up market sizing, b2b market size, claude tam skill, total addressable market"
  inputs: "ICP and segments, Pricing and average deal size, Account counts per segment"
  outputs: "Bottom-up TAM SAM SOM, Assumption table, Accounts per segment, Coverage check"
---

Use this when someone asks "how big is the market?" or "do we have enough accounts?". It produces a bottom-up size that survives questions, because every number traces to a count or a price.

## Inputs

- ICP and the segments you sell to.
- Pricing and the average first-year contract value per segment.
- Account counts per segment from a company database, industry registry or association data. Estimates are acceptable if labelled.

## The play

### 1. Count accounts, do not quote reports
Top-down numbers ("the sales software market is $X billion") cannot be worked and rarely survive diligence. Start from countable companies: headcount band × industry × region.

### 2. Define the three layers
- **TAM**: every account that could use the product at full price, globally.
- **SAM**: accounts you can serve today: regions, languages, integrations and segments you support.
- **SOM**: accounts you can realistically win in 3 years given team size, win rates and sales capacity.

### 3. Price each segment
Accounts × annual contract value. Use real deal data per segment; a blended average hides that enterprise accounts are 10x the value and 3x the cycle length.

### 4. Pressure-test SOM with capacity
SOM must be reachable by the go-to-market you have or plan to fund. Capacity check: reps × accounts each can work per year × win rate. If capacity reaches 400 wins and SOM says 4,000, SOM is wrong. Read [references/sizing-worked-example.md](references/sizing-worked-example.md) for the full table.

### 5. Check outbound coverage
Divide SAM accounts by the number of reps and by contacts touched per rep per quarter. If a team will exhaust its SAM in under 4 quarters, flag it: list fatigue is coming and the ICP needs widening or new channels.

## Output format

```
Segment table: segment | accounts | ACV | TAM $ | in SAM? | SOM share | SOM $
Totals: TAM $X (N accounts) | SAM $Y (N) | SOM $Z (N) in 3 years
Assumptions: <each with source or "estimate">
Capacity check: <reps x accounts x win rate = wins/year>
Coverage: <quarters until SAM is fully touched at current volume>
Biggest uncertainty: <one line + how to reduce it>
```

## What good looks like

- Every number in the deck can be traced to a row in the assumption table.
- SOM is constrained by capacity, not by ambition. "1% of a huge market" is the classic red flag investors look for.
- Segments are separated, because the decision the sizing supports is usually "which segment first".
- The best version ends with an account list size, not just a dollar figure, so sales can act on it.

## Rules

- MUST build bottom-up from account counts and prices.
- MUST label every estimate as an estimate.
- NEVER present a top-down analyst figure as your TAM without the bottom-up check.
- NEVER let SOM exceed what the sales capacity check supports.

## Example prompts

- "Size the market for our payroll tool for restaurant groups in the US and UK."
- "Build TAM, SAM and SOM for our seed deck, bottom-up, with every assumption shown."
- "We have 6 SDRs. Do we have enough accounts in our SAM for the next two years?"
