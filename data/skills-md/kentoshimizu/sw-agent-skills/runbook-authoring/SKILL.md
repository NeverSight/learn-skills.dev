---
name: runbook-authoring
description: "Runbook authoring workflow for clear, executable operational procedures for on-call responders. Use when incident response, rollback, failover, or maintenance steps must be documented before production use; do not use for production feature logic design."
---

# Runbook Authoring

## Overview
Use this skill to produce runbooks responders can execute reliably under incident pressure.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Runbook usability rules:
  - `references/runbook-usability-rules.md`

## Templates And Assets
- Runbook template:
  - `assets/runbook-template.md`
- Drill checklist:
  - `assets/runbook-drill-checklist.md`

## Inputs To Gather
- Operational scenario and trigger conditions.
- System dependencies, permissions, and tooling constraints.
- Recovery and rollback expectations.
- Escalation and communication policy.

## Deliverables
- Executable runbook with decision points.
- Drill validation evidence.
- Escalation and ownership mapping.

## Workflow
1. Draft procedure using `assets/runbook-template.md`.
2. Apply usability guidance from `references/runbook-usability-rules.md`.
3. Validate steps with `assets/runbook-drill-checklist.md`.
4. Refine ambiguous actions and missing prerequisites.
5. Publish runbook with owner and review cadence.

## Quality Standard
- Steps are actionable, ordered, and unambiguous.
- Rollback and escalation paths are explicit.
- Runbook works for responders beyond original author.

## Failure Conditions
- Stop when steps require hidden assumptions.
- Stop when rollback actions are undefined.
- Escalate when drill validation fails for critical scenarios.
