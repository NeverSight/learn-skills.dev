---
name: full-test-coverage
description: "Read this skill to write, generate, or add test code. Trigger when: (1) user asks to write, add, create, or generate tests of any kind (unit tests, integration tests, API tests, E2E tests, Playwright tests, Vitest tests); (2) user has code with missing or zero tests and wants coverage; (3) user just implemented a new service, endpoint, feature, or module and needs tests for it; (4) user refactored code and wants to verify nothing broke with tests; (5) user wants to improve or expand existing test coverage. This skill produces complete, pyramid-shaped test suites — reads the code, selects only the necessary layers (unit/integration/API/E2E), and generates every file needed (schema tests, service tests, factories, helpers, cleanup utilities, spec files) following strict Vitest and Playwright patterns. Skip this skill when debugging failing tests, asking how to use testing APIs or tools, explaining testing concepts, configuring test runners, reviewing existing test code, or migrating between test frameworks."
---

# Full Test Coverage — Test Generation

Generate the right tests for every layer of the testing pyramid: unit, integration, API, and E2E. The skill analyzes the code, selects the correct layers, and implements each one following strict guidelines.

## Testing Pyramid

```
        ╔═══════════════════════╗
        ║    E2E Tests          ║  Playwright browser · user journeys
        ╠═══════════════════════╣
        ║  API Tests            ║  Playwright HTTP · HTTP contracts
        ╠═══════════════════════╣
        ║Integration            ║  Vitest + Prisma · every branch with real DB
        ╠═══════════════════════╣
        ║  Unit Tests           ║  Vitest · isolated logic, no I/O
        ╚═══════════════════════╝
```

## Layer Responsibility Matrix

Each concern is owned by exactly one layer. Do not duplicate responsibilities.

| Concern | Unit | Integration | API | E2E |
|---------|------|-------------|-----|-----|
| Zod field exhaustive validation | **Owner** | 1–2 wiring checks | 1 per endpoint | No |
| Service method branches | **Owner** (mocked deps) | **Owner** (real DB) | No | No |
| Pure utility functions | **Owner** | No | No | No |
| Mock call argument verification | **Owner** | No | No | No |
| HTTP contract (status codes, body) | No | No | **Owner** | No |
| Write verification (POST→GET, DELETE→404) | No | No | **Owner** | No |
| Authorization enforcement (401, 403) | No | **Owner** | **Owner** | No |
| External service calls (mocked) | **Owner** (vi.mock) | **Owner** (Wiremock) | No | No |
| DB persistence verification | No | **Owner** | No | No |
| Complete user journey through UI | No | No | No | **Owner** |
| Navigation and routing | No | No | No | **Owner** |

---

## Step 1: Analyze the Code

Before selecting layers or writing any tests, read the target code.

**First, discover the full scope. Use the Explore agent** (subagent_type=Explore, thoroughness="very thorough") with the following prompt:

> "Find all source files related to [domain keyword] in this repository. Search comprehensively:
> - Files and directories whose name contains the keyword in any case variant (kebab-case, camelCase, snake_case)
> - Files anywhere in the repo whose content references the domain — route registrations, class names, import paths
> - HTTP route handlers, service classes, Zod schemas/DTOs, utility modules, serverless/Lambda handlers, shared infrastructure
> - Follow import chains from every file found to include referenced schemas, services, clients, and error definitions
> Do not restrict the search to src/ or any assumed directory. Return a complete list of files with a one-line description of each."

Use the returned file list as the scope for all subsequent steps.

Then read:
- Zod schemas / DTOs
- Service classes (regardless of naming prefix)
- Route and request handlers
- Utility and shared modules
- DB schema (`prisma/schema.prisma`)
- Error definitions
- External service clients (if any)
- UI components / pages (if any — look for `data-testid` attributes)

Build an inventory:
- Schemas found: _list field names and rules_
- Service methods found: _list method names and their dependencies_
- HTTP endpoints found: _list METHOD /path_
- Utility functions found: _list exported functions_
- External service calls found: _list service names_
- UI pages found: _list page URLs_

Write a one-paragraph summary: "This module has X schemas, Y service methods, Z endpoints... Recommended layers: [list]."

---

## Step 2: Select Layers

Apply this decision tree after completing Step 1:

```
Does the code have Zod schemas or pure utility functions?
  YES → Unit tests required (always the baseline layer)

Does the code have service methods with branches (if/else, switch, throw)?
  YES → Unit tests (mocked) + Integration tests (real DB) required
  Why: unit tests prove logic; integration tests prove wiring with real DB.
        Together they are not redundant — they cover different failure modes.

Does the code expose HTTP endpoints?
  YES → API tests required (one spec file per endpoint)

Does the code have browser UI with data-testid attributes?
  YES → E2E tests required (one spec per feature area)
```

