---
name: playwright-browser
description:
  Playwright CLI and MCP tools for headless browser automation, E2E testing,screenshots, and web scraping. Use for CI-safe browser operations.
---

# Playwright Browser Automation

Headless browser automation using Playwright CLI and MCP tools for E2E testing, UI verification, screenshots, and web scraping.

## When to Apply

### Positive Triggers

- E2E test execution (`test:e2e`, `playwright test`)
- UI screenshot capture for review or regression
- Web scraping / content extraction
- Form submission testing
- Visual regression testing
- Lighthouse / performance auditing via browser
- Multi-page workflow validation

### Negative Triggers (Do NOT Apply)

- Unit tests (use Vitest/Pytest)
- API-only tests (use httpx/fetch)
- Personal browser sessions (use `claude-browser` skill)
- Static code analysis

## Core Principles

1. **Headless by default** — use `--headed` only when debugging
2. **Screenshot at each step** — capture visual evidence for review
3. **Parallel sessions** — leverage Playwright's built-in parallelism
4. **Persistent profiles** — reuse auth state across test runs
5. **CI-safe** — all operations must work in headless CI environments

## MCP Playwright Tools

These tools are available via the `mcp__playwright__*` namespace:

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Navigate to URL |
| `browser_click` | Click element by selector or text |
| `browser_fill_form` | Fill form fields |
| `browser_take_screenshot` | Capture page screenshot |
| `browser_snapshot` | Get accessibility tree snapshot |
| `browser_evaluate` | Execute JavaScript in page context |
| `browser_press_key` | Simulate keyboard input |
| `browser_type` | Type text into focused element |
| `browser_select_option` | Select dropdown option |
| `browser_wait_for` | Wait for element/condition |
| `browser_network_requests` | Inspect network activity |
| `browser_console_messages` | Read console output |
| `browser_hover` | Hover over element |
| `browser_drag` | Drag and drop |
| `browser_handle_dialog` | Accept/dismiss dialogs |
| `browser_file_upload` | Upload files |
| `browser_tabs` | Manage browser tabs |
| `browser_navigate_back` | Go back |
| `browser_resize` | Resize viewport |
| `browser_close` | Close browser |
| `browser_install` | Install browser binaries |
| `browser_run_code` | Run Playwright code snippet |

### Usage Pattern

```
1. Load tools: ToolSearch "playwright"
2. Navigate: browser_navigate to target URL
3. Interact: browser_click, browser_fill_form, browser_type
4. Capture: browser_take_screenshot at each significant step
5. Verify: browser_snapshot for accessibility tree, browser_evaluate for assertions
6. Clean up: browser_close when done
```

## CLI Playwright Commands

```bash
# Install browsers
npx playwright install chromium

# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/login.spec.ts

# Run with headed browser (debugging)
npx playwright test --headed

# Generate test from user interaction
npx playwright codegen http://localhost:3000

# Show HTML report
npx playwright show-report

# Run with specific project/browser
npx playwright test --project=chromium
```

## Screenshot Workflow

### Naming Convention

```
{step-number}-{description}.png
```

Examples: `01-login-page.png`, `02-form-filled.png`, `03-dashboard-loaded.png`

### Storage

```
ai-review/screenshots/     # Automated review screenshots
test-results/              # Playwright test artifacts
playwright-report/         # HTML report with traces
```

### Capture Strategy

- **Before action**: Capture initial state
- **After action**: Capture result state
- **On failure**: Automatic screenshot (Playwright default)
- **Full page**: Use `fullPage: true` for long pages

## Session Management

### Auth State Reuse

```typescript
// Save auth state after login
await page.context().storageState({ path: 'auth-state.json' });

// Reuse in subsequent tests
const context = await browser.newContext({
  storageState: 'auth-state.json'
});
```

### Persistent Contexts

For multi-step workflows that span multiple tool calls, maintain browser context between operations. Close explicitly when done.

## Parallel Execution

Playwright supports parallel test execution natively:

```bash
# Run tests in parallel (default)
npx playwright test --workers=4

# Run serially (debugging)
npx playwright test --workers=1
```

For MCP tool usage, open multiple browser tabs for parallel story validation.

## Project Integration

| File | Purpose |
|------|---------|
| `apps/web/playwright.config.ts` | Playwright configuration |
| `apps/web/tests/e2e/` | E2E test directory |
| `apps/web/package.json` | `test:e2e` script |

## Anti-Patterns

- Running headed browsers in CI — always use headless
- Hardcoding selectors — prefer `data-testid` or accessible roles
- Ignoring timeouts — set explicit timeouts per action
- Skipping screenshots — always capture evidence for review
- Using `page.waitForTimeout()` — prefer `page.waitForSelector()` or `browser_wait_for`

## Pre-Merge Checklist

- [ ] All E2E tests pass in headless mode
- [ ] Screenshots captured for new UI flows
- [ ] Auth state properly managed (no credential leaks)
- [ ] Network requests validated (no unexpected external calls)
- [ ] Console errors checked (no uncaught exceptions)
- [ ] Viewport tested at standard breakpoints (mobile, tablet, desktop)