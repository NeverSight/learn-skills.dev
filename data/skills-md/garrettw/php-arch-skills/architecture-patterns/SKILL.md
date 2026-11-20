---
name: architecture-patterns
description: Use this skill when choosing a system-level architecture (monolith, modular monolith, microservices, event-driven, serverless, clean/hexagonal, or DDD) for a new or growing PHP application, or when weighing a premature move to a more distributed style. Provides a decision guide and the common pitfalls that cause distributed monoliths and premature complexity.
---

# Choosing an Architecture

This skill is about the **system-level** decision: which architecture style fits this application *before* you are deep into one. It does not redefine the individual patterns — those live in their own skills (linked below). Its job is to help you pick, and to warn you off the moves that teams most often regret.

## Decision Guide

These are three separate decisions. Answer each one on its own; a single application usually combines one answer from each.

### 1. Deployment topology (first matching branch wins)

```
START
  │
  ├─ Need independent deploy/scale per business area,  ─────→ Microservices for those areas
  │  with stable boundaries and clear owners?                 (only once boundaries are clear)
  │
  ├─ Variable / unpredictable, bursty, stateless work?  ────→ Serverless for those parts
  │                                                           (alongside the rest of the system)
  │
  └─ Otherwise  ────────────────────────────────────────────→ Modular Monolith (the default)
```

### 2. Internal structure (per bounded context, under any topology)

- **Simple CRUD or linear procedures:** Transaction Script or lean ORM entities behind thin controllers (see `php-domain-modeling`).
- **Complex business logic with many invariants:** Clean / Hexagonal + DDD (see `php-domain-modeling`, `application-layer`, `infrastructure-boundaries`).

### 3. Optional patterns (per context, only for a concrete need)

- **Event Sourcing:** state at a past point in time, replay, or history as the source of truth (see `event-sourcing`). A plain audit log is not enough reason.
- **CQRS:** read and write models that genuinely diverge (see `application-layer`). Command/query handlers alone are not CQRS.
- **Domain events and reliable messaging:** asynchronous reactions within or across contexts (see `domain-events`, `reliable-messaging`).

### How to read the decisions

- **Monolith / Modular Monolith** is the right default for most teams. A *modular* monolith organizes code by business capability, one folder per bounded context (see [directory-structure-templates.md](../application-layer/references/directory-structure-templates.md)), with explicit module boundaries, so you can later extract a service without a rewrite. Choose it unless the microservices or serverless branch clearly applies, and then split off only the areas it applies to.
- **Microservices** earn their cost only when you have (a) clear, stable bounded contexts and (b) a real need to deploy or scale them independently. Without both, they add distributed-systems complexity for no benefit.
- **Event-Driven / Event Sourcing / CQRS** are patterns for *specific* needs (temporal queries, replay, read/write divergence) — not a default. See `event-sourcing` and `domain-events` before reaching for them.
- **Clean / Hexagonal + DDD** is about *internal* structure (dependencies point inward, domain at the center, ports & adapters at the edge). It pairs with any of the above deployment styles. The boundary-protection patterns that realize it are catalogued in `distribution-patterns` ([boundary-protection-patterns.md](../distribution-patterns/references/boundary-protection-patterns.md)).
- **Serverless** suits bursty, stateless work; it is rarely the whole system. Keep functions small and push state to external stores.

## Common Pitfalls

### 1. Premature Microservices
**Problem:** Starting with microservices for a simple or early-stage application. The distributed complexity (service discovery, network failures, distributed transactions) arrives long before the scale that justifies it.
**Solution:** Start as a Modular Monolith. Extract a service only when a bounded context is stable and you genuinely need independent deployment or scaling.

### 2. Distributed Monolith
**Problem:** "Microservices" that must be deployed together or that call each other synchronously on every request — all the operational cost of distribution with none of the isolation benefit.
**Solution:** Ensure each service owns its behavior and data behind a clear contract (Remote Facade + DTO, see `distribution-patterns`). If a change forces coordinated deploys, the boundary is wrong.

### 3. Ignoring Data Boundaries
**Problem:** Multiple services share one database (or one service reaches into another's tables). Coupling at the data layer quietly re-creates a monolith and makes independent change impossible.
**Solution:** Each service/context owns its data; synchronize via events (`domain-events`) or explicit APIs, not shared tables. This is the data-layer expression of bounded contexts (`bounded-contexts`).

### 4. Forcing DDD Where It Doesn't Pay
**Problem:** Applying rich aggregates, repositories, and mappers to simple CRUD or a prototype. The ceremony costs more than the rules it protects.
**Solution:** Default to lean ORM entities or a Transaction Script for simple areas; reach for a Domain Model only where the invariants justify it. See `php-domain-modeling` ("Start simple. Evolve complexity only when needed.").

### 5. Big-Bang Rewrite to a "Better" Architecture
**Problem:** Rebuilding the whole system on a new architecture to gain purity. It stalls product delivery and usually fails (see `architecture-migration`).
**Solution:** Migrate incrementally, one touched area at a time (Strangler Fig), and only at a trigger (active feature, complex bug, new endpoint).

## Related Skills
- [php-domain-modeling](../php-domain-modeling/SKILL.md): the internal modeling decision (Transaction Script → Table Module → Domain Model) and when DDD pays off.
- [application-layer](../application-layer/SKILL.md): the use-case/Service Layer boundary; home of command/query handlers, and of CQRS when read and write models genuinely diverge.
- [distribution-patterns](../distribution-patterns/SKILL.md): Remote Facade + DTO — the contract shape that makes a service boundary real; boundary-protection pattern mapping.
- [infrastructure-boundaries](../infrastructure-boundaries/SKILL.md): ports & adapters / hexagonal realized at the infrastructure edge.
- [bounded-contexts](../bounded-contexts/SKILL.md): discovering the boundaries that microservices and data ownership depend on.
- [domain-events](../domain-events/SKILL.md) and [event-sourcing](../event-sourcing/SKILL.md): the event-driven and event-sourced options from the decision guide.
- [architecture-migration](../architecture-migration/SKILL.md): the incremental playbook for moving an existing system toward any of these.
