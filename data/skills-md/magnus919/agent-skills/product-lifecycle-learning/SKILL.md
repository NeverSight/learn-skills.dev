---
name: product-lifecycle-learning
description: >-
  Compare intended product outcomes against observed results to close the
  launch-to-learning loop: collect post-launch evidence, distinguish expected
  from observed from uncertain from inferred claims, update assumptions, assess
  feature health, and choose among
  continue/improve/harvest/pivot/pause/retire — including retirement lifecycles
  with deprecation, migration, customer treatment, and retained reusable
  learning. Do not use for incident postmortems or root-cause analysis (routes
  to incident-learning or site-reliability-engineering); do not use for
  analytics instrumentation or metric dashboard design (routes to
  product-analytics-and-measurement); do not use arbitrary thresholds as
  universal retirement rules — decisions require human judgment and context.
license: MIT
metadata:
  tags: product-lifecycle-learning, post-launch-review, outcome-review,
    feature-health, assumption-update, retirement-decisions, deprecation,
    sunset-planning, retained-learning, evidence-ledger, epistemic-discipline,
    lifecycle-closure
---

# Product Lifecycle Learning

Close the loop from launch to learning. This skill compares what was intended against
what actually happened, maintains an evidence-backed assumption ledger, assesses
feature health, and makes disciplined continue/improve/harvest/pivot/pause/retire
decisions — including full retirement lifecycles. It produces a durable retained
learning record that feeds back into roadmap, analytics, adoption, experimentation,
and future specifications.

## Loading Guide

Load only the reference or template relevant to the task. Do not load every file at once.

| File | Load when |
|------|-----------|
| [references/discovery-brief.md](references/discovery-brief.md) | You need to understand how lifecycle-learning concepts map across skills and where this skill's boundaries are |
| [references/epistemic-discipline.md](references/epistemic-discipline.md) | You need the full taxonomy for classifying claims as expected, observed, uncertain, or inferred |
| [references/retirement-lifecycle.md](references/retirement-lifecycle.md) | Planning a feature or product retirement, including deprecation, migration, customer treatment, and internal cleanup |
| [references/feedback-destinations.md](references/feedback-destinations.md) | Routing learning outputs to the right downstream skill — roadmap, analytics, adoption, experimentation, or specification |
| [templates/outcome-review.md](templates/outcome-review.md) | Conducting a structured post-launch outcome review comparing expected vs. observed |
| [templates/assumption-ledger-update.md](templates/assumption-ledger-update.md) | Updating the assumption ledger with new evidence and confidence shifts |
| [templates/feature-health-record.md](templates/feature-health-record.md) | Assessing feature health across multiple dimensions and surfacing signals |
| [templates/retirement-decision.md](templates/retirement-decision.md) | Making and recording a justified retirement or continuation decision |
| [templates/sunset-plan.md](templates/sunset-plan.md) | Planning deprecation communication, migration paths, customer treatment, and internal cleanup |
| [templates/retained-learning-record.md](templates/retained-learning-record.md) | Capturing durable reusable learning that survives beyond the feature |

## Core Methodology

### The Launch-to-Learning Loop

```
LAUNCH → [OBSERVE] → [COMPARE] → [IDENTIFY GAPS] → [UPDATE ASSUMPTIONS] → [ASSESS HEALTH] → [DECIDE] → [CAPTURE LEARNING] → (feed back)
              |            |              |                 |                    |               |               |
         Collect      Expected vs.    Gap analysis     Assumption         Feature health    Continue /      Retained
         outcome      observed        with confidence  ledger update      dimensions        Improve /       learning
         data         outcomes        intervals                                              Harvest /       record
                                                                                            Pivot /
                                                                                            Pause /
                                                                                            Retire
```

The loop starts after launch (the feature or capability is live and generating data) and ends with a
durable learning artifact that feeds the next cycle of roadmap, analytics, adoption, experimentation,
and specification work.

### Stage-by-Stage

