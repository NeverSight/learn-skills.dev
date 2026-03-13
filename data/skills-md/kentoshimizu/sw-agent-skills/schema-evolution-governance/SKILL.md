---
name: schema-evolution-governance
description: "Schema evolution governance workflow for safe migration sequencing, compatibility control, and rollback readiness across dependent systems. Use when shared schemas change and end-to-end compatibility governance is required; do not use for isolated query micro-optimizations."
---

# Schema Evolution Governance

## Overview
Use this skill to evolve shared schemas without breaking producers, consumers, or historical data integrity.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Compatibility window rules:
  - `references/compatibility-window-rules.md`

## Templates And Assets
- Schema change plan template:
  - `assets/schema-change-plan-template.md`
- Schema compatibility checklist:
  - `assets/schema-compatibility-checklist.md`

## Inputs To Gather
- Current schema and migration history.
- Producer/consumer dependency map.
- Data volume, retention, and rollback constraints.
- Release window and coordination limits.

## Deliverables
- Compatibility-aware schema change plan.
- Phased migration sequence with checkpoints.
- Rollback and data-recovery readiness criteria.

## Workflow
1. Define change impact in `assets/schema-change-plan-template.md`.
2. Apply compatibility rules from `references/compatibility-window-rules.md`.
3. Validate consumer migration sequence and cutover plan.
4. Verify rollback/data integrity with `assets/schema-compatibility-checklist.md`.
5. Publish execution ownership and residual risk log.

## Quality Standard
- Compatibility impact is explicit and testable.
- Migration and rollback paths are both validated.
- Consumer coordination is planned before destructive changes.

## Failure Conditions
- Stop when forward/backward compatibility is unverified.
- Stop when rollback or data recovery path is missing.
- Escalate when migration risk exceeds governance policy.
