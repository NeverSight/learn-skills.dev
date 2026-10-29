---
name: lettuce
description: "Test-driven development: the red → green → refactor loop of tests. Use when building a feature or fixing a bug test-first, or before planning or adding any test."
---

# Test-Driven Development

TDD is the red → green → refactor loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, how many, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

A good test is **sociable** and **state-based**: it runs the real collaborators and asserts on a returned value, resulting state, or tracked output. Where the code under test touches the outside world (database, files, network, clock, environment), that dependency is a **Nullable**, its own class with the outside world switched off. Before the first test at such a seam, call the Skill tool with "nullables": it owns `create()`/`createNull()`, Configurable Responses and Output Tracking.

See [tests.md](tests.md) for examples.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and the tests planned at each, one line per test: its name, the regression only it catches, its owner search (where you looked for a test already red on that regression, and what you found: none, or the test it extends), and its cost when it crosses a process, database or network boundary. Confirm the list with the user. No test is written at an unconfirmed seam, and a test the loop turns up later goes on the list, with its line, before it is written. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Owners: how many tests

Each behaviour has one **owner** test, at the highest seam that shows it. Tests of its dependents assert only what the dependent adds. James Shore: "don't test all phases of the moon in your describeMoonPhase() tests, but do test them in your Moon tests."

- **Name the regression.** Before adding a test, name the bug that would turn it red, then search for its owner: grep the tests at every seam the behaviour passes through, above and below this one, for the operation or a distinctive literal. When an existing test already goes red on that bug, extend that test or add a row to its table. Where two seams meet, follow the project's owner rules (its coding standards); where it has none, settle the owner with the user and record it there.
- **Equivalence classes.** Cases cover one ordinary value, each value the code treats differently, and the boundaries between them: one refused input per guard. A list the types already fix gets one row per class the code treats differently, not one per member.
- **Removed behaviour.** A change that removes a behaviour removes the tests and assertions that checked it, so none is left asserting about something that's gone.
- **Cost.** A test that crosses a process, database or network boundary costs orders of magnitude more than an in-memory one, on every run. It covers only what that boundary alone shows, such as a query or a file format.

## Anti-patterns

- **Implementation-coupled**: asserts on how the code works rather than what it does: assertions on how a mocked or spied-on collaborator was called (`jest.mock`, `vi.spyOn`), private methods, or a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed. The cure is a sociable test that asserts on a value, a state, or tracked output, which for a UI component includes what its callback props received (the `nullables` skill).
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **Green on first run is a finding.** A new test that passes the first time it runs is either checking a behaviour that already exists, whose owner is likely another test to extend, or one that can't go red. Find which before keeping it: search for the owner again, then break the code it guards, watch the test go red, and restore the code. The same goes for a test moved or written for existing code.
- **One slice at a time.** One seam, one behaviour, one minimal implementation per cycle. The behaviour's test is a new owner, or a row in the owner it extends.
- **Refactor on green, when it's due.** With the test green, look over the code the slice touched. When the slice left duplication, an unclear name, or a shape the next slice will fight, clean it up, keeping every test green. When it left the code clean, go straight to the next red. Review (the `code-review` skill) may turn up more to refactor afterwards, but that is optional.
