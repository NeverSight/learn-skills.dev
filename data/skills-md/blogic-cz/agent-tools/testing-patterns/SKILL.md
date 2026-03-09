---
name: testing-patterns
description: "LOAD THIS SKILL when: writing unit tests, TRPC integration tests, or E2E tests. Covers Vitest patterns, Effect service testing, PGlite database testing, and Playwright E2E."
compatibility: opencode
---

# Testing Patterns

## Test Hierarchy (ALWAYS prefer simpler)

1. **Unit tests** (preferred) - Pure functions, parsers, Effect services
2. **TRPC Integration** (ask first) - Full TRPC stack with PGlite
3. **E2E** (ask + justify) - Browser automation, slowest

## When to Use Each

| Situation                        | Test Type             | Action                       |
| -------------------------------- | --------------------- | ---------------------------- |
| Pure function, parser, util      | Unit                  | Write immediately            |
| Effect service with dependencies | Unit with mock layers | Write immediately            |
| TRPC procedure (DB logic)        | TRPC Integration      | Ask user first               |
| User-facing flow, UI behavior    | E2E                   | Ask + warn about maintenance |

## Test File Locations

| Code Location                                       | Test Location                           |
| --------------------------------------------------- | --------------------------------------- |
| `packages/X/src/file.ts`                            | `packages/X/src/__tests__/file.test.ts` |
| `apps/web-app/src/infrastructure/trpc/routers/X.ts` | `apps/web-app/src/__tests__/X.test.ts`  |
| `apps/web-app/src/routes/**`                        | `apps/web-app/e2e/feature.e2e.ts`       |

---

## Unit Test Patterns

### Basic Vitest

```typescript
import { describe, expect, it } from "vitest";

describe("parseResourceSize", () => {
  it("parses Ki units", () => {
    expect(parseResourceSize("512Ki")).toBe(524288);
  });
});
```

### Effect with @effect/vitest

```typescript
import { describe, expect, it } from "@effect/vitest";
import { Effect, Either, Layer } from "effect";

describe("K8sMetricsService", () => {
  // Mock layer factory
  const createMockLayer = (responses: Map<string, unknown>) =>
    Layer.succeed(K8sHttpClient, {
      request: (params) => Effect.succeed(responses.get(params.path)),
    });

  const testLayer = K8sMetricsService.layer.pipe(
    Layer.provide(createMockLayer(mockResponses))
  );

  it.effect("collects metrics", () =>
    Effect.gen(function* () {
      const service = yield* K8sMetricsService;
      const result = yield* service.collectMetrics({ ... });
      expect(result.namespaces).toHaveLength(3);
    }).pipe(Effect.provide(testLayer))
  );

  // Error handling with Either.match
  it.effect("handles error case", () =>
    Effect.gen(function* () {
      const result = yield* myEffect.pipe(Effect.either);
      Either.match(result, {
        onLeft: (error) => {
          expect(error._tag).toBe("K8sConnectionError");
        },
        onRight: () => {
          expect.fail("Expected Left but got Right");
        },
      });
    }).pipe(Effect.provide(testLayer))
  );
});
```

### Live Effect tests (real dependencies)

```typescript
it.live("returns success when endpoint is ready", () => {
  globalThis.fetch = vi.fn().mockResolvedValue(new Response("ok", { status: 200 }));

  return Effect.gen(function* () {
    const svc = yield* HealthCheckService;
    const result = yield* svc.checkApiHealth("http://api", {
      maxRetries: 1,
    });
    expect(result.success).toBe(true);
  }).pipe(Effect.provide(HealthCheckServiceLive));
});
```

---

## TRPC Integration Test Patterns

**Ask user before writing:** "Does an integration test make sense for this TRPC endpoint?"

### Setup

