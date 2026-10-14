---
name: playwright-e2e-test
description: Writes and runs one Playwright end-to-end test for a single critical user flow (e.g. checkout, booking, sign-up), so the agent can verify its own work in a real browser instead of claiming "it works". Proposes the test plan in plain language first and waits for approval, reuses an existing Playwright setup or installs a minimal one, runs only that spec, and proves the test can actually fail. When the test fails it reports with evidence and never edits the test just to make it pass — the human decides whether the bug is in the app or in the test. Use when the user asks to create an e2e test, a Playwright test, a browser test, or to cover a critical flow with automated QA.
---

# Playwright E2E Test

## Goal

Give the agent **eyes on the real app**. An agent that only reads code can only say "I think it
works". A Playwright test runs the flow in a real browser and answers with a fact: green or red.

This skill produces **one test for one critical flow** — a minimal safety net, not a QA plan.

## Non-negotiable rules

1. **Plan before code.** Propose the test plan in plain language and STOP until the user approves it.
2. **Never weaken a test to make it pass.** No editing assertions to match broken behavior, no
   `test.skip`, no `test.fixme`, no extra retries, no longer timeouts to hide a failure. A red test
   is reported, not silenced.
3. **The human decides.** When the test fails, diagnose and propose — the user chooses whether to
   fix the app or the test.
4. **Never run against production.** Local or staging only. If the flow writes to a real database,
   say so before the first run.

## Step 1 — Understand the flow

- Ask which flow to cover if the user did not name one. One flow per run of this skill.
- Read the code that implements it (pages, components, the API it calls) and any project docs
  (`CLAUDE.md`, `README`, PRD) to learn how the app starts and what "success" looks like.
- Identify the **visible success outcome** a user would see (a heading, a confirmation message, a
  new row in a list). That outcome becomes the final assertion.

## Step 2 — Propose the plan and STOP

Present, in plain language:

```
Flow: <name>
Start at: <url>
Steps:
  1. <user action> (e.g. click "Continue")
  2. ...
Final assertion: <what must be visible at the end, with its exact text>
Test data: <what it fills in, and whether it writes to a real database>
File: <path of the spec>
```

Wait for the user's OK or adjustments. Do not write code before that.

## Step 3 — Set up Playwright (only if missing)

**If the project already has `playwright.config.*`: reuse it.** Put the spec where the existing
specs live and follow their conventions (auth setup, helpers, fixtures). Do not create a second
harness.

**If it does not**, install the minimum:

```bash
npm install -D @playwright/test
npx playwright install chromium
```

On Linux or WSL the browser also needs system libraries (otherwise it fails with errors like
`libnspr4.so: cannot open shared object file`). Installing them requires `sudo`, so ask the user to
run it — never try to obtain their password:

```bash
sudo npx playwright install-deps chromium
```

And create `playwright.config.js` (`.ts` if the project uses TypeScript) with only what matters:

```js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000',     // the app's local URL
    trace: 'retain-on-failure',           // step-by-step recording, kept only when a test fails
    screenshot: 'only-on-failure',        // evidence for the human
  },
  webServer: {
    command: 'npm run dev',               // the project's real dev command
    url: 'http://localhost:3000',
    reuseExistingServer: true,
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
```

Take the port and the start command from the project — do not guess them. Add `test-results/` and
`playwright-report/` to `.gitignore`.

## Step 4 — Write the test

- **Locators the way a user sees the page**: `getByRole`, `getByLabel`, `getByText`,
  `getByPlaceholder`. Use `getByTestId` only if nothing visible identifies the element. Never CSS
  classes or XPath.
- **No manual waits**: no `waitForTimeout`, no `networkidle`. Playwright waits on its own; web-first
  assertions (`await expect(locator).toBeVisible()`) retry until they pass or time out.
- **At least one assertion on the final visible outcome.** Clicks without an assertion prove
  nothing.
- **Data that can run twice**: if the flow creates records or takes a limited resource (a time slot,
  a username), pick values that do not collide on the next run.
- Short comments only where a step is not obvious from the code.

## Step 5 — Run only this spec

```bash
npx playwright test <path-to-spec> --reporter=list
```

Never run the whole suite unless the user asks — on real projects it can take many minutes.

## Step 6 — Prove the test can fail

A test that passes with and without the feature verifies nothing. Once it is green:

1. Make one small, temporary change in the **app** that breaks the expected outcome (e.g. stop
   sending a required field), and tell the user what you changed.
2. Run the spec again — it must go red, for the reason you expect.
3. Revert the change and confirm with `git diff` that only the test files remain changed.

## Step 7 — Report

```
## E2E test: <flow>
- Spec: <path>
- Result: PASSED | FAILED
- Proof it can fail: <what was broken, and the error it produced>
- Command: npx playwright test <path>
```

If the test failed, add:

```
- What failed: <step and assertion>
- Evidence: <screenshot, `error-context.md` and trace paths under `test-results/`; open the trace
  with `npx playwright show-trace <trace.zip>` — its network tab shows the API status codes>
- Diagnosis: app bug | outdated test | environment (server down, data) — with the reasoning
- Proposed fix: <what to change, and where>
```

Then stop. The user decides what gets fixed.
