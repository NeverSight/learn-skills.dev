---
name: desktop-testing-electron
description: E2E testing with Playwright, main process unit testing, IPC testing, dialog/menu mocking, CI headless setup
---

# Electron Testing Patterns

> **Quick Guide:** Use Playwright's `_electron.launch()` for E2E tests -- it controls the full app via CDP. Unit test main process code (IPC handlers, business logic) with your test runner by mocking the `electron` module. Test preload scripts by mocking `contextBridge` and `ipcRenderer`. Spectron is dead since Electron 24 -- Playwright and WebDriverIO are the replacements. Run Electron tests on headless Linux CI with `xvfb-run` or the `xvfb-maybe` wrapper.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST `await electronApp.close()` in test teardown -- leaked Electron processes break CI and consume resources)**

**(You MUST mock the `electron` module in unit tests -- Electron APIs are only available inside the Electron runtime)**

**(You MUST use `xvfb-run` or `xvfb-maybe` for headless Linux CI -- Electron requires a display server)**

**(You MUST stub native dialogs in E2E tests -- `showOpenDialog`/`showSaveDialog` block the process and cannot be interacted with by Playwright)**

</critical_requirements>

---

**Auto-detection:** Electron testing, \_electron.launch, electronApp, electronApplication, firstWindow, Playwright Electron, electron-mock-ipc, electron-playwright-helpers, stubDialog, xvfb, xvfb-run, xvfb-maybe, Spectron migration, ipcMain.handle test, ipcRenderer mock, contextBridge mock, BrowserWindow mock, Electron E2E, Electron unit test

**When to use:**

- Writing E2E tests for an Electron application with Playwright
- Unit testing main process code (IPC handlers, lifecycle logic)
- Mocking Electron modules (`dialog`, `BrowserWindow`, `ipcMain`, `ipcRenderer`)
- Testing preload scripts and `contextBridge` APIs
- Setting up headless CI for Electron tests (Linux xvfb)
- Migrating from Spectron to Playwright
- Screenshot/visual regression testing of Electron windows
- Testing auto-update flows

**When NOT to use:**

- Testing renderer UI in isolation (use your web testing skill -- renderer is standard web)
- Writing tests unrelated to Electron-specific APIs
- Performance profiling or benchmarking Electron apps
- Packaging or distributing Electron apps (use the Electron framework skill)

**Key patterns covered:**

- Playwright E2E: `_electron.launch()`, `firstWindow()`, `evaluate()`, assertions
- Main process unit testing with mocked Electron modules
- IPC handler testing (`ipcMain.handle` / `ipcRenderer.invoke`)
- Preload script testing (mock `contextBridge.exposeInMainWorld`)
- Dialog and menu stubbing in E2E tests
- Auto-updater test strategies
- Headless CI configuration (xvfb, GitHub Actions)
- Screenshot and visual regression testing
- Spectron migration path

---

<philosophy>

## Philosophy

Electron testing splits along the same boundaries as the Electron process model:

1. **E2E tests** launch the full application with Playwright and exercise the complete flow -- main process, preload, renderer, and IPC together. These are slow but high-confidence.
2. **Main process unit tests** mock the `electron` module and test IPC handlers, lifecycle logic, and business logic in isolation. These are fast and catch logic bugs early.
3. **Renderer tests** are standard web tests -- the renderer is Chromium. Use your existing web testing approach.

**Guiding principle:** Test main process logic with unit tests, test integration through IPC with E2E, and test renderer UI with standard web tools. Don't try to unit test IPC communication itself -- the framework handles message passing. Test that your handlers produce the correct results given inputs.

**When to use E2E (Playwright):**

- Full user workflows (open file, edit, save)
- IPC round-trips that span main and renderer
- Window management (multi-window, modals, frameless)
- Visual regression / screenshot comparison
- Auto-update UI flow

**When to use unit tests:**

- IPC handler logic (validate input, produce output)
- Main process business logic (file operations, data processing)
- Preload API shape (correct channels exposed)
- Configuration and startup logic

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Playwright E2E -- Launch and Basic Assertions

Launch the Electron app, get the first window, and run assertions. Always close in teardown.

```typescript
import { test, expect, _electron as electron } from "@playwright/test";
import type { ElectronApplication, Page } from "@playwright/test";

let electronApp: ElectronApplication;
let window: Page;

test.beforeEach(async () => {
  electronApp = await electron.launch({ args: ["dist/main.js"] });
  window = await electronApp.firstWindow();
});

test.afterEach(async () => {
  await electronApp.close();
});

test("shows main window with title", async () => {
  const title = await window.title();
  expect(title).toBe("My App");
  await expect(window.locator("h1")).toHaveText("Welcome");
});
```

**Why good:** `afterEach` guarantees cleanup, `firstWindow()` waits for the window to load, standard Playwright assertions work on the Page object

See [examples/core.md](examples/core.md) for evaluate(), multi-window, and environment variable patterns.

---

### Pattern 2: Main Process Evaluation

Use `electronApp.evaluate()` to execute code in the main process context and access Electron APIs.

