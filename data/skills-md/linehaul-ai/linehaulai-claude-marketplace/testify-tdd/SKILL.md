---
name: testify-tdd
description: Use this skill when writing Go tests with stretchr/testify, implementing TDD workflows, creating mocks, or organizing test suites. Covers assert vs require patterns, interface mocking, table-driven tests, and the red-green-refactor cycle.
keywords: [go, testing, tdd, testify, unit-tests, mocking]
disable-model-invocation: false
user-invocable: true
---

# Go Testing with Testify and TDD

Comprehensive guide for writing Go tests using stretchr/testify and following Test-Driven Development methodology.

## Installation

```bash
go get github.com/stretchr/testify
```

## Testify Packages Overview

| Package | Purpose | When to Use |
|---------|---------|-------------|
| `testify/assert` | Assertions that continue on failure | Multiple independent checks in one test |
| `testify/require` | Assertions that halt on failure | Prerequisites that must pass to continue |
| `testify/mock` | Interface mocking | Isolating dependencies in unit tests |
| `testify/suite` | Test organization | Related tests sharing setup/teardown |

## Assert vs Require

**Critical distinction**: Choose based on whether the test should continue after failure.

### Use `require` for Prerequisites

```go
func TestUserService_GetByID(t *testing.T) {
    // Prerequisites - if these fail, nothing else matters
    db, err := setupTestDB()
    require.NoError(t, err, "database setup must succeed")
    require.NotNil(t, db, "database connection required")

    user, err := service.GetByID(ctx, userID)
    require.NoError(t, err)  // Can't verify user if this fails

    // Verifications - these can use assert
    assert.Equal(t, expectedName, user.Name)
    assert.Equal(t, expectedEmail, user.Email)
    assert.True(t, user.IsActive)
}
```

### Use `assert` for Multiple Independent Checks

```go
func TestOrderValidation(t *testing.T) {
    order := createTestOrder()
    errors := order.Validate()

    // All checks run even if earlier ones fail
    assert.NotEmpty(t, order.ID, "order should have ID")
    assert.Greater(t, order.Total, 0.0, "total should be positive")
    assert.NotEmpty(t, order.Items, "order should have items")
    assert.Empty(t, errors, "validation should pass")
}
```

### Common Assertion Methods

```go
// Equality
assert.Equal(t, expected, actual)
assert.NotEqual(t, expected, actual)
assert.EqualValues(t, expected, actual)  // Type-coerced comparison

// Nil checks
assert.Nil(t, value)
assert.NotNil(t, value)

// Boolean
assert.True(t, condition)
assert.False(t, condition)

// Collections
assert.Empty(t, collection)
assert.NotEmpty(t, collection)
assert.Len(t, collection, expectedLen)
assert.Contains(t, collection, element)
assert.ElementsMatch(t, expected, actual)  // Order-independent

// Errors
assert.NoError(t, err)
assert.Error(t, err)
assert.ErrorIs(t, err, expectedErr)
assert.ErrorContains(t, err, "substring")

// Comparisons
assert.Greater(t, a, b)
assert.GreaterOrEqual(t, a, b)
assert.Less(t, a, b)
assert.LessOrEqual(t, a, b)

// Strings
assert.Contains(t, str, substring)
assert.Regexp(t, pattern, str)

// JSON
assert.JSONEq(t, expectedJSON, actualJSON)

// Time
assert.WithinDuration(t, expected, actual, delta)
```

## Table-Driven Tests

The idiomatic Go pattern for testing multiple scenarios.

```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name           string
        orderTotal     float64
        customerTier   string
        expectedDiscount float64
        expectError    bool
    }{
        {
            name:           "no discount for small orders",
            orderTotal:     50.00,
            customerTier:   "standard",
            expectedDiscount: 0,
        },
        {
            name:           "10% discount for gold tier",
            orderTotal:     100.00,
            customerTier:   "gold",
            expectedDiscount: 10.00,
        },
        {
            name:           "20% discount for platinum over $500",
            orderTotal:     600.00,
            customerTier:   "platinum",
            expectedDiscount: 120.00,
        },
        {
            name:        "error for negative total",
            orderTotal:  -10.00,
            expectError: true,
        },
    }

    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            discount, err := CalculateDiscount(tc.orderTotal, tc.customerTier)

            if tc.expectError {
                require.Error(t, err)
                return
            }

            require.NoError(t, err)
            assert.Equal(t, tc.expectedDiscount, discount)
        })
    }
}
```

