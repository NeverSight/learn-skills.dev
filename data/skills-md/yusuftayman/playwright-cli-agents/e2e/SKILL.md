---
name: e2e
description: E2E test generation skill using Playwright CLI with Page Object Model pattern and visual regression testing via @visual tag.
---

# E2E Test Generator Skill

This skill generates E2E tests using **playwright-cli** commands for browser automation. It uses the **Page Object Model** pattern and supports **visual regression testing** with the `@visual` tag in test titles.

## When to Use

Use this skill when:
- The user provides a URL to explore and create tests for
- You need to create new E2E tests for a web application
- You want to generate Page Object classes for a website
- Visual regression tests are needed (integrated with integration tests using `@visual` tag)

## Prerequisites

- **playwright-cli** installed globally (`npm install -g @playwright/cli@latest`)
- Target URL must be accessible
- Project should have Playwright configured

---

## Workflow Overview

```
1. EXPLORE → Navigate to URL, take snapshot, understand the page structure
2. PLAN → Identify testable features and create test plan
3. GENERATE PAGES → Create Page Object classes
4. GENERATE TESTS → Create test specs (add @visual tag for visual checks)
5. VALIDATE → Run tests to ensure they pass
```

---

## References

For detailed exploration techniques and CLI commands, see:
- **[references/component-exploration.md](references/component-exploration.md)** - How to explore UI components, CLI browser commands, locator strategies
- **[references/api-mocking.md](references/api-mocking.md)** - How to mock API responses using `mockApi` utility for deterministic tests

## Examples

For code templates and patterns, see:
- **[examples/page-object-model.md](examples/page-object-model.md)** - Page Object class templates and helper patterns
- **[examples/e2e-tests.md](examples/e2e-tests.md)** - Integration test templates with `@visual` tag for visual testing

---

## Quick Start Workflow

### Phase 1: URL Exploration

1. **Open URL**
   ```bash
   playwright-cli open https://example.com
   ```

2. **Take Page Snapshot**
   ```bash
   playwright-cli snapshot
   ```

3. **Identify Interactive Elements** from snapshot output:
   - Buttons, links, form inputs
   - Navigation elements
   - Modal triggers
   - Dropdown menus

4. **Test Interactions** before generating code:
   ```bash
   playwright-cli click e12
   playwright-cli snapshot  # Verify result
   ```

### Phase 2: Test Planning

Based on exploration, identify:

1. **Happy Path Tests** - Core user workflows
2. **Edge Cases** - Error states, boundary conditions
3. **Visual Tests** - UI consistency checks (add `@visual` tag to test title when needed)

### Phase 3: Generate Page Objects

See [examples/page-object-model.md](examples/page-object-model.md) for templates.

Key rules:
- All locators as `readonly` class properties
- Initialize locators in constructor
- Every interaction method has `waitFor` before action
- Use `.catch(() => false)` for visibility checks

### Phase 4: Generate Tests

See [examples/e2e-tests.md](examples/e2e-tests.md) for templates.

Key patterns:
- Add `@visual` tag to test title for visual regression tests (e.g., `'should display page correctly @visual'`)
- Follow AAA pattern (Arrange, Act, Assert)
- Create constants for reusable test data
- All logic in Page Objects (no separate helpers or fixtures)

---

## Test File Structure

```
__tests__/
├── e2e/
│   ├── pages/           # Page Object classes (ALL locators & interaction logic)
│   │   └── [page-name]-page.ts
│   └── [feature].spec.ts  # Integration tests (include @visual tag for visual checks)
└── constants/           # Test data only (URLs, emails, text values)
    └── test-data.ts
```

**Important Notes:**
- **All locators in Page Objects** - No separate selectors file, locators are defined as class properties
- **No helpers folder** - All interaction methods belong in Page Object classes
- **No fixtures folder** - Use standard Playwright test setup
- **No visual folder** - Visual tests are integrated with integration tests using `@visual` tag

---

## Visual Testing Best Practices

### ALWAYS Prefer Component-Level Screenshots

**Never use full-page screenshots.** Component-level screenshots are more stable and focused:

```typescript
// CORRECT - Component-level screenshot
await expect(featurePage.header).toHaveScreenshot('preview-mode-header.png');
await expect(featurePage.globalStylesPanel).toHaveScreenshot('styles-expanded.png');

// WRONG - Full-page screenshot (too fragile)
await expect(page).toHaveScreenshot('preview-mode.png');
```

### Why Component-Level Screenshots?

| Full Page | Component |
|-----------|-----------|
| Fails when ANY element changes | Only fails when the specific component changes |
| Large image files | Small, focused images |
| Hard to diagnose failures | Easy to see what changed |
| Flaky due to animations | Stable, isolated scope |

