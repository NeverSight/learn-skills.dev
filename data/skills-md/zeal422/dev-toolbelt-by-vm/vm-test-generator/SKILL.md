---
name: vm-test-generator
description: Generates unit tests, integration tests, and edge cases for existing code. Auto-detects testing framework (Jest, Vitest, Pytest, Go test, etc.) and creates comprehensive tests to prevent regression.
---

# VM Test Generator Skill

Comprehensive test generation for unit tests, integration tests, and edge cases with automatic framework detection.

## Workflow

### Step 1: Initial Prompt

**ALWAYS start by asking the user:**

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "Ready to check for tests?",
      "type": "single_select",
      "options": [
        "Yes! Let's go!",
        "No, thanks."
      ]
    }
  ]
})
```

**If "No, thanks."** → Stop immediately with:
```
No problem! Let me know when you're ready to generate tests. 🧪
```

**If "Yes! Let's go!"** → Proceed with:
```
Detecting framework... 🔍
```

### Step 2: Framework Detection

Auto-detect testing framework(s) by examining:
- Package.json (Jest, Vitest, Mocha, Jasmine)
- requirements.txt / setup.py (Pytest, unittest)
- go.mod (Go testing)
- Cargo.toml (Rust testing)
- pom.xml / build.gradle (JUnit)
- Existing test files and their structure

**Display findings:**
```
Framework Detected: Jest 29.5 ✓
Test Directory: __tests__/
Coverage Tool: Istanbul
Current Coverage: 45% (23/51 files)

Analyzing codebase structure...
```

**Multi-framework projects:**
```
Frameworks Detected:
  - Frontend: Vitest 1.0 (React Testing Library)
  - Backend: Pytest 7.4 (Django)
  - API: Supertest (Express)
  
Proceeding with framework-specific test generation...
```

### Step 3: Scope Selection

**Prompt for scope:**

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "What scope should I analyze?",
      "type": "single_select",
      "options": [
        "Entire Codebase",
        "git diff"
      ]
    }
  ]
})
```

**Entire Codebase:**
- Scan all source files
- Identify untested or under-tested code
- Generate comprehensive test suite

**git diff:**
- Only analyze uncommitted changes
- Generate tests for new/modified code
- Update existing tests affected by changes

### Step 4: Execution Mode

**Prompt for action:**

```python
ask_user_input_v0({
  "questions": [
    {
      "question": "How would you like to proceed?",
      "type": "single_select",
      "options": [
        "Create Plan (TESTS_IMPLEMENTATION_PLAN.md)",
        "Implement Tests Now",
        "No, thanks."
      ]
    }
  ]
})
```

**Option 1: Create Plan**
- Generate `TESTS_IMPLEMENTATION_PLAN.md` in root
- Show test organization structure
- List all tests to be created
- Respond: `All done! The Plan is ready! 📋`
- Stop execution

**Option 2: Implement Tests Now**
- Generate all test files
- Organize per framework conventions
- Create helper/fixture files if needed
- Run initial test suite
- Respond: `ALL DONE! ✅`

**Option 3: No, thanks.**
- Stop with: `Understood. You can run this again anytime! 🧪`

## Test Types Generated

### 1. Unit Tests

Test individual functions/methods in isolation.

**JavaScript/TypeScript (Jest/Vitest):**
```javascript
// src/utils/calculator.js
export function add(a, b) {
  return a + b;
}

export function divide(a, b) {
  if (b === 0) throw new Error('Division by zero');
  return a / b;
}

// __tests__/utils/calculator.test.js
import { add, divide } from '@/utils/calculator';

describe('Calculator Utils', () => {
  describe('add', () => {
    it('adds two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('adds negative numbers', () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it('adds zero', () => {
      expect(add(5, 0)).toBe(5);
    });
  });

  describe('divide', () => {
    it('divides two numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    it('handles decimal results', () => {
      expect(divide(7, 2)).toBe(3.5);
    });

    it('throws on division by zero', () => {
      expect(() => divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

**Python (Pytest):**
```python
# src/calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# tests/test_calculator.py
import pytest
from src.calculator import add, divide

