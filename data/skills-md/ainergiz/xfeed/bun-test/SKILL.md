---
name: bun-test
description: Write and debug Bun tests with proper mocking, coverage, and isolation. Use when writing tests, debugging test failures, setting up test infrastructure, mocking fetch/modules, or improving test coverage.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Bun Test Guide

## Quick Start

```typescript
import { describe, expect, it, mock, spyOn, beforeEach, afterEach, afterAll } from "bun:test";

describe("MyModule", () => {
  it("does something", () => {
    expect(1 + 1).toBe(2);
  });
});
```

Run tests:
```bash
bun test                    # Run all tests
bun test --watch            # Watch mode
bun test --coverage         # With coverage report
bun test src/api            # Specific directory
bun test --test-name-pattern "pattern"  # Filter by name
```

## Mocking Patterns

### Mock Functions

```typescript
const mockFn = mock(() => "mocked value");
mockFn();
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(1);

// Reset between tests
mockFn.mockReset();
mockFn.mockImplementation(() => "new value");
```

### Spy on Object Methods

```typescript
import { myModule } from "./my-module";

let methodSpy: Mock<typeof myModule.method>;

beforeAll(() => {
  methodSpy = spyOn(myModule, "method").mockImplementation(() => "mocked");
});

afterAll(() => {
  methodSpy.mockRestore(); // IMPORTANT: Always restore spies
});
```

### Mock fetch (globalThis.fetch)

Bun's `fetch` has extra properties (like `preconnect`) that mocks don't have. Use `// @ts-nocheck` at file top for test files with fetch mocking:

```typescript
// @ts-nocheck - Test file with fetch mocking
import { afterEach, beforeEach, describe, expect, it, mock } from "bun:test";

const originalFetch = globalThis.fetch;

// Helper for mock responses
function mockResponse(body: unknown, options: { status?: number; ok?: boolean } = {}) {
  const status = options.status ?? 200;
  const ok = options.ok ?? (status >= 200 && status < 300);
  return {
    ok,
    status,
    text: () => Promise.resolve(typeof body === "string" ? body : JSON.stringify(body)),
    json: () => Promise.resolve(body),
  } as Response;
}

describe("API", () => {
  afterEach(() => {
    globalThis.fetch = originalFetch; // Always restore
  });

  it("fetches data", async () => {
    globalThis.fetch = mock(() => Promise.resolve(mockResponse({ data: "test" })));

    const result = await myApi.getData();
    expect(result).toEqual({ data: "test" });
  });

  it("handles errors", async () => {
    globalThis.fetch = mock(() => Promise.reject(new Error("Network error")));

    await expect(myApi.getData()).rejects.toThrow("Network error");
  });
});
```

### Mock Modules (External Dependencies)

Use `mock.module()` BEFORE importing the module under test:

```typescript
// @ts-nocheck - Test file with module mocking
import { describe, expect, it, mock } from "bun:test";

// Create mutable mock implementation
let mockImpl = () => Promise.resolve({ data: "default" });

// Mock the module BEFORE importing
mock.module("external-package", () => ({
  someFunction: () => mockImpl(),
}));

// NOW import the module that uses external-package
const { myFunction } = await import("./my-module");

// Helper to change mock behavior per test
function setMockReturn(value: unknown) {
  mockImpl = () => Promise.resolve(value);
}

describe("MyModule", () => {
  it("uses external package", async () => {
    setMockReturn({ data: "test" });
    const result = await myFunction();
    expect(result.data).toBe("test");
  });
});
```

## Test Isolation

### State Sharing Warning

Tests within a file share module-level state. Use setup/teardown hooks carefully:

```typescript
// Store original values at module level
const originalEnv = process.env.NODE_ENV;
const originalFetch = globalThis.fetch;

afterAll(() => {
  // Restore everything
  globalThis.fetch = originalFetch;
  if (originalEnv !== undefined) {
    process.env.NODE_ENV = originalEnv;
  } else {
    delete process.env.NODE_ENV;
  }
});
```

### Temp Directory Isolation

Use `mkdtemp()` per test, not a shared temp directory:

```typescript
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";

let testDir: string;

beforeEach(async () => {
  // Unique temp dir per test - avoids race conditions
  testDir = await mkdtemp(path.join(tmpdir(), "my-test-"));
});

afterEach(async () => {
  if (testDir) {
    await rm(testDir, { recursive: true, force: true }).catch(() => {});
  }
});
```

## Coverage

```bash
bun test --coverage              # Generate text report
bun test --coverage-reporter lcov # For CI/tooling integration
```

### Coverage Quirks

1. **Closing braces after return** may show uncovered even when executed
2. **Function declarations** may not count if only body runs
3. **100% may be impossible** - aim for 99%+ on meaningful code

### Improving Coverage

- Test all branches (if/else, switch cases)
- Test error paths and edge cases
- Test with different input types
- Don't obsess over unreachable code (closing braces, etc.)

## Common Patterns

### Async Tests

```typescript
it("handles async", async () => {
  const result = await asyncFunction();
  expect(result).toBe("expected");
});

it("expects rejection", async () => {
  await expect(asyncFunction()).rejects.toThrow("error message");
});
```

### Parameterized Tests

```typescript
const testCases = [
  { input: 1, expected: 2 },
  { input: 2, expected: 4 },
];

for (const { input, expected } of testCases) {
  it(`doubles ${input} to ${expected}`, () => {
    expect(double(input)).toBe(expected);
  });
}
```

### Testing Timeouts

```typescript
it("handles timeout", async () => {
  // Use small delays for tests
  const result = await functionWithDelay(1); // 1ms instead of 1000ms
  expect(result).toBeDefined();
});
```

## Checklist for New Test Files

1. Add `// @ts-nocheck` if mocking fetch or complex types
2. Store original values (fetch, env vars) before modifying
3. Restore everything in `afterEach` or `afterAll`
4. Use `mkdtemp()` for temp directories (not shared paths)
5. Call `mockRestore()` on spies in `afterAll`
6. Use descriptive test names that explain the scenario

## Debugging Tests

```bash
bun test --bail                  # Stop on first failure
bun test --timeout 30000         # Increase timeout (ms)
bun test --test-name-pattern "specific test"  # Run one test
```

Add console.log for debugging (remove before committing):
```typescript
it("debugging", () => {
  console.log("Value:", someValue);
  expect(someValue).toBeDefined();
});
```

## Additional Resources

For xfeed-specific patterns (XClient, RuntimeQueryIdStore, cookie mocking, GraphQL responses), see [PATTERNS.md](PATTERNS.md).