```typescript
import { describe, expect, it, beforeEach, afterEach } from "vitest";
import type { PGlite } from "@electric-sql/pglite";
import {
  createTestDb,
  cleanupTestDb,
  type TestDb,
  seedUser,
  seedOrganization,
  seedMember,
  seedProject,
} from "@project/db/testing";
import { createTestCaller } from "./trpc-test-utils";

describe("agents.listRuns", () => {
  let db: TestDb;
  let client: PGlite | undefined;

  beforeEach(async () => {
    const testDb = await createTestDb();
    db = testDb.db;
    client = testDb.client;
  });

  afterEach(async () => {
    await cleanupTestDb(client);
    client = undefined;
  });

  it("returns correct results", async () => {
    // Seed data
    const user = await seedUser(db);
    const org = await seedOrganization(db);
    await seedMember(db, {
      userId: user.id,
      organizationId: org.id,
    });
    const project = await seedProject(db, {
      organizationId: org.id,
    });

    // Create caller with auth context
    const caller = createTestCaller({
      db,
      userId: user.id,
    });

    // Call TRPC procedure
    const result = await caller.agents.listRuns({
      projectId: project.id,
      page: 1,
      pageSize: 10,
    });

    expect(result.runs).toHaveLength(0);
    expect(result.total).toBe(0);
  });
});
```

### Available seed helpers

```typescript
import {
  seedUser,
  seedOrganization,
  seedMember,
  seedProject,
  seedAgentTemplate,
  seedAgentInstance,
  seedAgentRun,
  seedGitHubIssue,
  seedCompleteScenario, // Creates full user -> org -> project -> agent -> run chain
} from "@project/db/testing";
```

---

## E2E Test Patterns

**Ask user + warn:** "E2E tests are the most expensive to maintain. Is this really needed for this feature?"

### Basic E2E

```typescript
import { expect, test } from "@playwright/test";
import { e2eEnv } from "./env";
import { ensureTestUserExists, signInWithEmail } from "./auth-helpers";

const testEmail = e2eEnv.E2E_TEST_EMAIL;
const testPassword = e2eEnv.E2E_TEST_PASSWORD;

test("auth: can sign in with email", async ({ page }) => {
  await ensureTestUserExists(page.request, {
    email: testEmail,
    password: testPassword,
    name: "E2E Test User",
  });

  await signInWithEmail(page, {
    email: testEmail,
    password: testPassword,
  });

  await expect(
    page.getByRole("heading", {
      name: "Dashboard",
      exact: true,
    }),
  ).toBeVisible({ timeout: 5_000 });
});
```

### Auth helpers

```typescript
import { signInWithEmail, ensureTestUserExists } from "./auth-helpers";
import { waitForHydration } from "./wait-for-hydration";

// Before interacting with forms
await waitForHydration(page);
```

### Test credentials

```typescript
// From e2eEnv
const testEmail = e2eEnv.E2E_TEST_EMAIL; // test@example.com
const testPassword = e2eEnv.E2E_TEST_PASSWORD; // TestPass123
```

---

## Commands

```bash
bun run test              # Run all unit + TRPC integration tests
bun run test:watch        # Watch mode
bun run test:coverage     # With coverage
bun run test:e2e          # Run E2E tests
bun run test:e2e:ui       # E2E with UI

# Run specific test file (FROM PROJECT ROOT, full path required)
bun run vitest run packages/common/src/__tests__/pagination.test.ts
bun run vitest run apps/web-app/src/__tests__/formatters.test.ts
```

**WRONG syntax (DO NOT USE):**

```bash
# These DO NOT work:
bun run test packages/common/src/__tests__/file.test.ts  # script doesn't accept path
cd packages/common && bun run vitest run src/__tests__/file.test.ts  # wrong cwd
```

---

## Decision Process

Before writing ANY test:

1. **Can this be unit tested?** -> Write unit test immediately
2. **Need DB behavior (joins, constraints)?** -> Ask: "Does an integration test make sense here?"
3. **Need browser/UI?** -> Ask + warn: "E2E tests are expensive to maintain. Is this necessary?"

**Never** write integration or E2E tests without user confirmation.
