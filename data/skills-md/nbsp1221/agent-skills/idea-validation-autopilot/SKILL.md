---
name: idea-validation-autopilot
description: Use when a founder has a rough product idea and wants autonomous deep validation, market and competitor research, and an evidence-based MVP decision with minimal back-and-forth.
---

# Idea Validation Autopilot

Turn a rough idea into an evidence-backed build decision in one run.

## Overview

This skill is a single orchestrator for:

1. idea clarification
2. market and competitor research
3. MVP scope definition
4. go/no-go style decision memo

Default behavior favors action over over-analysis:
- ask as few questions as possible
- run parallel research
- output a build-ready decision packet

## When to Use

Use this skill when:
- user says they have many ideas but cannot decide efficiently
- user wants "startup-like" process without paying for SaaS tools
- user wants AI to drive research and synthesis, not just brainstorm
- user asks for market validation + MVP boundaries + next execution steps

Do not use this skill when:
- user already has validated requirements and only wants implementation planning
- user wants only code generation with no discovery work

## Operating Defaults

If user context is missing, proceed with defaults instead of blocking:

- Goal priority: `speed-to-learning > polish`
- Budget assumption: `near-zero external spend`
- Team assumption: `solo builder or very small team`
- Timebox assumption: `one focused discovery cycle`

Only ask questions when missing data would invalidate the result (for example: unclear target user or regulated domain).

## Workflow

Copy this checklist and track progress:

```md
Progress
- [ ] Step 1: Normalize idea into problem hypothesis
- [ ] Step 2: Run 4 parallel research tracks
- [ ] Step 3: Grade evidence quality and resolve contradictions
- [ ] Step 4: Produce decision scorecard and verdict
- [ ] Step 5: Define MVP scope and exclusions
- [ ] Step 6: Define first experiments and stop rules
- [ ] Step 7: Deliver final report using template
```

### Step 1: Normalize the idea

Convert raw idea into this structure:

- target user
- painful job-to-be-done
- current workaround
- why-now trigger
- value promise in one sentence

If unclear, propose your best assumption and mark it explicitly.

### Step 2: Run 4 parallel research tracks

Dispatch four independent subagents (or equivalent parallel workers).

1. User/Problem Research
- Find who feels the pain and how urgently.
- Capture behavioral evidence, not just opinions.

2. Market/Competitor Research
- Map direct/adjacent alternatives, pricing, positioning, switching cost.
- Identify market gap with realistic differentiation.

3. Business Model/Risk Research
- Estimate willingness-to-pay signals, acquisition path, and major risks.
- Flag legal/compliance/data-access blockers early.

4. MVP/Technical Feasibility Research
- Define thinnest viable product delivering the core job.
- Identify build constraints, integration risks, and timeline risk.

### Step 3: Grade evidence quality

Use evidence tiers:

- `Tier A`: behavioral or monetary signal (payment, waitlist intent with commitment, repeated real usage)
- `Tier B`: strong secondary evidence (credible reports, robust competitor/user data)
- `Tier C`: weak signal (opinions, generic trend articles, unsupported claims)

Rules:
- critical claims need at least two independent sources
- if evidence is weak, lower confidence regardless of narrative quality

### Step 4: Score and decide

Score 0-100 using weighted dimensions:

| Dimension | Weight |
| --- | ---: |
| Problem severity and frequency | 25 |
| Distribution reachability | 20 |
| Willingness-to-pay potential | 20 |
| MVP speed/feasibility | 20 |
| Strategic differentiation | 15 |

Scoring rules (fixed):
- each dimension score is `0..100`
- `weighted_i = score_i * weight_i / 100`
- `total_score = round(sum(weighted_i), 1)`
- map verdict from `total_score` using the bands below

Verdict bands:
- `80-100`: Build now
- `60-79`: Validate-first (run targeted tests before building)
- `40-59`: Pivot
- `<40`: Drop

### Step 5: Define MVP scope

Use strict scope slicing:

- `Must`: smallest set proving core value
- `Should`: useful but deferrable
- `Won't (now)`: explicitly excluded features

Output a 2-week implementation target:
- week 1: build core flow
- week 2: launch to first users and collect signals

### Step 6: Define experiments and stop rules

For top risks, define:

- experiment
- pass threshold
- fail threshold
- next action if pass/fail

Keep experiments cheap and fast. Favor reversible steps.

### Step 7: Deliver final report

Use `assets/final-report-template.md`.

Output path rules:
- if `reports/` does not exist, create it first (`mkdir -p reports`)
- write report to `reports/YYYY-MM-DD-<idea-slug>-idea-validation.md`

Required output qualities:
- explicit assumptions table
- explicit unknowns
- citations and dated evidence
- final recommendation plus next 7-day action plan

## Common Failure Modes

1. Over-research without decisions
- Fix: enforce scorecard and verdict section every run.

2. Generic competitor list with no switching analysis
- Fix: include why users switch or stay.

3. MVP too large
- Fix: require "what can be deleted" before finalizing scope.

4. False confidence from weak sources
- Fix: downgrade to Tier C and force validation-first verdict.

## Quick Command Patterns

Adapt to available tools:

- web search + fetch for sources
- repository/API lookup for existing solutions
- parallel subagents for independent tracks
- markdown report output in project `reports/`

If one tool is unavailable, continue with the best fallback and document the limitation in assumptions.
