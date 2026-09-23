---
name: migration-engineering
description: >-
  Plan and execute safe cross-system migrations, including service extraction
  from monoliths. Use when moving data, schemas, interfaces, infrastructure, or
  service ownership through compatibility windows, dual-running, reconciliation,
  cutover, recovery, or deprecation. Do not use for deciding whether
  decomposition is justified, designing a target architecture, or implementing
  one named technology; route those to the relevant architecture or specialist
  skill.
license: MIT
compatibility: Platform-agnostic methodology. No runtime dependencies, API keys, or external services required.
metadata:
  tags: migration-engineering, data-migration, schema-migration, api-migration,
    infrastructure-migration, service-migration, expand-contract, compatibility-window,
    dual-running, backfill, reconciliation, cutover, deprecation, rollback,
    roll-forward, irreversible-migration
---

# Migration Engineering

Plan and execute safe migrations across system boundaries. A migration is any
change that moves data, schemas, interfaces, infrastructure, or services from a
current state to a target state while preserving correctness, availability, and
recoverability during the transition.

This skill owns the **cross-system migration method** — compatibility design,
staging, reconciliation, cutover, recovery, and deprecation. It does not own the
implementation details of any single technology or subsystem; those belong to
specialist skills.

## When to use

Load this skill when the task involves:

| Trigger | Example |
|---|---|
| A schema change that must not break existing readers or writers | "Add a non-nullable column to a high-traffic table with zero downtime" |
| A data migration between stores or representations | "Migrate user profiles from Postgres to a dedicated service with its own database" |
| An API version migration with a deprecation window | "Move consumers from v1 REST to v2 GraphQL over six months" |
| An infrastructure or service migration | "Shift a workload from self-hosted VMs to a managed platform across regions" |
| A cross-system change requiring dual-running and reconciliation | "Replace the legacy billing engine with a new one while keeping both in sync" |
| Planning cutover, rollback, or irreversible steps for a migration | "Define the recovery strategy for the warehouse schema migration" |

## When not to use

- **Single-technology quick fixes** — if the change is confined to one system
  with no compatibility window, no dual-running, and no cross-system coordination,
  use the relevant specialist skill directly (e.g., [data-engineering](../data-engineering/SKILL.md)
  for a simple DDL change, [api-design-and-evolution](../api-design-and-evolution/SKILL.md)
  for a single-endpoint deprecation).
- **Tool-specific how-to guides** — this skill provides the method, not
  vendor-specific instructions. It does not prescribe one migration technology, one
  database engine, one API gateway, or one infrastructure platform.
- **Migrations without a system boundary** — in-place refactors, code rewrites
  that don't cross a data or interface boundary, or single-service configuration
  changes are not migration-engineering scope.
- **Guaranteeing rollback** — this skill does not claim rollback is always possible.
  Some migrations include steps that are irreversible; the method requires
  identifying those steps explicitly and planning acceptance, communication, and
  contingency rather than implying a false safety net.

For service extraction, load [references/service-extraction-patterns.md](references/service-extraction-patterns.md)
when a boundary has been proposed and the transition pattern, coexistence shape,
or modular-monolith alternative needs assessment. Use
[templates/service-extraction-assessment.md](templates/service-extraction-assessment.md)
to capture the evidence before filling the general migration plan. This skill
sequences an approved extraction; it does not decide that a monolith should be
split or identify the target architecture.

## Core workflow

### 1. Classify and scope the migration

Determine which migration type(s) apply — real-world migrations often combine
types (a service extraction includes both a data migration and an API
migration). Document the current state, target state, boundary being crossed,
type(s) with their compatibility requirements, and affected systems, teams,
and consumers. Load [references/migration-types.md](references/migration-types.md)
for the classification of schema, data, API, infrastructure/service, and
service-extraction migrations.

### 2. Design the expand/contract sequence

The **expand/contract pattern** is the foundational safe-migration primitive:

1. **Expand** — add the new interface, schema, or system while the old one
   continues to serve; both coexist, and existing consumers are unaffected.
2. **Compatibility window** — a defined period during which both old and new
   are available, with an explicit end condition (date, metric threshold, or
   event such as all registered consumers confirmed).
3. **Dual-running or parallel operation** — for data and service migrations,
   both systems operate concurrently (dual writes, dual reads with comparison),
   producing the evidence needed for the cutover decision.
4. **Contract** — remove the old interface after the window closes and
   verification confirms correctness and completeness.

Not every migration uses all four phases: an additive schema change may need
only the expand phase; a complex service extraction uses all four.

### 3. Plan the backfill and reconciliation

For data migrations, choose a backfill strategy — full, incremental, or
streaming (CDC/event log). Reconciliation verifies source and target match on
four dimensions — completeness, accuracy, timeliness, and consistency — runs
continuously during the compatibility window, and must pass before cutover;
a reconciliation failure is a **stop condition**.

### 4. Design the cutover

Define the exact procedure (automated where possible, with pre/post
conditions), the window and acceptable downtime, interruption points where the
cutover can be paused or reversed (a cutover with none is a risk to flag
explicitly), and the observability that confirms progress and triggers abort.