class TestCalculator:
    def test_add_positive_numbers(self):
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert add(-2, -3) == -5

    def test_add_zero(self):
        assert add(5, 0) == 5

    def test_divide_numbers(self):
        assert divide(10, 2) == 5

    def test_divide_decimal(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Division by zero"):
            divide(10, 0)
```

**Go (testing):**
```go
// calculator.go
package calculator

import "errors"

func Add(a, b int) int {
    return a + b
}

func Divide(a, b int) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return float64(a) / float64(b), nil
}

// calculator_test.go
package calculator

import (
    "testing"
)

func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"with zero", 5, 0, 5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}

func TestDivide(t *testing.T) {
    t.Run("valid division", func(t *testing.T) {
        got, err := Divide(10, 2)
        if err != nil {
            t.Errorf("unexpected error: %v", err)
        }
        if got != 5.0 {
            t.Errorf("Divide(10, 2) = %f, want 5.0", got)
        }
    })

    t.Run("division by zero", func(t *testing.T) {
        _, err := Divide(10, 0)
        if err == nil {
            t.Error("expected error, got nil")
        }
    })
}
```

### 2. Integration Tests

Test interactions between components/modules.

**API Integration (Express + Supertest):**
```javascript
// src/routes/users.js
export const router = express.Router();

