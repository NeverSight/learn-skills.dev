---
name: automate-manual-test-cases
description: This skill converts manual test cases into production-ready automated test scripts. It analyzes the existing automation framework, interprets manual test steps, and generates maintainable tests following automation best practices. Use this skill whenever the user wants to automate manual test cases, expand test coverage, or create end-to-end automated flows from existing test documentation.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Automate Manual Test Cases

Generate production-ready automated test scripts from manual test cases, reusing the project's existing framework, patterns, and components.

## Checklist

Complete all steps in order:

1. [ ] Analyze project architecture => detect framework (1.1), analyze conventions (1.2), find reusable components (1.3).
2. [ ] Understand manual test => normalize input (2.1), handle ambiguous steps (2.2), detect inconsistencies (2.3).
3. [ ] Write test code => implement using existing POM/patterns (3.1-3.2), add assertions (3.3), output code (3.4).
4. [ ] Verify & heal => execute test (4.1), heal if fails: locators → timing → assertions → flow (4.2), **max 3 attempts**.
5. [ ] Finalization => save test (5.1), manage test data & fixtures (5.2), run related tests and output summary (5.3).

### Progress

* STEP: 1/5 (Analyze Project Architecture)
* Previous: (none)
* Next ➡️ Step 2: Understand Manual Test.

Update this block after completing each step (see CLAUDE.md).

## Step 1: Analyze Project Architecture

### 1.1 Detect Automation Framework

- If the user specifies a framework (e.g., "use CodeceptJS") => trust it.
- Otherwise inspect the project:
  - `package.json` dependencies and scripts.
  - Config files (`playwright.config.js`, `codecept.conf.js`, `cypress.json`, etc.).
- If detection fails, ask with numbered options:

  ```
  ❓ Which framework should I use?
  1. Playwright
  2. CodeceptJS
  3. Cypress
  4. Other (specify)
  ```

After detection, apply the matching reference:
- [CodeceptJS Best Practices](./references/CODECEPTJS_BEST_PRACTICES.md)
- [Playwright Best Practices](./references/PLAYWRIGHT_BEST_PRACTICES.md)

### 1.2 Analyze Project Conventions

- Test structure and naming: folders (`tests/`, `e2e/`) and file patterns (`*.spec.js`, etc.).
- Execution: `package.json` scripts and test commands.
- Configuration: base URLs, env variables, global setup.
- Assertion style: libraries and patterns used in existing tests.

### 1.3 Identify Reusable Components

Scan for:
- Page Objects: existing locators and methods (`src/pages`, `pages/`, `page-objects/`, etc.).
- Fixtures/hooks: setup and teardown patterns.
- Test data: constants, CSV, JSON (`test-data`, `src/testData`, etc.).
- Utils/helpers (`utils/`, `helpers/`, etc.).

Exclude from analysis:
- Dependency folders (`node_modules/`).
- Build artifacts (`dist/`, `build/`, `out/`).
- Hidden/system folders (`.git/`, `.cache/`).
- Deprecated code: `deprecated/`, `legacy/`, `old/`, `backup/`, `__backup__/`, `archive/`, `temp/`, files marked `outdated`, older versioned folders (`v1/`, `v2/`) when newer versions exist.
- Do not auto-exclude folders with unclear purpose.
- **User-specified exclusions always override auto-detected ones.**

## Step 2: Understand Manual Test

Input may be plain text, markdown steps, or comment blocks in source files (`//`, `/* */`).

### 2.1 Normalize Input Structure

Convert input into:
- `summary` (or scenario title).
- `preconditions` (optional).
- `steps` (required) — ordered actions with expected results.

For comment-based inputs:
- Treat comment markers (`//`, `*`, `-`) as structural hints.
- Convert bullet points into ordered steps.
- Bind `_Expected:_` or `Expected Results` blocks to the preceding step.
- Merge multiline expected results into a single logical expectation.

Example:

```md
* Navigate to page  
  _Expected:_ Page opens
* Click once on the ${Custom statuses} block
  _Expected_: List includes "manual" option.
```

**Do not delete or rewrite original manual test comments.**
- Keep them as-is in the file.
- Generate automation code below or alongside them.
- Separate with a marker: `// === AUTO-GENERATED TEST (based on steps above) ===`

### 2.2 Handle Ambiguous Steps

Classify each step:
- Clear => proceed.
- Partially clear => make a reasonable assumption, mark it with ⚠️ in output (e.g., "⚠️ Assuming 'Submit' button triggers form submission"), continue.
- Unclear and blocking => ask the user, with numbered options when there are alternatives:

  ```
  ❓ Do you want to:
  1. Use existing LoginPage
  2. Create new LoginPage
  3. Skip login step
  ```

