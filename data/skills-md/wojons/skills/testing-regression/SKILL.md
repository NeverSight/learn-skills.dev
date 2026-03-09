---
name: testing-regression
description: Run regression tests to ensure new changes don't break existing functionality
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Regression Testing

Run regression tests to ensure new changes don't break existing functionality, coordinating with other test types for comprehensive coverage.

## When to use me

Use this skill when:
- Making code changes that might affect existing functionality
- Preparing for releases or deployments
- Running automated test suites in CI/CD pipelines
- Validating fixes don't introduce new bugs
- Ensuring backward compatibility

## What I do

- **Coordinate with other test types**:
  - Run unit tests to verify individual components still work
  - Execute integration tests to check component interactions
  - Perform end-to-end tests for critical user workflows
  - Check API contracts remain unchanged

- **Test selection strategies**:
  - Run all tests for major changes
  - Selective testing based on change impact analysis
  - Risk-based regression testing for high-impact areas
  - Automated test suite prioritization

- **Integration with development workflow**:
  - Pre-commit regression testing
  - Pull request validation
  - Release candidate testing
  - Hotfix verification

## Examples

```bash
# Run full regression suite
npm run test:regression           # Full regression suite
npm run test:regression:quick     # Quick regression (smoke tests)
npm run test:regression:selective # Tests related to changed files

# CI/CD integration
npm run test:ci                   # CI regression suite
npm run test:pr                   # PR validation tests

# Test selection based on changes
npx jest --listTests | grep -E "(auth|user)"  # Select auth-related tests
npm run test:affected -- --base=main          # Run tests for changed code

# Coordinate with other test types
npm run test:unit && npm run test:integration && npm run test:e2e:critical
```

## Output format

```
Regression Test Results:
──────────────────────────────
Test Scope: Selective regression (changed: auth module)
Execution Order:
  1. Unit Tests (auth service): ✅ 42/42 passed
  2. Integration Tests (auth API): ✅ 8/8 passed  
  3. E2E Tests (login flow): ✅ 3/3 passed
  4. API Contract Tests: ✅ No breaking changes

Dependencies Verified:
  - User service depends on auth: ✅ No issues
  - Session management: ✅ Compatible
  - Third-party auth providers: ✅ Still functional

Impact Assessment:
  - High Risk Areas: 0 affected
  - Medium Risk Areas: 1 (password reset flow)
  - Low Risk Areas: 3

Recommendation:
  - All regression tests pass
  - Safe to merge/deploy
  - Monitor password reset in staging
```

## Notes

- Regression tests should be fast and reliable
- Automate regression testing in CI/CD pipelines
- Use test suites that other test types (unit, integration, e2e) have validated
- Implement flaky test detection and quarantine
- Consider visual regression testing for UI changes
- Track test execution time and optimize slow tests
- Use parallel execution where possible
- Maintain test data consistency across runs
