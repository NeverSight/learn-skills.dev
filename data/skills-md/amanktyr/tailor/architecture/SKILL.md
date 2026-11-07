---
name: architecture
description: Governs software architecture design, modular monolith patterns, layer boundary enforcement, and Architecture Decision Record (ADR) lifecycle management.
---

# Architecture Skill

Activate this skill when evaluating system boundaries, designing new subsystems, structuring directory layouts, resolving modular coupling, or maintaining Architecture Decision Records (ADRs).

> **Architectural Law:** *Make boundaries clear, keep modules cohesive, and defer distributed complexity until verifiable scale demands it.*

---

## 1. Clean Architecture & Layer Boundary Enforcement

Maintain strict separation of concerns across application layers:

```
┌────────────────────────────────────────────────────────┐
│ 1. Presentation / Transport Layer                      │
│    - HTTP Controllers, Route Handlers, CLI Commands    │
│    - Responsibility: Parse inputs, validate payload,   │
│      map HTTP status codes, serialize responses.       │
├────────────────────────────────────────────────────────┤
│ 2. Domain / Application Service Layer                  │
│    - Business Services, Use Cases, Workflows           │
│    - Responsibility: Pure business logic, permissions, │
│      orchestration, domain events. Zero HTTP details.  │
├────────────────────────────────────────────────────────┤
│ 3. Infrastructure & Persistence Layer                  │
│    - Database Repositories, Third-Party API Clients    │
│    - Responsibility: SQL queries, ORM calls, network   │
│      transports, cache storage.                        │
└────────────────────────────────────────────────────────┘
```

### Boundary Violations to Reject
* Writing raw SQL or database queries inside React components or HTTP controllers.
* Importing HTTP request/response objects (`req`, `res`) into domain service classes.
* Allowing circular module dependencies across domain boundaries.

---

## 2. Modular Monolith vs Distributed Microservices

* **Default Choice:** **Modular Monolith**. Group code into feature domains (`src/features/billing/`, `src/features/auth/`) with clear public API barriers (`index.ts`).
* **Reject Premature Microservices:** Do not split applications into separate microservices, message queues, or distributed transactions unless:
  1. Independent teams require isolated deployment pipelines.
  2. Distinct microservices have vastly different scaling and compute profiles (e.g. CPU-intensive video encoding vs lightweight CRUD).

---

## 3. Architecture Decision Record (ADR) Standard (`.ai/DECISIONS.md`)

When an architectural decision is adopted, document it using this format:

```markdown
## ADR-00X — [Short Descriptive Title]
**Status:** Accepted | Proposed | Deprecated | Superseded by ADR-YYY  
**Date:** YYYY-MM-DD  
**Deciders:** [Architects / Team Members]

### Context & Problem Statement
What technical challenge or product requirement are we addressing? What constraints exist?

### Decision
What specific architecture, technology, library, or pattern are we committing to?

### Rationale & Tradeoffs Considered
- **Option A (Chosen):** Key benefits, accepted trade-offs, and operational risks.
- **Option B (Rejected):** Why this alternative was considered and ultimately rejected.

### Evidence & Verification
References to benchmarks, documentation, or prototype results validating this decision.
```