**Common combinations:**
- Pure utility library → Unit only
- Backend service, no UI → Unit + Integration + API (if endpoints exist)
- Full-stack feature → All four layers

State explicitly which layers are selected and which are skipped with a reason:
_"Skipping E2E: no browser UI found in this module."_

---

## Step 3: Generate Tests, Layer by Layer

Work bottom-up. Generate unit tests first, then integration, then API, then E2E. Complete and self-validate each layer before moving to the next.

### If Unit tests are selected:

Read `references/unit-testing.md` before writing any code.

Key steps:
1. Read schemas, service, utils, errors
2. Map every field × rule and every service branch as a case tree (write as comments first)
3. Create `schema.helper.ts` and `<domain>.unit-factory.ts`
4. Write schema tests (one `describe` per field, one `it()` per rule)
5. Write service tests (all branches mocked, exact mock argument verification)
6. Write utility tests (if applicable)
7. Run: `vitest run src/modules/<domain>/test/unit/`
8. Run self-validation checklist from the reference file

### If Integration tests are selected:

Read `references/integration-testing.md` before writing any code.

Key steps:
1. Read source + auth implementation + error response shape (determines assertion format)
2. List every execution path as comments inside `describe` blocks
3. Create `DatabaseHelper`, `AuthHelper`, fixtures, api-utils
4. Write handler tests (1–2 validation wiring tests per endpoint — no exhaustive Zod rules)
5. Write service layer tests (direct calls, real DB)
6. Run: `yarn test:integration` (or equivalent)
7. Run self-validation checklist from the reference file

### If API tests are selected:

Read `references/api-testing.md` before writing any code.

Key steps:
1. Read route handlers, DTOs, error definitions
2. Verify/create response helpers for all error codes
3. Create test-owned factory (never import backend DTOs)
4. Create API utilities (one function per endpoint)
5. Create cleanup utilities
6. Write test specs: plan scenarios as comments first, then implement
7. Run: `npx playwright test --project=api`
8. Run self-validation checklist from the reference file

### If E2E tests are selected:

Read `references/e2e-testing.md` before writing any code.

Key steps:
1. Read PRD, page components (`data-testid` attributes), existing fixtures
2. Identify user flows (one spec file per feature area)
3. Create or update Page Object Models (locators via `data-testid` only)
4. Create test data factory with `counter + timestamp + random` pattern
5. Create API-based setup helper and cleanup helper
6. Write test specs (API setup, inject auth, navigate, UI interaction, assert)
7. Run: `npx playwright test --project=chromium`
8. Run self-validation checklist from the reference file

---

## Universal Patterns

These apply at every layer. Do not repeat in reference files.

### Unique test data
```typescript
let counter = 0;
function uniqueSuffix(): string {
  counter++;
  return `${counter}-${Date.now()}-${Math.floor(Math.random() * 100000)}`;
}
// Usage: `test-user-${uniqueSuffix()}@test.com`
```
Why: parallel test runs share a database. Non-unique data causes false failures when one test's cleanup deletes another test's records.

### Arrange-Act-Assert
Every test follows this exact structure:
```typescript
// Arrange — set up state
const cookie = await authenticateUser(request);
const dto = generateCreateNoteDto();

// Act — execute the behavior
const response = await executePostNoteRequest(request, dto, cookie);

// Assert — verify the result
expect201Created(response);
expect(response.data.title).toBe(dto.title);
```

### Cleanup in afterEach
```typescript
// ✓ Correct — runs even when test throws
test.afterEach(async ({ request }) => {
  for (const cookie of cookiesToCleanup) {
    await cleanupNotes(request, cookie);
    await cleanupUser(request, cookie);
  }
  cookiesToCleanup.length = 0;
});

// ✗ Wrong — skipped when test throws before reaching cleanup
test("...", async ({ request }) => {
  const cookie = await authenticateUser(request);
  // ...
  await cleanupUser(request, cookie); // This line may never run
});
```

### No shared state between tests
- No `beforeAll` for shared data
- No shared auth sessions
- Each test creates its own user and test entities

### No static waits
```typescript
// ✗ Forbidden at all layers
await new Promise(resolve => setTimeout(resolve, 1000));
await page.waitForTimeout(5000);

// ✓ Use explicit conditions instead
// API/Integration: poll with 400ms interval, 15s timeout
// E2E: locator.waitFor(), page.waitForURL(), expect(locator).toBeVisible()
```

