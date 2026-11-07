---
name: prospect-research-brief
description: "Use this skill when you need to research a specific person before reaching out or meeting them: \"look up this prospect\", \"what do I say to Jane\", \"find a personalised first line\". Reads the person's role, tenure, public posts, talks, career moves and company context, and produces a short brief with what they care about, what they are measured on, conversation hooks with sources, and a personalised opener for email and LinkedIn. For SDRs, AEs, founders and recruiters doing B2B outreach."
license: MIT
metadata:
  title: Prospect research brief
  category: research
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "prospect research, research a lead before outreach, personalized outreach research, claude prospect research skill, linkedin prospect research"
  inputs: "Person name and company, LinkedIn profile or public links, Your offer"
  outputs: "Person brief, Sourced hooks, Email opener, LinkedIn opener"
---

Use this for one person you are about to contact or meet. It produces a brief a rep can read in 60 seconds and a first line that proves the message was written for them.

## Inputs

- Name, company and title, plus a profile link if available.
- Your offer and the persona this person maps to.
- Any CRM history with this person or their company.

## The play

### 1. Confirm the person
Check they still work at the company and in the role. Roughly one in five B2B contacts changes jobs each year; a brief about the wrong job is wasted.

### 2. Gather in this order
1. Their own words: posts, comments, articles, podcast or event appearances from the last 6 months.
2. Career path: previous companies and roles, tenure in this role. A person 60 days into a role behaves differently from one 4 years in.
3. Company context: one or two triggers from the account level that land on their desk.
4. Shared ground: same former employer, same community, same school, a mutual customer. Use only if real and relevant.

### 3. Rank the hooks
Score each hook on two questions: is it specific to this person, and does it connect to the problem you solve? Keep only hooks that pass both. Read [references/hook-ranking.md](references/hook-ranking.md) for the ranking grid and examples of strong and weak hooks.

### 4. Write the openers
One for email, one for LinkedIn. One or two sentences each, built from the strongest hook, ending in a natural bridge to the problem, not to your product.

## Output format

```
Person: <name> - <title> at <company> - <tenure in role>
Confirmed current: yes/no (source)
Measured on: <likely metrics for the role>
What they talk about: <2-3 themes with links>
Hooks (ranked):
  1. <hook> - <source> - <why it connects>
  2. ...
Email opener: <1-2 sentences>
LinkedIn opener: <1-2 sentences, more conversational>
Avoid: <topics or claims to stay away from>
```

## What good looks like

- The opener could not be sent to anyone else. Swap the name and it breaks.
- It references their thinking, not their resume. "Loved your post" is weak; "your point that SDR ramp is a data problem, not a training problem" is strong.
- When nothing specific exists, the brief says so and falls back to a role-and-trigger opener instead of inventing intimacy.
- The common mistake is personalising on trivia (alma mater, hometown, a sports team) that has nothing to do with the reason for the message.

## Rules

- MUST confirm the person's current role before writing.
- MUST attach a source to every hook.
- NEVER use personal life details: family, health, location history, photos.
- NEVER claim to have read or watched something you did not.
- NEVER mention tracking data such as profile views or website visits in the opener.

## Example prompts

- "Research Priya Shah, VP Revenue at Lumen. Write an email and a LinkedIn opener."
- "I meet Tom Becker tomorrow. Give me a 60-second brief."
- "Find a real hook for each of these 15 prospects, or tell me when there isn't one."
