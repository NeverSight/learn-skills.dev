---
name: job-change-plays
description: "Use this skill when a contact changes jobs: a champion or happy user joins a new company, a new leader starts at a target account, or a key contact leaves a customer. Runs the three job-change plays: follow the champion to their new company, welcome the new leader at a target account, and protect the customer account they left. Produces the message for each with timing, who to contact and what never to say. One of the highest-converting outbound plays in B2B."
license: MIT
metadata:
  title: Job change plays
  category: signals
  tags: "Sales, SDR, Customer Success, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "job change outreach, champion tracking, follow champions to new companies, claude job change skill, new role outreach"
  inputs: "Job change alert, Relationship history, Account status"
  outputs: "Play choice, Messages with timing, Account risk note"
---

Use this whenever someone you know, or someone who matters, starts a new job. Former champions convert to meetings at several times the rate of cold contacts because trust travels with them.

## Inputs

- Who moved, from where, to where, and when.
- Your history with them: customer champion, user, lost-deal contact, never spoke.
- The status of both companies: customer, open deal, target, none.

## The play

### Play 1: Champion moved to a new company
They liked your product before, so the job is to reconnect, not to pitch.

1. **Week 1-3**: congratulate with no ask. Mention something real from working together.
2. **Day 30-60**: once they have settled in, ask how they are finding the new role and whether the problem you solved before exists there. Offer to show what changed since they last used it.
3. Check fit first: if the new company is outside the ICP, keep the relationship warm instead of selling.

### Play 2: New leader at a target account
New leaders review processes and tools in their first 90 days and want early wins.

1. **Day 14-30**: a short note on what people in their role usually prioritise early, with one useful resource. No meeting ask, or a very soft one.
2. **Day 30-60**: a specific angle tied to what they inherited, plus a peer proof point.
3. Do not congratulate a stranger on day two. Everyone else does.

### Play 3: Champion left a customer
The account is now at risk; a quarter of churn traces back to a lost champion.

1. Tell the account owner the same day.
2. Identify the next most engaged user and the new owner of the budget.
3. Offer the replacement a fresh onboarding or review, framed as help, not as protecting a renewal.
4. Run Play 1 on the departed champion as well.

Read [references/job-change-messages.md](references/job-change-messages.md) for message templates for each play and stage.

## What good looks like

- Plays run on timing, not on the alert. The day-one congratulation is the weakest message in sales.
- The champion message sounds like a person who remembers them, with a real detail from working together.
- Customer accounts get a risk flag within a day of a champion leaving.
- The common mistake is pitching a former champion in the first message, which spends the trust that made the play work.

## Rules

- MUST check the new company against the ICP before selling to a former champion.
- MUST alert the account owner when a champion leaves a customer.
- NEVER pitch in the first message to a former champion.
- NEVER mention how you found out about the move beyond public announcements.

## Example prompts

- "Maria, our champion at Contoso, just became VP Ops at Fabrikam. Write the play."
- "A new CRO started at one of our Tier 1 targets. Plan the first 60 days of outreach."
- "Our main user at Northwind left. What do we do this week?"
