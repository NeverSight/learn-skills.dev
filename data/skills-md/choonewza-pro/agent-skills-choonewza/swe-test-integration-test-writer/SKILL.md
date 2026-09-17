---
name: swe-test-integration-test-writer
description: >
  Guides AI agents to write high-quality TypeScript integration tests using
  Jest or Vitest with real databases (Prisma, Drizzle, TypeORM), HTTP endpoints
  (Supertest, Fastify, Next.js App Router, NestJS), Testcontainers, and MSW for
  external services. Covers sociable testing, database lifecycles (truncate vs
  rollback), worker concurrency, factory fixtures, and teardown hygiene. Use
  when asked to "write integration tests", "เขียน integration test", "เทสต์ API กับ
  DB", "สร้าง integration test", or to produce .integration.test.ts files.
license: Apache-2.0
allowed-tools: ReadFile, ListDirectory, RunCommand, WriteFile
metadata:
  author: choonewza
  version: "0.1"
---

## Overview

You are an integration test writer for **TypeScript** projects using **Jest** or **Vitest**.

> **Integration Testing Mindset (Sociable Testing):**
> Integration Test ไม่ใช่การจำลองทุกอย่างผ่าน Mock แต่คือการ **พิสูจน์ว่าชิ้นส่วนต่างๆ ทำงานร่วมกันได้จริงในสถานการณ์เสมือนจริง (Real Collaboration)**
> เป้าหมายหลักคือ:
>
> 1. **High Confidence Through Real I/O:** ทดสอบทะลุผ่าน Router/Controller → Service → Repository → Real Database
> 2. **Unmocked Internal Components:** ห้าม Mock โค้ดหรือ Service ภายในระบบตัวเอง (Mock เฉพาะ Third-party นอกองค์กร เช่น Stripe, SMS)
> 3. **Pristine State & Clean Lifecycle:** จัดการ Database State ให้สะอาด ไม่ปนเปื้อน (No Test Pollution) และปิด Connection เสมอ (No CI Hang)
> 4. **Deterministic & Concurrency-Safe:** ทำงานได้อย่างมั่นคง ไม่ Flaky ไม่พึ่งพา `sleep()` และปลอดภัยเมื่อรันแบบ Multi-worker

Your job is to produce `.integration.test.ts` / `.int.spec.ts` files that are:

- **Sociable** — runs real code across multiple architectural layers
- **Isolated** — resets DB state between tests so no test affects another
- **Resilient** — asserts on real database changes and API contracts, not internal methods
- **Leak-Free** — cleanly releases connection pools, HTTP listeners, and containers in `afterAll`
- **Safe** — strictly validates that tests never execute against production/staging databases

**Scope:** Integration tests (API-to-Database, Service-to-Database/Cache, Worker/Queue).
- For pure isolated unit tests, use `swe-test-unit-test-writer`.
- For test case design (BVA / EP tables), reference `swe-test-engineer`.
- For risk prioritization, reference `swe-test-planner`.

For detailed references, see:

- [references/integration-patterns.md](references/integration-patterns.md) — sociable testing, layer flow, async polling (`waitFor`), testing trophy
- [references/database-lifecycle.md](references/database-lifecycle.md) — migrations, truncate vs rollback, worker isolation, safety guards
- [references/testcontainers-and-docker.md](references/testcontainers-and-docker.md) — real Postgres, MySQL, Redis via Testcontainers & Docker Compose
- [references/api-and-http-testing.md](references/api-and-http-testing.md) — Supertest, Fastify inject, Next.js App Router, auth & sessions
- [references/external-mocking.md](references/external-mocking.md) — network-level boundary mocking with MSW / WireMock
- [references/fixtures-and-factories.md](references/fixtures-and-factories.md) — deterministic factory pattern, avoiding hardcoded IDs
- [references/naming-conventions.md](references/naming-conventions.md) — file naming, Given-When-Then, HTTP endpoint diagnostics
- [references/anti-patterns.md](references/anti-patterns.md) — 12 critical integration test anti-patterns to avoid
- [references/project-file-structure.md](references/project-file-structure.md) — test organization, vitest/jest configs, npm scripts, CI pipelines
- [references/examples.md](references/examples.md) — complete worked examples (Express + Prisma + Postgres, Next.js + Drizzle)

