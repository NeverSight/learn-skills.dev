---
name: agent-first-product-strategy
description: Reframe AI product and SaaS strategy from human-user assumptions to agent-first execution. Use when redefining product positioning, success metrics, API/docs priorities, go-to-market, or roadmap decisions for an AI-native market where agents are primary software users.
---

# Agent-First Product Strategy

## Overview

Use this skill to turn high-level AI-era ideas into concrete product strategy, metric design, and execution choices.

## Workflow

1. Identify old-paradigm assumptions in the current plan.
2. Reframe target user and value unit for agent-first operation.
3. Redesign product surface around API, protocol, and documentation quality.
4. Replace vanity metrics with outcome and reliability metrics.
5. Propose phased execution with explicit tradeoffs.

## Step 1: Find Old-Map Assumptions

Audit the current strategy for these legacy assumptions:

- `DAU` as primary growth signal.
- `tool -> community -> platform` as default path to defensibility.
- Human-first UX as the dominant moat.
- Attention-time capture as monetization logic.
- "overseas expansion" as localization-first growth logic.

If any assumption exists, mark it as a risk and quantify impact on cost, speed, or defensibility.

## Step 2: Reframe to Agent-First

Define strategy with these agent-era premises:

- Primary user can be `Agent`, not only human operators.
- Core value is `outcome delivery efficiency` (time-to-outcome and quality), not time spent.
- Product may be better positioned as `capability infrastructure` rather than consumer app.
- Distribution can be `agent discoverability + machine-usable docs`, not only human marketing funnels.

Return a one-line reframing statement:

`We help <agent/human+agent segment> achieve <outcome> via <capability/API>, optimized for <speed/reliability/cost>.`

## Step 3: Define Product Surface

Prioritize product work in this order:

1. API clarity and stability (`auth`, schema consistency, error model).
2. Documentation quality (machine-readable examples, clear contracts, rate limits, versioning).
3. Protocol interoperability (standard interfaces, predictable retries, idempotency).
4. Reliability layer (latency, success rate, graceful degradation, observability).
5. Human UI as a control surface, not the only surface.

When tradeoffs are hard, prefer decisions that improve repeatable agent invocation quality.

## Step 4: Replace Metrics

Convert success metrics from attention-era to productivity-era:

- Replace `DAU/time spent` with `task completion rate`, `unit outcome cost`, and `end-to-end delivery time`.
- Track `API success rate`, `P95 latency`, `agent repeat-call ratio`.
- Track `first-call success` (agent can integrate correctly on first attempt).
- Track `integration lead time` (from docs read to first production call).

Read `references/agent-first-metrics.md` to choose metric formulas and guardrails.

## Step 5: Build Execution Plan

Produce a phased plan:

1. `0-30 days`: fix integration blockers, tighten API contract, publish minimal docs set.
2. `31-90 days`: improve reliability/SLOs, ship agent onboarding examples, cut integration time.
3. `90+ days`: optimize cost-performance frontier, deepen protocol ecosystem, create domain moats.

For each phase include:

- Goal
- Top 3 actions
- Metric target
- Major risk and mitigation

## Output Format

When responding, output in this structure:

1. Current assumptions detected
2. Agent-first reframing statement
3. Product surface priorities
4. Metric redesign table
5. 30/90/+ day plan
6. Top unresolved strategic question
