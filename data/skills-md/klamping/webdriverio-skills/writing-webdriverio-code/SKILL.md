---
name: writing-webdriverio-code
description: Use when implementing, extending, or fixing WebdriverIO tests, including converting pseudo-code scaffolds into clean WDIO commands, selectors, waits, and assertions.
---

# Writing WebdriverIO Code

Convert scaffold comments into production-ready test code.

This skill can take either:
- a scaffold created by `creating-test-structure`, or
- an existing WebdriverIO spec that needs new tests, refactors, or bug fixes.

In both cases, it produces concrete WebdriverIO implementation that is stable, readable, and debuggable.

## When to Use

- A scaffold exists and needs conversion from pseudo-code to WDIO commands/assertions.
- An existing test file needs additional scenarios.
- Existing tests are flaky, brittle, or incorrect and need fixes.

## When Not to Use

- You need full-suite scaffolding from a markdown test plan (use `creating-test-structure`).
- You are only reorganizing describe/it hierarchy without code implementation.
- You need broad test strategy decisions (test pyramid/scope) rather than file-level WDIO code.

## Input Contract

- A scaffolded spec file with pseudo-code comments (optional).
- Or an existing implemented spec file to extend/fix.
- Existing page objects, fixtures, and helpers from the project.
- Project conventions (linting, naming, assertion style).

## Project Context Files

Before implementation, read project cache files when available:

- `.webdriverio-skills/project-context.md`
- `.webdriverio-skills/project-context.json`
- `.webdriverio-skills/custom-rules.md`
- `.webdriverio-skills/health-recommendations.md`
- `references/website-analysis/<target>/website-analysis.md`
- `references/website-analysis/<target>/website-analysis.json`

Use these as the default source for conventions, scripts, environment usage, and team overrides.

Use website analysis references for route/component context, expected states, and auth-gated flow awareness.

`<target>` should resolve to lowercase site host (prefer user URL or project `baseUrl` host).
If unavailable, use `unknown-target` and proceed with other context sources.

If files are missing or stale, run `managing-project-customizations` first.

## Conversion Workflow

1. Identify whether the target is scaffold-conversion or direct test enhancement/fix.
2. Load project context and custom rules, then apply them as hard constraints.
3. Implement comments in execution order when pseudo-code exists.
4. Prefer existing page object methods before creating new ones.
5. Use resilient selectors and explicit expectations.
6. Remove pseudo-code comments once behavior is clear.
7. Keep only comments that explain non-obvious intent.

## Suite Startup State Hygiene

- At suite start, reset state that can leak between tests (cookies, local storage, session/auth state).
- Make startup preconditions idempotent so re-runs produce the same baseline.
- Prefer explicit setup in hooks over hidden cross-test state.
- Treat cleanup as required, but do not rely only on `after` hooks that might not run after crashes.

## Deterministic Test Data Setup and Cleanup

- Create deterministic test data via APIs/fixtures when possible.
- Name fixtures/data so their purpose is obvious.
- Keep setup close to the test scope that needs it (`beforeEach` for strict isolation, `before` for shared stable state).
- Always include a cleanup path for created data.
- Verify test data assumptions in code before acting on them.

## Test Structure Rules

- Keep each test in clear phases: setup, validation, teardown.
- Keep setup in hooks when shared (`before`, `beforeEach`), not copy/pasted into every test.
- Keep each `it(...)` focused on one user-observable behavior.
- Keep tests independent and safe to run in isolation or in parallel.

## Framework Rules (Mocha/Jasmine)

- Match the project's existing style for `describe`, `it`, and hooks.
- Use nested `describe` blocks to represent user context, not implementation layers.
- Avoid deeply nested suites when a flatter structure reads better.
- Use `.only` / `.skip` only for local debugging and remove before finalizing.

## Page Object Rules

- Keep selectors and page-specific actions in page objects/components.
- Keep specs focused on behavior and assertions.
- Reuse existing page object methods before adding new abstractions.
- Add small, purpose-specific page object methods; avoid generic do-everything helpers.

## Efficient Element Querying

- Scope queries to meaningful containers before selecting child elements.
- Reuse located elements within a test step instead of re-querying the same selector repeatedly.
- Prefer unique semantic selectors over index-based lookups.
- Use index-based selection only when the UI contract is explicitly positional.

