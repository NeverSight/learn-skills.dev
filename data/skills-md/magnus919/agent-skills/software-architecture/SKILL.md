---
name: software-architecture
description: Design and review software architectures from business drivers through system boundaries, tradeoffs, runtime behavior, evolution, and architecture practice. Use when choosing a greenfield or target architecture, comparing modular-monolith and service shapes, designing distributed consistency, replication, partitioning, coordination, ordering, transaction isolation, or failure behavior, defining architecture fitness evidence, or facilitating a consequential architecture review. Do not use for reverse engineering, API contract semantics, data-platform design, implementation, infrastructure operations, security lifecycle, or migration execution; route those to the named specialist skills.
license: MIT
compatibility: Platform-agnostic methodology. No runtime dependencies.
metadata:
  tags: software-architecture, architecture-design, tradeoffs, modularity, distributed-systems, evolutionary-architecture, architecture-review
---

# Software Architecture

Use this skill to make system-level design decisions and leave an inspectable path from drivers to evidence. It owns the architecture decision workflow, not the implementation of any subsystem.

## Workflow

1. **Frame the decision.** Establish the desired outcome, stakeholders, constraints, decision horizon, reversibility, affected systems, and evidence gaps. Do not invent scale, regulatory, latency, or ownership facts.
2. **Turn qualities into scenarios.** Name the architecture characteristics that matter, express each as an observable scenario, prioritize them, and expose conflicts. Load `references/architecture-characteristics-and-tradeoffs.md`.
3. **Choose boundaries and shape.** Compare styles, topology, and deployment granularity against the scenarios and team operating capacity. Load `references/styles-topologies-and-granularity.md`.
4. **Test ownership and coupling.** Identify policy, data, change, runtime, and team boundaries. Treat a service split as a hypothesis, not a default. Load `references/coupling-modularity-and-data-ownership.md`.
5. **Make runtime behavior explicit.** For asynchronous or distributed flows, specify authority, consistency, ordering, retries, duplicates, timeouts, partial failure, recovery, and reconciliation. Load `references/distributed-workflows-and-consistency.md`.
6. **Record and verify.** Capture the decision and rejected alternatives in `templates/architecture-design-brief.md` and `templates/tradeoff-record.md`; use `templates/architecture-review.md` for challenge and sign-off. Define fitness evidence and drift response with `references/evolution-fitness-functions-and-drift.md`.
7. **Plan change without hiding execution ownership.** Identify evolutionary slices, coexistence assumptions, and handoff conditions. Load `references/migration-and-coexistence.md`; route an approved transition to `migration-engineering`.
8. **Facilitate proportionately.** Match review depth to blast radius, irreversibility, uncertainty, and cross-team impact. Load `references/architecture-practice-and-facilitation.md`.

## Output Contract

Produce an architecture decision brief or review that includes drivers, stakeholders, constraints, prioritized scenarios, candidate options, explicit tradeoffs, boundaries and ownership, runtime and failure behavior, operational implications, decisions, evidence gaps, fitness checks, evolution slices, and named owners. State what is decided, what remains open, and which specialist owns follow-up work.

## Ownership Boundaries

- Reverse engineer an existing codebase or infer architecture from repository evidence with `software-architecture-analysis`.
- Design interface contracts, schemas, compatibility, or API topology with `api-design-and-evolution`.
- Design data platforms, data products, data models, or data governance with `data-architect`.
- Implement services, integrations, transactions, or application code with `backend-engineering` and the relevant engineering owner.
- Provision or operate cloud, network, CI/CD, containers, secrets, or observability substrate with `platform-engineering` and its tool owners.
- Define security requirements, threat models, authorization, secrets, or security evidence with `secure-software-engineering`.
- Author the durable ADR with `adr-authoring`; this skill supplies the architecture decision context and tradeoff analysis.
- Execute an approved cross-system transition with `migration-engineering`; this skill decides whether the target shape and boundary are justified.
- Model capacity, unit cost, load evidence, or SLO-cost tradeoffs with `capacity-and-cost-engineering`.
- Design and exercise degradation, failover, restore, or recovery evidence with `resilience-and-recovery`.
- Create structural diagrams with `c4-diagramming` or `mermaid-diagrams`.
- Govern a technology portfolio, radar, or proportional technology governance path with `technology-radar`.

## When Not To Use

Do not use this skill as a substitute for those specialist owners, as a code review workflow, or as a vendor/tool runbook. If the request is only one interface, data platform, implementation, infrastructure, security, capacity, diagram, ADR, or migration concern, load the narrower owner directly. If the architecture question depends on facts from an existing system, start with `software-architecture-analysis` and return here for a target decision.

## Reference Guide

| Load when | Reference |
|---|---|
| Prioritizing qualities and comparing conflicting outcomes | `references/architecture-characteristics-and-tradeoffs.md` |
| Comparing styles, deployment topology, or granularity | `references/styles-topologies-and-granularity.md` |
| Testing modularity, coupling, boundaries, and data authority | `references/coupling-modularity-and-data-ownership.md` |
| Designing distributed workflows, consistency, or failure behavior | `references/distributed-workflows-and-consistency.md` |
| Choosing replication, partitioning, coordination, ordering, or transaction-isolation mechanisms | `references/distributed-workflows-and-consistency.md`, then the [DDIA mini reference](../programming-principles/references/designing-data-intensive-apps.mini.md); load the [full reference](../programming-principles/references/designing-data-intensive-apps.full.md) only when deeper mechanism analysis is necessary |
| Defining fitness evidence, drift response, or evolutionary change | `references/evolution-fitness-functions-and-drift.md` |
| Planning coexistence and handing execution to migration engineering | `references/migration-and-coexistence.md` |
| Running architecture workshops, reviews, and decision facilitation | `references/architecture-practice-and-facilitation.md` |
| Checking provenance and the licensed-books transformation boundary | `references/source-index.md` |

Keep the ownership split explicit when loading DDIA: this skill owns the system-level architecture decision and its tradeoffs; `programming-principles` supplies distributed-data principles and mechanism detail. Route message-handler implementation to `backend-engineering`, API or event contracts to `api-design-and-evolution`, data-platform design to `data-architect`, and exercised recovery evidence to `resilience-and-recovery`.

## Completion

Stop when the architecture decision has an accountable owner, explicit alternatives and consequences, evidence or a named gap for each material claim, a verification path for prioritized characteristics, and specialist handoffs. Escalate rather than silently resolve missing authority, security, data ownership, or operational evidence.
