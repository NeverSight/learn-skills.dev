---
name: browserforce
description: Browse the web using the user's real Chrome browser — already logged in, with real cookies and extensions. No headless browser. Uses BrowserForce relay + Playwright API via CLI.
read_when:
  - Browsing as the user with logged-in sessions
  - Accessing sites that require authentication
  - Interacting with the user's real Chrome tabs
  - Web automation with existing cookies and extensions
  - Taking screenshots of authenticated pages
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["node","browserforce"]},"install":[{"kind":"node","package":"browserforce","bins":["browserforce"],"label":"Install BrowserForce CLI"}]}}
allowed-tools: Bash(browserforce:*)
---

# BrowserForce — Your Real Chrome Browser

BrowserForce gives you the user's actual Chrome browser — all their logins,
cookies, and extensions already active. No headless browser, no fresh profiles.

## Prerequisites

The user must have:
1. BrowserForce Chrome extension installed and connected (green icon)
2. The relay auto-starts on first command — no manual step needed

Check with: `browserforce status`

## Quick Reference

```bash
browserforce status              # Check relay + extension status
browserforce tabs                # List open tabs
browserforce snapshot [n]        # Accessibility tree of tab n
browserforce screenshot [n]      # Screenshot tab n (PNG to stdout)
browserforce navigate <url>      # Open URL in new tab
browserforce -e "<code>"         # Run Playwright JavaScript (one-shot)
```

## Important: One-Shot Execution

Each `browserforce -e` call is independent — state does NOT persist between calls.
Do everything you need (navigate, act, observe) within a single `-e` call.

## Core Workflow: Observe → Act → Observe

### Quick observation (no code needed)
```bash
browserforce snapshot 0          # See what's on tab 0
browserforce tabs                # List all tabs
```

### Navigate and read a page
```bash
browserforce -e "
  state.page = await context.newPage();
  await state.page.goto('https://example.com');
  await waitForPageLoad();
  return await snapshot();
"
```

Note: `snapshot()` reads from `state.page` (if set) or `page` (default tab 0).
Always assign `state.page` when creating a new page so `snapshot()` reads the right tab.

### Click and verify
```bash
browserforce -e "
  state.page = context.pages()[context.pages().length - 1];
  await state.page.locator('role=button[name=\"Next\"]').click();
  await waitForPageLoad();
  return await snapshot();
"
```

### Fill a form
```bash
browserforce -e "
  state.page = context.pages()[context.pages().length - 1];
  await state.page.locator('role=textbox[name=\"Email\"]').fill('user@example.com');
  return await snapshot();
"
```

### Extract data
```bash
browserforce -e "
  const p = context.pages()[context.pages().length - 1];
  return await p.evaluate(() => document.querySelector('.price').textContent);
"
```

### Screenshot
```bash
browserforce screenshot 0 > page.png
# or via -e:
browserforce -e "
  state.page = context.pages()[0];
  return await state.page.screenshot();
" > page.png
```

## Rules

1. **snapshot() over screenshot()** — snapshot returns text (fast, cheap).
   Use screenshot only for visual layout verification.
2. **One-shot execution** — each -e call is independent. Do all steps in one call.
3. **Don't navigate existing tabs** — create your own via `context.newPage()`
   or `browserforce navigate <url>`.
4. **Use convenience commands** for simple operations: `browserforce tabs`,
   `browserforce snapshot`, `browserforce screenshot`.
5. **waitForPageLoad()** — call after navigation or clicks that trigger page loads.

## Error Recovery

- Connection lost: User must check `browserforce status`
- No tabs: `browserforce navigate https://example.com`
- Element not found: `browserforce -e "return await snapshot({ search: 'button' })"`

## Important

This is the user's REAL browser. Be respectful:
- Don't close tabs you didn't open
- Don't navigate tabs you didn't create
- Don't modify browser settings or stored data
