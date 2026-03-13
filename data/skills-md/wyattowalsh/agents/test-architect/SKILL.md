---
name: test-architect
description: >-
  Test strategy, coverage analysis, edge case identification, flaky test
  diagnosis. Use when designing test suites. NOT for running tests
  (devops-engineer), TDD, or code review (honest-review).
argument-hint: "<mode> [target]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Test Architect

Design test strategies, analyze coverage gaps, identify edge cases, diagnose flaky tests, and audit test suite architecture.

**Scope:** Test design and analysis only. NOT for running tests or CI/CD (devops-engineer), code review (honest-review), or TDD workflow.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `design <feature/module>` | Design test strategy and pyramid for a feature or module |
| `generate <file/function>` | Generate test cases (strategy text or actual test code based on context) |
| `gaps` | Analyze coverage gaps from coverage reports |
| `edge-cases <function>` | Systematic edge case identification for a function |
| `flaky` | Diagnose flaky tests from logs and code |
| `review` | Audit test suite architecture |
| Empty | Show mode menu with examples |

## Canonical Vocabulary

Use these terms exactly throughout all modes:

| Term | Definition |
|------|------------|
| **test pyramid** | Layered test distribution: unit (base), integration (middle), e2e (top) |
| **coverage gap** | Code path with no test coverage, weighted by complexity risk |
| **edge case** | Input at boundary conditions, null/empty, type coercion, overflow, unicode, concurrent |
| **flaky test** | Test with non-deterministic pass/fail behavior across identical runs |
| **mutation score** | Percentage of injected mutations detected by the test suite |
| **test strategy** | Document defining what to test, how, at what layer, with what tools |
| **property-based test** | Test asserting invariants over generated inputs (Hypothesis/fast-check) |
| **test isolation** | Guarantee that tests do not share mutable state or execution order dependencies |
| **fixture** | Reusable test setup/teardown providing controlled state |
| **test surface** | Set of public interfaces, code paths, and states requiring test coverage |

## Mode 1: Design

`/test-architect design <feature/module>`

### Surface Analysis

1. Read the feature/module code. Map the test surface: public API, internal paths, state transitions, error conditions.
2. Classify complexity: simple (pure functions), moderate (I/O, state), complex (distributed, concurrent, multi-service).

### Pyramid Design

3. Design test pyramid:
   - **Unit layer:** Pure logic, transformations, validators. Target: 70-80% of tests.
   - **Integration layer:** Database, API, file I/O, service boundaries. Target: 15-25%.
   - **E2E layer:** Critical user flows only. Target: 5-10%.
4. For each layer, list specific test cases with: description, input, expected output, rationale.
5. Recommend framework and tooling based on language/ecosystem.
6. Output: structured strategy document with pyramid diagram, case list, and priority order.

Reference: read references/test-pyramid.md for layer guidance.

## Mode 2: Generate

`/test-architect generate <file/function>`

1. Read the target file/function. Identify signature, dependencies, side effects.
2. Determine output format:
   - If test file exists for target: generate actual test code matching existing patterns.
   - If no test file exists: generate test strategy text with case descriptions.
   - If user specifies `--code`: always generate test code.
3. Generate test cases covering:
   - Happy path (expected inputs and outputs)
   - Error path (invalid inputs, exceptions, timeouts)
   - Edge cases (run edge-case-generator.py if function has typed parameters)
   - Boundary conditions (min/max values, empty collections, null)
4. Follow framework conventions: read references/framework-patterns.md for pytest/jest/vitest patterns.
5. Output: test cases or test code with clear section headers per category.

## Mode 3: Gaps

`/test-architect gaps`

1. Locate coverage reports. Search for:
   - `coverage.json`, `coverage.xml`, `.coverage` (Python/coverage.py)
   - `lcov.info`, `coverage/lcov.info` (JS/lcov)
   - `htmlcov/`, `coverage/` directories
2. Run coverage analyzer:
   ```
   uv run python skills/test-architect/scripts/coverage-analyzer.py <report-path>
   ```
3. Parse JSON output. Rank gaps by complexity-weighted risk.
4. For each gap, assess:
   - What code is untested and why it matters
   - Complexity score (cyclomatic complexity proxy)
   - Recommended test type (unit/integration/e2e)
   - Priority (P0: security/auth, P1: core logic, P2: utilities, P3: cosmetic)
5. Render dashboard if 10+ gaps:
   ```
   Copy templates/dashboard.html to a temporary file
   Inject gap data JSON into <script id="data"> tag
   Open in browser
   ```
6. Output: prioritized gap list with recommended actions.

Reference: read references/coverage-analysis.md for interpretation guidance.

## Mode 4: Edge Cases

`/test-architect edge-cases <function>`

1. Read the function. Extract parameter types, return types, and constraints.
2. Run edge case generator:
   ```
   uv run python skills/test-architect/scripts/edge-case-generator.py --name "<function_name>" --params "<param1:type,param2:type>"
   ```
