---
name: testing-strategies
description: Advanced testing strategies and methodologies. Use when user asks to "design tests", "test coverage", "property-based testing", "mutation testing", "contract testing", "chaos engineering", "test pyramid", "testing strategy", "behavior-driven development", "acceptance testing", or mentions comprehensive testing approaches.
---

# Testing Strategies & Methodologies

Comprehensive testing strategies for building reliable, high-quality software systems.

## Test Pyramid

```
        UI/E2E Tests
       /            \
      /              \
   Integration Tests
    /                \
  /                  \
Unit Tests
```

- **Unit Tests**: Fast, isolated, low-level (60%)
- **Integration Tests**: Component interactions (30%)
- **E2E Tests**: Full system workflows (10%)

## Testing Types

### Unit Testing
- Test individual functions/methods
- Mocking dependencies
- Fast execution
- Examples: Jest, Pytest, Mocha

### Integration Testing
- Test component interactions
- With real databases/services
- Slower than unit tests
- Examples: Postman, Supertest

### End-to-End Testing
- Complete user workflows
- Browser automation
- Slowest but most realistic
- Examples: Cypress, Selenium, Playwright

### Property-Based Testing
- Generate random inputs
- Verify invariants hold
- Find edge cases
- Examples: Hypothesis, QuickCheck

### Contract Testing
- Verify API contracts between services
- Consumer and provider sides
- Microservices testing
- Examples: Pact, Spring Cloud Contract

### Chaos Engineering
- Inject failures intentionally
- Test system resilience
- Find weak points
- Tools: Chaos Toolkit, Gremlin

## Best Practices

1. **Test Behavior, Not Implementation** - Focus on what, not how
2. **Keep Tests Fast** - Run frequently
3. **Isolate Dependencies** - Mock external systems
4. **Clear Test Names** - Describe what's being tested
5. **DRY Tests** - Eliminate duplication
6. **Test Edge Cases** - Boundaries, nulls, errors
7. **Use Test Fixtures** - Consistent setup
8. **Automate Testing** - CI/CD integration

## Test Naming Convention

```
test_[function]_[scenario]_[expected_outcome]

Example:
test_calculateDiscount_withValidCode_returnsDiscountedPrice
test_loginUser_withInvalidPassword_throwsAuthenticationError
```

## Example Test Patterns

### AAA Pattern (Arrange-Act-Assert)
```javascript
test('calculateTotal with items', () => {
  // Arrange
  const cart = new Cart();
  cart.addItem({ price: 10 }, 2);
  
  // Act
  const total = cart.getTotal();
  
  // Assert
  expect(total).toBe(20);
});
```

### BDD (Behavior-Driven Development)
```gherkin
Feature: User Authentication
  Scenario: Login with valid credentials
    Given a user with email "test@example.com"
    When the user logs in with correct password
    Then they should see the dashboard
```

## Metrics

- **Code Coverage**: % of code executed by tests (aim for 80%+)
- **Test Pass Rate**: % of tests passing
- **Test Execution Time**: How long tests take to run
- **Mutation Score**: % of introduced bugs caught

## Common Pitfalls to Avoid

- Over-testing trivial code
- Not testing error paths
- Flaky tests (non-deterministic)
- Testing implementation details
- Ignoring performance in tests
- Not testing concurrency

## References

- Test Driven Development (Kent Beck)
- Growing Object-Oriented Software, Guided by Tests
- Working Effectively with Legacy Code (Michael Feathers)
- Testing Strategies for Microservices
- Chaos Engineering (whitepaper)
