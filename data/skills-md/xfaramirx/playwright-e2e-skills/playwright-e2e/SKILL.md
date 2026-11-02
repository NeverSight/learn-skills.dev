---
name: playwright-e2e
description: "Generate A+ production-ready Playwright E2E tests with Page Object Model, zero hard waits, and complete documentation. **Use this skill whenever the user mentions**: 'test', 'e2e', 'end-to-end', 'playwright', 'accessibility', 'a11y', 'smoke test', 'API test', 'test automation', 'test suite', 'create tests', 'add tests', 'test this', 'test the', 'write tests', or wants to test any web application feature, page, component, or API endpoint. Also use for canvas testing, complex UI interactions (drag-drop, drawing, animations), or when user wants tests with proper Page Object Model architecture."
license: MIT
metadata:
  author: XFaramirX
  version: "1.2.0"
---

# Playwright E2E Testing Framework

Generates production-ready Playwright test suites with **A+ quality standards**: zero `waitForTimeout()`, proper assertions, constants management, and complete documentation. Built on Page Object Model architecture with accessibility testing, API validation, and multi-environment support.

## Quick Start

```
"Create E2E tests for the login feature"
"Add accessibility tests for the homepage"
"Generate API tests for the user service with schema validation"
"Create smoke tests with @smoke tags for critical flows"
"Test the canvas drawing functionality"
```

## How It Works

```
Your Request → Analyze Requirements → Generate Files → A+ Quality Assurance
                    ↓                        ↓                    ↓
            • Test patterns          • Spec files         • Zero hard waits
            • Page objects           • Page objects       • Action verification
            • Constants needs        • constants.ts       • Smart a11y filtering
                                     • Fixtures           • Force click docs
                                     • Selectors          • Constants usage
```

## What You Get

| Output | Includes | Quality |
|--------|----------|---------|
| **Spec File** | Tests with `test.describe()`, `test.step()`, proper tags | A+ |
| **Page Object** | Methods, BasePage inheritance, action verification | A+ |
| **Selectors** | Centralized, accessible (`getByRole`, `aria-label`) | A+ |
| **Constants** | All magic numbers extracted to `constants.ts` | A+ |
| **Fixtures** | Custom page injection, type-safe | A+ |
| **README** | Usage instructions, examples | Complete |

**Quality Guarantee:** Zero anti-patterns, production-ready code.

---

## Core Principles (A+ Standards)

### 1. Zero Hard Waits (CRITICAL)

**Never use `page.waitForTimeout()`**. Playwright has built-in auto-waiting.

```typescript
// ❌ NEVER
await page.click('button');
await page.waitForTimeout(500);

// ✅ ALWAYS - Auto-retrying assertion
await page.click('button');
await expect(page.locator('.result')).toBeVisible();
```

### 2. Constants Management (Required)

Extract all magic numbers to `constants.ts`:

```typescript
// pages/feature/constants.ts
export const CANVAS_COORDINATES = { center: { x: 400, y: 300 } };
export const SHAPE_SIZES = { small: 50, medium: 100, large: 150 };
```

### 3. Action Verification (Required)

Always verify actions succeeded:

```typescript
async selectTool(tool: string): Promise<void> {
    await this.page.locator(toolSelector).click();
    await expect(this.page.locator(toolSelector)).toBeChecked(); // ✅ Verify
}
```

### 4. Force Clicks (Document Exception)

Use `force: true` only when necessary, always document WHY:

```typescript
// Note: force: true is necessary because [App]'s radio buttons have SVG elements
// that intercept pointer events. This is a valid use case.
await this.page.locator(toolSelector).click({ force: true });
await expect(this.page.locator(toolSelector)).toBeChecked(); // Always verify!
```

### 5. Smart A11y Testing

Filter known third-party violations, focus on testable areas:

```typescript
const criticalViolations = violations.filter((v: any) => 
    v.impact === 'critical' && v.id !== 'known-third-party-issue'
);
expect(criticalViolations, 'No critical violations').toHaveLength(0);
```

---

## Test Structure Templates

### E2E Test

```typescript
import { test, expect } from '../../fixtures/base';
import config from '../../../playwright.config';

test.describe('Feature Name', { tag: ['@smoke'] }, () => {
    test.beforeEach(async ({ featurePage }) => {
        await featurePage.goto(config.baseUrl);
    });

    test('Feature - Specific behavior', async ({ featurePage, page }) => {
        await test.step('Clear action description', async () => {
            await featurePage.performAction();
            await expect(page.getByRole('button')).toBeVisible();
        });
    });
});
```

### API Test

```typescript
test.describe('API - Service', { tag: ['@api'] }, () => {
    test('API - Create and retrieve', async ({ apiClient }) => {
        const response = await apiClient.createResource(data);
        expect(response.status).toBe(201);
        
        const validated = Schema.parse(response.data); // Zod validation
        expect(validated.id).toBeDefined();
    });
});
```

### Accessibility Test

```typescript
test('A11y - Page compliance', async ({ homePage }, testInfo) => {
    const violations = await homePage.checkA11y();
    
    await testInfo.attach('a11y-results', {
        body: JSON.stringify(violations, null, 2),
        contentType: 'application/json'
    });
    
    // Filter known third-party issues
    const criticalViolations = violations.filter((v: any) => 
        v.impact === 'critical' && v.id !== 'button-name'
    );
    
    expect(criticalViolations).toHaveLength(0);
});
```

