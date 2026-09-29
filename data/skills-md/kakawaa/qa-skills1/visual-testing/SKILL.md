---
name: visual-testing
description: >-
  Implement visual regression testing with Playwright screenshots, Chromatic, Percy,
  and Argos CI. Covers baseline management, diff threshold tuning, dynamic content
  masking, responsive viewport testing, and review/approval workflows.
  Use when: "visual test," "screenshot," "visual regression," "pixel diff," "baseline,"
  "Chromatic," "Percy."
  Related: playwright-automation, ci-cd-integration, cross-browser-testing.
license: MIT
metadata:
  author: kindlmann
  version: "1.0"
  category: automation
---

# Visual Testing

Catch visual regressions that functional tests miss. A button that works perfectly but renders at 2px height is not caught by `toBeVisible()` or `click()`. Visual testing compares screenshots against approved baselines and flags pixel-level differences. This skill covers Playwright's built-in visual comparisons, dedicated tools (Chromatic, Percy, Argos CI), and the workflows around baseline management.

---

## Discovery Questions

Before implementing visual testing, gather context. Check `.agents/qa-project-context.md` first -- if it exists, use it and skip questions already answered there.

### Tool Selection

- **Playwright built-in or dedicated tool?** Playwright's `toHaveScreenshot` is free and requires no external service. Dedicated tools (Chromatic, Percy, Argos) add review workflows, browser rendering farms, and historical tracking. Choose based on team size and review needs.
- **Storybook in the project?** If yes, Chromatic is the natural fit -- it captures every story as a visual test. If no Storybook, Playwright or Percy are better options.
- **CI platform?** Visual testing generates large artifacts (screenshots, diffs). Ensure CI has storage and the pipeline can handle the extra time.

### Scope

- **Full-page or component screenshots?** Full-page catches layout issues but is sensitive to unrelated changes. Component-level screenshots are more stable and focused.
- **Which pages/components are visually critical?** Not everything needs visual testing. Focus on user-facing pages, marketing pages, design system components, and complex layouts.
- **Which viewports?** Desktop, tablet, mobile? Define the viewport matrix upfront.

### Dynamic Content

- **What content changes between runs?** Dates, timestamps, user-generated content, analytics IDs, randomized content, advertisements, avatars. All must be masked or frozen.
- **Are there animations or transitions?** These cause false positives if not disabled or waited for.
- **Does the page load external resources?** Fonts, images from CDNs, third-party widgets can vary between runs.

---

## Core Principles

### 1. Visual Tests Catch What Functional Tests Miss

Functional tests assert behavior: "clicking Submit shows a success message." Visual tests assert appearance: "the success message is green, correctly positioned, and does not overlap the form." Both are needed. Visual tests complement functional tests, they do not replace them.

### 2. Baseline Management Is the Hard Part

Taking screenshots is easy. Managing baselines -- updating them when design changes intentionally, reviewing diffs, coordinating approvals across a team -- is the real challenge. Invest in the review workflow early.

### 3. Dynamic Content Causes False Positives

Any content that changes between runs (timestamps, avatars, ads, random IDs) produces pixel differences that are not real regressions. Aggressively mask or freeze dynamic content. A visual test suite with a 10% false positive rate will be ignored within a month.

### 4. Threshold Tuning Is Iterative

The right diff threshold depends on the specific component, rendering engine, and what you consider "visually different." Start strict (zero tolerance), observe false positives, and loosen thresholds per-component as needed. Document why each threshold was chosen.

### 5. Screenshots Are Artifacts, Not Test Results

The screenshot file itself is evidence. Store it, version it, and make it accessible for review. A test that says "visual diff detected" without showing the diff is useless.

---

## Playwright Visual Comparisons

Playwright's built-in `toHaveScreenshot` and `toMatchSnapshot` provide visual regression testing without external services.

### Basic Screenshot Comparison

