---
name: fault-injection-testing
description: Simulates storage and network failures for resilience testing. Provides circuit breaker state machine, retry policies with backoff, and queue preservation assertions.
---

# Fault Injection Testing

Test failure paths, not just happy paths.

Production systems fail. Databases time out. Networks reset. Services degrade. If you only test happy paths, your first encounter with failure will be in production. This skill teaches you to systematically inject faults and verify resilience behavior.

**When to use**: Testing recovery paths, retry logic, circuit breakers, transaction rollback, queue preservation on failure, any code that interacts with external services.

**When not to use**: Happy-path-only tests, pure functions, UI components, code with no external dependencies.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "The happy path works" | Production failures aren't happy | Test each fault scenario explicitly |
| "Retry logic is simple" | Exponential backoff has edge cases | Verify delay calculations mathematically |
| "Circuit breakers are overkill" | Cascading failures take down systems | Implement and test all 3 states |
| "Queue data is safe" | Transient failures can lose queue items | Assert queue preservation on every failure |

---

## What To Protect (Start Here)

Before generating fault tests, identify which resilience decisions apply to your code:

| Decision | Question to Answer | If Yes → Use |
|----------|--------------------|--------------|
| Service degradation must not cascade | Does this code call an external service that other callers also depend on? | `CircuitBreaker` |
| Retries must not overwhelm the target | Can multiple clients retry simultaneously after an outage? | `RetryPolicy` with jitter |
| Failed operations must not lose queued work | Is there a queue or buffer that persists across retries? | `assertQueuePreserved` |
| Faults must be tested at boundaries, not inside logic | Where does your code cross a system boundary (DB, network, external API)? | `createFaultInjector` |

**Do not generate tests for decisions the human hasn't confirmed.** A circuit breaker test that verifies state transitions without connecting to a real failure scenario (cascading outage, thundering herd) is testing the mechanism, not the decision.

---

## Included Utilities

```typescript
import {
  createFaultScenario,
  CircuitBreaker,
  RetryPolicy,
  createFaultInjector,
  assertQueuePreserved,
  assertQueueTrimmed,
} from './fault-injection.ts';
```

## Core Workflow

### Step 1: Define Fault Scenarios

List all failure modes for your external dependencies:

```typescript
const faultScenarios = [
  createFaultScenario('timeout', 'ETIMEDOUT', 'retry_scheduled'),
  createFaultScenario('connection_reset', 'ECONNRESET', 'circuit_half_open'),
  createFaultScenario('rate_limited', '429', 'backoff_extended'),
  createFaultScenario('partial_write', 'SQLITE_CONSTRAINT', 'idempotent_retry'),
];
```

### Step 2: Implement Circuit Breaker

Circuit breakers prevent cascading failures by failing fast when a service is down:

```typescript
const cb = new CircuitBreaker({
  failureThreshold: 3,    // Open after 3 failures
  resetTimeout: 30000,    // Try half-open after 30s
  successThreshold: 2,    // Require 2 successes to close
}, Date.now);

// Usage
if (!cb.canExecute()) {
  throw new Error('Circuit open - service unavailable');
}

try {
  await callExternalService();
  cb.recordSuccess();
} catch (err) {
  cb.recordFailure();
  throw err;
}
```

### Step 3: Test Circuit Breaker State Machine

The circuit breaker is a state machine: closed → open → half-open → closed. Test all transitions:

```typescript
describe('circuit breaker', () => {
  it('starts closed', () => {
    const cb = new CircuitBreaker({ failureThreshold: 3, resetTimeout: 1000 });
    assert.equal(cb.getState(), 'closed');
  });

  it('opens after failure threshold', () => {
    const cb = new CircuitBreaker({ failureThreshold: 3, resetTimeout: 1000 });
    cb.recordFailure();
    cb.recordFailure();
    cb.recordFailure();
    assert.equal(cb.getState(), 'open');
  });

  // Use fake clock (inject nowFn) — no setTimeout, no flake
  it('transitions to half-open after timeout', () => {
    let now = 0;
    const cb = new CircuitBreaker({ failureThreshold: 1, resetTimeout: 50 }, () => now);
    cb.recordFailure();
    now = 60;
    assert.equal(cb.getState(), 'half-open');
  });

  it('closes on success in half-open', () => {
    let now = 0;
    const cb = new CircuitBreaker({ failureThreshold: 1, resetTimeout: 10 }, () => now);
    cb.recordFailure();
    now = 20;
    cb.recordSuccess();
    assert.equal(cb.getState(), 'closed');
  });

  it('reopens on failure in half-open', () => {
    let now = 0;
    const cb = new CircuitBreaker({ failureThreshold: 1, resetTimeout: 10 }, () => now);
    cb.recordFailure();
    now = 20;
    cb.recordFailure();
    assert.equal(cb.getState(), 'open');
  });
});
```

### Step 4: Implement Retry Policy with Backoff

Exponential backoff with jitter prevents thundering herd:

