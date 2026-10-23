---
name: superior-lean
description: Simplify coding implementations and reviews by reusing existing capabilities and removing unjustified abstractions, dependencies, configuration, and duplication. Use when implementation complexity or over-engineering is in scope. Do not use to weaken required behavior, safety, accessibility, or compatibility.
license: MIT
---

# Superior Lean

Solve the complete requested problem with the least new surface area. Economy applies to the solution, not to understanding, correctness, or verification.

## Search for the smallest owner

Trace the affected flow and inspect callers before editing. Prefer, in order:

1. no change when the requested behavior already exists or the proposal is speculative;
2. an existing project helper, type, component, configuration point, or pattern;
3. the language standard library;
4. a native framework, browser, database, or operating-system capability;
5. an already-installed dependency;
6. a small local implementation with an explicit owner.

Stop at the first option that completely satisfies realistic behavior and fits the codebase. Fewer lines in the wrong layer are not simpler.

Read [references/complexity-decisions-and-safe-removal.md](references/complexity-decisions-and-safe-removal.md) when removing or collapsing a shared abstraction, dependency, configuration path, extension point, or code that appears unused. Use it to distinguish accidental machinery from a real boundary and to trace indirect consumers before deletion.

## Remove accidental machinery

Challenge:

- interfaces with one implementation and no stable boundary;
- factories for one fixed product;
- configuration for values that do not vary;
- wrappers that only rename an existing API;
- parallel utilities for a capability the repository already owns;
- speculative extension points, registries, flags, and migration scaffolds;
- dependencies whose complete contract can be replaced with less total ownership, not merely fewer visible lines;
- repeated guards that should be one root-cause fix.

Prefer deletion when behavior remains intact. Do not compress straightforward code into clever expressions merely to reduce line count.

Preserve an abstraction when evidence shows that it owns a real shared contract, external boundary, existing variation, compatibility transition, framework lifecycle, or independently testable policy. One implementation alone neither proves nor disproves that value.

## Complexity that must remain

Do not simplify away:

- explicit user requirements or supported compatibility;
- validation and authorization at trust boundaries;
- privacy, authentication, security, and audit controls;
- recovery needed to prevent corruption or data loss;
- accessibility and responsive behavior;
- real concurrency, ordering, retry, idempotency, or cancellation guarantees;
- calibration and tuning controls required by physical or variable systems.

## Verification

Prove that removed machinery had no required consumers and that behavior remains intact. Use focused tests for non-trivial branches, parsers, state transitions, financial paths, and security-sensitive flows. For a review, distinguish observed complexity from hypothetical cleanup and recommend only changes with a concrete payoff.

Report what became simpler, what was deliberately preserved, and the real condition that would justify adding complexity later.
