---
name: buyer-persona-builder
description: "Use this skill when you need B2B buyer personas that sales and marketing will actually use: before writing outreach to a new title, when messaging feels generic, or when a deal stalls because the wrong person is engaged. Builds a persona per role in the buying committee with goals, pains in their own words, what they are measured on, objections, trusted sources and the message angle that works, plus a do-not-say list. Covers economic buyers, champions, users and blockers."
license: MIT
metadata:
  title: Buyer persona builder
  category: research
  tags: "Marketing, Sales, Founders, SDR"
  author: prosyo
  version: "1.0.0"
  keywords: "b2b buyer persona template, buyer persona generator, sales persona, claude persona skill, buying committee personas"
  inputs: "Target job titles, Call notes or interviews, Your product and ICP"
  outputs: "One persona card per role, Message angles, Do-not-say list"
---

Use this before writing to a role you have not sold to before, or when outreach reads like it was written for nobody in particular. It produces one persona card per role that changes what a rep writes.

## Inputs

- The job titles in the buying committee, or the deal type so you can propose them.
- Raw evidence: call recordings or notes, won-deal emails, support tickets, reviews, job listings for the role.
- The ICP and the product's core job.

## The play

### 1. Separate the roles
A deal usually has four: the **economic buyer** who signs, the **champion** who feels the pain and pushes, **users** who live in the tool, and the **blocker** (security, finance, IT, legal) who can stop it. Build a card per role. One blended persona produces messages that fit no one.

### 2. Start from what they are measured on
The fastest route to relevance is the number on their scorecard. A VP Sales is measured on bookings and forecast accuracy; a RevOps lead on data quality and tool cost; a founder on runway and growth rate. Pains connect to these numbers or they do not matter.

### 3. Use their words
Mine the evidence for exact phrases. Job listings are the most underrated source: they spell out the problems the company is paying to fix and the tools in use.

### 4. Map objections and proof
For each role, list the top three objections and the proof that answers each one: a customer story, a number, a demo moment, a security document.

### 5. Find the angle
One sentence per role: the reason this person would take a meeting this quarter.

## Persona card format

```
Role: <title variants>            Type: economic buyer | champion | user | blocker
Measured on: <2-3 metrics>
Goals this year: <2-3>
Pains (their words): <3 quotes or close paraphrases, with source>
Triggers: <events that make the pain urgent>
Objections → proof: <3 pairs>
Trusted sources: <communities, newsletters, peers, analysts>
Angle: <one sentence>
Do not say: <phrases that make them tune out>
```

Read [references/persona-examples.md](references/persona-examples.md) for two complete cards and the most common do-not-say phrases by role.

## What good looks like

- A rep reading the card can write a different first line for a VP Sales and a RevOps manager at the same company.
- Pains are quoted or traceable, not imagined. "Struggles with efficiency" is a sign the evidence step was skipped.
- The blocker has a card. Deals die in security review far more often than in the first call.
- The do-not-say list is specific: "revolutionary", "synergy" and "quick question" are on most lists for a reason.

## Rules

- MUST build separate cards for the economic buyer and the champion.
- MUST tie each pain to a metric the role is measured on.
- NEVER invent quotes; label paraphrases and inferred pains as such.
- NEVER use demographic stereotypes (age, gender, personal life) in a B2B persona.

## Example prompts

- "Build personas for selling our SOC 2 automation tool: CTO, Head of Security, and the finance approver."
- "Here are 12 call transcripts with heads of RevOps. Turn them into a persona card."
- "Our champion persona feels generic. Rewrite it using these job listings."
