---
name: proposal-follow-up
description: "Use this skill when a proposal or quote has been sent and the buyer has gone quiet or is stalling: \"follow up on my proposal\", \"they have the quote but no decision\", \"proposal stuck in review\". Diagnoses where the deal is really stuck (economic buyer, budget, competitor, priority, procurement, champion), writes a follow-up sequence that addresses that cause with value instead of nagging, and sets the point to escalate or close the opportunity."
license: MIT
metadata:
  title: Proposal follow-up
  category: deals
  tags: "Sales, Founders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "proposal follow up email, follow up after sending quote, stalled deal email, claude proposal follow up skill, sales proposal no response"
  inputs: "Proposal and date sent, Deal notes, Stakeholders"
  outputs: "Stall diagnosis, Follow-up sequence, Escalation and close plan"
---

Use this when a proposal sits unanswered. Silence after a proposal almost always has a specific cause; following up on the cause works better than asking "any updates?".

## Inputs

- The proposal: what, how much, when sent, any deadline in it.
- Deal notes: who saw it, who decides, competitors, what was promised.
- Stakeholders and the champion's last message.

## The play

### 1. Diagnose the stall
| Clue | Likely cause | Follow-up angle |
| --- | --- | --- |
| Champion silent, was engaged before | Lost internal fight or priority shift | Ask directly, offer help with the internal case |
| "Reviewing with the team" for 2+ weeks | Economic buyer not convinced or not involved | Offer a short call with the economic buyer |
| Questions about price only | Budget gap or competitor quote | Options: phasing, packaging, terms |
| Procurement or legal mentioned | Paper process | Offer documents and pre-approved terms |
| Nothing since the demo went poorly | Fit concern | Address the concern or offer a focused trial |

### 2. Sequence (over 2-3 weeks)
1. **Day 3-5**: value plus a question about the cause: a one-page business case built from their numbers, and "What questions came up when you shared it?"
2. **Day 8-10**: address the likely blocker: options for price, security documents, or an offer to join the internal meeting.
3. **Day 14-16**: multi-thread: a short note to another stakeholder you have met, adding value, not going around the champion.
4. **Day 21**: honest check-in with a multiple-choice question, or close the opportunity.

### 3. Escalate with care
Executive-to-executive outreach works when there was real engagement and the deal is meaningful. Frame it as a check on how the evaluation is going, never as pressure.

### 4. Decide when to close
If three touches over three weeks get nothing, mark the deal lost to "no decision" and move to nurture. An honest pipeline beats a hopeful one.

## Example

> Hi Priya, I put your numbers into a one-page case for the CFO: 5 days saved a month, about $480k a year at your volumes, against a $60k cost. Feel free to edit it before sharing. What questions came up when you discussed the proposal with the team?

## What good looks like

- Every follow-up contains something the buyer can use internally.
- The diagnosis drives the angle; price follow-ups do not go to a champion whose problem is the economic buyer.
- The common mistake is "Just checking in on the proposal" five times, then an unrequested discount.

## Rules

- MUST diagnose the stall before writing.
- MUST keep the champion informed before contacting other stakeholders.
- NEVER offer an unrequested discount as a follow-up tactic.
- NEVER invent an expiring offer.

## Example prompts

- "Sent the proposal 12 days ago, no reply from our champion. Diagnose and write the follow-ups."
- "They said 'reviewing internally' three weeks ago. What now?"
- "Build a business case one-pager from our discovery numbers to send as a follow-up."
