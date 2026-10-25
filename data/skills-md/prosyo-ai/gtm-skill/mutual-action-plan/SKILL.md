---
name: mutual-action-plan
description: "Use this skill when a B2B deal needs a shared plan to get from evaluation to signature and go-live: \"build a mutual action plan\", \"close plan for this deal\", \"what are the steps to sign\", \"deal keeps slipping\". Works backwards from the buyer's go-live date, lists every step on both sides (evaluation, security, legal, procurement, approvals, onboarding) with owners and dates, flags the critical path, and writes the email that introduces the plan to the champion as a tool to help them, not to pressure them."
license: MIT
metadata:
  title: Mutual action plan
  category: deals
  tags: "Sales, Founders, Sales Leaders, Customer Success"
  author: prosyo
  version: "1.0.0"
  keywords: "mutual action plan template, close plan b2b, mutual success plan, claude mutual action plan skill, deal timeline"
  inputs: "Buyer's target go-live, Known decision and paper process, Stakeholders"
  outputs: "Mutual action plan, Critical path, Champion email"
---

Use this once a buyer agrees the problem is worth solving. A shared plan turns "we'll get back to you" into dated steps both sides own, and shows early whether the close date is real.

## Inputs

- The buyer's target date for value (go-live, a launch, a quarter start) and why it matters.
- What is known about their decision and paper process.
- Stakeholders on both sides.

## The play

### 1. Anchor on their date
Start from the date the buyer needs results, not your quarter end. "To have reps using it by 1 March, onboarding starts 1 February, so signature by 25 January."

### 2. List every step, both sides
Evaluation, stakeholder meetings, technical review, security questionnaire, legal review, procurement and vendor setup, budget approval, signature, kickoff, onboarding milestones. Most slipped deals slip on steps nobody listed. Read [references/map-template.md](references/map-template.md) for the template and typical durations.

### 3. Assign owners and dates
Every step has a named owner (buyer or seller side) and a date. Steps without a buyer-side owner are wishes.

### 4. Mark the critical path
The longest chain of dependent steps, usually security plus legal plus procurement. Start them in parallel and early.

### 5. Introduce it as help
Send the plan to the champion as a tool for their internal process: "Here's a draft of what usually needs to happen; what did I miss?" Let them edit it. A plan the buyer has changed is a plan they own.

### 6. Review it every week
Update status, move dates honestly, and raise slips early.

## Champion email

> Hi Priya, to hit reps live by 1 March, I sketched the steps that usually need to happen on both sides (attached). Some I've guessed, especially security and procurement at Lumen. Could you fix what's wrong and add anything I missed? Happy to walk through it on Thursday's call.

## What good looks like

- The buyer edits the plan, adds steps and owns dates.
- Security, legal and procurement start before the final presentation, not after.
- The plan continues past signature into the first value milestone, which keeps the conversation about outcomes.
- The common mistake is a seller-only checklist sent as an ultimatum the week before quarter end.

## Rules

- MUST anchor dates on the buyer's goal.
- MUST name an owner for every step.
- NEVER invent deadlines or artificial urgency in the plan.

## Example prompts

- "Build a mutual action plan for our $60k deal with Lumen; they want reps live by 1 March."
- "This deal keeps slipping. Turn my notes into a close plan with the critical path."
- "Write the email that introduces the plan to our champion."
