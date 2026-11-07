---
name: create-tests
description: Generate Playwright E2E and Vitest unit tests for features, APIs, pages, components, and permissions (and RLS on a Supabase project), plus optional k6 load tests. Creates test files with proper setup, cleanup, and coverage. Use when the user needs tests, testing, E2E tests, API tests, security tests, load tests, or wants to test a feature.
argument-hint: "[target file or feature] [type: api|page|component|e2e|unit|security|load|permissions]"
---

# Create Tests

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

Generate comprehensive tests using Playwright (E2E/API/Page/Security) and Vitest (unit). Optionally generate k6 load tests.

> **Delegate large test work.** For coverage-gap analysis or authoring a big suite in parallel with feature work, hand it to the `test-engineer` subagent (see `subagent-delegation`), then run and verify the tests on the main thread.

## Two-Tier Testing Strategy

| Tier                  | Purpose                                | Auth Required | Command                                       |
| --------------------- | -------------------------------------- | ------------- | --------------------------------------------- |
| **Tier 1: Storybook** | Isolated component testing             | No            | `pnpm storybook:form` / `pnpm test:storybook` |
| **Tier 2: DaaS E2E**  | Full integration testing with real API | Yes           | `pnpm test` / `pnpm test:e2e`                 |

## Test File Location

<!-- buildpad-backend: supabase -->
```
tests/
├── auth.setup.ts                    # Global auth setup (auto-provisions test users)
├── setup-test-users.ts              # Legacy test user setup helper (optional)
├── helpers/
│   ├── test-utils.ts               # Shared test utilities
│   ├── test-fixtures.ts            # Database fixtures
│   └── auth-tokens.ts              # Auth token helpers (Bearer tokens for API)
├── api/                            # API endpoint tests → [endpoint].spec.ts
│   ├── rls-*.spec.ts               # Row-Level Security tests
│   ├── field-permissions/          # Field-level permission tests
│   ├── item-level-filtering/       # Item filtering tests
│   └── data-model/                 # Schema/field/relation tests
├── pages/                          # Page tests → [page].spec.ts (permissions-aware UI)
├── ui/                             # UI E2E tests → [feature].spec.ts
├── components/                     # Component tests → [component].spec.ts
├── e2e/                            # User flow tests → [flow].spec.ts
├── security/                       # Security-specific tests
└── load/                           # k6 Load testing
    ├── items-load-test.js          # Main k6 test script
    └── README.md                   # Load testing guide
```

<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
tests/
├── setup-test-users.ts              # Creates the test roles and users through the Engine's API
├── auth.setup.ts                    # Global auth setup (signs each test user in, saves storage states)
├── helpers/
│   ├── test-utils.ts               # Shared test utilities
│   ├── test-fixtures.ts            # Data fixtures, created through the API
│   └── auth-tokens.ts              # Direct sign-in and Bearer tokens for Engine API tests
├── api/                            # API endpoint tests → [endpoint].spec.ts
│   ├── access-*.spec.ts            # Access tests (roles, policies, permissions, scope)
│   ├── field-permissions/          # Field-level permission tests
│   ├── item-level-filtering/       # Item filtering tests
│   └── data-model/                 # Schema/field/relation tests
├── pages/                          # Page tests → [page].spec.ts (permissions-aware UI)
├── ui/                             # UI E2E tests → [feature].spec.ts
├── components/                     # Component tests → [component].spec.ts
├── e2e/                            # User flow tests → [flow].spec.ts
├── security/                       # Security-specific tests
└── load/                           # k6 Load testing
    ├── items-load-test.js          # Main k6 test script
    └── README.md                   # Load testing guide
