---
name: macos-safari-browser-use
description: Use Safari.app on macOS through agent-safe commands for tabs, windows, URLs, page extraction, DOM JavaScript, Reading List, screenshots, and Safari WebDriver setup.
---

# macOS Safari Browser Use

Use this skill when the user needs an agent to operate **Safari.app on macOS**: open pages, inspect tabs, read page text, extract links, run explicit DOM JavaScript, click/type into page elements, or prepare Safari WebDriver.

## Non-negotiables

1. Use only public entrypoints:
   - `macos-safari-browser-use/scripts/check-setup.sh`
   - `macos-safari-browser-use/scripts/safari`
   - `macos-safari-browser-use/scripts/commands/**`
2. Treat browsing state as private user data.
   - Do not read or export Safari History, cookies, passwords, Keychain data, or profile internals.
3. Require explicit user intent for write actions:
   - opening/closing tabs or windows;
   - clicking or typing in pages;
   - adding Reading List items;
   - enabling WebDriver remote automation.
4. Never run JavaScript from an untrusted page. Only run JavaScript that you or the user supplied for the current task.

## Quick start

```bash
# Verify macOS, Safari, osascript, JavaScript-from-Apple-Events, and WebDriver status.
macos-safari-browser-use/scripts/check-setup.sh

# List state.
macos-safari-browser-use/scripts/safari windows
macos-safari-browser-use/scripts/safari tabs
macos-safari-browser-use/scripts/safari current

# Navigate.
macos-safari-browser-use/scripts/safari open https://example.com current
macos-safari-browser-use/scripts/safari open https://example.com new-tab
macos-safari-browser-use/scripts/safari open https://example.com new-window

# Read the active page.
macos-safari-browser-use/scripts/safari wait 15
macos-safari-browser-use/scripts/safari title
macos-safari-browser-use/scripts/safari url
macos-safari-browser-use/scripts/safari text
macos-safari-browser-use/scripts/safari links

# Run explicit JavaScript in the current tab.
macos-safari-browser-use/scripts/safari js 'document.title'
macos-safari-browser-use/scripts/safari js-json '({title: document.title, href: location.href})'

# DOM interaction: use only when explicitly requested.
macos-safari-browser-use/scripts/safari click 'button[type="submit"]'
macos-safari-browser-use/scripts/safari type 'input[name="q"]' 'search terms'
```

## Command wrappers

The consolidated CLI and wrappers are equivalent:

```bash
macos-safari-browser-use/scripts/safari tabs
macos-safari-browser-use/scripts/commands/tab/list.sh

macos-safari-browser-use/scripts/safari open https://example.com new-tab
macos-safari-browser-use/scripts/commands/url/open.sh https://example.com new-tab
```

All public commands return JSON on success and failure.

## What to read next

- `macos-safari-browser-use/references/command-reference.md` — full command inventory and JSON shapes.
- `macos-safari-browser-use/references/permissions-and-setup.md` — Automation, JavaScript-from-Apple-Events, WebDriver, screenshots, troubleshooting.
- `macos-safari-browser-use/references/automation-patterns.md` — page-load, selector, JavaScript, screenshot, and WebDriver patterns.
- `macos-safari-browser-use/references/workflows.md` — end-to-end browser-use recipes.
- `macos-safari-browser-use/references/research-and-validation.md` — web research summary.

## Tool choice

| Need | Prefer | Reason |
|---|---|---|
| lightweight Safari tab/window use | `scripts/safari` or wrappers | Low dependency, direct Safari Apple Events. |
| extract current page text/links | `text`, `links`, `query`, `js` | Uses Safari’s DOM in the already-open page. |
| formal repeatable web tests | `safaridriver` / WebDriver | Standards-based automation and test assertions. |
| change Safari settings/profiles | manual user steps or MDM | Stable APIs are limited; UI scripting is brittle. |

## Safety boundary

Prefer read-only commands first: `windows`, `tabs`, `current`, `title`, `url`, `text`, `links`. For destructive or state-changing actions, restate the target tab/window and act only after the user’s request is concrete.
