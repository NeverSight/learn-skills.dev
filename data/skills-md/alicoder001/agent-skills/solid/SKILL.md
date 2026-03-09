---
name: solid
description: SOLID, DRY, KISS, and clean code principles for TypeScript applications. Use when designing scalable architecture, writing maintainable code, or reviewing code quality.
---

# Clean Code Principles

> Apply principles as constraints, not dogma. Prefer measurable maintainability over theoretical purity.

## Use This Skill When

- Refactoring complex modules with coupling and duplication.
- Reviewing architecture decisions or PR quality.
- Designing reusable TypeScript services/components.

## Principles to Apply

### SOLID

- SRP: one reason to change per unit.
- OCP: extend behavior without modifying stable core.
- LSP: subtype must preserve contract behavior.
- ISP: small consumer-focused interfaces.
- DIP: depend on abstractions, not concrete details.

### Supporting Rules

- DRY: remove duplicated business logic.
- KISS: prefer simple control flow and explicit naming.
- YAGNI: avoid speculative abstractions.

## Refactor Workflow

1. Detect smells:
- large functions/classes
- feature envy
- repeated condition branches
- temporal coupling
2. Write/extend tests around current behavior.
3. Extract boundaries:
- interfaces
- services
- adapters
4. Reduce responsibilities and dependencies.
5. Re-run tests and compare behavior.

## Code Review Checklist

- Does this change reduce or increase coupling?
- Are contracts explicit and stable?
- Is duplication reduced meaningfully?
- Are dependencies inverted where needed?
- Is complexity lower than before?

## Output Requirements for Agent

- Identify concrete smells with file-level evidence.
- Recommend smallest safe refactor sequence.
- State tradeoffs and migration risks.
- Provide test strategy for behavior preservation.

## References

- Detailed examples and before/after refactors: `references/guide.md`
