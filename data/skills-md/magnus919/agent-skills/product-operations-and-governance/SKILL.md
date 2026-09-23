---
name: product-operations-and-governance
description: >-
  Define and run product governance — recurring decision rights, intake,
  portfolio cadences, evidence standards, and cross-functional operating
  contracts. Covers six review cadences (intake, portfolio, roadmap,
  experiment, launch, lifecycle) with named accountable owners, minimum
  evidence standards per decision type, and escalation paths. Supports
  lightweight and high-assurance operating modes with configurable governance
  patterns. Use when designing a product governance model, resolving contested
  decisions, establishing evidence standards, recording exceptions and
  escalations, or building cross-functional operating contracts. Do NOT use
  for executive governance (capital allocation, org structure — route to
  chief-of-staff-methodology or strategy-frameworks), for technical delivery
  gates (CI/CD, release approval — route to release-engineering or
  spec-driven-development), or to impose a universal org chart.
license: MIT
compatibility: Agent-agnostic — works with any agent framework supporting the Agent Skills format. No external services, proprietary tools, or runtime dependencies required.
metadata:
  tags: product-operations, product-governance, decision-rights, operating-model,
    review-cadence, evidence-standards, escalation, exceptions, intake,
    portfolio-review, product-council
---

# Product Operations and Governance

Define and operate the recurring product governance system: who decides what, with what evidence, on what cadence, and what happens when decisions are contested or evidence is missing. This skill owns the product-level operating model — the connective tissue between product strategy, portfolio choices, experimentation, adoption, and lifecycle learning. It does not own executive governance or technical delivery gates.

## Governance Boundary (Read First)

This skill owns **product governance**: the recurring system for intake, portfolio review, roadmap decisions, experiment review, launch decisions, and lifecycle/health review. Product governance answers: what are we building, in what order, with what evidence, reviewed by whom, on what cadence?

This skill explicitly does **not** own:

- **Executive governance** — capital allocation, org structure, strategic bets at the company level, M&A evaluation. Route to [chief-of-staff-methodology](../chief-of-staff-methodology/SKILL.md) for decision-memo and executive-office methods, and [strategy-frameworks](../strategy-frameworks/SKILL.md) for strategic planning frameworks.
- **Technical delivery gates** — CI/CD pipelines, release approval workflows, deployment checklists, infrastructure change review. Route to [release-engineering](../release-engineering/SKILL.md) for release mechanics and [spec-driven-development](../spec-driven-development/SKILL.md) for specification-phase gates.

The three governance layers — product, executive, and delivery — are distinct. A product governance decision ("approve this experiment to proceed to launch review") is not an executive decision ("allocate $2M to the payments platform") and not a delivery gate ("the deployment pipeline must pass integration tests"). See [references/discovery-brief.md](references/discovery-brief.md) for the full boundary analysis.

## Core Framework

### Two Operating Modes

This skill supports two modes; choose one explicitly for every engagement. The mode determines evidence requirements, review formality, and escalation thresholds.

| Dimension | Lightweight | High-Assurance |
|-----------|-------------|----------------|
| Team size | Small (≤15 engineers, ≤3 product teams) | Any size, with regulatory or safety obligations |
| Review formality | Async written updates; synchronous only for contested decisions | Synchronous reviews with documented quorum |
| Evidence minimum | Hypothesis + qualitative signal or single quantitative metric | Statistical evidence, risk analysis, compliance sign-off |
| Exception tracking | Team wiki or decision log | Formal exception register with revisit dates |
| Escalation path | Direct to accountable executive | Formal escalation chain with documented resolution |
| Cadence | Bi-weekly or monthly | Weekly or per-release-cycle |
| Artifact retention | Lightweight (spreadsheet, shared doc) | Auditable (versioned records, immutable log) |

The mode is a **configuration choice**, not a maturity level. A startup building a non-regulated consumer app operates in lightweight mode. A medical-device team of 8 operates in high-assurance mode. A 200-person platform team may operate parts of its portfolio in lightweight mode and parts in high-assurance.

### Configurable Governance Patterns

No single org chart or governance model is imposed. The skill provides configurable patterns; select and adapt:

| Pattern | When to use | Key trait |
|---------|-------------|-----------|
| **Single accountable owner** | Small team, single product | One person decides; reviews are advisory |
| **Product council** | Multi-team, multi-product | Cross-functional group with defined voting/consensus rules |
| **Tiered review** | Portfolio with varied risk | Lightweight for low-risk; high-assurance for regulated |
| **Delegated authority with escalation** | Scaled organization | Decision rights pre-delegated by category; escalate only exceptions |

