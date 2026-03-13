---
name: playwright-flow-recorder
description: Creates Playwright test scripts from natural language user flow descriptions. This skill should be used when generating E2E tests from scenarios, converting user stories to test code, recording user flows, creating test scripts from descriptions like "user signs up and creates project", or translating acceptance criteria into executable tests. Trigger terms include playwright test, e2e flow, user scenario, test from description, record flow, user journey, test script generation, acceptance test, behavior test, user story test.
---

# Playwright Flow Recorder

Generate Playwright test scripts from natural language scenario descriptions.

## Overview

To create E2E tests from user flow descriptions, this skill translates natural language scenarios into executable Playwright test code with proper assertions, error handling, and best practices.

## When to Use

Use this skill when:
- Converting user stories to E2E tests
- Generating tests from acceptance criteria
- Creating test scripts from flow descriptions
- Translating business requirements into tests
- Documenting user journeys as executable tests
- Building test coverage for critical user paths

## Flow Description Format

### Simple Flow

```
User signs up with email and password
```

### Detailed Flow

```
1. User navigates to signup page
2. User fills in email field
3. User fills in password field
4. User clicks signup button
5. User sees success message
6. User is redirected to dashboard
```

### Acceptance Criteria Format

```
Given: User is on the homepage
When: User clicks "Get Started"
And: User fills in registration form
And: User submits the form
Then: User sees "Welcome" message
And: User is on the dashboard page
```

## Generation Process

### 1. Parse Flow Description

To analyze the scenario, use `scripts/parse_flow.py`:

```bash
python scripts/parse_flow.py --input "user creates entity and adds relationships"
```

The script identifies:
- Actions (navigate, click, fill, select, etc.)
- Elements (buttons, inputs, links, etc.)
- Assertions (sees, redirected, displays, etc.)
- Data inputs (form values, selections, etc.)

### 2. Map to Playwright Actions

To convert parsed steps to Playwright code, use the action mapping:

**Navigation:**
- "navigates to X" → `await page.goto('/x')`
- "clicks X" → `await page.getByRole('button', { name: /x/i }).click()`
- "selects X from Y" → `await page.getByLabel(/y/i).selectOption('x')`

**Form Input:**
- "fills X with Y" → `await page.getByLabel(/x/i).fill('y')`
- "enters X" → `await page.getByLabel(/x/i).fill('x')`
- "types X" → `await page.getByLabel(/x/i).type('x')`

**Assertions:**
- "sees X" → `await expect(page.getByText(/x/i)).toBeVisible()`
- "is redirected to X" → `await expect(page).toHaveURL(/x/)`
- "X displays Y" → `await expect(page.getByRole('x')).toContainText(/y/i)`

### 3. Generate Test Structure

To create the test file, use the template from `assets/test-template.ts`:

```typescript
import { test, expect } from '@playwright/test'

test.describe('Flow Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup steps
  })

  test('scenario description', async ({ page }) => {
    // Test steps
  })

  test.afterEach(async ({ page }) => {
    // Cleanup steps
  })
})
```

### 4. Add Assertions and Waits

To ensure test reliability, add:
- Explicit waits for dynamic content
- Assertions after state changes
- Error state checks
- Loading state handling

### 5. Generate Data Fixtures

To create test data, use `scripts/generate_fixtures.py`:

```bash
python scripts/generate_fixtures.py --entity character --count 5
```

## Usage Examples

### Example 1: User Signup Flow

**Input Description:**
```
User signs up with email and password, then creates their first project
```

**Generated Test:**
```typescript
import { test, expect } from '@playwright/test'

test.describe('User Signup and Project Creation', () => {
  test('user signs up and creates first project', async ({ page }) => {
    // Navigate to signup page
    await page.goto('/signup')

    // Fill in signup form
    await page.getByLabel(/email/i).fill('user@example.com')
    await page.getByLabel(/password/i).fill('SecurePass123!')
    await page.getByLabel(/confirm password/i).fill('SecurePass123!')

    // Submit signup
    await page.getByRole('button', { name: /sign up/i }).click()

    // Verify success message
    await expect(page.getByText(/welcome|success/i)).toBeVisible()

    // Verify redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard/)

    // Create first project
    await page.getByRole('button', { name: /create project/i }).click()

    // Fill project form
    await page.getByLabel(/project name/i).fill('My First World')
    await page.getByLabel(/description/i).fill('An epic fantasy realm')

    // Submit project
    await page.getByRole('button', { name: /create|save/i }).click()

    // Verify project created
    await expect(page.getByText('My First World')).toBeVisible()
    await expect(page.getByText(/project created/i)).toBeVisible()
  })
})
```

### Example 2: Entity Relationship Flow

**Input Description:**
```
User creates a character entity, then creates a location, and links them with "lives in" relationship
```

