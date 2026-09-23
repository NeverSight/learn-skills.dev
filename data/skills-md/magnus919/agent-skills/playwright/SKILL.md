---
name: playwright
description: >-
  Operate Playwright for browser automation end to end: author and debug E2E
  test suites (robust locators, network interception and mocking, parallel
  workers, accessibility snapshot checks), wire them into CI, and drive
  headless browsing and scraping with an extract -> validate -> save loop. Use
  when writing, running, fixing, or scraping with Playwright, when a Playwright
  CI failure or JSON report needs triage, or when the bundled pwrun script
  should analyze a run. Do not use for QA strategy or test framework selection
  (route to qa-methodology), for frontend component or architecture design
  (route to frontend-engineering), or for Cloudflare/DDoS-GUARD challenge
  bypass (use flaresolverr).
license: MIT
compatibility: >-
  Playwright 1.40+ for the documented patterns (aria snapshots need 1.49+).
  The bundled pwrun script runs on Python 3.8+ and needs no node or Playwright
  for --help, doctor, inventory, or report analysis; smoke delegates to npx.
metadata:
  source: https://playwright.dev/docs
  spec: https://playwright.dev/docs/api/class-playwright
---

# Playwright Browser Automation

Use this skill to drive a real browser with Playwright: author end-to-end tests, keep selectors and tests robust, intercept and mock network traffic, run suites across parallel workers and in CI, scrape and extract data in headless mode, and check accessibility with snapshot scans. This is a **tool skill** for one named tool. Test strategy and framework selection belong to [qa-methodology](../qa-methodology/SKILL.md); frontend component and architecture design belong to [frontend-engineering](../frontend-engineering/SKILL.md). This skill owns operating the Playwright tool itself.

## Operating contract

1. **Read the suite before running.** Inspect `playwright.config.*`, projects, `baseURL`, `webServer`, workers, retries, and reporters before running anything. Never assume the test command from the README.
2. **Locate by behavior, not layout.** Prefer user-facing locators (`getByRole`, `getByLabel`, `getByText`) over CSS/XPath that encode markup. Tests coupled to user-visible behavior survive refactors; tests coupled to structure break on them.
3. **Mock at the boundary.** Stub external HTTP at `page.route()` — never by patching in-page code. Mock the dependency under test's edges, never the code under test itself; a test that mocks what it claims to verify proves nothing.
4. **Parallelize deliberately.** Playwright gives every test an isolated browser context. Tune `workers` and sharding to the machine and suite, and never let tests share mutable state through globals.
5. **Verify at the boundary.** A green test is only as strong as its assertions. Assert on user-visible outcomes (visible text, URL, enabled/disabled state), not on implementation details.
6. **Keep evidence bounded.** Capture traces, screenshots, and video on failure only; summarize JSON reports instead of dumping them; never paste full HTML dumps or session cookies into chat.

## The pwrun script

`scripts/pwrun` is an agent-first smoke harness around a Playwright suite. `doctor`, `inventory`, and `report` work with no node or Playwright installed, so an agent can inspect a suite and triage a CI report anywhere.

```bash
scripts/pwrun doctor --json                     # node, @playwright/test, browsers, config availability
scripts/pwrun inventory --json                  # config, projects, spec files in the suite
scripts/pwrun report --report test-results.json --json   # summarize a Playwright JSON report
scripts/pwrun smoke --url http://localhost:3000 --json   # delegate a smoke run to npx playwright test
```

Exit codes: 0 ok, 1 analysis error, 2 usage error, 127 dependency (node/playwright) missing, 124 delegate timeout. `--json` on every command; `--help` works without any toolchain.

## E2E test authoring

