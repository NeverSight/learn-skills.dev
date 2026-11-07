---
name: funding-signal-outreach
description: "Use this skill when a target company announces a funding round, acquisition or major investment and you want to reach out: \"they just raised a Series B\", \"write a funding congratulations email that is not generic\", \"use funding as a buying signal\". Reads the announcement for what the money is for, maps it to the bottleneck your product removes, picks the right person and timing, and writes outreach that stands out from the flood of congratulation emails every funded company receives."
license: MIT
metadata:
  title: Funding signal outreach
  category: signals
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "funding announcement outreach, series a outreach email, recently funded companies, claude funding signal skill, congratulations on funding email"
  inputs: "Funding announcement, Account fit, Your offer and proof"
  outputs: "Use-of-funds map, Contact and timing, Outreach sequence"
---

Use this when a target account raises money. Funded companies have budget and pressure to grow, but they also get dozens of identical "congrats on the raise" emails in the first week. The job is to be relevant, not first.

## Inputs

- The announcement: amount, stage, investors, and especially what the money is for.
- Account fit and tier.
- Your offer and the proof points that match their stage.

## The play

### 1. Read the use of funds
Announcements and founder posts usually say it plainly: "expand into Europe", "double the sales team", "build out enterprise", "invest in AI". Each stated goal implies bottlenecks. Map one to your offer.

| Stated goal | Likely bottleneck | Who owns it |
| --- | --- | --- |
| Grow the sales team | Ramp time, pipeline per rep, tooling | VP Sales, Head of SDR |
| Expand to a new region | Local pipeline from zero, compliance, hiring | GM of region, CRO |
| Move upmarket | Security reviews, multi-threading, longer cycles | CRO, Head of Security |
| Product investment | Hiring engineers, infrastructure cost | CTO, VP Engineering |

### 2. Pick the person
Not the CEO of a 200-person company; the leader who owns the bottleneck. For companies under 30 people, the founder is right.

### 3. Time it
Skip week one. Weeks 2-6 are when plans turn into hiring, budgets and tool decisions, and the inbox has calmed down.

### 4. Write about their plan, not the raise
One line acknowledges the news; the rest is about the bottleneck the plan creates and a peer who got past it.

## Sequence

1. **Email, week 2-3**: plan → bottleneck → proof → soft question.
2. **LinkedIn, 3 days later**: short connection note referencing the same theme, no pitch.
3. **Email, week 4-5**: a useful asset for the stage (a hiring plan template, a benchmark), no ask.
4. **Email, week 6**: direct ask for 20 minutes, or close the loop politely.

Example first email:

> Subject: doubling the sales team
>
> Hi Sam, the Series B post said the plan is to double the sales team this year. The teams we see do that well usually hit a pipeline-per-rep problem around month four, when new reps have no warm accounts to work.
>
> Northwind solved it by giving each new rep a researched list on day one; their ramp dropped from 5 months to 3. Is that on your plan already?

## What good looks like

- The word "congrats" is at most one clause, never the whole message.
- The message names the stated goal from the announcement.
- The proof point is a company at the same stage.
- The common mistake is selling to the investor-announced vision instead of the operational problem a specific leader now owns.

## Rules

- MUST read what the funds are for before writing.
- MUST wait at least one week after the announcement.
- NEVER imply the company now "can afford" you.
- NEVER claim to be excited for them in a way that implies a relationship that does not exist.

## Example prompts

- "Fabrikam raised a $30M Series B to expand into Europe. Write a 4-step sequence to their CRO."
- "Here are 15 companies that raised this month. Who should we contact and with what angle?"
- "Rewrite my funding email so it doesn't sound like everyone else's."