## Interface Mocking

### Define the Mock

```go
import "github.com/stretchr/testify/mock"

// UserRepository is the interface to mock
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
}

// MockUserRepository implements UserRepository for testing
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) GetByID(ctx context.Context, id string) (*User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) Save(ctx context.Context, user *User) error {
    args := m.Called(ctx, user)
    return args.Error(0)
}

func (m *MockUserRepository) Delete(ctx context.Context, id string) error {
    args := m.Called(ctx, id)
    return args.Error(0)
}
```

### Use the Mock in Tests

```go
func TestUserService_UpdateEmail(t *testing.T) {
    ctx := context.Background()
    userID := "user-123"
    newEmail := "new@example.com"

    existingUser := &User{
        ID:    userID,
        Email: "old@example.com",
        Name:  "Test User",
    }

    // Create mock
    mockRepo := new(MockUserRepository)

    // Set expectations
    mockRepo.On("GetByID", ctx, userID).Return(existingUser, nil)
    mockRepo.On("Save", ctx, mock.MatchedBy(func(u *User) bool {
        return u.ID == userID && u.Email == newEmail
    })).Return(nil)

    // Create service with mock
    service := NewUserService(mockRepo)

    // Execute
    err := service.UpdateEmail(ctx, userID, newEmail)

    // Verify
    require.NoError(t, err)
    mockRepo.AssertExpectations(t)
}
```

### Mock Argument Matchers

```go
// Exact match
mockRepo.On("GetByID", ctx, "user-123")

// Any value of type
mockRepo.On("GetByID", mock.Anything, mock.AnythingOfType("string"))

// Custom matcher
mockRepo.On("Save", ctx, mock.MatchedBy(func(u *User) bool {
    return u.Email != "" && u.ID != ""
}))

// Verify call count
mockRepo.AssertNumberOfCalls(t, "GetByID", 2)
mockRepo.AssertCalled(t, "Save", ctx, mock.Anything)
mockRepo.AssertNotCalled(t, "Delete", mock.Anything, mock.Anything)
```

### Mock Return Values

```go
// Return specific values
mockRepo.On("GetByID", ctx, "exists").Return(&User{ID: "exists"}, nil)
mockRepo.On("GetByID", ctx, "not-found").Return(nil, ErrNotFound)

// Return dynamically
mockRepo.On("Save", ctx, mock.Anything).Return(nil).Run(func(args mock.Arguments) {
    user := args.Get(1).(*User)
    user.ID = "generated-id"  // Modify the argument
})

// Return different values on successive calls
mockRepo.On("GetByID", ctx, "user-1").Return(&User{}, nil).Once()
mockRepo.On("GetByID", ctx, "user-1").Return(nil, ErrNotFound).Once()
```

## Test Suites

Organize related tests with shared setup and teardown.

