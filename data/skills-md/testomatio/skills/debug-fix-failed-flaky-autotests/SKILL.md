---
name: debug-fix-failed-flaky-autotests
description: Diagnose and fix failing automated tests. Analyzes failures, inspects DOM, identifies root causes, and applies targeted fixes using framework tools and MCP/CLI debug modes. Use when tests fail, are flaky, or behave inconsistently (e.g., pass locally but fail in CI).
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Debug and Fix Failing Autotests

Diagnose failing automated tests and apply targeted fixes.
Follow the four steps in order.
Detailed fixes and code examples: [references/DEBUGGING_QUICK_REFERENCE.md](references/DEBUGGING_QUICK_REFERENCE.md).

## Step 1: Analyze Failure

- Identify the framework. It determines the debug tools:
  - Playwright: CLI debug, trace viewer, MCP snapshots.
  - CodeceptJS: `--steps` mode, CDP inspection.
  - Cypress: devTools, screenshots on failure.
  - WebdriverIO: Selenium logs.
- Categorize the error:
  - Locator (element missing/unreachable).
  - Timing (timeout/race).
  - Assertion (expected ≠ actual).
  - Flow (navigation, preconditions).
  - Infrastructure (CI/browser/network).
- End with a hypothesis: root cause + fix category.

## Step 2: Inspect and Diagnose

- DOM inspection:
  - Playwright: `page.locator('selector').evaluate(el => el.outerHTML)`.
  - CodeceptJS: `I.executeScript(() => document.querySelector('.selector').outerHTML)`.
  - MCP snapshot: capture live DOM state for complex elements.
- Console and network logs:
  - Console: `page.on('console', msg => console.log(msg.text()))`.
  - Failed requests: `page.on('requestfailed', r => console.log(r.failure().errorText))`.
- Trace analysis (Playwright): `npx playwright show-trace trace.zip`.
  - Inspect timing and order of clicks, navigation, network requests.

## Step 3: Apply Fix

**Fix in priority order: locators → timing → assertions → flow.**

- Locators: use stable selectors (`data-testid` → `aria-label` → `role` → `id` → `text` → CSS/XPath).
  - Re-fetch stale elements, scroll hidden elements into view, use `.first()` for multiple matches.
- Timing: use framework-native waits (`waitFor`, `waitForNavigation`, `waitForLoadState('networkidle')`).
  - **No hard sleeps** like `sleep(5000)` or `wait(2)`.
- Assertions: use contains/regex for flexible matching.
  - Verify expected values against the test spec, not assumptions.
- Flow: ensure preconditions (login, navigation order, test data).
  - Isolate test state from prior runs.

Before/after examples for each category: [references/DEBUGGING_QUICK_REFERENCE.md](references/DEBUGGING_QUICK_REFERENCE.md).

## Step 4: Verify and Stabilize

Re-run the test:

```bash
npx playwright test path/to/test.spec.ts
npx codeceptjs run path/to/test.js
```

Test is stable when:
- Passes 2 consecutive runs.
- Uses resilient locators.
- Waits properly for dynamic content.

**Max 3 healing attempts total.** After 3 failed attempts: stop, document what was tried, ask the user for guidance.

Document the fix: root cause, applied fix, verification result.

## MCP Debug Tools (Optional)

Use MCP when standard fixes fail, the UI is complex (dropdowns, modals, dynamic content), or live DOM inspection is needed:
- Playwright MCP: live snapshots, element counts, DOM inspection after each action.
- CodeceptJS MCP: CDP-based inspection, `--steps` mode for live debugging.

## User Interaction

Ask when unclear:

```
❓ Which element should I target for this action?

Options:
1. Submit button (data-testid="submit")
2. Save button (aria-label="Save")
3. Other (specify)
```

Report progress:

```
🔍 Analyzing failure...
  - Error: Element not found
  - Context: Login test, line 42

🔧 Applying fix...
  - Issue: Selector too broad
  - Fix: Using getByRole('button', { name: 'Login' })

✅ Test passed! (Run 1/2)
```
