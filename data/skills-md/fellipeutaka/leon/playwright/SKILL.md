---
name: playwright
description: >
  Write, debug, and maintain Playwright end-to-end tests for web applications. Use when working with
  Playwright test files, configuring playwright.config.ts, writing browser automation, debugging flaky
  E2E tests, setting up authentication for tests, API mocking/interception, visual regression testing,
  accessibility testing, or CI/CD integration for browser tests. Triggers: Playwright, E2E test,
  end-to-end, browser test, @playwright/test, playwright.config, page object model, test fixture,
  visual snapshot, trace viewer.
---

# Playwright

## Core Workflow

1. **Analyze** - Identify user flows and test scope
2. **Configure** - Set up `playwright.config.ts` (see [references/configuration.md](references/configuration.md))
3. **Write tests** - Use proper locators, auto-waiting, and assertions
4. **Organize** - Apply fixtures, POM, parallelism (see [references/test-organization.md](references/test-organization.md))
5. **Debug** - Use traces, UI mode (see [references/debugging.md](references/debugging.md))

## Reference Guide

Load based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Locators & Actions | [references/locators-and-actions.md](references/locators-and-actions.md) | Writing selectors, filling forms, clicking, drag-and-drop |
| Test Organization | [references/test-organization.md](references/test-organization.md) | Fixtures, parallel execution, retries, sharding, timeouts, annotations |
| Authentication | [references/authentication.md](references/authentication.md) | Login flows, multi-role tests, storageState |
| Network & Mocking | [references/network-and-mocking.md](references/network-and-mocking.md) | API mocking, route interception, HAR recording, API testing |
| Visual Testing | [references/visual-testing.md](references/visual-testing.md) | Screenshots, snapshots, ARIA snapshots, visual regression |
| Debugging | [references/debugging.md](references/debugging.md) | Flaky tests, trace viewer, UI mode, debug flags |
| Configuration | [references/configuration.md](references/configuration.md) | playwright.config.ts, projects, web server, CI/CD, reporters |
| Advanced | [references/advanced.md](references/advanced.md) | Clock mocking, evaluate, component testing, POM, accessibility |

## Critical Rules

### MUST DO
- Use `getByRole()` > `getByLabel()` > `getByTestId()` > `getByText()` (in priority order)
- Use web-first assertions: `await expect(locator).toBeVisible()` (auto-retries)
- Keep tests independent - no shared mutable state between tests
- Enable `trace: 'on-first-retry'` for debugging failures
- Use `fullyParallel: true` for speed
- Use `forbidOnly: !!process.env.CI` to prevent `.only` leaking to CI

### MUST NOT
- Use `waitForTimeout()` — always use proper auto-waiting assertions
- Use CSS class selectors — they break on refactors
- Use `expect(await locator.isVisible()).toBe(true)` — this does NOT auto-retry; use `await expect(locator).toBeVisible()` instead
- Share state between tests (each test gets a fresh `BrowserContext`)
- Use `first()`/`nth()` without narrowing first — filter or chain locators instead

## Common Gotchas

1. **Assertion retrying**: Only `expect(locator)` retries. `expect(await locator.something())` evaluates once.
2. **`has-text` pseudo-class**: Without another CSS specifier, matches everything including `<body>`. Always combine with an element selector.
3. **`getByText` whitespace**: Always normalizes whitespace, even with `exact: true`.
4. **`opacity: 0`**: Considered visible. Zero-size elements are NOT visible.
5. **Shadow DOM**: All locators pierce Shadow DOM by default EXCEPT XPath.
6. **`fill()` actionability**: Checks Visible + Enabled + Editable only. Does NOT check Stable or Receives Events.
7. **`press()`/`pressSequentially()`**: NO actionability checks at all.
8. **Dialogs**: Listener MUST handle (accept/dismiss) the dialog or the page action will stall permanently.
9. **`storageState`**: Covers cookies, localStorage, IndexedDB. Does NOT cover sessionStorage.
10. **TypeScript**: Playwright does NOT type-check — it only transpiles. Run `tsc` separately.
11. **`expect.toPass` timeout**: Defaults to `0` (no retry), NOT the expect timeout.
12. **Glob patterns**: `*` does not match `/`. `**` matches everything. `?` matches literal `?` only.
13. **Serial mode retries**: Retries ALL tests in the group, not just the failed one.
14. **Worker shutdown**: Worker processes are always killed after a test failure.
15. **Drag events**: For `dragover` to fire in all browsers, issue TWO `mouse.move()` calls.
16. **Videos**: Only available AFTER page/context is closed.

## Quick Setup

```bash
# New project
npm init playwright@latest

# Existing project
npm i -D @playwright/test
npx playwright install
```

### Minimal Config

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Minimal Test

```typescript
import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/My App/);
  await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
});
```

## CLI Quick Reference

```bash
npx playwright test                          # Run all
npx playwright test auth.spec.ts             # Run file
npx playwright test --grep @smoke            # Run tagged
npx playwright test --project=chromium       # Single browser
npx playwright test --debug                  # Debug mode (headed, timeout=0, workers=1)
npx playwright test --ui                     # UI mode
npx playwright show-report                   # HTML report
npx playwright show-trace trace.zip          # View trace
npx playwright codegen localhost:3000        # Generate tests
```
