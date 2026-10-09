---
name: refactoring-best-practices
description: Safe refactoring guidance for legacy and existing codebases. Use when improving design without changing behavior, creating seams around hard dependencies, migrating null/string/generic exceptions to typed failure contracts, extracting a repository from direct SQL/ORM access, introducing Domain Events into legacy workflows, adding characterization tests, splitting large classes or methods, introducing value objects, replacing conditionals, or incrementally evolving code under risk.
license: MIT
metadata:
  author: luckys
  version: "1.0.0"
---

# Refactoring Best Practices

Use this skill when the main challenge is changing existing code safely.

## Working Style

1. Protect behavior before improving design.
2. Prefer small reversible moves over dramatic rewrites.
3. Add feedback before adding abstraction.
4. Change one responsibility at a time.
5. Let the current pain point decide the next move.

## Safe Refactoring Workflow

1. Observe current behavior.
   - Identify outputs, side effects, and error paths.
   - Identify what must not change.

2. Add feedback.
   - Prefer characterization tests around visible behavior.
   - Add logs or temporary probes only when tests are not enough.

3. Find a seam.
   - Isolate time, file system, network, framework globals, singletons, and external APIs.
   - Create the narrowest possible boundary around the risky dependency.

4. Choose the next move.
   - extract method
   - extract class
   - introduce value object
   - introduce first-class collection
   - move method
   - replace conditional with polymorphism
   - separate construction from behavior
   - extract a Domain Event and one secondary subscriber

5. Re-run feedback after every meaningful step.

## High-Value Refactoring Moves

- Replace a cohesive domain parameter group with a Value Object; use a Parameter Object when the group has no shared domain meaning or invariant.
- Break large services into role-focused collaborators.
- Move business rules out of controllers, scripts, and utility classes.
- Replace type codes and unstable conditionals with explicit roles.
- Wrap infrastructure behind ports or adapters.
- Split classes when different method clusters change for different reasons.

## Red Flags

- Big-bang rewrites.
- New abstractions without a protected behavior baseline.
- Splitting code into tiny classes without a clearer model.
- Introducing inheritance only to make tests easier.
- Refactoring based on aesthetics alone while ignoring risk.

## Decision Rules

### Refactor now when

- the same knowledge is duplicated in multiple places
- the code is blocking a real change
- the next feature would deepen coupling or duplication
- the current structure makes defects likely

### Wait when

- there is no feedback loop yet
- the pain is hypothetical
- the abstraction is not yet stable enough to deserve a new type
- the change is broad but the understanding is still weak

## References

- Read `references/safe-change-workflow.md` for seam-based refactoring guidance, sensing and separation, and the legacy code change algorithm.
- Read `references/refactoring-moves.md` for tactical moves, including the incremental Value Object migration sequence, and when to use them.
- Read `references/code-smells.md` when recognizing a problem, using temporal co-change as design evidence, and choosing the right move.
- Read `references/legacy-code-techniques.md` for Sprout, Wrap, Extract and Override, and other techniques for working without tests.
- Read `references/characterization-tests.md` for how to write tests before refactoring untested code.
- Read `references/domain-event-migration.md` for incrementally moving legacy side effects to events/subscribers, preserving failure semantics, durable handoff, and CDC as a migration bridge.
- Read `references/error-contract-migration.md` for safely replacing nulls, strings, and generic exceptions while preserving failure timing, diagnostics, redaction, and public contracts.
- Read `references/fran-iglesias-refactoring-guidance.md` for practical refactoring heuristics distilled from Fran Iglesias.
- Read `references/language-examples.md` for before/after style examples in multiple languages.

## Related Skills

- Use `oop-best-practices` for everyday new code decisions.
- Use `design-patterns-best-practices` when the main issue is choosing an object collaboration pattern.
- Use `ddd-best-practices` when moving invariants, splitting a God Aggregate, introducing a root, changing a consistency boundary, or shaping a domain Repository extracted from legacy persistence.
- Use `data-migration-best-practices` for moving or backfilling persisted data; this skill owns only the safe code seams and compatibility paths around that operational migration.

## Source Influences

This skill is synthesized from ideas emphasized in:

- `Working Effectively with Legacy Code` by Michael Feathers
- `99 Bottles of OOP` by Sandi Metz
- `Practical Object-Oriented Design in Ruby` by Sandi Metz
- Fran Iglesias's `Object Calisthenics` series
- [CodelyTV Aggregates course](https://github.com/CodelyTV/aggregates-course) (temporal coupling and Aggregate evolution)
- [CodelyTV Value Objects course](https://github.com/CodelyTV/value_objects-course) (incremental primitive-to-domain-value refactoring)
- [CodelyTV Repository Pattern course](https://github.com/CodelyTV/repository_pattern-course) (incremental direct-SQL-to-port refactoring)
- [CodelyTV Domain Events course](https://github.com/CodelyTV/domain_modeling-domain_events-course) (legacy event seams and CDC counterexamples)
- [CodelyTV Domain Modeling Errors course](https://github.com/CodelyTV/domain_modeling-errors-course) (incremental exception-to-Result and boundary-contract lessons)
- [CodelyTV Four Rules of Simple Design course](https://github.com/CodelyTV/four_rules_of_simple_design-course) (behavior-preserving tests, speculative-element deletion, and duplication counterexamples)