---

## Page Object Model Structure

```
e2e/
├── fixtures/
│   └── base.ts              # Fixture registration
├── pages/
│   └── feature/
│       ├── feature.page.ts  # Page object class
│       ├── selectors.ts     # Centralized selectors
│       └── constants.ts     # Configuration values
└── specs/
    └── feature/
        ├── feature.spec.ts  # Test specifications
        └── README.md        # Documentation
```

**BasePage Methods Available:**
- `goto(url)` - Navigate with load wait
- `checkA11y()` - Run accessibility scan
- `takeQuerySnapshot(selector, name)` - Visual regression
- `getTrimmedText(locator)` - Get cleaned text
- `hoverAndClick(locator)` - Hover then click

---

## Anti-Patterns (Never Do These)

| ❌ Never | ✅ Instead | Why |
|----------|-----------|-----|
| `waitForTimeout()` | Auto-retrying assertions | Brittle, slow, violates guidelines |
| Magic numbers | Constants file | Maintainability |
| No verification | Assert after actions | Catch failures early |
| Force without docs | Document rationale | Future maintainers |
| Broken assertions | Ensure can fail | `expect(array).toBeTruthy()` always passes |

---

## Commands

```bash
# Run tests
npm run test                 # All tests
npm run test:smoke          # Smoke tests only
npm run test:ui             # UI mode

# Environment-specific
TEST_ENV=stage npm run test
TEST_ENV=prod npm run test

# Debug
PWDEBUG=1 npx playwright test
```

---

## A+ Quality Checklist

When generating tests, ensure:

**Architecture:**
- [ ] Page Object Model with BasePage inheritance
- [ ] Selectors in `selectors.ts`
- [ ] Constants in `constants.ts`
- [ ] Custom fixtures integrated

**Waiting & Timing:**
- [ ] **ZERO `waitForTimeout()` calls**
- [ ] All assertions use `await`
- [ ] Trust Playwright auto-waiting

**Assertions:**
- [ ] All assertions can fail (not always truthy)
- [ ] Action verification after clicks/fills/navigations
- [ ] Meaningful assertion messages

**Code Quality:**
- [ ] No magic numbers - all in constants
- [ ] Force clicks documented with rationale
- [ ] TypeScript types properly used

**Locators:**
- [ ] Prefer `getByRole()`, `getByLabel()`, `getByText()`
- [ ] No strict mode violations
- [ ] Avoid brittle CSS class selectors

---

## Grade Thresholds

| Grade | Score | Key Characteristics |
|-------|-------|-------------------|
| **A+** | 95-100 | Zero anti-patterns, exemplary |
| **A** | 90-94 | Solid, minor improvements possible |
| **B+** | 85-89 | Good, some anti-patterns present |

**Grade Blockers:**
- Hard waits (`waitForTimeout`): caps at B+
- Magic numbers: caps at B+
- Broken assertions: caps at B
- Force clicks without docs: -3 to -5 points
- No action verification: -1 to -2 points each

---

## Framework Features

### Tag-Based Execution

```typescript
test.describe('Feature', { tag: ['@smoke'] }, () => {
    // Critical path tests
});
```

```bash
npx playwright test --grep @smoke
npx playwright test --grep @a11y
```

### Multi-Environment Support

```bash
TEST_ENV=dev npm run test    # Development
TEST_ENV=stage npm run test  # Staging
TEST_ENV=prod npm run test   # Production
```

### API Testing with Zod

```typescript
import { z } from 'zod';

const UserSchema = z.object({
    id: z.number(),
    email: z.string().email(),
    name: z.string()
});

const user = UserSchema.parse(response.data); // Validates and types
```

### Visual Regression

```typescript
await homePage.takeQuerySnapshot("body", "homepage");
await homePage.takeQuerySnapshot(".nav", "navigation");
```

---

## Additional Resources

**For detailed patterns and examples, read these reference files:**

- **`references/advanced-patterns.md`** - Constants management, force clicks, canvas testing, no hard waits policy
- **`references/case-study.md`** - Real B+ to A+ transformation (11-point improvement)
- **`references/examples.md`** - Complete working examples for login, API, a11y, visual tests
- **`references/troubleshooting.md`** - Common issues and solutions

**When to read references:**
- Need force click pattern → `advanced-patterns.md`
- Canvas/complex UI testing → `advanced-patterns.md`
- Want to see full transformation → `case-study.md`
- Need complete test examples → `examples.md`
- Encountering errors/flaky tests → `troubleshooting.md`

---

## CI/CD Integration

```yaml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run smoke tests
  run: npm run test:smoke
  env:
    TEST_ENV: stage

- name: Upload report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

**Retry Strategy:**
```typescript
retries: process.env.CI ? 2 : 0
workers: process.env.CI ? 1 : undefined
```

---

## Key Reminders

1. **Trust Playwright's auto-waiting** - No hard waits needed
2. **Extract to constants** - All magic numbers
3. **Verify every action** - Assert state changed
4. **Document exceptions** - Force clicks need explanation
5. **Test assertions** - Ensure they can fail
6. **Use references** - Detailed guidance available

---

**"Hard waits in Playwright tests are like GOTO statements in code - technically possible, but always a red flag."** - Playwright Best Practices

**"Quality is never an accident; it is always the result of intelligent effort."** - John Ruskin
