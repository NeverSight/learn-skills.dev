---
name: tdd
description: "LOAD THIS SKILL when: implementing new features with TDD, user mentions 'TDD', 'test-first', 'red-green-refactor', 'failing test', or when building Effect services that need thorough testing. Covers TDD methodology, Red-Green-Refactor cycle, Effect service testing with mock layers, and test-first development workflow."
---

# Test-Driven Development (TDD)

## Philosophy

TDD is a development methodology where you write tests BEFORE implementation. This ensures:

- **Clear requirements** - Tests define expected behavior upfront
- **Better design** - Forces you to think about interfaces first
- **Confidence** - Every feature has test coverage from day one
- **Refactoring safety** - Tests catch regressions immediately

## When to Use TDD

| Situation                   | Use TDD? | Reason                                       |
| --------------------------- | -------- | -------------------------------------------- |
| New utility function        | **YES**  | Pure functions are perfect for TDD           |
| New Effect service          | **YES**  | Define interface via tests first             |
| Complex business logic      | **YES**  | Tests clarify requirements                   |
| Bug fix                     | **YES**  | Write failing test that reproduces bug first |
| UI component styling        | No       | Visual changes don't benefit from TDD        |
| Exploratory prototyping     | No       | Requirements unclear, iterate first          |
| TRPC endpoint (simple CRUD) | Optional | Ask user preference                          |

---

## Red-Green-Refactor Cycle

The TDD workflow follows three phases:

### 1. RED - Write Failing Test First

```typescript
import { describe, expect, it } from "vitest";
import { calculateDiscount } from "../calculate-discount";

describe("calculateDiscount", () => {
  it("applies 10% discount for orders over 100", () => {
    // This test will FAIL - function doesn't exist yet
    expect(calculateDiscount(150)).toBe(135);
  });
});
```

**Run test to see it fail:**

```bash
bun run vitest run packages/common/src/__tests__/calculate-discount.test.ts
```

### 2. GREEN - Minimal Implementation

Write the **minimum code** to make the test pass:

```typescript
// packages/common/src/calculate-discount.ts
export function calculateDiscount(amount: number): number {
  if (amount > 100) {
    return amount * 0.9;
  }
  return amount;
}
```

**Run test to see it pass:**

```bash
bun run vitest run packages/common/src/__tests__/calculate-discount.test.ts
```

### 3. REFACTOR - Improve Without Breaking

Improve code quality while keeping tests green:

```typescript
const DISCOUNT_THRESHOLD = 100;
const DISCOUNT_RATE = 0.1;

export function calculateDiscount(amount: number): number {
  if (amount <= DISCOUNT_THRESHOLD) {
    return amount;
  }
  return amount * (1 - DISCOUNT_RATE);
}
```

**Run tests again to verify refactoring didn't break anything.**

See `references/red-green-refactor.md` for detailed workflow examples.

---

## Test Hierarchy (Prefer Simpler)

1. **Unit tests** (preferred) - Pure functions, Effect services with mock layers
2. **TRPC Integration** (ask first) - Full TRPC stack with PGlite
3. **E2E** (ask + justify) - Browser automation, slowest

| Situation                        | Test Type             | Action                       |
| -------------------------------- | --------------------- | ---------------------------- |
| Pure function, parser, util      | Unit                  | Write immediately            |
| Effect service with dependencies | Unit with mock layers | Write immediately            |
| TRPC procedure (DB logic)        | TRPC Integration      | Ask user first               |
| User-facing flow, UI behavior    | E2E                   | Ask + warn about maintenance |

---

## Effect TDD Patterns

### Test-First Service Design

1. **Define interface via test** - What should the service do?
2. **Create mock layer** - Isolate dependencies
3. **Implement service** - Make tests pass
4. **Refactor** - Improve with confidence

```typescript
import { describe, expect, it } from "@effect/vitest";
import { Effect, Layer } from "effect";

describe("PricingService", () => {
  // 1. Define what the service should do via tests
  it.effect("calculates base price without discount", () =>
    Effect.gen(function* () {
      const service = yield* PricingService;
      const result = yield* service.calculatePrice({
        itemId: "item-1",
        quantity: 2,
      });
      expect(result.total).toBe(200);
    }).pipe(Effect.provide(testLayer)),
  );

  it.effect("applies bulk discount for quantity > 10", () =>
    Effect.gen(function* () {
      const service = yield* PricingService;
      const result = yield* service.calculatePrice({
        itemId: "item-1",
        quantity: 15,
      });
      expect(result.total).toBe(1350); // 15% discount
    }).pipe(Effect.provide(testLayer)),
  );
});
```

