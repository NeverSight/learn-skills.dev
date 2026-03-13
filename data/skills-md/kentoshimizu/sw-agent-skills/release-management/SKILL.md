---
name: release-management
description: "Release management workflow for go/no-go governance, readiness evidence, and rollback preparedness. Use when release decisions require explicit criteria and cross-team sign-off; do not use for application-domain algorithm or schema decisions."
---

# Release Management

## Overview
Use this skill to run release decisions with auditable evidence and explicit risk ownership.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Release signoff rules:
  - `references/release-signoff-rules.md`

## Templates And Assets
- Release readiness checklist:
  - `assets/release-readiness-checklist-template.md`
- Go/no-go decision log:
  - `assets/go-no-go-decision-log-template.md`

## Inputs To Gather
- Release scope and risk profile.
- Quality, security, and operational readiness evidence.
- Rollout and rollback execution readiness.
- Required approvers and escalation policy.

## Deliverables
- Readiness checklist with evidence status.
- Go/no-go decision record with conditions.
- Residual-risk log and follow-up owners.

## Workflow
1. Assemble readiness evidence with `assets/release-readiness-checklist-template.md`.
2. Evaluate go/no-go under `references/release-signoff-rules.md`.
3. Record decision in `assets/go-no-go-decision-log-template.md`.
4. Confirm rollout/rollback owner readiness.
5. Publish decision and unresolved risk actions.

## Quality Standard
- Go/no-go criteria are explicit and met.
- Decision authority and ownership are auditable.
- Rollback readiness is verified before release.

## Failure Conditions
- Stop when blocker evidence is missing.
- Stop when rollback readiness is unverified.
- Escalate when residual risk exceeds release policy.