```typescript
import { test, expect } from '@playwright/test';

test('dashboard matches baseline', async ({ page }) => {
  await page.goto('/dashboard');
  // Wait for all data to load before capturing
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  await expect(page.getByTestId('chart-container')).toBeVisible();

  await expect(page).toHaveScreenshot('dashboard.png');
});
```

On first run, this creates the baseline screenshot. On subsequent runs, it compares against the baseline and fails if pixels differ beyond the threshold.

### Configuration Options

```typescript
// Comparison with explicit thresholds
await expect(page).toHaveScreenshot('dashboard.png', {
  maxDiffPixels: 100,          // Allow up to 100 pixels to differ
  // OR
  maxDiffPixelRatio: 0.01,     // Allow up to 1% of pixels to differ
  threshold: 0.2,              // Per-pixel color difference tolerance (0-1)
  animations: 'disabled',      // Freeze CSS animations and transitions
  caret: 'hide',               // Hide blinking cursor
  timeout: 15000,              // Wait up to 15s for stable screenshot
});
```

**When to use which threshold:**

| Option | Use When |
|--------|----------|
| `maxDiffPixels: 0` | Pixel-perfect components (icons, logos, design system atoms) |
| `maxDiffPixels: 50-100` | Full-page layouts where antialiasing varies slightly |
| `maxDiffPixelRatio: 0.01` | Full-page screenshots where absolute pixel count varies with viewport |
| `threshold: 0.2` | Cross-browser testing where color rendering differs slightly |

### playwright.config.ts Visual Settings

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.005,    // Global default: 0.5% tolerance
      animations: 'disabled',
      caret: 'hide',
    },
    toMatchSnapshot: {
      maxDiffPixelRatio: 0.005,
    },
  },
  projects: [
    {
      name: 'visual-desktop',
      use: {
        viewport: { width: 1280, height: 720 },
        colorScheme: 'light',
      },
      testMatch: /.*visual.*\.spec\.ts/,
    },
    {
      name: 'visual-mobile',
      use: {
        viewport: { width: 375, height: 667 },
        colorScheme: 'light',
        isMobile: true,
      },
      testMatch: /.*visual.*\.spec\.ts/,
    },
  ],
});
```

### Masking Dynamic Regions

```typescript
test('profile page visual test', async ({ page }) => {
  await page.goto('/profile');
  await expect(page.getByRole('heading', { name: 'Profile' })).toBeVisible();

  await expect(page).toHaveScreenshot('profile.png', {
    mask: [
      page.getByTestId('user-avatar'),        // User-specific image
      page.getByTestId('last-login-time'),     // Timestamp
      page.getByTestId('activity-feed'),       // Dynamic content
    ],
    maskColor: '#FF00FF',                       // Visible mask color for debugging
  });
});
```

### Freezing Dynamic Content Before Capture

```typescript
test('dashboard with frozen data', async ({ page }) => {
  // Freeze time to eliminate timestamp differences
  await page.clock.install({ time: new Date('2026-01-15T10:00:00Z') });

  // Stub API to return deterministic data
  await page.route('**/api/dashboard', async (route) => {
    await route.fulfill({
      json: {
        stats: { users: 1234, revenue: 56789 },
        chart: [10, 20, 30, 40, 50],
      },
    });
  });

  // Disable font loading to prevent FOUT (Flash of Unstyled Text)
  await page.route('**/*.woff2', (route) => route.abort());

  await page.goto('/dashboard');
  await expect(page.getByTestId('chart-container')).toBeVisible();

  // Wait for animations to complete
  await page.evaluate(() => {
    document.getAnimations().forEach((a) => a.finish());
  });

  await expect(page).toHaveScreenshot('dashboard-frozen.png', {
    animations: 'disabled',
  });
});
```

### Handling Animations

Two options: use Playwright's built-in `animations: 'disabled'` in `toHaveScreenshot` (preferred), or inject a style tag that zeros out `animation-duration` and `transition-duration` for all elements. Always wait for the element to be visible before capturing.

### Component-Level Screenshots

```typescript
test('data table renders correctly with various states', async ({ page }) => {
  await page.goto('/admin/users');
  await expect(page.getByRole('table')).toBeVisible();

  // Screenshot just the table component, not the full page
  const table = page.getByRole('table', { name: 'Users' });
  await expect(table).toHaveScreenshot('users-table.png');
});