### Mock Layer Factory Pattern

```typescript
// Create parameterized mock layers for different test scenarios
const createMockInventoryLayer = (inventory: Map<string, number>) =>
  Layer.succeed(InventoryService, {
    getStock: (itemId) => Effect.succeed(inventory.get(itemId) ?? 0),
    reserveStock: (itemId, qty) => Effect.succeed(void 0),
  });

// Use in tests
const testLayer = PricingService.layer.pipe(
  Layer.provide(createMockInventoryLayer(new Map([["item-1", 100]]))),
);
```

See `references/effect-tdd-patterns.md` for comprehensive Effect testing patterns.

---

## Test File Locations

| Code Location                                       | Test Location                           |
| --------------------------------------------------- | --------------------------------------- |
| `packages/X/src/file.ts`                            | `packages/X/src/__tests__/file.test.ts` |
| `apps/web-app/src/infrastructure/trpc/routers/X.ts` | `apps/web-app/src/__tests__/X.test.ts`  |
| `apps/web-app/src/routes/**`                        | `apps/web-app/e2e/feature.e2e.ts`       |

---

## Commands

### Unit & Integration Tests

```bash
# Run all tests (unit + TRPC integration)
bun run test

# Watch mode - re-run on file changes
bun run test:watch

# Run with coverage report
bun run test:coverage

# Run specific test file (FROM PROJECT ROOT, full path required)
bun run vitest run packages/common/src/__tests__/pagination.test.ts
bun run vitest run apps/web-app/src/__tests__/formatters.test.ts

# Run tests matching pattern
bun run vitest run -t "calculateDiscount"
```

### E2E Tests

```bash
# Install Playwright browsers (first time only)
bun run test:e2e:install

# Run all E2E tests
bun run test:e2e

# Run E2E with interactive UI
bun run test:e2e:ui
```

### WRONG Syntax (DO NOT USE)

```bash
# These DO NOT work:
bun run test packages/common/src/__tests__/file.test.ts  # script doesn't accept path
cd packages/common && bun run vitest run src/__tests__/file.test.ts  # wrong cwd
```

---

## TDD Anti-Patterns

### 1. Writing Implementation First

```typescript
// ❌ BAD - Implementation before test
export function formatPrice(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

// Then writing test after - defeats TDD purpose
```

### 2. Skipping the RED Phase

```typescript
// ❌ BAD - Test passes immediately (you didn't verify it can fail)
it("returns true", () => {
  expect(true).toBe(true); // This always passes!
});
```

### 3. Too Many Tests at Once

```typescript
// ❌ BAD - Writing all tests before any implementation
describe("UserService", () => {
  it("creates user", () => {
    /* ... */
  });
  it("updates user", () => {
    /* ... */
  });
  it("deletes user", () => {
    /* ... */
  });
  it("lists users", () => {
    /* ... */
  });
  it("validates email", () => {
    /* ... */
  });
  // 10 more tests...
});
// Now you have 15 failing tests - overwhelming!
```

**Correct approach**: One test at a time. RED → GREEN → REFACTOR → next test.

### 4. Skipping Refactor Phase

```typescript
// ❌ BAD - Test passes, move on without cleanup
export function calc(a: number, b: number, c: string): number {
  if (c === "add") return a + b;
  if (c === "sub") return a - b;
  if (c === "mul") return a * b;
  return 0;
}

// ✅ GOOD - Refactor to cleaner design
type Operation = "add" | "subtract" | "multiply";

const operations: Record<Operation, (a: number, b: number) => number> = {
  add: (a, b) => a + b,
  subtract: (a, b) => a - b,
  multiply: (a, b) => a * b,
};

export function calculate(a: number, b: number, op: Operation): number {
  return operations[op](a, b);
}
```

---

## Resources

### references/

- `red-green-refactor.md` - Detailed TDD cycle workflow with examples
- `effect-tdd-patterns.md` - Effect service testing, mock layers, error cases
- `test-first-examples.md` - Step-by-step TDD examples for this codebase

### Related Skills

- `testing-patterns` - Test syntax, TRPC integration tests, E2E patterns
- `effect-ts` - Effect service design, layers, error handling
