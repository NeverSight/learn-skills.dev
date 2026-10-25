---
name: objection-handler
description: "Use this skill when a prospect raises an objection in a reply, on a call or in a deal: \"how do I respond to 'too expensive'\", \"handle this objection\", \"build an objection handling guide\", \"they said they're happy with their current vendor\". Diagnoses what the objection really means, picks the response pattern (clarify, reframe, prove, defer or walk away), writes responses for email, call and LinkedIn, and builds a reusable objection library with proof for each."
license: MIT
metadata:
  title: Objection handler
  category: replies-meetings
  tags: "SDR, Sales, Founders, Sales Leaders"
  author: prosyo
  version: "1.0.0"
  keywords: "sales objection handling, objection handling scripts, too expensive objection, claude objection handling skill, b2b sales objections"
  inputs: "The objection in their words, Context and stage, Proof points"
  outputs: "Diagnosis, Response per channel, Objection library entry"
---

Use this when a buyer pushes back. Most objections are questions in disguise; the response that works first finds out which question.

## Inputs

- The objection, in the buyer's exact words.
- Context: cold reply, discovery call, late-stage deal; who said it.
- Proof available: customer stories, numbers, documents.

## The play

### 1. Diagnose before answering
| Surface objection | Often really means |
| --- | --- |
| "Too expensive" | Value not clear yet, wrong package, budget timing, or a competitor quote |
| "We already have a solution" | Switching feels risky; current pain not acknowledged |
| "Not a priority" | Problem not tied to something they are measured on |
| "Send me some info" | Polite exit, or genuinely busy |
| "I need to talk to my team" | Not the decision-maker, or not convinced enough to champion |
| "We tried something like this" | Past failure; fear of repeating it |

### 2. Choose the pattern
- **Clarify**: ask a question that surfaces the real concern. Default first move.
- **Reframe**: change the comparison (cost of the problem vs the price; risk of doing nothing).
- **Prove**: a peer who had the same concern and what happened.
- **Defer**: agree a specific later moment when the condition changes.
- **Walk away**: when the objection reveals a genuine bad fit, say so. It builds trust and saves time.

### 3. Write the response
Acknowledge in a few words (no "I totally understand"), then the pattern. Keep email responses under 80 words. On calls, ask and then stop talking.

Read [references/objection-library.md](references/objection-library.md) for responses to the 12 most common B2B objections, by stage.

### 4. Log it
Every objection goes into the library with the response that worked. Patterns across deals feed messaging and product.

## What good looks like

- The first response is usually a question.
- Proof matches the objection: a security concern gets a security document, not a ROI story.
- Bad-fit objections are accepted, not "overcome".
- The common mistake is arguing: answering a price objection with a list of features.

## Rules

- MUST clarify before rebutting when the real concern is unclear.
- MUST use only approved proof points and real pricing.
- NEVER pressure with fake deadlines or "this price ends Friday" unless it is true.
- NEVER disparage a competitor the buyer uses.

## Example prompts

- "Prospect replied 'we're happy with our current vendor'. Draft a response."
- "Build an objection library for our sales team from these 20 call notes."
- "On calls I freeze at 'it's too expensive'. Give me a talk track."
