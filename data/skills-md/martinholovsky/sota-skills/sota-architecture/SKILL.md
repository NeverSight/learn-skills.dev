---
name: sota-architecture
description: >-
  State-of-the-art software and system architecture rules (2026) for both
  building and auditing. Use when designing, building, refactoring, or
  extending system architecture — boundaries, DDD, hexagonal/clean
  architecture, event-driven design, CQRS, sagas, messaging, caching,
  sharding, multi-tenancy, resilience, scalability, 12-factor/cloud-native —
  AND when auditing existing architecture for quality (design review,
  anti-patterns like distributed monolith or shared database,
  reliability/scalability assessment). Trigger keywords: architecture, system
  design, microservices, monolith, serverless, bounded context, DDD,
  aggregate, hexagonal, clean architecture, event-driven, Kafka, NATS,
  JetStream, messaging, pub/sub, stream, consumer, queue, saga, outbox,
  idempotency, CQRS, resilience, circuit breaker, retry, timeout,
  backpressure, caching, sharding, partitioning, multi-tenant, 12-factor,
  cloud-native, feature flag, ADR, scalability, anti-pattern, design review,
  architecture audit.
---

# SOTA Architecture (2026)

## Purpose

Dense, enforceable rules for software and system architecture: choosing styles,
drawing boundaries, surviving distributed systems, scaling state, and shipping
cloud-natively. One rule set, two modes — apply the rules while **building**,
or check code against them while **auditing**. All substance lives in `rules/`;
this file routes you to the right one.

## BUILD mode — designing or writing code

1. **Identify the decision surface.** Before writing code, list the architectural
   decisions in play (style, boundaries, sync/async, datastore, tenancy, caching).
   Use the index below to read the relevant rules files *before* committing to a
   design — minimum: 01 for any new system/service, 03 for anything crossing a
   network, 07 always (know what failure looks like).
2. **Default to boring.** Modular monolith, one database, sync calls within the
   deadline budget, queues only where semantics are async. Escalate complexity
   only when a rule's stated forces apply, and record it.
3. **Write the ADR first** for any Type 1 (hard to reverse) decision: context,
   decision, consequences (must include downsides), rejected alternatives. Put it
   in `docs/adr/`.
4. **Apply rules as you code, not after.** Timeouts/retries/idempotency at every
   integration point as you create it; ports before adapters; tenant_id and trace
   context plumbed from the first commit. Retrofitting these is 10x the cost.
5. **Encode the rules you adopted as fitness functions** (import-rule tests,
   contract tests in CI, SLO alerts) so they survive you.
6. **Before finishing**, run the relevant "Audit checklist" sections from each
   rules file you used against your own output. Fix what fails or document why
   it's accepted (in the ADR).

## AUDIT mode — reviewing existing code or designs

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

1. **Scope first.** Identify what you're auditing (whole system, one service, one
   PR) and read the matching rules files from the index. For a full architecture
   audit, work through every rules file; for a PR, pick by topic.
2. **Drive from the checklists.** Every rules file ends with an "Audit checklist"
   of yes/no questions — answer each with evidence (file:line, config, trace),
   never from the README's claims. Use [rules/07](rules/07-anti-patterns-catalog.md) detection signals as concrete
   grep/inspection targets.
3. **Verify mechanically where possible:** grep for client construction without
   timeouts, imports crossing layers, queries missing tenant scoping, `latest`
   image tags, dual-writes (DB write + publish in the same function without an
   outbox), shared DB credentials.
4. **Report every violation as a finding** in this exact format:

   ```
   [SEVERITY] file:line — Rule violated: <rules-file §section, short rule name>
   Evidence: <what you observed>
   Impact: <what fails and when>
   Fix: <specific, smallest correct remediation>
   Effort: trivial | small | medium | large
   ```

5. **Severity conventions:**
   - **Critical** — data loss/corruption, cross-tenant leak, full-outage mechanism, money/security path failing open: missing idempotency on payments, business data only in cache, shared-DB writes, liveness probe checking the DB, secrets in git, no owning team.
   - **High** — outage-magnifier or rollback-blocker: missing timeouts on hot paths, retry multiplication, lockstep deploys, breaking schema changes, sync chains > 2 on revenue paths, DLQ without alerting, missing read-your-writes on user-visible saves.
   - **Medium** — erodes evolvability/operability: leaky abstractions, anemic core domain, stale feature flags, missing ADRs, event spaghetti without cycles, unscoped shared libs.
   - **Low** — hygiene: naming drifting from ubiquitous language, missing runbook sections, unjittered crons that haven't yet caused incidents.
   - When in doubt between two severities on a revenue-, security-, or data-touching path, pick the higher.
6. **Summarize** findings by severity with counts, then list the top 3 structural
   themes (not symptoms) and the order to fix them (Critical correctness →
   rollback/deploy safety → evolvability).

## Rules index

