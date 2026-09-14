---
name: sniff
description: Use when the user types /sniff, or asks to "scan this project for bugs", "find bugs in my app", "QA my site", or "walk my app and tell me what's broken". For a running web app, finds real, reproducible issues (broken pages/links, console & network errors, broken forms, empty/placeholder data, state-loss, bad loading/error states, responsive and accessibility problems), each with reproduction proof, severity, confidence, and a fix. No API key needed.
---

# /sniff: find real bugs in this project

## What to do

1. Call the unified `sniff` MCP tool with:
   - `mode`: `"walk"`, the autonomous flow-walk that drives a real browser and finds runtime bugs (this is the one that matters; `"scan"` is source-only)
   - `rootDir`: the current project's absolute path
   - omit `baseUrl` to auto-detect the running dev server, or pass it if the user gives a URL
2. If the response is `{ needsSetup: "playwright-browsers" }`, call the `sniff_install` tool, then retry the walk.
3. If no app is running, sniff returns a note + a source-only scan. Tell the user to start their dev server (or pass a URL) for the full flow-walk that finds the real runtime bugs.
4. Present findings grouped by severity (CRITICAL and HIGH first). For each, show the **route**, the **reproduction steps**, the **confidence** (confirmed / likely / uncertain), and the **suggested fix**. Mention any finding marked `needsOutOfBandVerification` (e.g. "submitted but no success shown, confirm the email/job actually ran"). Offer `/sniff-fix` for the safe, auto-fixable ones.

## Example

```
User: /sniff
You: Walking your running app for real bugs…

[calls sniff with mode="walk", rootDir=/Users/user/projects/my-app]

Found 9 real issues (0 false positives) across 12 pages:

**Critical (1)**
- /checkout: Page returns HTTP 500 (crash screen shown to the user)

**High (3)**
- /: Broken link → /pricing-old (HTTP 404)
- /dashboard: Uncaught exception: cannot read 'map' of undefined
- /signup: Submit button does nothing (no request, no message, no change)

**Medium (5)**
- /orders: Empty table with no empty-state ("Your Orders")
- /profile: Placeholder data shipped (test@test.com)
- …each with reproduction steps + a screenshot + a fix.

Want me to fix the safe ones with /sniff-fix?
```
