---
name: zoonk-testing
description: Write tests following TDD principles. Use when implementing features, fixing bugs, or adding test coverage. Covers e2e, integration, and unit testing patterns.
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Testing Guidelines

Follow TDD (Test-Driven Development) for all features and bug fixes. **Always write failing tests first.**

## How to Think About Tests

Before writing any test, answer these questions:

### 1. What behavior am I verifying?

State it in one sentence. If you can't, the test is too complex.

- ✅ "Verify locale persists when navigating between pages"
- ✅ "Verify users can create a course with a title"
- ❌ "Verify the course description popover opens in the correct language when clicking from a Portuguese page"
- ❌ "Verify the sidebar collapses, remembers state, and shows tooltips on hover when collapsed"

### 2. What's the simplest proof?

Find the minimum actions to verify the behavior:

| Behavior             | Simplest Proof                                     | NOT This                                                           |
| -------------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| Locale persistence   | Navigate → click link → check URL contains `/pt`   | Navigate → click course → open popover → verify translation        |
| Course creation      | Fill title → submit → verify title appears         | Fill all fields → verify each field → check database → verify list |
| Login works          | Enter credentials → submit → see dashboard heading | Enter credentials → verify button enabled → submit → check cookie  |
| Item appears in list | Create item → verify it's visible                  | Create item → scroll list → filter → sort → find item              |

### 3. Am I testing the right thing?

Ask: "If this test passes, am I confident the feature works?"

- If "yes" requires trusting other unrelated UI mechanics, you're testing the wrong thing
- If the test could pass with broken code, it's too loose
- If the test could fail with working code, it's testing implementation details

**Example**: To test locale preservation, you don't need to verify translated content renders correctly. That's a translation test, not a locale persistence test. Just verify the URL maintains the locale segment.

## TDD Workflow

1. **Write a failing test** that describes the expected behavior
2. **Run the test to confirm it fails** - this is non-negotiable
3. **Write the minimum code** to make the test pass
4. **Run the test** to confirm it passes
5. **Refactor** while keeping tests green

### If the Test Passes Before Your Fix

The test is wrong. A passing test means one of:

1. The bug doesn't exist (investigate further)
2. The test is matching existing/seeded data instead of new behavior
3. The test assertion is too loose

**Never use workarounds to make a "failing" test pass:**

```typescript
// BAD: Using .first() to avoid multiple matches
await expect(page.getByText(courseTitle).first()).toBeVisible();
// This passes even if the item existed before your fix!

// GOOD: Use unique identifiers so only ONE element can match
const uniqueId = randomUUID().slice(0, 8);
const courseTitle = `Test Course ${uniqueId}`;
await expect(page.getByText(courseTitle)).toBeVisible();
// This ONLY passes if your code actually created this specific item
```

## Test Isolation Principle

**Core Rule: Tests must be completely self-contained.**

This means:

1. **Create your own data** - Don't rely on seed data existing or having specific values
2. **No cleanup needed** - If you need `afterEach` cleanup, your test isn't isolated
3. **Parallel safe** - Tests should run in any order, even simultaneously

### Why Not Seed Data?

Seed data creates hidden dependencies:

- Tests break when seed data changes
- Tests pass locally but fail in CI (different seeds)
- Tests can't run in parallel (shared state)
- Debugging requires knowing what's seeded

### The Pattern

Every test that needs data should create it:

```typescript
// Create unique data for THIS test
const uniqueId = randomUUID().slice(0, 8);
const course = await courseFixture({
  slug: `e2e-${uniqueId}`,
  title: `E2E Course ${uniqueId}`,
});

// Test uses only data it created
await page.goto(`/courses/${course.slug}`);
```

### Exception: Structural Dependencies

Using a seeded organization as a container is acceptable because:

1. It's a structural dependency, not a content assertion
2. Tests create their own content within it
3. The org is guaranteed to exist in all environments

```typescript
// ACCEPTABLE: Using seeded org as container
const org = await prisma.organization.findUniqueOrThrow({
  where: { slug: "ai" },
});
const course = await courseFixture({ organizationId: org.id });
```

### Exception: Read-Only Route Verification

For verifying that a page renders at all (not specific content), you may use known paths:

```typescript
// OK: Just verifying the route works
test("course detail page renders", async ({ page }) => {
  await page.goto("/b/ai/c/machine-learning"); // Seeded course
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});

// NOT OK: Relying on specific seeded content
test("shows machine learning description", async ({ page }) => {
  await page.goto("/b/ai/c/machine-learning");
  await expect(page.getByText("patterns|predictions")).toBeVisible(); // Fragile!
});
```

## Test Types