```

<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
## Process

1. **Analyze the target** — read the code, identify HTTP methods, UI elements, user flows, permissions
2. **Determine test types needed** — API, Page, Component, Security/RLS, Permissions, E2E, Load
3. **Create test file(s)** in the correct directory
4. **Write tests** with proper setup/cleanup following the patterns below
5. **Run tests** — `pnpm test tests/[type]/[name].spec.ts`
6. **Ensure all pass** before reporting completion

<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Process

1. **Analyze the target** — read the code, identify HTTP methods, UI elements, user flows, permissions
2. **Determine test types needed** — API, Page, Component, Access (roles, policies, permissions, scope), Permissions UI, E2E, Load
3. **Create test file(s)** in the correct directory
4. **Write tests** with proper setup/cleanup following the patterns below
5. **Run tests** — `pnpm test tests/[type]/[name].spec.ts`
6. **Ensure all pass** before reporting completion

<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
## Authentication Setup

Tests use Playwright's storage state for reusable auth across different user types. The `auth.setup.ts` file auto-provisions test users via Supabase admin API.

**Auto-provisioned users (created by auth.setup.ts):**

| Auth File                        | User                      | Permissions                                              |
| -------------------------------- | ------------------------- | -------------------------------------------------------- |
| `admin.json`                     | `admin@example.com`       | Full access (policy grants admin_access)                 |
| `user.json`                      | `e2e-basic-user@test.com` | Non-admin, no special permissions                        |
| `readonly.json`                  | `e2e-readonly@test.com`   | Read permission on core collections                      |
| `user-with-read-permission.json` | `e2e-read-perm@test.com`  | Read permission on daas_users, daas_roles, daas_policies |

**Required env vars:** `NEXT_PUBLIC_SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` in `.env.local`.

**Run auth setup:**

```bash
pnpm exec playwright test --project=setup
```

**For custom permission test users** (item-level filtering, field permissions), create dedicated setup scripts:

```bash
node scripts/setup-filter-tests.mjs      # Item-level filtering users
pnpm tsx scripts/setup-field-permission-tests.ts  # Field permission users
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Authentication Setup

Tests use Playwright's storage state for reusable auth across different user types. On an Engine project `tests/setup-test-users.ts` creates the test roles and users through the Engine's API with the test administrator's session, and `auth.setup.ts` signs each test user in through the application's login page and saves its storage state.

On an Engine project an administrator creates every user who signs in with a password, through the Engine's user API (`POST /api/users` with an administrator's session) or the Studio's Users module, and gives the user a role in the project's tenant (`POST /api/users/:id/roles` with `role_id`, or the Users module). A user's first XAppHub sign-in creates that user's account, which holds no role until an administrator gives it one in the same way. An administrator resets a user's password, in the Studio's Users module.

On an Engine project tests create their users and roles as an administrator does (above), sign in with each user's email and password, and use the Engine environment of **Required env vars**. The only secrets a pipeline needs are the test administrator's email and password; it needs no Supabase secret.

**The test administrator** is an account that an administrator creates once, in the Studio's Users module, with a role whose policy has administrator access. Its email and password are the pipeline's two secrets, `TEST_ADMIN_EMAIL` and `TEST_ADMIN_PASSWORD`; on a developer's machine they are in `.env.test.local`, which is not committed. Never write them in a test file, and never use the token in the project's MCP configuration instead: the data API refuses it.

**Test users (created by `setup-test-users.ts`, signed in by `auth.setup.ts`):**

| Auth File       | User                      | Permissions                                     |
| --------------- | ------------------------- | ----------------------------------------------- |
| `admin.json`    | `TEST_ADMIN_EMAIL`        | Full access (its policy has administrator access) |
| `user.json`     | `e2e-basic-user@test.com` | Non-admin; its role has no policy               |
| `readonly.json` | `e2e-readonly@test.com`   | Read permission on the collections under test   |
| `editor.json`   | `e2e-editor@test.com`     | Read and update                                 |
| `creator.json`  | `e2e-creator@test.com`    | Read and create                                 |
| `noperm.json`   | `e2e-noperm@test.com`     | None; its role has no policy                    |

Every test user holds a role in the project's tenant, a user without permissions included: an account that holds no role in the project's tenant is refused at sign-in.

