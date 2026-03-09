---
name: testing-e2e
description: Run end-to-end tests for complete user workflows
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# End-to-End Testing

Test complete user workflows from start to finish in a production-like environment.

## When to use me

Use this skill when:
- Testing critical user journeys before release
- Validating complete system integration
- Ensuring UI interactions work correctly
- Simulating real user behavior and scenarios
- Testing across multiple systems and services
- Performing acceptance testing from user perspective

## What I do

- Identify critical user workflows and happy paths
- Set up production-like test environments
- Simulate user interactions with the application
- Test across browsers, devices, and platforms
- Validate complete data flows from UI to database
- Test error scenarios and recovery flows
- Measure performance of complete user journeys

## Examples

```bash
# Run E2E tests with common frameworks
npm run test:e2e              # Cypress, Playwright, Selenium
npx cypress run              # Cypress specifically
npx playwright test         # Playwright
pytest tests/e2e/           # Python with Selenium

# Run specific E2E test suites
npm run test:e2e -- --spec "cypress/e2e/login.cy.js"
npx playwright test login.spec.js

# Run with different browsers
npx playwright test --browser=all
npx cypress run --browser chrome

# Run with visual testing
npx playwright test --screenshot=on
```

## Output format

```
End-to-End Test Results:
──────────────────────────────
✅ User Registration Flow
  ✓ Visit registration page
  ✓ Fill registration form
  ✓ Submit form successfully
  ✓ Verify confirmation email
  ✓ Login with new credentials

❌ Checkout Flow
  ✗ Add item to cart
  ✓ Proceed to checkout
  ✗ Payment processing fails (Timeout)
    Error: Payment gateway timeout after 30s

⚠️ Account Settings
  ⚠️ Password change saves but email not sent

Summary: 12 scenarios, 9 passed, 2 failed, 1 warning
Test Duration: 4m 23s
```

## Notes

- E2E tests are slowest but most realistic
- Run fewer E2E tests, focus on critical paths
- Use headless browsers for CI/CD pipelines
- Implement retry logic for flaky tests
- Clean up test data thoroughly
- Consider visual regression testing for UI
- Test across multiple viewport sizes
- Monitor test execution time and optimize
