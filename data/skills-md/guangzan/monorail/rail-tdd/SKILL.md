---
name: rail-tdd
description: Test-driven development with red-green-refactor. Use when building a behaviour test-first, fixing a bug with a regression test, or when rail-build needs TDD at an agreed seam.
---

# Rail TDD

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping.

When exploring the codebase, read `docs/monorail/CONTEXT.md` (if it exists — check with the shell, not a search tool, which skips gitignored paths) so vocabulary matches the project's domain language, and respect ADRs under `docs/monorail/adr/` in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. A good test reads like a specification and survives refactors.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary you test at. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test.

- **Standalone `/rail-tdd`:** confirm the seams with the user once before writing. No test is written at an unconfirmed seam.
- **Inside `/rail-build`:** the task's `Seams:` line is already agreed — it was set at slice time from the spec's code-anchored `## Testing Decisions`. Record it, do **not** re-confirm with the user; if opening the seam's anchor file shows the code contradicts a listed seam, stop and report per build §4 rather than re-deriving seams. No test is written at a seam not on the task's `Seams:` line.

Ask: "What's the public interface, and which seams should we test?"

## Anti-patterns

- **Implementation-coupled** — mocks internals, tests private methods, or verifies via side channels. Tell: breaks on refactor with unchanged behaviour.
- **Tautological** — assertion recomputes the expected value the way the code does. Expected values need an independent source of truth.
- **Horizontal slicing** — all tests first, then all implementation. Work in **vertical slices** instead — one test → one implementation → repeat.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactor after green.** When the suite is green, look for [refactor candidates](refactoring.md). Never refactor while red. Re-run tests after each refactor step.

## Completion

A behaviour is done when its failing test went red, then green, any needed refactor kept the suite green, and the agreed seam still holds.