| When                    | Test Type   | Framework  | Location                              |
| ----------------------- | ----------- | ---------- | ------------------------------------- |
| Apps/UI features        | E2E         | Playwright | `apps/{app}/e2e/`                     |
| Data functions (Prisma) | Integration | Vitest     | `apps/{app}/src/data/` or `packages/` |
| Utils/helpers           | Unit        | Vitest     | `packages/{pkg}/*.test.ts`            |

## E2E Testing (Playwright)

### Query Priority

Use semantic queries that reflect how users interact with the page:

```typescript
// GOOD: Semantic queries (in order of preference)
page.getByRole("button", { name: "Submit" });
page.getByRole("heading", { name: "Welcome" });
page.getByLabel("Email address");
page.getByText("Sign up for free");
page.getByPlaceholder("Search...");

// BAD: Implementation details
page.locator(".btn-primary");
page.locator("#submit-button");
page.locator("[data-testid='submit']");
page.locator("[data-slot='media-card-icon']");
```

**If you can't use `getByRole`, the component likely has accessibility issues.** Fix the component first.

### Wait Patterns

```typescript
// GOOD: Wait for visible state
await expect(page.getByRole("heading")).toBeVisible();
await expect(page.getByText("Success")).toBeVisible();

// GOOD: Wait for URL change
await page.waitForURL(/\/dashboard/);

// BAD: Arbitrary delays
await page.waitForTimeout(2000);
```

### Animated Elements

Elements with CSS transitions can cause "element is not stable" errors. Pattern: wait for visibility, then use `force: true`:

```typescript
// Wait for submenu content to be visible (animation complete)
await expect(page.getByRole("menuitem", { name: "English" })).toBeVisible();
// Force click bypasses stability check - safe because we confirmed visibility
await page.getByRole("menuitem", { name: "Español" }).click({ force: true });
```

**When to use `force: true`**:

- After confirming the element is visible via `toBeVisible()`
- When CSS animations cause repeated "element is not stable" errors
- Never as a first resort—always investigate why the element is unstable first

### Authentication Fixtures

Use pre-configured fixtures from your test setup:

```typescript
import { expect, test } from "./fixtures";

test("authenticated user sees dashboard", async ({ authenticatedPage }) => {
  await authenticatedPage.goto("/");
  await expect(authenticatedPage.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```

### Creating Test Data

**Use Prisma fixtures for tests that need specific data states:**

```typescript
import { postFixture } from "@/tests/fixtures/posts";

async function createTestPost() {
  const uniqueId = randomUUID().slice(0, 8);
  return postFixture({
    slug: `e2e-${uniqueId}`,
    title: `E2E Post ${uniqueId}`,
  });
}

test("edits post title", async ({ authenticatedPage }) => {
  const post = await createTestPost();
  await authenticatedPage.goto(`/posts/${post.slug}`);
  // ... test editing behavior
});
```

**Create unique users for user-specific state:**

When testing features that depend on user state (subscriptions, permissions), create a unique user per test:

```typescript
test("works with subscription", async () => {
  const uniqueId = randomUUID().slice(0, 8);
  const email = `e2e-test-${uniqueId}@zoonk.test`;

  // Create unique user via sign-up API
  const signupContext = await request.newContext({ baseURL });
  await signupContext.post("/v1/auth/sign-up/email", {
    data: { email, name: `E2E User ${uniqueId}`, password: "password123" },
  });

  // Create user-specific state
  const user = await prisma.user.findUniqueOrThrow({ where: { email } });
  await prisma.subscription.create({
    data: { referenceId: String(user.id), status: "active", plan: "hobby" },
  });

  // No cleanup needed - user is unique to this test
});
```

### Preventing Flaky Tests

**Run new tests multiple times before considering them done:**

```bash
for i in {1..5}; do pnpm e2e -- -g "test name" --reporter=line; done
```

**High-risk scenarios:**

| Scenario                         | Prevention                                         |
| -------------------------------- | -------------------------------------------------- |
| Clicking dropdown items          | Wait for visibility, use `force: true`             |
| Actions triggering navigation    | Use `waitForLoadState` or `waitForURL` after click |
| Form submissions                 | Wait for success indicator before next action      |
| Inputs with debounced validation | Use `waitForLoadState("networkidle")` after fill   |
| Server action persistence        | Assert UI immediately, then DB query with `toPass` |

### Server Actions

**Server Actions run server-side, so `page.route()` cannot intercept them.** To test error states, trigger real validation errors:

```typescript
// Whitespace passes HTML5 "required" but fails server-side when trimmed
await nameInput.fill("   ");
await page.getByRole("button", { name: /submit/i }).click();
await expect(page.getByRole("alert")).toBeVisible();
```

### Verifying Persistence in E2E Tests

When a server action mutates data (toggle, add, remove, reorder), verify two things separately:

