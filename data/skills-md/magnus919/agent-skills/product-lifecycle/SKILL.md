---
name: product-lifecycle
description: >-
  Route a product through its full lifecycle — discovery, strategy, portfolio choice,
  roadmap, UX and requirements, experimentation, delivery handoff, adoption, success,
  and lifecycle review — by composing existing specialist product skills with
  phase-entry evidence, handoff artifacts, and escalation rules. Use when evaluating
  a new product idea, managing a product through its lifecycle, or connecting product
  phases that currently operate in isolation. Do not use for a single product task
  that is already owned by a specialist skill (load that skill directly); do not use
  for software delivery lifecycle work (route to neckbeard); do not use to duplicate
  product discovery, strategy, UX, experimentation, analytics, release, or delivery
  methods.
license: MIT
compatibility: Agent harness with file read/write, terminal, and skill loading. No network or runtime dependency required by the bundle itself.
metadata:
  spec-version: "1.0"
  tags: product, lifecycle, portfolio, discovery, strategy, delivery, adoption, orchestration
---

# Product Lifecycle

A thin orchestration bundle that routes a product through nine lifecycle phases
by composing existing specialist product skills. It provides **cross-skill
routing and evidence handoff** — it does NOT duplicate any specialist's
step-by-step methodology. Load this umbrella when you need to navigate a product
across multiple lifecycle phases; load individual specialist skills directly
when you only need one phase's capability.

## Phase routing table

Each phase routes to one or more specialist skills. Entry evidence must exist
before the phase starts. Output artifacts are handed off to the next phase
through the lifecycle evidence ledger. Every phase has explicit escalation
behavior and completion criteria. Full phase contracts are in
[references/phases.md](references/phases.md).

| # | Phase | Primary specialist(s) | Entry evidence | Output artifacts | Escalation behavior | Completion criteria |
|---|---|---|---|---|---|---|
| 1 | **Discovery** | [product-discovery](../product-discovery/SKILL.md) | Product idea, market signal, or stakeholder request | Problem statement, stakeholder map, discovery log, product type classification | Stop if: problem cannot be articulated in user terms; no stakeholder describes a real need; problem is already solved; out of organizational remit | Problem statement exists that a stakeholder recognizes; product type classified; proceed/pause/stop decision recorded |
| 2 | **Strategy and portfolio choice** | [product-strategy](../product-strategy/SKILL.md), [strategy-frameworks](../strategy-frameworks/SKILL.md) | Problem statement and discovery log from Phase 1 | Strategic assessment, market sizing, portfolio recommendation, investment thesis | Stop if: opportunity conflicts with strategy; market evidence contradicts thesis; resource constraints are infeasible; strategic direction is ambiguous | Strategic assessment with fit/no-fit reasoning; portfolio decision recorded; resource estimate recorded |
| 3 | **Roadmap** | [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) | Strategic assessment and portfolio decision from Phase 2 | Outcome roadmap entry, Now/Next/Later placement, strategic bet record, dependency map, capacity allocation | Stop if: dependencies cannot be resolved; capacity unavailable; confidence below threshold; conflicts with higher-priority bet | Roadmap entry exists; bet record complete with kill criteria; dependencies mapped and acknowledged |
| 4 | **UX and requirements** | [product-design-and-ux](../product-design-and-ux/SKILL.md) | Roadmap entry and bet record from Phase 3; discovery log | Information architecture, task flows, interface contracts, acceptance criteria | Stop if: UX reveals fundamentally different problem; user research contradicts hypothesis; behavior cannot be specified testably; constraints cannot be satisfied | IA and task flows documented; interface contracts exist; acceptance criteria are testable and traceable |
| 5 | **Experimentation** | [product-experimentation](../product-experimentation/SKILL.md) | UX contracts, assumptions register, risk assessment | Experiment brief, experiment readout, updated assumptions register, proceed/pivot/stop decision | Stop if: experiment cannot be designed ethically; method infeasible; reveals safety/privacy/security risk; hypothesis disproved with no viable pivot | Experiment brief exists with hypothesis and decision rule; readout exists; proceed/pivot/stop decision recorded with evidence |
| 6 | **Delivery handoff** | [implementation-planning](../implementation-planning/SKILL.md), [production-readiness](../production-readiness/SKILL.md), [release-engineering](../release-engineering/SKILL.md) | Proceed decision, UX contracts, acceptance criteria, assumptions register | Implementation plan, formal spec, production-readiness verdict (Go/No-go/Defer/Exception), release plan | Stop if: infeasible dependency; readiness returns No-go or blocked Exception; security/privacy/compliance blocks launch; release plan cannot satisfy change-governance | Implementation plan accepted by delivery team; readiness verdict recorded with evidence; release plan documented and reviewed |
| 7 | **Adoption** | [product-adoption](../product-adoption/SKILL.md) | Launch decision (Go), release evidence, target segments, success metrics | Adoption plan, activation baseline, segmentation record, adoption metrics | Stop if: adoption materially below threshold after intervention; fundamental product-market mismatch; structural adoption problem beyond product changes | Adoption plan executed; activation and adoption baselines measured; proceed/intervene/pivot/stop decision recorded |
| 8 | **Success** | [product-analytics-and-measurement](../product-analytics-and-measurement/SKILL.md) | Adoption evidence, success criteria, experiment readouts | Outcome measurement, metric tree with actuals vs. targets, success/mixed/not-met assessment | Stop if: outcomes materially below expectations with unknown root cause; measurement infrastructure insufficient; evidence contradicts investment thesis | Outcome metrics measured against criteria; success assessment recorded; ledger complete for review |
| 9 | **Lifecycle review** | [product-lifecycle-learning](../product-lifecycle-learning/SKILL.md) | Outcome measurement, full evidence ledger, original assumptions register | Outcome review (expected vs. observed), assumption ledger update, continue/improve/harvest/pivot/pause/retire decision, retained learning record | Stop if: retirement has material implications beyond team authority; retained learning contradicts foundational assumption; systemic pattern requires executive attention | Outcome review recorded; lifecycle decision recorded with rationale; retained learning captured; ledger closed |

