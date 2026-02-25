---
name: pairwise-test-coverage
description: "Combinatorial testing with a greedy pairwise matrix generator. Covers all factor pairs in near-minimal test cases."
---

# Pairwise Test Coverage

Combinatorial testing that covers all factor pairs in near-minimal test cases.

**When to use**: Multi-factor systems where exhaustive testing is impractical, state machines, retry/recovery logic, configuration matrices, compatibility testing, any code with 3+ interacting parameters.

**When not to use**: Single-factor tests (just test each value), two-factor systems (test all combinations directly), UI snapshot tests, type-only changes.

## Core Philosophy

**Exhaustive testing doesn't scale.** If a system has 4 factors with 3 values each, that's 81 test cases. Pairwise testing covers all pair interactions in ~12 cases -- an 85% reduction with near-complete defect detection.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "We'll test the important combinations" | Unexpected factor interactions go untested without systematic coverage | Generate the pairwise matrix |
| "81 test cases is fine" | 81 cases means 81 things to maintain and debug when they fail | Use pairwise to get 12 |
| "The test passes, so the code works" | Test must FAIL before the fix to prove it catches the bug | Validate detection first |

---

## Quick Reference

| Technique | Use When | Key Pattern |
|-----------|----------|-------------|
| **Pairwise Matrix** | Multiple factors with discrete values | `it.each(cases)` table-driven |
| **Property-Based** | Value ranges, type safety invariants | `fc.assert(fc.property(...))` |
| **Model-Based** | State machine transitions | Transition table tests |
| **Fault Injection** | Storage/network failures | Mock rejection scenarios |
| **Contract Tests** | Schema validation at boundaries | `Schema.safeParse()` assertions |

## Included Utilities

```typescript
// Pairwise matrix generator (zero dependencies)
import { generatePairwiseMatrix, formatAsMarkdownTable } from './pairwise.ts';

// Pairwise test case helpers
import { createPairwiseTestCases, generateTestCaseName } from './test-fixtures.ts';
```

## Performance and Limits

The greedy algorithm never enumerates the Cartesian product. Pair count grows as O(factors² × values²).

| Factors | Values | Cartesian | Pairwise Cases | Time |
|---------|--------|-----------|----------------|------|
| 3 | 3 | 27 | ~10 | <1ms |
| 8 | 4 | 65,536 | ~46 | ~2ms |
| 8 | 8 | 16,777,216 | ~100 | ~10ms |

**Hard limits** (throws if exceeded): max 20 factors, max 50 values per factor. Beyond these, pair count exceeds ~475K (C(20,2) × 50²) and in-memory generation becomes impractical.

## Violation Rules

| Slug | Rule | Severity |
|------|------|----------|
| `missing_pairwise_coverage` | Multi-factor code changes need pairwise tests | must-fail |
| `bug_detection_not_validated` | Tests must fail before fix, pass after | must-fail |

## Definition of Done

- [ ] Factors documented in test file header
- [ ] Pairwise matrix as `it.each` test cases
- [ ] Tests fail before fix, pass after

## Details

See references for:
- **workflow.md**: Step-by-step implementation guide
- **violations.md**: Full violation rules with detection patterns
- **examples.md**: 6 testing technique examples (pairwise, property-based, model-based, fault injection, contract, observability)
