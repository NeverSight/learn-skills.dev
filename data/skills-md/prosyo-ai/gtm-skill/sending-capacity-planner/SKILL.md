---
name: sending-capacity-planner
description: "Use this skill when you need to know how many mailboxes, domains and LinkedIn accounts a meeting target requires, or how much a team can safely send: \"how many inboxes do I need\", \"plan our sending capacity\", \"can we hit 40 meetings a month\". Works backwards from the meeting goal through reply and conversion rates to contacts, touches and daily sends, then sizes email and LinkedIn infrastructure inside safe limits, with cost, ramp time and the bottleneck to fix first."
license: MIT
metadata:
  title: Sending capacity planner
  category: deliverability
  tags: "RevOps, Founders, Sales Leaders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "how many inboxes for cold email, cold email capacity planning, sending volume calculator, claude sending capacity skill, outbound infrastructure planning"
  inputs: "Meeting goal, Current conversion rates, Channels and limits"
  outputs: "Contacts and sends needed, Mailboxes domains and accounts needed, Ramp timeline, Bottleneck"
---

Use this when a target meets the limits of safe sending. It answers whether the goal is reachable, what infrastructure it needs, and how long until it runs at full speed.

## Inputs

- Monthly meeting goal.
- Conversion rates from recent campaigns (or the defaults below, labelled as assumptions).
- Channels in use and per-account safe limits.

## The play

### 1. Work backwards
```
Meetings needed per month: M
÷ meeting rate from positive replies (default 50%)  = positive replies
÷ positive reply rate per contact (default 1.5%)    = contacts per month
× touches per contact (email steps)                 = emails per month
÷ working days (21)                                 = emails per day
```

Example: 40 meetings ÷ 0.5 = 80 positive replies ÷ 0.015 = 5,333 contacts × 4 emails = 21,333 emails a month ÷ 21 = about 1,016 emails a day.

### 2. Size email infrastructure
Mailboxes = daily emails ÷ 30 (a conservative per-mailbox cold volume). Domains = mailboxes ÷ 3. Add 20% spare.
Example: 1,016 ÷ 30 = 34 mailboxes → 41 with spare, across about 14 domains.

### 3. Size LinkedIn
Per account: about 15-25 invitations a day, so roughly 100 a week. If LinkedIn carries part of the load, divide contacts between channels and size accounts accordingly. Each account must belong to a real person on the team.

### 4. Check the list can feed it
5,333 new contacts a month is about 64,000 a year. Compare with the SAM: if the ICP has 20,000 reachable contacts, the plan exhausts it in four months. That is the real bottleneck, and the fix is better conversion, not more mailboxes.

### 5. Show ramp and cost
New mailboxes need 4-6 weeks to reach full volume. Show month by month capacity and the monthly cost of domains and mailboxes.

### 6. Name the bottleneck
Usually one of: list size (SAM), reply rate (copy and targeting), meeting conversion (reply handling speed), or infrastructure. Raising positive reply rate from 1.5% to 3% halves every number above.

## Output format

```
Goal: M meetings/month
Funnel: contacts N → positive replies N → meetings M (rates used, assumed or measured)
Email: N/day → N mailboxes, N domains (incl. spare)
LinkedIn: N accounts (if used)
List check: N contacts/month vs SAM N → months of runway
Ramp: month 1 X%, month 2 Y%, full from week 6
Bottleneck: <one thing to fix first>
```

## What good looks like

- Every rate is labelled measured or assumed.
- The plan checks list supply, not only sending capacity.
- The common mistake is solving a 0.5% reply rate with 50 more mailboxes; volume multiplies whatever the conversion is, including burned contacts.

## Rules

- MUST use conservative per-mailbox and per-account limits.
- MUST check the plan against the size of the reachable market.
- NEVER plan LinkedIn capacity on fake or shared profiles.

## Example prompts

- "We need 30 meetings a month from outbound. How many mailboxes and LinkedIn accounts?"
- "Here are our real conversion rates. Is 60 meetings a month realistic?"
- "Plan our sending capacity for next quarter and tell me the bottleneck."
