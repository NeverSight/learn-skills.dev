---
name: expansion-opportunity-finder
description: "Use this skill when you want to grow revenue from existing customers: \"find upsell and cross-sell opportunities\", \"which customers are ready to expand\", \"net revenue retention plan\", \"expansion playbook\". Scores customer accounts on usage, health, growth signals and whitespace (teams, products and seats not yet bought), finds the strongest expansion opportunities with the evidence behind each, and writes the value-review outreach that opens the conversation without sounding like an upsell."
license: MIT
metadata:
  title: Expansion opportunity finder
  category: abm-expansion
  tags: "Customer Success, Sales, Founders, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "upsell cross sell opportunities, customer expansion playbook, net revenue retention, claude expansion skill, account whitespace analysis"
  inputs: "Customer list with usage and contract data, Products and pricing, Health signals"
  outputs: "Scored expansion list, Whitespace map, Evidence per account, Value-review outreach"
---

Use this quarterly or before renewals. Expansion is usually the cheapest revenue a company can win, but only from customers who are getting value; pushing more onto unhappy customers accelerates churn.

## Inputs

- Customers: plan, seats or units, contract value, renewal date.
- Usage: active users vs paid seats, feature adoption, trends.
- Health: support tickets, satisfaction scores, champion status, payment issues.
- Products and pricing: what else could they buy.

## The play

### 1. Check health first
Exclude or flag accounts with falling usage, unresolved escalations, a departed champion or payment problems. They need a save plan, not an upsell.

### 2. Score expansion signals
| Signal | Example | Weight |
| --- | --- | --- |
| Usage near limits | 90%+ of seats or volume used | High |
| Growth at the company | Hiring, funding, new locations | High |
| New team showing interest | Users from another department signing up or asking | High |
| Strong adoption of core features | Ready for an advanced tier | Medium |
| Successful outcomes documented | A result they can repeat elsewhere | Medium |
| Renewal in 60-120 days | Natural moment to resize | Timing |

### 3. Map the whitespace
Per account: which teams, regions, sites or products could use it and do not yet. Sister companies and subsidiaries count.

### 4. Open with a value review
The best expansion conversation starts with what the customer got: results so far, usage, what peers do next. The expansion idea follows from their goals, not from your quota.

> Hi Priya, it's been a year since rollout, so I put together a short review: close time down from 9 days to 4, and your team is now running reconciliation for all three entities. Two other finance teams in your group asked about it last month. Would a 30-minute review with you be useful before planning season?

### 5. Route and track
Account managers or customer success own the conversation; sales joins for new buyers. Track expansion pipeline and net revenue retention by segment.

## What good looks like

- Every opportunity has evidence: usage numbers, a growth signal, an interested team.
- Unhealthy accounts get a save plan before any expansion pitch.
- The common mistake is a blanket "upgrade now" campaign to all customers, which annoys the ones not getting value.

## Rules

- MUST check health before recommending expansion.
- MUST base opportunities on actual usage and signals.
- NEVER pressure customers with artificial limits or surprise price increases.

## Example prompts

- "Here's our customer export with usage. Who's ready to expand and why?"
- "Map whitespace across our top 30 accounts."
- "Write value-review emails for customers renewing next quarter."
