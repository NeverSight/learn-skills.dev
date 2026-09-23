---
name: product-roadmapping-and-portfolio
description: >-
  Build and maintain outcome-based product roadmaps and portfolio views that
  sequence strategic bets by evidence, not dates. Covers Now/Next/Later views,
  strategic-bet management, capacity allocation, dependency and confidence
  mapping, scenario planning, continue/pause/kill/revisit criteria, stakeholder
  narratives, and roadmap review cadences. Use when building or reviewing a
  product roadmap, managing a portfolio of bets, or communicating strategic
  sequencing to stakeholders. Do NOT use for tactical prioritization mechanics
  (RICE, MoSCoW, Kano, OST — route to product-methodology or product-strategy),
  for project scheduling or Gantt charts, or for delivery-flow management
  (route to kanban-guru).
license: MIT
compatibility: Agent harness with file read/write and skill loading
metadata:
  tags: product-roadmapping, portfolio-management, strategic-bets, outcome-roadmaps,
    now-next-later, scenario-planning, roadmap-communication
---

# Product Roadmapping and Portfolio Management

Build roadmaps that communicate strategic intent without pretending to predict the future. This skill covers outcome-based sequencing, strategic-bet management, and portfolio-level choices — not feature-level prioritization or project scheduling.

## Core Principles

1. **Roadmaps are not project schedules.** A roadmap communicates strategic direction and sequencing intent. It does not commit to dates by default. The default view is Now/Next/Later; dates appear only when explicitly labeled as commitments.

2. **Distinguish four categories in every artifact.** Every roadmap output separates evidence (observed data), assumptions (beliefs not yet validated), commitments (decisions with consequences for reversal), and options (alternatives under consideration).

3. **Bets, not plans.** Each roadmap item is a strategic bet — an investment with an expected outcome, a confidence level, explicit dependencies, and pre-defined continue/pause/kill/revisit criteria. A roadmap is a portfolio of bets, not a to-do list.

4. **Portfolio thinking scales up and down.** The same bet-record and roadmap structure works for a single product and for a portfolio of products.

## Loading Guide

| File | Load when |
|---|---|
| [references/outcome-roadmapping.md](references/outcome-roadmapping.md) | Building or reviewing a Now/Next/Later outcome roadmap |
| [references/strategic-bets.md](references/strategic-bets.md) | Defining, evaluating, or comparing strategic bets |
| [references/dependency-confidence-view.md](references/dependency-confidence-view.md) | Mapping cross-bet dependencies or calibrating confidence |
| [references/scenario-comparison.md](references/scenario-comparison.md) | Comparing alternative futures or building scenario plans |
| [references/roadmap-review-cadence.md](references/roadmap-review-cadence.md) | Designing or running a roadmap review process |
| [references/discovery-brief.md](references/discovery-brief.md) | Understanding ownership boundaries and routing rules |
| [templates/outcome-roadmap.md](templates/outcome-roadmap.md) | Fillable Now/Next/Later roadmap template |
| [templates/bet-record.md](templates/bet-record.md) | Fillable strategic-bet record |
| [templates/roadmap-review-record.md](templates/roadmap-review-record.md) | Recording a roadmap review session |

## Working Method

### 1. Start with outcomes, not features
Define outcomes as measurable "from → to" statements. Route evidence to `product-analytics-and-measurement`.

### 2. Map the Now/Next/Later landscape
Now = committed (WIP-limited), Next = validated/provisional, Later = options only. Dates only when labeled as commitments.

### 3. Build bet records
Every bet: outcome hypothesis, evidence, confidence (H/M/L with rationale), risk, dependencies, capacity, continue/pause/kill/revisit criteria.

### 4. Map dependencies and confidence
Blocking, enabling, shared-capacity, external dependencies. Effective confidence bounded by dependency health.

### 5. Compare scenarios
Base case + alternative scenarios for consequential decisions. Identify robust, conditional, fragile bets.

### 6. Define review cadence
Monthly for Now, quarterly for Next/Later. Record decisions with rationale.

### 7. Communicate to stakeholders
Executive narrative, team view, external/customer view — each tailored.

## Routing Table

| When the task involves... | Route to... |
|---|---|
| RICE scoring, MoSCoW prioritization, OST workflow | [product-methodology](../product-methodology/SKILL.md) — canonical tactical owner |
| Kano model, OST strategic framing, competitive positioning | [product-strategy](../product-strategy/SKILL.md) — strategic frameworks |
| Capital allocation, M&A portfolio choices | [strategy-frameworks](../strategy-frameworks/SKILL.md) — corporate strategy |
| Delivery flow, WIP limits, throughput, cycle time | [kanban-guru](../kanban-guru/SKILL.md) — execution-level flow |
| Evidence, metrics, analytics instrumentation | `product-analytics-and-measurement` — analytics layer (prose reference) |
| Implementation planning for approved bets | `implementation-planning` — handoff target (prose reference) |
| Experiment design for low-confidence bets | `product-experimentation` — downstream consumer (prose reference) |
| Adoption measurement for shipped bets | `product-adoption` — downstream consumer (prose reference) |
| Lifecycle learning from bet outcomes | `product-lifecycle-learning` — downstream consumer (prose reference) |

## When Not to Use

- **For tactical prioritization mechanics** (RICE scores, MoSCoW buckets, Kano categorization, OST trees): route to `product-methodology` or `product-strategy`. This skill references these frameworks only to describe *where* they fit, never to re-explain formulas or mechanics.
- **For cross-project program coordination** (integrated dependencies, shared capacity, program benefits, or transformation delivery): route to [technical-program-management](../technical-program-management/SKILL.md). This skill sequences product bets; it does not coordinate their technical program execution.
- **For project scheduling, Gantt charts, or milestone tracking:** route to [technical-project-management](../technical-project-management/SKILL.md) for ongoing project control; use [implementation-planning](../implementation-planning/SKILL.md) for detailed planning of approved work. This skill owns outcome roadmaps.
- **For delivery-flow management:** route to `kanban-guru`.
- **For corporate capital allocation and M&A portfolio decisions:** route to `strategy-frameworks`.
- **For shaping a single bet** (setting its appetite, narrowing it into a bounded
  problem, writing its pitch): route to `product-shaping`. This skill sequences bets
  across cycles at the portfolio level; shaping packages one bet before it enters a
  roadmap — "strategic bet" here means a roadmap entry with sequencing criteria, not
  the shaped single-project commitment that `product-shaping` produces.

## Evidence, Assumptions, Commitments, and Options

Every roadmap artifact distinguishes these four categories:

| Category | Definition | Example |
|---|---|---|
| **Evidence** | Observed data, validated learning, experiment results | "A/B test showed 12% lift in retention (p < 0.05, n=4,200)" |
| **Assumptions** | Beliefs not yet validated | "We assume users grant notification permissions at ~40%" |
| **Commitments** | Decisions with defined consequences for reversal | "Q3: 8 engineer-weeks for payments migration" |
| **Options** | Alternatives under consideration | "Build in-house vs. integrate third-party" |

An artifact that mixes assumptions into evidence or presents options as commitments is not a valid output of this skill.
