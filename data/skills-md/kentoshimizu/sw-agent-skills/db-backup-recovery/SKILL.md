---
name: db-backup-recovery
description: "Database backup and recovery workflow for defining RPO/RTO-aligned retention, restore strategy, and disaster readiness. Use when data durability and recovery guarantees are in scope; do not use for query-only tuning tasks."
---

# DB Backup Recovery

## Overview
Use this skill to define backup and restore behavior that is credible under incident pressure, not only compliant on paper.

## Scope Boundaries
- Data loss tolerance and recovery time objectives must be formalized.
- Backup policy is changing due to scale, compliance, or architecture change.
- Teams need confidence that restore procedures actually work.

## Core Judgments
- RPO/RTO targets per data class and business workflow.
- Backup modality: full, incremental, log-based, snapshot, or hybrid.
- Retention and immutability policy by legal and business requirements.
- Restore topology: point-in-time restore, region restore, partial table restore.

## Practitioner Heuristics
- Start from restore requirements, then derive backup schedule.
- Separate operational backups from archival/legal-retention copies.
- Encryption, key rotation, and access logging apply to backups too.
- Recovery procedures must assume partial infrastructure outage, not ideal environment.

## Workflow
1. Define data criticality tiers and required RPO/RTO per tier.
2. Select backup mechanisms and cadence aligned to write patterns.
3. Define retention lifecycle and deletion rules.
4. Design restore paths for common and worst-case incident scenarios.
5. Establish ownership and escalation for recovery execution.
6. Document assumptions that invalidate the current strategy.

## Common Failure Modes
- Backup success is monitored but restore path is untested.
- One global retention policy ignores data criticality differences.
- Recovery relies on undocumented manual knowledge.

## Failure Conditions
- Stop when RPO/RTO cannot be mapped to concrete mechanisms.
- Stop when backup policy has no feasible restore path.
- Escalate when recovery guarantees exceed infrastructure capability.
