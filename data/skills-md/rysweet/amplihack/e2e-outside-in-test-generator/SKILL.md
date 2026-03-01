---
name: e2e-outside-in-test-generator
version: 1.0.0
description: Generates comprehensive end-to-end Playwright tests using outside-in methodology
activation_keywords:
  - "add e2e tests"
  - "add playwright tests"
  - "add browser tests"
  - "add outside-in tests"
  - "generate e2e suite"
category: testing
requires:
  - Frontend framework (Next.js, React, Vue, Angular)
  - Backend API
invokes:
  - test-gap-analyzer (test coverage analysis)
  - shadow-testing (parallel test execution)
  - outside-in-testing (methodology validation)
output_location: e2e/
---

# E2E Outside-In Test Generator

Automatically generates comprehensive end-to-end Playwright tests for full-stack applications using outside-in testing methodology. Generates 40+ tests across 7 categories, finds real bugs, and validates through iterative fix loops.

## LEVEL 1: Quick Start

### Purpose

This skill analyzes your full-stack application and generates a complete Playwright test suite that:

- **Validates user journeys** from browser through backend
- **Finds real bugs** through systematic exploration
- **Runs deterministically** with no flakiness
- **Integrates with CI** out of the box

### When to Use

Activate this skill when you:

- Need comprehensive browser testing for a full-stack app
- Want to validate critical user flows end-to-end
- Need regression coverage before major refactoring
- Are preparing for production deployment

**Requirements**: Your project must have both a frontend (Next.js, React, Vue, Angular) and backend API.

### Quick Start

```bash
# In your project root
$ claude

> add e2e tests
```

The skill automatically:

1. **Analyzes** your application (routes, API endpoints, database schema)
2. **Sets up infrastructure** (Playwright config, test helpers, seed data)
3. **Generates 40+ tests** across 7 categories
4. **Runs tests** and fixes failures (up to 5 iterations)
5. **Reports coverage** and recommendations

### Expected Output

```
e2e/
├── playwright.config.ts          # Playwright configuration
├── test-helpers/
│   ├── auth.ts                   # Authentication helpers
│   ├── navigation.ts             # Navigation helpers
│   ├── assertions.ts             # Custom assertions
│   └── data-setup.ts             # Test data management
├── fixtures/
│   ├── users.json                # Test user data
│   ├── products.json             # Test product data
│   └── seed.sql                  # Database seed script
├── happy-path/
│   ├── user-registration.spec.ts
│   ├── user-login.spec.ts
│   └── checkout-flow.spec.ts
├── edge-cases/
│   ├── invalid-inputs.spec.ts
│   └── boundary-conditions.spec.ts
├── error-handling/
│   ├── network-failures.spec.ts
│   └── validation-errors.spec.ts
├── performance/
│   ├── page-load-times.spec.ts
│   └── api-response-times.spec.ts
├── security/
│   ├── unauthorized-access.spec.ts
│   └── xss-protection.spec.ts
├── accessibility/
│   ├── keyboard-navigation.spec.ts
│   └── screen-reader.spec.ts
└── integration/
    ├── database-persistence.spec.ts
    └── api-integration.spec.ts

Total: 42 tests across 7 categories
```

### Run Your Tests

```bash
# Run all tests
npx playwright test

# Run specific category
npx playwright test e2e/happy-path

# Run in headed mode
npx playwright test --headed

# Run in debug mode
npx playwright test --debug
```

### Success Criteria

After generation, your test suite achieves:

- ✓ **40+ tests** across all 7 categories
- ✓ **100% pass rate** after fix loop
- ✓ **<2 minute** total execution time
- ✓ **≥1 real bug** discovered during generation
- ✓ **Zero flakiness** (deterministic test data)

## LEVEL 2: Full Features

### The 5 Phases

```mermaid
graph LR
    A[Phase 1: Analysis] --> B[Phase 2: Infrastructure]
    B --> C[Phase 3: Generation]
    C --> D[Phase 4: Fix Loop]
    D --> E[Phase 5: Coverage Audit]
```

#### Phase 1: Stack Analysis

