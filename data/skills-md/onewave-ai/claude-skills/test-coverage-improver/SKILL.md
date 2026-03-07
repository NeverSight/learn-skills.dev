---
name: test-coverage-improver
description: Analyze test coverage gaps and generate tests to improve coverage. Use when improving test coverage, finding untested code, or writing missing tests.
---

# Test Coverage Improver

## Instructions

When improving test coverage:

1. **Run coverage report** to identify gaps
2. **Prioritize** critical/complex code paths
3. **Write tests** for uncovered code
4. **Verify coverage improved**

## Generate Coverage Report

```bash
# Jest
npx jest --coverage

# Vitest
npx vitest --coverage

# NYC (Istanbul) for any test runner
npx nyc npm test

# View HTML report
open coverage/lcov-report/index.html
```

## Coverage Targets

| Type | Minimum | Good | Excellent |
|------|---------|------|-----------|
| Lines | 70% | 80% | 90%+ |
| Branches | 60% | 75% | 85%+ |
| Functions | 70% | 80% | 90%+ |
| Statements | 70% | 80% | 90%+ |

## Test Templates

### Unit Test (Jest/Vitest)

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { calculateTotal, formatCurrency } from './utils';

describe('calculateTotal', () => {
  it('should sum all item prices', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 1 },
    ];
    expect(calculateTotal(items)).toBe(25);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle decimal prices', () => {
    const items = [{ price: 10.99, quantity: 1 }];
    expect(calculateTotal(items)).toBeCloseTo(10.99);
  });
});
```

### Testing Async Functions

```typescript
describe('fetchUser', () => {
  it('should return user data', async () => {
    const user = await fetchUser(1);
    expect(user).toEqual({
      id: 1,
      name: expect.any(String),
      email: expect.stringContaining('@'),
    });
  });

  it('should throw for non-existent user', async () => {
    await expect(fetchUser(999)).rejects.toThrow('User not found');
  });
});
```

### Mocking Dependencies

```typescript
import { vi } from 'vitest';
import { sendEmail } from './email';
import { createUser } from './user';

vi.mock('./email', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true }),
}));

describe('createUser', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should send welcome email after creating user', async () => {
    await createUser({ name: 'John', email: 'john@test.com' });

    expect(sendEmail).toHaveBeenCalledWith({
      to: 'john@test.com',
      template: 'welcome',
    });
  });
});
```

### React Component Testing

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('should render children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### API Route Testing

```typescript
import { createMocks } from 'node-mocks-http';
import handler from './api/users';

describe('GET /api/users', () => {
  it('should return users list', async () => {
    const { req, res } = createMocks({ method: 'GET' });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    expect(JSON.parse(res._getData())).toHaveProperty('users');
  });
});
```

## Branch Coverage Checklist

Ensure tests cover:

- [ ] If/else branches
- [ ] Ternary operators
- [ ] Switch cases (including default)
- [ ] Try/catch blocks
- [ ] Early returns
- [ ] Nullish coalescing (`??`)
- [ ] Optional chaining results (`?.`)
- [ ] Loop conditions (0, 1, many iterations)

## Coverage Configuration

```javascript
// vitest.config.ts
export default {
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        '**/*.d.ts',
        '**/*.test.ts',
        '**/types/',
      ],
      thresholds: {
        lines: 80,
        branches: 75,
        functions: 80,
        statements: 80,
      },
    },
  },
};
```

## Priority Order for Testing

1. **Critical paths**: Auth, payments, data mutations
2. **Complex logic**: Algorithms, state machines, calculations
3. **Error handlers**: Catch blocks, error boundaries
4. **Edge cases**: Empty arrays, null values, boundaries
5. **Integration points**: API calls, database queries