**Required env vars** (in `.env.test.local`): the project's environment — `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_BUILDPAD_DAAS_URL` (both the Engine_URL), `NEXT_PUBLIC_SUPABASE_ANON_KEY` (the fixed public value) and `NEXT_PUBLIC_BUILDPAD_TENANT_ID` — and `TEST_ADMIN_EMAIL` and `TEST_ADMIN_PASSWORD`. There is no service-role key on an Engine project: add none.

**Signing in from a script.** On an Engine project the data API serves no request without a session; only the sign-in, `GET /api/server/info` and the Engine's password routes (which an application does not use: password recovery is not available on an Engine project) are served without one. The requests that take their tenant from the header `X-Tenant-Id` are the password sign-in, XAppHub sign-in and anonymous reads of public files. A browser can send `X-Tenant-Id` to the Engine from another origin, without cookies or credentials: the Engine allows that header from any origin and allows no credentialed cross-origin request. Even so, the request that names the tenant is the sign-in made through the application's own server route, which sends `X-Tenant-Id` with the value of `NEXT_PUBLIC_BUILDPAD_TENANT_ID`. A public file shown in a browser is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read. A request without a session that names no tenant is served from the Engine's host plane, not from the project. A request with a session takes its tenant from the session.

A setup script or an API test runs in Node, not in a browser, so it signs in directly and sends `X-Tenant-Id` itself, with the value of `NEXT_PUBLIC_BUILDPAD_TENANT_ID`, in one of two ways:

- password sign-in through the Supabase client, created against the Engine_URL with the global header `X-Tenant-Id`;
- `POST <Engine_URL>/api/auth/login` with the header `X-Tenant-Id` and the body `{ "email": "...", "password": "...", "tenant": "<the tenant id>" }`. The body's `tenant` names the tenant the session acts in. The answer is `{ "data": { "access_token": "...", "refresh_token": "...", "expires": <Unix time> } }`.

Send the access token as `Authorization: Bearer <access token>`. It expires after one hour unless the Engine's operator set another lifetime; sign in again then.

**Budgets.** The Engine limits how fast tests may create accounts and send requests:

- **Account creation:** 30 account creations (or address changes) per caller per 10 minutes, unless the Engine's operator set `USERS_CREATE_RATE_LIMIT` and `USERS_CREATE_RATE_WINDOW`. Every `POST /api/users` spends it, one refused as a duplicate (`409`) included. Beyond it the Engine answers `429` (`REQUESTS_EXCEEDED`, with `Retry-After`). So `setup-test-users.ts` looks each user up first (`GET /api/users?search=<email>`) and creates only the missing ones, and no test creates a user on every run.
- **Requests:** 20 requests per second per client address, unless the operator set `RATE_LIMIT_RPS`. Beyond it the Engine answers `429` (`REQUESTS_EXCEEDED`). The requests a test sends through the application's routes reach the Engine from the application's address, so the whole suite shares one budget: keep `workers` low against a shared Engine.
- **Sign-in:** the Engine checks a limited number of passwords at a time and answers `503` when it cannot check one in time. Sign the test users in one after another, not in parallel.

**Run setup:**

```bash
pnpm tsx tests/setup-test-users.ts        # once, and again after adding a test user
pnpm exec playwright test --project=setup
```

**For custom permission test users** (item-level filtering, field permissions), create dedicated setup scripts. They create roles, policies, permissions and users through the Engine's API with the test administrator's session (see the [create-rbac](../create-rbac/SKILL.md) skill), look users up before creating them, and save the users' access tokens to `playwright/.auth/tokens.json`:

```bash
node scripts/setup-filter-tests.mjs      # Item-level filtering users
pnpm tsx scripts/setup-field-permission-tests.ts  # Field permission users
```
<!-- /buildpad-backend -->

## API Test Pattern

