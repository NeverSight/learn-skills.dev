---
name: lead-scoring-model
description: "Use this skill when you need a lead scoring model that sales trusts: inbound leads pile up unworked, marketing and sales argue about MQL quality, or reps chase the wrong leads first. Designs a two-axis model (fit and engagement) from your won and lost data, sets point values and decay, defines the handoff threshold and the SLA, and includes the test that proves the model works. Produces a documented scoring model ready to configure in any CRM or marketing system."
license: MIT
metadata:
  title: Lead scoring model
  category: prospecting
  tags: "RevOps, Marketing, Demand Gen, Sales Leaders"
  author: prosyo
  version: "1.0.0"
  keywords: "lead scoring model, b2b lead scoring template, mql scoring, claude lead scoring skill, predictive lead score"
  inputs: "Won and lost leads with attributes, Engagement data, Sales capacity"
  outputs: "Fit and engagement scoring tables, Handoff threshold, SLA, Validation report"
---

Use this when the question is "which leads should sales call first?". It produces a scoring model with point tables, a threshold and a validation test, documented well enough that anyone can configure it.

## Inputs

- 6 to 12 months of leads with outcome: became an opportunity, won, or went nowhere.
- Firmographic and role data on each lead.
- Engagement events: form fills, page visits, email replies, event attendance, product sign-ups.
- Sales capacity: how many leads a week the team can work properly.

## The play

### 1. Two axes, never one
- **Fit** (who they are): role, company size, industry, region, stack. Changes rarely.
- **Engagement** (what they did): actions, weighted by intent, decaying over time.

A single blended number lets a student who downloads ten ebooks outrank a VP who visited pricing once.

### 2. Derive points from data
For each attribute and action, compare the opportunity rate of leads that have it with the base rate. Points roughly follow the lift: an action with 4x the base opportunity rate earns about twice the points of one with 2x. Read [references/scoring-tables.md](references/scoring-tables.md) for starter tables and the lift method.

### 3. Add negative scores and decay
Subtract for students, competitors, personal emails, job seekers and unsubscribes. Halve engagement points every 30 days so old activity does not keep a lead hot.

### 4. Set the threshold from capacity
Choose the fit and engagement cut-offs that send sales roughly the number of leads they can work within the SLA. A threshold that produces 300 leads a week for a team that can work 80 trains reps to ignore scores.

### 5. Define the handoff
- High fit + high engagement: route to sales, first touch within 1 business hour (inbound) or same day.
- High fit + low engagement: targeted outbound or nurture.
- Low fit + high engagement: self-serve path or marketing nurture.
- Low fit + low engagement: no action.

High-intent actions such as a demo request or pricing contact bypass scoring entirely.

### 6. Validate before launch
Backtest on last quarter: the top 20% of scored leads should hold at least 50% of the opportunities. Then review monthly.

## What good looks like

- Sales can explain any score from the point table in 30 seconds.
- The top-scored decile converts to opportunity at 3x or more the average.
- Demo requests never wait for a score.
- The common mistake is guessing points in a meeting ("a webinar feels like 10 points") instead of deriving them from outcomes.

## Rules

- MUST keep fit and engagement as separate scores.
- MUST include decay and negative scoring.
- MUST backtest before going live.
- NEVER route a direct demo or pricing request through scoring delays.

## Example prompts

- "Build a lead scoring model from this export of 4,000 leads with outcomes."
- "Our MQLs convert at 3%. Redesign the scoring so sales trusts it."
- "Set a threshold that sends my 5 reps about 60 leads a week."
