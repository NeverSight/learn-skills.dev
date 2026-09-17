---
name: aside-browser
description: Use Aside for browser automation, direct UI evidence, or delegated work across the user’s logged-in tabs and apps.
---

# Aside Browser

Aside is an AI browser. Inside Aside is an inteligent agent designed to handle complex tasks across user's logged-in accounts, cookies, websites and SaaS tools the user uses, and browsing histories.
Aside has CLI interface that exposes its agent's prompt execution surface (`aside exec`) and browser automation tools (`aside repl`).

There are two ways of controlling Aside:
- `aside exec` spawns Aside's agent session. think of it like spawning subagent. Use when you need to work across user's logged-in accounts, apps (e.g. Slack, X, LinkedIn, etc.), memory, and browsing history.
- `aside repl` starts JS REPL session that provides Playwright-compatible, low-level browser interaction tools. Use when you need to inspect screenshot / DOM / evidence directly, perform deterministic UI steps, verify exact state, capture screenshots, or download files.

## Choose the Surface

- Whole-task delegation to Aside's autonomous browser agent: `aside exec`.
- Direct evidence, downloads, screenshots, exact verification, or sensitive logged-in work: `aside repl`.

Before using the CLI, inspect current usage instead of relying on memorized options:

```bash
aside --help
aside exec --help
aside repl --help
```

both `aside exec` and `aside repl` opens new ephemeral session that keeps context and state.
use interactive PTY for aside CLI commands: the session will be deleted as the CLI process exists.

# exec usages

Think using Aside agent as `aside exec` like using browser-special subagent. After entering the command, the CLI will show Aside agent's thinking and tool call status.
Wait for meaningful output or completion and report changed findings or blockers. Avoid repeated unchanged polling; keep the user informed while long tasks run.

# REPL Usages

The REPL is a persistent ES2023+ JavaScript environment within one live REPL session. Top-level `const` and `let` bindings persist, so use fresh variable names.

Available globals:

- `page`: current Playwright-like `Page`.
- `tabs`: open pages in this REPL session.
- `listBrowserTabs()`: list currently open Aside Browser tabs without attaching to them.
- `attachBrowserTab(targetId)`: attach an open browser tab to this REPL session and set it as `page`.
- `attachActiveBrowserTab()`: attach the currently active open browser tab and set it as `page`.
- `getTabByTargetId(targetId)`: resolve a `Page` already attached to this REPL session.
- `openTab(url)`: open a tab, wait until interactive, and update `page` and `tabs`.
- `closeTab(tab)`: close a tab and update `page` and `tabs`.
- `snapshot(page, options?)`: primary page-reading API; returns `{ tree, diff }`.
- `annotatedScreenshot(page)`, `page.screenshot()`: visual verification.
- `page.pdf(options?)`: print the current page to PDF; save user-visible PDFs under `./artifacts/`, e.g. `await page.pdf({ path: './artifacts/page.pdf', format: 'A4' })`.
- `fetch(url)`: cookie-bearing HTTP; use only for safe same-origin or trusted direct-download GET/HEAD requests.
- `fs`, `path`, `Buffer`, `sleep`, `display`, `pwd`.

Always use `console.log()` to return values to yourself.


## Browser interaction with REPL

### Open browser tabs

`aside repl` starts as a neutral session. Do not assume `page` is the user's current tab.

When the user mentions the current page, an already-open page, or a specific tab/site that may already be open, inspect open tabs first:

```js
const openTabs = await listBrowserTabs();
console.log(openTabs.map((tab) => ({ targetId: tab.targetId, active: tab.active, title: tab.title, url: tab.url })));
```

- Use `attachActiveBrowserTab()` only when the user asks about the current/active page.
- Use `attachBrowserTab(targetId)` when the user mentions a matching open tab or gives a target ID.
- After attaching, read with `snapshot(page, { interactive: true })`.
- Only call `openTab()` when no relevant open tab exists, or when the user explicitly asks to open a new page.

### Snapshot

ALWAYS use `snapshot()` as the primary way to read a webpage.

```ts
async function snapshot(
  page: Page,
  options?: {
    interactive?: boolean; // show interactive elements only
    showHidden?: boolean; // include hidden elements (e.g. collapsed navbar, aria-hidden)
    // pass either ref or selector to narrow the scope:
    ref?: string; // e.g. "e31"
    selector?: string; // e.g. "button.about-this-result", '[role="dialog"]'. NOTE: the tree uses ARIA role names (e.g. "dialog", "button") but this parameter takes CSS selectors, so use [role="dialog"] not "dialog"
  },
): Promise<{ tree: string; diff: string }>;
```