test('empty state renders correctly', async ({ page }) => {
  await page.route('**/api/users', (route) => route.fulfill({ json: { users: [] } }));
  await page.goto('/admin/users');

  const emptyState = page.getByTestId('empty-state');
  await expect(emptyState).toHaveScreenshot('users-empty-state.png');
});

test('error state renders correctly', async ({ page }) => {
  await page.route('**/api/users', (route) => route.fulfill({ status: 500 }));
  await page.goto('/admin/users');

  const errorState = page.getByTestId('error-state');
  await expect(errorState).toHaveScreenshot('users-error-state.png');
});
```

### Updating Baselines

```bash
# Update all baselines (when design intentionally changes)
npx playwright test --update-snapshots

# Update baselines for specific tests only
npx playwright test visual-dashboard --update-snapshots

# Review what changed before committing
git diff --stat  # See which baseline files changed
# Open the test report to visually review each change
npx playwright show-report
```

**Baseline update workflow:**

1. Design change is implemented
2. Run visual tests -- they fail with expected diffs
3. Review each diff: is the change intentional?
4. Update baselines: `npx playwright test --update-snapshots`
5. Commit updated baselines with a descriptive message referencing the design change
6. PR reviewers verify the baseline changes look correct

---

## Dedicated Visual Testing Tools

### Tool Comparison

| Tool | Best When | Integration | Key Feature |
|------|-----------|-------------|-------------|
| **Chromatic** | Project uses Storybook | Every story = a visual test | Review/approval UI, cross-browser |
| **Percy** | No Storybook, need multi-browser | Any test framework via SDK | Multi-width captures, CSS overrides |
| **Argos CI** | Open-source preference, budget-conscious | Playwright reporter | Self-hosting option, generous free tier |

### Chromatic (Storybook)

```yaml
# GitHub Actions
- uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    exitZeroOnChanges: true    # Changes go to review, not CI failure
    onlyChanged: true          # Only test stories affected by code changes
```

Workflow: push code, CI captures screenshots, reviewers approve/reject in Chromatic UI, PR merges after approval.

### Percy (Any Framework)

```typescript
import { percySnapshot } from '@percy/playwright';

test('checkout page visual', async ({ page }) => {
  await page.goto('/checkout');
  await percySnapshot(page, 'Checkout Page', {
    widths: [375, 768, 1280],
    percyCSS: `.ad-banner { display: none !important; }`,
  });
});
// CI: npx percy exec -- npx playwright test --grep @visual
```

### Argos CI (Open Source)

```typescript
import { argosScreenshot } from '@argos-ci/playwright';

test('pricing page visual', async ({ page }) => {
  await page.goto('/pricing');
  await argosScreenshot(page, 'pricing-page', { viewports: ['macbook-16', 'iphone-x'] });
});
```

---

## Responsive Visual Testing

Test at breakpoints where layout changes, not at every possible viewport. Define a viewport matrix based on analytics data.

```typescript
const VISUAL_VIEWPORTS = [
  { name: 'mobile', width: 375, height: 667, isMobile: true },
  { name: 'tablet', width: 768, height: 1024, isMobile: false },
  { name: 'desktop', width: 1280, height: 720, isMobile: false },
] as const;

