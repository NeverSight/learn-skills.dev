---
name: api-doc-generator
description: Generates comprehensive API documentation from source code by analyzing endpoint definitions, request/response schemas, authentication requirements, and error codes. Produces structured docs in OpenAPI-compatible format with examples, parameter descriptions, and usage guides. Use when documenting APIs, generating API reference docs, creating endpoint documentation, or when the user needs API docs from their codebase.
---

# API Documentation Generator

## Overview

Generate comprehensive, structured API documentation by analyzing source code.
The skill extracts endpoint definitions, HTTP methods, parameters,
request/response schemas, authentication requirements, and error handling
patterns, then produces documentation in both human-readable Markdown and
machine-readable OpenAPI 3.0 JSON format.

## When to use

- When the user asks to document an API or generate API docs
- When a codebase has REST endpoints that need reference documentation
- When migrating undocumented APIs and need to capture existing behavior
- When generating OpenAPI/Swagger specs from source code
- When the user mentions "API docs", "endpoint documentation", or "API
  reference"

**Do NOT use when:**

- The user needs to _consume_ existing API docs (just read them directly)
- The API is already fully documented and the user wants to call it
- The user needs GraphQL schema docs (different structure, different tool)
- The task is writing API _code_, not documenting existing code

## Workflow

### 1. Scan for route/endpoint definitions

Search the codebase for route registration patterns. Look for framework-specific
patterns:

| Framework    | Pattern to find                                      |
| ------------ | ---------------------------------------------------- |
| Express.js   | `app.get()`, `router.post()`, `app.use()` with paths |
| FastAPI      | `@app.get()`, `@router.post()`, path decorators      |
| Django REST  | `urlpatterns`, `@api_view`, ViewSet classes          |
| Spring Boot  | `@GetMapping`, `@PostMapping`, `@RequestMapping`     |
| Go (Gin/Chi) | `r.GET()`, `r.POST()`, `r.Route()`                   |
| Rails        | `routes.rb`, `resources :`, controller actions       |
| NestJS       | `@Get()`, `@Post()`, `@Controller()` decorators      |

**Output:** A list of all endpoints with their file locations.

### 2. Extract HTTP methods, paths, and parameters

For each endpoint, extract:

- **HTTP method** (GET, POST, PUT, PATCH, DELETE)
- **Path** including path parameters (e.g., `/users/:id`)
- **Query parameters** from request parsing code
- **Request body** schema from validation or type definitions
- **Response body** from return statements or serializers
- **Content types** (JSON, form-data, multipart)

Parse path parameters from the route string. Look for query parameter access
(`req.query`, `request.args`, `@Query`) and body parsing (`req.body`,
`request.json()`, `@Body`).

### 3. Analyze request/response types

Trace type information from:

- TypeScript interfaces/types used in handlers
- Pydantic models, dataclasses, or serializers
- Zod/Joi/Yup validation schemas
- Database model definitions that map to responses
- JSDoc/docstring annotations

Build a schema for each request body and response body. Include field names,
types, required/optional status, and constraints (min/max, regex, enum values).

### 4. Document authentication requirements

Look for:

- Middleware applied to routes (`authenticate`, `requireAuth`, `jwt_required`)
- Decorator-based auth (`@login_required`, `@Depends(get_current_user)`)
- Guard classes (NestJS `@UseGuards(AuthGuard)`)
- API key checks in handler code
- OAuth scopes or role-based access control

Document the auth scheme (Bearer token, API key, session cookie, OAuth2) and
which endpoints require it. Note any role/permission requirements.

### 5. Generate error response documentation

Analyze error handling to document:

- **Validation errors** (400) - what triggers them, response format
- **Authentication errors** (401) - when auth fails or is missing
- **Authorization errors** (403) - permission denied scenarios
- **Not found errors** (404) - when resources don't exist
- **Conflict errors** (409) - duplicate resources, state conflicts
- **Rate limit errors** (429) - if rate limiting is present
- **Server errors** (500) - generic error response format

For each error, document the status code, error response schema, and conditions
that trigger it. Look for custom error classes, error middleware, and exception
handlers.

### 6. Add usage examples

For every endpoint, generate:

- A **curl example** showing a complete request with realistic data
- A **success response** example with realistic field values
- An **error response** example showing the most common failure case
- **Request body examples** for POST/PUT/PATCH endpoints

