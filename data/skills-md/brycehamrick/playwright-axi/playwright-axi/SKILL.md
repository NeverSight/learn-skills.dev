---
name: playwright-axi
description: "Agent-ergonomic browser automation over the Playwright engine — navigate, click, fill, extract, screenshot, inspect console/network, manage sessions. Use whenever a task needs a real browser; prefer fetch/curl-style tools for static pages."
---

# playwright-axi

Browser automation for coding agents, built on the `playwright` npm package's
agent CLI with AXI ergonomics: TOON output, combined operations (action +
fresh snapshot in one call), inline filtered snapshots, and structured errors
with clean exit codes.

## Running it

```
npx -y playwright-axi@latest <command> [args] [flags]
```

Or install once: `npm install -g playwright-axi`, then run `playwright-axi <command>`.

If no browser is installed yet, run `playwright-axi install` (Chromium) first.
To keep installs lean, `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install -g playwright-axi`
skips the automatic browser download; `playwright-axi install chromium` adds it later.

## When to use this vs. simpler tools

- **Use playwright-axi** when the task needs a real browser: clicking through
  flows, filling forms, SPAs, pages behind auth, JavaScript-rendered content,
  screenshots/PDFs, console errors, or network inspection.
- **Do not use it** for static pages, APIs, or JSON endpoints — fetch/curl-style
  tooling is cheaper and faster. Do not spin up a browser to read a file.

## Core loop

Every action returns the fresh page state, so you rarely need a separate
snapshot call:

```
playwright-axi open https://example.com
→ page: {url, title} + inline snapshot with [ref=eN] + next-step help

playwright-axi click e6 --query "sign in"     # act + filter what matters
playwright-axi fill e12 "hello" --submit      # fill + Enter + fresh snapshot
playwright-axi find "pricing"                 # grep the snapshot with context
playwright-axi eval "document.title"          # run JS on the page
playwright-axi screenshot                     # save PNG, path is returned
```

`--query <text>` filters any snapshot output to matching lines: every
whitespace-separated term must appear in the line (case-insensitive).
Long snapshots are truncated by default; use `--full` when you truly need
everything, or `--query` to stay focused.

## Element targeting

Use `[ref=eN]` values from the most recent snapshot or `find` result, e.g.
`click e21`. Refs are only valid against the latest snapshot taken in the
session; if the page navigated, refs go stale and the CLI fails loudly with
`STALE_REF` — take a fresh `snapshot` and retry. CSS selectors and Playwright
locators (`getByRole(...)`) also work as targets.

## Command families

| Family | Commands |
| --- | --- |
| Session | open, attach, detach, close, sessions, close-all, kill-all, delete-data (--confirm), install, show |
| Navigation | goto, go-back, go-forward, reload |
| Snapshot & inspection | snapshot, find, eval, generate-locator, highlight |
| Interaction | click, dblclick, fill, type, press, keydown/keyup, hover, select, check/uncheck, drag, drop, upload, dialog-accept/dismiss, resize |
| Mouse (coordinates) | mousemove, mousedown, mouseup, mousewheel |
| Tabs | tab-list, tab-new, tab-close, tab-select |
| Capture | screenshot, pdf (Chromium), state-save, state-load |
| Cookies & storage | cookie-*, localstorage-*, sessionstorage-* |
| Console & network | console, requests, request, request-headers/body, response-headers/body, route, route-list, unroute, network-state-set |
| DevTools | run-code, recording-*, tracing-*, video-*, pause-at, resume, step-over |
| WebMCP (experimental) | webmcp-list, webmcp-call |

Run `playwright-axi --help` for the full list and
`playwright-axi <command> --help` for exact arguments.

## Sessions

Each browser is a named session. Pass `--session <name>` (or set
`PLAYWRIGHT_AXI_SESSION`) to isolate work, e.g. one session per app under
test. `playwright-axi sessions` lists live sessions with their current page.
Headless sessions shut down after an hour idle; `open` starts a new one.

Browsers default to headless Chromium. `open --browser firefox`, `--headed`,
`--mobile`, `--device "iPhone 15"`, and `--persistent` change that.

## Output contract

- Default output is compact TOON text; `--json` switches any command to JSON.
- Exit codes: `0` success, `2` usage error (unknown flag, missing argument),
  `1` runtime error (navigation failure, stale ref, no session, timeout).
- Empty results are explicit (`sessions: 0`, `matches: 0`), never blank.
- Every mutation that deletes persisted data (`delete-data`) requires `--confirm`.

## Ambient context (optional)

```
playwright-axi setup hooks
```

installs a SessionStart hook (Claude Code, Codex, OpenCode) that surfaces the
live browser-session dashboard at the start of each agent session.
