---
name: test-ui
description: "[DevOps & Infra] Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging."
license: Apache-2.0
version: 1.2.0
---

# Chrome DevTools Agent Skill

Browser automation via Puppeteer scripts with persistent sessions. All scripts output JSON.

## Summary

**Goal:** Automate browser interactions, take screenshots, and analyze performance using Puppeteer CLI scripts.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Install | `cd .claude/skills/test-ui/scripts && npm install` |
| 2 | Navigate | `node navigate.js --url <url>` (session persists via `.browser-session.json`) |
| 3 | Interact | `click.js`, `fill.js`, `evaluate.js`, `select-ref.js` |
| 4 | Inspect | `screenshot.js`, `snapshot.js`, `aria-snapshot.js`, `console.js` |
| 5 | Analyze | `performance.js` for Core Web Vitals, `network.js` for HTTP tracking |
| 6 | Close | `node navigate.js --url about:blank --close true` |

**Key Principles:**
- Never use `file://` for local HTML -- serve via `npx serve` instead
- Session persists between scripts; delete `.browser-session.json` to reset
- Source-available sites: read source first for selectors; unknown layouts: use `aria-snapshot.js`

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **⚠️ MUST READ** `references/devtools-patterns.md` — ARIA, screenshots, console, custom scripts
- **⚠️ MUST READ** `references/cdp-domains.md` — CDP domain reference
- **⚠️ MUST READ** `references/puppeteer-reference.md` — Puppeteer API reference
- **⚠️ MUST READ** `references/performance-guide.md` — Performance analysis guide
- **⚠️ MUST READ** `scripts/README.md` — Script options reference

## Choosing Your Approach

| Scenario               | Approach                                           |
| ---------------------- | -------------------------------------------------- |
| Source-available sites | Read source code first, write selectors directly   |
| Unknown layouts        | Use `aria-snapshot.js` for semantic discovery      |
| Visual inspection      | Take screenshots to verify rendering               |
| Debug issues           | Collect console logs, analyze with session storage |

## Quick Start

```bash
cd .claude/skills/test-ui/scripts
npm install
node navigate.js --url https://example.com
# Headless on Linux/WSL/CI; headed on macOS/Windows
# Linux/WSL: Run ./install-deps.sh first for Chrome system libraries
```

## Session Persistence

Browser state persists via `.browser-session.json`. Scripts disconnect but keep browser running.

```bash
node navigate.js --url https://example.com/login
node fill.js --selector "#email" --value "user@example.com"
node click.js --selector "button[type=submit]"
node navigate.js --url about:blank --close true   # Close when done
```

## Available Scripts

All in `.claude/skills/test-ui/scripts/`:

| Script             | Purpose                                      |
| ------------------ | -------------------------------------------- |
| `navigate.js`      | Navigate to URLs                             |
| `screenshot.js`    | Capture screenshots (auto-compress >5MB)     |
| `click.js`         | Click elements                               |
| `fill.js`          | Fill form fields                             |
| `evaluate.js`      | Execute JS in page context                   |
| `snapshot.js`      | Extract interactive elements (JSON)          |
| `aria-snapshot.js` | Get ARIA accessibility tree (YAML with refs) |
| `select-ref.js`    | Interact with elements by ARIA ref           |
| `console.js`       | Monitor console messages/errors              |
| `network.js`       | Track HTTP requests/responses                |
| `performance.js`   | Measure Core Web Vitals                      |

## Script Options (All scripts)

- `--headless false` - Show browser window
- `--close true` - Close browser completely
- `--timeout 30000` - Set timeout (ms)
- `--wait-until networkidle2` - Wait strategy

## Common Patterns

```bash
# Web scraping
node evaluate.js --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent, link: el.querySelector('a')?.href
  }))" | jq '.result'

# Form automation
node fill.js --selector "#search" --value "query"
node click.js --selector "button[type=submit]"

# Performance
node performance.js --url https://example.com | jq '.vitals'
```

## Local HTML Files

**Never use `file://`.** Serve via local server: `npx serve ./dist -p 3000 &`

## Troubleshooting

| Error                             | Solution                                      |
| --------------------------------- | --------------------------------------------- |
| `Cannot find package 'puppeteer'` | Run `npm install` in scripts directory        |
| `libnss3.so` missing (Linux)      | Run `./install-deps.sh`                       |
| Element not found                 | Use `snapshot.js` to find correct selector    |
| Script hangs                      | Use `--timeout 60000` or `--wait-until load`  |
| Screenshot >5MB                   | Auto-compressed; use `--max-size 3` for lower |
| Session stale                     | Delete `.browser-session.json` and retry      |


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
