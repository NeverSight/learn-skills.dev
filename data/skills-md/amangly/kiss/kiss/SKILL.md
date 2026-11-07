---
name: kiss
description: Enforce KISS when implementing, refactoring, or reviewing code for simplicity. Use for /kiss, requests to remove over-engineering, or choosing the simplest complete solution to a concrete requirement.
---

# KISS: Strict Enforcement

Simplicity is mandatory. The simplest readable solution that fully satisfies the current requirement wins. Cleverness earns nothing. Minimize concepts and moving parts before counting lines.

Apply to the requested scope: implement when asked to build or simplify; report findings when asked to review. A bare invocation uses the active task or diff; ask for a target only when neither exists. No other skill is required.

## Mandatory rules

1. **Solve today's problem.** Complete the concrete requirement. No speculative features, unused flags, or future extension points.
2. **Take the shortest correct path.** Prefer fewer lines, files, dependencies, and abstractions when equally readable and correct. Preserve required behavior, validation, and error handling.
3. **Choose boring code.** Use clear names, plain loops, and readable steps. Expand clever chains and nested ternaries. A junior developer should grasp a function's purpose and flow in about 30 seconds.
4. **Wait for real reuse.** Small duplication beats premature abstraction. Reassess at the third occurrence; extract only a stable shared rule, never coincidental similarity.
5. **Keep flow flat.** Use guard clauses and early returns. Maximum two nested control-flow levels; the function body does not count. Split responsibilities, not arbitrary line ranges.
6. **Call directly.** Prefer concrete types and functions. Remove single-implementation interfaces, pass-through wrappers, and middleman classes unless they pass the complexity gate.
7. **Use existing tools.** Prefer standard-library, framework, and installed primitives before adding dependencies or custom frameworks.
8. **Understand before deleting.** Inspect callers, tests, history, and relevant decisions. Preserve real contracts, ownership boundaries, and incident fixes. Keep comments explaining non-obvious reasons; simplify code needing comments to explain basic operations.

## Stop and simplify

Resolve each trigger before adding more code: simplify it or justify it through the complexity gate.

| Trigger | Default correction |
| --- | --- |
| Function over ~30 lines doing multiple jobs, or cyclomatic complexity over 7 | Flatten branches; extract a cohesive responsibility |
| Interface with one implementation; abstraction with one consumer | Inline or use the concrete implementation |
| Factory/Builder/Strategy/Visitor for trivial logic | Use a function or direct construction |
| Configuration with 10+ optional flags | Remove unused options; separate actual concerns |
| Generics where concrete types fit | Use concrete types |
| Inheritance deeper than two links | Flatten or compose |
| Four or more forwarding layers for CRUD | Collapse layers without independent responsibility |
| DSL/wrapper around a short standard-library call | Use the existing operation |
| Cache, parallelism, or batching without measured need | Start with the straightforward version |

"Later", "more flexible", "elegant", and "a known pattern" are not evidence.

## Complexity gate

Additional complexity is allowed only when:

- Profiling proves the simple version misses a concrete performance requirement.
- Multiple real consumers need the same stable abstraction.
- The domain inherently requires it, such as a parser, compiler, or scheduler.
- A familiar pattern is the simplest correct expression of a current requirement or contract.

Name the evidence and why the simpler option fails. A framework-required interface or real external contract can qualify with one implementation; imagined substitution cannot. Leave unfamiliar existing code intact when its purpose remains unresolved, and report that uncertainty.

## Workflow and verification

1. **Bound the task.** Identify behavior, constraints, and an observable completion check. Read the relevant code and callers; reuse domain names. Reproduce bugs and measure performance claims.
2. **Build the minimum.** Implement one complete behavior at a time. Add options only for immediate needs.
3. **Read the diff cold.** Apply every trigger. Imagine deleting each abstraction: if complexity disappears, remove it; if required logic spreads across callers, it may earn its place.
4. **Check behavior.** Run relevant existing checks. Add focused regression or behavior tests when needed, testing observable contracts rather than private structure. Preserve supported cases and report checks that could not run.
5. **Check simplicity.** No speculative config, generics, dependencies, or unjustified wrappers remain. Target functions <=30 lines, cyclomatic complexity <=7, and enforce nesting <=2. Exceptions must pass the complexity gate; cosmetic extraction to game metrics fails.
6. **Report briefly.** State the result, verification, and justified complexity. Reviews give concrete findings and their simplest correction. Claim compliance only after inspecting the code and accounting for exceptions; never invent measurements.

Every element earns its place through behavior, correctness, or readability. Useful tests and explanations count even when removing them leaves runtime output unchanged.