The skill performs deep application analysis:

**Frontend Analysis:**

- Detects framework (Next.js, React, Vue, Angular)
- Maps routes and pages
- Identifies navigation patterns
- Extracts interactive elements

**Backend Analysis:**

- Discovers API endpoints (REST/GraphQL)
- Maps data models and relationships
- Identifies authentication mechanisms
- Detects validation rules

**Database Analysis:**

- Extracts schema and relationships
- Identifies required fields
- Determines foreign key constraints
- Maps enum types

**Example Analysis Output:**

```python
StackConfig(
    frontend_framework="nextjs",
    frontend_dir="app/",
    backend_framework="fastapi",
    api_base_url="http://localhost:8000/api",
    database_type="postgresql",
    auth_mechanism="jwt",
    routes=[
        Route(path="/", component="Home"),
        Route(path="/login", component="Login"),
        Route(path="/products", component="ProductList"),
        Route(path="/products/:id", component="ProductDetail"),
        Route(path="/checkout", component="Checkout")
    ],
    api_endpoints=[
        APIEndpoint(path="/auth/login", method="POST"),
        APIEndpoint(path="/auth/register", method="POST"),
        APIEndpoint(path="/products", method="GET"),
        APIEndpoint(path="/products/:id", method="GET"),
        APIEndpoint(path="/orders", method="POST")
    ],
    models=[
        Model(name="User", fields=["id", "email", "password"]),
        Model(name="Product", fields=["id", "name", "price", "stock"]),
        Model(name="Order", fields=["id", "user_id", "product_id", "quantity"])
    ]
)
```

#### Phase 2: Infrastructure Setup

Generates complete testing infrastructure:

**Playwright Configuration:**

```typescript
// e2e/playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false, // CRITICAL: workers=1 for deterministic test data
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // NEVER > 1 to prevent data races
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

**Test Helpers:**

```typescript
// e2e/test-helpers/auth.ts
export async function login(page: Page, email: string, password: string) {
  await page.goto("/login");
  await page.getByRole("textbox", { name: /email/i }).fill(email);
  await page.getByRole("textbox", { name: /password/i }).fill(password);
  await page.getByRole("button", { name: /sign in/i }).click();
  await page.waitForURL("/dashboard");
}

export async function logout(page: Page) {
  await page.getByRole("button", { name: /logout/i }).click();
  await page.waitForURL("/");
}
```

**Seed Data:**

```json
// e2e/fixtures/users.json
[
  {
    "email": "test@example.com",
    "password": "Test123!", // pragma: allowlist secret
    "name": "Test User",
    "role": "customer"
  },
  {
    "email": "admin@example.com",
    "password": "Admin123!", // pragma: allowlist secret
    "name": "Admin User",
    "role": "admin"
  }
]
```

#### Phase 3: Test Generation

Generates tests across 7 mandatory categories:

**1. Happy Path Tests** (Critical user journeys)

```typescript
// e2e/happy-path/user-registration.spec.ts
import { test, expect } from "@playwright/test";

