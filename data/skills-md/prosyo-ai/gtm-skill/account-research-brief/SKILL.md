---
name: account-research-brief
description: "Use this skill when you need to research a target company before outreach, a first call or an account plan: \"research this account\", \"what should I know about Acme before the call\", \"find a reason to reach out\". Produces a one-page account brief with what the company does, current priorities, recent trigger events, likely pains tied to your offer, the people to contact and three specific outreach angles, each with its source. Built for SDRs, AEs and founders doing B2B sales."
license: MIT
metadata:
  title: Account research brief
  category: research
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "account research template, company research for sales, pre-call research, claude account research skill, account brief"
  inputs: "Company name or domain, Your offer and ICP, CRM history if any"
  outputs: "One-page account brief, Trigger events with sources, Three outreach angles, Contacts to target"
---

Use this before the first touch on a Tier 1 account or before any first call. It produces a one-page brief that answers one question: why would this company care about us this quarter?

## Inputs

- Company name and domain.
- Your offer and ICP, so research stays relevant.
- What the CRM already knows: past conversations, open or lost deals, current customers in the same group.

## The play

### 1. Check history first
Search the CRM before the web. A lost deal from last year, an existing customer in a sister company or an unsubscribed contact changes the whole approach.

### 2. Read the primary sources, in this order
1. The company's own site: homepage claim, pricing page, careers page, newsroom.
2. Job listings: the clearest public signal of priorities, budgets and tools in use.
3. Leadership posts and interviews from the last six months.
4. Press releases, funding announcements, earnings notes for public companies.
5. Customer reviews of their product: the problems their customers complain about often become their priorities.

Stop when the brief is complete. Thirty minutes of research for a Tier 1 account, five for Tier 2.

### 3. Pick the triggers that matter
A trigger is a change that creates urgency: a new leader, funding, expansion, a hiring wave, a launch, a regulation, a bad quarter. Keep only triggers from the last 6 months and only those that connect to your offer. Read [references/trigger-library.md](references/trigger-library.md) for the trigger list with suggested angles.

### 4. Connect triggers to pains
Write each as "Because <trigger>, they probably <pain>, which we solve by <outcome>." If you cannot fill all three parts, it is trivia, not an angle.

### 5. Name the people
Economic buyer, likely champion and one alternate. Include title, tenure and anything they have said publicly about the problem.

## Output format

```
Account: <name> (<domain>)  |  Fit: Tier 1/2/3  |  CRM history: <one line>
What they do: <one sentence in plain words>
Priorities this year: <2-3 bullets, each with source>
Triggers (last 6 months): <date - event - source>
Likely pains: <2-3, each tied to a trigger or evidence>
People: <name - title - why them>
Angles:
  1. <angle> - opener idea - source
  2. ...
  3. ...
Risks: <reasons this might be a bad fit or bad timing>
```

## What good looks like

- Every angle has a dated source. A brief full of unsourced claims is worse than no brief.
- The angles are about the prospect's situation, not your features.
- The best researchers notice what is missing: no sales leader on the team page, a pricing page that changed, a product line that quietly disappeared.
- Risks are listed. A brief that only argues for outreach is a sales pitch to yourself.
- The common mistake is summarising the company's About page. That tells a rep nothing they could not guess.

## Rules

- MUST check CRM history before external research.
- MUST date and source every trigger and angle.
- NEVER treat information older than 12 months as a current trigger.
- NEVER use personal information unrelated to the person's work.

## Example prompts

- "Research northwind.com before my call on Thursday. We sell warehouse scheduling software."
- "Give me an account brief and three angles for Acme Health. Tier 1, VP Operations is the buyer."
- "Research these 10 accounts and rank them by how timely outreach would be."
