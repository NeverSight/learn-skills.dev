---
name: e2e-testing
description: >-
  End-to-end testing patterns with Playwright for full-stack Python/React applications.
  Use when writing E2E tests for complete user workflows (login, CRUD, navigation),
  critical path regression tests, or cross-browser validation. Covers test structure,
  page object model, selector strategy (data-testid > role > label), wait strategies,
  auth state reuse, test data management, and CI integration. Does NOT cover unit tests
  or component tests (use pytest-patterns or react-testing-patterns).
license: MIT
compatibility: 'Playwright 1.40+, Node.js 20+'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: testing
allowed-tools: Read Edit Write Bash(npx:*) Bash(npm:*)
context: fork
---

# E2E Testing

## When to Use

Activate this skill when:
- Writing E2E tests for complete user workflows (login, CRUD operations, multi-page flows)
- Creating critical path regression tests that validate the full stack
- Testing cross-browser compatibility (Chromium, Firefox, WebKit)
- Validating authentication flows end-to-end
- Testing file upload/download workflows
- Writing smoke tests for deployment verification

Do NOT use this skill for:
- React component unit tests (use `react-testing-patterns`)
- Python backend unit/integration tests (use `pytest-patterns`)
- TDD workflow enforcement (use `tdd-workflow`)
- API contract testing without a browser (use `pytest-patterns` with httpx)

## Instructions

### Test Structure

```
e2e/
├── playwright.config.ts         # Global Playwright configuration
├── fixtures/
│   ├── auth.fixture.ts          # Authentication state setup
│   └── test-data.fixture.ts     # Test data creation/cleanup
├── pages/
│   ├── base.page.ts             # Base page object with shared methods
│   ├── login.page.ts            # Login page object
│   ├── users.page.ts            # Users list page object
│   └── user-detail.page.ts     # User detail page object
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── logout.spec.ts
│   ├── users/
│   │   ├── create-user.spec.ts
│   │   ├── edit-user.spec.ts
│   │   └── list-users.spec.ts
│   └── smoke/
│       └── critical-paths.spec.ts
└── utils/
    ├── api-helpers.ts           # Direct API calls for test setup
    └── test-constants.ts        # Shared constants
```

**Naming conventions:**
- Test files: `<feature>.spec.ts`
- Page objects: `<page-name>.page.ts`
- Fixtures: `<concern>.fixture.ts`
- Test names: human-readable sentences describing the user action and expected outcome

### Page Object Model

Every page gets a page object class that encapsulates selectors and actions. Tests never interact with selectors directly.

**Base page object:**
```typescript
// e2e/pages/base.page.ts
import { type Page, type Locator } from "@playwright/test";

export abstract class BasePage {
  constructor(protected readonly page: Page) {}

  /** Navigate to the page's URL. */
  abstract goto(): Promise<void>;

  /** Wait for the page to be fully loaded. */
  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState("networkidle");
  }

  /** Get a toast/notification message. */
  get toast(): Locator {
    return this.page.getByRole("alert");
  }

  /** Get the page heading. */
  get heading(): Locator {
    return this.page.getByRole("heading", { level: 1 });
  }
}
```

**Concrete page object:**
```typescript
// e2e/pages/users.page.ts
import { type Page, type Locator } from "@playwright/test";
import { BasePage } from "./base.page";

export class UsersPage extends BasePage {
  // ─── Locators ─────────────────────────────────────────
  readonly createButton: Locator;
  readonly searchInput: Locator;
  readonly userTable: Locator;

  constructor(page: Page) {
    super(page);
    this.createButton = page.getByTestId("create-user-btn");
    this.searchInput = page.getByRole("searchbox", { name: /search users/i });
    this.userTable = page.getByRole("table");
  }

  // ─── Actions ──────────────────────────────────────────
  async goto(): Promise<void> {
    await this.page.goto("/users");
    await this.waitForLoad();
  }

  async searchFor(query: string): Promise<void> {
    await this.searchInput.fill(query);
    // Wait for search results to update (debounced)
    await this.page.waitForResponse("**/api/v1/users?*");
  }

  async clickCreateUser(): Promise<void> {
    await this.createButton.click();
  }

  async getUserRow(email: string): Promise<Locator> {
    return this.userTable.getByRole("row").filter({ hasText: email });
  }

  async getUserCount(): Promise<number> {
    // Subtract 1 for header row
    return (await this.userTable.getByRole("row").count()) - 1;
  }
}
```

**Rules for page objects:**
- One page object per page or major UI section
- Locators are public readonly properties
- Actions are async methods
- Page objects never contain assertions -- tests assert
- Page objects handle waits internally after actions

### Selector Strategy

**Priority order (highest to lowest):**

| Priority | Selector | Example | When to Use |
|----------|----------|---------|-------------|
| 1 | `data-testid` | `getByTestId("submit-btn")` | Interactive elements, dynamic content |
| 2 | Role | `getByRole("button", { name: /save/i })` | Buttons, links, headings, inputs |
| 3 | Label | `getByLabel("Email")` | Form inputs with labels |
| 4 | Placeholder | `getByPlaceholder("Search...")` | Search inputs |
| 5 | Text | `getByText("Welcome back")` | Static text content |

**NEVER use:**
- CSS selectors (`.class-name`, `#id`) -- brittle, break on styling changes
- XPath (`//div[@class="foo"]`) -- unreadable, extremely brittle
- DOM structure selectors (`div > span:nth-child(2)`) -- break on layout changes

