---
name: ui-ux-audit
description: Run a UI/UX audit on a running web app — Playwright walkthrough at three viewports, axe-core WCAG 2.1 AA scan, and Lighthouse mobile audit. Produces ./audit/report.md, screenshots, a Playwright smoke test in ./tests/, and (for Expo/Vite projects) a dev-vs-prod-build Lighthouse comparison. Triggers on "audit ui/ux", "ui audit", "ux audit", "ux review", "a11y audit", "accessibility audit", "lighthouse audit", or any request to audit a localhost / staging URL.
---

# UI/UX Audit

A three-stage audit pipeline against a running web app. Used to ship a punch-list of P0/P1 UX bugs, axe-core a11y violations, and Lighthouse perf scores in one pass.

## Required MCP servers

This skill **will not work** without these three MCPs configured (one-time setup, see `INSTALL.md` next to this file):

| Name | Package | Why |
|---|---|---|
| `playwright` | `@playwright/mcp` | Drives a real browser — navigate, click, screenshot, viewport sizing |
| `a11y` | `a11y-mcp` | Runs axe-core WCAG 2.1 against any URL |
| `lighthouse` | `lighthouse-mcp` | Performance / a11y / best-practices / SEO scores |

Verify with `claude mcp list` before starting. If any are missing, point the user at `INSTALL.md` rather than soldiering on.

## Inputs

The user invokes with at minimum a URL. Common forms:

- `audit ui/ux http://localhost:3000`
- `ux audit https://staging.example.com`
- `accessibility audit my app`  ← if no URL given, **ask** which URL

Optional things to extract from the prompt or ask about:

- **Primary user flow** to walk (e.g. "sign up → create project → invite teammate"). If unspecified, **auto-discover** by exploring from the landing page — start with what the landing page suggests is the primary CTA.
- **Auth strategy.** If the landing page has both "Continue with Google" and an email/password signup, prefer email signup with a dummy account named `audit-{ISO-timestamp}@example.com` and a throwaway password. Only attempt Google OAuth if email signup isn't available — and even then, warn the user before opening the OAuth flow.
- **Output directory.** Default `./audit/` for the report and screenshots, `./tests/` for the smoke test. Use the cwd unless the user asks otherwise.

## Pipeline

### Stage 0 — Pre-flight (do this once before any Playwright call)

1. Confirm the URL is reachable. If it's `localhost:*`, do a `curl -s -o /dev/null -w "%{http_code}"` first; fail fast with a clear message if the dev server isn't running.
2. Check that `./audit/screenshots/` and `./tests/` are writable from the cwd. If not, propose an alternative directory.
3. **Playwright cache dir gotcha (Windows + read-only cwd):** Playwright MCP tries to create `.playwright-mcp/` in its cwd. If cwd is read-only the very first `browser_navigate` call fails with `EPERM, mkdir '.playwright-mcp'`. Fix is `claude mcp remove playwright -s user && claude mcp add playwright -s user -- npx -y @playwright/mcp@latest --output-dir <writable-path>`, then restart Claude Code. Mention this to the user *before* you run the audit so they don't waste a turn.

### Stage 1 — Playwright walkthrough

For each viewport in `[1440x900, 768x1024, 375x812]` (in this order — start desktop, narrow down):

1. `browser_resize` to the viewport.
2. `browser_navigate` to the URL. Wait for hydration if it's a SPA (`browser_wait_for` with `time: 2-3` or text from the snapshot).
3. `browser_snapshot` to get the accessibility tree. Read it carefully — the `target` ref IDs are how you'll click things.
4. `browser_take_screenshot` with `fullPage: true` to `./audit/screenshots/{NN}-{slug}-{viewport}.png` (e.g. `01-signin-1440.png`). Use absolute paths if `--output-dir` was set; relative otherwise.
5. Walk the primary flow. For each meaningful state, repeat snapshot + screenshot.
6. Check `browser_console_messages` after the flow — note errors (especially silent failures like a button click that triggers a navigator error and does nothing).

While walking the flow, **look for these classes of issue** and capture them in your notes:

- Layout: content full-width on desktop (form fields > 800px wide), drawer/nav rendered off-screen (eval `getBoundingClientRect()` to confirm `x < 0`), broken responsive breakpoints
- Dead controls: buttons that do nothing, console errors after click
- Copy bugs: pluralization (`1 men` should be `1 man`), platform-wrong verbs (`tap to edit` on desktop), unfilled placeholders
- Missing affordances: tabs without an active state, required fields with no announcement, low-contrast disabled states
- Empty / first-run UX: huge whitespace, no logo/marketing, full-width CTAs

### Stage 2 — Axe-core a11y scan