1. **UI updates immediately** (no reload) — tests the user experience
2. **Data persisted to DB** (via Prisma query) — tests the server action, fast and deterministic

```typescript
// GOOD: UI assertion + DB assertion
await openCategoryPopover(page);
await getCategoryOption(page, /technology/i).click();
await page.keyboard.press("Escape");

// 1. Badge appears immediately — user doesn't need to refresh
await expect(page.getByText("Technology")).toBeVisible();

// 2. Server action persisted — fast DB check with retry
await expect(async () => {
  const record = await prisma.courseCategory.findUnique({
    where: { courseCategory: { category: "tech", courseId: course.id } },
  });
  expect(record).not.toBeNull();
}).toPass({ timeout: 10_000 });

// BAD: Reloading to verify persistence
await page.reload();
await expect(page.getByText("Technology")).toBeVisible();
// This is slow, flaky (caching), and doesn't catch "user must refresh" bugs
```

**When reload IS appropriate**: Auto-save flows (type → debounce → "saved" indicator → persist) where the reload verifies the complete UX cycle end-to-end. The user types, sees "saved", and expects data to survive a refresh — that IS the behavior being tested.

```typescript
// Auto-save flow: reload is the right tool
await titleInput.fill(uniqueTitle);
await expect(page.getByText(/^saved$/i)).toBeVisible();
await page.reload();
await expect(titleInput).toHaveValue(uniqueTitle);
```

**Decision guide:**

| Action type                        | Immediate check           | Persistence check            |
| ---------------------------------- | ------------------------- | ---------------------------- |
| Server action (click → mutation)   | UI assertion (no reload)  | DB query with `toPass` retry |
| Auto-save (type → debounce → save) | "saved" indicator visible | Reload + verify value        |
| URL/cookie state (locale, filters) | URL assertion             | Reload + verify URL          |

### Drag and Drop (dnd-kit)

Use `locator.dragTo()` with the `steps` parameter. The `steps` option emits intermediate `mousemove` events, which dnd-kit's `PointerSensor` requires to activate a drag:

```typescript
const firstHandle = page.getByRole("button", { name: "Drag to reorder" }).first();
const secondHandle = page.getByRole("button", { name: "Drag to reorder" }).nth(1);

await firstHandle.dragTo(secondHandle, { steps: 20 });
```

**Why `steps` matters**: Without `steps`, Playwright emits a single `mousemove` at the destination, which isn't enough for dnd-kit's PointerSensor to recognize a drag gesture. Use `steps: 20` for smooth, reliable drags.

**Non-deterministic landing position**: `dragTo` between adjacent items can produce different results across runs (swap vs move-to-end). This happens because dnd-kit's `closestCenter` collision detection is sensitive to layout shifts — when an item is "lifted" into the DragOverlay, remaining items shift to fill the gap, moving the drop target. Assert that the order **changed**, not a specific final order:

```typescript
// BAD: Asserts a specific order — flaky because drag can land in different positions
const reorderedItems = [
  { position: 1, title: "Item 2" },
  { position: 2, title: "Item 1" },
  { position: 3, title: "Item 3" },
];
await expectItemsVisible(page, reorderedItems);

// GOOD: Asserts that reordering happened — stable regardless of exact landing position
const firstItem = page.getByRole("listitem").filter({ hasText: /01/ });
await expect(firstItem.getByRole("link", { name: /item 1/i })).not.toBeVisible();
```

## Common Thinking Mistakes

### Over-Testing Through UI Mechanics

**Mistake**: Testing locale preservation by opening popovers and verifying their content.

**Why it's wrong**: You're testing popover behavior, not locale persistence.

**Fix**: Test the simplest proof - URL changes preserve locale.

```typescript
// BAD: Tests translation rendering, not locale persistence
test("preserves locale", async ({ page }) => {
  await page.goto("/pt/courses/intro");
  await page.getByRole("button", { name: /detalhes/i }).click();
  await expect(page.getByText(/descrição em português/i)).toBeVisible();
});

// GOOD: Tests actual locale persistence
test("preserves locale when navigating", async ({ page }) => {
  await page.goto("/pt/courses");
  await page.getByRole("link", { name: /machine learning/i }).click();
  await expect(page).toHaveURL(/^\/pt\//);
});
```

### Testing Implementation Instead of Behavior

**Mistake**: `await expect(page.locator('[data-slot="badge"]')).toBeVisible()`

**Why it's wrong**: You're testing that an attribute exists, not user-visible behavior.

**Fix**: What does the user see? Test that.

```typescript
// BAD: Testing CSS implementation
await expect(page.locator('[data-slot="badge"]')).toBeVisible();

// GOOD: Testing what user sees
await expect(page.getByRole("img", { name: /course thumbnail/i })).toBeVisible();
```

