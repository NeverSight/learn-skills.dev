---
name: infrastructure-as-code
description: "Declarative infrastructure change workflow for plan-reviewed operations, state safety, and drift prevention. Use when infrastructure changes must be represented declaratively with reviewable plans and controlled apply; do not use for API contract design or requirement prioritization."
---

# Infrastructure As Code

## Overview
Use this skill to manage infrastructure changes as reviewable, reproducible code with explicit state and drift controls.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- State safety rules:
  - `references/iac-state-safety-rules.md`

## Templates And Assets
- IaC change plan template:
  - `assets/iac-change-plan-template.md`
- IaC review checklist:
  - `assets/iac-review-checklist.md`
- Drift response runbook:
  - `assets/drift-response-runbook-template.md`

## Inputs To Gather
- Target environment, module scope, and change intent.
- State mutation risk and blast radius expectations.
- Security/compliance constraints.
- Drift detection and response capabilities.

## Deliverables
- IaC change plan with risk and rollback notes.
- Reviewed plan/apply decision record.
- Drift response process with ownership.
- Verification evidence after apply.

## Workflow
1. Capture scope and risk in `assets/iac-change-plan-template.md`.
2. Evaluate state safety with `references/iac-state-safety-rules.md`.
3. Review plan and apply readiness via `assets/iac-review-checklist.md`.
4. Execute controlled apply and validate expected state.
5. Define drift response using `assets/drift-response-runbook-template.md`.

## Quality Standard
- Infrastructure changes are fully reviewable before apply.
- State risks and rollback feasibility are explicit.
- Drift detection and remediation ownership are defined.
- Declarative source remains the single source of truth.

## Failure Conditions
- Stop when changes cannot be reviewed declaratively before apply.
- Stop when state risk is unknown or rollback is unplanned.
- Escalate when drift risk exceeds operational policy thresholds.
