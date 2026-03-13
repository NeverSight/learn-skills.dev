---
name: api-mock-designer
description: Designs realistic API mock servers. Goes beyond happy paths by designing stateful mocks (create order -> get order) for complex integrations.
---

# API Mock Designer Protocol

This skill allows mobile and frontend developers to construct robust UIs without waiting for the backend to be finished. It goes beyond simple static JSON stubs to provide a truly simulated environment that mimics production chaos.

**Core assumption:** If a frontend only tests against static `200 OK` responses, it will break immediately in production when a `503 Service Unavailable` or a 4-second latency spike occurs.

---

## 1. Scenario Planning (Static)
Analyze the API spec and design scenarios that consumers *must* handle:
- **Happy Path:** Standard CRUD operations.
- **Chaos / Edge Cases:** 
  - `429 Too Many Requests` (Testing retry logic).
  - `500/503` (Testing error boundaries/toasts).
  - High Latency Responses (Testing loading spinners/skeleton screens).
  - Partial or Empty Lists (Testing "No items found" UI states).

## 2. Stateful Design
A good mock server must be stateful in a single session.
- If a client sends `POST /users`, the next call to `GET /users` MUST include the newly created user in memory.

## 3. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/api-mock-report.md`)**
```markdown
### 🧪 API Mock Server Blueprint

**Tooling Recommendation:** WireMock or MSW (Mock Service Worker)

#### 🚥 Configured Scenarios

**1. Stateful Order Flow**
- `POST /orders`: Returns `201` and saves `{ id: 123 }` to memory.
- `GET /orders/123`: Returns the saved order instead of a random stub.

**2. The Chaos Endpoint (Latency & Reliability)**
- `GET /products`:
  - 80% chance: Returns `200 OK` (with 500ms - 2000ms randomized latency).
  - 15% chance: Returns `503 Service Unavailable` (to test failure UI).
  - 5% chance: Returns `429 Too Many Requests`.

**3. Empty State Testing**
- `GET /notifications`: Purposefully returns an empty array `[]` to ensure the frontend displays the "All caught up!" screen correctly.
```

2. **Machine-Readable JSON (`docs/api-report/api-mock-output.json`)**
```json
{
  "skill": "api-mock-designer",
  "tooling": "MSW",
  "scenarios": [
    {"name": "Stateful Validation", "endpoint": "/orders", "method": "POST/GET"},
    {"name": "Chaos Latency", "endpoint": "/products", "error_rate_pct": 20, "max_latency_ms": 2000},
    {"name": "Empty State", "endpoint": "/notifications", "returns": []}
  ]
}
```

---

## Guardrails
- **Avoid Over-Engineering:** Mock servers shouldn't recreate complex backend business logic (like computing tax). They just need to faithfully replay expected structural responses.
- **Schema Validation:** Ensure the mock data strictly adheres to the definitions in the `contract-first-designer`'s OpenAPI spec.