### 5. Define recovery paths

Every migration step has exactly one of four recovery classifications — never
conflate them: **rollback** (undo the change), **roll-forward** (fix forward in
the new state), **restore** (recover from backup/snapshot), and **irreversible**
(no reversal possible at any level). Irreversible steps require explicit
acknowledgment before execution; distinguish "we chose not to build a reversal
path" from "reversal is physically impossible." Both require acceptance,
communication, and contingency. Load
[references/recovery-classification.md](references/recovery-classification.md)
when classifying concrete steps.

### 6. Plan deprecation and cleanup

After verified cutover: define the deprecation window for the old system in
read-only/degraded mode, track which consumers still depend on the old
interface, remove old schemas/code paths/flags/configuration/credentials/
infrastructure, and communicate at each stage (window opens, cutover scheduled,
cutover complete, window closing, removal).

### 7. Verify and close

Before declaring completion, collect correctness evidence (reconciliation
reports, consumer verification, error-rate comparisons, SLO compliance),
confirm observability shows the expected steady state, verify recovery
procedures were tested and irreversible steps acknowledged, and obtain owner
sign-off per phase.

## Loading guide

Load references and templates on demand — do not load everything at once.

| File | Load when |
|---|---|
| [references/discovery-brief.md](references/discovery-brief.md) | You need to understand how migration concepts map across sibling skills and where this skill's boundaries are |
| [references/migration-types.md](references/migration-types.md) | Classifying a migration (schema, data, API, infrastructure/service, service extraction) before selecting patterns |
| [references/compatibility-patterns.md](references/compatibility-patterns.md) | Designing forward/backward compatibility for a specific migration type |
| [references/recovery-classification.md](references/recovery-classification.md) | Classifying recovery paths (rollback, roll-forward, restore, irreversible) for a concrete migration step |
| [references/planning-fields.md](references/planning-fields.md) | Drafting or reviewing the structured planning fields (reconciliation, evidence, observability, customer impact, ownership) a plan must address |
| [references/service-extraction-patterns.md](references/service-extraction-patterns.md) | Assessing extraction seams and selecting strangler routing, branch by abstraction, anti-corruption, CDC, and parallel-run patterns; includes modular-monolith retention criteria |
| [templates/migration-plan.md](templates/migration-plan.md) | Producing a complete migration plan with all structured fields |
| [templates/compatibility-matrix.md](templates/compatibility-matrix.md) | Building a compatibility matrix for a multi-consumer migration |
| [templates/reconciliation-plan.md](templates/reconciliation-plan.md) | Designing a reconciliation strategy for a data migration |
| [templates/cutover-and-recovery-record.md](templates/cutover-and-recovery-record.md) | Recording cutover procedures, recovery paths, and irreversible-step acknowledgments |
| [templates/service-extraction-assessment.md](templates/service-extraction-assessment.md) | Capturing boundary evidence, coupling, ownership, coexistence, sequencing, operational risk, reversibility, and the decision to extract or retain a modular monolith |

## Specialist routing

Migration engineering composes domain specialists — it never duplicates their
methodology. Route implementation details to the skill that owns the subsystem.

| Migration concern | Route to |
|---|---|
| Decomposition justification and target-boundary decision | [`software-architecture`](../software-architecture/SKILL.md); this skill sequences an authorized transition |
| API contract design, versioning policy, deprecation mechanics | [api-design-and-evolution](../api-design-and-evolution/SKILL.md) |
| Database schema evolution, ETL/ELT pipeline design, backfill operations | [data-engineering](../data-engineering/SKILL.md) |
| Infrastructure provisioning, service networking, secret management during migration | [platform-engineering](../platform-engineering/SKILL.md) |
| Release sequencing, progressive delivery, canary rollout, artifact promotion | [release-engineering](../release-engineering/SKILL.md) |
| SLO definition, error budgets, operational readiness, incident response during migration | [site-reliability-engineering](../site-reliability-engineering/SKILL.md) |
| Work breakdown, dependency mapping, critical path, ownership assignment | [implementation-planning](../implementation-planning/SKILL.md) |
| Threat modeling, security review of migration surface, auth boundary changes | [secure-software-engineering](../secure-software-engineering/SKILL.md) |
| Test strategy, regression coverage, verification gates during migration | [qa-methodology](../qa-methodology/SKILL.md) |
| Verification verdicts, evidence standards, boundary testing | [verification-methodology](../verification-methodology/SKILL.md) |

### Routing to same-wave and future skills

Migration evidence — reconciliation reports, cutover records, recovery-path
classifications, and deprecation tracking — feeds **production-readiness**
assessments. The production-readiness skill consumes migration plans as evidence
that a service is ready for production operation.

The **production-excellence** bundle composes migration-engineering alongside
production-readiness, resilience-and-recovery, capacity-and-cost-engineering,
incident-learning, and privacy-engineering. Migration-engineering contributes
the safe-change dimension to the production-excellence lifecycle.

### Routing to product-lifecycle skills

When a migration is triggered by a feature retirement or product sunset,
coordinate with **product-lifecycle-learning** for the retirement decision
record, deprecation timeline, and customer-treatment plan.