### Supporting and cross-cutting skills

These skills are loaded on trigger, not by phase. They support multiple phases
and are routed to when their specific capability is needed.

| Skill | When loaded |
|---|---|
| [product-methodology](../product-methodology/SKILL.md) | When a phase produces alternatives that need ranking (RICE, MoSCoW, Kano, OST) |
| [product-operations-and-governance](../product-operations-and-governance/SKILL.md) | When setting up or changing governance; at phase boundaries needing formal decision authority |
| [financial-modeling](../financial-modeling/SKILL.md) | When unit economics, pricing, or business-model analysis is needed (Phases 2, 8) |
| [go-to-market](../go-to-market/SKILL.md) | When positioning, acquisition strategy, or growth modeling is needed (Phases 7, 8) |
| [data-scientist](../data-scientist/SKILL.md) | When statistical design, causal inference, or rigorous experiment analysis is needed (Phases 5, 8) |
| [spec-driven-development](../spec-driven-development/SKILL.md) | When formal specification with phase gates is needed (Phase 6) |
| [privacy-engineering](../privacy-engineering/SKILL.md) | When any phase handles PII, consent, retention, or data flows |
| [secure-software-engineering](../secure-software-engineering/SKILL.md) | When any phase touches trust boundaries, auth, or sensitive data |
| [verification-methodology](../verification-methodology/SKILL.md) | At every phase gate where evidence is required |
| [qa-methodology](../qa-methodology/SKILL.md) | When test strategy and quality gates are needed (Phase 6) |
| [site-reliability-engineering](../site-reliability-engineering/SKILL.md) | When reliability, SLOs, or operational readiness is needed (Phase 6) |
| [platform-engineering](../platform-engineering/SKILL.md) | When infrastructure, CI/CD, or platform capabilities are needed (Phase 6) |
| [neckbeard](../neckbeard/SKILL.md) | When the software delivery lifecycle (SDLC) change-request journey is needed for implementation (Phase 6) |
| `production-excellence` bundle (when available) | When the full production-excellence bundle is available as a handoff target (Phase 6) — composes production-readiness, migration-engineering, resilience-and-recovery, capacity-and-cost-engineering, and incident-learning |

## Loading protocol

This umbrella is the guaranteed discoverable entry point. Nested skills and
referenced specialists load on trigger — the umbrella does not pre-load them.

1. Read this SKILL.md for the phase routing table and locate the current phase.
2. Load the phase contract from [references/phases.md](references/phases.md) for
   detailed entry evidence, escalation behavior, and completion criteria.
3. Load the specialist skill(s) named in the phase row. Follow the specialist's
   method; do not re-derive it from the umbrella.
4. Write phase outputs to the lifecycle evidence ledger (see
   [references/phases.md](references/phases.md) for ledger fields and conventions).
5. The next phase reads the ledger; it does not re-derive prior-phase evidence.
6. When the lifecycle completes or stops, the ledger is the durable record.

For capability lookup without traversing the full lifecycle, use the
[references/capability-map.md](references/capability-map.md).

## When not to use

- **Single specialist task.** If the work is entirely within one phase (e.g., a
  stakeholder interview, an experiment design, a roadmap update), load the
  specialist skill directly. The umbrella adds orchestration overhead that is
  unnecessary for single-phase work.
- **Software delivery lifecycle.** If the work is a code change, bug fix, or
  feature implementation — not product-level decision-making — route to
  [neckbeard](../neckbeard/SKILL.md).
- **Duplicate methodology.** This bundle does NOT duplicate product-discovery,
  product-strategy, product-design-and-ux, product-experimentation,
  product-analytics-and-measurement, or release-engineering methods. Load those
  skills directly for their step-by-step instructions.
- **B2B SaaS assumption.** This bundle does NOT assume a B2B SaaS product.
  Customer-success routing (Phase 8) is CONDITIONAL on product type.
  Internal tools, public-service products, transactional products, and consumer
  products proceed without loading
  [conditional-customer-success](../conditional-customer-success/SKILL.md).
- **Strategic frameworks.** For standalone strategic analysis (Five Forces,
  Blue Ocean, Ansoff) without a lifecycle context, load
  [strategy-frameworks](../strategy-frameworks/SKILL.md) directly.
- **Financial modeling.** For standalone financial analysis without a lifecycle
  context, load [financial-modeling](../financial-modeling/SKILL.md) directly.

## File map

| Path | Loaded when |
|---|---|
| [references/phases.md](references/phases.md) | Entering any lifecycle phase; defines entry evidence, output artifacts, escalation behavior, and completion criteria per phase |
| [references/discovery-brief.md](references/discovery-brief.md) | Understanding the bundle boundary and how it compares to existing bundles |
| [references/capability-map.md](references/capability-map.md) | Looking up which specialist skill owns a specific capability without traversing the full lifecycle |
| [manifest.yaml](manifest.yaml) | Machine-readable composition contract (schema v1): purpose, audience, stages, included skills, prerequisites, outputs, handoffs, conflicts, and eval suite; consumed by the lifecycle capability matrix |