### Relying on Seed Data Content

**Mistake**: Asserting specific seeded values appear in results.

**Why it's wrong**: Test breaks if seed data changes; can't run in parallel.

**Fix**: Create test data with unique identifiers.

```typescript
// BAD: Depends on seed data
test("finds course by title", async ({ page }) => {
  await page.getByRole("textbox").fill("Machine Learning");
  await expect(page.getByText("Introduction to ML")).toBeVisible();
});

// GOOD: Creates its own data
test("finds course by title", async ({ page }) => {
  const uniqueId = randomUUID().slice(0, 8);
  await courseFixture({ title: `Search Test ${uniqueId}` });

  await page.getByRole("textbox").fill(`Search Test ${uniqueId}`);
  await expect(page.getByText(`Search Test ${uniqueId}`)).toBeVisible();
});
```

### Reloading to Verify Server Action Persistence

**Mistake**: Reloading the page to verify a server action persisted data.

**Why it's wrong**: Slow, flaky (caching/timing), and doesn't catch bugs where the UI doesn't update without a refresh.

**Fix**: Assert the UI updates immediately, then query the DB for persistence.

```typescript
// BAD: Reload for persistence — slow, flaky, misses "must refresh" bugs
await page.getByRole("button", { name: /publish/i }).click();
await expect(toggle).toBeChecked();
await page.reload();
await expect(toggle).toBeChecked();

// GOOD: UI check + DB check — fast, reliable, catches UI bugs
await page.getByRole("button", { name: /publish/i }).click();
await expect(toggle).toBeChecked();
await expect(async () => {
  const course = await prisma.course.findUniqueOrThrow({ where: { id: course.id } });
  expect(course.isPublished).toBe(true);
}).toPass({ timeout: 10_000 });
```

### Redundant Tests

**Mistake**: Writing separate tests when a higher-level test already covers the behavior.

**Why it's wrong**: More tests to maintain without more confidence.

**Fix**: If a test proves the final outcome, intermediate steps are implicitly verified.

```typescript
// BAD: Two redundant tests
test("auto-saves title changes", async ({ page }) => {
  await page.getByRole("textbox").fill("New Title");
  await expect(page.getByText(/saved/i)).toBeVisible();
});

test("persists title after reload", async ({ page }) => {
  await page.getByRole("textbox").fill("New Title");
  await page.reload();
  await expect(page.getByRole("textbox")).toHaveValue("New Title");
});

// GOOD: Single test proves both
test("auto-saves and persists title", async ({ page }) => {
  await page.getByRole("textbox").fill("New Title");
  await expect(page.getByText(/saved/i)).toBeVisible();
  await page.reload();
  await expect(page.getByRole("textbox")).toHaveValue("New Title");
});
```

## Integration Testing (Vitest + Prisma)

### Structure

```typescript
import { prisma } from "@/lib/db";
import { postFixture, memberFixture, signInAs } from "@/tests/fixtures";

describe("createComment", () => {
  describe("unauthenticated users", () => {
    test("returns unauthorized error", async () => {
      const result = await createComment({ headers: new Headers(), postId: 1, content: "Test" });
      expect(result.error?.message).toBe(ErrorCode.unauthorized);
    });
  });

  describe("admin users", () => {
    let post: Post;
    let headers: Headers;

    beforeAll(async () => {
      const { organization, user } = await memberFixture({ role: "admin" });
      post = await postFixture({ organizationId: organization.id });
      headers = await signInAs(user.email, user.password);
    });

    test("creates comment successfully", async () => {
      const result = await createComment({ headers, postId: post.id, content: "New Comment" });
      expect(result.data?.content).toBe("New Comment");
    });
  });
});
```

### Test All Permission Levels

```typescript
describe("unauthenticated users", () => {
  /* ... */
});
describe("members", () => {
  /* ... */
});
describe("admins", () => {
  /* ... */
});
```

## Unit Testing (Vitest)

### When to Add Unit Tests

- Edge cases not covered by e2e tests
- Complex utility functions
- Error boundary conditions

```typescript
import { removeAccents } from "./string";

describe("removeAccents", () => {
  test("removes diacritics from string", () => {
    expect(removeAccents("café")).toBe("cafe");
    expect(removeAccents("São Paulo")).toBe("Sao Paulo");
  });
});
```

## Commands

```bash
# Unit/Integration tests
pnpm test                    # Run all tests once
pnpm test -- --run src/data/posts/create-post.test.ts  # Run specific file

# E2E tests
pnpm --filter {app} build:e2e  # Always run before e2e tests
pnpm --filter {app} e2e        # Run all e2e tests
```

## Best Practices

- Read [Playwright best practices before writing e2e tests](https://playwright.dev/docs/best-practices)
