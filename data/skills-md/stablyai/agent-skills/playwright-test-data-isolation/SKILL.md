---
name: playwright-test-data-isolation
description: |
  Playwright-first strategy for shared DB + shared test accounts. Use when E2E
  tests collide in QA/staging, need safe parallelism, or require deterministic
  cleanup without touching baseline data. Covers per-test ownership,
  namespacing, ID-based teardown, serial shared-state suites, and optional
  stale-data janitor jobs.
---

# Playwright Test Data Isolation

Use this skill when teams run Playwright tests in a shared QA/staging environment with:

- A shared database (often production-connected)
- Shared test user accounts
- Parallel CI and local test runs
- Flaky tests caused by data collisions, cross-test interference, or unsafe cleanup

Goal: make tests parallel-safe and operationally safe while staying standard Playwright.

## When To Use This Skill

Use this skill for tasks like:

- "Our Playwright tests share a database and keep colliding"
- "How do we run E2E safely with shared accounts?"
- "How should we isolate test data in CI?"
- "How do we clean up test data without deleting real data?"
- "How do we keep parallel Playwright runs stable?"
- "How do we design fixtures for safe create-and-cleanup?"

## Core Contract (Non-Negotiable)

Every test must follow this contract:

1. Create the entities it needs (test-owned data).
2. Mutate only entities it created.
3. Treat shared baselines (accounts, workspaces, org settings) as read-only.
4. Clean up by exact IDs captured during the test (never broad filters).

If a test cannot follow this contract, move it to a serial suite.

## Non-Negotiable Guardrails

- Treat shared users and shared workspaces as read-only containers.
- Never update shared workspace settings, membership, billing, or global toggles in parallel suites.
- Prefix test-created records with a unique namespace (`e2e-<run>-<worker>-<uuid>`).
- Delete by exact IDs; never run broad delete filters in test teardown.
- Keep a scheduled stale-data janitor as backup, not as the primary cleanup mechanism.

## Recommended Architecture

Use shared accounts for authentication only, then isolate all mutable data by namespace.

- Shared accounts: identity only
- Test data: fully owned by one test via namespace
- Cleanup: deterministic, ID-based, reverse order
- Shared-state mutation suites: serialized
- Scheduled cleanup: removes stale `e2e-*` artifacts older than a threshold

## Account Strategy

Pick the highest isolation level your environment can support:

1. Best: one account per worker (pool accounts and map by `workerIndex`).
2. Acceptable: shared account for sign-in only, test-owned child data for all writes.
3. Avoid: many tests mutating top-level account/workspace settings in parallel.

## Implementation Pattern (Playwright-Native)

### 1) Reuse auth state for shared accounts (setup project)

```ts
// auth/setup-auth.ts
import { test as setup } from "@playwright/test";

setup("login as shared qa account", async ({ page }) => {
  await page.goto(process.env.BASE_URL!);
  await page.getByLabel("Email").fill(process.env.E2E_USER_EMAIL!);
  await page.getByLabel("Password").fill(process.env.E2E_USER_PASSWORD!);
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.context().storageState({ path: "playwright/.auth/qa-user.json" });
});
```

Wire this into a `setup` project dependency in `playwright.config.ts` so parallel projects reuse a stable signed-in state.

### 2) Add namespace + cleanup tracker fixtures

```ts
// tests/fixtures/test-data.ts
import { test as base } from "@playwright/test";
import { randomUUID } from "crypto";

type CleanupFn = () => Promise<void>;

type IsolationFixtures = {
  namespace: string;
  trackCleanup: (fn: CleanupFn) => void;
};

export const test = base.extend<IsolationFixtures>({
  namespace: async ({}, use, testInfo) => {
    const runId = process.env.CI_RUN_ID ?? process.env.GITHUB_RUN_ID ?? "local";
    const ns = [
      "e2e",
      runId,
      testInfo.project.name,
      String(testInfo.workerIndex),
      randomUUID(),
    ].join("-");
    await use(ns);
  },

  trackCleanup: async ({}, use) => {
    const fns: CleanupFn[] = [];
    await use((fn: CleanupFn) => fns.push(fn));

    for (const fn of fns.reverse()) {
      try {
        await fn();
      } catch (err) {
        console.error("cleanup failed", err);
      }
    }
  },
});

export { expect } from "@playwright/test";
```

Notes:

- `runId + project + worker + uuid` keeps names unique across CI, shards, and local runs.
- Reverse-order cleanup (LIFO) avoids dependency-order teardown bugs.

### 3) Create child resources in shared containers only

