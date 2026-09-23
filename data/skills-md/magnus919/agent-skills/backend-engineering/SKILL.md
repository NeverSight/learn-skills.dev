---
name: backend-engineering
description: Design and implement backend services and APIs — REST, gRPC, GraphQL,
  event-driven handlers, transaction boundaries, outbox/inbox delivery, migration
  coexistence, database access, integration, error handling, and service-level testing.
  Use for application/domain/infrastructure implementation decisions. Language and
  framework agnostic. Do not use for frontend, data engineering, platform provisioning,
  API contract ownership, service decomposition strategy, or cross-system migration
  planning.
license: MIT
metadata:
  tags: backend, api, services, server, database, integration, middleware, events, outbox,
    inbox, idempotency, coexistence, query-optimization, testing
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Backend Engineering Methodology

Backend engineering is the craft of building the server-side systems that power applications — APIs, services, data access, integrations, and the runtime behavior that makes the architecture real. This methodology covers implementation after target design in `software-architecture` and before quality validation in `qa-methodology`; use `software-architecture-analysis` when the current system must first be reverse-engineered. It makes runtime boundaries, transaction behavior, message handling, and coexistence seams executable without taking ownership of the surrounding architecture or migration decision.

## The Backend Engineer's Domain

| You own | You don't own |
|---------|--------------|
| API implementation — REST/gRPC/GraphQL endpoints, request validation, response formatting, error handling, middleware chains | API contracts belong to `api-design-and-evolution`; service decomposition and target boundaries belong to `software-architecture` |
| Service logic — business rules, workflow orchestration, state management, background job processing | Deployment pipeline and infrastructure — that's `platform-engineering` |
| Event-driven implementation — domain-event publication, outbox/inbox coordination, handler idempotency, replay and failure paths | Event contract ownership and delivery semantics — that's the api-design-and-evolution |
| Migration seams inside a service — adapters, selectable paths, authority checks, and implementation handoffs | Cross-system migration lifecycle and cutover authority — that's the migration-engineering |
| Database access patterns — query design, connection management, transaction boundaries, N+1 detection, pagination | Data-platform and model strategy belong to `data-architect`; schema and pipeline operations belong to `data-engineering` |
| Integration code — third-party API clients, webhook handlers, message queue consumers/producers | Code review and quality gates — that's `qa-methodology` |
| Observability instrumentation at the service level — structured logging, metrics, tracing hooks | Observability infrastructure and reliability policy belong to `platform-engineering` and `site-reliability-engineering` |
| Service-level tests — unit tests for business logic, integration tests for API contracts | Test strategy and automation — that's `qa-methodology` |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/api-patterns.md` | Designing or implementing API endpoints — resource modeling, versioning, pagination, error response formats, request validation |
| `references/service-patterns.md` | Structuring service logic — clean/hexagonal/layered architecture, dependency injection, middleware composition, request lifecycle, background jobs |
| `references/event-driven-service-implementation.md` | Implementing event-driven application flows — domain events, unit of work, transactional outbox/inbox, idempotent handlers, retry/replay, observability, and failure handling |
| `references/migration-coexistence-patterns.md` | Keeping old and new implementations safe to run together — adapters, strangler handoffs, anti-corruption boundaries, dual paths, authority, and removal conditions |
| `references/database-testing.md` | Database access patterns (connection pooling, query optimization, N+1 detection, pagination strategies, transaction boundaries, read/write splitting, replication lag) and service-level testing (unit testing business logic, integration testing API contracts with test containers/WireMock, contract testing with Pact, test fixtures, CI integration) |
| `references/integration-patterns.md` | Integrating with external systems — retry with backoff, circuit breakers, idempotency keys, webhook verification, message queue consumers |
| `references/error-handling.md` | Handling errors systematically — classification (client vs server), structured responses, exception handling patterns, observability correlation |
| `references/source-index.md` | Provenance and ownership notes for this original synthesis; load when reviewing scope or source boundaries |

## Templates

| Template | When to Use |
|-----------|-------------|
| `templates/service-design-record.md` | Designing or restructuring a service — structure, API surface, data access, error handling, and testing plan in one reviewable record |
| `templates/error-handling-taxonomy.md` | Defining or auditing a service's error contract — classification, response format, retry/idempotency policy, and error-path tests |