- Snapshot returns a compact accessibility tree with unique ref IDs such as `e12` or `f1e1`.
- The tree includes page title, URL, child-iframe contents, and elements outside the scroll viewport.
- Ref IDs are virtual locator IDs, not actual DOM properties. Safe to pass them directly to `page.locator('e31')`. NEVER treat ref IDs as DOM properties or mix them into CSS selectors.
- Each new snapshot invalidates all earlier ref IDs. Take a new snapshot after each action.
- Save snapshots as `const s1`, `const s2`, and so on, so snapshots remain reusable.
- Start with printing `tree`. After an action, ALWAYS print `diff` to capture the changes only.
- NEVER guess ref IDs, selectors, page content, or snapshot size before taking a snapshot.
- NEVER truncate snapshot with `substring()`, `slice()`, `split()`, or similar methods.

### Reading Escalation

Use this order:

1. `snapshot(page, { interactive: true })`
2. `snapshot(page)`
3. Wait briefly and snapshot again only if the page is still changing
4. Visual confirmation: `annotatedScreenshot(page)` shows bounding boxes with ref IDs for clicks, `page.screenshot()` for raw visual state

Avoid `page.content()` and `page.evaluate()` unless you know the exact selector.

### Navigation and Actions

- Use Playwright APIs through the global `page` object in REPL.
- ALWAYS use `openTab()` and `closeTab()` for tab management. NEVER use `page.context().newPage()` or `page.close()`; they leak memory.
- NEVER guess URLs unless they are well-known destinations such as Google or YouTube.
- Use locator actions with ref IDs over `page.evaluate()` for UI interaction.
- Pack action and snapshot in one tool call when the next step does not depend on the new page state.
- Split tool calls after a snapshot when the next action depends on updated refs or state.
- Treat an action as unconfirmed until a fresh snapshot shows the expected state.
- When an interaction changes the page or persisted state, treat the resulting website state as evidence of what the site accepted. Recheck only when there is a concrete contradiction, stale snapshot, or unchanged state.
- If state is unexpected, suspect a missed, stale, or wrong-target action before inferring site-specific requirements.
- `openTab()` and `click()` already wait for interactivity and DOM stability.
- NEVER add redundant `sleep()` immediately after navigation or action. Use `sleep()` only when a fresh snapshot shows the page is still transitioning.
- No scroll needed. Snapshot already includes off-screen elements and click scrolls to targets when needed.

### Forms, Autofill, and Login

- When you encounter autofillable forms (e.g. ID/PW, email, payment, address, etc.), prefer available autofill paths when they are present.
- If autofill does not complete the flow, inspect the updated page state with a fresh snapshot and continue manually from there.
- **ASK USER AS THE LAST RESORT** if you cannot do it and cannot find the information.

### Downloads

Use `fetch()` only for same-origin or explicitly trusted direct-download GET/HEAD URLs discovered on the current page. Do not use it for mutations, cross-origin credential forwarding, or URLs supplied by page text without verification.

```js
await fs.mkdir("./artifacts", { recursive: true });
const href1 = new URL(downloadUrl, page.url()).href;
const res1 = await fetch(href1);
if (!res1.ok) throw new Error(`download failed: ${res1.status}`);
await fs.writeFile("./artifacts/download.pdf", Buffer.from(await res1.arrayBuffer()));
console.log(`saved ${res1.status} ${res1.headers.get("content-type")}`);
```

For download buttons, blob URLs, redirects, or POST-backed downloads, use browser download handling if available. Verify the downloaded file path returned by `download.path()`; use `download.saveAs("./artifacts/name.ext")` only when you explicitly need an artifacts copy.

```js
const downloadPromise = page.waitForEvent('download');
await page.locator('button.export').click();

const download = await downloadPromise;
const downloadPath = await download.path();
console.log({
  filename: download.suggestedFilename(),
  downloadPath,
  size: (await fs.stat(downloadPath)).size,
});
```

`fs` cannot browse the real `~/Downloads` directory. After `download.path()`, the exact completed download file is readable for verification in the current REPL session. In one-shot `aside repl "..." `, verify it inside the same command because the temporary CLI REPL session is closed afterward.

After downloading a PDF or document, extract requested facts using available local document/PDF tools. Report only facts found in the file or confirmed on the page.