3. Parse JSON output. Review generated categories:
   - **Null/empty:** None, "", [], {}, 0, False
   - **Boundary:** min/max int, float limits, string length limits
   - **Type coercion:** "123" vs 123, True vs 1, None vs "null"
   - **Overflow:** large numbers, deep nesting, long strings
   - **Unicode:** emoji, RTL text, zero-width chars, combining marks
   - **Concurrent:** race conditions, deadlocks, stale reads
4. For each edge case, provide: input value, expected behavior, rationale.
5. Flag cases where current code would likely fail (no guard, no validation).

Reference: read references/edge-case-heuristics.md for category details.

## Mode 5: Flaky

`/test-architect flaky`

### Log Collection

1. Locate test result logs. Search for:
   - CI logs, pytest output, jest output
   - `.pytest_cache/`, `test-results/`
   - Ask user for log path if not found
2. Run flaky test analyzer:
   ```
   uv run python skills/test-architect/scripts/flaky-test-analyzer.py <log-path>
   ```

### Root Cause Classification

3. Parse JSON output. For each flaky test:
   - Failure count vs pass count
   - Failure pattern (timing, ordering, resource, state)
   - Likely root cause classification:
     - **Timing:** sleep/timeout dependencies, race conditions
     - **Ordering:** test execution order dependencies
     - **Resource:** external service, database, file system
     - **State:** shared mutable state between tests
     - **Environment:** platform-specific, timezone, locale
4. Recommend fix strategy per root cause.
5. Prioritize by failure frequency and blast radius.

Reference: read references/flaky-diagnosis.md for root cause patterns.

## Mode 6: Review

`/test-architect review`

1. Scan the test suite. Map: test file count, framework(s), directory structure.
2. Assess architecture dimensions:
   - **Pyramid balance:** ratio of unit:integration:e2e tests
   - **Isolation:** shared state, global fixtures, test ordering dependencies
   - **Naming:** consistency, descriptiveness, convention adherence
   - **Coverage distribution:** even vs clustered coverage
   - **Fixture health:** duplication, complexity, setup/teardown balance
   - **Assertion quality:** specific assertions vs generic assertTrue
   - **Speed:** identify slow tests (>1s unit, >10s integration)
   - **Determinism:** potential flakiness indicators
3. Run coverage analyzer if reports exist.
4. Cross-reference with source code:
   - Untested public APIs
   - Tests for deleted/renamed code (orphaned tests)
   - Missing negative test cases
5. Output: architecture audit report with scores per dimension, findings, and recommendations.

Reference: read references/test-suite-audit.md for scoring criteria.

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| references/test-pyramid.md | Test pyramid layers, distribution targets, anti-patterns | Mode 1 (Design) |
| references/framework-patterns.md | pytest, jest, vitest patterns and conventions | Mode 2 (Generate), Mode 6 (Review) |
| references/coverage-analysis.md | Coverage report interpretation, complexity weighting | Mode 3 (Gaps) |
| references/edge-case-heuristics.md | Edge case categories by data type, generation strategies | Mode 4 (Edge Cases) |
| references/flaky-diagnosis.md | Flaky test root causes, fix strategies, prevention patterns | Mode 5 (Flaky) |
| references/test-suite-audit.md | Test architecture scoring rubric, quality dimensions | Mode 6 (Review) |
| references/property-testing.md | Property-based testing with Hypothesis and fast-check | Mode 1 (Design), Mode 2 (Generate) |
| references/mutation-testing.md | Mutation testing plan design, tool integration | Mode 1 (Design), Mode 6 (Review) |

| Script | When to Run |
|--------|-------------|
| scripts/coverage-analyzer.py | Mode 3 (Gaps) -- parse coverage reports |
| scripts/edge-case-generator.py | Mode 4 (Edge Cases) -- generate edge cases from function signature |
| scripts/flaky-test-analyzer.py | Mode 5 (Flaky) -- parse test logs for flaky indicators |

| Template | When to Render |
|----------|----------------|
| templates/dashboard.html | Mode 3 (Gaps) with 10+ gaps -- coverage gap visualization |

## Critical Rules

1. Never run tests -- design and analyze only. Suggest commands but do not execute.
2. Never modify source code -- test architecture is advisory, not implementation.
3. Always recommend the correct test layer (unit/integration/e2e) for each test case.
4. Edge cases must include rationale -- "why this matters" not just "try this input."
5. Coverage gaps must be prioritized by risk, not by line count.
6. Flaky test diagnosis must identify root cause category before recommending fixes.
7. Framework recommendations must match the project's existing stack.
8. Property-based testing is recommended only when invariants are identifiable.
9. Load ONE reference file at a time -- do not preload all references.
10. Every finding must cite the specific file and function it applies to.
11. Test generation must follow existing test patterns in the project when present.
12. Dashboard rendering requires 10+ gaps -- do not render for small gap sets.
