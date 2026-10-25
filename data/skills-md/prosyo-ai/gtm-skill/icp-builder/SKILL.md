---
name: icp-builder
description: "Use this skill when you need to define or sharpen an ideal customer profile (ICP) for B2B sales: starting outbound, the reply rate is low, the pipeline is full of bad-fit deals, or leadership asks who we should really sell to. Analyses closed-won and closed-lost deals, finds the firmographic, technographic and situational traits that predict a win, and produces a one-page ICP with must-haves, nice-to-haves, disqualifiers and list-building filters. Works for founders with five customers and for teams with hundreds."
license: MIT
metadata:
  title: ICP builder
  category: research
  tags: "Founders, Sales Leaders, Marketing, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "ideal customer profile template, icp builder, define icp b2b, claude icp skill, icp framework"
  inputs: "Closed-won and closed-lost deals, Product and pricing, Sales cycle notes"
  outputs: "One-page ICP, Disqualifiers, List-building filters, Confidence notes"
---

Use this when the question is "who should we sell to?". It produces a one-page ICP that a rep, a marketer and a list builder can all act on the same day.

## Inputs

Ask for as much as exists, then work with what you get:

- Closed-won deals for the last 12 to 24 months: company, size, industry, region, deal value, cycle length, who signed, why they bought.
- Closed-lost and churned accounts with the reason.
- The product's core job and price range.
- If there are fewer than 10 customers: the founder's notes on the best five conversations, plus the best five failures.

## The play

### 1. Rank customers by value, not by count
Sort won deals by a blend of revenue, cycle speed and retention. The top 20% is the real ICP; the long tail is noise. A segment with many small, slow, churn-prone deals looks big on a pie chart and loses money.

### 2. Find the traits that separate winners from losers
For each trait, compare the share among top customers with the share among lost or churned ones. Traits worth keeping show a gap of at least 20 points. Look at four layers:

| Layer | Examples |
| --- | --- |
| Firmographic | Industry, headcount band, revenue band, region, business model |
| Technographic | Tools they already run, data maturity, stack that integrates with yours |
| Situational | Hiring for a role, new leader in seat, funding, expansion, a regulation deadline |
| Behavioural | How they buy: committee size, procurement, self-serve trial or demo |

Situational traits usually predict timing better than firmographics predict fit. Read [references/icp-scoring.md](references/icp-scoring.md) for the comparison table and the scoring weights.

### 3. Write the pain in the buyer's words
Pull phrases from call notes, emails and reviews. "We lose two days a month reconciling payouts" beats "operational inefficiency".

### 4. Set disqualifiers
Hard noes save more time than must-haves. Typical ones: below a headcount that can afford the price, a region you cannot serve, a tech stack you cannot integrate with, a business model where the pain does not exist.

### 5. Translate it into filters
Every trait becomes a filter a list builder can run: industry codes, headcount ranges, job titles, keywords in job listings, technologies detected. Flag traits that cannot be filtered and must be checked by research.

## Output format

```
ICP: <one-line name, e.g. "Multi-location restaurant groups, 5-50 sites">
Why they buy: <pain in their words>  |  Trigger: <what makes now the moment>
Must-haves: <3-5 traits>
Nice-to-haves: <2-4 traits that raise priority>
Disqualifiers: <3-5 hard noes>
Buyer: <title that signs>  Champion: <title that feels the pain>  Users: <who uses it>
Filters: <list-builder ready criteria>
Confidence: <high / medium / low and why: sample size, data gaps>
```

## What good looks like

- Narrow enough that a rep can name 50 target accounts from memory after reading it. "B2B SaaS companies" is not an ICP.
- It includes a trigger. Fit without timing produces polite "not right now" replies.
- Disqualifiers are as specific as the must-haves.
- The confidence note is honest: an ICP built from six customers says so and lists what to test next.
- The common mistake is describing the customers you want instead of the customers who bought, renewed and expanded.

## Rules

- MUST base every trait on deal data or explicit notes, and say which.
- MUST include at least three disqualifiers.
- NEVER mix the economic buyer and the end user into one persona.
- NEVER present a trait with fewer than five supporting accounts as proven; mark it as a hypothesis.

## Example prompts

- "Here are our last 40 closed-won and 25 closed-lost deals. Build our ICP."
- "We have 7 customers. Help me write a first ICP and tell me what to test."
- "Our reply rate dropped to 1%. Check whether our ICP is too broad."
