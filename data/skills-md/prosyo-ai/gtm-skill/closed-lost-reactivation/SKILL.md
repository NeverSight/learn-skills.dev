---
name: closed-lost-reactivation
description: "Use this skill when you want to revive closed-lost deals and old opportunities: \"re-engage lost deals\", \"win back closed lost opportunities\", \"reactivation campaign\", \"which lost deals should we try again\". Filters lost deals by reason and time since loss, checks for new triggers, picks the ones worth reopening, and writes reactivation messages that reference what changed (on their side or yours) instead of repeating the old pitch. Often the cheapest pipeline a team can create."
license: MIT
metadata:
  title: Closed-lost reactivation
  category: deals
  tags: "Sales, SDR, Founders, Sales Leaders"
  author: prosyo
  version: "1.0.0"
  keywords: "closed lost reactivation, win back lost deals email, re engage old opportunities, claude closed lost skill, lost deal follow up"
  inputs: "Closed-lost deals with reasons and dates, What changed since, Current triggers"
  outputs: "Prioritised reactivation list, What changed per deal, Reactivation messages"
---

Use this when pipeline is thin or each quarter. Lost deals already know you, already have the problem and often lost on timing; reopening them costs far less than finding new ones.

## Inputs

- Closed-lost deals from the last 3-24 months: reason, stage lost, contacts, notes, competitor chosen.
- What changed on your side since: product releases, new pricing or packages, new proof.
- Current triggers at those accounts: new leaders, funding, hiring, the competitor's contract term ending.

## The play

### 1. Filter by reason and timing
| Lost reason | Reopen when | Angle |
| --- | --- | --- |
| Timing / no priority | 3-6 months later, or a trigger fires | "Is it a priority now?" |
| Budget | New fiscal year or funding | New budget, phasing options |
| Chose a competitor | 9-12 months later, before their renewal | Check-in on how it's going |
| Product gap | When the gap ships | "You asked for X; it's live" |
| No decision / went dark | 3-4 months later | New proof, fresh angle |
| Bad fit | Only if their situation changed | Usually leave it |

### 2. Score each deal
Priority = how far it got (later stage = higher) + new trigger present + the lost reason has been resolved + contacts still in role.

### 3. Lead with what changed
The message must answer "why talk again now?". Something changed: their situation (new leader, growth), your product (the missing feature), or the market (a new requirement).

### 4. Pick the contact
The original champion if still there; if they left, the new person in the role (and run a job-change play on the champion).

### 5. Write short and honest
> Hi Priya, when we spoke in March, multi-entity support was the deal-breaker. It went live last month, and Contoso is running four entities on it. Worth a fresh look, or has the team moved on?

## What good looks like

- Every message names a specific change.
- Deals lost to a competitor are approached near the end of the competitor's likely contract term, not a month after signing.
- The common mistake is re-sending the original pitch with "circling back" on top, which reminds the buyer why they said no.

## Rules

- MUST name what changed in every reactivation message.
- MUST check contacts are still in role and have not opted out.
- NEVER disparage the competitor they chose.
- NEVER misstate the reason they gave for saying no.

## Example prompts

- "Here are 120 closed-lost deals from the last 18 months. Which should we reopen and with what?"
- "We just shipped SSO. Write messages to every deal we lost because of it."
- "Plan a quarterly closed-lost reactivation play."