test("user can register with valid credentials", async ({ page }) => {
  await page.goto("/register");

  await page.getByRole("textbox", { name: /email/i }).fill("newuser@example.com");
  await page.getByRole("textbox", { name: /password/i }).fill("Password123!");
  await page.getByRole("textbox", { name: /confirm password/i }).fill("Password123!");
  await page.getByRole("button", { name: /create account/i }).click();

  await expect(page).toHaveURL("/dashboard");
  await expect(page.getByText(/welcome/i)).toBeVisible();
});
```

**2. Edge Case Tests** (Boundary conditions)

```typescript
// e2e/edge-cases/boundary-conditions.spec.ts
test("rejects password that is too short", async ({ page }) => {
  await page.goto("/register");

  await page.getByRole("textbox", { name: /email/i }).fill("test@example.com");
  await page.getByRole("textbox", { name: /password/i }).fill("123"); // Too short
  await page.getByRole("button", { name: /create account/i }).click();

  await expect(page.getByText(/password must be at least 8 characters/i)).toBeVisible();
});
```

**3. Error Handling Tests** (Failure scenarios)

```typescript
// e2e/error-handling/network-failures.spec.ts
test("shows error when API is unavailable", async ({ page, context }) => {
  // Simulate network failure
  await context.route("**/api/**", (route) => route.abort());

  await page.goto("/products");

  await expect(page.getByText(/unable to load products/i)).toBeVisible();
  await expect(page.getByRole("button", { name: /retry/i })).toBeVisible();
});
```

**4. Performance Tests** (Speed validation)

```typescript
// e2e/performance/page-load-times.spec.ts
test("homepage loads in under 2 seconds", async ({ page }) => {
  const startTime = Date.now();
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  const loadTime = Date.now() - startTime;

  expect(loadTime).toBeLessThan(2000);
});
```

**5. Security Tests** (Authorization/XSS)

```typescript
// e2e/security/unauthorized-access.spec.ts
test("redirects unauthenticated users from protected routes", async ({ page }) => {
  await page.goto("/dashboard");

  await expect(page).toHaveURL("/login");
  await expect(page.getByText(/please sign in/i)).toBeVisible();
});
```

**6. Accessibility Tests** (WCAG compliance)

```typescript
// e2e/accessibility/keyboard-navigation.spec.ts
import { test, expect } from "@playwright/test";

