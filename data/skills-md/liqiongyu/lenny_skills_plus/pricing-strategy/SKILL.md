---
name: "pricing-strategy"
description: "Create a Pricing Strategy Pack (value metric + willingness-to-pay plan, packaging & price-point options, self-serve vs sales-led thresholds, experiments, rollout + review cadence). Use for pricing, monetization, freemium, free trial, reverse trial, and packaging decisions. Category: Growth."
---

# Pricing Strategy

## Scope

**Covers**
- Pricing strategy and price setting (new product or repricing)
- Packaging and plan design (freemium, trials, feature gating, add-ons)
- Willingness-to-pay (WTP) research plan and evidence collection
- Self-serve vs sales-led handoffs (incl. thresholds and operational constraints)
- Conversion mechanics (sampling premium features, trial/discount design)
- Rollout, migration, and measurement (guardrails + review cadence)

**When to use**
- “Create a pricing strategy / monetization strategy.”
- “Propose packaging and plans for freemium → paid.”
- “We need new price points and a rationale tied to value.”
- “Design a free trial / reverse trial / capped trial.”
- “Figure out when self-serve tops out and when we need sales-led.”

**When NOT to use**
- You need to define the customer, core use case, or value proposition first (do that before pricing)
- You only want a quick competitor price scrape (no synthesis or decision support)
- You need legal/tax/accounting advice (coordinate with qualified experts)
- You’re making irreversible billing changes without a rollback/migration plan

## Inputs

**Minimum required**
- Product: what it does, for whom, and the primary job-to-be-done
- Target segment(s) and buying context (B2B/B2C, who pays vs who uses)
- Current pricing (if any): plans, price points, value metric, discounts, trial
- Objective + constraints: what decision this pricing work should change, and by when
- Sales motion: self-serve only, sales-led, or hybrid; typical deal sizes (if known)
- Any evidence: conversion/funnel metrics, retention, revenue mix, win/loss notes, customer quotes, competitor references

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns. Include a “Validation plan” section in the output.

## Outputs (deliverables)

Produce a **Pricing Strategy Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (goal, ICP, motion, constraints, time box)
2) **Value metric + segmentation hypotheses** (primary + alternates)
3) **WTP evidence plan** (who to talk to, what to ask, how to interpret)
4) **Packaging & plans** (plan table: who it’s for, limits, included value)
5) **Price-point options + recommendation** (ranges, rationale, discount policy)
6) **Conversion mechanics plan** (trial type, sampling premium value, friction reduction)
7) **Rollout + instrumentation** (migration steps, KPIs/guardrails, monitoring)
8) **Pricing review cadence** (update triggers; default 6–12 months)
9) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the decision, timeline, and who will use the output. Capture current pricing (if any), motion (self-serve vs sales-led), and constraints (billing, contracts, compliance, brand).
- **Outputs:** Context snapshot + “success looks like” metrics.
- **Checks:** A stakeholder can answer: “What decision will this pricing work change?”

### 2) Clarify value and who pays (segment map)
- **Inputs:** ICP/use case; current customers/users (if any).
- **Actions:** Define 1–3 primary segments, buyer vs user roles, and the core value delivered (outcomes + avoided risks). Identify switching costs and “must-have” trust requirements.
- **Outputs:** Segment map + value narrative per segment.
- **Checks:** Value is stated as outcomes (not features). Buyer and user are not conflated.

### 3) Choose pricing architecture (value metric + packaging)
- **Inputs:** Segment map; product capabilities; constraints.
- **Actions:** Propose 1 primary value metric (and 1–2 alternates). Design packaging: plans, limits, add-ons, and what is free vs paid. Explicitly define self-serve vs sales-led boundaries (e.g., contract size, security needs, procurement).
- **Outputs:** Value metric options table + packaging & plans table.
- **Checks:** Each plan has a clear “who it’s for” and an upgrade path tied to value.

### 4) Treat price as a measure of value (WTP plan)
- **Inputs:** Value narrative; packaging; any evidence.
- **Actions:** Draft a WTP evidence plan: which segments to interview, what scenarios to test, and how to triangulate price sensitivity (qual + quant). Keep hypotheses explicit; avoid “pricing by vibes”.
- **Outputs:** WTP plan + interview/survey prompts (as needed).
- **Checks:** For each plan, the price is justified by value delivered and a plan to validate WTP.

### 5) Design conversion mechanics (sampling + friction reduction)
- **Inputs:** Funnel metrics; onboarding/trial experience.
- **Actions:** Propose how users experience paid value before paying: sampling premium features, reverse trial/capped trial, and/or time-boxed trial. Identify monetary friction to remove (trial costs, upfront commitments) and define guardrails to protect revenue leakage.
- **Outputs:** Conversion mechanics plan + experiment backlog.
- **Checks:** Mechanics demonstrate premium value in-product; there are clear abuse controls and success metrics.

### 6) Recommend price points + rollout and ops plan
- **Inputs:** Packaging; WTP plan; constraints.
- **Actions:** Propose 2–3 price-point options (good/better/best), plus a recommendation with tradeoffs. Include discounting/annual plans, sales assist triggers, and a migration/rollback approach. Define a pricing review cadence (default revisit every 6–12 months, or when value changes materially).
- **Outputs:** Recommended price points + rollout/migration plan + review cadence.
- **Checks:** Recommendation is operationally feasible (billing, sales, support) and has a rollback/migration path.

### 7) Quality gate + finalize
- **Inputs:** Draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add **Risks / Open questions / Next steps** and a short validation plan (what to learn next, by when).
- **Outputs:** Final Pricing Strategy Pack.
- **Checks:** Assumptions are explicit; evidence needs are clear; the pack is ready to share.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS, hybrid motion):**  
“Use `pricing-strategy`. We sell workflow automation to mid-market ops teams. Current: $49/user/mo with low conversion. Goal: improve paid conversion and expansion. Motion: self-serve + sales assist. Output: a Pricing Strategy Pack with packaging options and a rollout plan.”

**Example 2 (Freemium → paid, consumer):**  
“Use `pricing-strategy`. We’re a creator tool with freemium + subscription. We want to introduce a reverse trial and improve upgrades without hurting retention. Output: pricing + trial mechanics + experiment backlog.”

**Boundary example:**  
“Pick a price for us with no product, customer, or market context.”  
Response: request minimum inputs (ICP/use case, value metric candidates, objective) and propose a WTP plan + 2–3 pricing architecture options with explicit assumptions.
