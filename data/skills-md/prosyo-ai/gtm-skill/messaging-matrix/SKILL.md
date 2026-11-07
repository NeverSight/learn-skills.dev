---
name: messaging-matrix
description: "Use this skill when one message does not fit every buyer and you need messaging by persona, industry or stage: \"build a messaging matrix\", \"tailor our pitch for each persona\", \"different messages for CFO and CTO\", \"sales messaging framework\". Maps each persona to its top pains, the outcome they care about, proof that persuades them, objections and the words to use and avoid, then writes ready-to-use lines for cold email, LinkedIn, calls and landing pages."
license: MIT
metadata:
  title: Messaging matrix
  category: positioning
  tags: "Marketing, Sales Leaders, Founders, SDR"
  author: prosyo
  version: "1.0.0"
  keywords: "messaging matrix template, persona based messaging, sales messaging framework, claude messaging matrix skill, b2b messaging by persona"
  inputs: "Value proposition, Personas, Proof points"
  outputs: "Persona by message matrix, Ready-to-use lines per channel, Words to use and avoid"
---

Use this when the same pitch goes to a CFO, a team lead and an engineer. It produces a matrix that keeps the core value proposition but changes the pain, proof and words for each reader.

## Inputs

- The core value proposition and pillars.
- Personas (economic buyer, champion, user, technical evaluator).
- Proof points, tagged by what they prove.

## The play

### 1. Build the grid
Rows are personas; columns are:

| Column | What goes in |
| --- | --- |
| Measured on | The metric they own |
| Top pain | The pain in their words |
| Outcome | The result they want |
| Pillar to lead with | Which of your pillars fits best |
| Proof | The proof point that persuades this role |
| Objection | Their most likely pushback and the answer |
| Use | Words that resonate |
| Avoid | Words that make them tune out |

### 2. Pick the lead pillar per persona
A CFO hears cost and risk; a team lead hears time and quality; an engineer hears how it works and what it touches. Same product, different first sentence.

### 3. Write the lines
Per persona: an email opener, a LinkedIn opener, a 20-second call opener and a landing page headline. Lines reuse the matrix words exactly.

### 4. Add industry or stage variants only when they change the pain
A variant earns a row when the pain or the proof genuinely differs (healthcare compliance, a seed-stage team without a RevOps person). Otherwise, the persona row is enough.

## Example row

| Persona | Measured on | Top pain | Outcome | Lead pillar | Proof | Objection → answer | Use | Avoid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFO | Close time, audit findings, headcount cost | "We hire analysts to do reconciliation" | 5-day close without new hires | Automation of reconciliation | Contoso: 9 → 4 days, one analyst redeployed | "Another tool to buy" → replaces 2 tools and manual hours | close, audit trail, headcount | revolutionary, synergy, seamless |

Lines for the CFO:
- Email: "Most finance teams your size close in 8-10 days, and most of it is reconciliation."
- Call: "I work with CFOs who'd rather not hire another analyst to get to a 5-day close."
- Landing page: "A 5-day close, without another analyst."

## What good looks like

- Every persona row has a different first sentence.
- Proof is matched to persona.
- The matrix fits on one page; reps actually use it.
- The common mistake is building a 12-column matrix for 15 micro-segments that nobody opens again.

## Rules

- MUST keep the core value proposition consistent across rows.
- MUST use only approved proof points.
- NEVER create rows for segments without distinct pains.

## Example prompts

- "Build a messaging matrix for CFO, Controller and AP Manager from our value prop."
- "Our SDRs use the same pitch for everyone. Create persona lines for email and LinkedIn."
- "Add healthcare and fintech variants to our messaging matrix where they truly differ."