test("login form is fully keyboard accessible", async ({ page }) => {
  await page.goto("/login");

  await page.keyboard.press("Tab"); // Focus email
  await page.keyboard.type("test@example.com");
  await page.keyboard.press("Tab"); // Focus password
  await page.keyboard.type("Test123!");
  await page.keyboard.press("Tab"); // Focus submit button
  await page.keyboard.press("Enter"); // Submit form

  await expect(page).toHaveURL("/dashboard");
});
```

**7. Integration Tests** (Database/API)

```typescript
// e2e/integration/database-persistence.spec.ts
test("product order persists across sessions", async ({ page, context }) => {
  // Create order
  await login(page, "test@example.com", "Test123!");
  await page.goto("/products/123");
  await page.getByRole("button", { name: /add to cart/i }).click();
  await page.goto("/checkout");
  await page.getByRole("button", { name: /place order/i }).click();

  const orderNumber = await page.getByText(/order #\d+/).textContent();

  // Logout and login again
  await logout(page);
  await login(page, "test@example.com", "Test123!");

  // Verify order exists
  await page.goto("/orders");
  await expect(page.getByText(orderNumber!)).toBeVisible();
});
```

#### Phase 4: Fix Loop

Automatically fixes failing tests through iterative debugging:

**Fix Loop Process:**

1. **Run tests** → Collect failures
2. **Analyze failures** → Categorize issues (locator, timing, data, logic)
3. **Apply fixes** → Update tests based on issue type
4. **Rerun tests** → Verify fixes
5. **Repeat** → Max 5 iterations

**Common Fix Patterns:**

```typescript
// Before: Flaky locator
await page.click(".submit-button");

// After: Role-based locator
await page.getByRole("button", { name: /submit/i }).click();

// Before: Race condition
await page.click("#login");
await page.fill("#email", "test@example.com");

// After: Wait for navigation
await page.click("#login");
await page.waitForLoadState("networkidle");
await page.fill("#email", "test@example.com");

// Before: Hardcoded data
await page.fill("#quantity", "5");

// After: Dynamic data from fixtures
const product = await getTestProduct();
await page.fill("#quantity", product.minQuantity.toString());
```

**Fix Loop Results:**

```
Iteration 1: 42 tests, 8 failures
  - Fixed 5 locator issues
  - Fixed 2 timing issues
  - Fixed 1 data issue

Iteration 2: 42 tests, 3 failures
  - Fixed 2 locator issues
  - Fixed 1 timing issue

Iteration 3: 42 tests, 0 failures ✓

Fix loop completed in 3 iterations.
```

#### Phase 5: Coverage Audit

Generates comprehensive coverage report and recommendations:

**Coverage Report:**

```markdown
## Test Coverage Report

### Tests Generated: 42

- Happy Path: 12 tests
- Edge Cases: 8 tests
- Error Handling: 6 tests
- Performance: 4 tests
- Security: 5 tests
- Accessibility: 4 tests
- Integration: 3 tests

### Routes Covered: 12/15 (80%)

Uncovered routes:

- /admin/settings (requires admin role)
- /api/webhooks/\* (external integrations)
- /debug/\* (development-only)

### API Endpoints Covered: 18/22 (82%)

Uncovered endpoints:

- POST /api/admin/users (admin-only)
- DELETE /api/products/:id (soft delete, needs verification)
- GET /api/analytics (complex aggregations)
- POST /api/webhooks/stripe (external trigger)

### Bugs Found: 2

1. **CRITICAL**: Login form allows SQL injection via email field
   - Location: app/login/page.tsx:45
   - Test: e2e/security/sql-injection.spec.ts

2. **MEDIUM**: Checkout fails with international phone numbers
   - Location: lib/validation.ts:12
   - Test: e2e/edge-cases/international-phone.spec.ts

### Recommendations

1. Add admin-role tests (requires admin user setup)
2. Add webhook integration tests (requires test webhook server)
3. Add load testing for high-traffic endpoints
4. Increase accessibility coverage (current: 9%, target: 15%)
```

### Customization Options

**Custom Locator Strategies:**

```typescript
// e2e/playwright.config.ts
export default defineConfig({
  use: {
    // Prioritize test IDs
    testIdAttribute: "data-testid",
  },
});
```

**Custom Test Categories:**

```python
# Add custom category during generation
custom_categories = [
    "happy-path",
    "edge-cases",
    "error-handling",
    "performance",
    "security",
    "accessibility",
    "integration",
    "custom-business-rules"  # Your custom category
]
```

**Custom Seed Data:**

```json
// e2e/fixtures/custom-data.json
{
  "scenarios": [
    {
      "name": "bulk-order",
      "users": [...],
      "products": [...],
      "expected_discount": 0.15
    }
  ]
}
```

### Configuration

**Environment Variables:**

```bash
# .env.test
DATABASE_URL=postgresql://test:test@localhost:5432/testdb  # pragma: allowlist secret
API_BASE_URL=http://localhost:8000/api
FRONTEND_URL=http://localhost:3000
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!  # pragma: allowlist secret
```

**Playwright Options:**

```typescript
// e2e/playwright.config.ts
export default defineConfig({
  // Test execution
  workers: 1, // MANDATORY: prevents data races
  fullyParallel: false, // Sequential execution
  retries: process.env.CI ? 2 : 0,

  // Timeouts
  timeout: 30000, // Per-test timeout
  expect: { timeout: 5000 }, // Assertion timeout

  // Artifacts
  use: {
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    trace: "on-first-retry",
  },
});
```

## LEVEL 3: Advanced Usage

### Integration with Other Skills

**With test-gap-analyzer:**

```bash
> analyze test gaps and generate e2e tests to fill them
```

The skill:

1. Runs test-gap-analyzer to identify uncovered flows
2. Prioritizes test generation based on gap analysis
3. Focuses on high-risk uncovered areas

**With shadow-testing:**

```bash
> generate e2e tests and run shadow testing against production
```

The skill:

1. Generates full test suite
2. Configures shadow-testing with production mirror
3. Runs tests against both environments
4. Reports discrepancies

**With outside-in-testing methodology:**

The skill inherently follows outside-in testing:

- Starts from user-facing UI
- Tests through all layers (UI → API → DB)
- Validates end-to-end contract adherence
- No mocking (real integration)

### Custom Template Development

**Template Structure:**

```python
# e2e/templates/custom-template.py
CUSTOM_TEST_TEMPLATE = """
import {{ test, expect }} from '@playwright/test';
import {{ {helpers} }} from '../test-helpers/{helper_module}';

test.describe('{feature_name}', () => {{
  test.beforeEach(async ({{ page }}) => {{
    // Setup
    {setup_code}
  }});

  test('{test_description}', async ({{ page }}) => {{
    // Arrange
    {arrange_code}

    // Act
    {act_code}

    // Assert
    {assert_code}
  }});
}});
"""
```

**Using Custom Templates:**

```python
from e2e_outside_in_test_generator.template_manager import TemplateManager

template_manager = TemplateManager()
template_manager.register_template("custom-flow", CUSTOM_TEST_TEMPLATE)

test_code = template_manager.render("custom-flow", {
    "feature_name": "Payment Processing",
    "helpers": "login, checkout",
    "helper_module": "payment",
    "setup_code": "await setupPaymentGateway();",
    "arrange_code": "const cart = await createCart();",
    "act_code": "await processPayment(cart);",
    "assert_code": "await expect(page.getByText(/payment successful/i)).toBeVisible();"
})
```

### Advanced Locator Strategies

**Priority Hierarchy:**

1. **Role-based** (preferred): `getByRole('button', { name: /submit/i })`
2. **User-visible text**: `getByText(/welcome/i)`
3. **Test IDs**: `getByTestId('submit-button')`
4. **CSS selectors** (last resort): `locator('.submit-button')`

**Custom Locator Builders:**

```typescript
// e2e/test-helpers/locators.ts
export function findByDataAttribute(page: Page, attr: string, value: string) {
  return page.locator(`[data-${attr}="${value}"]`);
}

export function findByAriaLabel(page: Page, label: string) {
  return page.locator(`[aria-label*="${label}" i]`);
}

// Usage in tests
await findByDataAttribute(page, "action", "submit").click();
```

### Performance Optimization

**Test Execution Time:**

```typescript
// Group fast tests together
test.describe("Quick smoke tests", () => {
  test("homepage renders", async ({ page }) => {
    /* <1s */
  });
  test("navigation works", async ({ page }) => {
    /* <1s */
  });
});

// Isolate slow tests
test.describe("Full checkout flow @slow", () => {
  test("complete purchase", async ({ page }) => {
    /* 10s */
  });
});
```

**Run profiles:**

```json
// package.json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:quick": "playwright test --grep-invert @slow",
    "test:e2e:full": "playwright test",
    "test:e2e:smoke": "playwright test e2e/happy-path"
  }
}
```

### CI/CD Integration

**GitHub Actions:**

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### Troubleshooting

**Common Issues:**

1. **Flaky tests due to parallel execution**
   - **Cause**: `workers > 1` causes database race conditions
   - **Fix**: Ensure `workers: 1` in `playwright.config.ts`

2. **Locator timeouts**
   - **Cause**: Element not yet rendered
   - **Fix**: Add explicit waits: `await page.waitForLoadState('networkidle')`

3. **Test data conflicts**
   - **Cause**: Shared test database without cleanup
   - **Fix**: Use `test.beforeEach()` to reset database state

4. **Authentication failures**
   - **Cause**: Session timeout or incorrect credentials
   - **Fix**: Verify test credentials in `e2e/fixtures/users.json`

**Debug Commands:**

```bash
# Run single test in headed mode
npx playwright test e2e/happy-path/login.spec.ts --headed

# Run with debugger
npx playwright test --debug

# Generate trace for failing test
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Best Practices

1. **Keep workers at 1** - Never increase for deterministic test data
2. **Use role-based locators** - Most resilient to UI changes
3. **Small seed datasets** - 10-20 records max for predictability
4. **Explicit waits** - Avoid race conditions with `waitForLoadState()`
5. **Cleanup between tests** - Use `beforeEach` to reset state
6. **Test isolation** - Each test should run independently
7. **Meaningful assertions** - Test business logic, not implementation

### Success Metrics

After implementing this skill, you should achieve:

- **Test count**: 40+ tests (all 7 categories)
- **Pass rate**: 100% after fix loop
- **Execution time**: <2 minutes total
- **Bug detection**: ≥1 real bug found
- **Coverage**: ≥80% of routes and endpoints
- **Flakiness**: 0% (deterministic)
- **CI integration**: Green checks on every PR

---

**See also:**

- [README.md](./README.md) - Developer documentation
- [examples.md](./examples.md) - Usage examples
- [reference.md](./reference.md) - API reference
- [patterns.md](./patterns.md) - Common patterns