---

## When to Activate

Activate when the user:

- Asks to write integration tests for an API, route handler, service, or database repository
- Says "เขียน integration test", "เขียน test ต่อ database", "test api", "write integration tests"
- Needs to verify an end-to-end flow between controllers, services, and real databases
- Mentions Supertest, Testcontainers, Database Migration in tests, or MSW
- Asks to debug flaky integration tests, database state pollution, or unclosed open handles in CI

Do NOT activate when:

- The user wants pure unit tests without database or network I/O → use `swe-test-unit-test-writer`
- The user wants frontend browser UI automation (Cypress/Playwright E2E)
- The user wants test case design analysis (BVA/EP tables) → use `swe-test-engineer`
- The user wants test prioritization → use `swe-test-planner`

---

## Anti-Patterns

Before writing any integration test, internalize these rules. See [references/anti-patterns.md](references/anti-patterns.md) for details.

- ❌ **Do not mock internal services or database repositories** — if you mock the repository, you wrote a slow fake unit test, not an integration test.
- ❌ **Do not use `sleep()` or `setTimeout()` to wait for async events** — use deterministic polling utilities (`waitFor()`).
- ❌ **Do not leave open database pools or HTTP servers** — always close pools, clients, and servers in `afterAll`.
- ❌ **Do not share mutable DB records between tests** — each test must seed its own data and clean up.
- ❌ **Do not hardcode auto-increment or fixed IDs** — use deterministic Factory functions with dynamic UUIDs or sequences.
- ❌ **Do not run tests against staging/production databases** — include an environment safety guard that halts if `NODE_ENV !== 'test'`.
- ❌ **Do not test 20 math branch permutations in integration tests** — test branch math in fast unit tests (Testing Trophy).
- ❌ **Do not ignore worker collisions in parallel test runners** — use single-thread mode or schema-per-worker.

---

## Instructions

### Step 1: Detect Test Framework, DB & HTTP Stack

Inspect the project to identify the active technologies:

1. **Test Runner:**
   - Vitest: `vitest.config.ts` / `package.json` contains `vitest`
   - Jest: `jest.config.ts` / `package.json` contains `jest`
2. **Database & ORM:**
   - Prisma (`prisma/schema.prisma`), Drizzle (`drizzle.config.ts`), TypeORM (`ormconfig.*`), Mongoose (`mongoose`)
3. **HTTP / Web Framework:**
   - Express (`express`), Fastify (`fastify`), NestJS (`@nestjs/core`), Next.js App Router (`app/api/**/route.ts`)
4. **Database Infrastructure:**
   - Testcontainers (`@testcontainers/postgresql`), Docker Compose (`docker-compose.test.yml`), or local test DB URL in `.env.test`

---

### Step 2: Define Integration Boundaries & Testing Trophy Scope

Before writing tests, determine the exact boundary:

1. **What is INSIDE the boundary (Run Real):**
   - Real HTTP route handlers / controllers
   - Real middleware (Authentication, validation, error handlers)
   - Real business services and domain logic
   - Real ORM / query builders and Real Database (Postgres, MySQL, Redis, MongoDB)
2. **What is OUTSIDE the boundary (Mock at Network Level via MSW):**
   - External Payment Gateways (Stripe, Omise)
   - External Communication (Twilio, SendGrid, LINE Notify)
   - Third-party SaaS Webhooks and REST APIs
3. **Scope Discipline (Testing Trophy):**
   - Focus integration tests on **Critical User Journeys, Database Transactions, and HTTP Contracts**.
   - Leave edge-case arithmetic and string formatting permutations to unit tests.

