---
name: e2e-reviewer
description: Use when reviewing, auditing, or improving E2E test specs for Playwright, Cypress, or Puppeteer — static code analysis of existing test files, not diagnosing runtime failures. Triggers on "review my tests", "audit test quality", "find weak tests", "my tests always pass but miss bugs", "tests pass CI but miss regressions", "improve playwright tests", "improve cypress tests", "check test coverage gaps". Detects 14 anti-patterns — naming-assertion mismatch, missing Then, error swallowing, always-passing assertions, boolean traps, conditional bypass, raw DOM queries, render-only tests, duplicate scenarios, misleading names, over-broad assertions, subject-inversion, hard-coded timeouts, flaky patterns (positional selectors, missing mocks, animation races), and YAGNI violations in Page Objects.
---

# E2E Test Scenario Quality Review

Systematic checklist for reviewing E2E **spec files AND Page Object Model (POM) files**. Framework-agnostic principles; code examples show Playwright, Cypress, and Puppeteer where they differ.

## Phase 1: Automated Grep Checks (Run First)

Once the review target files are determined, use the Grep tool to mechanically detect known anti-patterns **before** LLM analysis. Run each check below against the `e2e/` directory (or equivalent). Replace `e2e/` with the actual test directory if different.

**What each check detects:**

- **#3 Error Swallowing** — `.catch(() => {})` or `.catch(() => false)` silently hides failures. Search `.ts/.js/.cy.*` for `\.catch(\s*() =>`, excluding `node_modules` and lines with `// justified`.
- **#4 Always-Passing** — assertions that can never fail (e.g. `count >= 0`). Search for `toBeGreaterThanOrEqual(0)` or `should.*(gte|greaterThan).*0`.
- **#5 Boolean Trap** — `toBeTruthy()` on Locator/ElementHandle objects (objects are always truthy). Search `.spec.*/.test.*/.cy.*` for `expect(.*).toBeTruthy()`, excluding lines ending in `.ok()`, `.isVisible()`, `.isChecked()`, `.isDisabled()`, `.isEnabled()`, `.isEditable()`, `.isHidden()`.
- **#6 Conditional Bypass** — `expect()` inside `if(isVisible)` silently skips assertions. Search `.spec.*/.test.*/.cy.*` for `if.*(isVisible|is\(.*:visible.*\))`.
- **#7 Raw DOM Queries** — `document.querySelector` bypasses framework auto-wait. Search `.spec.*/.test.*/.cy.*` for `document\.querySelector`.
- **#12 Hard-coded Timeouts** — arbitrary sleeps cause flakiness. Search `.ts/.js/.cy.*` for `waitForTimeout` or `cy\.wait\(\d`.
- **#13b Missing Network Mock** — `page.goto`/`cy.visit` without nearby route/intercept creates real network dependency. Search `.spec.*/.test.*/.cy.*` for `page\.goto|cy\.visit`, then filter out lines containing `route.`, `intercept`, or `mock`.

**Interpreting results:**
- Zero hits → no mechanical issues found, proceed to Phase 2
- Any hit → report each line as an issue (includes file:line)
- Lines with `// justified` comments are intentional — skip them

**Output Phase 1 results as-is.** The LLM must not reinterpret them.

---

## Phase 2: LLM Review (Subjective Checks Only)