Every pattern requires the same outputs: a decision-rights map, review cadences with evidence standards, and escalation paths. Use [templates/operating-model.md](templates/operating-model.md) to capture the selected pattern and configuration.

## Decision Rights

A decision-rights map answers five questions for every decision type:

1. **Who decides?** Named role (not "engineering" or "leadership" — a specific accountable owner).
2. **Who must be consulted?** Roles or individuals whose input is required before the decision.
3. **Who must be informed?** Roles or individuals who are notified after the decision.
4. **What evidence is required?** The minimum evidence standard for this decision type (varies by mode).
5. **What is the escalation path?** Who resolves it when the accountable owner cannot decide or the decision is contested.

Decision types the skill covers:

| Decision type | Typical cadence | Lightweight evidence | High-assurance evidence |
|---------------|----------------|---------------------|------------------------|
| Intake accept/reject | Per-request (continuous) | Problem statement + one signal | Problem statement, cost of delay, strategic alignment score, capacity check |
| Portfolio prioritization | Monthly or quarterly | Relative rank with rationale | Ranked with cost-of-delay, strategic alignment, capacity model, risk assessment |
| Roadmap commitment | Per-planning cycle | Hypothesis + success criteria | Hypothesis, experiment results or market evidence, dependency map, confidence interval |
| Experiment proceed/stop | Per-experiment | Guardrail check + qualitative signal | Statistical analysis, guardrail verification, ethics review, decision rule |
| Launch go/no-go | Per-launch | Readiness checklist + stakeholder sign-off | Full readiness evidence packet, risk acceptance sign-off, rollback plan verified |
| Lifecycle continue/invest/harvest/retire | Per-review cycle | Usage + outcome data, team recommendation | Usage, financial, competitive, and risk data; multi-stakeholder review |

Use [templates/decision-rights-map.md](templates/decision-rights-map.md) to document the map for a specific product or portfolio.

## Review Cadences

Six recurring reviews form the product governance rhythm. Each review has a defined purpose, participants, inputs, outputs, and decision authority.

| Review | Purpose | Typical participants | Key inputs | Key outputs | Decision authority |
|--------|---------|---------------------|------------|-------------|-------------------|
| **Intake / Opportunity review** | Decide which new work enters the product system | Product lead, engineering lead, design lead (varies by pattern) | Problem statement, strategic alignment, rough sizing | Accept/reject/defer decision, assigned owner | Product lead (or council vote) |
| **Portfolio review** | Sequence and resource-allocation across the portfolio | Product council or leadership group | Bet records, capacity model, strategic priorities | Prioritized portfolio, resource allocations, deferrals | Product council or accountable exec |
| **Roadmap review** | Commit, adjust, or defer roadmap items; review evidence updates | Product lead, engineering lead, key stakeholders | Updated bet records, new evidence, dependency status | Updated Now/Next/Later, continue/pause/kill decisions | Product lead with stakeholder input |
| **Experiment review** | Decide whether experiment results support proceeding, iterating, or stopping | Product lead, data/science lead, engineering lead | Experiment readout, guardrail report, decision recommendation | Proceed/stop/pivot decision, updated bet record | Product lead (with science input) |
| **Launch review** | Confirm readiness to ship; accept residual risk | Product lead, engineering lead, QA, security, support, marketing | Readiness evidence packet, risk register, rollback plan | Go/no-go/defer decision, accepted risks | Product lead (go/no-go); risk acceptance may require exec |
| **Lifecycle / Health review** | Assess product health; decide continue/invest/harvest/retire | Product lead, engineering lead, support, finance (high-assurance) | Usage data, outcome metrics, cost data, competitive intel | Lifecycle decision, updated investment level, migration plan if retiring | Product council or accountable exec |

Use [templates/review-cadence.md](templates/review-cadence.md) to configure cadences for a specific operating model. Routes to [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) for roadmap review mechanics, [product-experimentation](../product-experimentation/SKILL.md) for experiment review methods, and product-lifecycle-learning (prose — same-wave skill, directory not yet created) for lifecycle/health review evidence.

## Evidence Standards

Every decision type has a minimum evidence standard. The standard scales with the operating mode. Evidence is classified into four categories in every artifact:

- **Observed** — measured, verified, reproducible data.
- **Inferred** — conclusion from observed data with stated assumptions and confidence.
- **Asserted** — stakeholder claim not yet verified; treated as an assumption.
- **Committed** — a decision with consequences for reversal; recorded with accountable owner and revisit trigger.

Missing required evidence is not a reason to skip a review — it is a reason to **escalate**. A review that proceeds without required evidence must produce an exception record, not silent approval.

## Exceptions and Escalations

### Exception Record

