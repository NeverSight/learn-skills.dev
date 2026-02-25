---
name: dev
description: |
    Use when working with fundamental software development knowledge — patterns, algorithms, architecture, and craftsmanship principles drawn from canonical published works.
    USE FOR: development fundamentals, pattern selection, architecture decisions, algorithm choice, code quality principles, choosing between architectural styles
    DO NOT USE FOR: specific pattern implementations (use sub-skills: design-patterns, integration-patterns, algorithms, etc.), testing strategy (use testing), infrastructure (use iac)
license: MIT
metadata:
  displayName: "Development Fundamentals"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Refactoring.Guru — Design Patterns"
    url: "https://refactoring.guru/design-patterns"
  - title: "Enterprise Integration Patterns — Hohpe & Woolf"
    url: "https://www.enterpriseintegrationpatterns.com/"
  - title: "Martin Fowler — Software Architecture Guide"
    url: "https://martinfowler.com/architecture/"
---

# Development Fundamentals

## Overview
This skill covers the foundational knowledge every software developer should command — drawn from canonical published works and industry-proven practices. It spans from low-level algorithms through code craftsmanship to system-level architecture.

## Knowledge Map

```
┌─────────────────────────────────────────────────────────┐
│  Architecture                                           │
│  Microservices, Monoliths, DDD, Event-Driven,          │
│  Hexagonal, Well-Architected Frameworks                 │
├─────────────────────────────────────────────────────────┤
│  Frontend                    │  Backend                 │
│  SPA, PWA, Micro-frontends, │  Data Modeling, API      │
│  SSR, Islands Architecture  │  Design, Caching, Auth   │
├─────────────────────────────────────────────────────────┤
│  Integration Patterns        │  Design Patterns         │
│  EIP: Messaging, Routing,   │  GoF: Creational,        │
│  Transformation, Endpoints  │  Structural, Behavioral  │
├─────────────────────────────────────────────────────────┤
│  Algorithms & Data Structures                           │
│  Sorting, Searching, Graphs, DP, Combinatorial          │
├─────────────────────────────────────────────────────────┤
│  Craftsmanship                                          │
│  Clean Code, Clean Architecture, SOLID, 12-Factor,     │
│  Refactoring, Boy Scout Rule                            │
└─────────────────────────────────────────────────────────┘
```

## Canonical Works

| Book | Author | Covers |
|------|--------|--------|
| *Design Patterns* | Gamma, Helm, Johnson, Vlissides (GoF) | 23 object-oriented patterns |
| *Enterprise Integration Patterns* | Hohpe & Woolf | Messaging, routing, transformation |
| *The Art of Computer Programming* | Donald Knuth | Algorithms, data structures, combinatorics |
| *Clean Code* | Robert C. Martin | Naming, functions, formatting, comments |
| *Clean Architecture* | Robert C. Martin | Dependency rule, boundaries, layers |
| *Refactoring* | Martin Fowler | Code smells, refactoring catalog |
| *Domain-Driven Design* | Eric Evans | Bounded contexts, aggregates, ubiquitous language |
| *Building Microservices* | Sam Newman | Service decomposition, communication, deployment |
| *The Pragmatic Programmer* | Hunt & Thomas | Career, approach, tools, pragmatic philosophy |
| *The Twelve-Factor App* | Adam Wiggins (Heroku) | Cloud-native application methodology |
| *Release It!* | Michael Nygard | Stability patterns, capacity, deployment |
| *Fundamentals of Software Architecture* | Richards & Ford | Architecture styles, characteristics, decisions |

## Choosing the Right Pattern Category

| Problem | Look In |
|---------|---------|
| Object creation complexity | Design Patterns → Creational |
| Composing objects / adapting interfaces | Design Patterns → Structural |
| Object communication / state management | Design Patterns → Behavioral |
| Service-to-service messaging | Integration Patterns |
| Algorithm selection / optimization | Algorithms |
| Code readability and maintainability | Craftsmanship |
| System decomposition and boundaries | Architecture |
| Client-side application structure | Frontend |
| Server-side data and API structure | Backend |

## Best Practices
- Learn patterns as a vocabulary, not a checklist — apply them when the problem calls for it, not preemptively.
- Start with the simplest architecture that works (monolith), evolve toward complexity (microservices) only when you have evidence you need it.
- Apply the Boy Scout Rule: leave code better than you found it, every time you touch it.
- Use SOLID principles as guardrails for daily decisions, not just for greenfield design.
- Prefer composition over inheritance — most GoF patterns are variations of this principle.
- Study algorithms for problem-solving intuition, not memorization — know when to reach for a graph algorithm vs. dynamic programming.
- Keep integration patterns in mind whenever systems need to communicate — messaging solves problems that synchronous calls create.