| Stage | Input | Activity | Output |
|-------|-------|----------|--------|
| **Observe** | Analytics data, adoption metrics, user feedback, support tickets, operational metrics | Collect outcome evidence from observed behavior and system data. Distinguish signal from noise. Flag missing or low-confidence data. | Collected outcome data with confidence labels |
| **Compare** | Expected outcomes (from spec/roadmap), observed outcomes, confidence intervals | Compare the two; identify alignment, deviation, and surprise. Do not conflate expectation with observation. | Gap analysis: what matched, what diverged, what was ambiguous |
| **Identify gaps** | Gap analysis, assumption ledger | Identify which assumptions held and which broke. Distinguish between measurement gaps (could not observe) and outcome gaps (observed deviation). | Assumption gap register with confidence |
| **Update assumptions** | Assumption gap register, prior assumption ledger | Revise assumptions: strengthen confirmed ones, weaken contradicted ones, add new ones surfaced by the data. Record confidence shifts. | Updated assumption ledger. Use [templates/assumption-ledger-update.md](templates/assumption-ledger-update.md). |
| **Assess health** | Updated assumptions, adoption data, operational metrics, user feedback | Evaluate feature health across adoption, technical, operational, and strategic dimensions. Do not reduce to a single score. | Feature health assessment. Use [templates/feature-health-record.md](templates/feature-health-record.md). |
| **Decide** | Feature health assessment, business context, portfolio priorities | Choose one of six lifecycle decisions. The decision requires human judgment; no automated threshold. | Decision record with accountable owner. Use [templates/retirement-decision.md](templates/retirement-decision.md). |
| **Capture learning** | Decision record, gap analysis, updated assumptions, context | Produce a durable retained learning record: what was learned, why, and how it should inform future work. Not a transient meeting summary. | Retained learning record. Use [templates/retained-learning-record.md](templates/retained-learning-record.md). |
| **Feed back** | Retained learning record | Route learning to downstream skills: roadmap, analytics, adoption, experimentation, specifications. See [references/feedback-destinations.md](references/feedback-destinations.md). | Routed learning outputs |

### Epistemic Discipline

Every claim in lifecycle-learning output is classified into exactly one of four categories. These are not
conflated; a comparison is not an observation, and an inference is not a fact.

| Category | Definition | Example | Source |
|----------|-----------|---------|--------|
| **Expected** | What was intended or predicted before launch | "We expected activation to reach 60% within 30 days" | Spec, roadmap, launch brief |
| **Observed** | What actually happened, measured from data | "Activation reached 43% at 30 days (95% CI: 39-47%)" | Analytics, adoption data, operational metrics |
| **Uncertain** | What is ambiguous, noisy, or contested | "Attribution is confounded by a simultaneous pricing change; cannot isolate feature effect" | Confidence intervals, conflicting signals, data-quality issues |
| **Inferred** | What is concluded from evidence, with reasoning | "The gap between expected 60% and observed 43% suggests the onboarding redesign did not reduce time-to-value as hypothesized; the pricing change confound means we cannot rule out an external cause" | Reasoned implication from evidence |

Full taxonomy and field guide in [references/epistemic-discipline.md](references/epistemic-discipline.md).

### Lifecycle Decisions

Six outcomes are available after assessment. The choice requires human judgment informed by evidence;
no numeric threshold or automated rule replaces context and accountability.

| Decision | Meaning | Typical evidence profile | Follow-up |
|----------|---------|--------------------------|-----------|
| **Continue** | Keep as-is; feature is healthy | Outcomes match or exceed expectations; stable, low-risk | Schedule next review |
| **Improve** | Invest in enhancement | Adoption gap exists but fixable; underlying need confirmed | Feed roadmap and experimentation |
| **Harvest** | Reduce investment, maintain for existing users | Declining growth but stable base; not worth expanding | Monitor for retirement signals |
| **Pivot** | Change direction significantly | Need confirmed but current approach failed | Feed roadmap, discovery, experimentation |
| **Pause** | Temporarily halt investment | Ambiguous results, external confounds, or resource constraint | Schedule re-assessment with new evidence |
| **Retire** | Deprecate and remove | Sustained non-adoption, replacement exists, or strategic misalignment | Execute retirement lifecycle |

### Retirement Lifecycle

When the decision is Retire, a structured retirement lifecycle covers the full path from deprecation
announcement through internal cleanup. Full detail in [references/retirement-lifecycle.md](references/retirement-lifecycle.md).