---

### Step 3: Manage Database Lifecycle & Worker Isolation

Ensure tests are completely isolated and clean up after themselves.
See [references/database-lifecycle.md](references/database-lifecycle.md).

1. **Safety Guard Check:**
   ```typescript
   if (process.env.NODE_ENV !== 'test' || process.env.DATABASE_URL?.includes('prod')) {
     throw new Error('SAFETY VIOLATION: Integration tests cannot run against non-test databases!')
   }
   ```
2. **Choose Cleanup Strategy:**
   - **Strategy A (Table Truncate):** Clean tables in `beforeEach` or `afterEach` (`TRUNCATE TABLE users CASCADE;`). Best for tests that commit real transactions.
   - **Strategy B (Transaction Rollback):** Wrap each test in a database transaction and execute `ROLLBACK` at the end. Extremely fast, best for read-heavy suites.
3. **Concurrency Protection:**
   - Configure integration test scripts with `--no-threads` (Vitest) or `--runInBand` (Jest), or assign a dedicated schema per worker (`search_path = test_worker_1`).
4. **Teardown Hygiene in `afterAll`:**
   - Always disconnect ORM (`await prisma.$disconnect()`, `await pool.end()`).
   - Stop test container (`await container.stop()`) or close HTTP server (`server.close()`).

---

### Step 4: Prepare Fixtures & Seed Data via Factories

Never insert raw hardcoded rows with fixed IDs directly into test blocks.
See [references/fixtures-and-factories.md](references/fixtures-and-factories.md).

- Use **Factory Functions** with sensible defaults and override capabilities:
  ```typescript
  export async function createTestUser(overrides: Partial<User> = {}) {
    return prisma.user.create({
      data: {
        email: `user-${Date.now()}-${Math.random().toString(36).slice(2, 7)}@example.com`,
        name: 'Test User',
        role: 'MEMBER',
        ...overrides,
      },
    })
  }
  ```
- Ensure foreign-key parent records are created first.

---

### Step 5: Write Integration Tests (Arrange–Act–Assert for Sociable Tests)

Structure integration tests clearly with Given-When-Then or Arrange-Act-Assert.
See [references/api-and-http-testing.md](references/api-and-http-testing.md).

```typescript
// 1. Imports
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest'
import request from 'supertest'
import { app } from '../src/app'
import { prisma } from '../src/lib/prisma'
import { createTestUser } from './factories/user.factory'
import { cleanDatabase } from './helpers/clean-db'

describe('POST /api/v1/orders (Checkout Flow)', () => {
  // 2. Lifecycle setup & teardown
  beforeEach(async () => {
    await cleanDatabase()
  })

  afterAll(async () => {
    await prisma.$disconnect()
  })

  it('creates order in database and returns 201 when payload is valid', async () => {
    // Arrange — Seed database state with real factories
    const user = await createTestUser({ role: 'MEMBER' })
    const payload = { items: [{ productId: 'prod-1', quantity: 2 }] }

    // Act — Real HTTP call dispatched through middleware & routers
    const response = await request(app)
      .post('/api/v1/orders')
      .set('Authorization', `Bearer ${user.authToken}`)
      .send(payload)

    // Assert 1 — HTTP Contract
    expect(response.status).toBe(201)
    expect(response.body).toMatchObject({
      orderId: expect.any(String),
      status: 'CONFIRMED',
    })

    // Assert 2 — Real Database Verification (Critical for Integration Tests!)
    const savedOrder = await prisma.order.findUnique({
      where: { id: response.body.orderId },
      include: { items: true },
    })
    expect(savedOrder).not.toBeNull()
    expect(savedOrder?.userId).toBe(user.id)
    expect(savedOrder?.items).toHaveLength(1)
  })
})
```

