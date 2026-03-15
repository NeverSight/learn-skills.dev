---
name: browse
description: |
  Browser automation workflow built on the `agent-browser` CLI. Use when you need to open pages, inspect content, click through flows, fill forms, capture screenshots, inspect console or network activity, or compare pages.
---

# browse

Use `agent-browser` directly for browser automation. Keep commands explicit and prefer the built-in session model instead of adding a second wrapper layer.

## Requirements

- `agent-browser` must be available on `PATH`.
- If browser binaries are missing, run `agent-browser install`.
- Reuse the default session unless isolation matters; close it with `agent-browser close` when the workflow is finished.

## Default Flow

```bash
agent-browser open https://example.com
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Use `snapshot -i` when selectors are unclear, then interact with `@ref` targets from the snapshot output.

## Command Map

```bash
# Open or navigate
agent-browser open https://example.com
agent-browser back
agent-browser forward
agent-browser reload

# Inspect content
agent-browser get title
agent-browser get url
agent-browser get text body
agent-browser get html main
agent-browser snapshot -i

# Interact
agent-browser click @e3
agent-browser fill @e4 "test@example.com"
agent-browser type @e5 "hello"
agent-browser press Enter
agent-browser select @e6 option-a
agent-browser upload @e7 /tmp/file.png
agent-browser wait @e8

# Visual checks
agent-browser screenshot /tmp/page.png
agent-browser screenshot --full /tmp/page-full.png
agent-browser pdf /tmp/page.pdf

# Debugging
agent-browser console
agent-browser errors
agent-browser network requests
agent-browser eval "document.title"

# State and tabs
agent-browser cookies get
agent-browser storage local get
agent-browser tab new
agent-browser tab list
agent-browser tab 2
agent-browser close
```

## Working Rules

- Prefer `wait --load networkidle` after navigation-heavy steps.
- Prefer `snapshot -i` before `click`, `fill`, or `select` when the page is not stable enough for CSS selectors.
- Use `console`, `errors`, and `network requests` before concluding that a page is broken.
- Use `--profile <path>` when a persistent login or browser profile matters.
- Use `--session <name>` when separate browser contexts are required in the same task.
- If `agent-browser` is missing, tell the user exactly how to install it before continuing.