| Phase | Activity | Template |
|-------|----------|----------|
| **Deprecation communication** | Announce retirement: timeline, rationale, alternatives. Target affected users with segmentation. | [templates/sunset-plan.md](templates/sunset-plan.md) |
| **Migration path** | Provide migration tooling, documentation, and support for existing users. Define the recommended path. | [templates/sunset-plan.md](templates/sunset-plan.md) |
| **Customer treatment** | Support commitments during sunset: data export, grace periods, extended support windows, SLA preservation, refund/credit policies where applicable. Coordinate with customer-success. | [templates/sunset-plan.md](templates/sunset-plan.md); route communication plans to `conditional-customer-success` |
| **Internal cleanup** | Remove feature flags, archive code, update documentation, retire monitoring and alerting, reclaim infrastructure. | [templates/sunset-plan.md](templates/sunset-plan.md) |
| **Learning closure** | Capture what the feature's lifecycle taught — not a postmortem, but a closure record that completes the learning loop. | [templates/retained-learning-record.md](templates/retained-learning-record.md) |

### Retained Learning Record

Every lifecycle-learning cycle produces a durable retained learning record — not a transient meeting
summary. The record captures:

- What the feature or capability was intended to achieve (expected outcomes)
- What actually happened (observed outcomes, with confidence)
- What was uncertain and why
- What assumptions were updated and how
- What decision was made (continue/improve/harvest/pivot/pause/retire) and who made it
- Why that decision was reached, with evidence
- What should inform future decisions — reusable patterns, anti-patterns, assumptions to test next time
- Where the learning was routed (roadmap, analytics, adoption, experimentation, specifications)

This record is the durable learning artifact. It is the evidence that the launch-to-learning loop
actually closed.

## When Not to Use

This skill does **not** own:

- **Incident postmortems, root-cause analysis, or operational incident review** — these belong to `incident-learning` (not yet landed) and [../site-reliability-engineering/SKILL.md](../site-reliability-engineering/SKILL.md). Lifecycle-learning consumes incident signals as input but does not produce postmortems.
- **Analytics instrumentation, metric dashboard design, tracking-plan creation, or event taxonomy** — these belong to [../product-analytics-and-measurement/SKILL.md](../product-analytics-and-measurement/SKILL.md). Lifecycle-learning consumes analytics data as input but does not own measurement infrastructure.
- **Customer-success account management, renewal decisions, or health scoring** — these belong to `conditional-customer-success` (not yet landed). Lifecycle-learning routes retirement communication plans and customer-treatment strategies there.
- **Roadmap prioritization or portfolio allocation** — these belong to [../product-roadmapping-and-portfolio/SKILL.md](../product-roadmapping-and-portfolio/SKILL.md). Lifecycle-learning feeds evidence into roadmap decisions but does not make them.
- **Arbitrary or automated retirement thresholds** — this skill never applies rules like "retire if DAU < 100" or "kill if NPS < 30" without context about the product, market, user base, and alternatives. Retirement decisions require human judgment and named accountability.

## Routing and Feedback

### Inputs (consumed by lifecycle-learning)

| Input | Source |
|-------|--------|
| Expected outcomes, acceptance criteria | [../spec-driven-development/SKILL.md](../spec-driven-development/SKILL.md), roadmap briefs |
| Observed outcomes, metric data, funnels, cohorts | [../product-analytics-and-measurement/SKILL.md](../product-analytics-and-measurement/SKILL.md) |
| Adoption evidence, activation rates, retention signals | [../product-adoption/SKILL.md](../product-adoption/SKILL.md) |
| Experiment results, readout learning entries | [../product-experimentation/SKILL.md](../product-experimentation/SKILL.md) |
| Incident signals, reliability data | [../site-reliability-engineering/SKILL.md](../site-reliability-engineering/SKILL.md), `incident-learning` |
| Customer feedback, support trends, health signals | `conditional-customer-success` |

### Outputs (produced by lifecycle-learning, routed to)