Use realistic but obviously fake data (e.g., `user@example.com`, not
`test@test.com`). Include all required headers (Content-Type, Authorization).

### 7. Produce final structured output

Generate TWO output files:

**`api-docs.md`** - Human-readable Markdown documentation:

````markdown
# API Reference

## Overview

Brief description of the API, base URL, and common patterns.

## Authentication

How to authenticate, token format, where to include credentials.

## Endpoints

### Resource Name

#### METHOD /path

Description of what this endpoint does.

**Parameters:**

| Name | In | Type | Required | Description |
| ---- | -- | ---- | -------- | ----------- |

**Request Body:**

```json
{ "example": "value" }
```

**Response (200):**

```json
{ "example": "response" }
```

**Error Responses:**

| Status | Description |
| ------ | ----------- |

**Example:**

```bash
curl -X METHOD https://api.example.com/path ...
```
````

**`openapi.json`** - OpenAPI 3.0 specification:

```json
{
  "openapi": "3.0.3",
  "info": { "title": "API Name", "version": "1.0.0" },
  "paths": { "...": {} },
  "components": { "schemas": { "...": {} }, "securitySchemes": { "...": {} } }
}
```

## Checklist

- [ ] All route/endpoint files identified and scanned
- [ ] Every endpoint has HTTP method, path, and description
- [ ] Path parameters, query parameters, and request bodies documented
- [ ] Request/response schemas include field types and constraints
- [ ] Authentication requirements documented per-endpoint
- [ ] Error responses documented with status codes and schemas
- [ ] Every endpoint has at least one curl example
- [ ] POST/PUT/PATCH endpoints have request body examples
- [ ] Output includes both api-docs.md and openapi.json
- [ ] OpenAPI spec is valid (correct structure, $ref usage)

## Example

**Input:** Express.js route file

```javascript
// routes/users.js
const express = require("express");
const router = express.Router();
const { authenticate } = require("../middleware/auth");
const { validate } = require("../middleware/validate");
const { body, param, query } = require("express-validator");

// GET /api/users - List users with pagination
router.get("/", authenticate, [
  query("page").optional().isInt({ min: 1 }).toInt(),
  query("limit").optional().isInt({ min: 1, max: 100 }).toInt(),
  query("role").optional().isIn(["admin", "user", "moderator"]),
], async (req, res) => {
  const { page = 1, limit = 20, role } = req.query;
  const users = await User.find(role ? { role } : {})
    .skip((page - 1) * limit)
    .limit(limit);
  const total = await User.countDocuments(role ? { role } : {});
  res.json({ users, total, page, limit });
});

// POST /api/users - Create a new user
router.post(
  "/",
  authenticate,
  [
    body("email").isEmail().normalizeEmail(),
    body("name").trim().isLength({ min: 2, max: 100 }),
    body("role").isIn(["admin", "user", "moderator"]),
    body("password").isLength({ min: 8 }),
  ],
  validate,
  async (req, res) => {
    const existing = await User.findOne({ email: req.body.email });
    if (existing) {
      return res.status(409).json({ error: "Email already registered" });
    }
    const user = await User.create(req.body);
    res.status(201).json({ user: user.toPublic() });
  },
);

// GET /api/users/:id - Get user by ID
router.get(
  "/:id",
  authenticate,
  [param("id").isMongoId()],
  validate,
  async (req, res) => {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json({ user: user.toPublic() });
  },
);
```

**Output:** (excerpt from api-docs.md)

````markdown
# API Reference

## Authentication

All endpoints require a Bearer token in the Authorization header:

    Authorization: Bearer <your-jwt-token>

## Endpoints

### Users

#### GET /api/users

List users with optional filtering and pagination.

**Query Parameters:**

| Name  | Type    | Required | Default | Description                               |
| ----- | ------- | -------- | ------- | ----------------------------------------- |
| page  | integer | No       | 1       | Page number (minimum: 1)                  |
| limit | integer | No       | 20      | Results per page (1-100)                  |
| role  | string  | No       | -       | Filter by role: admin, user, or moderator |

**Response (200 OK):**

```json
{
  "users": [
    {
      "id": "507f1f77bcf86cd799439011",
      "email": "jane@example.com",
      "name": "Jane Smith",
      "role": "admin"
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 20
}
```

**Error Responses:**