### No snapshot tests
`.toMatchSnapshot()` and `.toMatchInlineSnapshot()` are forbidden at all layers. Snapshots hide intent and produce opaque diffs.

### No hardcoded URLs
Always use relative paths. Playwright's `baseURL` from config handles environment switching.

---

## Reference File Guide

When generating tests for a layer, read the corresponding reference file first. Each file includes the full workflow, verbatim templates, and a self-validation checklist.

| File | Contains | Key templates |
|------|----------|---------------|
| `references/unit-testing.md` | 8-step workflow, Zod test patterns, mocking rules | `schema.helper.ts`, unit factory, service test structure |
| `references/integration-testing.md` | 5-step workflow, parallel-safe cleanup, validation wiring | `DatabaseHelper`, `AuthHelper` (both variants), fixture structure |
| `references/api-testing.md` | 8-step workflow, test-owned interfaces, write verification | `authenticateUser()`, API utilities, response helpers, per-endpoint test counts |
| `references/e2e-testing.md` | 9-step workflow, POM rules, waiting strategy | `createUserViaApi()`, `injectAuthCookie()`, Page Object Model, 5 wait patterns |

---

## Cross-Layer Checklist

After all layers are complete, verify the pyramid is correctly shaped:

**No layer duplication:**
- [ ] Unit tests cover Zod field validation exhaustively — integration/API/E2E do not
- [ ] Integration tests have only 1–2 validation wiring tests per endpoint
- [ ] API tests have only 1 validation test per endpoint
- [ ] E2E tests cover user journeys and navigation — no field validation

**Pyramid shape (count tests per layer):**
- [ ] Unit tests cover the most cases — exhaustive per field and per branch
- [ ] Integration tests are fewer — only real DB wiring and auth paths
- [ ] API tests are fewer still — one spec per endpoint
- [ ] E2E tests are the fewest — one spec per user journey

**All self-validation checklists were run:**
- [ ] Unit layer checklist ✓
- [ ] Integration layer checklist ✓
- [ ] API layer checklist ✓
- [ ] E2E layer checklist ✓

---

## Cross-Layer Examples

The same "notes" domain — showing exactly how coverage is divided, not duplicated.

### Testing a `title` field (min 1, max 255, required)

| Layer | What to test | Test count |
|-------|-------------|-----------|
| **Unit** | missing, undefined, null, empty string, min boundary (1 char ✓), max boundary (255 chars ✓), 256 chars ✗, wrong type (number) | 8+ tests |
| **Integration** | one representative: missing title → 400 VALIDATION_ERROR (proves Zod is wired) | 1 test |
| **API** | one representative: missing title → 400 (verifies HTTP contract) | 1 test |
| **E2E** | nothing — E2E tests do not test field validation | 0 tests |

### Testing a `notFound` service branch

| Layer | What to test |
|-------|-------------|
| **Unit** | mock `prisma.note.findUnique` to return null → verify `Errors.notFound()` thrown; verify downstream mocks NOT called |
| **Integration** | request with a real non-existent ID in DB → verify 404 response with correct `NOT_FOUND` code |
| **API** | `GET /api/notes/:nonExistentId` → verify 404 with correct error body |
| **E2E** | nothing — E2E tests don't test error branches |

### Testing an authorization rule

| Layer | What to test |
|-------|-------------|
| **Unit** | mock `prisma.note.findUnique` to return a note with `organizationId: "other-org"` → verify `Errors.forbidden()` thrown; verify update mock NOT called |
| **Integration** | user B requests note owned by user A's organization → verify 403 FORBIDDEN response and DB unchanged |
| **API** | user B requests note owned by user A → verify 403 response |
| **E2E** | verify user B cannot see user A's notes in the UI (data isolation test) |

---

## Completion

After all layers are generated, provide:

**File inventory per layer:**

| Layer | Files created | Run command |
|-------|-------------|-------------|
| Unit | `<domain>.schema.test.ts`, `<domain>.service.test.ts`, `schema.helper.ts`, `<domain>.unit-factory.ts` | `vitest run src/modules/<domain>/test/unit/` |
| Integration | `<endpoint>.test.ts` (×N), `<domain>.service.test.ts`, `database.helper.ts`, `auth.helper.ts`, `<domain>.fixture.ts`, api-utils | `yarn test:integration` |
| API | `<method>-<endpoint>.spec.ts` (×N), `<domain>.factory.ts`, `<domain>.api-utils.ts`, `<domain>.cleanup.ts` | `npx playwright test --project=api` |
| E2E | `<domain>.<feature>.spec.ts`, `<domain>.page.ts`, `<domain>.factory.ts`, setup.ts, cleanup.ts | `npx playwright test --project=chromium` |

