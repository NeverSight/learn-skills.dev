---
name: playwright
description: >-
  End-to-end testing with Playwright for web applications. Use when writing E2E tests, browser
  automation, visual regression testing, or debugging test failures. Triggers on Playwright, E2E,
  browser testing, or test automation questions.
---

# Playwright E2E Testing

Playwright is a modern end-to-end testing framework that supports Chromium, Firefox, and WebKit.
It provides auto-wait, network interception, and powerful debugging tools.

## Core Concepts

### Project Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { open: 'never' }], ['list'], process.env.CI ? ['github'] : ['line']],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 14'] } },
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

### Basic Test Structure

```typescript
// e2e/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('has correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/My App/);
  });

  test('navigation works', async ({ page }) => {
    await page.getByRole('link', { name: 'About' }).click();
    await expect(page).toHaveURL('/about');
  });

  test('search functionality', async ({ page }) => {
    await page.getByPlaceholder('Search...').fill('test query');
    await page.getByRole('button', { name: 'Search' }).click();
    await expect(page.getByTestId('results')).toBeVisible();
  });
});
```

## Locator Strategies

### Best Practices (Priority Order)

```typescript
// 1. Role-based (best accessibility)
page.getByRole('button', { name: 'Submit' });
page.getByRole('heading', { level: 1 });
page.getByRole('link', { name: /learn more/i });

// 2. Label-based (forms)
page.getByLabel('Email');
page.getByPlaceholder('Enter your email');

// 3. Text-based (visible text)
page.getByText('Welcome');
page.getByText(/sign up/i);

// 4. Test ID (when others don't work)
page.getByTestId('user-avatar');

// 5. CSS/XPath (last resort)
page.locator('.card:has-text("Featured")');
page.locator('//button[contains(@class, "primary")]');
```

### Filtering Locators

```typescript
// Filter by text
page.getByRole('listitem').filter({ hasText: 'Product' });

// Filter by another locator
page.getByRole('listitem').filter({
  has: page.getByRole('button', { name: 'Buy' }),
});

// Chain locators
page.getByRole('article').getByRole('button');

// Nth element
page.getByRole('listitem').nth(2);
page.getByRole('listitem').first();
page.getByRole('listitem').last();
```

## Actions & Assertions

### Common Actions

```typescript
// Click
await page.getByRole('button').click();
await page.getByRole('button').dblclick();
await page.getByRole('button').click({ button: 'right' });

// Type
await page.getByLabel('Email').fill('user@example.com');
await page.getByLabel('Email').pressSequentially('user@example.com');
await page.keyboard.press('Enter');

// Select
await page.getByLabel('Country').selectOption('USA');
await page.getByLabel('Colors').selectOption(['red', 'blue']);

// Checkbox/Radio
await page.getByLabel('Agree').check();
await page.getByLabel('Agree').uncheck();

// Upload
await page.getByLabel('Upload').setInputFiles('file.pdf');
await page.getByLabel('Upload').setInputFiles(['file1.pdf', 'file2.pdf']);

// Drag and drop
await page.locator('#source').dragTo(page.locator('#target'));
```

### Assertions

```typescript
// Element state
await expect(locator).toBeVisible();
await expect(locator).toBeHidden();
await expect(locator).toBeEnabled();
await expect(locator).toBeDisabled();
await expect(locator).toBeChecked();
await expect(locator).toBeFocused();

// Content
await expect(locator).toHaveText('Hello');
await expect(locator).toContainText('Hello');
await expect(locator).toHaveValue('input value');
await expect(locator).toHaveAttribute('href', '/about');
await expect(locator).toHaveClass(/active/);
await expect(locator).toHaveCSS('color', 'rgb(0, 0, 0)');

// Page
await expect(page).toHaveTitle(/Home/);
await expect(page).toHaveURL('/dashboard');

// Count
await expect(locator).toHaveCount(3);

// Screenshot comparison
await expect(page).toHaveScreenshot('homepage.png');
await expect(locator).toHaveScreenshot('button.png');
```

## Page Object Model

```typescript
// e2e/pages/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toHaveText(message);
  }
}

// e2e/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';

test('successful login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

## Fixtures

```typescript
// e2e/fixtures.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';

type Fixtures = {
  loginPage: LoginPage;
  authenticatedPage: void;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Set auth cookies
    await page
      .context()
      .addCookies([{ name: 'session', value: 'test-session', domain: 'localhost', path: '/' }]);
    await use();
  },
});

export { expect };

// Usage
test('authenticated test', async ({ page, authenticatedPage }) => {
  await page.goto('/dashboard');
  await expect(page.getByText('Welcome')).toBeVisible();
});
```

## API Testing

```typescript
import { test, expect } from '@playwright/test';

test.describe('API Tests', () => {
  test('GET users', async ({ request }) => {
    const response = await request.get('/api/users');
    expect(response.ok()).toBeTruthy();

    const users = await response.json();
    expect(users).toHaveLength(3);
  });

  test('POST create user', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: { name: 'John', email: 'john@example.com' },
    });
    expect(response.status()).toBe(201);
  });
});
```

## Network Interception

```typescript
test('mock API response', async ({ page }) => {
  await page.route('/api/users', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([{ id: 1, name: 'Mocked User' }]),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('Mocked User')).toBeVisible();
});

test('intercept and modify', async ({ page }) => {
  await page.route('/api/**', async (route) => {
    const response = await route.fetch();
    const json = await response.json();
    json.modified = true;
    await route.fulfill({ response, json });
  });
});
```

## Visual Regression Testing

```typescript
test('visual comparison', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    maxDiffPixelRatio: 0.01,
  });

  // Component screenshot
  const card = page.getByTestId('feature-card');
  await expect(card).toHaveScreenshot('feature-card.png');
});
```

## Debugging

```bash
# Run in headed mode
npx playwright test --headed

# Run with UI mode
npx playwright test --ui

# Debug specific test
npx playwright test --debug

# Show HTML report
npx playwright show-report
```

## Best Practices

1. **Use role-based locators** for accessibility and stability
2. **Page Object Model** for maintainable tests
3. **Fixtures** for shared setup and authentication
4. **Auto-wait** - avoid explicit waits when possible
5. **Isolate tests** - each test should be independent
6. **CI parallelization** - run tests in parallel for speed

## References

- [references/selectors.md](references/selectors.md) - Selector patterns
- [references/fixtures.md](references/fixtures.md) - Fixtures and setup
