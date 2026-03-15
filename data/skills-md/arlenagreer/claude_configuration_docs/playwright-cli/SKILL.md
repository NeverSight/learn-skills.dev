---
name: playwright-cli
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, extract information from web pages, debug web apps, record browser sessions as video, mock or intercept API requests, manage browser cookies/localStorage, generate Playwright test code, capture execution traces, or run multiple browser sessions concurrently.
allowed-tools: Bash(playwright-cli:*)
---

# Browser Automation with playwright-cli

## How it works

Every command returns a **snapshot** — a structured view of the page with element refs (e1, e2, e3...). Use these refs to target elements in subsequent commands. Always take a snapshot before interacting with unfamiliar page state.

## Quick start

```bash
# open new browser
playwright-cli open
# navigate to a page
playwright-cli goto https://playwright.dev
# take a snapshot to see element refs
playwright-cli snapshot
# interact with the page using refs from the snapshot
playwright-cli click e15
playwright-cli type "page.click"
playwright-cli press Enter
# take a screenshot (rarely used, as snapshot is more common)
playwright-cli screenshot
# close the browser
playwright-cli close
```

## Commands

### Core

```bash
playwright-cli open
# open and navigate right away
playwright-cli open https://example.com/
playwright-cli goto https://playwright.dev
playwright-cli type "search query"
playwright-cli click e3
playwright-cli dblclick e7
playwright-cli fill e5 "user@example.com"
playwright-cli drag e2 e8
playwright-cli hover e4
playwright-cli select e9 "option-value"
playwright-cli upload ./document.pdf
playwright-cli check e12
playwright-cli uncheck e12
playwright-cli snapshot
playwright-cli snapshot --filename=after-click.yaml
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
playwright-cli dialog-accept
playwright-cli dialog-accept "confirmation text"
playwright-cli dialog-dismiss
playwright-cli resize 1920 1080
playwright-cli close
```

### Navigation

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

### Keyboard

```bash
playwright-cli press Enter
playwright-cli press ArrowDown
playwright-cli keydown Shift
playwright-cli keyup Shift
```

### Mouse

```bash
playwright-cli mousemove 150 300
playwright-cli mousedown
playwright-cli mousedown right
playwright-cli mouseup
playwright-cli mouseup right
playwright-cli mousewheel 0 100
```

### Save as

```bash
playwright-cli screenshot
playwright-cli screenshot e5
playwright-cli screenshot --filename=page.png
playwright-cli pdf --filename=page.pdf
```

### Tabs

```bash
playwright-cli tab-list
playwright-cli tab-new
playwright-cli tab-new https://example.com/page
playwright-cli tab-close
playwright-cli tab-close 2
playwright-cli tab-select 0
```

### Storage

```bash
playwright-cli state-save auth.json
playwright-cli state-load auth.json
playwright-cli cookie-list
playwright-cli cookie-set session_id abc123 --domain=example.com --httpOnly --secure
playwright-cli localstorage-set theme dark
```

For full cookie, localStorage, sessionStorage, and IndexedDB operations, see [references/storage-state.md](references/storage-state.md).

### Network

```bash
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
playwright-cli route-list
playwright-cli unroute "**/*.jpg"
playwright-cli unroute
```

### DevTools

```bash
playwright-cli console
playwright-cli console warning
playwright-cli network
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli tracing-start
playwright-cli tracing-stop
playwright-cli video-start
playwright-cli video-stop video.webm
```

## Open parameters
```bash
# Use specific browser when creating session
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit
playwright-cli open --browser=msedge
# Connect to an existing Chrome browser via extension (reuses logged-in sessions)
playwright-cli open --extension

# Use persistent profile (by default profile is in-memory)
playwright-cli open --persistent
# Use persistent profile with custom directory
playwright-cli open --profile=/path/to/profile

# Start with config file
playwright-cli open --config=my-config.json

# Close the browser
playwright-cli close
# Delete user data for the default session
playwright-cli delete-data
```

## Snapshots

After each command, playwright-cli provides a snapshot of the current browser state.