#### Key Rules When Writing:
1. **Always verify database side effects:** Don't stop at checking the HTTP response; query the real database to ensure data was persisted correctly.
2. **Never use `sleep()` for async queues:** When waiting for background jobs, use `await waitFor(async () => expect(...))`.
3. **Use `.toMatchObject()` for responses:** Don't compare raw timestamps or auto-generated IDs with `.toEqual()`.
4. **Mock external APIs at network level:** Use MSW handlers (`http.post('https://api.stripe.com/...', () => ...)`).

---

### Step 6: Validate Quality & Teardown Hygiene

Before completing your integration test suite, run through this checklist:

**Sociable & Quality Check:**
- [ ] No internal service, repository, or database client is mocked with `vi.mock()` or `jest.mock()`
- [ ] Tests verify both HTTP response AND persistent Database state
- [ ] External 3rd-party APIs are intercepted at the network level via MSW or WireMock
- [ ] No `sleep()` or `setTimeout()` calls are used for async operations (uses `waitFor()` polling)
- [ ] Factory functions are used for data seeding (no hardcoded IDs)

**Safety & Lifecycle Check:**
- [ ] Safety guard prevents running against non-test or production databases
- [ ] Database is cleaned up between tests (via truncate or transaction rollback)
- [ ] All database pools, client connections, and server sockets are closed in `afterAll`
- [ ] Concurrency collisions are prevented via `--no-threads` / `--runInBand` or worker schemas
- [ ] CI runner exits cleanly without hanging open handles (`--detectOpenHandles`)

---

### Step 7: Run Integration Suite Safely

Run integration tests using dedicated configuration or npm scripts:

```bash
# Vitest
npx vitest run --config vitest.config.integration.ts

# Vitest single file (safe concurrency)
npx vitest run path/to/order.integration.test.ts --no-threads

# Jest (with open handles detection)
npx jest path/to/order.integration.test.ts --runInBand --detectOpenHandles --forceExit=false
```

Verify that all tests pass AND the test runner process terminates immediately without hanging.

---

## Relationship to Other Testing Skills

```
swe-test-planner                → "ควร test อะไรก่อน?"                  (Risk-based prioritization)
swe-test-engineer               → "กำหนดค่า test data & case อย่างไร?" (BVA/EP/STT → test data & values)
swe-test-unit-test-writer       → "เขียน isolated unit test อย่างไร?"   (Fast, pure functions, solitary)
swe-test-integration-test-writer → "เขียน sociable integration test ยังไง?"(Real API + Real DB + MSW) ← YOU ARE HERE
```

---

## Examples & References

- [references/integration-patterns.md](references/integration-patterns.md) — Architectural patterns, async polling, testing trophy
- [references/database-lifecycle.md](references/database-lifecycle.md) — DB setup, truncation, transactions, concurrency
- [references/testcontainers-and-docker.md](references/testcontainers-and-docker.md) — Testcontainers setup
- [references/api-and-http-testing.md](references/api-and-http-testing.md) — Supertest & Next.js route testing
- [references/external-mocking.md](references/external-mocking.md) — MSW configuration
- [references/fixtures-and-factories.md](references/fixtures-and-factories.md) — Factory pattern
- [references/naming-conventions.md](references/naming-conventions.md) — Naming and file standards
- [references/anti-patterns.md](references/anti-patterns.md) — Comprehensive anti-patterns list
- [references/project-file-structure.md](references/project-file-structure.md) — Directory layout & CI scripts
- [references/examples.md](references/examples.md) — Complete runnable examples

**Trigger phrases:**

- "เขียน integration test สำหรับ API นี้"
- "สร้าง test ทดสอบ flow ระหว่าง controller กับ database"
- "เขียน integration test ด้วย Vitest และ Prisma"
- "test Next.js App Router API กับ database จริง"
- "write integration tests for our Express / NestJS backend"
- "แก้ปัญหา integration test ค้างใน CI หรือแก้ flaky test"
