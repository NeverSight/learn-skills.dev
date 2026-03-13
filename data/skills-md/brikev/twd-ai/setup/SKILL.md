---
name: setup
description: Configures TWD for a project — detects settings and generates .claude/twd-patterns.md
disable-model-invocation: true
allowed-tools: [Read, Write, Glob, Grep, Bash(npm install *), Bash(npx twd-js init *), AskUserQuestion]
---

# TWD Project Setup

You are configuring TWD (Test While Developing) for this project. Your job is to detect project settings, ask questions for what can't be auto-detected, and generate a `.claude/twd-patterns.md` configuration file.

## Step 1: Auto-Detect Project Settings

Read these files to pre-fill answers (read all in parallel):

1. **`package.json`** — detect framework from dependencies:
   - `react` / `react-dom` → React
   - `vue` → Vue
   - `@angular/core` → Angular
   - `solid-js` → Solid
   - Also detect CSS/component libraries: `@mui/material`, `@chakra-ui/react`, `antd`, `@mantine/core`, `vuetify`, `primevue`, `element-plus`, `@angular/material`

2. **`vite.config.ts`** (or `.js`, `.mjs`) — detect:
   - `base` field (Vite base path, default `/`)
   - `server.port` (dev server port, default `5173`)

3. **`index.html`** — detect entry point from `<script>` src attribute

4. **Glob for `src/services/`, `src/api/`, `src/lib/api`** — detect API/services folder

5. **Check if `public/` directory exists** — confirm public folder name

6. **Detect state management** from `package.json` dependencies:
   - `zustand` → Zustand
   - `@reduxjs/toolkit` or `redux` → Redux
   - `jotai` → Jotai
   - `pinia` → Pinia

7. **Check if `.claude/twd-patterns.md` already exists** — offer to update vs overwrite

## Step 2: Ask Questions

**IMPORTANT: Use the `AskUserQuestion` tool for ALL questions.** This provides an interactive UI experience. Never dump questions as a plain numbered list in text output.

Present auto-detected values as a summary first, then ask questions in two batches:

### Batch 1: Project basics (confirm auto-detected values)

**Do NOT ask individual questions for values you already detected.** Show a single summary of all detected values and ask "Does anything look wrong?" using `AskUserQuestion`. The user only needs to respond if something is incorrect. Example:

> Here's what I detected:
> - Framework: React
> - Vite base path: `/`
> - Dev server port: `5173`
> - Entry point: `src/main.tsx`
> - Public folder: `public/`
> - API services: `src/services/`
> - CSS library: MUI
> - State management: Zustand
>
> Does anything look wrong, or should I continue?

### Batch 2: Testing concerns (need user input)

After confirming batch 1, use `AskUserQuestion` for each of these that requires user input:

1. **CSS library docs** (only if a CSS library was detected): Where are the docs? (URL, local path, or "skip")
2. **Auth middleware**: Does your project have route-based auth/permissions? If yes, briefly describe the pattern.
3. **Third-party modules**: Does your project use external services that need mocking in tests? (e.g., Auth0, Stripe, analytics)
   - If yes: Which modules and how are they imported?
   - The agent needs this to know what to Sinon-stub in tests — "test what you own, mock what you don't"
4. **State reset** (only if state management was detected): How do you reset the store? (e.g., `useStore.setState(initialState)`, `store.$reset()`)
   - TWD runs without page reloads — store state persists between tests and must be reset in beforeEach

## Step 3: Generate `.claude/twd-patterns.md`

Create the `.claude/` directory if it doesn't exist, then write `.claude/twd-patterns.md` with the following sections. **Only include sections that are relevant** — omit sections that don't apply.

```markdown
# TWD Project Patterns

## Project Configuration

- **Framework**: FRAMEWORK
- **Vite base path**: BASE_PATH
- **Dev server port**: PORT
- **Entry point**: ENTRY_FILE
- **Public folder**: PUBLIC_DIR

### Relay Commands

```bash
# Run all tests (default — use this if base path is / and port is 5173)
npx twd-relay run

