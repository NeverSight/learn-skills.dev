---
name: audience-personas
description: Build evidence-led social audience personas from customer interviews, comments, reviews, or CRM notes.
user-invokable: true
argument-hint: "[paste customer evidence]"
license: MIT
metadata: { author: Ootto, version: "1.0.0", category: marketing }
---
# Audience Personas

Turn supplied customer evidence into grounded audience segments. Use it when a marketer has interviews, comments, reviews, or CRM notes and needs to decide who a message is for. It is not for inventing demographics, market size, or personas from intuition.

## 1. Establish the evidence

Ask for the source, date range, decision owner, offer, and desired audience action. Keep direct quotes separate from summaries and name material that is missing.

## 2. Group observable patterns

Cluster the evidence by job-to-be-done, desired outcome, objection, exact language, and trigger. Cite the source for each cluster. Do not manufacture a segment just to reach a round number.

## 3. Produce a usable segment

For each evidence-backed segment, return its job, language, objections, useful message angles, and the question it is already asking. Label confidence and unresolved questions.

## 4. Hold claims for review

Flag any demographic statement, outcome claim, or customer quote that needs approval before public use.

## Hard rules

- Do not infer demographics, income, identity, or intent not present in the source.
- Do not turn one loud comment into a market-wide claim.
- Keep observed language distinct from suggested copy.
- If evidence is thin, ask for more comments, reviews, or interviews.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Generic personas | source has no concrete language | ask for verbatim comments or interviews |
| False certainty | inference appears as fact | label it as a hypothesis |
| Too many segments | minor differences treated as groups | merge around the shared job-to-be-done |

## Where it sits

`social-listening` gathers recurring conversation → **audience-personas** groups it → `positioning-audit` turns it into a message.