<!-- buildpad-backend: supabase -->
```typescript
import { test, expect } from "@playwright/test";

test.describe("[Feature] API", () => {
  let createdIds: string[] = [];

  test.afterEach(async () => {
    for (const id of createdIds) {
      await deleteTestDataViaAPI(`/api/[endpoint]/${id}`);
    }
    createdIds = [];
  });

  test("GET returns all items", async ({ request }) => {
    const response = await request.get("http://localhost:3000/api/[endpoint]");
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(Array.isArray(data.data)).toBeTruthy();
  });

  test("POST creates with valid data", async ({ request }) => {
    const response = await request.post(
      "http://localhost:3000/api/[endpoint]",
      { data: { name: "Test" } },
    );
    expect(response.status()).toBe(201);
    const data = await response.json();
    createdIds.push(data.data.id);
  });

  test("POST validates required fields", async ({ request }) => {
    const response = await request.post(
      "http://localhost:3000/api/[endpoint]",
      { data: {} },
    );
    expect(response.status()).toBe(400);
  });
});
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```typescript
import { test, expect } from "@playwright/test";
import { deleteTestDataViaAPI } from "../helpers/test-utils";

test.describe("[Feature] API", () => {
  test.use({ storageState: "playwright/.auth/admin.json" });
  let createdIds: string[] = [];

  test.afterEach(async ({ request }) => {
    for (const id of createdIds) {
      await deleteTestDataViaAPI(`/api/[endpoint]/${id}`, request);
    }
    createdIds = [];
  });

  test("GET returns all items", async ({ request }) => {
    const response = await request.get("http://localhost:3000/api/[endpoint]");
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.data).toBeDefined();
    expect(Array.isArray(data.data)).toBeTruthy();
  });

  test("POST creates with valid data", async ({ request }) => {
    const response = await request.post(
      "http://localhost:3000/api/[endpoint]",
      { data: { name: "Test" } },
    );
    expect(response.status()).toBe(200); // the Engine answers a create on /api/items with 200
    const data = await response.json();
    createdIds.push(data.data.id);
  });

  test("POST validates required fields", async ({ request }) => {
    const response = await request.post(
      "http://localhost:3000/api/[endpoint]",
      { data: {} },
    );
    expect(response.status()).toBe(400);
  });
});
```

On an Engine project `/api/items` answers a create with `200`, a delete of one item with `204` and no body, and a delete of several with `200` and a body, and a route that passes the Engine's answer through answers the same. A create on `/api/users`, `/api/roles`, `/api/policies` or `/api/permissions` answers `201`.
<!-- /buildpad-backend -->

## DaaS Query Parameters Test Pattern

Test DaaS-compatible query parameters for every collection endpoint:

```typescript
test.describe("Query Parameters", () => {
  // Fields parameter
  test("should return specific fields only", async ({ request }) => {
    const response = await request.get("/api/[endpoint]?fields=id,name,status");
    const data = await response.json();
    const keys = Object.keys(data.data[0]);
    expect(keys).toContain("id");
    expect(keys).not.toContain("password");
  });

  // Filter parameter
  test("should filter with _eq operator", async ({ request }) => {
    const filter = JSON.stringify({ status: { _eq: "active" } });
    const response = await request.get(`/api/[endpoint]?filter=${filter}`);
    const data = await response.json();
    data.data.forEach((item: any) => expect(item.status).toBe("active"));
  });

  // Search parameter
  test("should search across text fields", async ({ request }) => {
    const response = await request.get("/api/[endpoint]?search=keyword");
    expect(response.status()).toBe(200);
  });

  // Sort parameter
  test("should sort descending with - prefix", async ({ request }) => {
    const response = await request.get("/api/[endpoint]?sort=-date_created");
    expect(response.status()).toBe(200);
  });

  // Pagination parameters
  test("should paginate with limit and offset", async ({ request }) => {
    const response = await request.get("/api/[endpoint]?limit=10&offset=0");
    const data = await response.json();
    expect(data.data.length).toBeLessThanOrEqual(10);
  });

  // Meta parameter
  test("should return total_count in meta", async ({ request }) => {
    const response = await request.get("/api/[endpoint]?meta=total_count");
    const data = await response.json();
    expect(data.meta.total_count).toBeDefined();
  });
});
```

<!-- buildpad-backend: supabase -->
## Security / RLS Test Pattern

Every collection/endpoint must include Row-Level Security tests:
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Security / Access Test Pattern

Every collection/endpoint must include access tests. On an Engine project access is roles, policies and permissions, which the Engine enforces on every request, and data is separated by scope inside the project's tenant: test them through the API, with the users of `setup-test-users.ts`. There is no database policy to test. The pattern below holds on an Engine project as written (its names say RLS):
<!-- /buildpad-backend -->

```typescript
import { test, expect } from "@playwright/test";