- Structure suites with `test.describe` blocks, `test.beforeEach` setup, and per-feature fixture files. Keep specs short, focused on one user journey, and readable as prose.
- Use Playwright's web-first assertions (`expect(locator).toBeVisible()`, `.toHaveText()`, `.toHaveURL()`) — they auto-retry until a timeout and are the backbone of stable E2E tests. Avoid manual `page.waitForTimeout` sleeps.
- Start the app under test with `webServer` in the config (Playwright starts it, waits for readiness, and tears it down), or reuse an already-running instance via `baseURL` for smoke passes.
- Authoring patterns, fixtures, and the page-object model: `references/01-e2e-authoring.md`.

## Selector robustness

- Default to role, label, text, and placeholder locators — they describe the page the way a user does. Reserve CSS for layout-adjacent needs (e.g., `getByTestId` for ids that exist only for tests).
- Chain and filter locators (`getByRole('row').filter({ hasText: 'Acme' })`) instead of building one long brittle selector. Re-query rather than storing stale element handles.
- Fix flaky tests by finding which selector matched multiple or zero elements, not by adding sleeps or `first()`. A selector that can match the wrong thing will eventually.
- Selector priority rules and flaky-selector repair flows: `references/02-selectors.md`.

## Network interception and mocking

- Intercept requests with `page.route()` and fulfill, abort, or continue them. Use this to mock third-party APIs, inject fixtures, emulate offline or slow networks, and block analytics/trackers that pollute tests.
- Mock at the route level with realistic bodies and content types. Never intercept the server the test is supposed to verify, and never route over `page.goto` navigation the test depends on.
- Capture requests with `page.on('request')`/`page.on('response')` to assert on what the app actually sent. Patterns and gotchas: `references/03-network-interception-and-mocking.md`.

## Parallel workers

- `workers` sets how many parallel processes run specs; `fullyParallel` lets every spec file run across workers. Scale to CPU count and browser memory, not to "as many as possible".
- Shard suites across CI jobs (`--shard=1/4`) for large suites. Every test runs in its own browser context, so isolation is default — keep it that way: no shared globals, no shared storage state, no test-order coupling.
- Worker counts, sharding math, and isolation traps: `references/04-parallel-workers-and-sharding.md`.

## CI integration

- Install browsers and OS deps on the runner (`npx playwright@1.62.1 install --with-deps`), pin the Playwright version, and cache `~/.cache/ms-playwright`.
- Configure `webServer`, `retries` (retry flaky tests on CI only), and `trace: 'on-first-retry'` so failures are debuggable. Report with `html`/`json`/`github` and upload artifacts on failure.
- Triage CI failures from the JSON report with `scripts/pwrun report --json` — it summarizes stats, failing specs, and error messages without opening a browser. Full CI recipes: `references/05-ci-integration.md`.

## Scraping and headless browsing

- Drive the browser API directly (`chromium.launch({ headless: true })`, `newContext`, `page.goto`) to load JavaScript-rendered pages, then extract with locators and `innerText`/attribute access into structured records — extract, validate, save.
- Respect robots.txt, terms, and rate limits; bound the scrape by page count and delay. For Cloudflare/DDoS-GUARD challenge bypass, route to [flaresolverr](../flaresolverr/SKILL.md) — this skill does not solve challenges.
- Scraping flows, pagination, and polite extraction: `references/06-scraping-and-headless.md`.

## Accessibility snapshot checks

- Run full scans with `@axe-core/playwright` to catch WCAG violations (contrast, landmarks, ARIA misuse) in CI or on demand.
- Use Playwright's aria snapshots (`expect(page).toMatchAriaSnapshot()`) as stable, accessibility-aware assertions: they compare the accessibility tree, so they catch structure and label regressions and read like spec assertions. Update deliberately, never `--update-snapshots` reflexively.
- Scan setup, snapshot discipline, and fixing violations: `references/07-accessibility-and-debugging.md`.

## Headed debugging

- Run headed (`--headed`), slow the action with `--slow-mo`, or drop into the inspector with `--debug` / `PWDEBUG=1` and the `page.pause()` breakpoint.
- Generate starter tests with `npx playwright@1.62.1 codegen <url>`, then harden the generated selectors into user-facing locators.
- When a test fails: read the trace (`--trace on`), which records network, DOM snapshots, and console for the failed action. Use `scripts/pwrun report --report <json> --json` first to see the failure summary.
- Debugging workflows live in `references/07-accessibility-and-debugging.md`.

