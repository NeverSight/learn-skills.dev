---
name: sre-sli-slo
description: "SRE SLI/SLO workflow for reliability target definition, measurable telemetry mapping, and error-budget policy. Use when service reliability objectives must be formalized with escalation actions; do not use for business-feature implementation logic."
---

# Sre Sli Slo

## Overview
Use this skill to define reliability goals that directly drive operational decisions.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- SLO target setting rules:
  - `references/slo-target-setting-rules.md`

## Templates And Assets
- SLI/SLO catalog template:
  - `assets/sli-slo-catalog-template.csv`
- Error budget policy template:
  - `assets/error-budget-policy-template.md`

## Inputs To Gather
- Service criticality and user-impact expectations.
- Available telemetry quality and coverage.
- Historical reliability and incident patterns.
- Operational response and escalation constraints.

## Deliverables
- SLI/SLO catalog with ownership.
- Error budget policy with action triggers.
- Reliability governance and review cadence.

## Workflow
1. Define SLI/SLO set in `assets/sli-slo-catalog-template.csv`.
2. Set targets using `references/slo-target-setting-rules.md`.
3. Define burn-rate actions in `assets/error-budget-policy-template.md`.
4. Validate measurability from telemetry.
5. Publish ownership and escalation policy.

## Quality Standard
- SLO targets are measurable and risk-aligned.
- Error budget actions are explicit and owned.
- Reliability decisions are traceable to telemetry.

## Failure Conditions
- Stop when SLOs cannot be measured reliably.
- Stop when error budget actions are undefined.
- Escalate when reliability risk exceeds accepted policy.