router.get('/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

router.post('/users', async (req, res) => {
  const user = await db.users.create(req.body);
  res.status(201).json(user);
});

// __tests__/integration/users.test.js
import request from 'supertest';
import app from '@/app';
import { db } from '@/db';

describe('Users API', () => {
  beforeEach(async () => {
    await db.users.deleteAll(); // Clean database
  });

  describe('GET /users/:id', () => {
    it('returns user when found', async () => {
      const user = await db.users.create({ name: 'Alice', email: 'alice@example.com' });
      
      const response = await request(app)
        .get(`/users/${user.id}`)
        .expect(200);

      expect(response.body).toEqual({
        id: user.id,
        name: 'Alice',
        email: 'alice@example.com'
      });
    });

    it('returns 404 when user not found', async () => {
      const response = await request(app)
        .get('/users/nonexistent')
        .expect(404);

      expect(response.body).toEqual({ error: 'User not found' });
    });
  });

  describe('POST /users', () => {
    it('creates new user', async () => {
      const userData = { name: 'Bob', email: 'bob@example.com' };
      
      const response = await request(app)
        .post('/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject(userData);
      expect(response.body.id).toBeDefined();

      // Verify in database
      const user = await db.users.findById(response.body.id);
      expect(user).toBeTruthy();
    });
  });
});
```

**Database Integration (Pytest + Django):**
```python
# tests/integration/test_user_service.py
import pytest
from django.test import TestCase
from myapp.models import User
from myapp.services import UserService

@pytest.mark.django_db
class TestUserService:
    def test_create_user(self):
        service = UserService()
        user = service.create_user(
            name="Alice",
            email="alice@example.com"
        )
        
        assert user.id is not None
        assert user.name == "Alice"
        
        # Verify database
        db_user = User.objects.get(id=user.id)
        assert db_user.email == "alice@example.com"

    def test_get_user_by_email(self):
        # Setup
        User.objects.create(name="Bob", email="bob@example.com")
        
        # Test
        service = UserService()
        user = service.get_user_by_email("bob@example.com")
        
        assert user is not None
        assert user.name == "Bob"

    def test_get_nonexistent_user_returns_none(self):
        service = UserService()
        user = service.get_user_by_email("nonexistent@example.com")
        assert user is None
```

### 3. Edge Cases

Test boundary conditions, unusual inputs, and error scenarios.

**Edge Case Examples:**

```javascript
// __tests__/edge-cases/string-parser.test.js
describe('StringParser edge cases', () => {
  describe('boundary values', () => {
    it('handles empty string', () => {
      expect(parse('')).toEqual([]);
    });

    it('handles very long string (10MB)', () => {
      const longString = 'a'.repeat(10 * 1024 * 1024);
      expect(() => parse(longString)).not.toThrow();
    });

    it('handles single character', () => {
      expect(parse('x')).toEqual(['x']);
    });
  });

  describe('special characters', () => {
    it('handles unicode emoji', () => {
      expect(parse('Hello 👋 World 🌍')).toContain('👋');
    });

    it('handles null bytes', () => {
      expect(parse('text\x00more')).toBeDefined();
    });

    it('handles mixed encodings', () => {
      expect(parse('café')).toBe('café');
    });
  });

  describe('malformed input', () => {
    it('handles null input', () => {
      expect(() => parse(null)).toThrow('Invalid input');
    });

    it('handles undefined input', () => {
      expect(() => parse(undefined)).toThrow('Invalid input');
    });

    it('handles non-string input', () => {
      expect(() => parse(123)).toThrow('Expected string');
    });
  });

  describe('concurrent access', () => {
    it('handles parallel parsing', async () => {
      const promises = Array(100).fill(0).map((_, i) => 
        parse(`string ${i}`)
      );
      const results = await Promise.all(promises);
      expect(results).toHaveLength(100);
    });
  });
});
```

**Numeric Edge Cases:**
```python
# tests/edge_cases/test_numeric_operations.py
import pytest
import math
import sys
from decimal import Decimal
from numeric_ops import add, subtract, divide, multiply, add_decimal

class TestNumericEdgeCases:
    def test_max_integer(self):
        result = add(sys.maxsize, 1)
        assert result > sys.maxsize  # Should handle overflow

    def test_min_integer(self):
        result = subtract(-sys.maxsize, 1)
        assert result < -sys.maxsize

    def test_float_precision(self):
        # 0.1 + 0.2 != 0.3 in floating point
        result = add(0.1, 0.2)
        assert math.isclose(result, 0.3, rel_tol=1e-9)

    def test_infinity(self):
        result = divide(1, 0.0)
        assert math.isinf(result)

    def test_nan_handling(self):
        result = multiply(float('nan'), 5)
        assert math.isnan(result)

    def test_decimal_precision(self):
        result = add_decimal(Decimal('0.1'), Decimal('0.2'))
        assert result == Decimal('0.3')  # Exact precision
```

### 4. Async/Promise Tests

**JavaScript Async:**
```javascript
// __tests__/async/api-client.test.js
describe('API Client async operations', () => {
  it('fetches data successfully', async () => {
    const data = await fetchUser(123);
    expect(data).toHaveProperty('id', 123);
  });

  it('handles timeout', async () => {
    await expect(
      fetchUser(999, { timeout: 100 })
    ).rejects.toThrow('Request timeout');
  });

  it('retries on failure', async () => {
    const mockFetch = jest.fn()
      .mockRejectedValueOnce(new Error('Network error'))
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValueOnce({ data: 'success' });

    const result = await fetchWithRetry(mockFetch, { retries: 3 });
    expect(result).toEqual({ data: 'success' });
    expect(mockFetch).toHaveBeenCalledTimes(3);
  });

  it('handles concurrent requests', async () => {
    const promises = [
      fetchUser(1),
      fetchUser(2),
      fetchUser(3)
    ];

    const results = await Promise.all(promises);
    expect(results).toHaveLength(3);
    results.forEach((result, i) => {
      expect(result.id).toBe(i + 1);
    });
  });
});
```

### 5. Mocking & Stubbing

**Mock External Dependencies:**

```javascript
// __tests__/mocks/payment-service.test.js
import { processPayment } from '@/services/payment';
import { stripeAPI } from '@/lib/stripe';

jest.mock('@/lib/stripe');

describe('Payment Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('processes successful payment', async () => {
    stripeAPI.charge.mockResolvedValue({
      id: 'ch_123',
      status: 'succeeded',
      amount: 1000
    });

    const result = await processPayment({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa'
    });

    expect(result.success).toBe(true);
    expect(stripeAPI.charge).toHaveBeenCalledWith({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa'
    });
  });

  it('handles payment failure', async () => {
    stripeAPI.charge.mockRejectedValue(
      new Error('Card declined')
    );

    const result = await processPayment({
      amount: 1000,
      currency: 'usd',
      source: 'tok_visa'
    });

    expect(result.success).toBe(false);
    expect(result.error).toBe('Card declined');
  });
});
```

**Python Mocking:**
```python
# tests/mocks/test_email_service.py
from unittest.mock import Mock, patch
import pytest
from myapp.services import EmailService

