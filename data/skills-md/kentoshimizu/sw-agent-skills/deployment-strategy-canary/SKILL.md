---
name: deployment-strategy-canary
description: "Design canary rollout strategy with progressive traffic steps, guardrail metrics, and automated stop/rollback decisions. Use when releases need incremental risk containment and evidence-based promotion gates; do not use for full-environment cutover planning where blue-green is required."
---

# Deployment Strategy Canary

## Overview
Use this skill to release changes gradually while measuring real-user impact before broad rollout.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Promotion and stop decision rules:
  - `references/canary-promotion-rules.md`

## Templates And Assets
- Rollout plan template:
  - `assets/canary-rollout-plan-template.md`
- Guardrail matrix template:
  - `assets/canary-guardrail-matrix-template.csv`

## Inputs To Gather
- Critical SLOs and business guardrail metrics.
- Traffic segmentation options (region, tenant, cohort).
- Maximum acceptable degradation and rollback thresholds.
- Release window and incident response readiness.

## Deliverables
- Canary progression plan (percentage/time/gates).
- Guardrail matrix and promotion rules.
- Automatic stop/rollback policy.
- Post-promotion verification and observation window plan.

## Quick Progression Example
- Steps: 1% -> 5% -> 20% -> 50% -> 100%.
- Hold at each step for fixed minimum time and metric stability checks.
- Auto-rollback if error rate rises > threshold or SLO drops below floor.

## Quality Standard
- Promotion gates are objective and pre-registered.
- Guardrails include technical and business impact signals.
- Rollback automation/authority is clearly defined.
- Segment choice avoids exposing highest-risk cohorts first.

## Workflow
1. Define canary audience and progression steps in `assets/canary-rollout-plan-template.md`.
2. Set promotion and rollback criteria for each step using `assets/canary-guardrail-matrix-template.csv`.
3. Deploy canary and monitor guardrails in real time.
4. Promote only when criteria pass under `references/canary-promotion-rules.md`; otherwise stop/rollback.
5. Complete rollout and run post-release verification.

## Failure Conditions
- Stop when promotion criteria are ambiguous or non-measurable.
- Stop when telemetry cannot detect regressions quickly.
- Escalate when rollback path is manual-only for high-criticality services.
