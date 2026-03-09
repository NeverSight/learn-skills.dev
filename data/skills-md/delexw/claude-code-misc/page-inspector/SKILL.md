---
name: page-inspector
description: Capture current page layout, styles, and structure from a live web page using Chrome DevTools MCP. Use when you need to understand the existing UI before making changes — captures screenshots, DOM structure, computed styles, and layout properties. Useful as a pre-implementation baseline for frontend or UI-affecting changes.
argument-hint: URL [OUT_DIR] (e.g. "http://localhost:3000/page ./output")
allowed-tools: mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__emulate, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__select_page, mcp__chrome-devtools__resize_page, mcp__chrome-devtools__wait_for, Read, Write, Edit, Bash
model: sonnet
context: fork
---

# Page Inspector — Capture Current Page Layout & Styles

Connects to a running Chrome browser session via Chrome DevTools MCP, navigates to the target page, and captures a comprehensive snapshot of the current layout, styles, and structure. This output serves as a baseline reference for implementation.

## Arguments
- `$ARGUMENTS[0]` — Target URL to inspect (e.g. `http://localhost:3000/page`)
- `$ARGUMENTS[1]` — (optional) Output directory. Defaults to `./page-inspector-output`

## Prerequisites

1. Chrome running with remote debugging enabled (or Chrome DevTools MCP server configured)
2. Target page accessible (dev server running)
3. If the page requires authentication, attempt to find credentials from environment variables. If none are found or authentication fails, skip the inspection

## Execution

### 1. Connect & Navigate

- List available pages via `list_pages`
- Navigate to `$ARGUMENTS[0]` or select it if already open
- **Clear the page cache and hard-refresh** before inspecting:
  ```js
  // Run via evaluate_script to clear page cache and hard-refresh
  caches.keys().then(names => names.forEach(name => caches.delete(name)));
  location.reload(true);
  ```
- Wait for the page to fully reload

### 2. Capture Desktop Screenshot

- Take a full-page screenshot at the current viewport width
- Save to `$ARGUMENTS[1]/screenshots/desktop.png`

### 3. Capture Key Viewport Screenshots

Take screenshots at these widths to capture responsive breakpoints:
- 1440px (desktop large)
- 1024px (tablet landscape)
- 768px (tablet portrait)
- 375px (mobile)

Save each to `$ARGUMENTS[1]/screenshots/{width}px.png`

### 4. Inspect Layout Structure

Use `evaluate_script` to extract:
- Key layout containers and their CSS display/position properties
- Flex/grid configurations on major layout elements
- Any fixed/sticky positioned elements
- Overall page structure (header, nav, main content, sidebar, footer)

### 5. Inspect Computed Styles

For the main content area and key UI elements, capture:
- Font families, sizes, weights, line heights
- Colors (text, background, borders)
- Spacing (margins, paddings)
- Box sizing and dimensions

### 6. Write Output

Create `$ARGUMENTS[1]/output.md` with:

```markdown
# Page Inspector Report: {url}

## Screenshots
- Desktop (current): `screenshots/desktop.png`
- 1440px: `screenshots/1440px.png`
- 1024px: `screenshots/1024px.png`
- 768px: `screenshots/768px.png`
- 375px: `screenshots/375px.png`

## Page Structure
{DOM structure overview — key containers and their roles}

## Layout Properties
{CSS display, grid/flex configs, positioning for key elements}

## Typography & Colors
{Font stacks, sizes, color palette observed}

## Spacing & Dimensions
{Key measurements observed}

## Notes
{Any observations relevant to upcoming changes}
```

Ensure `mkdir -p $ARGUMENTS[1]/screenshots` before writing files.