class TestEmailService:
    @patch('myapp.services.email_client')
    def test_send_email_success(self, mock_client):
        mock_client.send.return_value = {'id': 'msg_123', 'status': 'sent'}
        
        service = EmailService()
        result = service.send(
            to='user@example.com',
            subject='Test',
            body='Hello'
        )
        
        assert result['status'] == 'sent'
        mock_client.send.assert_called_once()

    @patch('myapp.services.email_client')
    def test_send_email_failure(self, mock_client):
        mock_client.send.side_effect = Exception('SMTP error')
        
        service = EmailService()
        with pytest.raises(Exception, match='SMTP error'):
            service.send(
                to='user@example.com',
                subject='Test',
                body='Hello'
            )
```

### 6. Component Tests (React)

**React Testing Library:**
```javascript
// __tests__/components/UserCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import UserCard from '@/components/UserCard';

describe('UserCard Component', () => {
  const mockUser = {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    avatar: 'https://example.com/avatar.jpg'
  };

  it('renders user information', () => {
    render(<UserCard user={mockUser} />);
    
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('src', mockUser.avatar);
  });

  it('calls onDelete when delete button clicked', () => {
    const handleDelete = jest.fn();
    render(<UserCard user={mockUser} onDelete={handleDelete} />);
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);
    
    expect(handleDelete).toHaveBeenCalledWith(mockUser.id);
  });

  it('shows loading state', () => {
    render(<UserCard user={mockUser} loading={true} />);
    
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
    expect(screen.queryByText('Alice')).not.toBeInTheDocument();
  });

  it('handles missing avatar gracefully', () => {
    const userWithoutAvatar = { ...mockUser, avatar: null };
    render(<UserCard user={userWithoutAvatar} />);
    
    const avatar = screen.getByRole('img');
    expect(avatar).toHaveAttribute('src', '/default-avatar.png');
  });
});
```

## Test Organization by Framework

### Jest/Vitest (JavaScript/TypeScript)
```
project/
├── src/
│   ├── components/
│   ├── utils/
│   └── services/
├── __tests__/
│   ├── unit/
│   │   ├── utils/
│   │   └── services/
│   ├── integration/
│   │   └── api/
│   ├── e2e/
│   └── fixtures/
│       └── mockData.js
├── jest.config.js
└── package.json
```

### Pytest (Python)
```
project/
├── src/
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_utils.py
│   ├── integration/
│   │   └── test_services.py
│   ├── fixtures/
│   │   └── conftest.py
│   └── __init__.py
├── pytest.ini
└── requirements-dev.txt
```

### Go Testing
```
project/
├── pkg/
│   ├── calculator/
│   │   ├── calculator.go
│   │   └── calculator_test.go
│   └── models/
│       ├── user.go
│       └── user_test.go
├── internal/
│   └── services/
│       ├── auth.go
│       └── auth_test.go
└── go.mod
```

### Rust Testing
```
project/
├── src/
│   ├── lib.rs
│   ├── calculator.rs
│   └── models/
│       └── user.rs
├── tests/
│   ├── integration_test.rs
│   └── common/
│       └── mod.rs
└── Cargo.toml
```

## Test Coverage Analysis

**Generate coverage report showing:**

```
Coverage Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File                    Coverage    Missing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
src/utils/calculator.js  100%       -
src/utils/parser.js       85%       lines 45-52
src/services/user.js      60%       lines 23-35, 89-105
src/models/order.js       40%       lines 12-89
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                     71%       
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority Test Generation:
1. src/models/order.js (40% → target 80%)
2. src/services/user.js (60% → target 85%)
3. src/utils/parser.js (85% → target 95%)

Estimated tests to write: 47
Estimated time: 2-3 hours
```

## TESTS_IMPLEMENTATION_PLAN.md Format

```markdown
# Test Implementation Plan

**Generated**: 2026-02-14
**Framework**: Jest 29.5 + React Testing Library
**Scope**: Entire Codebase
**Current Coverage**: 45%
**Target Coverage**: 85%

