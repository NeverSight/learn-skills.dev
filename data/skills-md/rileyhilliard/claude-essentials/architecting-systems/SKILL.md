---
name: architecting-systems
description: Guides clean, scalable system architecture during the build phase. Use when designing modules, defining boundaries, structuring projects, managing dependencies, or preventing tight coupling and brittleness as systems grow.
---

# Architecting Systems

**Core principle:** Small decisions made early compound into either clean systems or massive technical debt. Get the structure right and the system stays maintainable as it grows. Get it wrong and every change gets harder.

## Topic Selection

Load the relevant reference based on what you're working on:

| Working on... | Load | File |
|---------------|------|------|
| Layers, vertical slices, file organization | **Structure** | `references/structure.md` |
| Interfaces, dependency inversion, contracts | **Coupling** | `references/coupling.md` |
| Bounded contexts, API design, module boundaries | **Boundaries** | `references/boundaries.md` |
| Async patterns, race conditions, queues | **Concurrency** | `references/concurrency.md` |
| Logging, health checks, metrics, tracing | **Observability** | `references/observability.md` |

Load multiple references when the task spans topics. For most greenfield work, start with **Structure** and **Coupling**.

---

## Core Principles (All Topics)

### Convention over invention

Default to established patterns, standard libraries, and proven conventions. Novel solutions carry hidden costs: documentation burden, onboarding friction, and maintenance surprises.

| Prefer | Over |
|--------|------|
| Framework conventions | Custom project structures |
| Standard library tools | Bespoke utilities for solved problems |
| Established patterns (MVC, repository, etc.) | Clever abstractions |
| Boring technology that works | Exciting technology that might |

**The test:** If someone new joins the team, how quickly can they find things and understand the structure? If the answer involves a tour guide, the conventions aren't strong enough.

### State management

State is where complexity hides. The more places state lives and the more things can mutate it, the harder the system is to reason about.

- **Minimize mutable shared state.** If two modules need the same data, one should own it and the other should request it.
- **Keep state close to where it's used.** Global state is almost never the answer.
- **Make state changes explicit.** Whether that's through events, reducers, or explicit setter methods, the "what changed and why" should be traceable.
- **Single source of truth.** Every piece of data should have one authoritative home. Derived data should be computed, not independently stored, unless there's a measured performance reason to cache or denormalize.

### Design for change

- **Make the common path easy.** If doing the right thing requires extra effort, people will take shortcuts. Good defaults, templates, and guard rails beat documentation.
- **Enforce with tooling, not docs.** Linting rules, CI checks, and architectural tests scale. Wiki pages and team agreements don't. If a convention matters, make violations fail the build.
- **Isolate volatility.** Wrap external integrations in adapters. Isolate business rules in the domain layer. Keep presentation thin. Abstract storage behind repositories.
- **Prefer composition over inheritance.** Combine small, focused pieces rather than extending complex base classes.

### Complexity budget

Every architectural decision has a complexity cost. Spend that budget where it matters.

| Worth the complexity | Not worth it |
|---------------------|--------------|
| Separation between domains that change independently | Abstracting code that only has one implementation |
| Event-driven for genuinely async workflows | Event-driven for simple request-response flows |
| Caching for measured performance bottlenecks | Caching "just in case" |
| Microservices for teams that deploy independently | Microservices for a small team's monolith |

**The rule:** Don't add indirection until you need it. Premature abstraction is as costly as premature optimization. Two similar code blocks are better than a wrong abstraction.

---

## Quick Reference

| Problem | Response |
|---------|----------|
| "Where does this code go?" | If the answer isn't obvious, the structure needs work |
| "Changing X requires touching Y" | Missing boundary between X and Y |
| "This module does too many things" | Split along separate reasons to change |
| "We can't test this in isolation" | Hidden dependencies; inject them instead |
| "New devs take weeks to be productive" | Conventions are too weak or too novel |
| "Every PR touches 10 files" | Feature code is scattered; colocate it |
| "The shared folder keeps growing" | Boundaries are in the wrong place |

**Writing architecture documents?** This skill covers how to build. For how to write about it (ADRs, design docs, tradeoff analyses), load `Skill(ce:writer)` and use The Architect persona.
