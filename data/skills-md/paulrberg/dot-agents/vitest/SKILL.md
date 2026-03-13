---
name: vitest
description: This skill should be used when the user asks to "write tests", "add tests", "test coverage", "run tests", "debug failing tests", "mock functions", or mentions Vitest, unit tests, component tests, test-driven development, or testing utilities. Provides comprehensive Vitest v4 guidance for TypeScript React/Next.js projects.
---

# Your Role

You are an expert in writing tests with Vitest v4 for TypeScript React/Next.js projects. You help users write
high-quality tests, debug failures, and maintain test suites efficiently.

**Typical setup:**

- Vitest v4 with jsdom environment
- Globals enabled (`describe`, `test`, `expect`, `vi`)
- Path aliases configured per project

# Quick Start

## Running Tests

```bash
# Run all unit tests
nlx vitest run

# Run tests matching pattern
nlx vitest run tokens

# Run specific test file
nlx vitest run src/utils/format.test.ts

# Run tests with matching name
nlx vitest run -t "adds token"

# Watch mode
nlx vitest
```

## Writing Your First Test

**File naming:** `*.test.ts` or `*.test.tsx`

**Location:** Colocate with source files

```typescript
import { describe, test, expect } from "vitest";
import { myFunction } from "./my-function";

describe("myFunction", () => {
  test("returns expected value", () => {
    expect(myFunction(5)).toBe(10);
  });
});
```

# Project-Specific Patterns

## Test Organization

Use visual separators and descriptive blocks:

```typescript
describe("TokenStore", () => {
  /* ----------------------------------------------------------------
   * Setup
   * ------------------------------------------------------------- */

  const validToken = { address: "0x123", symbol: "TEST" };

  afterEach(() => {
    // Reset state between tests
    useTokensStore.getState().clearAll();
  });

  /* ----------------------------------------------------------------
   * Adding tokens
   * ------------------------------------------------------------- */

  describe("addToken", () => {
    test("adds valid token and returns true", () => {
      const success = useTokensStore.getState().addToken(validToken);
      expect(success).toBe(true);
    });
  });
});
```

## Cleanup Pattern

Always reset state in `afterEach()`:

```typescript
import { afterEach } from "vitest";

afterEach(() => {
  // Reset mocks
  vi.clearAllMocks();

  // Reset environment
  process.env.NODE_ENV = originalEnv;

  // Reset stores
});
```

## Factory Mock Pattern

Prefer factory functions for complex mocks:

```typescript
// __mocks__/localStorage.ts
import { vi } from "vitest";

export function createLocalStorageMock() {
  const store = new Map<string, string>();

  return {
    getItem: vi.fn((key: string) => store.get(key) ?? null),
    setItem: vi.fn((key: string, value: string) => {
      store.set(key, value);
    }),
    removeItem: vi.fn((key: string) => {
      store.delete(key);
    }),
    clear: vi.fn(() => {
      store.clear();
    })
  };
}

// Usage in tests
import { createLocalStorageMock } from "./__mocks__/localStorage";

const mockStorage = createLocalStorageMock();
global.localStorage = mockStorage as Storage;
```

## Shared Setup File

Global mocks and configuration live in a setup file (e.g., `tests/setup.ts`):

```typescript
import { vi } from "vitest";

// Mock logger for all tests
vi.mock("@/utils/logger", () => ({
  createLogger: vi.fn(() => ({
    debug: vi.fn(),
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn()
  }))
}));
```

# Common Testing Scenarios

## Testing Utilities

```typescript
import { describe, test, expect, afterEach } from "vitest";
import { getEnvironment } from "./environment";

describe("getEnvironment", () => {
  const originalEnv = process.env.NODE_ENV;

  afterEach(() => {
    process.env.NODE_ENV = originalEnv;
  });

  test("returns production when NODE_ENV is production", () => {
    process.env.NODE_ENV = "production";
    expect(getEnvironment()).toBe("production");
  });

  test("returns development by default", () => {
    process.env.NODE_ENV = undefined;
    expect(getEnvironment()).toBe("development");
  });
});
```

## Async Testing

```typescript
test("async function resolves correctly", async () => {
  const result = await fetchData();
  expect(result).toEqual({ data: "value" });
});

test("async function rejects with error", async () => {
  await expect(failingFunction()).rejects.toThrow("Error message");
});
```

## Mocking Functions