## Summary

- **Total Files**: 51
- **Files with Tests**: 23 (45%)
- **Files Needing Tests**: 28 (55%)
- **Estimated Tests to Write**: 142
- **Estimated Time**: 6-8 hours

## Priority 1: Critical Untested Code (0% coverage)

### src/services/payment.js
- [ ] Unit: `processPayment()` - happy path
- [ ] Unit: `processPayment()` - card declined
- [ ] Unit: `processPayment()` - network error
- [ ] Unit: `refundPayment()` - full refund
- [ ] Unit: `refundPayment()` - partial refund
- [ ] Integration: Payment flow with Stripe API
- [ ] Edge: Large payment amounts
- [ ] Edge: Multiple concurrent payments

**Estimated**: 8 tests, 30 minutes

### src/models/Order.js
- [ ] Unit: `create()` - valid order
- [ ] Unit: `create()` - invalid data
- [ ] Unit: `calculateTotal()` - with tax
- [ ] Unit: `calculateTotal()` - with discount
- [ ] Unit: `updateStatus()` - valid transition
- [ ] Unit: `updateStatus()` - invalid transition
- [ ] Integration: Order lifecycle (create → pay → ship)
- [ ] Edge: Concurrent order updates

**Estimated**: 8 tests, 45 minutes

## Priority 2: Low Coverage (< 50%)

### src/utils/validation.js (30% coverage)
- [ ] Unit: `validateEmail()` - valid formats
- [ ] Unit: `validateEmail()` - invalid formats
- [ ] Unit: `validatePhone()` - international formats
- [ ] Unit: `sanitizeInput()` - XSS prevention
- [ ] Edge: Very long inputs
- [ ] Edge: Special characters

**Estimated**: 6 tests, 20 minutes

### src/components/CheckoutForm.jsx (40% coverage)
- [ ] Component: Renders all fields
- [ ] Component: Submit with valid data
- [ ] Component: Shows validation errors
- [ ] Component: Handles API errors
- [ ] Component: Disables submit while processing
- [ ] Integration: Full checkout flow
- [ ] Edge: Network timeout during submit

**Estimated**: 7 tests, 40 minutes

## Priority 3: Moderate Coverage (50-80%)

### src/services/user.js (65% coverage)
Missing tests for:
- [ ] `resetPassword()` - expired token
- [ ] `updateProfile()` - concurrent updates
- [ ] Edge: Rate limiting

**Estimated**: 3 tests, 15 minutes

### src/utils/formatter.js (70% coverage)
Missing tests for:
- [ ] `formatCurrency()` - negative values
- [ ] `formatDate()` - invalid dates
- [ ] Edge: Locale-specific formatting

**Estimated**: 3 tests, 15 minutes

## Test Organization

```
__tests__/
├── unit/
│   ├── services/
│   │   ├── payment.test.js (NEW)
│   │   └── user.test.js (UPDATE)
│   ├── models/
│   │   └── Order.test.js (NEW)
│   ├── utils/
│   │   ├── validation.test.js (NEW)
│   │   └── formatter.test.js (UPDATE)
│   └── components/
│       └── CheckoutForm.test.jsx (NEW)
├── integration/
│   ├── checkout-flow.test.js (NEW)
│   └── payment-flow.test.js (NEW)
└── fixtures/
    ├── mockOrders.js (NEW)
    └── mockUsers.js (UPDATE)
```

## Test Helpers to Create

```javascript
// __tests__/helpers/mockStripe.js
export const mockStripeClient = {
  charge: jest.fn(),
  refund: jest.fn()
};

// __tests__/helpers/testDatabase.js
export async function setupTestDB() {
  // Setup logic
}

export async function cleanupTestDB() {
  // Cleanup logic
}
```

## Coverage Goals

| Category       | Current | Target | Tests Needed |
|----------------|---------|--------|--------------|
| Critical Code  | 0%      | 100%   | 16 tests     |
| Services       | 45%     | 85%    | 32 tests     |
| Components     | 60%     | 90%    | 28 tests     |
| Utils          | 70%     | 95%    | 18 tests     |
| Models         | 40%     | 85%    | 25 tests     |
| Integration    | 20%     | 70%    | 23 tests     |

