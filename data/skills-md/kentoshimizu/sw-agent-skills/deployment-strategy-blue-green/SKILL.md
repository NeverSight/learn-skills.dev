---
name: deployment-strategy-blue-green
description: "Design blue-green deployment strategy with explicit cutover checks, rollback triggers, and state/data compatibility safeguards. Use when release risk requires fast rollback and environment-level switch control; do not use for canary-percentage experimentation policy design."
---

# Deployment Strategy Blue Green

## Overview
Use this skill to design low-risk cutovers between two production environments with clear rollback paths.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Data/schema compatibility guidance:
  - `references/blue-green-data-compatibility.md`

## Templates And Assets
- Cutover runbook template:
  - `assets/blue-green-cutover-runbook-template.md`
- Readiness checklist:
  - `assets/blue-green-readiness-checklist.md`

## Inputs To Gather
- Service criticality and acceptable deployment interruption.
- Data/schema compatibility constraints between old/new versions.
- Traffic switching mechanism (LB, DNS, gateway, mesh).
- Health/SLO guardrails and rollback authority.

## Deliverables
- Blue-green rollout and cutover plan.
- Readiness checklist for green environment.
- Rollback trigger matrix and execution runbook.
- Post-cutover verification checklist.

## Quick Cutover Example
1. Deploy to green and run smoke + synthetic checks.
2. Mirror a small read-only validation traffic slice.
3. Switch 100% traffic at cutover window.
4. Rollback immediately if p95/error guardrails breach for N minutes.

## Quality Standard
- Green environment parity is validated before switch.
- Cutover decision uses explicit health/SLO criteria.
- Rollback path is operationally tested and time-bounded.
- Stateful compatibility risks are mitigated in advance.

## Workflow
1. Define cutover/rollback criteria and owners.
2. Validate environment parity and dependencies using `assets/blue-green-readiness-checklist.md`.
3. Execute pre-cutover verification in green and capture steps in `assets/blue-green-cutover-runbook-template.md`.
4. Perform controlled traffic switch.
5. Monitor guardrails and either stabilize or rollback.
6. Decommission blue only after stabilization window.

## Failure Conditions
- Stop when rollback cannot be executed within required recovery time.
- Stop when data/schema compatibility between blue/green is unresolved.
- Escalate when guardrails are missing for critical user paths.
