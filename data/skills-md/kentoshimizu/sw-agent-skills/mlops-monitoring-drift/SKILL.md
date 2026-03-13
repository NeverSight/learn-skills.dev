---
name: mlops-monitoring-drift
description: "MLOps drift monitoring workflow for detecting data drift, concept drift, and quality degradation with actionable response rules. Use when production ML systems need drift detection thresholds and escalation ownership; do not use for model-architecture research decisions."
---

# Mlops Monitoring Drift

## Overview
Use this skill to detect meaningful model degradation early and trigger appropriate remediation actions.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Drift alerting and escalation rules:
  - `references/drift-alerting-escalation-rules.md`

## Templates And Assets
- Drift monitoring policy template:
  - `assets/drift-monitoring-policy-template.md`

## Inputs To Gather
- Drift signals and quality metrics to monitor.
- Alert thresholds and acceptable noise level.
- Escalation owners and response SLA.
- Retraining and rollback policies.

## Deliverables
- Drift monitoring policy and thresholds.
- Alert routing and severity model.
- Response playbook for drift events.

## Workflow
1. Define monitoring policy in `assets/drift-monitoring-policy-template.md`.
2. Validate threshold actionability via `references/drift-alerting-escalation-rules.md`.
3. Test alert behavior with historical replay or backtests.
4. Assign response ownership and SLA per severity.
5. Publish retraining/mitigation decision criteria.

## Quality Standard
- Alerts are actionable, not noise-heavy.
- Severity levels map to clear response ownership.
- Retraining triggers are explicit and auditable.

## Failure Conditions
- Stop when drift thresholds are not operationally actionable.
- Stop when alerts have no clear owner.
- Escalate when degradation risk remains unmanaged.
