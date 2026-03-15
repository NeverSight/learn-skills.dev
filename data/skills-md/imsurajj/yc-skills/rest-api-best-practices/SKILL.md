---
name: rest-api-best-practices
description: >
  Expert guidance for designing, building, and documenting production-ready
  REST APIs. Use when the user asks to build an API, design endpoints, handle
  errors, implement authentication, write API docs, version an API, structure
  responses, or review existing API code for best practices.
---

# REST API Best Practices

You are a senior backend engineer with deep expertise in designing and building
production-grade REST APIs. Your goal is to produce APIs that are consistent,
secure, scalable, and easy for other developers to consume.

---

## 1. URL & Endpoint Design

### Use nouns, not verbs
```
✅ GET    /users
✅ POST   /users
✅ GET    /users/:id
✅ PUT    /users/:id
✅ DELETE /users/:id

❌ GET  /getUsers
❌ POST /createUser
❌ GET  /deleteUser?id=1
```

### Use plural nouns consistently
```
✅ /users        not /user
✅ /products     not /product
✅ /orders       not /order
```

### Nest resources to show relationships (max 2 levels deep)
```
✅ GET /users/:id/orders          → orders belonging to a user
✅ GET /users/:id/orders/:orderId → specific order of a user

❌ GET /users/:id/orders/:orderId/items/:itemId/reviews  → too deep, flatten it
✅ GET /order-items/:itemId/reviews                      → flatten instead
```

### Use kebab-case for multi-word resources
```
✅ /product-categories
✅ /blog-posts
✅ /payment-methods

❌ /productCategories
❌ /product_categories
```

### Keep query params for filtering, sorting, searching, pagination
```
GET /products?category=shoes&sort=price&order=asc&page=2&limit=20
GET /users?search=john&role=admin&status=active
```

---

## 2. HTTP Methods — Use Them Correctly

| Method  | Use For               | Idempotent | Body |
|---------|-----------------------|------------|------|
| GET     | Fetch resource(s)     | ✅ Yes     | ❌ No |
| POST    | Create new resource   | ❌ No      | ✅ Yes |
| PUT     | Replace entire resource | ✅ Yes   | ✅ Yes |
| PATCH   | Update partial resource | ✅ Yes   | ✅ Yes |
| DELETE  | Remove resource       | ✅ Yes     | ❌ No |

### PUT vs PATCH — know the difference
```json
// PUT — send the FULL object (replaces everything)
PUT /users/123
{ "name": "John", "email": "john@mail.com", "role": "admin" }

// PATCH — send ONLY the fields you want to change
PATCH /users/123
{ "email": "newemail@mail.com" }
```

---

## 3. HTTP Status Codes — Use the Right One

### 2xx — Success
```
200 OK           → successful GET, PUT, PATCH
201 Created      → successful POST (always return the created resource)
204 No Content   → successful DELETE (no body needed)
```

### 4xx — Client Errors
```
400 Bad Request       → invalid input, validation failed
401 Unauthorized      → not authenticated (no token / bad token)
403 Forbidden         → authenticated but no permission
404 Not Found         → resource doesn't exist
409 Conflict          → duplicate entry (email already exists)
422 Unprocessable     → valid JSON but business rule failed
429 Too Many Requests → rate limit hit
```

### 5xx — Server Errors
```
500 Internal Server Error → unexpected crash (never expose stack traces)
502 Bad Gateway           → upstream service failed
503 Service Unavailable   → server is down or overloaded
```

### Common mistakes to avoid
```
❌ 200 OK with { "error": "user not found" } in body — always use correct status
❌ 404 for auth failures — use 401/403 (don't leak resource existence)
❌ 500 for validation errors — use 400
```

---

## 4. Response Structure — Be Consistent

### Always use a consistent response envelope

**Success (single resource):**
```json
{
  "data": {
    "id": "usr_123",
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": "2025-01-15T10:30:00Z"
  }
}
```

**Success (list with pagination):**
```json
{
  "data": [
    { "id": "usr_123", "name": "John Doe" },
    { "id": "usr_124", "name": "Jane Smith" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 84,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": false
  }
}
```

**Error response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      { "field": "email", "message": "Must be a valid email address" },
      { "field": "password", "message": "Must be at least 8 characters" }
    ]
  }
}
```

### Rules for responses
- Always return `id` as a string, not an integer (avoids JS precision issues)
- Always use ISO 8601 for dates: `"2025-01-15T10:30:00Z"`
- Never return `null` fields — omit them or return empty array `[]`
- Never expose internal fields: `password`, `__v`, `_id` (use `id` not `_id`)
- Use `camelCase` for JSON keys (not `snake_case`)

---

## 5. Authentication & Authorization

### Use Bearer tokens in headers (not query params)
```
✅ Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...

❌ GET /users?token=eyJhbGciOiJIUzI1NiIsInR5...  (tokens in URLs get logged)
```

### JWT Best Practices
```
- Access token expiry:  15 minutes
- Refresh token expiry: 7–30 days
- Store refresh tokens in httpOnly cookies (not localStorage)
- Rotate refresh tokens on every use
- Sign with RS256 (asymmetric) in production, HS256 ok for small apps
- Never store sensitive data in JWT payload (it's base64, not encrypted)
```

### API Key Best Practices (for server-to-server)
```
- Prefix keys so they're identifiable: sk_live_xxx, pk_test_xxx
- Hash keys before storing in DB (bcrypt or SHA-256)
- Never return the full key after creation — show once only
- Support key rotation without breaking existing integrations
- Scope keys to specific permissions
```

### Always separate Authentication from Authorization
```
401 Unauthorized  → WHO are you? (not logged in / bad token)
403 Forbidden     → WHO you are doesn't have access to THIS (logged in but no permission)
```

---

## 6. Validation & Error Handling

### Validate everything at the boundary (before it touches business logic)
```javascript
// Example schema validation with Zod
const createUserSchema = z.object({
  name:     z.string().min(2).max(100),
  email:    z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
  role:     z.enum(['admin', 'user', 'guest']).default('user')
})
```

### Return ALL validation errors at once, not one at a time
```json
// ✅ Return all errors together
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "password", "message": "Must be at least 8 characters" }
    ]
  }
}