| Status | Condition             | Body                                     |
| ------ | --------------------- | ---------------------------------------- |
| 401    | Missing/invalid token | `{ "error": "Unauthorized" }`            |
| 422    | Invalid query params  | `{ "errors": [{ "param": "...", ... }]}` |

**Example:**

```bash
curl -H "Authorization: Bearer eyJhbG..." \
  "https://api.example.com/api/users?page=1&limit=10&role=admin"
```

---

#### POST /api/users

Create a new user account.

**Request Body:**

| Field    | Type   | Required | Constraints                    |
| -------- | ------ | -------- | ------------------------------ |
| email    | string | Yes      | Valid email format             |
| name     | string | Yes      | 2-100 characters               |
| role     | string | Yes      | One of: admin, user, moderator |
| password | string | Yes      | Minimum 8 characters           |

```json
{
  "email": "jane@example.com",
  "name": "Jane Smith",
  "role": "user",
  "password": "secureP@ss123"
}
```

**Response (201 Created):**

```json
{
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "jane@example.com",
    "name": "Jane Smith",
    "role": "user"
  }
}
```

**Error Responses:**

| Status | Condition             | Body                                      |
| ------ | --------------------- | ----------------------------------------- |
| 401    | Missing/invalid token | `{ "error": "Unauthorized" }`             |
| 409    | Email already exists  | `{ "error": "Email already registered" }` |
| 422    | Validation failed     | `{ "errors": [{ "param": "...", ... }]}`  |

**Example:**

```bash
curl -X POST https://api.example.com/api/users \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","name":"Jane Smith","role":"user","password":"secureP@ss123"}'
```
````

## Common mistakes

| Mistake                        | Fix                                                                                                            |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Missing error responses        | Check every `res.status()` call and error middleware. Document ALL non-2xx responses, not just the happy path. |
| Undocumented auth requirements | Trace middleware chains. If `authenticate` is applied to a router, ALL sub-routes require auth.                |
| No request/response examples   | Generate examples for every endpoint. Use realistic data, not `"string"` or `"test"`.                          |
| Ignoring query parameters      | Search for `req.query`, `request.args`, `@Query()` — these are often undocumented.                             |
| Missing parameter constraints  | Document min/max, regex patterns, enum values — not just the type.                                             |
| Incomplete OpenAPI spec        | Validate the JSON against the OpenAPI 3.0 schema. Common gaps: missing `required` arrays, wrong `$ref` paths.  |
| Documenting internal routes    | Skip health checks, metrics endpoints, and internal admin routes unless explicitly requested.                  |
| Inconsistent formatting        | Use the same table structure and section order for every endpoint. Consistency aids scanning.                  |

## Quick reference

| Operation             | How                                                                         |
| --------------------- | --------------------------------------------------------------------------- |
| Find Express routes   | Search for `router.get\|post\|put\|delete\|patch`                           |
| Find FastAPI routes   | Search for `@app.get\|post\|put\|delete\|patch` or `@router.`               |
| Find auth middleware  | Search for `authenticate`, `requireAuth`, `jwt_required`, `@login_required` |
| Find validation       | Search for `body()`, `param()`, `query()`, Zod schemas, Pydantic models     |
| Find error handling   | Search for `res.status(4`, `raise HTTP`, `throw new`, custom error classes  |
| Build OpenAPI paths   | One entry per unique path, methods nested under path object                 |
| Build OpenAPI schemas | Extract from TypeScript types, Pydantic models, or validation schemas       |

## Key principles

1. **Document every parameter** - Every path param, query param, header, and
   body field must appear in the docs. Undocumented parameters are the #1 source
   of API integration bugs.

2. **Include realistic examples** - Every endpoint needs a curl example with
   realistic (but fake) data, a success response, and at least one error
   response. Developers copy-paste from docs; make it work.

3. **Show error cases explicitly** - Document every error status code with its
   trigger condition and response body. Developers spend more time debugging
   errors than writing happy-path code.

4. **Maintain consistent structure** - Every endpoint section must follow the
   same format: description, parameters table, request body, response, errors,
   example. Consistency lets developers scan quickly.

5. **Dual output format** - Always produce both human-readable Markdown and
   machine-readable OpenAPI JSON. The Markdown is for developers reading docs;
   the OpenAPI spec is for tooling (Postman, SDK generators, API gateways).
