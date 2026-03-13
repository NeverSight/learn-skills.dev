---
name: observability-alerting
description: "Observability alerting workflow for signal quality, routing policy, and actionable thresholds. Use when alert rules need design or tuning to detect incidents with clear ownership and noise control; do not use for business-feature implementation logic."
---

# Observability Alerting

## Overview
Use this skill to design alerting that catches real incidents quickly without overwhelming responders.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Alert threshold actionability rules:
  - `references/alert-threshold-actionability-rules.md`

## Templates And Assets
- Alert catalog template:
  - `assets/alert-catalog-template.csv`
- Alert noise review checklist:
  - `assets/alert-noise-review-checklist.md`

## Inputs To Gather
- Critical user/system failure modes.
- Available telemetry signals and quality.
- On-call routing and escalation policy.
- Historical false-positive/false-negative patterns.

## Deliverables
- Alert catalog with severity, owner, and runbook linkage.
- Threshold and routing policy.
- Noise-control and tuning plan.

## Workflow
1. Build initial alert catalog in `assets/alert-catalog-template.csv`.
2. Set thresholds using `references/alert-threshold-actionability-rules.md`.
3. Define routing/escalation by severity.
4. Validate with `assets/alert-noise-review-checklist.md`.
5. Publish tuning backlog and ownership.

## Quality Standard
- Alerts are actionable and owned.
- Critical paths have coverage with bounded noise.
- Paging vs non-paging intent is explicit.

## Failure Conditions
- Stop when alerts are noisy, non-actionable, or ownerless.
- Stop when critical failure modes lack alert coverage.
- Escalate when alert quality risks SLO breach response.
