---
name: qa-web-test
description: QA web testing skill using Chrome DevTools MCP tools for visual regression testing, responsive breakpoint validation, and CSS layout debugging. Use this skill whenever the user asks to "test a page", "check breakpoints", "verify responsive layout", "QA this page", "test CSS at different viewports", "check for layout bugs", "verify the fix", or wants to visually inspect a web page at specific viewport widths. Also triggers when the user provides a URL and asks to take screenshots, compare layouts, or inspect element dimensions. Works with any Chrome DevTools MCP-connected browser session on localhost or staging environments.
argument-hint: URL [OUT_DIR] (e.g. "http://localhost:3000", "http://localhost:3000 ./qa-reports")
allowed-tools: mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__emulate, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__select_page, mcp__chrome-devtools__resize_page, mcp__chrome-devtools__click, mcp__chrome-devtools__fill, mcp__chrome-devtools__wait_for, Read, Glob, Grep, Bash, Write, Edit
model: sonnet
context: fork
---

# QA Web Testing with Chrome DevTools MCP

Automate visual QA testing of web pages using Chrome DevTools MCP tools. Connects to an
already-running Chrome browser session, navigates to pages, emulates viewports, takes
screenshots, and inspects CSS properties to catch responsive layout bugs.

## Arguments
- `$ARGUMENTS[0]` — Target URL to test (e.g. `http://localhost:3000/page`)
- `$ARGUMENTS[1]` — (optional) Output directory for the QA report and screenshots. Defaults to `./qa-reports`

## Output Location

- Creates or updates `$ARGUMENTS[1]/qa-report-{timestamp}.md` (e.g. `./qa-reports/qa-report-2026-02-27.md`)
- Screenshots are saved to `$ARGUMENTS[1]/screenshots/` (e.g. `./qa-reports/screenshots/page-700px.png`)
- Run `mkdir -p $ARGUMENTS[1]/screenshots` before writing to ensure directories exist.

## Prerequisites

1. Chrome running with remote debugging enabled (or Chrome DevTools MCP server configured)
2. Target page accessible (dev server running, or staging/production URL)
3. If the page requires authentication, attempt to find credentials from environment variables. If none are found or authentication fails, skip the test

## Before You Start

After connecting to the browser and navigating to the target URL, **always hard-refresh the page and clear the cache** before any testing:

```js
// Run via evaluate_script to clear page cache and hard-refresh
caches.keys().then(names => names.forEach(name => caches.delete(name)));
location.reload(true);
```

Then wait for the page to fully reload before proceeding.

## Workflow

Follow these steps in order. Read each step file for detailed instructions.

1. **[Connect to browser](steps/step-01-connect.md)** — List pages and navigate to target URL
2. **[Determine breakpoints](steps/step-02-breakpoints.md)** — Choose viewport widths to test
3. **[Emulate and capture](steps/step-03-emulate-and-capture.md)** — Set viewport, screenshot, inspect dimensions
4. **[CSS inspection](steps/step-04-css-inspection.md)** — Inspect computed styles and container queries
5. **[Visual design inspection](steps/step-04b-visual-inspection.md)** — Check typography, color, spacing, borders, and visibility
6. **[Report results](steps/step-05-report.md)** — Summarize findings with pass/fail table

## Reference Files

| Reference | When to Read |
|-----------|-------------|
| [references/breakpoints.md](references/breakpoints.md) | Common breakpoint values, container query vs media query gotchas |
| [references/css-inspection.md](references/css-inspection.md) | JS snippets for overflow detection, grid/flex inspection, DOM traversal |