```typescript
import { vi } from "vitest";

// Mock a function
const mockCallback = vi.fn((x: number) => x * 2);
mockCallback(5);
expect(mockCallback).toHaveBeenCalledWith(5);
expect(mockCallback).toHaveReturnedWith(10);

// Spy on object method
const spy = vi.spyOn(console, "log").mockImplementation(() => {});
console.log("test");
expect(spy).toHaveBeenCalledWith("test");
spy.mockRestore();
```

## Mocking Modules

```typescript
// At top level, before imports
vi.mock("./api-client", () => ({
  fetchUser: vi.fn(() => Promise.resolve({ id: 1, name: "Test" }))
}));

import { fetchUser } from "./api-client";

test("uses mocked API", async () => {
  const user = await fetchUser();
  expect(user.name).toBe("Test");
});
```

## Timer Mocking

```typescript
import { vi } from "vitest";

test("debounced function", () => {
  vi.useFakeTimers();

  const callback = vi.fn();
  const debounced = debounce(callback, 1000);

  debounced();
  debounced();
  debounced();

  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledTimes(1);

  vi.useRealTimers();
});
```

# Debugging Failed Tests

## Reading Test Output

Focus on these signals:

- **File and line number** - Where the failure occurred
- **Expected vs. received** - What went wrong
- **Stack trace** - Ignore framework internals, focus on your code

## Common Failures

**State bleeding between tests:**

```typescript
// Problem: Previous test left state
test("first test", () => {
  store.addItem("test");
});

test("second test", () => {
  expect(store.items).toHaveLength(0); // Fails! Still has "test"
});

// Solution: Add cleanup
afterEach(() => {
  store.clear();
});
```

**Mock not working:**

```typescript
// Problem: Mock path doesn't match import
vi.mock("./utils/logger");
import { logger } from "@/utils/logger"; // Different path!

// Solution: Match exact import path
vi.mock("@/utils/logger");
```

**Async timeout:**

```typescript
// Problem: Default 5s timeout too short
test("slow operation", async () => {
  await verySlowOperation(); // Times out
});

// Solution: Increase timeout
test("slow operation", async () => {
  await verySlowOperation();
}, 10000); // 10 second timeout
```

## Debugging Tools

```bash
nlx vitest --reporter=verbose   # Detailed output
nlx vitest --ui                  # Visual debugging interface
nlx vitest --coverage            # See what's tested
nlx vitest --inspect             # Node debugger
nlx vitest --run                 # Disable watch mode
```

# Best Practices

## DO

- Colocate tests with source files (`feature.ts` + `feature.test.ts`)
- Use `describe` blocks to group related tests
- Add `afterEach()` cleanup for state/mocks
- Use visual separators for clarity (`/* --- */`)
- Test behavior, not implementation
- Use explicit type annotations for mocks
- Keep tests focused and independent
- Write tests before fixing bugs (reproduce the bug first)

## DON'T

- Test implementation details (internal variables)
- Share state between tests
- Mock everything (only mock boundaries: network, storage, time)
- Forget to restore mocks/timers
- Use `any` types in tests
- Create brittle tests tied to DOM structure
- Add backward-compatibility hacks for test utilities

# Advanced Topics

For deeper dives, see the `./references/` directory:

- **`testing-patterns.md`** - Complete pattern library (component tests, complex mocking, async patterns)
- **`monorepo-testing.md`** - Workspace-specific strategies (shared vs. app tests, path aliases, organization)
- **`troubleshooting.md`** - Debug guide (common errors, performance, coverage, CI/CD)

# Coverage Analysis

To add coverage:

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: "v8",
      reporter: ["text", "html", "json"],
      exclude: ["**/*.test.ts", "**/__mocks__/**", "**/node_modules/**"]
    }
  }
});
```

Run with: `nlx vitest --coverage`

# Configuration Reference

Example config: `vitest.config.ts`

```typescript
{
  environment: "jsdom",           // React/DOM APIs available
  globals: true,                  // No imports needed for describe/test/expect
  include: ["**/*.test.{js,ts,tsx}"],
  exclude: ["**/node_modules/**", "**/e2e/**"],
  setupFiles: ["./tests/setup.ts"],
  alias: {
    "@": "./src",
    // Add your project's path aliases
  },
}
```

# Next Steps

1. **For component testing** - See `./references/testing-patterns.md` (React Testing Library setup)
3. **For monorepo-specific strategies** - See `./references/monorepo-testing.md`
4. **For debugging help** - See `./references/troubleshooting.md`

Start with simple unit tests, add component tests as needed.
