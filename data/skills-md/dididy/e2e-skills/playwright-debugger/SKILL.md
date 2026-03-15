---
name: playwright-debugger
description: Use when Playwright tests have actually failed and you need to diagnose runtime failures — from a playwright-report directory, local or CI. Triggers on "debug playwright tests", "why did playwright tests fail", "playwright CI failure", "flaky playwright test failures", "playwright timeout error", "tests pass locally but fail in CI", "analyze playwright-report", "PR failing in CI". Classifies runtime failures into root causes (not static code analysis) and suggests concrete fixes.
---

# Playwright Failed Test Debugger

Diagnose Playwright test failures from report files. Classifies root causes and provides concrete fixes.

## Prerequisites: Get the Report

Determine the report source in this order:

**1. `playwright-report/` already exists locally** → skip to Phase 1.

**2. No report available** → run tests locally and write output to a file (do NOT read stdout directly — output may be truncated):

```bash
npx playwright test --reporter=json 2>/dev/null > playwright-report/results.json
```

## Phase 1: Extract Failures

Locate `results.json` under `playwright-report/`, then extract all tests where `status` is `"failed"` or `"timedOut"`. For each failed test, collect: `title`, `status`, `error.message`, `location.file`, `duration`.

Use `jq` if available:

```bash
cat playwright-report/results.json | jq '[
  .. | objects |
  select(.status == "failed" or .status == "timedOut") |
  {title: .title, status: .status, error: .error.message, file: .location.file, duration: .duration}
] | unique'
```

If `jq` is unavailable, read the JSON file directly with the Read tool and extract failed tests manually.

## Phase 2: Classify Root Cause

Use Phase 1 output (error message + duration + file) to classify each failure. **Most failures are identifiable here — only go to Phase 3 if still unclear.**

| # | Category | Signals | Review Pattern |
|---|----------|---------|----------------|
| F1 | **Flaky / Timing** | `TimeoutError`, duration near maxTimeout, passes on retry | #9a |
| F2 | **Selector Broken** | `locator not found`, `strict mode violation`, element count mismatch | #6, #10 |
| F3 | **Network Dependency** | `net::ERR_*`, unexpected API response, `404`/`500` | — |
| F4 | **Assertion Mismatch** | `Expected X to equal Y`, over-broad check | #4 |
| F5 | **Missing Then** | Action completed but wrong state remains | #2 |
| F6 | **Condition Branch Missing** | Element conditionally present, assertion always runs | #5 |
| F7 | **Test Isolation Failure** | Passes alone, fails in suite; leaked state | — |
| F8 | **Environment Mismatch** | CI vs local only; viewport, OS, timezone | — |
| F9 | **Data Dependency** | Missing seed data, hardcoded IDs | — |
| F10 | **Auth / Session** | Session expired, role-based UI not rendered | — |
| F11 | **Async Order Assumption** | `Promise.all` order, parallel race | — |
| F12 | **POM / Locator Drift** | DOM changed, POM locator not updated | #10 |
| F13 | **Error Swallowing** | `.catch(() => {})` hiding failure, test passes silently | #3 |
| F14 | **Animation Race** | Element visible but content not yet rendered | #9a |

Classification steps:
1. Match error message to signals above
2. `duration` near timeout → F1 or F3
3. CI-only failure → F7 or F8
4. Passes on retry → F1

## Phase 3: Trace Analysis (only if Phase 2 is unclear)

`trace.zip` contains three parts:
- `trace.trace` — newline-delimited JSON events (actions, snapshots, console logs)
- `trace.network` — newline-delimited JSON (network requests and responses)
- `resources/` — JPEG screenshots per step

Find trace files: `find playwright-report -name "*.zip" | head -10`

Extract and read each file using `unzip -p <trace.zip> <entry>`, then parse the newline-delimited JSON. Stop as soon as the root cause is clear.

**What to look for at each step:**

1. **Which step failed** — filter `trace.trace` events where `type === "after"` and `error` is present. Log `apiName` and `error.message`.

2. **All actions with pass/fail** — filter `trace.trace` for `type === "after"`, log index, `apiName`, and whether `error` is set.

3. **DOM at the failed step** (selector issues) — filter `trace.trace` for `type === "frame-snapshot"` matching the `beforeSnapshot` name from step 2. Inspect `snapshot.html`.

4. **Failed network requests** — filter `trace.network` for `type === "resource-snapshot"` where `response.status >= 400`. Log status and URL.

5. **JS console errors** — filter `trace.trace` for `type === "console"` and `messageType === "error"`. Log `text`.

6. **Still unclear** — add temporary `page.screenshot()` calls before and after the failing action, re-run, then inspect the screenshots with a browser agent. Remove screenshots after debugging.

## Phase 4: Fix Suggestions

For each failure, produce a finding in this format:

**`[P0/P1/P2] test name — Category`**
- **Category:** e.g. F2 — Selector Broken (#10 POM Drift)
- **Error:** the raw error message
- **Root Cause:** one sentence explanation
- **Fix:** before/after code showing the concrete change

**Severity:**
- **P0:** Test passes silently when feature is broken (F6, F13)
- **P1:** Intermittent or misleading failures (F1, F2, F3, F7, F11, F14)
- **P2:** Consistent failures, straightforward fix (F4, F5, F8, F9, F10, F12)

## Output Format

```
Failure Summary
- Total: N failed (M flaky, K broken, J environment)

[P0] `test name` — F13 Error Swallowing
...

Review Summary
| Sev | Count | Top Category     | Files            |
|-----|-------|------------------|------------------|
| P0  | 1     | Error Swallowing | auth.spec.ts     |
| P1  | 3     | Flaky / Timing   | dashboard.spec.ts|
| P2  | 2     | POM Drift        | settings.spec.ts |

Fix P0 first. Run npx playwright test --retries=2 to confirm flaky tests.
```
