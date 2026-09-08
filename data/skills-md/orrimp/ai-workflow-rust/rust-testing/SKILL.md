---
name: rust-testing
description: 'Use when writing, reviewing, or fixing Rust unit tests, integration tests, property tests, snapshots, mocks, fixtures, cargo test workflows, and embedded/no_std test strategies.'
argument-hint: 'Describe the Rust testing task, failure, or test coverage you need'
---

# Rust Testing

## When To Use
- Add unit tests for module-level behavior
- Add integration tests for crate-level or public API behavior
- Improve test coverage after a bug fix or refactor
- Debug failing `cargo test` runs, flaky tests, or missing fixtures
- Design mocks, fakes, or test helpers for local Rust development
- Plan host-vs-target testing for embedded no_std crates and hardware behavior

## Procedure
1. Decide the test scope first: unit tests for implementation details, integration tests for public behavior, doctests for API examples.
2. Reproduce the current failure or missing coverage with the narrowest useful `cargo test` target.
3. For embedded crates, split validation deliberately: host tests for pure logic and hardware-in-loop checks for peripheral and timing behavior.
4. Keep tests close to the behavior they verify. Prefer module-local tests for internal logic and `tests/` for external behavior.
5. Design APIs to be testable without hidden filesystem, network, clock, or environment dependencies. Pass these capabilities in explicitly when practical.
6. Prefer deterministic tests. Avoid time-based sleeps, shared mutable global state, and external service dependencies unless the test explicitly covers them.
7. When test-only escape hatches weaken production guarantees, guard them behind a clearly named feature such as `test-util`.
8. Use assertions that explain intent. Verify behavior and invariants, not just incidental formatting or implementation details.
9. Keep test code clean and idiomatic: descriptive names, focused helpers, and no commented-out experiments or leftover debug output.
10. Run the narrow test first, then broader validation when the change touches shared code.

## Testing Heuristics
- Prefer small fixtures built in code unless realistic file fixtures materially improve clarity.
- Mock I/O and system boundaries, not pure computation.
- For parsers and transformations, include invalid inputs and edge cases, not only happy paths.
- For error handling, assert the relevant error kind, message, or contextual accessor instead of only checking that the call failed.
- For async tests, keep task coordination explicit and avoid hiding race conditions with arbitrary delays.
- Use `use super::*` in unit tests when it improves readability, but otherwise keep imports explicit.
- Prefer direct, maintainable assertions over overly clever iterator or macro-heavy test construction.
- In no_std crates, test allocation-free paths and fixed-capacity behavior explicitly.
- Keep interrupt-related checks deterministic and avoid asserting on incidental timing jitter.

## Validation
- Start with targeted commands such as `cargo test module_name`, `cargo test test_name`, or `cargo test --test integration_name`
- Broaden to `cargo test` when the local change is stable
- Use `cargo clippy --tests` when test code itself is substantial
- For embedded targets, also run the target-specific check/build command used by the workspace

## Delivery Checklist
- Tests prove the intended behavior
- The narrowest relevant test command was run first
- Test-only helpers are clearly separated from production behavior
- New mocks or fixtures are justified and minimal
- Test code does not rely on commented-out cases, arbitrary sleeps, or leftover debug printing

## Results Presentation Template

When presenting completed testing work to the user, structure the response as:

**Changes Made:**
- List test files created or modified
- Summarize what behavior is now covered
- Note any test utilities or fixtures added

**Validation Results:**
```
cargo test <specific_test> → [PASSED/FAILED]
cargo test → [X passed, Y failed]
cargo clippy --tests → [clean/N warnings]
```

**Next Steps:**
Suggest 2-3 logical follow-ups based on context:
- "Run `cargo test --doc` to verify documentation examples"
- "Add integration tests in `tests/` for public API behavior"
- "Consider property-based tests with `proptest` for edge case coverage"
- "Add benchmarks with `criterion` if performance is critical"
- "For embedded targets, validate on hardware with [specific command]"
- "Improve coverage for error paths in [specific module]"

Keep the presentation concise. Link to modified files using workspace-relative paths. Skip sections that don't apply to the specific work completed.