When a governance requirement is waived or deferred, record the exception. Without a record, the exception becomes the new default.

Fields: what was excepted, why, who approved, date approved, when to revisit (specific date or trigger condition), and what evidence (if any) substitutes for the waived requirement.

Use [templates/exception-record.md](templates/exception-record.md).

### Escalation Record

When a decision cannot be resolved at its designated level — because evidence is missing, stakeholders are deadlocked, or the accountable owner cannot decide — escalate. Escalation is not failure; it is the governance system working as designed.

Fields: what was escalated, to whom, why the lower level could not resolve, resolution, date resolved, and closure evidence.

Use [templates/escalation-record.md](templates/escalation-record.md).

## Loading Guide

Load only the file relevant to the current task. Do not load everything at once.

| File | Load when |
|------|-----------|
| [references/discovery-brief.md](references/discovery-brief.md) | You need to understand governance boundaries, ownership, and routing across skills |
| [templates/operating-model.md](templates/operating-model.md) | Designing or configuring a product operating model from scratch |
| [templates/decision-rights-map.md](templates/decision-rights-map.md) | Mapping decision rights for a product or portfolio |
| [templates/review-cadence.md](templates/review-cadence.md) | Configuring review cadences with purposes, participants, inputs, outputs |
| [templates/exception-record.md](templates/exception-record.md) | Recording a waived or deferred governance requirement |
| [templates/escalation-record.md](templates/escalation-record.md) | Recording an escalation through the governance system |

## Working Method

### 1. Select the operating mode

Start every engagement by choosing lightweight or high-assurance mode. Do not default to one. Ask: is this product regulated, safety-critical, or subject to external compliance obligations? If yes, high-assurance. If the team is small and the product is non-regulated, lightweight.

### 2. Choose the governance pattern

Select from single accountable owner, product council, tiered review, or delegated authority with escalation. Adapt, don't copy. Document the choice in the operating model template.

### 3. Map decision rights

For every decision type in scope, fill the decision-rights map: who decides, who is consulted, who is informed, what evidence is required, and where to escalate. Use [templates/decision-rights-map.md](templates/decision-rights-map.md).

### 4. Configure review cadences

Set the purpose, participants, inputs, outputs, and decision authority for each review. Adjust frequency to match the operating mode. Use [templates/review-cadence.md](templates/review-cadence.md).

### 5. Establish evidence standards

Define the minimum evidence standard per decision type, scaled to the operating mode. Record the standard in the decision-rights map. Evidence standards are not aspirational — they gate the decision.

### 6. Record exceptions and escalations

Every exception and escalation gets a dated record with accountable owner and revisit trigger. Exception records prevent waiver-by-neglect. Escalation records make the governance system observable and improvable.

## Routing Table

| When you need... | Load this skill |
|------------------|-----------------|
| Product vision, North Star, competitive positioning | [product-strategy](../product-strategy/SKILL.md) |
| Tactical prioritization (RICE, MoSCoW), decision logs, specs | [product-methodology](../product-methodology/SKILL.md) |
| Outcome roadmaps, strategic bets, portfolio sequencing | [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) |
| Multi-project technical coordination, shared capacity, program benefits, transformation delivery | [technical-program-management](../technical-program-management/SKILL.md) |
| Experiment design, method selection, guardrails, readouts | [product-experimentation](../product-experimentation/SKILL.md) |
| Post-launch learning, lifecycle decisions, assumption updates | product-lifecycle-learning (prose — same-wave skill) |
| Executive decision memos, CoS methods, board materials | [chief-of-staff-methodology](../chief-of-staff-methodology/SKILL.md) |
| Strategic planning, capital allocation, OKR frameworks | [strategy-frameworks](../strategy-frameworks/SKILL.md) |
| Release mechanics, deployment pipelines, rollback plans | [release-engineering](../release-engineering/SKILL.md) |
| Specification-phase gates, acceptance criteria, task planning | [spec-driven-development](../spec-driven-development/SKILL.md) |

## When Not to Use

Do not load this skill for:

- **Executive governance.** Capital allocation, org structure decisions, strategic bets at the company level, or M&A evaluation — route to `chief-of-staff-methodology` or `strategy-frameworks`.
- **Technical delivery gates.** CI/CD pipelines, release approval workflows, deployment checklists, or infrastructure change review — route to `release-engineering` or `spec-driven-development`.
- **Imposing a universal org chart.** The governance patterns are configurable templates, not a mandated structure. If the ask is to design an org chart from scratch, this skill is the wrong tool.
- **Single decisions without a recurring system.** If you need to make one decision (not design the system for making decisions over time), use `product-methodology` for decision logs or `adr-authoring` for architecture decisions.
