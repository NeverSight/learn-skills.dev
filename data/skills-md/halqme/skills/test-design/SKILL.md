---
name: test-design
description: Design, review, modify, or add tests as executable specifications of behavior. Use before touching tests/*, spec/*, *.test.*, or *.spec.* files, and when deciding what a change should verify. Focus on user-visible contracts, invariants, failure boundaries, recovery, and isolation—not implementation trivia. Do not use for implementation or documentation changes that do not alter test strategy.
---

# Test Design

Treat tests as executable specifications of behavior, not proof that code has a particular shape.

## Before editing

1. Inspect the production boundary, callers, existing tests, fixtures, package scripts, and CI.
2. Write acceptance conditions as observable outcomes:
   - caller/user-visible results;
   - durable or external effects;
   - invariants that must hold;
   - rejection or recovery for invalid, concurrent, or failed inputs.
3. Separate contract from implementation detail. Do not add a test solely for function names, private state, call counts, registration counts, or tool names unless explicitly public and compatibility-critical.
4. Choose the smallest useful boundary:
   - prefer an integration test through the public API;
   - use unit tests for pure transformations, resolution, or isolated failure-prone logic;
   - do not mock away the state transition under test.

## Cases to cover

For each material acceptance condition, consider:

- **Success:** minimal valid input produces the expected result.
- **Boundaries:** empty, multiple, Unicode, limits, ranges, and file layouts.
- **Failure:** invalid input, missing targets, unsupported formats, syntax errors, and I/O/permission errors.
- **Recovery:** pass returned `next`, handles, continuations, or retry inputs unchanged into the next call and complete successfully.
- **Staleness/concurrency:** if the target changes after discovery or confirmation, reject safely or require revalidation.
- **Non-effect:** failed operations do not modify files, databases, caches, or external state.
- **Ambiguity:** multiple matches do not silently select the first candidate.

Use the smallest fixture that isolates one failure mechanism. Do not make large fixtures pass accidentally.

## LLM and tool APIs

Test actual call sequences, not descriptions or schemas alone.

- Parse the first response and pass its `next`, handle, or continuation unchanged to the next call.
- If text content and structured details represent the same contract, assert they agree.
- Test that structured recovery completes the task; merely checking that a Hint exists is insufficient.
- Include natural model mistakes such as directory-vs-file paths, stale IDs, missing targets, and ambiguous matches.
- Test tool registration names only when they are an explicit compatibility contract; otherwise test the operation's result.
- Exercise real state transitions instead of mocking away the boundary.

## Isolation and lifecycle

- Each test must be independent: isolate or reset shared databases, parsers, caches, environment variables, cwd, and global state.
- Do not trigger process-global shutdown or singleton teardown inside one test when later tests share the process. Use one suite teardown or an explicit reset API.
- Give temporary files, ports, and external resources unique names and clean them up after failure as well as success.
- Avoid dependence on time, randomness, or execution order; isolate non-parallelizable state.

## Review each test

A test should answer:

1. What meaningful regression makes it fail?
2. What user, caller, integrity, or safety impact does that regression have?
3. Would it survive an internal rewrite that preserves the contract?
4. Would it fail when the relevant behavior is broken?
5. Does it verify failure side effects and recovery where relevant?

Do not use test count, coverage, snapshot size, or registration count as quality proxies. More tests do not help if important contracts, failures, recovery, or non-effects remain untested.

## Verification

1. Run the narrowest relevant tests first, then broaden proportionally.
2. Map each acceptance condition to evidence from success, failure, recovery, and non-effect cases.
3. Challenge the suite with an internal rewrite that should preserve the contract and a targeted break that should fail.
4. Report skipped boundaries, shared state, external dependencies, and nondeterminism.

Do not add tests while the contract or expected result is unclear. If only implementation trivia can be tested, first identify the public boundary or acceptance condition. Replace low-value tests with fewer public-path tests before increasing test count.