**Adding data-testid attributes:**
```tsx
// In React components -- add data-testid to interactive elements
<button data-testid="create-user-btn" onClick={handleCreate}>
  Create User
</button>

// Convention: kebab-case, descriptive
// Pattern: <action>-<entity>-<element-type>
// Examples: create-user-btn, user-email-input, delete-confirm-dialog
```

### Wait Strategies

**NEVER use hardcoded waits:**
```typescript
// BAD: Hardcoded wait -- flaky, slow
await page.waitForTimeout(3000);

// BAD: Sleep
await new Promise((resolve) => setTimeout(resolve, 2000));
```

**Use explicit wait conditions:**
```typescript
// GOOD: Wait for a specific element to appear
await page.getByRole("heading", { name: "Dashboard" }).waitFor();

// GOOD: Wait for navigation
await page.waitForURL("/dashboard");

// GOOD: Wait for API response
await page.waitForResponse(
  (response) =>
    response.url().includes("/api/v1/users") && response.status() === 200,
);

// GOOD: Wait for network to settle
await page.waitForLoadState("networkidle");

// GOOD: Wait for element state
await page.getByTestId("submit-btn").waitFor({ state: "visible" });
await page.getByTestId("loading-spinner").waitFor({ state: "hidden" });
```

**Auto-waiting:** Playwright auto-waits for elements to be actionable before clicking, filling, etc. Explicit waits are needed only for assertions or complex state transitions.

### Auth State Reuse

Avoid logging in before every test. Save auth state and reuse it.

**Setup auth state once:**
```typescript
// e2e/fixtures/auth.fixture.ts
import { test as base } from "@playwright/test";
import path from "path";

const AUTH_STATE_PATH = path.resolve("e2e/.auth/user.json");

export const setup = base.extend({});

setup("authenticate", async ({ page }) => {
  // Perform real login
  await page.goto("/login");
  await page.getByLabel("Email").fill("testuser@example.com");
  await page.getByLabel("Password").fill("TestPassword123!");
  await page.getByRole("button", { name: /sign in/i }).click();

  // Wait for auth to complete
  await page.waitForURL("/dashboard");

  // Save signed-in state
  await page.context().storageState({ path: AUTH_STATE_PATH });
});
```

**Reuse in tests:**
```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // Setup project runs first and saves auth state
    { name: "setup", testDir: "./e2e/fixtures", testMatch: "auth.fixture.ts" },
    {
      name: "chromium",
      use: {
        storageState: "e2e/.auth/user.json",  // Reuse auth state
      },
      dependencies: ["setup"],
    },
  ],
});
```

### Test Data Management

**Principles:**
- Tests create their own data (never depend on pre-existing data)
- Tests clean up after themselves (or use API to reset)
- Use API calls for setup, not UI interactions (faster, more reliable)

**API helpers for test data:**
```typescript
// e2e/utils/api-helpers.ts
import { type APIRequestContext } from "@playwright/test";

export class TestDataAPI {
  constructor(private request: APIRequestContext) {}

  async createUser(data: { email: string; displayName: string }) {
    const response = await this.request.post("/api/v1/users", { data });
    return response.json();
  }

  async deleteUser(userId: number) {
    await this.request.delete(`/api/v1/users/${userId}`);
  }

  async createOrder(userId: number, items: Array<Record<string, unknown>>) {
    const response = await this.request.post("/api/v1/orders", {
      data: { user_id: userId, items },
    });
    return response.json();
  }
}
```

**Usage in tests:**
```typescript
test("edit user name", async ({ page, request }) => {
  const api = new TestDataAPI(request);

  // Setup: create user via API (fast)
  const user = await api.createUser({
    email: "edit-test@example.com",
    displayName: "Before Edit",
  });

  try {
    // Test: edit via UI
    const usersPage = new UsersPage(page);
    await usersPage.goto();
    // ... perform edit via UI ...
  } finally {
    // Cleanup: remove test data
    await api.deleteUser(user.id);
  }
});
```

### Debugging Flaky Tests

**1. Use trace viewer for failures:**
```typescript
// playwright.config.ts
use: {
  trace: "on-first-retry",  // Capture trace only on retry
}
```

View trace: `npx playwright show-trace trace.zip`

**2. Run in headed mode for debugging:**
```bash
npx playwright test --headed --debug tests/users/create-user.spec.ts
```

**3. Common causes of flaky tests:**
| Cause | Fix |
|-------|-----|
| Hardcoded waits | Use explicit wait conditions |
| Shared test data | Each test creates its own data |
| Animation interference | Set `animations: "disabled"` in config |
| Race conditions | Wait for API responses before assertions |
| Viewport-dependent behavior | Set explicit viewport in config |
| Session leaks between tests | Use `storageState` correctly, clear cookies |

**4. Retry strategy:**
```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,  // Retry in CI only
});
```

### CI Configuration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Start application
        run: |
          docker compose up -d
          npx wait-on http://localhost:3000 --timeout 60000

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14

      - name: Upload traces on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-traces
          path: test-results/
```

Use `scripts/run-e2e-with-report.sh` to run Playwright with HTML report output locally.

## Examples

See `references/page-object-template.ts` for annotated page object class.
See `references/e2e-test-template.ts` for annotated E2E test.
See `references/playwright-config-example.ts` for production Playwright config.
