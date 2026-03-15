---
name: cypress-debugger
description: Use when Cypress tests have actually failed and you need to diagnose runtime failures — from mochawesome or JUnit report files, local or CI. Triggers on "debug cypress tests", "why did cypress tests fail", "cypress CI failure", "flaky cypress test failures", "cypress timed out retrying", "cypress tests pass locally but fail in CI", "analyze cypress/reports". Classifies runtime failures into root causes (not static code analysis) and suggests concrete fixes.
---

# Cypress Failed Test Debugger

Diagnose Cypress test failures from mochawesome or JUnit report files. Classifies root causes and provides concrete fixes.

## Prerequisites: Generate Report First

**Do NOT rely on Cypress stdout** — use a structured reporter instead:

```bash
# mochawesome (recommended)
cypress run --reporter mochawesome --reporter-options "reportDir=cypress/reports,json=true,html=false"

# JUnit (CI-friendly)
cypress run --reporter junit --reporter-options "mochaFile=cypress/reports/results.xml"
```

## Phase 1: Extract Failures

```bash
# Find report if path not specified
find . -name "mochawesome.json" -path "*/cypress/*" | head -5
find . -name "*.xml" -path "*/cypress/*" | head -5

# Extract failed tests from mochawesome (jq)
cat cypress/reports/mochawesome.json | jq '[
  .. | objects |
  select(.fail == true) |
  {title: .title, fullTitle: .fullTitle, duration: .duration, error: .err.message, stack: .err.estack}
]'

# Extract failed tests (node fallback)
node -e "
const r = require('./cypress/reports/mochawesome.json');
const flat = (s) => [...(s.tests||[]), ...(s.suites||[]).flatMap(flat)];
r.results.flatMap(flat)
  .filter(t => t.fail)
  .forEach(t => console.log('FAIL', t.fullTitle, '\n ', t.err?.message?.slice(0,120)))
"

# Extract failed tests from JUnit XML (node)
node -e "
const fs = require('fs');
const xml = fs.readFileSync('./cypress/reports/results.xml', 'utf-8');
const failures = [...xml.matchAll(/<testcase[^>]+name=\"([^\"]+)\"[^>]*>[\s\S]*?<failure[^>]*message=\"([^\"]+)\"/g)];
failures.forEach(([,name,msg]) => console.log('FAIL', name, '\n ', msg.slice(0,120)));
"
```

## Phase 2: Classify Root Cause

Use Phase 1 output (error message + duration) to classify. **Most failures are identifiable here — only go to Phase 3 if still unclear.**

| # | Category | Signals | Review Pattern |
|---|----------|---------|----------------|
| F1 | **Flaky / Timing** | `Timed out retrying`, duration near defaultCommandTimeout, passes on retry | #9a |
| F2 | **Selector Broken** | `Expected to find element: '...' but never found it`, `cy.get() failed` | #6, #10 |
| F3 | **Network Dependency** | `cy.intercept()` not matched, `XHR failed`, unexpected API response | — |
| F4 | **Assertion Mismatch** | `expected X to equal Y`, `AssertionError` | #4 |
| F5 | **Missing Then** | Action completed but wrong state remains | #2 |
| F6 | **Condition Branch Missing** | Element conditionally present, assertion always runs | #5 |
| F7 | **Test Isolation Failure** | Passes alone, fails in suite; leaked state via `cy.session` or cookies | — |
| F8 | **Environment Mismatch** | CI vs local only; baseUrl, viewport, OS differences | — |
| F9 | **Data Dependency** | Missing seed data, hardcoded IDs, `cy.fixture()` mismatch | — |
| F10 | **Auth / Session** | `cy.session()` expired, role-based UI not rendered | — |
| F11 | **Async Order Assumption** | `.then()` chain order, parallel `cy.request()` race | — |
| F12 | **Selector Drift** | DOM changed, custom command or Page Object selector not updated | #10 |
| F13 | **Error Swallowing** | `cy.on('uncaught:exception', () => false)` hiding failures | #3 |
| F14 | **Animation Race** | Element visible but content not yet rendered; CSS transition not complete | #9a |

Classification steps:
1. Match error message to signals above
2. `duration` near `defaultCommandTimeout` (4s) → F1 or F2
3. CI-only failure → F7 or F8
4. Passes on retry → F1

## Phase 3: Screenshot & Video Analysis (only if Phase 2 is unclear)

Cypress automatically captures screenshots on failure and optionally records video.

```bash
# Find screenshots for failed tests
find cypress/screenshots -name "*.png" | head -20

# Find videos
find cypress/videos -name "*.mp4" | head -10
```

Progressive disclosure — stop as soon as root cause is clear:

```bash
# 1. Check screenshot path from mochawesome report
cat cypress/reports/mochawesome.json | jq '[
  .. | objects | select(.fail == true) |
  {title: .title, screenshots: [.context? // empty | .. | strings | select(endswith(".png"))]}
]'

# 2. Check for JS errors in report context
cat cypress/reports/mochawesome.json | jq '[
  .. | objects | select(.fail == true) | .err.estack // empty
] | .[]' 2>/dev/null | head -50

# 3. Still unclear — inspect screenshot via browser agent
#    → open cypress/screenshots/<spec>/<test name> (failed).png and compare
#    → check cypress/videos/<spec>.mp4 for full run context
```

## Phase 4: Fix Suggestions

```markdown
## [P0/P1/P2] `test name`

- **Category:** F2 — Selector Broken
- **Error:** `Expected to find element: '.submit-btn', but never found it`
- **Root Cause:** Button selector too broad after DOM refactor
- **Fix:**
  ```javascript
  // before
  cy.get('.submit-btn').click();
  // after
  cy.get('[data-testid="login-submit"]').click();
  ```
```

**Severity:**
- **P0:** Test passes silently when feature is broken (F6, F13)
- **P1:** Intermittent or misleading failures (F1, F2, F3, F7, F11, F14)
- **P2:** Consistent failures, straightforward fix (F4, F5, F8, F9, F10, F12)

## Output Format

```markdown
## Failure Summary
- Total: N failed (M flaky, K broken, J environment)

## [P0] `test name` — F13 Error Swallowing
...

## Review Summary
| Sev | Count | Top Category | Files |
|-----|-------|-------------|-------|
| P0  | 1     | Error Swallowing | auth.cy.ts |
| P1  | 3     | Flaky / Timing | dashboard.cy.ts |
| P2  | 2     | Selector Drift | settings.cy.ts |

Fix P0 first. Run `cypress run --spec <file> --headed` to reproduce locally.
```
