---
name: barrier-concurrency-testing
description: Deterministic race condition testing using barriers and deferred promises. Replaces flaky setTimeout-based timing tests with reproducible interleaving control.
---

# Barrier Concurrency Testing

Deterministic race condition testing -- no flaky timing-based tests.

Instead of `setTimeout` (flaky) or `sleep` (slow), use **barriers** to pause execution at exact interleave points. The test controls when each concurrent operation proceeds, making race condition tests deterministic and reproducible on every run.

**When to use**: Testing concurrent operations, flush conflicts, parallel mutations, race windows between read and write, lock contention scenarios, any code where timing affects correctness.

**When not to use**: Sequential-only code, simple unit tests, UI components, read-only operations, code with no concurrency concerns.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "setTimeout is good enough" | Timing-based tests are inherently flaky -- they pass 99 times, fail on CI | Use barriers for deterministic control |
| "It passed 10 times, it's fine" | Heisenbugs hide in timing windows that haven't been hit yet | Barrier at every interleave point |
| "We don't have race conditions" | Any concurrent code has race windows | Write a barrier test to prove it |
| "Barriers are too complex" | 15 lines of setup prevents hours of debugging flaky failures | Copy the pattern from references |

---

## Included Utilities

```typescript
// Barrier infrastructure + invariant assertions + test data generators
import {
  createBarrier,
  createTrackedBarrier,
  releaseAllBarriers,
  assertPreservesConcurrentItems,
  assertPreservesOnFailure,
  assertSequenceContinuity,
  assertLastSequenceCorrect,
  assertRetryCountReset,
  createTestItems,
} from './test-fixtures.ts';
```

## Violation Rules

### inadequate_barrier_coverage
Race conditions MUST have barrier tests at each interleave point. If there are N interleave points in the code, there must be N barrier test cases.
**Severity**: must-fail

### flaky_timing_test
NEVER use `setTimeout`, `sleep`, or arbitrary delays for concurrency testing. Use barriers for deterministic control.
**Severity**: must-fail

---

## Quick Reference

| Scenario | Pattern | Example |
|----------|---------|---------|
| Block before transaction | `barrier.wait()` in transaction start | Verify concurrent writes preserved |
| Block during I/O | `deferred.promise` as mock return | Verify queue depth during processing |
| Multiple interleave points | Multiple barriers, release in sequence | Test all orderings of concurrent ops |
| Cleanup | `afterEach(() => releaseAllBarriers())` | Prevent test hangs |

See [patterns.md](./references/patterns.md) for full code examples, deferred promise alternative, and framework adaptation guide.
