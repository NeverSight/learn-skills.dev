---
name: renewal-risk-review
description: "Use this skill when renewals are coming up and you need to know which customers might not renew: \"renewal risk review\", \"which accounts will churn\", \"prepare for renewals next quarter\", \"customer health check before renewal\". Scores each upcoming renewal on usage, outcomes, relationships, support and commercial signals, flags at-risk accounts with evidence, and writes a save plan and the value-review outreach for each. Produces a renewal risk table and a 90-day action plan."
license: MIT
metadata:
  title: Renewal risk review
  category: abm-expansion
  tags: "Customer Success, Sales Leaders, Founders, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "renewal risk assessment, customer health score, churn risk review, claude renewal skill, saas renewal playbook"
  inputs: "Renewals due in the next 120 days, Usage and support data, Contacts and recent conversations"
  outputs: "Renewal risk table, Evidence per account, Save plans, Value-review messages"
---

Use this 90 to 120 days before renewals. Most churn is decided months before the renewal date; the review finds it while there is still time to change it.

## Inputs

- Renewals due in the next 120 days: account, value, date, plan.
- Usage: active users against paid seats, trend over 90 days, key feature adoption.
- Outcomes: what the customer said success looks like, and whether it happened.
- Relationships: champion status, executive sponsor, last meaningful conversation.
- Support and commercial signals: open escalations, late payments, price complaints, requests to downgrade.

## The play

### 1. Score five dimensions
| Dimension | Healthy | Risk |
| --- | --- | --- |
| Usage | Active users 70%+ of seats, stable or rising | Under 40% or falling 20%+ in 90 days |
| Outcomes | A measurable result the customer agrees on | No agreed result, or "we're not sure it's working" |
| Relationships | Engaged champion plus a sponsor | Champion left or silent 60+ days |
| Support | Issues resolved, no open escalations | Repeated issues, open escalation |
| Commercial | On-time payments, no price pushback | Downgrade requests, procurement review, budget cuts |

Each dimension: green 0, amber 1, red 2. Total 0-2 healthy, 3-5 watch, 6+ at risk. Any red on relationships or outcomes makes an account at least "watch".

### 2. Write the evidence
Each score cites a fact: "11 of 40 seats active, down from 26", "champion Priya left in August". No evidence, no score.

### 3. Plan the save
| Main risk | Save move |
| --- | --- |
| Low usage | Re-onboarding for the team that matters most, with a 30-day target |
| No proven outcome | Value review with numbers before any renewal talk |
| Lost champion | Find and onboard the new owner; executive-to-executive check-in |
| Support pain | Fix plan with dates, owned by a named person |
| Budget | Right-size the plan before they ask; protect the core use case |

### 4. Open with a value review
Lead with what the customer got, not the renewal. Share usage, results, and what similar customers do next; ask what would make next year a clear yes.

### 5. Review weekly
Move accounts between bands as evidence changes. Escalate any at-risk account above a value threshold to a leader within the week.

## What good looks like

- Every risk score is backed by a fact a manager can check.
- At-risk accounts get a save plan 90 days out, not a discount 9 days out.
- The value review happens before the renewal conversation.
- The common mistake is a health score built from logins alone, which misses the account whose one power user logs in daily while the budget owner has already decided to cancel.

## Rules

- MUST cite evidence for every score.
- MUST run the review at least 90 days before renewal.
- NEVER lead a renewal conversation with a discount.
- NEVER mark an account healthy when its champion has left and no new owner is engaged.

## Example prompts

- "Here are our 40 renewals for next quarter with usage data. Which are at risk and what do we do?"
- "Build a renewal risk scorecard our CS team can run monthly."
- "Write a value-review email for an account whose usage dropped 30%."