test.describe("[Feature] RLS Security", () => {
  // Test authentication (401)
  test("should return 401 without authentication", async ({ request }) => {
    const response = await request.get("/api/[endpoint]", {
      headers: { Authorization: "" },
    });
    expect(response.status()).toBe(401);
  });

  // Test authorization (403)
  test.describe("Non-Admin Access", () => {
    test.use({ storageState: "playwright/.auth/user.json" });

    test("should return 403 for admin-only operations", async ({ request }) => {
      const response = await request.delete("/api/[endpoint]/some-id");
      expect(response.status()).toBe(403);
    });
  });

  // Test admin bypass
  test.describe("Admin Access", () => {
    test.use({ storageState: "playwright/.auth/admin.json" });

    test("admin should access all resources", async ({ request }) => {
      const response = await request.get("/api/[endpoint]");
      expect(response.status()).toBe(200);
    });
  });

  // Test self-access pattern
  test("user should only see own records when filtered", async ({
    request,
  }) => {
    // Use auth state for a user with self-access filter
    // Verify only their records are returned
  });

  // Test data isolation
  test("should not expose cross-user data", async ({ request }) => {
    // Verify user A cannot access user B's records
  });
});
```

<!-- buildpad-backend: supabase -->
## Permissions-Aware UI Test Pattern

Test that the frontend correctly shows/hides features based on user permissions:

```typescript
test.describe("[Feature] Permissions UI", () => {
  test.describe("Admin User", () => {
    test.use({ storageState: "playwright/.auth/admin.json" });

    test("should show all action buttons", async ({ page }) => {
      await page.goto("/[feature]");
      await expect(page.getByRole("button", { name: "Add" })).toBeVisible();
      // Edit and Delete buttons visible in table rows
    });
  });

  test.describe("Read-Only User", () => {
    test.use({ storageState: "playwright/.auth/readonly.json" });

    test("should hide create button", async ({ page }) => {
      await page.goto("/[feature]");
      await expect(page.getByRole("button", { name: "Add" })).toBeHidden();
    });

    test("should disable edit actions", async ({ page }) => {
      await page.goto("/[feature]");
      // Edit buttons disabled or hidden
    });
  });

  test.describe("No-Permission User", () => {
    test.use({ storageState: "playwright/.auth/noperm.json" });

    test("should redirect or show no access", async ({ page }) => {
      await page.goto("/[feature]");
      // Should redirect or show "No access" message
    });
  });
});
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Permissions-Aware UI Test Pattern

Test that the frontend correctly shows/hides features based on user permissions. On an Engine project the frontend reads them from `GET /api/permissions/me`, which answers `{ "data": { "<collection>": { "<action>": { ... } } }, "isAdmin": ..., "moduleAccess": { ... }, "meta": { ... } }`. `isAdmin` sits beside `data`, not inside it, and for an administrator `data` is `{}`: a screen checks `isAdmin` before it reads `data`.