```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
)

type UserServiceTestSuite struct {
    suite.Suite
    service  *UserService
    mockRepo *MockUserRepository
    ctx      context.Context
}

// SetupSuite runs once before all tests
func (s *UserServiceTestSuite) SetupSuite() {
    s.ctx = context.Background()
}

// SetupTest runs before each test
func (s *UserServiceTestSuite) SetupTest() {
    s.mockRepo = new(MockUserRepository)
    s.service = NewUserService(s.mockRepo)
}

// TearDownTest runs after each test
func (s *UserServiceTestSuite) TearDownTest() {
    s.mockRepo.AssertExpectations(s.T())
}

// Test methods must start with "Test"
func (s *UserServiceTestSuite) TestGetByID_Success() {
    expected := &User{ID: "123", Name: "Test"}
    s.mockRepo.On("GetByID", s.ctx, "123").Return(expected, nil)

    user, err := s.service.GetByID(s.ctx, "123")

    s.Require().NoError(err)
    s.Equal(expected.Name, user.Name)
}

func (s *UserServiceTestSuite) TestGetByID_NotFound() {
    s.mockRepo.On("GetByID", s.ctx, "999").Return(nil, ErrNotFound)

    user, err := s.service.GetByID(s.ctx, "999")

    s.Nil(user)
    s.ErrorIs(err, ErrNotFound)
}

// Run the suite
func TestUserServiceSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

## TDD Workflow: Red-Green-Refactor

### 1. Red: Write a Failing Test First

```go
func TestShippingCalculator_CalculateCost(t *testing.T) {
    calc := NewShippingCalculator()

    cost, err := calc.CalculateCost(Weight(5.0), Zone("US-WEST"))

    require.NoError(t, err)
    assert.Equal(t, Money(12.50), cost)
}
```

Run the test - it should fail (function doesn't exist or returns wrong value).

### 2. Green: Write Minimal Code to Pass

```go
func (c *ShippingCalculator) CalculateCost(weight Weight, zone Zone) (Money, error) {
    // Minimal implementation to make the test pass
    return Money(12.50), nil
}
```

Run the test - it should pass.

### 3. Refactor: Improve While Keeping Tests Green

```go
func (c *ShippingCalculator) CalculateCost(weight Weight, zone Zone) (Money, error) {
    baseRate := c.getBaseRate(zone)
    weightCharge := weight.Kilograms() * c.ratePerKg
    return Money(baseRate + weightCharge), nil
}
```

Run tests after each refactor to ensure they still pass.

### 4. Add More Test Cases

```go
func TestShippingCalculator_CalculateCost(t *testing.T) {
    tests := []struct {
        name         string
        weight       Weight
        zone         Zone
        expectedCost Money
        expectError  bool
    }{
        {"small package US-WEST", Weight(1.0), Zone("US-WEST"), Money(5.00), false},
        {"medium package US-WEST", Weight(5.0), Zone("US-WEST"), Money(12.50), false},
        {"large package US-EAST", Weight(10.0), Zone("US-EAST"), Money(22.00), false},
        {"zero weight error", Weight(0), Zone("US-WEST"), Money(0), true},
        {"negative weight error", Weight(-1), Zone("US-WEST"), Money(0), true},
    }

    calc := NewShippingCalculator()

    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            cost, err := calc.CalculateCost(tc.weight, tc.zone)

            if tc.expectError {
                require.Error(t, err)
                return
            }

            require.NoError(t, err)
            assert.Equal(t, tc.expectedCost, cost)
        })
    }
}
```

## Test File Organization

### Same-Package Tests (Unit Tests)

```go
// user_service.go
package users

type UserService struct { ... }

// user_service_test.go
package users  // Same package - can test private functions

func TestUserService_validateEmail(t *testing.T) {
    // Can access private method validateEmail
}
```

### Black-Box Tests (Integration Tests)

```go
// user_repository_integration_test.go
package users_test  // Different package - tests public API only

import "myapp/internal/users"

func TestUserRepository_Create(t *testing.T) {
    // Can only access public API
    repo := users.NewRepository(db)
}
```

## Test Naming Conventions

```
Test[Unit]_[Scenario]_[ExpectedBehavior]

Examples:
- TestUserService_GetByID_ReturnsUser
- TestUserService_GetByID_ReturnsErrorWhenNotFound
- TestCalculateDiscount_GoldTier_Returns10Percent
- TestOrderValidator_EmptyItems_ReturnsValidationError
```

## Running Tests

```bash
# Run all tests
go test ./...

# Verbose output
go test -v ./...

# Disable test caching
go test -count=1 ./...

# Run specific test
go test -v -run TestUserService ./...

# Run with coverage
go test -cover ./...

# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Best Practices

1. **One logical assertion per test** - Test one behavior, though you may have multiple assert calls
2. **Descriptive test names** - The name should explain what's being tested
3. **Arrange-Act-Assert pattern** - Structure tests clearly
4. **Use `require` for setup, `assert` for verification**
5. **Table-driven tests for multiple scenarios** - Avoid copy-paste test code
6. **Mock at interface boundaries** - Don't mock what you don't own
7. **Keep tests independent** - No shared state between tests
8. **Test edge cases** - Empty inputs, nil, zero values, boundaries
9. **Don't test implementation details** - Test behavior, not internal structure
10. **Verify mock expectations** - Always call `AssertExpectations(t)`
