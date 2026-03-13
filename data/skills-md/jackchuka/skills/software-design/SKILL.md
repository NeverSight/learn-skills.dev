---
name: software-design
description: Opinionated guide to software design principles and architectural patterns. Use when reviewing code design, planning feature architecture, asking "is this the right design?", "how should I structure this?", or requesting design philosophy guidance. Triggers on questions about SOLID, DRY, KISS, YAGNI, Clean Architecture, DDD, hexagonal architecture, composition vs inheritance, coupling, cohesion, or any software design trade-off discussion.
compatibility: NA
metadata:
  author: jackchuka
  scope: generic
---

# Software Design Philosophies

Opinionated guidance on classic design principles and architectural patterns, with concrete code examples and trade-off analysis.

## When Applying Design Guidance

1. **Diagnose first** — Identify the specific design tension (coupling, cohesion, complexity, rigidity)
2. **Name the principle** — State which principle applies and why
3. **Show the trade-off** — Every principle has a cost; state it explicitly
4. **Demonstrate with code** — Before/after examples grounded in the user's codebase context

## Core Stance: Pragmatism Over Dogma

- Principles are heuristics, not laws. Apply them when they reduce complexity; skip them when they add it.
- Prefer boring, obvious code over clever, abstract code.
- The best design is the simplest one that handles current requirements. Speculative generality is a code smell.
- Three concrete duplications are better than one wrong abstraction (Rule of Three).

## Classic Principles Quick Reference

| Principle | One-liner                        | Apply when...                                     | Skip when...                                           |
| --------- | -------------------------------- | ------------------------------------------------- | ------------------------------------------------------ |
| SRP       | One reason to change             | A module mixes unrelated concerns                 | Splitting creates indirection with no clarity gain     |
| OCP       | Extend, don't modify             | You need plugin-style variation                   | You're still discovering requirements                  |
| LSP       | Subtypes must be substitutable   | Building type hierarchies                         | Using composition instead                              |
| ISP       | Small, focused interfaces        | Clients depend on methods they don't use          | Interface has natural cohesion                         |
| DIP       | Depend on abstractions           | You need testability or swappable implementations | Only one implementation exists or will ever exist      |
| DRY       | Single source of truth           | Identical logic with identical reasons to change  | Similar-looking code with different reasons to change  |
| KISS      | Simplest solution that works     | Always the default                                | Never skip this                                        |
| YAGNI     | Don't build it until you need it | Tempted to add "just in case" features            | Building foundational APIs with known extension points |

For detailed explanations, examples, and anti-patterns for each principle, see [references/principles.md](references/principles.md).

## Architectural Patterns Quick Reference

| Pattern         | Best for                                   | Avoid when                                     |
| --------------- | ------------------------------------------ | ---------------------------------------------- |
| Clean/Hexagonal | Long-lived systems with complex domains    | Simple CRUD apps, prototypes                   |
| DDD             | Complex business logic with domain experts | Technical/infrastructure-heavy systems         |
| Event-Driven    | Decoupled workflows, audit trails          | Simple request/response flows                  |
| CQRS            | Read/write asymmetry, complex queries      | Uniform read/write patterns                    |
| Monolith-first  | New projects, small teams                  | Already proven need for independent deployment |
| Microservices   | Independent team deployment at scale       | Small team, shared database, tight coupling    |

For detailed guidance on each pattern including structure, trade-offs, and code examples, see [references/architecture.md](references/architecture.md).

## Decision Framework

When advising on design, follow this priority order:

1. **Does it work correctly?** — Correctness over elegance
2. **Can someone else read it?** — Clarity over cleverness
3. **Can it be tested?** — Testability over convenience
4. **Can it change safely?** — Isolation of change over DRY
5. **Does it perform adequately?** — Performance only when measured

## Common Design Smells and Remedies

| Smell                                                              | Likely violation                      | Remedy                              |
| ------------------------------------------------------------------ | ------------------------------------- | ----------------------------------- |
| God class / function                                               | SRP                                   | Extract cohesive responsibilities   |
| Shotgun surgery (one change touches many files)                    | Low cohesion                          | Colocate related logic              |
| Feature envy (method uses another object's data more than its own) | Misplaced responsibility              | Move method to the data owner       |
| Primitive obsession                                                | Missing domain concept                | Introduce a value type              |
| Deep inheritance trees                                             | Favoring inheritance over composition | Flatten with composition/interfaces |
| Boolean parameters                                                 | SRP, OCP                              | Split into separate functions       |
| Speculative generality                                             | YAGNI                                 | Delete unused abstractions          |

## Offering Guidance

When reviewing or advising:

- Reference the specific principle by name with a one-sentence rationale
- Show a minimal before/after code example in the user's language
- State the trade-off honestly ("this adds an interface but isolates the database dependency")
- If multiple principles conflict, state the tension and recommend based on context
- Load [references/principles.md](references/principles.md) for deep-dive principle discussions
- Load [references/architecture.md](references/architecture.md) for architectural pattern guidance
