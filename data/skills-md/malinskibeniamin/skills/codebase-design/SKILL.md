---
name: codebase-design
description: Design deep modules with small interfaces. Use when choosing seams, reducing file-hop friction, deepening modules, testing APIs, or applying shared design vocabulary.
---

Design **deep modules**: substantial behavior behind a small interface at a clean seam, testable through that interface. Optimize caller leverage, maintainer locality, and testability.

Depth must improve semantic density now. No modules, seams, adapters, or interfaces for hypothetical reuse. A design wins only when it removes more caller knowledge/coordination than it adds.

## Glossary

Use exactly:

**Module** -- interface plus implementation: function, class, package, slice.

**Interface** -- everything callers know: types, invariants, ordering, errors, config, performance; broader than signature.

**Implementation** -- module internals.

**Depth** -- interface leverage. **Deep** means small interface/large behavior; **shallow** means similar interface and implementation complexity.

**Seam** -- where behavior can vary without editing the caller; its interface lives here. Avoid: boundary, except DDD bounded context.

**Adapter** -- concrete implementation at a seam, named by role.

**Leverage** -- capability per interface learned.

**Locality** -- change, bugs, knowledge, verification concentrate together.

Ask whether methods/parameters can shrink and more complexity can hide.

## Principles

- Depth is an interface property, not line ratio; private seams need not leak.
- **Deletion test:** if removal makes complexity vanish, the module was pass-through; if complexity spreads into callers/tests, it earned its keep.
- **The interface is the test surface:** callers and tests cross the same seam. Testing past it signals a weak shape.
- **One adapter is a hypothetical seam; Two adapters means a real one.**
- Direct local code beats an abstraction that only moves code.

## Testability

1. Accept dependencies; do not create them internally.
2. Return results; minimize ambient side effects.
3. Keep methods/parameters few and invariants clear.

When two designs survive deletion, use `/plan-arbiter` on depth, locality, test surface, and rollback.

Relationships: Module has one Interface; Depth is measured against it; Seam hosts it; Adapter satisfies it; Depth creates Leverage and Locality.

Reject depth-by-line-count, interface-as-TypeScript-keyword, and vague boundary wording.

Read [DEEPENING.md](DEEPENING.md) for dependency/seam/testing discipline and [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) for parallel designs.
For reader load, structural enforcement, and first-principles integration, use the shared
[Poteto engineering rules](../shared/POTETO-ENGINEERING.md) instead of duplicating them here.