| File | Topics | Read this when... |
|---|---|---|
| [`rules/01-architecture-styles-and-decisions.md`](rules/01-architecture-styles-and-decisions.md) | Modular monolith vs microservices vs serverless, **monorepos (build-enforced visibility, CODEOWNERS enforcement, workspace lockfiles, affected-only CI and its global inputs, §2a)**, extraction forces, ADRs, evolutionary architecture, fitness functions, Type 1/2 decisions, retiring a service completely, Conway's law, strangler fig, buy vs build | Starting a system, proposing/justifying a service split or merge, reviewing whether the architecture style fits, setting up ADRs or CI architecture gates |
| [`rules/02-domain-modeling-and-boundaries.md`](rules/02-domain-modeling-and-boundaries.md) | Bounded contexts, context maps, ubiquitous language, aggregates & invariants, hexagonal ports/adapters, clean-architecture dependency rule, ACLs, domain events, value objects, **how absence is encoded — the in-band-sentinel class and its three audit probes**, repositories, optimistic concurrency | Modeling a domain, defining module/service internals, reviewing layering and imports, fixing anemic models or god aggregates, wrapping vendors |
| [`rules/03-distributed-systems-and-events.md`](rules/03-distributed-systems-and-events.md) | CAP/PACELC per-operation, idempotency mechanics, exactly-once myth, outbox/inbox, sagas (orchestration vs choreography, conservative leg ordering), reconciliation against an external system of record, event vs command, CQRS/event-sourcing adoption bar, DLQs, ordering, backpressure, schema evolution, contract tests, IDs & time, distributed locks and leases, checking a protocol's design with a model checker (TLA+/TLC, P, Quint) before building it | Anything crosses a network or a queue: designing/reviewing messaging, workflows spanning services, consistency questions, retry/duplicate bugs, integrations with a third party that holds authoritative state, API/event versioning |
| [`rules/04-resilience-and-failure-design.md`](rules/04-resilience-and-failure-design.md) | Timeouts & deadline budgets, retries with jitter & budgets, circuit breakers, bulkheads, graceful degradation, fail open/closed, load shedding, liveness vs readiness, chaos engineering, SLOs, safe rollback/restart, stampedes, disaster recovery (RTO/RPO) | Designing or reviewing any integration point, incident follow-ups, "is this service production-ready", overload or cascading-failure concerns |
| [`rules/05-scalability-state-and-data.md`](rules/05-scalability-state-and-data.md) | Stateless services, autoscaling signals, DB scaling order, replica staleness, caching tiers & invalidation, partitioning/sharding keys, data lifecycle/retention, multi-tenancy models & isolation, workload separation, async heavy work, large objects and blobs (presigned uploads) | Scaling questions, cache design/review, choosing shard or partition keys, building/auditing multi-tenant systems, read-after-write bugs |
| [`rules/06-cloud-native-config-and-delivery.md`](rules/06-cloud-native-config-and-delivery.md) | 12-factor updated 2026: immutable artifacts, config & secrets, GitOps, disposability, observability (logs/metrics/traces/SLOs), backing services & dev/prod parity, feature-flag discipline, progressive delivery, expand/contract migrations, runbooks, cost signals | Setting up a new service's operational skeleton, reviewing deployability/config/secrets/flags, CI/CD and migration-safety review |
| [`rules/07-anti-patterns-catalog.md`](rules/07-anti-patterns-catalog.md) | Distributed monolith, shared database, god services, premature microservices, leaky abstractions, sync chain of doom, event spaghetti, cache-as-truth, shared `common` libs, resume-driven design — each with detection signals, fix, default severity | Every audit (use as the detection playbook); in BUILD mode as the "never do this" list; naming and severity-rating a smell you've spotted |
| [`rules/08-nats-jetstream.md`](rules/08-nats-jetstream.md) | NATS JetStream as primary bus (Go): core NATS vs JetStream, subject/stream design, stream limits & retention/discard, R3/mirrors/sources, publish dedup (`Nats-Msg-Id` + duplicate window), pull consumers (`jetstream` pkg), ack/nak/term, `MaxAckPending`/`MaxDeliver`, DLQ-via-advisory, KV & Object stores, accounts/domains/leafnodes | Designing, building, or auditing anything on NATS JetStream — streams, consumers, KV/Object stores, multi-tenant accounts; apply on top of [rules/03](rules/03-distributed-systems-and-events.md) (general eventing) for JetStream-specific config and Go client mechanics |

## Top-10 non-negotiables

Check these on every build and every audit, regardless of scope:

1. **Every remote call has an explicit timeout**, sized from measured latency, fitting the edge deadline budget. (04 §1)
2. **Every message handler and retried operation is idempotent**, with dedupe state committed atomically with the state change. (03 §2)
3. **No dual-writes**: DB state change + event publish happen via outbox/CDC, never as two independent writes. (03 §4)
4. **One writer-owner per table**; services never integrate through a shared database. (07 §2)
5. **Dependencies point inward**: domain imports no framework/ORM/vendor/transport types — enforced by an automated architecture test, not convention. (02 §5)
6. **Retries are bounded, jittered, idempotent-only, and owned by exactly one layer** per edge. (04 §2)
7. **Every queue has bounded size, a DLQ with alerting, and a tested redrive procedure.** (03 §7)
8. **Tenant/user scoping is enforced below application code** (RLS or mandatory scoped layer) and present in every query, cache key, message, and log line. (05 §7)
9. **Cross-service contracts (APIs and events) are versioned with CI compatibility checks**; changes are expand/contract; previous code version must still run (rollback-safe). (03 §8, 06 §7)
10. **Every Type 1 decision has an ADR with consequences and rejected alternatives**, and every prod component has exactly one owning team. (01 §4, §7)

A violation of any of these is at minimum High severity; most are Critical on
data-, money-, or security-touching paths.