for (const vp of VISUAL_VIEWPORTS) {
  test.describe(`Visual @ ${vp.name}`, () => {
    test.use({ viewport: { width: vp.width, height: vp.height }, isMobile: vp.isMobile });

    test('homepage layout', async ({ page }) => {
      await page.goto('/');
      await expect(page.getByRole('main')).toBeVisible();
      await expect(page).toHaveScreenshot(`homepage-${vp.name}.png`, {
        fullPage: true,
        animations: 'disabled',
      });
    });
  });
}
```

Alternatively, use Playwright projects (in `playwright.config.ts`) to define viewport configurations and run all visual tests across them automatically.

---

## Baseline Management

### Git-Stored Baselines

Playwright stores baselines alongside test files by default.

```
e2e/
  tests/
    visual/
      dashboard.visual.spec.ts
      dashboard.visual.spec.ts-snapshots/
        dashboard-chromium-linux.png         # Platform-specific baselines
        dashboard-chromium-darwin.png
        dashboard-firefox-linux.png
```

**Pros:** Baselines are versioned with the code, reviewed in PRs, and available offline.

**Cons:** Repository size grows. Large baseline files bloat git history.

Use Git LFS (`.gitattributes`: `*.png filter=lfs diff=lfs merge=lfs -text`) to prevent repository bloat. Customize snapshot paths with `snapshotPathTemplate` in `playwright.config.ts`.

### Platform-Specific Baselines

Playwright renders differently across operating systems. Use Docker in CI for consistency:

```yaml
jobs:
  visual-tests:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright:v1.50.0-noble
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright test --grep @visual
```

Generate baselines in CI (not locally) so they always match the CI rendering environment.

### Review and Approval Workflow

1. CI detects visual diff, uploads expected/actual/diff images as artifacts
2. PR reviewer examines diffs
3. Intentional change: update baselines (`--update-snapshots`), re-commit
4. Unintentional regression: fix the code, re-run tests

---

## Anti-Patterns

### Full-Page Screenshots Without Masking

Capturing entire pages without masking dynamic content (timestamps, user avatars, live data). Every run produces diffs that are not real regressions. The team stops trusting visual tests and ignores them. Always mask dynamic regions and freeze time-dependent content.

### No Artifact Storage in CI

Running visual tests in CI without uploading screenshot artifacts. When a test fails, there is no way to see the actual vs. expected image. The developer has to reproduce locally, which may produce different results due to platform rendering differences. Always upload screenshots, diffs, and test reports as CI artifacts.

### No Review Process for Baseline Updates

Running `--update-snapshots` and committing without reviewing the changes. Regressions get baked into baselines and become invisible. Every baseline update should go through code review. Reviewers must look at the before/after images, not just the file diff.

### Testing Visual Stability of Unstable Components

Writing visual tests for components that change frequently by design (A/B tests, personalized content, frequently updated marketing banners). These tests fail constantly with intentional changes, creating noise. Either exclude these components from visual testing or stub their content.

### Pixel-Perfect Thresholds on Full Pages

Setting `maxDiffPixels: 0` on full-page screenshots. Sub-pixel rendering differences across browser versions, OS updates, and font rendering changes produce false positives. Use `maxDiffPixelRatio: 0.005` (0.5%) for full pages. Reserve zero tolerance for small, critical components like logos and icons.

### No Consistent Rendering Environment

Running visual tests on developer machines (macOS, Windows, various displays) and expecting baselines to match. Font rendering, antialiasing, and scaling differ across platforms. Run visual tests in a consistent CI environment (Docker) and generate baselines there.

### Skipping Animation Handling

Not disabling animations before taking screenshots. CSS transitions and JavaScript animations captured mid-frame produce random diffs. Use `animations: 'disabled'` in Playwright or inject CSS to zero-out animation durations.

---

## Related Skills

- **playwright-automation** -- The foundation for Playwright-based visual tests; Page Object Model, fixtures, and test structure apply to visual tests too.
- **ci-cd-integration** -- Pipeline configuration for running visual tests, uploading artifacts, and integrating review workflows.
- **cross-browser-testing** -- Visual tests across browsers catch rendering differences; viewport matrix and browser project configuration overlap.
- **qa-project-context** -- The project context file captures which pages are visually critical and what dynamic content exists.
