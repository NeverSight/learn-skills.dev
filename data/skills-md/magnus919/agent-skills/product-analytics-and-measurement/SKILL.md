---
name: product-analytics-and-measurement
description: >-
  Define observable, governed evidence for product outcomes through metric
  trees, event/tracking plans, instrumentation QA, and measurement governance. Use
  when defining product metrics, designing tracking plans, building event taxonomies,
  running product funnels or cohort analysis, setting up dashboard contracts, or
  auditing instrumentation quality. Do NOT use for statistical inference or
  experiment design (route to data-scientist), data pipeline implementation (route
  to data-engineering), data architecture decisions (route to data-architect),
  observability or infrastructure monitoring (route to site-reliability-engineering),
  or general business intelligence and dashboard building (route to BI tooling).
license: MIT
metadata:
  tags: product-analytics, measurement, metrics, instrumentation, tracking-plan,
    event-taxonomy, funnels, cohorts, retention, adoption, dashboard-contracts,
    privacy-aware-measurement
---

# Product Analytics and Measurement

A dedicated operating method for turning intended product outcomes into observable,
governed evidence. This skill covers the full measurement lifecycle: from defining
what success looks like through metric trees and leading/lagging indicators, to
specifying how that success is tracked through event taxonomies and tracking plans,
to verifying that the instrumentation actually captures what it claims.

## Loading Guide

Load this skill when the task involves any of:

| Trigger | What to load |
|---------|-------------|
| Define product outcomes, North Star, or success metrics | `SKILL.md` + `references/metric-tree.md` |
| Design an event taxonomy or tracking plan | `SKILL.md` + `templates/tracking-plan.md` |
| Audit or QA instrumentation quality | `SKILL.md` + `templates/instrumentation-qa-checklist.md` |
| Build product funnels, path analysis, or cohort definitions | `SKILL.md` + `references/metric-tree.md` |
| Set up a dashboard contract or measurement governance | `SKILL.md` + `templates/outcome-review.md` |
| Resolve conflicting metric definitions across teams | `SKILL.md` + `references/discovery-brief.md` (ownership boundaries) |
| Design a privacy-aware measurement strategy | `SKILL.md` |

## When to Use

- You need to define measurable outcomes, metric trees, and leading/lagging indicators for a product (SaaS, internal tool, public service, or consumer).
- You need a tracking plan that specifies events, properties, identity resolution, session boundaries, data quality rules, and ownership.
- You need to verify that existing instrumentation produces trustworthy data.
- You need a dashboard contract that pins metric definitions, sources, refresh cadences, and ownership.
- You need a product outcome review cadence that ties measurements back to decisions.

## When Not to Use

This skill does **not** replace:

- **Data architecture** — schema design, storage selection, data modeling at the infrastructure level belong to `../data-architect/SKILL.md`.
- **Data engineering** — pipeline implementation, ETL/ELT, dbt models, and data quality monitoring at the operational level belong to `../data-engineering/SKILL.md`.
- **Statistical inference** — experiment design, hypothesis testing, causal inference, and model selection belong to `../data-scientist/SKILL.md`.
- **Observability** — system health, latency, error budgets, and infrastructure monitoring belong to `../site-reliability-engineering/SKILL.md`.
- **Business intelligence** — dashboard building, report generation, and data visualization as an end in itself. This skill governs the *measurement contract* and *metric definitions* that feed BI, not the BI layer itself.

This skill also does **not** prescribe universal benchmark thresholds. Every metric target, retention curve, or conversion rate cited in outputs is labeled as contextual — tied to the specific product, market, stage, and business model under discussion.

## Core Concepts

### Metric Tree

A hierarchical decomposition of a North Star or primary outcome into its constituent drivers. Each node in the tree is:

- **Observable** — it can be measured from instrumentation or a defined data source.
- **Actionable** — a change in the metric suggests a specific product or operational response.
- **Owned** — exactly one team or role is accountable for its definition, collection, and interpretation.

The metric tree distinguishes **leading indicators** (predictive, sensitive to change) from **lagging indicators** (confirmatory, slow to move) and pairs every metric with at least one **countermetric** (a guardrail that detects adverse side effects). See `references/metric-tree.md`.

### Event and Tracking Plan

An **event** is a recorded action or state change with a timestamp, actor, and properties. A **tracking plan** is the contract that makes events trustworthy:

- **Event name and taxonomy** — consistent naming conventions, versioned, with a catalog of standard events.
- **Properties** — typed fields with allowed values, required vs optional, and default behaviors.
- **Identity resolution** — how actors are identified across sessions, devices, and authentication states (anonymous id, logged-in id, merged identities).
- **Session definition** — timeout rules, activity boundaries, and cross-platform session continuity.
- **Data quality rules** — validation checks (null rates, freshness, cardinality bounds, distribution drift).
- **Ownership** — who defines the event, who instruments it, who consumes it, and who is paged when it breaks.