### Strict Pixel Comparison

In `playwright.config.ts`, use strict comparison (no tolerance):

```typescript
expect: {
  toHaveScreenshot: {
    maxDiffPixels: 0, // Strict - no pixel difference allowed
  },
},
```

### Add Component Locators to Page Objects

```typescript
// In your Page Object class constructor
this.header = page.locator('.guido__header, header').first();
this.globalStylesPanel = page.getByRole('tabpanel', { name: 'General Styles' });
this.leftSidebar = page.locator('.left-sidebar, [class*="sidebar"]').first();
```

### Screenshot Naming Convention

Use descriptive names that indicate the component and state:

```typescript
// Good names
await expect(featurePage.header).toHaveScreenshot('header-preview-mode.png');
await expect(featurePage.globalStylesPanel).toHaveScreenshot('styles-mobile-view.png');

// Bad names (too generic)
await expect(element).toHaveScreenshot('test1.png');
```

---

## API Mocking

For deterministic tests, mock API responses using the `mockApi` utility:

```typescript
import { API_ENDPOINTS } from '../enums/constants';
import { mockApi } from '../mockServer';

test('displays empty state @visual', async ({ page }) => {
  // Setup mocks BEFORE navigation
  await mockApi(page, `**/${API_ENDPOINTS.LIST_DATA}**`, 'list-data/empty.json');

  const featurePage = new FeaturePage(page);
  await featurePage.goto('/page');
  await expect(featurePage.emptyState).toHaveScreenshot('empty-state.png');
});
```

See **[references/api-mocking.md](references/api-mocking.md)** for full documentation.

---

## Important Notes

- **Always explore first** - Use `playwright-cli snapshot` before writing any code
- **Mock APIs** - Use `mockApi` utility for deterministic test data
- **Test interactions** - Verify element refs work before generating Page Objects
- **Visual tests use `@visual` tag in title** - e.g., `'component visual test @visual'`
- **Use component-level screenshots** - NEVER use full-page screenshots
- **Strict pixel comparison** - Use `maxDiffPixels: 0` in config
- **Don't separate visual tests** - Integrate them with integration tests when needed
- **Follow existing patterns** - Match project structure exactly
- **Use descriptive names** - Test names should describe expected behavior
- **Keep Page Objects comprehensive** - Include wait methods, helper methods, and assertion helpers
- **Never use `page.waitForTimeout()`** - Use proper `waitFor` conditions instead

## Error Handling

| Error | Solution |
|-------|----------|
| Element not found | Take new snapshot, verify ref value |
| Timeout on navigation | Increase timeout or check URL |
| Screenshot mismatch | Update baseline with `--update-snapshots` |
| Network errors | Check console messages and network requests |

---

## GitHub Actions Workflow

Example CI/CD workflow for E2E tests with sharding and visual regression:

```yaml
name: E2E Tests

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  push:
    branches: [develop]
  workflow_dispatch:
    inputs:
      update_snapshots:
        description: 'Update snapshots only'
        required: false
        default: 'false'
        type: boolean

jobs:
  run-e2e-tests:
    if: github.event_name == 'workflow_dispatch' || github.event_name == 'pull_request' || github.event_name == 'push'
    timeout-minutes: 60
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    permissions:
      contents: read
      issues: write
      pull-requests: write
    env:
      APP_URL: https://localhost:3000
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Start dev server
        run: |
          npm run dev &
          npx wait-on ${{ env.APP_URL }}

      - name: Run E2E Tests
        run: |
          if [ "${{ inputs.update_snapshots }}" == "true" ]; then
            npx playwright test --grep @visual --update-snapshots --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }} --reporter=blob
          else
            npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }} --reporter=blob
          fi

      - name: Upload blob report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: blob-report-${{ github.run_id }}-${{ matrix.shardIndex }}
          path: blob-report/
          retention-days: 3

  merge-reports:
    if: always()
    needs: [run-e2e-tests]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Download blob reports
        uses: actions/download-artifact@v4
        with:
          path: all-blob-reports
          pattern: blob-report-${{ github.run_id }}-*
          merge-multiple: true

      - name: Merge reports
        run: npx playwright merge-reports --reporter html ./all-blob-reports

      - name: Upload HTML report
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### Key Workflow Features

| Feature | Description |
|---------|-------------|
| **Sharding** | Tests split across 4 parallel runners for speed |
| **Visual update** | `workflow_dispatch` with `update_snapshots` input to update baselines |
| **Blob reports** | Each shard uploads blob report for later merging |
| **Report merging** | Combined HTML report from all shards |
| **grep @visual** | Only visual tests updated when `update_snapshots` is true |