**Total**: 142 tests

## Implementation Schedule

**Phase 1 (Day 1)**: Critical untested code
- Payment service
- Order model
- Estimated: 3-4 hours

**Phase 2 (Day 2)**: Low coverage files
- Validation utils
- Checkout component
- Estimated: 2-3 hours

**Phase 3 (Day 3)**: Integration tests
- Checkout flow
- Payment flow
- Estimated: 2-3 hours

**Phase 4 (Day 4)**: Polish & edge cases
- Fill gaps to reach target coverage
- Estimated: 1-2 hours

## Commands to Run

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific file
npm test -- payment.test.js

# Watch mode
npm test -- --watch

# Update snapshots
npm test -- -u
```

## Notes

- Mock external APIs (Stripe, SendGrid)
- Use test database, not production
- Set up CI/CD to run tests on every push
- Add pre-commit hook to run tests locally
- Configure coverage thresholds in jest.config.js
```

## Framework-Specific Test Templates

### Jest Template
```javascript
import { functionToTest } from '@/module';

describe('ModuleName', () => {
  describe('functionName', () => {
    it('handles normal case', () => {
      const result = functionToTest('input');
      expect(result).toBe('expected');
    });

    it('handles edge case', () => {
      expect(() => functionToTest(null)).toThrow();
    });
  });
});
```

### Pytest Template
```python
import pytest
from mymodule import function_to_test

class TestModuleName:
    def test_normal_case(self):
        result = function_to_test('input')
        assert result == 'expected'

    def test_edge_case(self):
        with pytest.raises(ValueError):
            function_to_test(None)
```

### Go Template
```go
package mypackage

import "testing"

func TestFunctionName(t *testing.T) {
    t.Run("normal case", func(t *testing.T) {
        got := FunctionToTest("input")
        want := "expected"
        if got != want {
            t.Errorf("got %q, want %q", got, want)
        }
    })

    t.Run("edge case", func(t *testing.T) {
        defer func() {
            if r := recover(); r == nil {
                t.Error("expected panic")
            }
        }()
        FunctionToTest(nil)
    })
}
```

## Regression Prevention

Tests generated include:
1. **Current behavior snapshot** - Ensure changes don't break existing functionality
2. **Error path coverage** - Test all error conditions
3. **Edge case validation** - Boundary values, null/undefined, empty inputs
4. **Integration checkpoints** - Verify component interactions
5. **Performance benchmarks** - Track performance regressions (when applicable)

## Best Practices Applied

✅ **AAA Pattern** - Arrange, Act, Assert  
✅ **One assertion per test** (when logical)  
✅ **Descriptive test names** - Clear what's being tested  
✅ **Isolated tests** - No dependencies between tests  
✅ **Fast execution** - Mock external dependencies  
✅ **Deterministic** - Same input = same output  
✅ **Maintainable** - Easy to update when code changes  

## Final Output Messages

**Plan Mode:**
```
✅ Test Implementation Plan Created!

📋 Plan Location: /project-root/TESTS_IMPLEMENTATION_PLAN.md

Summary:
- 142 tests planned
- Target coverage: 85%
- Estimated time: 6-8 hours

All done! The Plan is ready! 📋
```

**Implementation Mode:**
```
✅ Test Generation Complete!

📊 Results:
- Tests created: 142
- Files created: 28
- Coverage: 45% → 87%

📁 Test files organized in:
- __tests__/unit/ (98 tests)
- __tests__/integration/ (32 tests)
- __tests__/fixtures/ (12 helpers)

🧪 Run tests: npm test
📈 Check coverage: npm test -- --coverage

ALL DONE! ✅
```

## Execution Notes

1. **Framework detection is critical** - Wrong framework = wrong test structure
2. **Analyze existing tests first** - Don't duplicate, extend
3. **Generate meaningful test data** - Not just placeholder values
4. **Cover error paths** - Don't just test happy path
5. **Use real examples** - Based on actual code, not generic templates
6. **Organize logically** - Follow framework conventions
7. **Include setup/teardown** - Proper test isolation
8. **Mock external dependencies** - Tests should be fast and isolated
