---
name: api-endpoint
description: >-
  Builds new API endpoints end-to-end. Use when adding routes, handlers/controllers,
  validation, service/action logic, response schemas/resources, and endpoint tests.
---

# API Endpoint Skill

## When to Apply
- User asks to add a new API endpoint or CRUD route.
- Existing API contract needs extension.
- Backend changes require request validation and response contract updates.

## Workflow
1. Read project specs first: `specs/specs.md`, then role-specific specs as needed.
2. Detect backend conventions from the repo (routing, controller/service patterns, validation style).
3. Define endpoint contract before implementation:
   - Path + method
   - Auth requirements
   - Request validation
   - Response shape and error shape
4. Implement with thin transport layer and business logic in domain/service/action classes.
5. Add focused tests for success path, validation failure, and authorization failure.

## Quality Bar
- Keep endpoint behavior idempotent where required.
- Avoid N+1 queries and over-fetching.
- Return consistent JSON payloads.