## Scripts

| Script | When to Use |
|-----------|-------------|
| `scripts/n1-query-spotter.py` | Scanning Python source for potential N+1 query patterns (query-like calls inside loops); `--json` for CI-friendly output, exit 1 on findings |

## Related Skills

- [programming-principles](../programming-principles/SKILL.md) — DDD owns bounded contexts, aggregates, domain language, repositories, and domain-modeling guidance. This skill applies those decisions at implementation seams rather than duplicating that catalog.
- [api-design-and-evolution](../api-design-and-evolution/SKILL.md) — owns event/message contracts, delivery semantics, compatibility, and consumer-facing API decisions.
- [migration-engineering](../migration-engineering/SKILL.md) — owns cross-system migration classification, compatibility windows, reconciliation, cutover, recovery, deprecation, and cleanup. This skill only implements service-local coexistence seams.
- [software-architecture](../software-architecture/SKILL.md) — owns service decomposition and target-boundary strategy; backend engineering implements an approved boundary.
- [data-engineering](../data-engineering/SKILL.md) — owns schema migration and pipeline operations; application code may expose the repository or transaction interfaces those operations use.
- [secure-software-engineering](../secure-software-engineering/SKILL.md) — owns threat modeling, authorization, secrets, untrusted inputs, and security acceptance evidence.
- [release-engineering](../release-engineering/SKILL.md) — owns progressive delivery, artifact promotion, release gates, and rollback mechanics.
- [postgres](../postgres/SKILL.md) — diagnosing the PostgreSQL side of a database problem: configuration review, index and query-plan issues, vacuum/bloat, backups/PITR, replication and failover. Application-level data access patterns stay here; engine-level operations route there.
- [supabase](../supabase/SKILL.md) — building on Supabase: migrations, RLS, Auth, Storage, and Edge Functions. To measure an agent's Supabase task competence, use its [agent evals harness reference](../supabase/references/agent-evals.md).

## Core Principles

**The interface is the contract** — API boundaries are service-level contracts. Every endpoint signature, request schema, response format, and error code is a promise to consumers. Breaking changes are coordination problems, not version bumps.

**Business logic is the center of gravity** — Keep business rules isolated from framework concerns, transport protocols, and infrastructure details. A well-structured service can survive changes to its HTTP library, database driver, and deployment platform.

**Handle errors where they make sense** — Catch errors at the boundary where you have enough context to handle them meaningfully. Catch too early and you lose context. Catch too late and you can't recover.

**Design for failure, not just success** — Every external call can fail. Every database connection can drop. Every message can be duplicated. Idempotency, retry, and graceful degradation are not optimizations — they're requirements.

**Test at the right level** — Business logic gets unit tests. API contracts get integration tests. Service boundaries get contract tests. Each level catches a different class of failure.

## Implementation Decision Path

1. Name the bounded context, aggregate/invariant boundary, and source of truth. Use
   [programming-principles](../programming-principles/SKILL.md) for DDD choices rather
   than rebuilding its catalog here.
2. Put transport, broker, database, clock, and vendor concerns behind ports owned by
   the application or domain-facing code. Let infrastructure implement those ports.
3. For a command that changes durable state and emits a fact, load the aggregate,
   invoke domain behavior, and commit state plus outbox records in one unit of work.
   Do not hold that transaction open across network calls.
4. For an incoming message, validate the envelope at the edge, deduplicate within the
   consumer's authority, apply the handler, and acknowledge only after its durable
   effects commit. Load the event reference for replay and poison-message decisions.
5. If old and new paths coexist, record which path is authoritative for each operation,
   how outputs are compared, and what evidence permits handoff or removal. Load the
   migration reference for the implementation seam; route the migration lifecycle out.
6. Add unit tests for domain/application behavior and boundary integration tests for
   transaction, outbox, inbox, duplicate, retry, replay, and recovery behavior.

## Exit Criteria

This skill is complete when the implementation has explicit dependency direction,
transaction and authority boundaries, classified failure/retry behavior, observable
message or coexistence paths, focused tests for duplicate and failure cases, and clear
links to the neighboring owner for every out-of-scope decision.