// ❌ Don't make the user fix one error at a time
{ "error": "Invalid email format" }
```

### Use error codes (not just messages)
```
Error codes let clients handle errors programmatically without parsing strings.

VALIDATION_ERROR
RESOURCE_NOT_FOUND
DUPLICATE_ENTRY
INSUFFICIENT_PERMISSIONS
RATE_LIMIT_EXCEEDED
INVALID_TOKEN
TOKEN_EXPIRED
```

### Never expose internal errors to clients
```javascript
// ✅ Safe
res.status(500).json({
  error: { code: "INTERNAL_ERROR", message: "Something went wrong" }
})

// ❌ Never do this — exposes stack trace, DB queries, file paths
res.status(500).json({ error: err.stack })
```

---

## 7. Pagination

### Always paginate list endpoints — never return unbounded lists

**Offset pagination (simple, good for most cases):**
```
GET /products?page=2&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 340,
    "totalPages": 17
  }
}
```

**Cursor pagination (better for large datasets / real-time data):**
```
GET /feed?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}
```

### Rules
- Default limit: 20
- Max limit: 100 (reject requests above this)
- Never default to returning all records

---

## 8. API Versioning

### Version in the URL path (most common, easiest to understand)
```
✅ /api/v1/users
✅ /api/v2/users

❌ /api/users?version=1   (messy)
❌ Accept: application/vnd.api.v1+json  (hard to test in browser)
```

### Versioning rules
- Start with v1 from day one — even if you're solo
- Never break v1 when releasing v2 — run both simultaneously
- Deprecate with a sunset header before removing:
  `Sunset: Sat, 01 Jan 2026 00:00:00 GMT`
- What counts as a breaking change:
  - Removing a field from response
  - Renaming a field
  - Changing a field's data type
  - Removing an endpoint
  - Changing required/optional params

---

## 9. Security Essentials

### Rate Limiting — always implement before going to production
```
General API:       100 requests / 15 min per IP
Auth endpoints:    5 requests / 15 min per IP (strict)
Password reset:    3 requests / hour per email
Public endpoints:  200 requests / min per IP
```

### CORS — lock it down
```javascript
// ✅ Explicit origin whitelist
cors({ origin: ['https://yourapp.com', 'https://admin.yourapp.com'] })

// ❌ Never in production
cors({ origin: '*' })
```

### Security Headers (use helmet.js in Node)
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

### Input Security Rules
- Sanitize all inputs before DB queries (prevent SQL injection / NoSQL injection)
- Validate file uploads: type, size, and scan for malware
- Never trust `Content-Type` header alone — validate the actual content
- Strip unknown fields from request bodies before processing

---

## 10. Performance

### Use compression
```javascript
app.use(compression()) // gzip all responses above 1KB
```

### Add caching headers for GET endpoints
```
Cache-Control: public, max-age=300        → cache for 5 minutes
Cache-Control: private, no-store          → sensitive data, never cache
ETag: "abc123"                            → conditional requests
```

### Database query rules
- Never do N+1 queries — use eager loading / joins
- Always paginate — never fetch all records
- Add indexes on columns used in WHERE, JOIN, ORDER BY
- Use `SELECT specific_columns` not `SELECT *`

### Response size rules
- Return only the fields the client needs
- Support field selection: `GET /users?fields=id,name,email`
- Compress large payloads with gzip

---

## 11. API Documentation

### Every endpoint must document
```markdown
## POST /users

Creates a new user account.

**Auth required:** No

**Request Body:**
| Field    | Type   | Required | Description           |
|----------|--------|----------|-----------------------|
| name     | string | ✅       | Full name (2-100 chars) |
| email    | string | ✅       | Valid email address   |
| password | string | ✅       | Min 8 chars           |

**Success Response: 201 Created**
\```json
{
  "data": {
    "id": "usr_123",
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": "2025-01-15T10:30:00Z"
  }
}
\```

**Error Responses:**
- 400 — Validation error
- 409 — Email already exists
```

### Use OpenAPI/Swagger spec for larger APIs
- Generate docs automatically from code (swagger-jsdoc, tsoa, fastify-swagger)
- Always keep docs in sync with actual behavior
- Include example requests and responses for every endpoint

---

## 12. Output Format for API Design Tasks

When designing or reviewing an API, always output in this structure:

```
ENDPOINT DESIGN:
  Method + URL + Description

REQUEST:
  Headers:
  Body (with types and validation rules):

RESPONSE:
  Success (status code + body):
  Errors (status code + error code + message):

SECURITY NOTES:
  Auth required: yes/no
  Rate limit: x requests / y minutes
  Special considerations:

IMPLEMENTATION NOTES:
  DB queries needed:
  Edge cases to handle:
  Performance considerations:
```

---

## When to Activate This Skill

- User says "build an API", "design endpoints", "create a REST API"
- User asks "how should I structure my routes / responses"
- User shares API code and asks for a review
- User asks about auth, tokens, JWT, API keys
- User asks about error handling, status codes, validation
- User asks "how do I paginate", "how do I version my API"
- User asks about rate limiting, CORS, API security
- User asks to document an API or write OpenAPI spec

