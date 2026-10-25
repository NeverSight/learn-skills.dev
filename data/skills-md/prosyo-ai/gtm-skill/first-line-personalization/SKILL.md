---
name: first-line-personalization
description: "Use this skill when you need personalised first lines (icebreakers) for cold emails or LinkedIn messages at scale: \"write personalised openers for this list\", \"add a custom first line for each lead\", \"make my outreach feel 1:1\". Researches each prospect for a real, relevant hook, writes a one or two sentence opener that bridges to the email's problem, grades each line, and falls back to an honest role-based line when nothing specific exists. Never invents details."
license: MIT
metadata:
  title: First line personalization
  category: cold-email
  tags: "SDR, Founders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "personalized first lines, cold email icebreakers, ai personalization at scale, claude personalization skill, personalized opening lines"
  inputs: "Lead list with names and companies, The email the line opens, Research sources"
  outputs: "One opener per lead, Source per line, Quality grade, Fallback lines"
---

Use this to add a personal opener to each contact on a list. The line proves the email was written for the reader and leads naturally into the problem the email is about.

## Inputs

- The list: name, title, company, profile link, domain.
- The email the line will open, so the line can bridge into it.
- Allowed sources: company site, news, job listings, the person's public posts and talks.

## The play

### 1. Research each lead quickly
Spend 1-3 minutes per lead. Look for, in order: something they said or wrote, a change in their role or team, a company trigger, a specific detail of how their company works.

### 2. Write the line with a bridge
Formula: **specific observation + why it connects to the email's problem**. The second half is what makes personalization work; an observation with no bridge is a compliment, and compliments get ignored.

- No bridge: "Loved your podcast episode on hiring."
- With bridge: "Your point on the podcast that hiring SDRs is easy and ramping them is hard is exactly the problem below."

### 3. Grade every line
| Grade | Meaning |
| --- | --- |
| A | Specific to the person and connected to the problem |
| B | Specific to the company and connected |
| C | Role or industry level, honest and relevant (fallback) |
| Fail | Invented, generic flattery, or unrelated trivia; never ship |

Aim for A or B on Tier 1 contacts; C is acceptable for Tier 3.

### 4. Write fallbacks, never fiction
When research finds nothing, write a C line about the role at their company's stage. A sincere role-level line outperforms a fake personal one, and it never gets caught.

### 5. Check the merge
The line must read naturally after "Hi {first name}," and before the email's second sentence. Check 5 rendered examples.

## Output format

```
name | company | first line | grade | source link | bridge used
```

Plus counts per grade and the leads where research found nothing.

## What good looks like

- Every A and B line has a source link a reviewer can click.
- Lines vary in structure; 200 lines starting "I saw that..." read as automation.
- The common mistake is personalising on trivia (school, hometown, a vacation photo) that has nothing to do with the email.

## Rules

- MUST attach a source to every A and B line.
- MUST use a fallback line rather than invent a detail.
- NEVER mention personal life, family, health or appearance.
- NEVER claim to have read, watched or listened to something you did not.
- NEVER reference profile views, website visits or other tracking.

## Example prompts

- "Write personalised first lines for these 80 leads. The email is about cutting SDR ramp time."
- "Grade the first lines in this campaign and rewrite the C and Fail ones."
- "Give me fallback openers for Heads of Operations when there's no research."
