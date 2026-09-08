---
name: architecture-patterns
description: "Architectural decision guide by complexity. Trigger: When choosing architecture, planning strategic refactoring, or evaluating pattern trade-offs."
license: "Apache 2.0"
metadata:
  version: "1.0"
  type: universal
---

# Architecture Patterns

Decision guide for choosing architectural approaches by project complexity, team size, and context. Orchestrates architectural thinking without coupling to specific patterns.

## When to Use

- Deciding WHEN to apply architecture vs keeping it simple
- Choosing architectural approach by project complexity
- Planning strategic refactoring (module boundaries, layers)
- Understanding frontend vs backend architectural differences
- Evaluating architecture trade-offs

Don't use for:

- Learning specific patterns → use pattern-specific skills (solid, domain-driven-design, clean-architecture)
- Tactical refactoring (rename, extract, inline) → use code-refactoring skill
- Code review → use critical-partner skill

---

## Critical Patterns

### ✅ REQUIRED: Complexity-Driven Architecture

Match architecture complexity to project size and team.

```
Small (1-3 devs, <10k LOC):
  → Keep simple — folder structure + code-conventions is enough
  → Apply: Basic separation (routes, components, utils)
  → Avoid: Layered architecture, DDD, Clean Architecture (overkill)

Medium (4-10 devs, 10k-100k LOC):
  → Modular architecture — clear module boundaries
  → Apply: Single responsibility per module, layer separation
  → Consider: Clean Architecture for testability

Large/Enterprise (10+ devs, >100k LOC, multiple teams):
  → Full architectural approach required
  → Apply: Strict boundaries, domain-driven modules, hexagonal for testability
  → Consider: DDD for complex business domains
```

**Guideline**: Start simple. Apply architecture when pain points emerge.

### ✅ REQUIRED: Recognize Architecture Pain Points

Apply architecture when you see these signals:

```
❌ Files >500 lines with mixed responsibilities
❌ Changing one feature breaks unrelated features
❌ Tests require 5+ mocks to test one unit
❌ New devs take >2 weeks to make first contribution
❌ Same bug fixed multiple times in different places
```

### ✅ REQUIRED: Frontend vs Backend Architecture

Different architectural concerns by platform:

```
Frontend architecture:
  → Component hierarchy and composition
  → State management boundaries (local vs global)
  → Data fetching and caching strategies
  → Route-based code splitting

Backend architecture:
  → Request/response flow layers
  → Business logic isolation from infrastructure
  → Database access patterns
  → API contract design
```

**Common mistake**: Applying backend patterns (repositories, use cases) to simple frontends. Most SPAs need state management + component composition, not full Clean Architecture.

### ✅ REQUIRED: Strategic vs Tactical Refactoring

```
Tactical (use code-refactoring skill):
  → Rename variables/functions
  → Extract small function
  → Inline variable

Strategic (THIS skill):
  → Define module boundaries
  → Separate layers (presentation, domain, data)
  → Extract entire modules
  → Redesign dependencies

When to refactor strategically:
  → Files >500 lines
  → Changing one feature breaks unrelated features
  → Tests require mocking 5+ dependencies
```

---

## Decision Tree

```
Choosing architecture approach?
  → Small project (<10k LOC, 1-3 devs)?
    → Keep simple - folder structure + code-conventions
  → Medium project (10k-100k LOC, 4-10 devs)?
    → Apply modular architecture - clear module boundaries
  → Large project (>100k LOC, 10+ devs)?
    → Apply full architecture - strict boundaries, domain-driven

Frontend or backend?
  → Frontend → Focus: component composition, state management, data fetching
  → Backend → Focus: layer separation, business logic isolation, API contracts

Planning refactoring?
  → Tactical (rename, extract, inline)?  → Use code-refactoring skill
  → Strategic (modules, layers)?         → Use THIS skill

Need specific pattern knowledge?
  → SOLID principles              → solid skill
  → Clean Architecture            → clean-architecture skill
  → Domain-Driven Design          → domain-driven-design skill
  → Ports and Adapters            → hexagonal-architecture skill
  → Domain-first folder structure → screaming-architecture skill
  → Error handling pattern        → result-pattern skill
  → Eliminate duplication         → dry-principle skill
  → Decoupled communication       → mediator-pattern skill
  → State / workflow modeling     → state-machines-pattern skill
  → Flexible component APIs       → composition-pattern skill
  → Fault tolerance / fast fail   → circuit-breaker-pattern skill
  → Microservice sidecar          → sidecar-pattern skill
```

---

## Example

Repository + Service Layer pattern applied to a user feature in a medium-sized backend.

```
Request: POST /api/v1/users
         ↓
UserController          (Presentation)
  → validates input with zod
  → calls UserService.createUser(dto)
         ↓
UserService             (Business Logic)
  → checks email uniqueness
  → hashes password
  → calls UserRepository.save(user)
         ↓
UserRepository          (Data Access)
  → IUserRepository interface defined in application layer
  → PostgresUserRepository implements it in infrastructure
  → returns saved User entity
         ↓
UserController
  → maps result to 201 Created + UserResponseDTO
```

Why this fits a medium project (4-10 devs, 10k–100k LOC):

- Clear layer boundaries make code navigable for new team members
- Repository interface lets tests inject in-memory fakes (no DB required)
- Service layer owns business rules (uniqueness, hashing) — not the controller

---

## Edge Cases

**Over-engineering**: Applying Clean Architecture to a 1000-line app. Start simple, add architecture when pain emerges.

**Under-engineering**: No architecture in 100k LOC app with 10 devs. Technical debt compounds, velocity slows dramatically.

**Premature abstraction**: Creating 5 layers before knowing requirements. Apply YAGNI — add layers when needed, not speculatively.

**Frontend Clean Architecture**: Usually overkill for React apps. State management (Redux/Zustand) + smart component composition is sufficient for most cases.

---

## Checklist

- [ ] Project complexity assessed (small/medium/large)
- [ ] Architecture approach chosen for complexity level
- [ ] Frontend vs backend context considered
- [ ] Strategic vs tactical refactoring distinguished
- [ ] Specific pattern skills consulted if needed

---

## Resources

- [code-refactoring](../code-refactoring/SKILL.md) — Tactical refactoring patterns
- [frontend-dev](../frontend-dev/SKILL.md) — Frontend workflow and patterns
- [backend-dev](../backend-dev/SKILL.md) — Backend workflow and patterns

**Pattern-specific skills:**

- [solid](../solid/SKILL.md), [clean-architecture](../clean-architecture/SKILL.md), [domain-driven-design](../domain-driven-design/SKILL.md)
- [hexagonal-architecture](../hexagonal-architecture/SKILL.md), [screaming-architecture](../screaming-architecture/SKILL.md)
- [result-pattern](../result-pattern/SKILL.md), [dry-principle](../dry-principle/SKILL.md)
- [mediator-pattern](../mediator-pattern/SKILL.md), [composition-pattern](../composition-pattern/SKILL.md)
- [state-machines-pattern](../state-machines-pattern/SKILL.md), [circuit-breaker-pattern](../circuit-breaker-pattern/SKILL.md)
- [sidecar-pattern](../sidecar-pattern/SKILL.md)

**Integration examples:**

- [backend-integration.md](references/backend-integration.md) — Architecture in Node.js/NestJS/Express
- [frontend-integration.md](references/frontend-integration.md) — Architecture in React + Redux