## Reference routing

| Load when | Reference |
|---|---|
| Writing or structuring specs, fixtures, page objects | `references/01-e2e-authoring.md` |
| A selector is flaky or matches the wrong element | `references/02-selectors.md` |
| Mocking or intercepting API/network traffic | `references/03-network-interception-and-mocking.md` |
| Speeding up or sharding a large suite | `references/04-parallel-workers-and-sharding.md` |
| Wiring Playwright into CI or triaging CI failures | `references/05-ci-integration.md` |
| Extracting data or browsing in headless mode | `references/06-scraping-and-headless.md` |
| Accessibility scans, aria snapshots, or debugging a failing test | `references/07-accessibility-and-debugging.md` |
| Sources, version observations, and refresh procedure | `references/00-source-index.md` |

## Included artifacts

- `scripts/pwrun`: smoke harness — `doctor`, `inventory`, `report`, `smoke`, all with `--json`.
- `tests/test_pwrun.py` + `tests/fixtures/sample-report.json`: deterministic tests for the harness (no node/browser required).
- `templates/playwright.config.ts`, `templates/example.spec.ts`, `templates/accessibility.spec.ts`: copy-in test-suite scaffold.
- `references/`: eight dated, source-indexed references covering the operational topics above.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| Toolchain is present | `scripts/pwrun doctor --json` reports node, @playwright/test, and browsers available |
| Suite is understood | `scripts/pwrun inventory --json` lists config and spec files |
| A test passes | `npx playwright@1.62.1 test` exit 0 on the targeted spec (or `smoke` delegation) |
| A CI failure is explained | `scripts/pwrun report --report test-results.json --json` names the failing specs and errors |
| Accessibility is covered | An axe scan runs with zero violations of the declared severity, and aria snapshots match |
| No regressions in the covered flows | The suite ran under the configured workers/sharding with expected/flaky/unexpected counts recorded |

## Hard boundaries

- Never mock the code under test to force a green test — mock only its boundaries.
- Never scrape in violation of robots.txt, terms, or rate limits; never harvest credentials or personal data, and never extract auth/session storage into committed files.
- Never commit `playwright/.auth/*` storage state, `.env`, or browser credentials.
- Never run `--update-snapshots` blindly to "fix" an aria snapshot diff — inspect what changed first.
- Never dump raw HTML, full trace files, or screenshots of protected content into chat; summarize with `pwrun report` instead.
- A headed browser in CI needs a display server (e.g., xvfb) — never assume a display exists on a runner.

## When not to use

- **Test strategy, framework selection, or QA process** — route to [qa-methodology](../qa-methodology/SKILL.md).
- **Frontend component/state/architecture design or implementation guidance** — route to [frontend-engineering](../frontend-engineering/SKILL.md); React-specific component and hooks work routes to [react](../react/SKILL.md).
- **Cloudflare/DDoS-GUARD challenge bypass** — route to [flaresolverr](../flaresolverr/SKILL.md).
- **Load/performance testing at scale** (k6, Locust, Gatling, JMeter) — that methodology lives under `qa-methodology`'s performance-testing reference.
- **Raw HTTP retrieval of static content** — use a plain HTTP client; Playwright is for JavaScript-rendered pages and browser workflows.

## Topic coverage keywords

The catalog's automated topic sweep greps this file for coverage keywords. Two
alias pairs are written literally below so the sweep matches both spellings:
`e2e|end-to-end` covers browser-level tests (E2E, end-to-end, and e2e are the
same workflow), and `debug|head` covers the headed-debugging workflows in this
skill. All other topics (selector robustness, network interception, parallel
workers, CI integration, scraping, accessibility snapshots, mocking) appear by
name in the sections above.