```bash
> playwright-cli goto https://example.com
### Page
- Page URL: https://example.com/
- Page Title: Example Domain
### Snapshot
[Snapshot](.playwright-cli/page-2026-02-14T19-22-42-679Z.yml)
```

You can also take a snapshot on demand using `playwright-cli snapshot` command.

If `--filename` is not provided, a new snapshot file is created with a timestamp. Default to automatic file naming, use `--filename=` when artifact is a part of the workflow result.

## Browser Sessions

```bash
# create new browser session named "mysession" with persistent profile
playwright-cli -s=mysession open example.com --persistent
# same with manually specified profile directory (use when requested explicitly)
playwright-cli -s=mysession open example.com --profile=/path/to/profile
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close  # stop a named browser
playwright-cli -s=mysession delete-data  # delete user data for persistent session

playwright-cli list
# Close all browsers
playwright-cli close-all
# Forcefully kill all browser processes
playwright-cli kill-all
```

## Parallel UAT with Subagents

Named sessions (`-s=name`) provide full process-level isolation, making them ideal for parallel UAT: each subagent gets its own browser with independent cookies, storage, and state.

**Session naming:** Always use `-s=uat-{test-name}` for UAT sessions:

```bash
# Team lead spawns 3 subagents, each with their own session
playwright-cli -s=uat-login open https://app.example.com/login
playwright-cli -s=uat-checkout open https://app.example.com/checkout
playwright-cli -s=uat-settings open https://app.example.com/settings

# After all subagents complete, team lead cleans up
playwright-cli close-all
```

**WARNING:** Do NOT use MCP Playwright tools (`mcp__plugin_playwright_playwright__*`) for parallel testing — all subagents share the same MCP server with a single browser context. Use `playwright-cli` with named sessions instead.

**Resource limit:** Max 3–5 parallel sessions. Monitor with `playwright-cli list`.

See [references/parallel-uat.md](references/parallel-uat.md) for the full workflow including evidence collection, error recovery, and result aggregation.

## Local installation

In some cases user might want to install playwright-cli locally. If running globally available `playwright-cli` binary fails, use `npx playwright-cli` to run the commands. For example:

```bash
npx playwright-cli open https://example.com
npx playwright-cli click e1
```

## Example: Form submission

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot

playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
playwright-cli snapshot
playwright-cli close
```

## Example: Multi-tab workflow

```bash
playwright-cli open https://example.com
playwright-cli tab-new https://example.com/other
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli snapshot
playwright-cli close
```

## Example: Debugging with DevTools

```bash
playwright-cli open https://example.com
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli console
playwright-cli network
playwright-cli close
```

```bash
playwright-cli open https://example.com
playwright-cli tracing-start
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli tracing-stop
playwright-cli close
```

## References

Read these when the specific capability is needed:

* **Request mocking** — Read when intercepting, blocking, or modifying network requests: [references/request-mocking.md](references/request-mocking.md)
* **Running Playwright code** — Read when CLI commands are insufficient and custom page code is needed (geolocation, permissions, iframes, downloads): [references/running-code.md](references/running-code.md)
* **Browser session management** — Read when running multiple concurrent browsers or managing persistent profiles: [references/session-management.md](references/session-management.md)
* **Storage state** — Read when managing cookies, localStorage, sessionStorage, or saving/restoring auth state: [references/storage-state.md](references/storage-state.md)
* **Test generation** — Read when building Playwright test files from interactive browser sessions: [references/test-generation.md](references/test-generation.md)
* **Tracing** — Read when capturing detailed execution traces for debugging (DOM snapshots, network, console): [references/tracing.md](references/tracing.md)
* **Video recording** — Read when recording browser sessions as video for demos or documentation: [references/video-recording.md](references/video-recording.md)
* **Parallel UAT testing** — Read when running multiple subagents for simultaneous user acceptance testing: [references/parallel-uat.md](references/parallel-uat.md)

## Troubleshooting

If `playwright-cli` is not found, fall back to `npx playwright-cli`. If the browser fails to open, try `playwright-cli kill-all` to clear stale processes, then retry.