| Output | Destination | Purpose |
|--------|-------------|---------|
| Revised assumptions, decision evidence | [../product-roadmapping-and-portfolio/SKILL.md](../product-roadmapping-and-portfolio/SKILL.md) | Roadmap updates, bet re-evaluation |
| Metric refinement needs, measurement gaps | [../product-analytics-and-measurement/SKILL.md](../product-analytics-and-measurement/SKILL.md) | Improve instrumentation, close measurement gaps |
| Adoption pattern changes, behavior insights | [../product-adoption/SKILL.md](../product-adoption/SKILL.md) | Adoption strategy adjustments |
| New hypotheses, experiment ideas | [../product-experimentation/SKILL.md](../product-experimentation/SKILL.md) | Feed experimentation pipeline |
| Spec improvements, acceptance-criteria refinements | [../spec-driven-development/SKILL.md](../spec-driven-development/SKILL.md) | Future specification quality |
| Retirement communication plans, migration coordination, customer treatment during sunset | `conditional-customer-success` | Customer-facing retirement execution; prose reference (skill not yet landed) |
| Incident-driven learning signals | `incident-learning` | Incident-driven learning loop; prose reference (skill not yet landed) |

At least five feedback destinations must be updated per cycle: roadmap, analytics, adoption,
experimentation, and specifications. Additional routing to customer-success and incident-learning
is conditional on the decision.

## File Map

| File | Purpose | Load when |
|------|---------|-----------|
| [references/discovery-brief.md](references/discovery-brief.md) | Maps existing lifecycle, learning, and retirement material; ownership boundaries | Understanding the skill's place in the catalog |
| [references/epistemic-discipline.md](references/epistemic-discipline.md) | Full taxonomy: expected / observed / uncertain / inferred with field guide | Classifying claims in any lifecycle-learning output |
| [references/retirement-lifecycle.md](references/retirement-lifecycle.md) | Complete retirement lifecycle: deprecation, migration, customer treatment, internal cleanup | Retirement decision or sunset planning |
| [references/feedback-destinations.md](references/feedback-destinations.md) | Detailed routing guide for each feedback destination | Routing learning outputs to downstream skills |
| [templates/outcome-review.md](templates/outcome-review.md) | Structured post-launch outcome review | Conducting an outcome review |
| [templates/assumption-ledger-update.md](templates/assumption-ledger-update.md) | Assumption ledger update with confidence shifts | Updating assumptions after new evidence |
| [templates/feature-health-record.md](templates/feature-health-record.md) | Multi-dimensional feature health assessment | Assessing feature health |
| [templates/retirement-decision.md](templates/retirement-decision.md) | Justified retirement or continuation decision record | Making a lifecycle decision |
| [templates/sunset-plan.md](templates/sunset-plan.md) | Deprecation communication, migration, customer treatment, internal cleanup plan | Planning a retirement execution |
| [templates/retained-learning-record.md](templates/retained-learning-record.md) | Durable reusable learning artifact | Capturing learning that survives the feature |

## Related Skills

- [../product-analytics-and-measurement/SKILL.md](../product-analytics-and-measurement/SKILL.md) — Owns instrumentation and metric definition. Lifecycle-learning consumes analytics outputs.
- [../product-adoption/SKILL.md](../product-adoption/SKILL.md) — Owns adoption diagnostics and strategy. Lifecycle-learning consumes adoption evidence.
- [../product-experimentation/SKILL.md](../product-experimentation/SKILL.md) — Owns experiment design and readout. Lifecycle-learning consumes experiment results.
- [../product-roadmapping-and-portfolio/SKILL.md](../product-roadmapping-and-portfolio/SKILL.md) — Owns roadmap and portfolio decisions. Lifecycle-learning feeds evidence.
- [../spec-driven-development/SKILL.md](../spec-driven-development/SKILL.md) — Owns specifications and acceptance criteria. Lifecycle-learning feeds spec improvements.
- [../site-reliability-engineering/SKILL.md](../site-reliability-engineering/SKILL.md) — Owns operational reliability. Lifecycle-learning consumes incident signals.
- `conditional-customer-success` — Consumer for retirement communication plans, customer treatment during sunset, migration support coordination. Prose reference; skill not yet landed.
- `incident-learning` — Destination for incident-driven learning signals. Prose reference; skill not yet landed.