**Generated Test:**
```typescript
import { test, expect } from '@playwright/test'

test.describe('Entity and Relationship Creation', () => {
  test('creates character and location with relationship', async ({ page }) => {
    await page.goto('/entities')

    // Create character
    await page.getByRole('button', { name: /create entity/i }).click()
    await page.getByLabel(/name/i).fill('Aria Shadowblade')
    await page.getByLabel(/type/i).selectOption('character')
    await page.getByLabel(/description/i).fill('A skilled rogue')
    await page.getByRole('button', { name: /save|create/i }).click()

    // Verify character created
    await expect(page.getByText('Aria Shadowblade')).toBeVisible()

    // Navigate back to entity list
    await page.getByRole('link', { name: /entities/i }).click()

    // Create location
    await page.getByRole('button', { name: /create entity/i }).click()
    await page.getByLabel(/name/i).fill('Shadowfen City')
    await page.getByLabel(/type/i).selectOption('location')
    await page.getByLabel(/description/i).fill('A dark urban settlement')
    await page.getByRole('button', { name: /save|create/i }).click()

    // Open character details
    await page.getByText('Aria Shadowblade').click()

    // Add relationship
    await page.getByRole('button', { name: /add relationship/i }).click()
    await page.getByLabel(/related entity/i).fill('Shadowfen')
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('Enter')
    await page.getByLabel(/relationship type/i).selectOption('lives_in')
    await page.getByRole('button', { name: /create|save/i }).click()

    // Verify relationship
    await expect(page.getByText(/lives in.*shadowfen/i)).toBeVisible()
  })
})
```

### Example 3: Timeline Flow

**Input Description:**
```
User creates a timeline, adds three events, and reorders them chronologically
```

**Generated Test:**
```typescript
import { test, expect } from '@playwright/test'

test.describe('Timeline Creation and Management', () => {
  test('creates timeline with events and reorders them', async ({ page }) => {
    await page.goto('/timelines')

    // Create timeline
    await page.getByRole('button', { name: /create timeline/i }).click()
    await page.getByLabel(/name/i).fill('Age of Heroes')
    await page.getByRole('button', { name: /create/i }).click()

    // Verify timeline created
    await expect(page.getByText('Age of Heroes')).toBeVisible()

    // Click to open timeline
    await page.getByText('Age of Heroes').click()

    // Add first event
    await page.getByRole('button', { name: /add event/i }).click()
    await page.getByLabel(/event name/i).fill('The Founding')
    await page.getByLabel(/date/i).fill('Year 0')
    await page.getByRole('button', { name: /save/i }).click()

    // Add second event
    await page.getByRole('button', { name: /add event/i }).click()
    await page.getByLabel(/event name/i).fill('The Great War')
    await page.getByLabel(/date/i).fill('Year 150')
    await page.getByRole('button', { name: /save/i }).click()

    // Add third event
    await page.getByRole('button', { name: /add event/i }).click()
    await page.getByLabel(/event name/i).fill('The Alliance')
    await page.getByLabel(/date/i).fill('Year 75')
    await page.getByRole('button', { name: /save/i }).click()

    // Verify all events visible
    await expect(page.getByText('The Founding')).toBeVisible()
    await expect(page.getByText('The Great War')).toBeVisible()
    await expect(page.getByText('The Alliance')).toBeVisible()

    // Sort chronologically
    await page.getByRole('button', { name: /sort/i }).click()
    await page.getByRole('menuitem', { name: /chronological/i }).click()

    // Verify order
    const events = page.locator('[data-testid="timeline-event"]')
    await expect(events.nth(0)).toContainText('The Founding')
    await expect(events.nth(1)).toContainText('The Alliance')
    await expect(events.nth(2)).toContainText('The Great War')
  })
})
```

## Advanced Features

### Authentication Flows

To handle authentication, use the setup from `references/auth-patterns.md`:

```typescript
test.describe('Authenticated Flow', () => {
  test.use({ storageState: 'auth.json' })

  test('user performs action', async ({ page }) => {
    // Test steps with authenticated user
  })
})
```

### API Mocking

To mock API responses, use Playwright's route handlers:

```typescript
test('displays entities from API', async ({ page }) => {
  await page.route('**/api/entities', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([
        { id: '1', name: 'Test Entity' }
      ])
    })
  })

  await page.goto('/entities')
  await expect(page.getByText('Test Entity')).toBeVisible()
})
```

### Error Scenarios

To test error handling:

```typescript
test('handles server error gracefully', async ({ page }) => {
  await page.route('**/api/entities', route => {
    route.fulfill({ status: 500 })
  })

  await page.goto('/entities')
  await expect(page.getByText(/error|failed/i)).toBeVisible()
})
```

## Command Usage

### Generate Test from Description

```bash
python scripts/generate_flow_test.py \
  --description "User signs up and creates project" \
  --output test/e2e/signup-flow.spec.ts
```

### Generate Test from File

```bash
python scripts/generate_flow_test.py \
  --input flows/user-onboarding.txt \
  --output test/e2e/onboarding.spec.ts
```

### Generate Multiple Tests

```bash
python scripts/batch_generate_tests.py \
  --flows-dir flows/ \
  --output-dir test/e2e/
```

## Resources

Consult the following resources for detailed information:

- `scripts/parse_flow.py` - Flow description parser
- `scripts/generate_flow_test.py` - Test generator
- `scripts/generate_fixtures.py` - Test data generator
- `references/playwright-actions.md` - Action mapping reference
- `references/auth-patterns.md` - Authentication patterns
- `references/selectors.md` - Selector best practices
- `assets/test-template.ts` - Base test template
- `assets/action-templates/` - Action code templates

## Best Practices

- Use semantic selectors (role, label, text)
- Add explicit waits for dynamic content
- Include assertions after state changes
- Test error scenarios
- Keep tests independent
- Use descriptive test names
- Add comments for complex flows
- Group related tests with describe blocks
