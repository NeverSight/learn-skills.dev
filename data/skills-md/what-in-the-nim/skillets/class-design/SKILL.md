---
name: class-design
description: Apply whenever designing, modifying, or reviewing a class.
---

# Class Design

A class owns one coherent concept, protects its invariants, and exposes a small, usable interface.

## Scope

Trace constructors, callers, wrappers, subclasses, configuration, tests, and resource owners. Inspect caller workarounds: repeated validation, leaked internals, manual ordering, duplicated state, defensive flags, and broad exception handling.

During implementation, apply these checks internally and keep edits within scope. Propose broader redesigns only when justified; implement them within existing authorization. For stateless pytest grouping classes, apply `testing-principle` instead of production lifecycle and class-justification rules.

## Rules

1. **Single responsibility.** Own one responsibility; split unrelated responsibilities.
2. **Cohesion.** Keep fields and methods focused on the same concept; separate independent state groups.
3. **Conceptual clarity.** Name the class after the concept it represents, and make its primary state and operations unsurprising from that name. A reader should be able to form a correct basic usage model without inspecting the implementation. Prefer conventional attribute and method names; avoid hidden roles, ambiguous state, and interfaces that require source-code archaeology.
4. **Minimal interface.** Expose necessary operations, preferably at the level of the caller's task. Each public method or mutable property adds states and misuse paths.
5. **Valid states.** Use explicit states or constrained representations to prevent contradictory combinations. Define transitions for non-trivial lifecycles.
6. **Lifecycle.** Define when the object is usable, allowed operations, resource ownership, cleanup, and initialization or shutdown failure behavior.
7. **Idempotent cleanup.** Repeated close, stop, cancel, cleanup, or unsubscribe calls must not corrupt state, leak resources, or race.
8. **Invariants.** Enforce correctness internally. Encapsulate operations that must happen together rather than relying on caller sequencing.
9. **Encapsulation.** Keep queues, locks, tasks, counters, transports, and caches private unless callers need them.
10. **Explicit dependencies.** Inject significant dependencies when internal construction would obscure configuration, testing, replacement, or ownership.
11. **Temporal coupling.** Simplify required call ordering; document and enforce remaining sequences through the interface or lifecycle states.
12. **Abstraction level.** Keep methods at consistent levels; delegate parsing, protocols, serialization, and persistence to appropriate components.
13. **Composition.** Prefer composition to deep inheritance. Use inheritance for substitutability, not implementation reuse alone.
14. **Concurrency ownership.** Define who creates, cancels, and awaits tasks; failure propagation; allowed concurrency; lifecycle races; and whether tasks can outlive the object. Owners clean up background work.
15. **Failure safety.** Preserve a defined, valid state after partial initialization, shutdown, cancellation, timeout, or failed transitions.
16. **Justify the class.** Require meaningful state, identity, invariants, lifecycle, resource ownership, encapsulation, polymorphism, or cohesive behavior. Otherwise use functions or modules.

## Review

Prioritize ownership, valid states, lifecycle, concurrency, failure and cancellation, idempotency, cohesion, interface, dependencies, then implementation structure. Correctness and misuse prevention outrank stylistic purity.

For requested reviews, report each finding as **rule number/name → concrete failure mode → minimal reproducing code → remedy**. Keep each example focused. If another review workflow owns the report, fit these details into its format. During implementation, report only findings affecting the requested change.

Assess all findings and relevant usage before choosing remedies. Shared causes may justify redesign; independent defects call for focused fixes. For a redesign, describe responsibility, state and invariants, interface and dependencies, lifecycle and concurrency ownership, caller responsibilities, and how each finding is addressed. Avoid theoretical abstractions.