Patterns already detected in Phase 1 (#3, #4, #5 partial, #6, #7, #12, #13b partial) are **skipped**.
The LLM performs only these checks:

| # | Check | Reason |
|---|-------|--------|
| 1 | Name-Assertion Alignment | Requires semantic interpretation |
| 2 | Missing Then | Requires logic flow analysis |
| 8 | Render-Only | Requires test value judgment |
| 9 | Duplicate Scenarios | Requires similarity comparison |
| 10 | Misleading Names | Requires semantic interpretation |
| 11 | Over-Broad Assertions + Subject-Inversion | Requires domain context |
| 13 | Flaky Patterns (partial) | Requires context judgment for nth(), animation, network patterns |
| 14 | YAGNI in POM | Requires usage grep then judgment |

---

## Phase 3: Coverage Gap Analysis (After Review)

After completing Phase 1 + 2, identify scenarios the test suite does NOT cover. Scan the page/feature under test and flag missing:

| Gap Type | What to look for |
|----------|-----------------|
| Error paths | Form validation errors, API failure states, network offline, 404/500 pages |
| Edge cases | Empty state, max-length input, special characters, concurrent actions |
| Accessibility | Keyboard navigation, screen reader labels, focus management after modal/dialog |
| Auth boundaries | Unauthorized access redirects, expired session handling, role-based visibility |

**Output:** List up to 5 highest-value missing scenarios as suggestions, not requirements. Format:

```markdown
## Coverage Gaps (Suggestions)
1. **[Error path]** No test for form submission with server error — add API mock returning 500
2. **[Edge case]** No test for empty list state — verify empty state message shown
```

---

## Review Checklist

Run each check against every **non-skipped** test and every **changed POM file**.

**Important:** `test.skip()` with a reason comment or reason string is intentional — do NOT flag or remove these. Only flag mid-test conditional skips that hide failures (see #6).

---

### Tier 1 — P0/P1 (always check)

#### 1. Name-Assertion Alignment `[LLM-only]`

**Symptom:** Test name promises something the assertions don't verify.

```typescript
// BAD — name says "status" but only checks visibility
test('should display paragraph status', () => {
  await expect(status).toBeVisible();  // no status content check
});
```

**Rule:** Every noun in the test name must have a corresponding assertion. Add it or rename.

**Procedure:**
1. Extract all nouns from the test name (e.g., "should display paragraph **status**")
2. For each noun, search the test body for `expect()` that verifies it
3. Missing noun → add assertion or remove noun from name

**Common patterns:** "should display X" with only `toBeVisible()` (no content check), "should update X and Y" with assertion for X but not Y, "should validate form" with only happy-path assertion.

#### 2. Missing Then `[LLM-only]`

**Symptom:** Test acts but doesn't verify the final expected state.

```typescript
// BAD — toggles but doesn't verify the dismissed state
test('should cancel edit on Escape', () => {
  await input.click();
  await page.keyboard.press('Escape');
  await expect(text).toBeVisible();
  // input still hidden?
});
```

**Rule:** For toggle/cancel/close actions, verify both the restored state AND the dismissed state.

**Procedure:**
1. Identify the action verb (toggle, cancel, close, delete, submit, undo)
2. List the expected state changes (element appears/disappears, text changes, count changes)
3. Check that BOTH sides of the state change are asserted

**Common patterns:** Cancel/Escape without verifying input is hidden, delete without verifying count decreased, submit without verifying form resets, tab switch without verifying previous tab content is hidden.

#### 3. Error Swallowing `[grep-detectable]`

**Symptom (spec):** `try/catch` wrapping assertions — test passes on error.

**Symptom (POM):** `.catch(() => {})` or `.catch(() => false)` on awaited operations — caller never sees the failure.

```typescript
// BAD spec — silent pass
try { await expect(header).toBeVisible(); }
catch { console.log('skipped'); }

// BAD POM — caller thinks execution succeeded
await runningIndicator.waitFor({ state: 'detached' }).catch(() => {});
```

**Rule (spec):** Never wrap assertions in try/catch. Use `test.skip()` in `beforeEach` if the test can't run.

**Rule (POM):** Remove `.catch(() => {})` / `.catch(() => false)` from wait/assertion methods. If the operation can legitimately fail, the caller should decide how to handle it. Only keep catch for UI stabilization like `editor.click({ force: true }).catch(() => textArea.focus())`.

#### 4. Always-Passing Assertions `[grep-detectable]`

**Symptom:** Assertion that can never fail.

```typescript
// BAD — count >= 0 is always true
expect(count).toBeGreaterThanOrEqual(0);
```

**Rule:** Search for `toBeGreaterThanOrEqual(0)`, `toBeTruthy()` on always-truthy strings, `||` chains that accept defaults as valid.

#### 5. Boolean Trap Assertions `[grep-detectable]`

**Symptom (spec):** `expect(locator).toBeTruthy()` on a Locator/ElementHandle object — always passes because objects are always truthy regardless of whether the element exists in the DOM.

**NOT a boolean trap:** `expect(response.ok()).toBeTruthy()` or `expect(await el.isVisible()).toBe(true)` — these operate on actual boolean return values. While `toBe(true)` is slightly more precise than `toBeTruthy()` for booleans, this is a **style preference, not a bug**. Only flag as P1 when the value is a non-boolean object (Locator, ElementHandle, Promise).

**Symptom (POM):** Method returns `Promise<boolean>` instead of exposing an element handle — forces spec into boolean trap.

```typescript
// BAD — boolean return forces spec into trap
async isEditorVisible(index = 0): Promise<boolean> {
  return await paragraph.locator('code-editor').isVisible();
}
expect(await page.isEditorVisible(0)).toBe(true);
```

**Rule (spec):** Use the framework's built-in assertion instead of extracting a boolean first:
- **Playwright:** `await expect(locator).toBeVisible()`
- **Cypress:** `cy.get(selector).should('be.visible')`
- **Puppeteer:** `await page.waitForSelector(selector, { visible: true })`

**Rule (POM):** Expose the element handle (Locator / selector string) instead of returning `Promise<boolean>`. Let specs use framework assertions directly.

#### 6. Conditional Bypass (Silent Pass / Hidden Skip) `[grep-detectable]`

**Symptom:** `expect()` inside `if` block, or mid-test `test.skip()` — test silently passes when feature is broken.

```typescript
// BAD — if spinner never appears, assertion never runs
if (await spinner.isVisible()) {
  await expect(spinner).toBeHidden({ timeout: 5000 });
}
```

**Rule:** Every test path must contain at least one `expect()`. Move environment checks to `beforeEach` or declaration-level `test.skip()`.

#### 7. Raw DOM Queries (Bypassing Framework API) `[grep-detectable]`

**Symptom:** Test drops into raw `document.querySelector*` / `document.getElementById` via `evaluate()` when the framework's element lookup API could do the same job.

```typescript
// BAD — no auto-wait, returns stale boolean
const has = await page.evaluate((i) => {
  return !!document.querySelectorAll('.para')[i]?.querySelector('.result');
}, 0);
expect(has).toBe(true);
```

**Why it matters:** No auto-waiting, no retry, boolean trap, framework error messages lost.

**Rule:** Use the framework's element API instead of raw DOM:
- **Playwright:** `page.locator()` + web-first assertions
- **Cypress:** `cy.get()` / `cy.find()` — avoid `cy.window().then(win => win.document.querySelector(...))`
- **Puppeteer:** `page.$()` / `page.waitForSelector()` — avoid `page.evaluate(() => document.querySelector(...))`

Only use `evaluate`/`waitForFunction` when the framework API can't express the condition (`getComputedStyle`, cross-element DOM relationships). In POM, add a comment explaining why.

---

### Tier 2 — P1/P2 (check when time permits)

#### 8. Render-Only Tests (Low E2E Value) `[LLM-only]`

**Symptom:** Test only calls `toBeVisible()` with no interaction or content assertion.

**Rule:** Add at least one of: content assertion (`not.toBeEmpty()`, `toContainText()`), count assertion (`toHaveCount(n)`), or sibling element assertion.

#### 9. Duplicate Scenarios (DRY) `[LLM-only]`

**Symptom:** Two tests share >70% of their steps with minor variations.

**Rule (within file):** Merge tests that differ only in setup or a single assertion. Use the richer verification set from both.

**Rule (cross-file):** After reviewing all files in scope, cross-check tests with similar names across different spec files. If test A in `feature-settings.spec.ts` is a subset of test B in `feature-form-validation.spec.ts`, delete A and strengthen B.

**Procedure:**
1. List all test names in the file — look for similar prefixes or overlapping verbs
2. For each pair with >70% step overlap, compare their assertion sets
3. If one is a subset of the other, delete the weaker test and keep the richer one

**Common patterns:** "should add item" and "should add item and verify count" (subset), "should open dialog" in file A and "should open dialog and fill form" in file B (cross-file subset), parameterizable tests written as separate cases.

#### 10. Misleading Test Names (KISS) `[LLM-only]`

**Symptom:** Name implies UI interaction but test uses API/REST, or name implies feature X but tests feature Y.

**Rule:** If the test uses REST API, reload, or indirect methods, the name must make that explicit.

#### 11. Over-Broad Assertions (KISS) `[LLM-only]`

**Symptom:** Assertion too loose to catch regressions.

```typescript
// BAD — any string containing '%' passes
expect(content.includes('%')).toBe(true);
```

**Rule:** Prefer exact matches or explicit value lists over `.includes()` or loose regex when valid values are known and small.

#### 11b. Subject-Inversion `[LLM-only]`

**Symptom:** Expected values placed in `expect()` instead of the actual value — failure messages become confusing.

```typescript
// BAD — subject is the expected values array, not the actual result
//        failure message: "Expected [200, 202] to contain 204" (confusing)
expect([200, 202]).toContain(deleteResponse.status());

// GOOD — actual value as subject, clear failure message
const status = deleteResponse.status();
expect(status === 200 || status === 202).toBe(true);
```

**Rule:** The value under test (actual) must always be the argument to `expect()`. Expected values go in the matcher. If the matcher doesn't support multi-value checks natively, use a boolean expression with `toBe(true)` rather than inverting the subject.

#### 12. Hard-coded Timeouts `[grep-detectable]`

**Symptom:** `waitForTimeout()` or magic timeout numbers scattered across tests and POM.

```typescript
// BAD — arbitrary sleep
await page.waitForTimeout(2000);

// BAD — magic number, no explanation
await element.waitFor({ state: 'visible', timeout: 30000 });
```

**Rule:** Never use explicit sleep (`waitForTimeout` / `cy.wait(ms)`) — rely on framework auto-wait or retry mechanisms. For custom timeouts, extract named constants with comments explaining why the default isn't sufficient.

#### 13. Flaky Patterns `[LLM-only + grep]`

**Symptom:** Test passes locally but fails intermittently in CI due to timing, ordering, or environment assumptions.

**Sub-patterns:**

**13a. Positional selectors** — `nth()`, `first()`, `last()` without comment.

```typescript
// BAD — breaks if DOM order changes
await expect(items.nth(2)).toContainText('Settings');
```

**Rule:** Prefer `data-testid`, role-based, or attribute selectors. If `nth()` is unavoidable, add a comment explaining why.

**13b. Network dependency without mock** — Test relies on real API responses without `route.fulfill()` / `cy.intercept()`.

```typescript
// BAD — fails if API is slow or returns different data
await page.goto('/dashboard');
await expect(page.locator('.user-count')).toHaveText('42');
```

**Rule:** For data-dependent assertions, mock the network response or assert on structure (element exists, is not empty) rather than exact values.

**13c. Animation race** — Assertion runs before CSS transition or animation completes.

```typescript
// BAD — modal may still be animating
await button.click();
await expect(modal).toBeVisible(); // passes
await expect(modal.locator('.content')).toHaveText('Done'); // flaky — content not rendered yet
```

**Rule:** After triggering animations, wait for the final state element, not the container. Use `waitForSelector` with stable content or `toHaveCSS('opacity', '1')` for fade-ins.

#### 14. YAGNI in Page Objects `[LLM-only]`

**Symptom:** POM has locators/methods never referenced by any spec.

**Procedure:**
1. List all public members of each changed POM file
2. Grep each member across all test files and other POMs
3. Classify: USED / INTERNAL-ONLY (`private`) / UNUSED (delete)

**Common patterns:** Convenience wrappers (`clickEdit()` when specs use `editButton.click()`), getter methods (`getCount()` when specs use `toHaveCount()`), state checkers (`isEditMode()` when specs assert on elements directly), pre-built "just in case" locators.

**Rule:** Delete unused members. Make internal-only members `private`. When creating new shared utils, ensure they will be used by 2+ specs. Do not delete existing util files/classes that are actively imported and used by specs — only flag unused individual members within them.

**Output:**
```
| File | Member | Used In | Status |
|------|--------|---------|--------|
| page.ts | addLinks | (none) | DELETE |
| page.ts | searchDialog | internal only | PRIVATE |
```

---

## Output Format

Present findings grouped by severity:

```markdown
## [P0/P1/P2] Task N: [filename] — [issue type]

### N-1. `[test name or POM method]`
- **Issue:** [description]
- **Fix:** [name change / assertion addition / merge / deletion]
- **Code:**
  ```typescript
  // concrete code to add or change
  ```
```

**After all findings, append a summary table:**

```markdown
## Review Summary

| Sev | Count | Top Issue | Affected Files |
|-----|-------|-----------|----------------|
| P0  | 3     | Missing Then | auth.spec.ts, form.spec.ts |
| P1  | 5     | Duplicate Scenarios | settings.spec.ts |
| P2  | 2     | Render-Only | dashboard.spec.ts |

**Total: 10 issues across 4 files. Fix P0 first.**
```

**Severity classification:**
- **P0 (Must fix):** Test silently passes when the feature is broken — no real verification happening
- **P1 (Should fix):** Test works but gives poor diagnostics, wastes CI time, or misleads developers
- **P2 (Nice to fix):** Weak but not wrong — maintenance and robustness improvements

## Quick Reference

| # | Check | Sev | Phase | Detection Signal |
|---|-------|-----|-------|-----------------|
| 1 | Name-Assertion | P0 | LLM | Noun in name with no matching `expect()` |
| 2 | Missing Then | P0 | LLM | Action without final state verification |
| 3 | Error Swallowing | P0 | grep | `try/catch` in spec, `.catch(() => {})` in POM |
| 4 | Always-Passing | P0 | grep | `>=0`, truthy on non-empty, `\|\|` defaults |
| 5 | Boolean Trap | P1 | grep | `expect(locator).toBeTruthy()` on non-boolean objects; skip when value is actual boolean (`.ok()`, `.isVisible()`) |
| 6 | Conditional Bypass | P0 | grep | `expect()` inside `if`, mid-test `test.skip()` |
| 7 | Raw DOM Queries | P1 | grep | `document.querySelector` in `evaluate` |
| 8 | Render-Only | P2 | LLM | Only `toBeVisible()`, no content/count |
| 9 | Duplicate | P1 | LLM | >70% shared steps, cross-file overlap |
| 10 | Misleading Name | P1 | LLM | API/reload in "should [UI verb]" test |
| 11 | Over-Broad | P2 | LLM | `.includes()` where enum values known |
| 11b | Subject-Inversion | P1 | LLM | `expect([expected]).toContain(actual)` — confusing failure messages |
| 12 | Hard-coded Timeout | P2 | grep | `waitForTimeout()`, magic numbers |
| 13 | Flaky Patterns | P1 | LLM+grep | `nth()`, missing network mock, animation race |
| 14 | YAGNI in POM | P2 | LLM | Public member not referenced in any spec |

---

## Suppression

When a grep-detected pattern is intentional, add a `// justified: [reason]` comment to the line. Phase 1 will exclude it.

Example: `await editor.click({ force: true }).catch(() => textArea.focus()); // justified: UI stabilization fallback`