```typescript
test.describe("[Feature] Permissions UI", () => {
  test.describe("Permissions answer", () => {
    test.use({ storageState: "playwright/.auth/admin.json" });

    test("reports the administrator beside data", async ({ request }) => {
      const response = await request.get("/api/permissions/me");
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.isAdmin).toBe(true);
      expect(body.data).toEqual({});
    });
  });

  test.describe("Admin User", () => {
    test.use({ storageState: "playwright/.auth/admin.json" });

    test("should show all action buttons", async ({ page }) => {
      await page.goto("/[feature]");
      await expect(page.getByRole("button", { name: "Add" })).toBeVisible();
      // Edit and Delete buttons visible in table rows
    });
  });

  test.describe("Read-Only User", () => {
    test.use({ storageState: "playwright/.auth/readonly.json" });

    test("should hide create button", async ({ page }) => {
      await page.goto("/[feature]");
      await expect(page.getByRole("button", { name: "Add" })).toBeHidden();
    });

    test("should disable edit actions", async ({ page }) => {
      await page.goto("/[feature]");
      // Edit buttons disabled or hidden
    });
  });

  test.describe("No-Permission User", () => {
    test.use({ storageState: "playwright/.auth/noperm.json" });

    test("should redirect or show no access", async ({ page }) => {
      await page.goto("/[feature]");
      // Should redirect or show "No access" message
    });
  });
});
```
<!-- /buildpad-backend -->

## Field-Level Permissions Test Pattern

Test that field access control correctly filters responses and validates writes:

```typescript
test.describe("Field-Level Permissions", () => {
  test("admin should see all fields", async ({ request }) => {
    const response = await request.get("/api/[endpoint]/item-id");
    const data = await response.json();
    expect(Object.keys(data.data)).toContain("sensitive_field");
  });

  test("limited user should see only allowed fields", async ({ request }) => {
    // Use limited-user auth
    const response = await request.get("/api/[endpoint]/item-id");
    const data = await response.json();
    expect(Object.keys(data.data)).not.toContain("sensitive_field");
  });

  test("should block writes to forbidden fields", async ({ request }) => {
    // Use limited-user auth
    const response = await request.patch("/api/[endpoint]/item-id", {
      data: { forbidden_field: "value" },
    });
    expect(response.status()).toBe(403);
  });
});
```

## Page Test Pattern

```typescript
test.describe("[Page] List", () => {
  test.use({ storageState: "playwright/.auth/admin.json" });

  test("displays page title", async ({ page }) => {
    await page.goto("/[path]");
    await expect(page.locator("h1, h2").first()).toBeVisible();
  });

  test("displays data table", async ({ page }) => {
    await page.goto("/[path]");
    await expect(page.locator("table")).toBeVisible();
  });

  test("navigates to detail on row click", async ({ page }) => {
    await page.goto("/[path]");
    await page.waitForSelector("tbody tr", { timeout: 10000 });
    await page.locator("tbody tr").first().click();
    await page.waitForURL(/\/\[path\]\/[a-f0-9-]+/, { timeout: 5000 });
  });

  test("filters when searching", async ({ page }) => {
    await page.goto("/[path]");
    const searchInput = page
      .locator('input[type="search"], input[placeholder*="Search"]')
      .first();
    await searchInput.fill("search term");
    await page.waitForTimeout(800); // Debounce
    expect(await page.locator("tbody tr").count()).toBeGreaterThanOrEqual(1);
  });
});
```

## Mantine / Buildpad UI Selector Strategies

Use these selector patterns for Mantine v8 / Buildpad components:

```typescript
// ✅ RECOMMENDED: Role-based selectors (most reliable)
await page.getByRole("textbox", { name: "Email" }).fill("test@example.com");
await page.getByRole("button", { name: "Sign In" }).click();

// ✅ For PasswordInput (Mantine), use role with exact match
await page
  .getByRole("textbox", { name: "Password", exact: true })
  .fill("password");

// ✅ Data test IDs (most reliable for complex components)
await page.getByTestId("submit-button").click();

// ✅ Text content
await expect(page.getByText("User created successfully")).toBeVisible();

// ❌ AVOID: Placeholder-based selectors (fragile)
await page.fill('input[placeholder="Your password"]', "password");

// ❌ AVOID: getByLabel for PasswordInput (may match multiple)
await page.getByLabel("Password").fill("password");
```

