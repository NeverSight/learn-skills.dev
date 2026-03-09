---
name: testing-functional-suite
description: Run comprehensive functional test suite
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Functional Test Suite

Run comprehensive functional testing covering unit, integration, and system tests to validate application functionality.

## When to use me

Use this skill when:
- Running complete functional validation before releases
- Setting up CI/CD pipeline with full test coverage
- Testing all functional requirements systematically
- Ensuring code changes don't break existing functionality
- Preparing for QA review or user acceptance testing

## What I do

1. **Unit Testing Layer**
   - Run isolated component tests
   - Validate individual functions and methods
   - Achieve high code coverage (>80%)
   - Mock external dependencies

2. **Integration Testing Layer**
   - Test component interactions
   - Validate API contracts and data flows
   - Test database and external service integrations
   - Check error handling across boundaries

3. **System Testing Layer**
   - Test complete end-to-end workflows
   - Validate functional requirements
   - Test user interfaces and interactions
   - Perform smoke and regression testing

## Examples

```bash
# Run complete functional test suite
npm run test:functional           # Custom functional suite
npm run test                      # Default test command

# Run in CI/CD pipeline
npm run test:ci                   # CI-optimized testing
npm run test:coverage             # With coverage reporting

# Sequential execution
npm run test:unit && npm run test:integration && npm run test:e2e

# Parallel execution (if supported)
npm run test:all --parallel
```

## Output format

```
Functional Test Suite Results:
──────────────────────────────
Test Pyramid Execution:

Unit Tests (1,234 tests):
  ✅ Passed: 1,230 (99.7%)
  ⚠️ Skipped: 2
  ❌ Failed: 2
  📊 Coverage: 92%

Integration Tests (87 tests):
  ✅ Passed: 85 (97.7%)
  ❌ Failed: 2
    - Database connection pooling
    - Payment gateway timeout

System Tests (23 tests):
  ✅ Passed: 20 (87.0%)
  ❌ Failed: 3
    - User registration flow
    - Checkout process
    - Admin dashboard

Overall: 1,344 tests, 95.2% pass rate
Critical Paths: 15/18 passed (83.3%)
Recommendation: Fix system test failures before release
```

## Notes

- Follow test pyramid principle: many unit tests, fewer integration, even fewer system tests
- Run fast unit tests on every commit
- Run integration tests on pull requests
- Run system tests before releases
- Automate functional testing in CI/CD
- Track test metrics and trends over time
- Use test tags to categorize test types
- Implement flaky test detection and management