Use context from previous steps and common UI patterns (click, input, navigation).
**Do not block the whole flow on one unclear step — continue with the rest.**

### 2.3 Detect Inconsistencies

If step actions, expected results, and known UI patterns disagree:
- Proceed with best-effort interpretation.
- Flag with ⚠️ in output.

## Step 3: Write Test Code

### 3.1 Choose Implementation Strategy

- Reusable components exist (Page Objects, helpers, fixtures) => reuse them; follow project patterns and naming.
- Partial structure exists => extend existing components; keep consistency with current design.
- No structure => simple readable locators, minimal implementation, no unnecessary abstractions.

Priorities: consistency with the project, then readability, then maintainability.

**Do not ignore existing Page Objects or duplicate selectors/logic.**

### 3.2 Follow Framework Patterns

- One test, one flow — each test validates a single scenario.
- Separation of concerns: tests => assertions and flow control; Page Objects => UI interactions; utils => reusable logic.
- Extend, don't modify — add to existing components without changing stable code.
- Use fixtures for setup, authentication, and shared state.

See [POM Best Practices](./references/POM_BEST_PRACTICES.md).

### 3.3 Generate Assertions

- Base assertions on expected results from manual steps.
- Validate UI state (visibility, text, attributes), data correctness, navigation outcomes.
- Avoid weak assertions (only checking page load) and over-asserting irrelevant details.

### 3.4 Output Test Code

- Generate complete, runnable code that integrates with the existing framework.
- Follow project formatting and style conventions.
- Place code in the appropriate test file or suggest a location.

## Step 4: Verify & Heal

### 4.1 Execute Test

**Run only the generated test, never the full suite:**
- Playwright: `npx playwright test path/to/spec.ts`
- CodeceptJS: `npx codeceptjs run path/to/test.js`

If it passes => go to Step 5. If it fails => heal (4.2).

### 4.2 Heal Failed Tests

Fix one issue at a time, in priority order:
1. Locators — prefer stable selectors (`data-testid`, `aria-label`), avoid deeply nested XPath.
2. Timing — use framework-native waits, avoid hard sleeps.
3. Assertions — match actual app behavior, not assumptions.
4. Flow — verify navigation, preconditions, missing steps.

Process: identify a single failure => apply one fix => re-run => repeat.
Keep the last working version to roll back to if stuck.

**Max 3 healing attempts. If still failing, stop and report the issues.**

When the root cause is unclear, use the debug-fix-failed-flaky-autotests skill for structured step-by-step diagnosis.

If MCP/debug tools are available:
- Inspect DOM (`document.querySelector(...).outerHTML`).
- Use step-by-step execution.
- Capture logs, screenshots, or traces.

### 4.3 Stability Criteria

A test is stable when it:
- Passes 1-2 consecutive runs.
- Has no hard waits.
- Uses resilient locators.

## Step 5: Finalization

### 5.1 Save Final Test Code

- Save the working test to the appropriate project location.
- Follow naming conventions and stay consistent with existing tests.

### 5.2 Test Data & Fixtures

- Use centralized test data if the project has it (JSON/CSV/constants).
- Reuse authentication/setup fixtures; don't duplicate setup inside tests.

See [Test Data Management](./references/TEST_DATA_MANAGEMENT.md).

### 5.3 Final Run & Summary

- Execute 1-2 related tests to confirm integration (related tests only, not the full suite).
- Exit condition: test passes 2 consecutive runs.
- Show a spec-to-code mapping:

  | Manual Step | Automation Action |
  |-------------|-------------------|
  | Navigate to Settings | `basePage.clickOnNavigationMenuButton("Settings")` |

- Output the final summary using [Final Summary Template](./references/FINAL_SUMMARY_TEMPLATE.md).

## Example: Comment-Based Request

```
Use automate-manual-test-cases skill for CodeceptJS framework to write automation
script "tests/plan-for-guest.test.ts" based on manual steps below in this file as
comments (leaving comments in the file for further analysis). Set a specific "smoke"
tag for this test.
Use as reference for extra proper examples:
* `tests/payment-methods.test.ts` - Canonical test file with team approved format.
* `src/pages/paymentMethods.page.ts` - Good described payment page object.
Avoid mistakes from legacy code examples:
* `src/pages/paymentOutdated.page.ts` - Outdated example with old patterns.

Finally, verify that the generated test is passed on - `BASE_URL = 'https://test.com/'`
and provide final review for user.
```
