---
name: test-value
description: Evaluate test value when choosing tests to write, reviewing new or changed tests, or assessing an existing test suite.
---
Evaluate test value for the requested scope: choosing tests to write, reviewing new tests, or reviewing existing tests.

Favor tests that detect consequential bugs, tolerate behavior-preserving changes, and make failures easy to diagnose at proportionate cost.

Read the relevant implementation, consumers, tests, and helpers. Establish the meaningful contract and nearby coverage before judging individual tests. Assess:

- **Fault detection:** Identify plausible bugs the test distinguishes. Challenge assertions with missing work, empty/truncated output, wrong-source values, and incorrect ordering. Fixtures must separate competing decisions. Expected results must be independent of the production decision under test; compatibility claims need historical fixtures.
- **Meaningful behavior:** Connect the assertion to an external consequence. Internal contracts matter through their consumers. Property-copying and forwarding tests are presumptively low value; consequential mapping, protocol, or compatibility mistakes can justify exceptions.
- **Implementation coupling:** Flag assertions or setup that enforce a choice the required behavior leaves open—for example, object identity, call order, or exact formatting. Identify the unnecessary constraint and suggest how to relax it. Compilation repairs are acceptable maintenance; still-compiling tests that require setup changes after behavior-preserving changes indicate coupling.
- **Boundaries:** Test responsibilities where they belong. Exercise real production behavior with inexpensive real collaborators. Prefer test implementations over mocks for expensive dependencies. Check whether doubles supply the behavior supposedly being tested.
- **Contribution:** Explain the additional fault coverage or diagnostic help beyond existing tests. More cases or assertions alone add no value. Framework conventions should be covered through review or static checks, not tests.
- **Reliability:** Control time, culture, shared state, dependencies, and scheduling. Reproduce races deliberately. Intermittent tests need repair or redesign; retries do not establish reliability. Expose environmental failures clearly.
- **Diagnostics and cost:** Require an understandable discrepancy and practical reproduction. Weigh execution, feedback delay, fixture upkeep, and investigation effort. Larger integration tests can be preferable when they express intent better and justify their cost. Minimize steps and assertions; each addition must catch a distinct plausible fault.

Recommend:
- For proposed tests: **write, refine, or skip**, with decisive scenarios and assertions.
- For test code: **retain**, **repair** fixable weaknesses, **redesign** the boundary or approach, or **remove** insufficiently valuable coverage.

Distinguish a worthwhile requirement with a defective test from coverage not worth having.

Report prioritized recommendations with source locations, decisive evidence, and the smallest appropriate improvement. Account for the requested scope; disclose sampling and uncertainties. Distinguish inspected, executed, and measured evidence from hypothetical counterexamples and estimated costs. Use qualitative judgments rather than invented scores.

Apply code changes only when implementation is also requested.