```typescript
test("returns correct app version", async () => {
  const version = await electronApp.evaluate(async ({ app }) => {
    return app.getVersion();
  });
  expect(version).toMatch(/^\d+\.\d+\.\d+$/);
});

test("app path is set correctly", async () => {
  const appPath = await electronApp.evaluate(async ({ app }) => {
    return app.getAppPath();
  });
  expect(appPath).toContain("dist");
});
```

**Why good:** `evaluate()` receives the Electron `module` object (containing `app`, `BrowserWindow`, etc.) as its first argument, runs in the real main process, returns serializable values

See [examples/core.md](examples/core.md) for browserWindow handle access and process-level assertions.

---

### Pattern 3: Unit Testing IPC Handlers

Extract handler logic into pure functions, then unit test those functions. Mock the `electron` module so it doesn't fail outside the Electron runtime.

```typescript
// main/handlers/file-handler.ts -- extracted pure logic
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const ALLOWED_EXTENSIONS = [".txt", ".md", ".json"];

export async function handleReadFile(
  filePath: string,
): Promise<{ success: boolean; content?: string; error?: string }> {
  const ext = path.extname(filePath);
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return { success: false, error: `Unsupported extension: ${ext}` };
  }
  const content = await readFile(filePath, "utf-8");
  return { success: true, content };
}
```

```typescript
// main/handlers/file-handler.test.ts
import { describe, it, expect } from "vitest";
import { handleReadFile } from "./file-handler.js";

describe("handleReadFile", () => {
  it("rejects unsupported extensions", async () => {
    const result = await handleReadFile("/tmp/file.exe");
    expect(result).toStrictEqual({
      success: false,
      error: "Unsupported extension: .exe",
    });
  });
});
```

**Why good:** Handler logic is a pure function with no Electron dependency, testable with any test runner, no mocking required

See [examples/core.md](examples/core.md) for the full IPC registration pattern and wiring handlers to `ipcMain.handle`.

---

### Pattern 4: Mocking the Electron Module

When main process code imports directly from `electron`, mock the module in your test runner so tests don't fail outside the Electron runtime.

```typescript
// test setup file -- mock the electron module globally
vi.mock("electron", () => ({
  app: {
    getPath: vi.fn().mockReturnValue("/tmp/mock-app-data"),
    getVersion: vi.fn().mockReturnValue("1.0.0"),
    whenReady: vi.fn().mockResolvedValue(undefined),
  },
  BrowserWindow: vi.fn().mockImplementation(() => ({
    loadFile: vi.fn(),
    webContents: { send: vi.fn() },
    on: vi.fn(),
  })),
  ipcMain: {
    handle: vi.fn(),
    on: vi.fn(),
    removeHandler: vi.fn(),
  },
  dialog: {
    showOpenDialog: vi.fn(),
    showSaveDialog: vi.fn(),
    showMessageBox: vi.fn(),
  },
}));
```

**Why good:** Provides minimal stubs for common Electron APIs, tests run in Node.js without Electron runtime, each mock returns sensible defaults

See [examples/mocking.md](examples/mocking.md) for per-test overrides and more granular mock patterns.

---

### Pattern 5: Dialog Stubbing in E2E Tests

Native dialogs cannot be interacted with by Playwright. Stub them via `evaluate()` before triggering the dialog.

```typescript
test("opens a file via dialog", async () => {
  // Stub the dialog before the UI triggers it
  await electronApp.evaluate(async ({ dialog }) => {
    dialog.showOpenDialog = async () => ({
      canceled: false,
      filePaths: ["/tmp/test-file.txt"],
    });
  });

  // Click the button that triggers showOpenDialog
  await window.click('button[data-testid="open-file"]');
  await expect(window.locator('[data-testid="file-name"]')).toHaveText(
    "test-file.txt",
  );
});
```

**Why good:** Stubs the dialog module in the running main process, returns controlled data, test can verify the downstream UI effect

See [examples/e2e-patterns.md](examples/e2e-patterns.md) for save dialog, message box, and `electron-playwright-helpers` library patterns.

---

### Pattern 6: Headless CI Configuration

Electron requires a display server. On Linux CI, use `xvfb-run` or the cross-platform `xvfb-maybe` wrapper.

```yaml
# GitHub Actions example
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: xvfb-run --auto-servernum -- npx playwright test
```

**Key point:** `xvfb-run --auto-servernum` creates a virtual display and sets `$DISPLAY` automatically. On macOS/Windows runners, `xvfb-run` is not needed -- Electron has native display access. `xvfb-maybe` wraps this cross-platform: it applies xvfb on Linux and does nothing elsewhere.

See [examples/e2e-patterns.md](examples/e2e-patterns.md) for the full CI matrix and `xvfb-maybe` npm script pattern.

---

### Pattern 7: Screenshot and Visual Regression Testing

Playwright's `toHaveScreenshot()` works with Electron windows for visual regression testing.

