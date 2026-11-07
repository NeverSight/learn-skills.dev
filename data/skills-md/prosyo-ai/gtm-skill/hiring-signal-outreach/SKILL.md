---
name: hiring-signal-outreach
description: "Use this skill when a target company is hiring for roles your product supports or replaces: \"they are hiring SDRs\", \"use job postings as a buying signal\", \"write outreach based on their job listing\". Reads the job listing for priorities, tools, team size and pain, decides whether the hire means need for your product, picks the right contact (usually the hiring manager), and writes outreach that helps the new hire succeed rather than threatening the role. Includes a scoring rule for which listings are worth acting on."
license: MIT
metadata:
  title: Hiring signal outreach
  category: signals
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "job posting buying signal, hiring signal outreach, outreach based on job listings, claude hiring signal skill, job change and hiring intent"
  inputs: "Job listing text or link, Account fit, Your offer"
  outputs: "Signal verdict, Pain map from the listing, Contact choice, Outreach messages"
---

Use this when a job listing at a target account touches the problem you solve. A company paying to hire for a problem has budget and urgency; the listing tells you what they think the problem is in their own words.

## Inputs

- The job listing text.
- Account fit and tier.
- Your offer and the roles it supports.

## The play

### 1. Read the listing like a brief
Extract: the team the role joins and its size, what the person will own, the tools named, metrics they will be measured on, the phrases that reveal pain ("build from scratch", "clean up", "scale from 10 to 50"), and seniority.

### 2. Decide what the hire means
| Listing type | Meaning | Worth acting? |
| --- | --- | --- |
| First hire in a function | Building the process from zero | Yes: strong |
| Several roles in one team at once | Scaling fast, process strain | Yes: strong |
| Leader for an existing team | Change is coming | Yes: time it to their start |
| Single backfill | Replacing someone | Weak, unless the listing reveals new scope |
| Role your product partly automates | Budget exists; handle with care | Yes, with a support angle |

### 3. Pick the contact
The hiring manager (the role's future boss) is almost always right. Not HR, not recruiting, and never the new hire before they start.

### 4. Write the angle: help, not replace
Frame the product as what makes the new team productive faster, or what covers the gap until the hire lands. "You don't need to hire" insults the plan they already approved.

### 5. Time it
Within 7 days of the listing appearing, while the problem is top of mind. A second touch when the role closes ("as your new team starts...").

## Message pattern

> Subject: the new SDR team
>
> Hi Dana, saw Lumen is hiring four SDRs and the listing mentions building outbound "from the ground up". The part that usually slows new teams most is not the calling, it is getting a clean, researched list in front of each rep every morning.
>
> We help teams like Northwind's get new reps booking in their second week. Worth a look before they start?

## What good looks like

- The opener quotes or closely paraphrases the listing, proving it was read.
- The angle supports the hiring plan.
- Listings are scored, and backfills are mostly ignored.
- The common mistake is "I noticed you're hiring" followed by a generic pitch, which every vendor in the category sends the same week.

## Rules

- MUST contact the hiring manager, not recruiting or the candidate.
- MUST act within the listing's lifetime.
- NEVER suggest the company should not make the hire.
- NEVER contact candidates or new hires to sell to their future employer.

## Example prompts

- "Here's a job listing for a RevOps manager at Contoso. Is it a signal for us, and what should we send?"
- "Write outreach for these 20 accounts hiring SDRs this month."
- "Score these job listings and tell me which to act on."
