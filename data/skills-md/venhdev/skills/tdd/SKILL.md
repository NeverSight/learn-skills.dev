---
name: tdd
description: "Enforce strict Red-Green-Refactor test-driven development loop, public seam testing, and minimal implementation discipline."
disable-model-invocation: false
---

# tdd — Test-Driven Development Behavioral Protocol

## Operating Invariants

- **Public Seam Only**: Test observable behaviors strictly through public module interfaces; never assert against private helper methods or internal state variables.
- **Single Failing Assertion (RED)**: Write exactly one failing test representing the acceptance criteria before touching production code. Run the test and verify it fails with the expected assertion error, not a syntax or import error.
- **Minimal Implementation (GREEN)**: Write only the minimal production code necessary to turn the failing test green; forbid speculative features, anticipatory abstractions, or untested code branches.
- **Zero Assertion Roulette**: Assert on concrete state transitions, return payloads, or domain invariants; forbid shallow existence assertions (`expect(res).toBeDefined()`, `assert len(x) > 0`).
- **Canonical Output Contract**: *(Omitted by Design — This is a Model-Invoked Behavioral Protocol. Its output is the production code and test suite delta).*

## Domain Rubric

### 1. The Red-Green-Refactor Cycle
1. **RED**: Write a single test case capturing the concrete acceptance criteria. Execute test runner to verify RED status.
2. **GREEN**: Implement minimal logic to pass. Run test runner and typechecker to verify GREEN status.
3. **REFACTOR**: Prune redundant variables, eliminate duplicate logic, and align naming with domain language while preserving passing tests.

### 2. Invariant & Property Checks
Prefer invariant testing over shallow example tests:
- *Boundedness*: Range boundaries must hold under arbitrary input (`0 <= discount <= total`).
- *Idempotency*: Re-applying the same mutation yields the identical resulting state.
- *Round-Trip*: Serializing and deserializing a domain entity preserves deep equality.

## Smells vs. Remedies

```typescript
// Smell: Testing private internals (Couples test to implementation)
expect(service['internalCache'].has('item-123')).toBe(true);

// Remedy: Testing through public observable seam
const result = await service.fetchItem('item-123');
expect(result.id).toBe('item-123');
```

```python
# Smell: Shallow assertion roulette (Passes even if data is corrupt)
assert response.status_code == 200
assert response.json() is not None

# Remedy: Concrete invariant assertion
assert response.status_code == 200
data = response.json()
assert data["order_id"] == expected_id
assert data["status"] == "CONFIRMED"
```
