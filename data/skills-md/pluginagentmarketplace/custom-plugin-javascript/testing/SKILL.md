---
name: testing
description: JavaScript testing with Jest, Vitest, and Testing Library for comprehensive test coverage.
sasmp_version: "1.3.0"
bonded_agent: 08-javascript-testing-quality
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [framework]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_vitest_basics

observability:
  entry_log: "Testing skill activated"
  exit_log: "Testing reference provided"
---

# JavaScript Testing Skill

## Quick Reference Card

### Vitest/Jest Basics
```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('Calculator', () => {
  it('adds numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('handles edge cases', () => {
    expect(add(0, 0)).toBe(0);
    expect(add(-1, 1)).toBe(0);
  });
});
```

### Common Matchers
```javascript
// Equality
expect(value).toBe(exact);
expect(value).toEqual(deepEqual);
expect(value).toStrictEqual(strictDeep);

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeDefined();

// Numbers
expect(num).toBeGreaterThan(3);
expect(num).toBeLessThanOrEqual(10);
expect(float).toBeCloseTo(0.3, 5);

// Strings
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');

// Arrays
expect(arr).toContain(item);
expect(arr).toHaveLength(3);

// Errors
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('message');
```

### Mocking
```javascript
// Mock function
const mockFn = vi.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue(data);
mockFn.mockRejectedValue(error);

// Verify calls
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith(arg);
expect(mockFn).toHaveBeenCalledTimes(2);

// Mock module
vi.mock('./api', () => ({
  fetchData: vi.fn().mockResolvedValue({ data: [] })
}));

// Spy
const spy = vi.spyOn(obj, 'method');
```

### Async Testing
```javascript
it('handles async', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

it('handles promises', async () => {
  await expect(fetchData()).resolves.toEqual({ id: 1 });
  await expect(failingFn()).rejects.toThrow('Error');
});
```

### React Testing Library
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('renders and interacts', async () => {
  render(<Button onClick={handleClick}>Click me</Button>);

  // Query
  const btn = screen.getByRole('button', { name: /click/i });
  expect(btn).toBeInTheDocument();

  // Interact
  await userEvent.click(btn);
  expect(handleClick).toHaveBeenCalled();
});
```

### Test Setup
```javascript
// vitest.config.ts
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      thresholds: { lines: 80 }
    }
  }
});
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Test timeout | Hangs | Check async/await |
| Mock not working | Real fn called | Verify mock setup |
| Flaky test | Random failures | Add waits, fix race |
| Coverage low | Under threshold | Add edge cases |

### Debug Checklist
```javascript
// 1. Isolate test
it.only('specific test', () => {});

// 2. Log state
console.log('Value:', variable);

// 3. Debug DOM
screen.debug();

// 4. Check mocks
console.log(mockFn.mock.calls);
```

## Production Patterns

### Test Organization
```javascript
describe('UserService', () => {
  describe('create', () => {
    it('creates user with valid data', () => {});
    it('throws on invalid email', () => {});
  });

  describe('delete', () => {
    it('removes existing user', () => {});
    it('throws if not found', () => {});
  });
});
```

### Test Factories
```javascript
function createUser(overrides = {}) {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@test.com',
    ...overrides
  };
}
```

## Related

- **Agent 08**: Testing & Quality (detailed learning)
- **Skill: debugging**: Debug techniques
- **Skill: ecosystem**: CI setup