```ts
// tests/e2e/projects.spec.ts
import { test, expect } from "../fixtures/test-data";

test.use({ storageState: "playwright/.auth/qa-user.json" });

test("creates isolated project safely", async ({ page, request, namespace, trackCleanup }) => {
  const workspaceId = process.env.E2E_SHARED_WORKSPACE_ID!; // read-only container
  const projectName = `e2e-${namespace}`;

  await page.goto(`/workspaces/${workspaceId}/projects`);
  await page.getByRole("button", { name: "New project" }).click();
  await page.getByLabel("Project name").fill(projectName);
  await page.getByRole("button", { name: "Create" }).click();

  const projectId = await getProjectIdByName(request, workspaceId, projectName);
  trackCleanup(async () => {
    await deleteProjectById(request, workspaceId, projectId);
  });

  await expect(page.getByText(projectName)).toBeVisible();
});

async function getProjectIdByName(
  request: import("@playwright/test").APIRequestContext,
  workspaceId: string,
  name: string,
) {
  const res = await request.get(
    `/api/internal/workspaces/${workspaceId}/projects?name=${encodeURIComponent(name)}`,
  );
  if (!res.ok()) throw new Error(`project lookup failed: ${res.status()}`);
  const body = await res.json();
  return body.items[0].id as string;
}

async function deleteProjectById(
  request: import("@playwright/test").APIRequestContext,
  workspaceId: string,
  id: string,
) {
  const res = await request.delete(`/api/internal/workspaces/${workspaceId}/projects/${id}`);
  if (!res.ok()) throw new Error(`project delete failed: ${res.status()}`);
}
```

### 4) Isolate true shared-state tests in serial suites

```ts
import { test } from "@playwright/test";

test.describe.configure({ mode: "serial" });
```

Only use this for tests that must mutate global/shared settings. Keep most tests fully parallel by using test-owned child resources.

### 5) Add a stale-data janitor project (backup safety net)

```ts
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  projects: [
    {
      name: "e2e",
      testDir: "tests/e2e",
      use: { storageState: "playwright/.auth/qa-user.json" },
    },
    {
      name: "cleanup",
      testDir: "tests/cleanup",
      workers: 1,
      retries: 0,
    },
  ],
});
```

```ts
// tests/cleanup/stale-e2e-data.spec.ts
import { test, expect } from "@playwright/test";

test("delete stale e2e data older than 24h", async ({ request }) => {
  const res = await request.post("/api/internal/cleanup/e2e", {
    data: {
      prefix: "e2e-",
      olderThanHours: 24,
    },
  });

  expect(res.ok()).toBeTruthy();
});
```

Run janitor on a schedule (nightly or multiple times/day), but keep per-test cleanup as the primary defense.

## Collision Debugging Checklist

When a test collides, collect these first:

- Namespace used by each failing test
- Worker index and project name
- IDs created by each test before cleanup
- Which shared entity was mutated (if any)

If retries make failures disappear, treat that as a signal of shared-state coupling, not success.

## Optional: If Team Uses Stably

Stably can help with orchestration and operations, but this strategy does not depend on it.

- Use `npx stably test` as a Playwright-compatible runner wrapper when you want hosted reporting/ops.
- Use Stably environments to inject shared account credentials by environment.
- Use Stably schedules/cloud workers for janitor jobs and large parallel runs.
- Keep the same isolation contract regardless of runner.

## Anti-Patterns To Block

- Parallel tests writing to the same shared entity
- Shared mutable fixtures reused across files
- Cleanup using broad filters like "delete all e2e rows"
- Relying on execution order
- Using retries to mask shared-data collisions
- Treating nightly cleanup as the only cleanup

## Agent Output Requirements

When this skill is activated, the agent should:

1. Confirm environment constraints (shared DB, shared accounts, parallelism level).
2. Produce or update a namespace fixture and deterministic cleanup tracker.
3. Classify tests into parallel-safe vs shared-state-mutation suites.
4. Refactor at least one target test to create-and-own data.
5. Add or propose a stale-data cleanup project and schedule.
6. Return a short risk report listing remaining unsafe tests.

## Rollout Plan

1. Add namespace + cleanup fixtures.
2. Migrate flaky mutable tests to create-and-own data.
3. Add cleanup project and schedule.
4. Move shared-state mutation tests to serial mode.
5. Increase workers only after collision-free runs.

## Success Criteria

- Parallel runs no longer collide on shared data.
- Teardown never touches non-test data.
- Flake rate drops for data-dependent tests.
- Shared environment remains stable for manual QA and CI.