## Selector Rules

- Prefer user-facing selectors: `button=...`, `aria/...`.
- Use `data-testid` when text/ARIA is unstable.
- Avoid brittle class-chain and layout-coupled selectors.
- Scope element queries to reduce collisions.

## Waiting Rules

- Rely on auto-wait for interactions (`click`, `setValue`) when possible.
- Use explicit waits for meaningful UI state transitions (`waitForDisplayed`, `waitForClickable`, `waitUntil`).
- Prefer waiting on user-visible outcomes over internal implementation details.
- Do not use `browser.pause` as a synchronization strategy.
- Small hard waits are allowed only when tied to known UI constraints (e.g., unavoidable animation timing) and should be rare and documented.
- Keep implicit timeouts at default unless there is a documented reason.

### Waiting Decision Guide

| Situation | Preferred approach | Avoid |
|---|---|---|
| Element interaction | WDIO auto-wait + interact | pre-emptive `pause` |
| Async UI update after action | assertion retry or `waitFor...` | fixed sleep |
| Non-element condition | `browser.waitUntil(...)` with clear condition | polling with manual loops |
| Known animation delay | tiny documented `pause` only if no stable signal exists | large blanket pauses |

## Avoid Third-Party Dependency Assertions

- Test behavior your application owns, not external provider internals.
- Stub/mock third-party integrations where feasible to avoid external flake.
- Validate your contract with external services (request/response handling), not vendor uptime or UI.
- Keep a very small set of smoke checks for external integration paths only when needed.

## Assertion Rules

- Assert user-visible outcomes and critical state.
- Use `expect-webdriverio` matchers (`toHaveText`, `toBeDisplayed`, `toHaveUrlContaining`).
- Prefer meaningful failure messages via clear assertion targets.
- Assert list counts/order explicitly when behavior depends on ordering.
- Verify only behavior that matters for the scenario; avoid noisy over-assertion.

## Test Naming Rules

- Test names should read as clear behavior statements.
- Use domain language users and developers recognize.
- Avoid vague names (`should work`, `happy path test`).
- Name tests by expected outcome, not implementation steps.

## Security Rules

- Never hardcode secrets.
- Mask sensitive values when entering credentials (`setValue(..., { mask: true })` where supported).
- Avoid leaking tokens or credentials in logs.

## Write Tests for Fast Debugging

- Keep test steps readable in execution order.
- Use assertion targets that reveal what failed without extra digging.
- Add concise step-level logs for complex journeys.
- Keep abstraction shallow in specs so failures map back to intent quickly.

## Flaky Test Triage Playbook

1. Reproduce the failure reliably (single test, then repeated runs).
2. Isolate the flaky step (selector, wait, data, environment, or shared state).
3. Classify root cause (timing, state leakage, brittle locator, test-data drift, external dependency).
4. Fix the root cause (do not hide with sleeps/retries).
5. Re-run multiple times to verify stability before closing.

## Quick Reference

| Test intent | Typical WDIO implementation |
|---|---|
| Navigate to a page | `await browser.url('/path')` |
| Interact with a control | `await el.click()` / `await el.setValue(...)` |
| Validate visible outcome | `await expect(el).toBeDisplayed()` |
| Validate content/state | `await expect(el).toHaveText(...)` / `toHaveValue(...)` |
| Wait for async state change | `await el.waitForDisplayed()` or `browser.waitUntil(...)` |

## Common Mistakes

- Assuming a scaffold is always required.
- Leaving pseudo-code comments unimplemented.
- Converting comments to brittle selectors.
- Using `browser.pause` instead of waiting for a condition.
- Overusing helper abstractions that hide test intent.
- Coupling tests to execution order.
- Treating retries as a substitute for root-cause fixes.

## Example

```js
it('should default to showing the global feed', async function () {
  const activeTabs = await $$('.feed-toggle .nav-link.active');
  await expect(activeTabs).toBeElementsArrayOfSize(1);
  await expect(activeTabs[0]).toHaveText('Global Feed');
});
```

Done means all pseudo-code comments are converted into maintainable WDIO code or intentionally retained only for non-obvious context.