```typescript
test("main window matches screenshot", async () => {
  // Wait for the UI to stabilize
  await window.waitForLoadState("domcontentloaded");
  await expect(window).toHaveScreenshot("main-window.png", {
    maxDiffPixelRatio: 0.01,
  });
});

test("dialog state matches screenshot", async () => {
  await window.click('button[data-testid="open-settings"]');
  await window.waitForSelector('[data-testid="settings-panel"]');
  await expect(
    window.locator('[data-testid="settings-panel"]'),
  ).toHaveScreenshot("settings-panel.png");
});
```

**Key point:** Run screenshot tests on a single OS in CI (Linux with xvfb) for consistent baselines. Cross-OS font rendering differences cause false positives. Use `maxDiffPixelRatio` or `maxDiffPixels` for tolerance.

</patterns>

---

<decision_framework>

## Decision Framework

### What to Test Where

```
What are you testing?
+-- Full user workflow (open, edit, save, multi-window)?
|   +-- Playwright E2E (launch real app)
+-- Main process handler logic (validate input, transform data)?
|   +-- Unit test with mocked electron module
+-- Preload script API shape?
|   +-- Unit test with mocked contextBridge/ipcRenderer
+-- Renderer UI components?
|   +-- Standard web testing tools (not Electron-specific)
+-- IPC round-trip (main <-> renderer)?
|   +-- Playwright E2E (tests the real channel)
+-- Dialog/menu interactions?
|   +-- Playwright E2E with stubbed dialogs
+-- Visual appearance?
|   +-- Playwright screenshot comparison
+-- Auto-update flow?
    +-- Mock event emission in unit tests + real staging server for integration
```

### Mocking Decision

```
Does your code import from "electron"?
+-- YES: Is the logic separable from Electron APIs?
|   +-- YES --> Extract pure function, test without mocking
|   +-- NO  --> Mock the electron module (use your test runner's module mocking)
+-- NO: Standard Node.js code
    +-- Test normally, no special setup needed
```

</decision_framework>

---

**Detailed resources:**

- [examples/core.md](examples/core.md) - Playwright launch, evaluate, firstWindow, IPC handler unit testing, preload testing
- [examples/e2e-patterns.md](examples/e2e-patterns.md) - Dialog stubbing, CI setup, screenshot testing, auto-update testing, multi-window
- [examples/mocking.md](examples/mocking.md) - Mocking electron module, ipcMain/ipcRenderer, BrowserWindow, dialog, contextBridge
- [reference.md](reference.md) - Playwright Electron API quick reference, Spectron migration, test runner comparison

---

<red_flags>

## RED FLAGS

**Critical Issues:**

- Not closing `electronApp` in test teardown -- leaked processes accumulate, break CI, and cause port conflicts
- Running Electron E2E tests on Linux CI without xvfb -- tests fail immediately with "no display" errors
- Testing IPC communication logic itself rather than handler outcomes -- the framework handles message passing, test your business logic
- Using Spectron for Electron 24+ -- Spectron is unmaintained and incompatible with modern Electron

**Architecture Issues:**

- Putting all test logic in E2E tests when unit tests would suffice -- E2E is slow, unit test handler logic separately
- Mocking `ipcRenderer` in E2E tests -- E2E tests use the real IPC channel; mock only native OS APIs (dialogs, menus)
- Testing renderer components through Electron launch -- renderer is standard Chromium, test with web tools for speed
- Coupling handler logic directly to `ipcMain.handle` registration -- extract handlers to pure functions for testability

**Common Mistakes:**

- Forgetting `await electronApp.firstWindow()` returns a `Page`, not a `BrowserWindow` -- use Playwright page API, not Electron window API
- Assuming `evaluate()` can return non-serializable values (functions, DOM nodes) -- it serializes via JSON
- Hardcoding file paths in E2E dialog stubs -- use `path.join(os.tmpdir(), ...)` or test fixtures
- Not waiting for window load before assertions -- use `waitForLoadState()` or `waitForSelector()` before checking content

**Gotchas & Edge Cases:**

- `_electron.launch()` uses the `electron` binary from `node_modules/.bin/` by default -- set `executablePath` if your app bundles a different Electron version
- Playwright Electron support is marked "experimental" -- API may change between major Playwright versions
- `electronApp.evaluate()` receives the Electron module object (not `require("electron")`) as its first argument -- destructure `{ app }`, `{ dialog }`, etc.
- Screenshot baselines differ across OSes due to font rendering -- pin to one OS in CI or use per-OS baselines
- `BrowserWindow` handle from `electronApp.browserWindow(page)` returns a `JSHandle`, not a direct object -- call methods via `evaluate` on the handle
- `ipcMain.handle` can only have one handler per channel -- calling `handle` twice on the same channel throws; use `removeHandler` first in tests

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST `await electronApp.close()` in test teardown -- leaked Electron processes break CI and consume resources)**

**(You MUST mock the `electron` module in unit tests -- Electron APIs are only available inside the Electron runtime)**

**(You MUST use `xvfb-run` or `xvfb-maybe` for headless Linux CI -- Electron requires a display server)**

**(You MUST stub native dialogs in E2E tests -- `showOpenDialog`/`showSaveDialog` block the process and cannot be interacted with by Playwright)**

**Failure to follow these rules will cause leaked processes, CI failures, and untestable dialog interactions.**

</critical_reminders>