<!-- buildpad-backend: supabase -->
## Load Testing (k6)

For performance testing, generate k6 test scripts:

```bash
# Install k6
brew install k6  # macOS

# Setup test environment
pnpm load:setup  # Creates users, generates tokens

# Run tests
pnpm load:smoke    # Quick test (1 min, 1 VU)
pnpm load:test     # Standard load test (16 min, 10-20 VUs)
pnpm load:stress   # Stress test (23 min, 20-60 VUs)
pnpm load:spike    # Spike test (5 min, 5-100 VUs)
```

**Key metrics to validate:**

- `http_req_duration p(95)` < threshold (500ms smoke, 800ms load)
- `errors` rate < threshold (10% smoke, 5% load)
- `checks` pass rate > 95%
- Custom metrics: `get_items_duration`, `create_item_duration`, etc.

**Request distribution:** 50% GET list, 25% GET single, 15% POST create, 10% PATCH update.

## Coverage Checklist

**API Routes:** GET all (200), GET single (200/404), POST valid (201), POST invalid (400), PATCH (200/404), DELETE (200/404), query params (fields, filter, search, sort, pagination, meta)

**Security/RLS:** 401 unauthenticated, 403 unauthorized, admin bypass, self-access, data isolation, SQL injection protection

**Field Permissions:** Admin full access, limited field read, forbidden field write (403), wildcard permissions, field merging (OR logic)
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Load Testing (k6)

For performance testing, generate k6 test scripts. On an Engine project a k6 script sends a test user's access token as `Authorization: Bearer <access token>` to `<Engine_URL>/api/items/<collection>`; never the token in the project's MCP configuration.

```bash
# Install k6
brew install k6  # macOS

# Setup test environment
pnpm load:setup  # Signs the test users in, saves tokens (creates only missing users)

# Run tests
pnpm load:smoke    # Quick test (1 min, 1 VU)
pnpm load:test     # Standard load test (16 min, 10-20 VUs)
pnpm load:stress   # Stress test (23 min, 20-60 VUs)
pnpm load:spike    # Spike test (5 min, 5-100 VUs)
```

**Rate budget:** the Engine serves 20 requests per second per client address unless its operator set `RATE_LIMIT_RPS`, and answers `429` (`REQUESTS_EXCEEDED`) beyond it. A k6 run from one machine is one client address. Run the smoke test against any Engine; run the load, stress and spike tests only against an Engine whose operator raised the limit for the test, or they measure the limiter. Count `429` answers apart from other errors. Access tokens expire after one hour by default: re-run `pnpm load:setup` when requests fail with `401`.

**Key metrics to validate:**

- `http_req_duration p(95)` < threshold (500ms smoke, 800ms load)
- `errors` rate < threshold (10% smoke, 5% load)
- `checks` pass rate > 95%
- Custom metrics: `get_items_duration`, `create_item_duration`, etc.

**Request distribution:** 50% GET list, 25% GET single, 15% POST create (answered `200`), 10% PATCH update.

## Coverage Checklist

**API Routes:** GET all (200), GET single (200/404), POST valid (200 on `/api/items`; 201 on `/api/users`, `/api/roles`, `/api/policies`, `/api/permissions`), POST invalid (400), PATCH (200/404), DELETE (204, no body), query params (fields, filter, search, sort, pagination, meta)

**Access:** 401 unauthenticated, 403 unauthorized, admin bypass, self-access, row filters, field lists, scope separation (403 `FORBIDDEN_SCOPE` for a scope outside the tenant), SQL injection protection