For each unique URL visited (typically just `/` for a SPA — note that the MCP doesn't carry session cookies, so it only audits the *public* page unless you pre-seed auth):

```
mcp__a11y__audit_webpage with tags: ["wcag2a","wcag2aa","wcag21a","wcag21aa","best-practice"], includeHtml: true
```

Group results by `impact` (critical / serious / moderate / minor). For each violation, capture:

- Rule ID (e.g. `color-contrast`, `autocomplete-valid`, `region`)
- Failing target selector
- One-line failure summary from `failureSummary`
- A specific suggested fix (not "improve contrast" — give the actual hex, like "darken `#2a9d5f` to `~#218754` to clear 4.5:1")

**Document the auth limitation.** If authenticated screens couldn't be audited, say so explicitly in the report — don't pretend the unauthenticated audit covers them.

### Stage 3 — Lighthouse mobile audit

```
mcp__lighthouse__run_audit with device: "mobile", categories: ["performance","accessibility","best-practices","seo"], throttling: true
```

**Critical caveat — dev server numbers are fiction.** Vite/Expo/Next.js dev servers have hot-reload, no minification, on-demand transforms. FCP/LCP routinely come back at 7s+ on the dev server but 1–3s on a real build. **If the URL is a dev server, before reporting Lighthouse numbers, build the production output and re-run.** Detection rule: any URL on a port commonly used by dev servers (`3000`, `5173`, `8080`, `8081`) AND the response has framework dev-server signatures (e.g. `Hermes transform`, `vite/dist/client`, `__next_dev__`).

Production rebuild flow per framework:

| Framework | Build | Serve |
|---|---|---|
| Expo (React Native Web) | `npx expo export -p web` | `npx serve dist -l 8090` |
| Vite | `npm run build` | `npx serve dist -l 8090` |
| Next.js | `npm run build && npm start` | already on a different port |
| Create React App | `npm run build` | `npx serve build -l 8090` |

Then re-run Lighthouse against the new port. Save the full JSON to `./audit/lighthouse-prod.json` for diffing.

**Lighthouse MCP fallback (Windows / Defender EPERM).** On Windows with real-time AV protection, `mcp__lighthouse__run_audit` sometimes fails with `EPERM, Permission denied: lighthouse.{NNNN}` on the temp dir. The audit usually completed before the cleanup failed. Fall back to the CLI:

```powershell
npx --yes lighthouse@12.8.2 "<url>" --form-factor=mobile --throttling-method=simulate --output=json --output-path=./audit/lighthouse-prod.json --quiet --chrome-flags="--headless=new --no-sandbox"
```

Then parse the JSON yourself for `categories.{performance,accessibility,best-practices,seo}.score`, `audits.{first-contentful-paint,largest-contentful-paint,total-blocking-time,cumulative-layout-shift,speed-index,interactive}.{displayValue,score}`, and the top opportunities (`audits.<id>.details.overallSavingsMs`).

## Outputs

Always produce these three artifacts in the cwd:

### 1. `./audit/report.md`

Three sections, in this order:

```markdown
# {AppName} — UI/UX Audit

**Audited:** {date} · **URL:** {url} · **Build:** {dev|prod export of <framework>}
**Tooling:** @playwright/mcp · a11y-mcp (axe-core <version>) · lighthouse-mcp (<version>)
**Primary flow walked:** {one-line description}
**Viewports captured:** 1440×900, 768×1024, 375×812. Screenshots in `audit/screenshots/`.
**Caveats:** {auth limitations, dev-vs-prod, anything the reader needs to know}

## 1. UX findings (ranked by impact)

### P0 — {one-line title}
- **What I saw:** {observation, with a screenshot reference}
- **Why it matters:** {user impact}
- **Fix:** {specific, actionable — code path or library API where possible}

### P1 — ...
### P2 — ...

## 2. Accessibility violations (axe-core, WCAG 2.1 A/AA + best-practice)

| # | Rule ID | Severity | Element | Failing detail | Suggested fix |
|---|---|---|---|---|---|

## 3. Lighthouse — mobile, throttled

| Category | Dev server | Prod build | Δ |    ← include both columns if you ran both
| Performance | 43 🔴 | 60 🟡 | +17 |
... (metrics table, then top 3 fixes)
```

Rank UX findings P0/P1/P2/P3 by **user impact**, not by what's easy to fix:
- **P0** = ship-blocker, broken feature, dead control, critical accessibility (e.g. nav unreachable)
- **P1** = serious UX issue affecting most users (e.g. desktop layout broken)
- **P2** = noticeable but non-blocking (copy bugs, inconsistent affordances)
- **P3** = polish / nice-to-have

### 2. `./audit/screenshots/`

PNG screenshots named `{NN}-{slug}-{viewport}.png`. Use a leading number for ordering (`01-signin-1440`, `02-signup-1440`, etc.) so the reader can scroll through them in flow order. Re-use the same `NN` across viewports (`01-signin-1440`, `01-signin-768`, `01-signin-375`).

### 3. `./tests/smoke.spec.ts`

A Playwright test (`@playwright/test`, not the MCP) that re-runs the primary flow you walked, ready to drop into CI:

- Use `BASE_URL = process.env.BASE_URL ?? '<url>'`
- Generate a unique account per run (`audit-${new Date().toISOString().replace(/[:.]/g,'-')}@example.com`) so re-runs against the same backend don't collide
- Match assertions to the `data-testid` attributes if present, otherwise role-based (`getByRole('button', { name: '…' })`) — do NOT rely on css class names
- Include a `test.describe` with viewport sanity checks (1440 / 768 / 375) that just hits the landing page and verifies it renders

## Report-writing tips

- Don't sandbag the criticism. If the home page looks like a wall of nothing, say so. The user asked for an audit, not a review.
- Always pair a finding with a *specific* fix. "Improve contrast" is useless; "darken `#2a9d5f` to `~#218754` (clears 4.5:1 against white)" is useful.
- Cite screenshots by filename when describing visual issues. Saves the reader from hunting.
- Note what you couldn't audit (auth-gated pages without a session) — the absence of findings is itself information the user needs.
- Top 3 Lighthouse fixes should be sequenced by **payoff**, not severity. A 2.25 s saving from code-splitting beats a 0.3 s CSS purge even if the CSS warning is "more red."

## When NOT to use this skill

- The user asks for a code review of a PR — that's `code-review`, not this.
- The user asks for a security review — that's `security-review`.
- The user asks "is my design good?" without a running URL to test — push back and ask for a URL or a Figma link first.
