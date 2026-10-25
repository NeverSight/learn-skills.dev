---
name: testing
description: Governs automated testing discipline, unit tests, integration tests, vitest, jest, pytest, mocking boundaries, anti-flakiness, behavioral assertions, regression tests, and truthful verification.
---

# Testing Discipline Skill

Activate this skill when creating features, fixing bugs, refactoring code, or running verification test suites.

> **Testing Law:** *Untested code is broken code. Flaky tests are liabilities. Verified code has exit code 0.*

---

## 1. Targeted Test Execution Matrix

Run targeted tests for modified files to provide fast feedback, then run the full suite before concluding:

| Stack / Tool | Targeted Single-File Test Command | Full Project Test Suite Command |
| :--- | :--- | :--- |
| **Node.js (Vitest)** | `npm test -- path/to/file.test.ts` | `npm test` |
| **Node.js (Jest)** | `npx jest path/to/file.test.ts` | `npm test` |
| **Python (Pytest)** | `pytest tests/test_file.py -k "test_name"` | `pytest` |
| **Django** | `python manage.py test app.tests.TestClass` | `python manage.py test` |
| **Go** | `go test -v ./pkg/service -run TestFunctionName` | `go test ./...` |
| **Rust** | `cargo test test_name` | `cargo test` |
| **.NET C#** | `dotnet test --filter "FullyQualifiedName~TestMethod"` | `dotnet test` |
| **PHP (PHPUnit)** | `vendor/bin/phpunit tests/UserTest.php` | `vendor/bin/phpunit` |

---

## 2. The Testing Pyramid & Mocking Boundaries

```
      /\
     /  \     E2E Tests (Crucial user journeys only)
    /────\
   /      \   Integration Tests (API routes + DB queries + contracts)
  /────────\
 /          \ Unit Tests (Pure domain logic, utilities, edge cases)
/────────────\
```

### Mocking Rules
* **Mock External Boundaries Only:** Mock third-party payment gateways, email delivery, and cloud storage.
* **Do NOT Mock Pure Logic:** Never mock internal business functions or data transformers; test them with real inputs and assert exact outputs.
* **Use Deterministic Factories:** Use factories with fixed seeds; avoid random numbers (`Math.random()`) or unpinned system clocks in test assertions.

---

## 3. Non-Negotiable Testing Invariants

1. **Zero Fabrication:** Never state *"All tests passed"* without executing the test command and confirming that the process exited with code 0.
2. **Regression Assertion for Bugfixes:** Every bug fix must include an automated regression test reproducing the original bug condition and asserting its resolution.
3. **Clean Teardown:** Ensure tests clean up temporary files, mock servers, and database records to prevent cross-test pollution.

---

## 4. Testing Execution Workflow & Mocking Contrasts

### Step-by-Step Testing Protocol
1. **Runner Discovery:** Identify the project test runner from `package.json` or stack manifests (`vitest`, `jest`, `pytest`, `go test`).
2. **Reproduction / Contract Test:** Before fixing a bug, create a minimal test case asserting the failing condition. Before adding a feature, write tests defining the acceptance criteria.
3. **Targeted Execution:** Run the test targeting only the modified test file (`npm test -- path/to/spec.test.ts`).
4. **Full Verification:** Run the full project test suite (`npm test`) and confirm exit code 0 before concluding.

### Mocking Contrast Matrix
```ts
// ❌ WRONG: Mocking internal pure business functions (tests nothing meaningful)
vi.spyOn(userService, 'calculateDiscount').mockReturnValue(10);
// Tests become brittle and assert implementation details rather than real behavior!
```
```ts
// ✅ CORRECT: Test pure logic with real inputs, mock ONLY external I/O
// Test pure logic directly:
expect(calculateDiscount({ userTier: 'GOLD', cartTotal: 100 })).toBe(10);

// Mock external network/payment gateway only:
vi.spyOn(stripeClient.charges, 'create').mockResolvedValue({ id: 'ch_test123', status: 'succeeded' });
```

---

## 5. Anti-Flakiness Invariants & Behavioral Test Standards

### A. Zero Arbitrary Sleeps / Hardcoded Delays
* **Flaky Anti-Pattern:**
  ```ts
  // ❌ BRITTLE: Hardcoded sleep fails on busy CI runners and wastes seconds locally
  await new Promise((r) => setTimeout(r, 1000));
  expect(queryStatus()).toBe('COMPLETED');
  ```
* **Robust Standard (Deterministic Polling):**
  ```ts
  // ✅ ROBUST: Resolves as soon as the condition is satisfied
  await vi.waitFor(() => {
    expect(queryStatus()).toBe('COMPLETED');
  }, { timeout: 2000, interval: 50 });
  ```

### B. Test User-Visible Behavior, Not Implementation Details
* **Brittle Anti-Pattern:** Querying by internal CSS classes (`container.querySelector('.btn-primary-blue-400')`) or inspecting private component state.
* **Robust Standard:** Query by accessible ARIA roles, labels, or test IDs:
  ```ts
  // ✅ ROBUST: Resilient to CSS refactors and verifies real accessibility
  const submitBtn = screen.getByRole('button', { name: /save changes/i });
  expect(submitBtn).toBeEnabled();
  ```

### C. Deterministic Time & Clocks
* Never write tests that depend on the current real-world clock (`new Date()`).
* Use fake timers (`vi.useFakeTimers()`, `vi.setSystemTime(new Date('2026-01-01'))`) for time-dependent operations.

---

## 6. Pre-Commit Testing Checklist

Before marking any task complete:
* [ ] **Targeted Verification:** Executed targeted test command for the modified file with exit code 0.
* [ ] **Full Suite Verification:** Executed `npm test` (or ecosystem equivalent) with exit code 0.
* [ ] **Zero Arbitrary Sleeps:** Verified tests use `waitFor()` instead of `setTimeout()`.
* [ ] **Behavioral Assertions:** Asserted public contracts or accessible roles, not private methods or CSS classes.
* [ ] **Clean State Isolation:** Verified tests do not leak database records or global mocks.
