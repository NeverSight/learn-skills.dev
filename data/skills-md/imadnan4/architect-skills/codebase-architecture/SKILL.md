---
name: codebase-architecture
description: How to organize CODE by business domain, not framework. Use when structuring folders/modules, monorepos, layered dependencies, module independence, code hygiene, detecting architecture smells, and refactoring.
when_to_use: |
  - organizing folders / modules, monorepos
  - layered dependencies, module independence
  - code hygiene, refactoring, detecting architecture smells
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Codebase Architecture & Project Organization

A project is a collection of independent systems that evolve together. **Folders are architecture;
structure communicates design.** Poor organization becomes technical debt.

## Golden rule

Never organize by framework — organize by **business domain**.

- Bad: `controllers/ services/ models/ routes/ utils/`
- Good: `billing/ authentication/ projects/ notifications/ payments/ users/`

The business should be visible from the root.

## Domain-driven organization & layout

Every feature owns its API, business logic, validation, tests, types, DB, events, docs — keep
related things together. Default top-level: `apps/ packages/ services/ workers/ docs/
infrastructure/ scripts/ tests/` (one purpose each).

**Monorepo (default):** single source of truth, shared types/UI/utils/architecture, simpler
refactoring, better AI context. Split repos only for organizational need.

```
apps/   web/ mobile/ admin/ desktop/
packages/  ui/ config/ types/ sdk/ eslint/ shared/
services/  auth/ billing/ inference/
workers/   indexing/ email/ cron/
```

## Layered dependencies (point inward)

```
UI → Application → Domain → Infrastructure      (never reverse; business logic never imports UI)
```

- **Domain:** rules, policies, entities, value objects, use cases, domain events — no framework/HTTP/DB.
- **Application:** orchestrates use cases, transactions, permissions, workflow.
- **Infrastructure:** DB, Redis, storage, queues, search, email, payments, cloud — replaceable, never leaks into domain.
- **Interface:** REST/GraphQL/gRPC/CLI/workers/webhooks/controllers — translate requests into app calls only.

## Module design rules

- **Independence:** what do I own? who depends on me? who do I depend on? can I be removed/replaced?
  Expose interfaces, not implementation.
- **Shared package rule:** put code in `shared/` only after ≥2 modules need it. Never prematurely.
- **No circular dependencies** — graph must stay acyclic.
- **Feature independence:** adding a feature shouldn't touch twenty files. High cohesion, low coupling.
- **Utils:** keep tiny; move business helpers into the domain. **Event boundaries:** prefer
  events/interfaces over importing internals. **Public interfaces:** one API per module; hide complexity.

## Code hygiene

- **Config** lives outside code — never hardcode URLs/secrets/ports/flags/env names.
- **Naming:** folders=domains, files=responsibilities, classes=concepts, functions=actions, variables=meaning.
- **Sizes:** files 100–300 (ok 500, avoid 1000+); functions do one thing; classes = one concept.
- **Tech debt** acceptable only when documented (reason, owner, removal plan). **Refactor** only when
  complexity/duplication drops or perf/readability/testability improves. **AI code is a draft** —
  review architecture/naming/deps/complexity/perf/security; never merge blindly.

## Architecture smells (stop & refactor)

God objects · massive services · huge controllers · circular imports · global state · shared
mutable data · deep inheritance · massive utils · feature scattering · duplicate logic.

**Health metrics:** high cohesion, low coupling, small modules, fast tests, clear ownership, good
docs, stable interfaces, simple deployments.

## Architecture checklist (before a module)

- [ ] Belongs to an existing domain? · No duplication? · Can be simpler?
- [ ] Another engineer/AI finds it? · Testable independently? · Scales independently? · Replaceable?

## Architecture decision tree

```
Organizing a codebase
  ↓
Group by business domain, NOT framework
  ↓
Shared logic across ≥2 modules? → packages/shared (else keep local)
  ↓
Module adds a responsibility? → single concept owns it? NO → split
  ↓
Cross-module call? → event / interface, not internal import
  ↓
Dependencies point inward? → YES, else reverse & fix
  ↓
Circular dependency? → FORBIDDEN → restructure
```

## Anti-patterns

- ❌ Organizing by framework folders (controllers/services/models)
- ❌ Circular dependencies · business logic leaking into UI/infra
- ❌ Premature `shared/` libraries · God objects / massive services / huge controllers
- ❌ Hardcoding config · merging AI-generated code without review · refactoring for preference

## Architecture prompts

- Does this belong to an existing domain or is it new?
- Does this duplicate existing functionality?
- Can another engineer (and the AI) understand it quickly?
- Can it be tested / scaled / replaced independently?
- Does the dependency graph stay acyclic and point inward?