```typescript
const policy = new RetryPolicy({
  maxRetries: 5,
  baseDelay: 100,
  maxDelay: 30000,     // Hard cap: final jittered delay never exceeds this
  jitterFactor: 0.1,  // ±10% randomization
}, Math.random);

// Get delay for attempt N (0-indexed)
const delay = policy.getDelay(2);  // ~400ms ± jitter
```

Inject deterministic RNG for stable tests:

```typescript
const low = new RetryPolicy({ maxRetries: 3, baseDelay: 1000, jitterFactor: 0.1 }, () => 0);
const high = new RetryPolicy({ maxRetries: 3, baseDelay: 1000, jitterFactor: 0.1 }, () => 1);
```

`RetryPolicy` and `CircuitBreaker` validate numeric config and throw on invalid values (negative delays, non-integer thresholds/retry counts, jitter outside `[0, 1]`).

### Step 5: Test Backoff Calculations

Verify mathematical correctness of backoff:

```typescript
describe('retry policy', () => {
  it('doubles delay each attempt', () => {
    const policy = new RetryPolicy({ maxRetries: 5, baseDelay: 100 });
    assert.equal(policy.getDelayWithoutJitter(0), 100);
    assert.equal(policy.getDelayWithoutJitter(1), 200);
    assert.equal(policy.getDelayWithoutJitter(2), 400);
    assert.equal(policy.getDelayWithoutJitter(3), 800);
  });

  it('caps at maxDelay', () => {
    const policy = new RetryPolicy({ maxRetries: 10, baseDelay: 100, maxDelay: 500 });
    assert.equal(policy.getDelayWithoutJitter(10), 500);
  });

  it('jitter stays within bounds', () => {
    const policy = new RetryPolicy({ maxRetries: 5, baseDelay: 1000, jitterFactor: 0.1 });
    for (let i = 0; i < 20; i++) {
      const delay = policy.getDelay(0);
      assert.ok(delay >= 900 && delay <= 1100);
    }
  });
});
```

### Step 6: Inject Faults at Boundaries

Use `createFaultInjector` to wrap functions with controlled failure triggers:

```typescript
const realDbWrite = async (data) => { /* ... */ };

const faultMap = {
  timeout: new Error('ETIMEDOUT'),
  constraint: new Error('SQLITE_CONSTRAINT'),
  reset: new Error('ECONNRESET'),
};

const dbWrite = createFaultInjector(realDbWrite, faultMap);

// In tests
await dbWrite(null, data);       // Normal execution
await dbWrite('timeout', data);  // Throws ETIMEDOUT (synchronously)
```

> **Note**: `createFaultInjector` throws synchronously even when wrapping async functions. This is intentional — fault injection simulates failures at the call boundary, not inside the async pipeline. Use `assert.throws()`, not `assert.rejects()`.

### Step 7: Assert Queue Preservation

Transient failures must NOT lose queued data:

```typescript
it('preserves queue on transient failure', async () => {
  const queueBefore = [{ sequenceNumber: 1 }, { sequenceNumber: 2 }];

  // Simulate failure during processing
  try {
    await processWithFault(queueBefore, 'timeout');
  } catch {}

  const queueAfter = getQueue();
  assertQueuePreserved(queueBefore, queueAfter);
});

it('trims queue after successful processing', async () => {
  const queueBefore = [{ sequenceNumber: 1 }, { sequenceNumber: 2 }, { sequenceNumber: 3 }];

  await processSuccessfully(queueBefore, /* maxSeq */ 2);

  const queueAfter = getQueue();
  assertQueueTrimmed(queueAfter, 2);  // Only seq 3 should remain
});
```

---

## Violation Rules

### missing_circuit_breaker_test
Circuit breakers MUST have tests for all 3 state transitions: closed→open, open→half-open, half-open→closed/open.
**Severity**: must-fail

### missing_backoff_verification
Retry policies MUST verify exponential calculation, max delay cap, and jitter bounds.
**Severity**: must-fail

### missing_queue_preservation_test
Operations that can fail MUST have tests verifying no data loss on transient failure.
**Severity**: must-fail

### fault_injection_inside_unit
Fault injection should only happen at system BOUNDARIES (database, network, external services), not inside business logic.
**Severity**: should-fail

---

## Companion Skills

This skill provides **testing utilities** for resilience patterns, not resilience architecture guidance. For broader methodology:

- Search `resilience` on [skills.sh](https://skills.sh) for bulkhead isolation, health checks, graceful degradation
- The circuit breaker is a state machine — use [model-based-testing](https://github.com/apankov1/quality-engineering/tree/main/skills/model-based-testing) for systematic transition matrix coverage

---

## Quick Reference

| Component | States/Behavior | Key Tests |
|-----------|-----------------|-----------|
| Circuit Breaker | closed → open → half-open → closed | All 4 transitions, threshold counts, timeout timing |
| Retry Policy | Exponential backoff with cap | Delay doubling, max cap, jitter bounds |
| Fault Injector | Named faults → specific errors | Each fault triggers correct error |
| Queue Preservation | No data loss on failure | Before/after sequence comparison |

See [patterns.md](./references/patterns.md) for failure matrix methodology, boundary-only injection rules, and integration with real infrastructure.