# Run all tests (custom config)
npx twd-relay run --port PORT --path "BASE_PATH__twd/ws"
```

## Standard Imports

```typescript
import { twd, userEvent, screenDom, expect } from "twd-js";
import { describe, it, beforeEach, afterEach } from "twd-js/runner";
// Project-specific imports go here (added by user)
```

## Visit Paths

All `twd.visit()` calls must include the base path prefix:

```typescript
await twd.visit("BASE_PATH");
await twd.visit("BASE_PATHsome-page");
```

## Standard beforeEach / afterEach

```typescript
beforeEach(() => {
  twd.clearRequestMockRules();
  twd.clearComponentMocks();
  Sinon.restore();
  // STORE_RESET (if applicable — e.g., useStore.setState(initialState), store.$reset())
  // AUTH_SETUP (if applicable)
  // THIRD_PARTY_STUBS (if applicable — e.g., Sinon.stub(authModule, 'useAuth').returns(...))
});

afterEach(() => {
  twd.clearRequestMockRules();
});
```

## API Service Types

Service/API types are located in: `API_FOLDER`

Read files in this folder to understand endpoint URLs and response shapes when writing mock data.

## CSS / Component Library

- **Library**: CSS_LIB
- **Docs**: CSS_DOCS_LOCATION

When writing tests, refer to library docs for correct ARIA roles and component structure.

## Auth Middleware

AUTH_DESCRIPTION

### Route → Permission Mapping

| Route | Required Permissions |
|-------|---------------------|
| (to be filled by developer) | |

## Third-Party Modules

"Test what you own, mock what you don't." These external modules should be stubbed in tests:

| Module | Import Pattern | Stub Strategy |
|--------|---------------|---------------|
| MODULE_NAME | `import { hook } from 'package'` | `Sinon.stub(moduleObj, 'hook').returns(...)` |
| (to be filled by developer) | | |

See the test-writing reference for the default-export object pattern required for ESM stubbing.

## Portals and Dialogs

Use `screenDomGlobal` instead of `screenDom` for elements rendered in portals (modals, dropdowns, tooltips):

```typescript
import { screenDomGlobal } from "twd-js";
const modal = screenDomGlobal.getByRole("dialog");
```
```

### Template rules:
- If base path is `/`, simplify visit paths to just `await twd.visit("/page")`
- If port is `5173` and base path is `/`, use `npx twd-relay run` (no flags)
- Omit the "Auth Middleware" section entirely if no auth
- Omit the "Third-Party Modules" section entirely if no external modules
- Omit the "CSS / Component Library" section if none detected
- Omit the "API Service Types" section if no services folder found
- Omit the `STORE_RESET` comment in beforeEach if no state management library
- Omit the `AUTH_SETUP` comment in beforeEach if no auth middleware
- Omit the `THIRD_PARTY_STUBS` comment in beforeEach if no third-party modules

## Step 4: Optionally Run Setup

After generating the config file, check if TWD is already installed. If not, ask the user if they want to run setup now:

1. `npm install twd-js`
2. `npm install --save-dev twd-relay`
3. `npx twd-js init PUBLIC_DIR --save`
4. Configure entry point — **insert this DEV block BEFORE the existing app mount code** (before `createRoot`, `createApp`, etc.). The import is **`twd-js/bundled`**, NOT `twd-js`:

```typescript
if (import.meta.env.DEV) {
  const { initTWD } = await import('twd-js/bundled');
  const tests = import.meta.glob("./**/*.twd.test.ts");

  initTWD(tests, {
    open: true,
    position: 'left',
    serviceWorker: true,
    serviceWorkerUrl: '/mock-sw.js',
  });

  // Connect twd-relay browser client
  const { createBrowserClient } = await import('twd-relay/browser');
  const client = createBrowserClient({ url: `${window.location.origin}/__twd/ws` });
  client.connect();
}
```

   > **Adjustments**: If Vite `base` is not `/`, update `serviceWorkerUrl` to `'/BASE/mock-sw.js'` and relay URL to `` `${window.location.origin}/BASE/__twd/ws` ``.

5. Add Vite plugins:

```typescript
import { twdHmr } from 'twd-js/vite-plugin';
import { twdRemote } from 'twd-relay/vite';
import type { PluginOption } from 'vite';

// Add to plugins array:
plugins: [
  // ... other plugins
  twdHmr(),
  twdRemote() as PluginOption,
]
```

6. Write a first test file

Only run steps the user approves. Show what each step does before executing.

## Output

When done, summarize:
- Where the config file was written
- What values were detected vs asked
- What setup steps were completed (if any)
- Next steps for the user (e.g., "Run `npm run dev` to see the TWD sidebar")