See `templates/tracking-plan.md`.

### Instrumentation QA

Before a metric appears on a dashboard, the instrumentation that produces it must be verified. The QA checklist covers:

- **Client-side** — event firing on correct triggers, property values match UI state, no duplicate firings, no missing required properties.
- **Server-side** — event ingestion, transformation correctness, identity stitching, timestamp integrity.
- **Pipeline** — schema compatibility, no silent drops, latency within SLA, deduplication behavior.
- **End-to-end** — the metric computed from raw events matches the value observed through a manual product walkthrough.

See `templates/instrumentation-qa-checklist.md`.

### Privacy-Aware Measurement

Every measurement design must address:

- **Consent boundary** — what is measured before consent vs after; what is never measured.
- **Minimization** — collect only what the metric requires; avoid speculative properties.
- **Aggregation threshold** — metrics reported only when the cohort meets a minimum size.
- **Retention and deletion** — raw event retention period; how measurement continues after data deletion requests.
- **Jurisdictional awareness** — note when metric collection crosses regulatory boundaries (GDPR, CCPA, etc.).

### Dashboard Contracts

A dashboard without a contract is an argument waiting to happen. A dashboard contract pins:

- **Metric definition** — the exact formula, data source, and filter conditions.
- **Refresh cadence** — how often the dashboard updates and the acceptable staleness.
- **Owner** — who is accountable for accuracy and who to contact when numbers look wrong.
- **Audience and decision** — who consumes this dashboard and what decision it informs.
- **Thresholds and alerts** — when a metric value triggers investigation (not a universal benchmark, but a product-specific threshold).

### Decision Cadence

Measurement without a decision cadence is measurement theater. This skill guides the rhythm:

- **Daily** — operational metrics, anomaly detection, automated alerts.
- **Weekly** — leading indicators, experiment readouts, funnel health.
- **Monthly** — outcome reviews, metric tree health, countermetric checks.
- **Quarterly** — North Star reassessment, metric tree restructuring, tracking plan deprecation.

## Working Method

1. **Start with the outcome, not the event.** Define what success looks like and decompose it into a metric tree before designing any tracking.
2. **Verify measurability before committing.** If a metric cannot be observed from available or feasibly instrumented data sources, reject it — do not fabricate a proxy without documenting the instrumentation constraint.
3. **Design the tracking plan as a contract.** Every event has a defined owner, schema, quality rule, and consumer. No orphan events.
4. **QA instrumentation before trusting the dashboard.** Run the instrumentation QA checklist on every new or changed event before the metric enters a decision cadence.
5. **Pair every metric with a countermetric.** For every metric that drives a decision, define at least one countermetric that would reveal an adverse side effect.
6. **Label every threshold as contextual.** State the product, market, stage, and business model that the threshold assumes.
7. **Review measurement governance periodically.** Deprecate unused events, retire stale metrics, update metric trees when the product strategy shifts.

## File Map

| Path | Loaded when |
|------|------------|
| `references/discovery-brief.md` | Understanding ownership boundaries and how this skill relates to existing catalog skills |
| `references/metric-tree.md` | Building or reviewing a metric tree, defining leading/lagging indicators, selecting countermetrics |
| `templates/tracking-plan.md` | Designing an event taxonomy or writing a tracking plan contract |
| `templates/instrumentation-qa-checklist.md` | Auditing or verifying instrumentation quality before trusting metrics |
| `templates/outcome-review.md` | Running a product outcome review or setting up a measurement decision cadence |
| `evals/evals.json` | Evaluating the skill's output quality across representative scenarios |

## Related Skills

### Routes to (resolvable, existing skills)

- `../data-engineering/SKILL.md` — for pipeline implementation, ETL/ELT, dbt models, and data quality monitoring at the operational level.
- `../data-scientist/SKILL.md` — for statistical inference, experiment design, hypothesis testing, causal inference, and model selection.
- `../product-strategy/SKILL.md` — for North Star definition, product vision, PMF assessment, and roadmap prioritization.
- `../go-to-market/SKILL.md` — for growth modeling, CAC/LTV, cohort analysis by channel, and PLG/SLG funnel metrics.
- `../financial-modeling/SKILL.md` — for unit economics, ARR/MRR, churn, NDR, and SaaS operating metrics definitions.

### Feeds (prose references to skills not yet landed)

This skill produces measurement contracts, metric trees, and tracking plans that feed:

- **product-roadmapping-and-portfolio** — roadmap decisions grounded in measured outcomes.
- **product-experimentation** — experiment design and readout on a trustworthy measurement foundation.
- **product-adoption** — adoption funnels, activation metrics, and time-to-value measurement.
- **conditional-customer-success** — account health scores and customer outcome tracking.
- **product-lifecycle-learning** — post-launch learning loops and metric-informed iteration.
