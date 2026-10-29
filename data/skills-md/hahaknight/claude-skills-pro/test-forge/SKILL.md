---
name: test-forge
description: >
  MUST USE when writing tests, 补测试/write tests/单元测试/test coverage,
  or when asked to verify a module with tests. Produces test suites that
  actually kill mutants: edge cases, boundaries, failure paths, property
  tests — not happy-path theater.
  Part of claude-skills-pro - 8 more skills (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) + 11-chapter CN handbook, all free: github.com/Hahaknight/claude-skills-pro
---

# Test Forge — Tests That Catch Real Bugs

## Philosophy

A test suite earns its keep by failing when the code is wrong. Before submitting, ask: "if I flipped a comparison operator or removed a null-check, would some test fail?" If not, the suite is decoration.

## Workflow

1. **Detect the framework** from existing tests / package.json / go.mod / Cargo.toml. Match the repo's test style, fixtures, and assertion library exactly. Do not introduce a new framework.
2. **Read the code under test fully** and list its behaviors as a table before writing anything:
   - every branch, every early return, every thrown error
   - boundary values for each input (0, 1, -1, empty, max, unicode, null/undefined, NaN)
   - external effects (I/O, network, clock, random, env) → decide mock vs real (prefer real for pure logic, fake clock/fake time, injected randomness)
3. **Test selection order** (highest value first):
   - Regression: any bug this code ever had → a named test
   - Boundaries & edge cases
   - Failure paths: errors propagate with useful messages; retries; cleanup on failure
   - Concurrency: race-prone paths get a stress test if the harness allows
   - Property-based tests for pure functions (invariants round-trip, idempotence, monotonicity) using fast-check / hypothesis / your lang's equivalent
   - Happy path last — it's usually already covered by the framework's examples
4. **Write the tests**: descriptive names that read as specifications — `rejectsExpiredToken_beforeRefreshBoundary`, not `test_case_3`. Arrange-Act-Assert with one behavior per test. Shared setup in beforeEach/fixtures, but keep each test independently readable.
5. **Prove the suite works — mutation check**: run the suite, then mentally (or actually, by temporarily breaking the code) verify key tests fail. Report: "mutated X, tests Y and Z failed". Delete tests that never catch anything.
6. **Run the full suite.** All green, no skips. If a test is flaky by nature (timing), mark it with the repo's flaky convention and say so.

## Output

- Files written + count of cases by category
- Coverage delta if the repo has coverage tooling (`npm run cover` / `go test -cover`)
- One line on what you deliberately did NOT test and why (e.g., "e2e payment flow — needs sandbox, tracked in #57")

## Anti-patterns

- Never mock what you own through another mock (mock calling a mock).
- Never assert on implementation details (private method calls, call counts) when the observable behavior can be asserted instead.
- Never `catch (e) { /* ignore */ }` inside a test — that's a test that can't fail.
- Never write snapshot tests as the primary coverage for logic; snapshots are for rendered output only.
- Don't chase 100% coverage — chase the failure modes. State your reasoning.
---

*(Part of [claude-skills-pro](https://github.com/Hahaknight/claude-skills-pro) — 15 skills in total: 7 MIT samples in-repo plus 8 more in the free full pack (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) and an 11-chapter CN handbook. Everything is free — grab the pack from [Releases](https://github.com/Hahaknight/claude-skills-pro/releases).)*
