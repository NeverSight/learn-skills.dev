---
name: observability-metrics
description: "Observability metrics workflow for metric model design aligned to service health and business impact. Use when teams define or revise service metrics/SLIs for reliable health and capacity decisions; do not use for business-feature implementation logic."
---

# Observability Metrics

## Overview
Use this skill to define metrics that reflect real reliability and business impact, not vanity signals.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Metric cardinality and SLI rules:
  - `references/metric-cardinality-and-sli-rules.md`

## Templates And Assets
- Metrics taxonomy template:
  - `assets/metrics-taxonomy-template.csv`
- Metrics quality checklist:
  - `assets/metrics-quality-checklist.md`

## Inputs To Gather
- Service health objectives and user-impact expectations.
- Capacity and performance decision needs.
- Current metric set and cardinality risks.
- Dashboard and alert consumer requirements.

## Deliverables
- Metrics taxonomy and ownership mapping.
- SLI-aligned metric set.
- Dashboard/alert readiness evidence.

## Workflow
1. Define metric taxonomy in `assets/metrics-taxonomy-template.csv`.
2. Apply SLI/cardinality rules from `references/metric-cardinality-and-sli-rules.md`.
3. Validate coverage and quality with `assets/metrics-quality-checklist.md`.
4. Tune labels and aggregation for operability.
5. Publish metric governance and maintenance plan.

## Quality Standard
- Metrics support reliability and capacity decisions.
- Label strategy avoids high-cardinality failure.
- Ownership and operational usage are explicit.

## Failure Conditions
- Stop when key health indicators are missing or misleading.
- Stop when cardinality makes metrics operationally unstable.
- Escalate when metric gaps block incident response.
