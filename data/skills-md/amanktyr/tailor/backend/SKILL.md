---
name: backend
description: Governs backend architecture, API endpoints, REST, GraphQL, database schemas, SQL, ORM, Prisma, Drizzle, migrations, transactions, concurrency, idempotency, and error handling standards.
---

# Backend Engineering Skill

Activate this skill when creating or updating API endpoints, database models, background jobs, caching layers, or backend services.

> **Operational Directive:** *Design resilient, validated, concurrent-safe, and performant backend services with strict data integrity.*

---

## 1. API Contract Design & HTTP Standards

Check `.ai/API.md` for project-specific conventions (REST, GraphQL, tRPC). Adhere to standard HTTP semantics:

### Status Code Standards
* `200 OK`: Successful retrieval or synchronous update.
* `201 Created`: Resource successfully created (include `Location` header or created object).
* `204 No Content`: Successful mutation with no response body (e.g. deletion).
* `400 Bad Request`: Malformed syntax, invalid JSON, or failed input schema validation.
* `401 Unauthorized`: Missing or invalid authentication token.
* `403 Forbidden`: Authenticated user lacks permission to access this resource.
* `404 Not Found`: Resource does not exist.
* `409 Conflict`: Unique constraint violation, race conflict, or state transition conflict.
* `422 Unprocessable Entity`: Semantically invalid payload (business rule failure).
* `429 Too Many Requests`: Rate limit threshold exceeded.
* `500 Internal Server Error`: Unhandled server error (never leak internal stack traces to client).

### Standard Error Response Envelope
```json
{
  "error": {
    "code": "INVALID_PAYLOAD",
    "message": "The provided email address is already in use.",
    "details": [
      { "field": "email", "issue": "Unique constraint violation" }
    ],
    "requestId": "req_01h7x..."
  }
}
```

---

## 2. Input Validation & Schema Guardrails

* Always parse and validate incoming request payloads at the boundary using schema validators (`Zod`, `Pydantic`, `Joi`, `Validator.js`) before calling business logic.
* Strip unvalidated fields to prevent Mass Assignment vulnerabilities.

---

## 3. Database Integrity, Queries & Transactions

* **Transactional Boundaries:** Always wrap multi-table write operations inside atomic database transactions (`tx.run()`, `db.transaction()`).
* **Prevent N+1 Query Anti-Patterns:** Use ORM joins (`include`, `select_related`, `prefetch_related`) or DataLoader rather than executing queries inside loops.
* **Pagination Standards:**
  - For small, static sets: Offset-based pagination (`limit`, `offset`).
  - For high-volume, real-time data: Keyset / Cursor-based pagination (`cursor`, `take`).
* **Connection Pooling:** Reuse connection pools; never instantiate new database connection clients per HTTP request.

---

## 4. Concurrency Guardrails, Atomic Mutations & Idempotency

### A. Preventing Race Conditions & Double-Spending
* **Anti-Pattern (Read-Modify-Write Race Condition):**
  ```ts
  // ❌ VULNERABLE: Concurrent requests will both read 100 and overwrite each other!
  const account = await db.account.findUnique({ where: { id } });
  if (account.balance >= amount) {
    await db.account.update({ where: { id }, data: { balance: account.balance - amount } });
  }
  ```
* **Correct Standard (Atomic Database Mutation):**
  ```ts
  // ✅ CORRECT: Atomic operation executed at the database engine level
  const updated = await db.account.updateMany({
    where: { id, balance: { gte: amount } },
    data: { balance: { decrement: amount } }
  });
  if (updated.count === 0) {
    throw new DomainError('INSUFFICIENT_FUNDS', 'Balance is insufficient for withdrawal.', 409);
  }
  ```

### B. Idempotency Keys for Financial & Critical Mutations
* For state-mutating requests (payments, checkout orders, refunds, webhooks):
  - Support `Idempotency-Key` in request headers.
  - Store incoming idempotency keys with their processing state and response payload in Redis/DB.
  - If a key is currently processing, return `409 Conflict` or wait; if already completed, return the cached successful response immediately without re-executing logic.

### C. Graceful Shutdown & Resource Teardown
Always register process signal handlers (`SIGTERM`, `SIGINT`) to stop accepting new traffic, finish in-flight requests, and cleanly close database pools and queues.

---

## 5. Mandatory Backend Execution Checklist

Follow this sequence for every backend route, handler, or service mutation:

1. **Pre-Flight Reuse Check:** Inspect `src/services/` or `src/controllers/` to reuse existing database clients, validators, and error classes.
2. **Boundary Validation:** Parse headers, query parameters, and JSON bodies with schema validation (`zod`, `pydantic`). Reject invalid input with `400` or `422`.
3. **Atomic Operations:** Ensure state-changing operations are atomic; guard against race conditions and wrap multi-entity writes in transactions.
4. **Error Handling:** Catch expected domain errors and map them to standard HTTP status codes. Never swallow errors silently or leak internal stack traces.
5. **Targeted Verification:** Run the targeted test for the modified handler or endpoint (e.g., `npm test -- user.test.ts`).

---

## 6. Contrast Matrix: Anti-Patterns vs Required Standards

### Anti-Pattern 1: Silent Error Swallowing
```ts
// ❌ WRONG: Swallows error silently, leaving system in inconsistent state
try {
  await db.user.create({ data });
} catch (err) {
  // Silent fail or meaningless console.log
}
```
```ts
// ✅ CORRECT: Log internal error and return structured error response
try {
  await db.user.create({ data });
} catch (err: unknown) {
  logger.error('Failed to create user', { error: err, requestId });
  throw new DomainError('USER_CREATION_FAILED', 'Unable to register user account.', 409);
}
```

### Anti-Pattern 2: Missing Boundary Validation (Mass Assignment)
```ts
// ❌ WRONG: Blindly trust user-supplied request body
app.post('/api/profile', async (req, res) => {
  await db.user.update({ where: { id: req.user.id }, data: req.body }); // Can overwrite isAdmin!
});
```
```ts
// ✅ CORRECT: Strict schema parsing stripping unvetted fields
const ProfileUpdateSchema = z.object({
  displayName: z.string().min(2).max(50),
  bio: z.string().max(280).optional(),
});

app.post('/api/profile', async (req, res) => {
  const validated = ProfileUpdateSchema.parse(req.body);
  await db.user.update({ where: { id: req.user.id }, data: validated });
});
```