**Field Permissions:** Admin full access, limited field read, forbidden field write (403), wildcard permissions, field merging (the union of the matching rules' fields)
<!-- /buildpad-backend -->

**Permissions UI:** Admin sees all actions, read-only hides create/delete, no-permission redirects, navigation links conditional, action buttons gated

**Pages:** Load correctly, title visible, data displays, navigation works, empty state, search/filter

**Components:** Renders, modal open/close, form validation, form submission, loading/error states, form change detection (dirty indicator, modified badge, revert)

**E2E Flows:** Complete CRUD journey, auth flow, admin vs non-admin access, workflow transitions

**Load (optional):** Smoke test passes, standard load meets p95 thresholds, error rate acceptable

## Debugging Tests

```bash
pnpm test:debug                          # Playwright Inspector
pnpm test tests/[file].spec.ts --debug   # Debug specific test
pnpm test:ui                             # Interactive UI mode
pnpm test:headed                         # See browser
```

**Screenshots:** Auto-captured on failure (`screenshot: 'only-on-failure'` in config).  
**Videos:** `video: 'retain-on-failure'` saves to `test-results/`.  
**Console/Network logs:**

```typescript
page.on("console", (msg) => console.log("Browser:", msg.text()));
page.on("request", (req) => console.log("Request:", req.url()));
```

## Test Commands

<!-- buildpad-backend: supabase -->
```bash
pnpm test                              # All Playwright tests
pnpm test tests/[type]/[name].spec.ts  # Specific test
pnpm test -g "pattern"                 # Tests matching pattern
pnpm test tests/api/rls-*.spec.ts      # All RLS tests
pnpm test:ui                           # UI mode
pnpm test:unit                         # Vitest unit tests
pnpm test:headed                       # Headed browser
pnpm test --project=chromium           # Specific browser
pnpm load:smoke                        # k6 smoke test
pnpm load:test                         # k6 standard load test
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```bash
pnpm test                              # All Playwright tests
pnpm test tests/[type]/[name].spec.ts  # Specific test
pnpm test -g "pattern"                 # Tests matching pattern
pnpm test tests/api/access-*.spec.ts   # All access tests
pnpm test:ui                           # UI mode
pnpm test:unit                         # Vitest unit tests
pnpm test:headed                       # Headed browser
pnpm test --project=chromium           # Specific browser
pnpm load:smoke                        # k6 smoke test
pnpm load:test                         # k6 standard load test
```
<!-- /buildpad-backend -->

## CI/CD Integration

<!-- buildpad-backend: supabase -->
```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 24
      - run: pnpm install
      - run: pnpm exec playwright install --with-deps
      - run: pnpm test
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
          SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 24
      - run: pnpm install
      - run: pnpm exec playwright install --with-deps
      - run: pnpm tsx tests/setup-test-users.ts
        env:
          NEXT_PUBLIC_BUILDPAD_DAAS_URL: ${{ vars.ENGINE_URL }}
          NEXT_PUBLIC_BUILDPAD_TENANT_ID: ${{ vars.BUILDPAD_TENANT_ID }}
          TEST_ADMIN_EMAIL: ${{ secrets.TEST_ADMIN_EMAIL }}
          TEST_ADMIN_PASSWORD: ${{ secrets.TEST_ADMIN_PASSWORD }}
      - run: pnpm test
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ vars.ENGINE_URL }}
          NEXT_PUBLIC_BUILDPAD_DAAS_URL: ${{ vars.ENGINE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: buildpad-engine-public-anon-key
          NEXT_PUBLIC_BUILDPAD_TENANT_ID: ${{ vars.BUILDPAD_TENANT_ID }}
          TEST_ADMIN_EMAIL: ${{ secrets.TEST_ADMIN_EMAIL }}
          TEST_ADMIN_PASSWORD: ${{ secrets.TEST_ADMIN_PASSWORD }}
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

The Engine_URL and the tenant id are not secrets: keep them as repository variables. The test administrator's email and password are the only secrets the pipeline needs.
<!-- /buildpad-backend -->

## References

- [Playwright testing guide](references/playwright-testing.instructions.md)
