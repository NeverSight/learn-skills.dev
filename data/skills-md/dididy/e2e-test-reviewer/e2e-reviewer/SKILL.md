---
name: e2e-reviewer
description: Use when reviewing, auditing, or improving E2E test specs for Playwright, Cypress, or Puppeteer — static code analysis of existing test files, not diagnosing runtime failures. Triggers on "review my tests", "audit test quality", "find weak tests", "my tests always pass but miss bugs", "tests pass CI but miss regressions", "improve playwright tests", "improve cypress tests", "check test coverage gaps", "my tests are fragile", "tests break on every UI change", "test suite is hard to maintain", "we have coverage but bugs still slip through". Detects 10 anti-patterns -- name-assertion mismatch, missing Then, error swallowing, always-passing assertions, bypass patterns (conditional assertions + force:true), raw DOM queries, focused test leak (test.only committed), flaky test patterns (positional selectors + serial ordering), hard-coded sleeps, and YAGNI + zombie specs (unused POM members, single-use Util wrappers, zombie spec files).
---

# E2E Test Scenario Quality Review

Systematic checklist for reviewing E2E **spec files AND Page Object Model (POM) files**. Framework-agnostic principles; code examples show Playwright, Cypress, and Puppeteer where they differ.

**Reference:**
- Playwright best practices: https://playwright.dev/docs/best-practices
- Cypress best practices: https://docs.cypress.io/app/core-concepts/best-practices

## Phase 1: Automated Grep Checks (Run First)

Once the review target files are determined, use the Grep tool to mechanically detect known anti-patterns **before** LLM analysis. Run each check below against the `e2e/` directory (or equivalent). Replace `e2e/` with the actual test directory if different.

**What each check detects:**

- **#3 Error Swallowing** — `.catch(() => {})` or `.catch(() => false)` silently hides failures. Search `.ts/.js/.cy.*` for `\.catch\(\s*(async\s*)?\(\)\s*=>`, excluding `node_modules` and lines with `// JUSTIFIED` on the line above.
- **#4 Always-Passing** — assertions that can never fail. Search for `toBeGreaterThanOrEqual(0)` or `should.*(gte|greaterThan).*0`. Also search `.ts/.js/.cy.*` (including POM/util files, not just specs) for `toBeAttached()` — flag every hit unless `// JUSTIFIED:` appears on the line above. Also search `.spec.*/.test.*/.cy.*` for `expect\(await.*\.isVisible\(\)\)` — one-shot boolean with no auto-retry; flag unless `// JUSTIFIED:` is on the line above.
- **#5 Bypass Patterns** — two sub-patterns that suppress what the framework would normally catch: (a) `expect()` inside `if(isVisible)` silently skips assertions — search `.spec.*/.test.*/.cy.*` for `if.*(isVisible|is\(.*:visible.*\))`; (b) `{ force: true }` bypasses actionability checks (visibility, enabled state) — search `.ts/.js/.cy.*` for `force:\s*true`. Exclude lines where `// JUSTIFIED` appears on the line above. **Note:** The `if(isVisible)` grep covers spec files only — review POM helper methods manually in Phase 2.
- **#6 Raw DOM Queries** — `document.querySelector` bypasses framework auto-wait. Search `.spec.*/.test.*/.cy.*` for `document\.querySelector` (covers both `evaluate()` and `waitForFunction()`).
- **#7 Focused Test Leak** — `test.only` / `it.only` / `describe.only` committed to source silently skips the rest of the suite in CI. Search `.spec.*/.test.*/.cy.*` for `\.(only)\(`. No `// JUSTIFIED:` exemption — there are zero legitimate committed uses; remove before committing.
- **#8 Flaky Test Patterns (partial)** — two sub-patterns that cause CI instability: (a) positional selectors `nth()`, `first()`, `last()` without explanation — search `.spec.*/.test.*/.cy.*` for `\.nth\(|\.first\(\)|\.last\(\)`; (b) `test.describe.serial()` creates order-dependent tests that break parallel sharding `[Playwright only]` — search `.spec.*/.test.*` for `\.describe\.serial\(`. Exclude lines where `// JUSTIFIED` appears on the line above.
- **#9 Hard-coded Sleeps** — explicit sleeps cause flakiness. Search `.ts/.js/.cy.*` for `waitForTimeout` or `cy\.wait\(\d`.

