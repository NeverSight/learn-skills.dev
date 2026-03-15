---
name: e2e-test
description: '[Testing] Use when generating, updating, or maintaining E2E tests from recordings, specs, or code changes. Supports Playwright, Selenium, Cypress, and other frameworks.'
---

# Skill: e2e-test

**Category:** [Testing]
**Trigger:** e2e test, e2e from recording, generate e2e, playwright test, cypress test, selenium test, webdriver, puppeteer

Generate and maintain E2E tests using the project's configured testing framework.

- `docs/test-specs/` — Test specifications by module (read existing TCs for E2E scenario coverage; match TC codes to E2E test implementations)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

---

## ⚠️ MANDATORY: Read Project E2E Reference (FIRST)

**BEFORE ANY E2E WORK, you MUST:**

```bash
# 1. Read project-specific E2E patterns (REQUIRED)
head -100 docs/project-reference/e2e-test-reference.md

# 2. Read project config for framework, paths, commands
grep -A 50 '"e2eTesting"' docs/project-config.json

# 3. Find TC codes you need to implement
grep -r "TC-.*-E2E-" docs/test-specs/ docs/business-features/
```

**The `e2eTesting` section in `docs/project-config.json` contains:**

- Framework, language, paths, run commands, TC code format
- Project-specific best practices and entry points

**When investigating/fixing E2E failures, update `docs/project-reference/e2e-test-reference.md` with learnings.**

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

---

## Framework Detection (SECOND STEP)

Detect the project's E2E stack before generating tests:

```bash
# TypeScript/JavaScript
grep -l "playwright\|cypress\|selenium\|webdriver" package.json 2>/dev/null
ls playwright.config.* cypress.config.* wdio.conf.* 2>/dev/null

# C# .NET
grep -r "Selenium.WebDriver\|Microsoft.Playwright" **/*.csproj 2>/dev/null
```

| Framework    | Config File          | Test Extension | Run Command           |
| ------------ | -------------------- | -------------- | --------------------- |
| Playwright   | playwright.config.ts | \*.spec.ts     | `npx playwright test` |
| Cypress      | cypress.config.ts    | \*.cy.ts       | `npx cypress run`     |
| WebdriverIO  | wdio.conf.js         | \*.e2e.ts      | `npx wdio run`        |
| Selenium.NET | \*.csproj            | \*Tests.cs     | `dotnet test`         |

---

## Workflow Modes

| Mode             | Input                      | Output                       |
| ---------------- | -------------------------- | ---------------------------- |
| `from-recording` | Recording JSON + feature   | Test spec + page object      |
| `update-ui`      | Git diff of UI changes     | Updated screenshot baselines |
| `from-changes`   | Changed test specs or code | Updated test implementations |
| `from-spec`      | TC codes from test specs   | New tests matching specs     |

---

## Core Principles

### 1. TC Code Traceability (MANDATORY)

**Every E2E test MUST have:**

- TC code in test name: `TC-{MODULE}-E2E-{NNN}`
- Tag/trait linking to spec
- Comment linking to feature doc

```typescript
// TypeScript
test('TC-LR-E2E-001: Submit leave request', async () => { ... });
```

```csharp
// C# .NET
[Fact]
[Trait("TC", "TC-LR-E2E-001")]
public async Task SubmitLeaveRequest() { ... }
```

### 2. Page Object Model

All frameworks should use Page Object pattern:

- Encapsulate page locators in page class
- Methods represent user actions
- Assertions in test file, not page object

### 3. Selector Strategy (Priority Order)

1. **Semantic classes** — BEM (`.block__element`), component classes
2. **Data attributes** — `[data-testid]`, `[data-cy]`, `[data-test]`
3. **ARIA/Role** — `role=button`, `aria-label`
4. **Text content** — Visible user text (last resort)

**AVOID:** Generated classes (`.ng-star-inserted`, `.MuiButton-root`), positional selectors (`:nth-child`), XPath

### 4. Unique Test Data

Tests must generate unique data to be repeatable:

- Append GUIDs/timestamps to test data
- Don't depend on specific database state
- Don't clean up data (creates side effects)

### 5. Preconditions Documentation

Document what must exist before test runs:

- System: Infrastructure running, APIs healthy
- Data: Seed data exists (users, companies)
- Feature: Configurations complete

---

## Steps

1. **Detect framework** from project files
2. **Read project E2E docs** for conventions and patterns
3. **Load test specs** with TC codes from feature docs
4. **Generate/update tests** following Page Object pattern
5. **Run tests** using project's configured commands
6. **Update e2e-test-reference.md** with any learnings

---

## Output

Report:

- Files created/modified
- TC codes covered
- Run command to execute tests
- Any preconditions or setup needed

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `e2e-from-changes` workflow** (Recommended) — scout → e2e-test → test → watzup
> 2. **Execute `/e2e-test` directly** — run this skill standalone
