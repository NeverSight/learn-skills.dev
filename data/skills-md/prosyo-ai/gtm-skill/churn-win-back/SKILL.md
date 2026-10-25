---
name: churn-win-back
description: "Use this skill when you want former customers back: \"win back churned customers\", \"re-engage cancelled accounts\", \"churn win-back campaign\", \"which lost customers should we call\". Sorts churned accounts by why and when they left, picks the ones worth winning back, finds what changed since (product, pricing, their situation), and writes a short, honest win-back sequence with the right offer for each churn reason. Produces a prioritised win-back list, messages and the rules for when to leave an account alone."
license: MIT
metadata:
  title: Churn win-back
  category: abm-expansion
  tags: "Customer Success, Founders, Sales"
  author: prosyo
  version: "1.0.0"
  keywords: "win back churned customers, customer win back email, re-engage cancelled customers, claude churn win-back skill, winback campaign saas"
  inputs: "Churned accounts with reason and date, What changed since, Usage history"
  outputs: "Prioritised win-back list, Win-back sequence per churn reason, Leave-alone list"
---

Use this for customers who cancelled in the last 3 to 24 months. Former customers already know the product and the problem; the question is whether the reason they left still holds.

## Inputs

- Churned accounts: churn date, plan and value, the stated reason, who the champion was, usage in the last 90 days before churn.
- What changed since: features shipped, pricing or packaging changes, support improvements.
- Current signals at those accounts: new leaders, growth, hiring, funding.

## The play

### 1. Group by real churn reason
| Reason | Typical evidence | Win-back angle |
| --- | --- | --- |
| Missing feature | Ticket or request for it | "The thing you needed now exists" |
| Price or budget | Downgrade attempts, finance involved | New plan, smaller package, annual terms |
| Low adoption | Few active users, onboarding never finished | Guided restart, done-with-you setup |
| Champion left | Main user departed before churn | New owner, fresh onboarding |
| Switched to a competitor | Said so in the exit call | Check in near their contract renewal |
| Business change | Downsizing, pivot, acquisition | Only if the situation reversed |

### 2. Prioritise
Score each account: past value, how far they got (active users, outcomes), whether the churn reason is now fixed, and whether a new trigger exists. Start with accounts where the reason is fixed **and** a trigger fired.

### 3. Time it
- Feature or price reasons: as soon as the fix ships.
- Competitor switch: 9 to 11 months after churn, ahead of their renewal.
- Low adoption: 3 to 6 months later, with a new owner if possible.

### 4. Write short and honest
Name the reason they left, say what changed, offer one easy step back. Never pretend the relationship ended well if it did not. Read [references/win-back-messages.md](references/win-back-messages.md) for messages by churn reason.

### 5. Make returning easy
A clear path: data restored if retained, a short guided restart, a fair price. Ask what would need to be true for it to work this time.

## What good looks like

- Every message names the reason they left and the specific change.
- Accounts that churned for reasons nothing has fixed are left alone.
- Returners get an onboarding plan, so they do not churn twice for the same reason.
- The common mistake is a blanket "We miss you! Here's 20% off" email to every former customer, which ignores why they left and trains people to churn for discounts.

## Rules

- MUST check the churn reason before writing.
- MUST respect opt-outs and data-retention promises made at cancellation.
- NEVER claim a fix that has not shipped.
- NEVER discount by default; match the offer to the reason.

## Example prompts

- "Here are 85 accounts that churned last year with reasons. Who should we win back and how?"
- "We just shipped the integration 12 churned customers asked for. Write the win-back emails."
- "Plan a quarterly win-back play for customers who left for a competitor."