**Interpreting results:**
- Zero hits → no mechanical issues found, proceed to Phase 2
- Any hit → report each line as an issue (includes file:line)
- Lines where the **immediately preceding line** contains `// JUSTIFIED:` are intentional — skip them

**Output Phase 1 results as-is.** The LLM must not reinterpret them.

---

## Phase 2: LLM Review (Subjective Checks Only)

Patterns already detected in Phase 1 (#3, #4, #5, #6, #7, #8 partial, #9) are **skipped**.
The LLM performs only these checks:

| # | Check | Reason |
|---|-------|--------|
| 1 | Name-Assertion Alignment | Requires semantic interpretation |
| 2 | Missing Then | Requires logic flow analysis |
| 8 | Flaky Test Patterns | Requires context judgment for nth() and serial ordering |
| 10 | YAGNI in POM + Zombie Specs | Requires usage grep then judgment |

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

**Important:** `test.skip()` with a reason comment or reason string is intentional — do NOT flag or remove these. Only flag mid-test conditional skips that hide failures (see #5).

---

### Tier 1 — P0/P1 (always check)

#### 1. Name-Assertion Alignment `[LLM-only]`

**Symptom:** Test name promises something the assertions don't verify.

```typescript
// BAD — name says "status" but only checks visibility
test('should display user status', () => {
  await expect(status).toBeVisible();  // no status content check
});
```

**Rule:** Every noun in the test name must have a corresponding assertion. Add it or rename.

**Procedure:**
1. Extract all nouns from the test name (e.g., "should display user **status**")
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
await loadingSpinner.waitFor({ state: 'detached' }).catch(() => {});
```

**Rule (spec):** Never wrap assertions in try/catch. Use `test.skip()` in `beforeEach` if the test can't run.

**Rule (POM):** Remove `.catch(() => {})` / `.catch(() => false)` from wait/assertion methods. If the operation can legitimately fail, the caller should decide how to handle it. Only keep catch for UI stabilization like `input.click({ force: true }).catch(() => textarea.focus())`.

#### 4. Always-Passing Assertions `[grep-detectable + LLM confirmation]`

**Symptom:** Assertion that can never fail.

```typescript
// BAD — count >= 0 is always true
expect(count).toBeGreaterThanOrEqual(0);

// SUSPECT — element may always be in DOM; needs review
await expect(page.locator('.app-shell')).toBeAttached();

// SUSPECT — boolean resolves immediately, no auto-retry
const visible = await page.getByText('welcome').isVisible();
expect(visible).toBe(true);
```

**Rule:** Search for `toBeGreaterThanOrEqual(0)` and `toBeAttached()`. Also flag `expect(await.*\.isVisible\(\))` — these resolve a one-shot boolean with no retry; use `expect(locator).toBeVisible()` instead (web-first, auto-retries). For `toBeAttached()` hits with no `// JUSTIFIED:` on the line above, confirm whether the element can ever be absent from the DOM. If it is unconditionally rendered or always present in the static HTML shell, the assertion is vacuous → flag P0. If `// JUSTIFIED:` explains the element is intentionally CSS-hidden (`visibility:hidden`, not `display:none`), skip.

**Fix:** Replace `toBeGreaterThanOrEqual(0)` with `toBeGreaterThan(0)`. Replace vacuous `toBeAttached()` with `toBeVisible()`, or remove if other assertions already cover the element. `expect(await el.isVisible()).toBe(true)` → `await expect(el).toBeVisible()`

#### 5. Bypass Patterns `[grep-detectable]`

Two sub-patterns that suppress what the framework would normally catch — making tests pass when they should fail.

**5a. Conditional assertion bypass** — `expect()` inside `if` block or mid-test `test.skip()`.

```typescript
// BAD — if spinner never appears, assertion never runs
if (await spinner.isVisible()) {
  await expect(spinner).toBeHidden({ timeout: 5000 });
}
```

**Rule:** Every test path must contain at least one `expect()`. Move environment checks to `beforeEach` or declaration-level `test.skip()`.

**5b. Force true bypass** — `{ force: true }` skips actionability checks (visibility, enabled state, pointer-events), hiding real UX problems that real users would encounter.

**Rule:** Each `{ force: true }` must have `// JUSTIFIED:` on the line above explaining why the element is not normally actionable. Without a comment, flag P1.

#### 6. Raw DOM Queries (Bypassing Framework API) `[grep-detectable]`

**Symptom:** Test uses `document.querySelector*` / `document.getElementById` inside `evaluate()` or `waitForFunction()` when the framework's element API could do the same job.

**Why it matters:** No auto-waiting, no retry, boolean trap, framework error messages lost.

```typescript
// BAD
await page.waitForFunction(() => document.querySelectorAll('.item').length > 0);
const has = await page.evaluate(() => !!document.querySelector('.result'));

// GOOD
await page.locator('.item').waitFor({ state: 'attached' });
await expect(page.locator('.result')).toBeVisible();
```

**Rule:** Use the framework's element API instead of raw DOM:
- **Playwright:** `locator.waitFor({ state: 'attached' })` replaces `waitForFunction(() => querySelector(...) !== null)`; `page.locator()` + web-first assertions replaces `evaluate(() => querySelector(...))`
- **Cypress:** `cy.get()` / `cy.find()` — avoid `cy.window().then(win => win.document.querySelector(...))`
- **Puppeteer:** `page.$()` / `page.waitForSelector()` — avoid `page.evaluate(() => document.querySelector(...))`

Only use `evaluate`/`waitForFunction` when the framework API genuinely can't express the condition: multi-condition AND/OR logic, `getComputedStyle`, `children.length`, cross-element DOM relationships, or `body.textContent` checks. Add `// JUSTIFIED:` explaining why.

#### 7. Focused Test Leak (`test.only` / `it.only`) `[grep-detectable]`

**Symptom:** A `.only` modifier left in committed code causes CI to run only the focused test(s) and silently skip the rest of the suite — all other tests show as "not run" but the CI step passes.

```typescript
// SILENT CI DISASTER — every other test in the suite is skipped
test.only('should show user profile', async ({ page }) => { ... });
it.only('submit form', () => { ... });      // Jest / Cypress
describe.only('auth flow', () => { ... });
```

**Rule** (Playwright & Cypress best practices): `.only` is a development-time focus tool. It must never be committed. Search `.spec.*/.test.*/.cy.*` for `\.(only)\(` — every hit is P0. No `// JUSTIFIED:` exemption exists; there are no legitimate committed uses.

**Fix:** Delete the `.only` modifier. If the test is intentionally isolated, use `test.skip()` with a reason on the others, or run a single file via the CLI (`--grep` / `--spec`).

---

### Tier 2 — P1/P2 (check when time permits)

#### 8. Flaky Test Patterns `[LLM-only + grep]`

Two sub-patterns that cause tests to fail intermittently in CI or parallel runs.

**8a. Positional selectors** — `nth()`, `first()`, `last()` without a comment break when DOM order changes.

```typescript
// BAD — breaks if DOM order changes
await expect(items.nth(2)).toContainText('Settings');
```

**Rule:** Prefer `data-testid`, role-based, or attribute selectors. If `nth()` is unavoidable, add `// JUSTIFIED:` explaining why.

**Selector priority** (best → worst): `data-testid`/`data-cy` → role/label → `name` attr → `id` → class → generic. Class and generic selectors are "Never" — coupled to CSS and DOM structure.

**8b. Serial test ordering** `[Playwright only]` — `test.describe.serial()` makes tests order-dependent: a single failure cascades to all subsequent tests, and the suite can't be sharded.

**Rule:** Replace serial suites with self-contained tests using `beforeEach` for shared setup. If sequential flow is genuinely required, use a single test with `test.step()` blocks. If serial is unavoidable, add `// JUSTIFIED:` on the line above `test.describe.serial(`.

#### 9. Hard-coded Sleeps `[grep-detectable]`

**Symptom:** Explicit sleep calls pause execution for a fixed duration instead of waiting for a condition.

**Rule:** Never use explicit sleep (`waitForTimeout` / `cy.wait(ms)`) — rely on framework auto-wait or condition-based waits.

Note: `timeout` option values in `waitFor({ timeout: N })` or `toBeVisible({ timeout: N })` are NOT flagged — these are bounds, not sleeps.

#### 10. YAGNI — Dead Test Code `[LLM-only]`

Two sub-patterns: unused code in Page Objects, and zombie spec files.

**10a. YAGNI in Page Objects** — POM has locators or methods never referenced by any spec. Or a POM class extends a parent with zero additional members (empty wrapper class).

**Procedure:**
1. List all public members of each changed POM file
2. Grep each member across all test files and other POMs
3. Classify: USED / INTERNAL-ONLY (`private`) / UNUSED (delete)
4. Check if any POM class has zero members beyond what it inherits — empty wrappers add no value unless the convention is intentional

**Common patterns:** Convenience wrappers (`clickEdit()` when specs use `editButton.click()`), getter methods (`getCount()` when specs use `toHaveCount()`), state checkers (`isVisible()` when specs assert on locators directly), pre-built "just in case" locators, empty subclass created for future expansion.

**Single-use Util wrappers** — a separate `*Util` / `*Helper` class whose methods are each called from only one test. These add indirection with no reuse benefit; inline them. Keep a Util method only if called from **2+ tests** or invoked **2+ times** within one test.

**Rule:** Delete unused members. Make internal-only members `private`. Apply the 2+ threshold before creating or keeping Util methods — if a helper is called from only one place, inline it. Flag empty wrapper classes for review — they may be intentional convention or dead code.

**10b. Zombie spec files** — An entire spec file whose tests are all subsets of tests in another spec file covering the same feature. The file adds no coverage that isn't already verified elsewhere.

**Procedure:** After reviewing all files in scope, cross-check spec files with similar names or feature coverage. If every test in file A is a subset of a test in file B, flag file A for deletion.

**Common patterns:** `feature-basic.spec.ts` where every case also appears in `feature-full.spec.ts`; a 1–2 test file created as a "quick smoke" that was never expanded while a comprehensive suite grew alongside it.

**Rule:** Delete the zombie file. If any test in it is not covered elsewhere, migrate it to the comprehensive suite first.

**Output:**
```
| File | Member | Used In | Status |
|------|--------|---------|--------|
| modal-page.ts | openModal() | (none) | DELETE |
| modal-page.ts | closeButton | internal only | PRIVATE |
| search-page.ts | (class body empty) | — | REVIEW |
| basic.spec.ts | (entire file) | covered by full.spec.ts | DELETE |
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
| P1  | 5     | Flaky Selectors | settings.spec.ts |
| P2  | 2     | Hard-coded Sleeps | dashboard.spec.ts |

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
| 4 | Always-Passing | P0 | grep+LLM | `>=0`; `toBeAttached()` with no `// JUSTIFIED:`; `expect(await.*isVisible())` (no retry) → confirm if element can be absent |
| 5 | Bypass Patterns | P0/P1 | grep | `expect()` inside `if`; `force: true` without `// JUSTIFIED:` |
| 6 | Raw DOM Queries | P1 | grep | `document.querySelector` in `evaluate` |
| 7 | Focused Test Leak | P0 | grep | `test.only(`, `it.only(`, `describe.only(` — no `// JUSTIFIED:` exemption |
| 8 | Flaky Test Patterns | P1 | LLM+grep | `nth()` without comment; `test.describe.serial()` |
| 9 | Hard-coded Sleeps | P2 | grep | `waitForTimeout()`, `cy.wait(ms)` |
| 10 | YAGNI + Zombie Specs | P2 | LLM | Unused POM member; empty wrapper; single-use Util; zombie spec file (all tests covered elsewhere) |

---

## Suppression

When a grep-detected pattern is intentional, add `// JUSTIFIED: [reason]` on the **line immediately above** the flagged line. When reviewing grep hits, if the line immediately above contains `// JUSTIFIED:`, skip the hit. Each individual flagged line needs its own `// JUSTIFIED:` — a comment higher up in the block does not count.

**Exception — #7 Focused Test Leak:** `// JUSTIFIED:` does not suppress `.only` hits. There are no legitimate committed uses of `test.only` / `it.only` / `describe.only` — every hit is P0.
