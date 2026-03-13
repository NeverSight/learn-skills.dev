---
name: cost-optimization-cloud
description: "Optimize cloud spend with explicit tradeoffs across cost, performance, and reliability. Use when spend or forecast misses budget targets and teams need concrete optimization actions without violating SLOs or compliance constraints; do not use for purely functional product behavior design."
---

# Cost Optimization Cloud

## Overview
Use this skill to produce actionable cloud cost reductions that preserve service quality and operational safety.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Cost breakdown by service/account/environment/tag.
- Utilization telemetry (CPU, memory, I/O, request profile, idle windows).
- Reliability and performance guardrails (SLO, latency, availability).
- Contractual/compliance constraints and migration limits.

## Deliverables
- Prioritized optimization backlog with savings estimate and confidence.
- Risk-assessed rollout sequence.
- Verification plan for savings and regression detection.
- Reversal plan for harmful optimizations.

## Optimization Decision Buckets
- `waste removal`: idle resources, overprovisioned instances, orphaned storage.
- `efficiency`: rightsizing, autoscaling policy tuning, query/request optimization.
- `pricing`: reservations/savings plans, spot usage where safe.
- `architecture`: storage tiering, cache strategy, async/off-peak processing.

## Quick Example
- Observation: cluster CPU < 15% for 14 days, memory < 25%.
- Action: downsize node class + adjust autoscaling floor.
- Guardrail: p95 latency and error rate must remain within pre-change bounds.
- Rollback: revert size within one deployment window if guardrail breaches.

## Quality Standard
- Every recommendation includes expected savings, confidence, and risk.
- Recommendations explicitly state SLO/compliance impact.
- Rollout uses low-blast-radius sequence.
- Post-change metrics and rollback triggers are pre-defined.

## Workflow
1. Identify top cost drivers with workload attribution.
2. Generate candidate actions by decision bucket.
3. Quantify savings, risk, and implementation effort.
4. Sequence actions by ROI and operational safety.
5. Execute incrementally with guardrail monitoring.
6. Validate realized savings and capture lessons.

## Failure Conditions
- Stop when savings action violates SLO/compliance constraints.
- Stop when cost attribution confidence is too low for safe action.
- Escalate when forecast variance remains unexplained after top-driver analysis.
