---
name: api-design
description: REST API design principles and patterns - use when designing new endpoints, creating DTOs, or planning API structure
---

# REST API Design Principles

## URL Structure

```
GET    /api/v1/resources           # List all
GET    /api/v1/resources/{id}      # Get one
POST   /api/v1/resources           # Create
PUT    /api/v1/resources/{id}      # Replace
PATCH  /api/v1/resources/{id}      # Partial update
DELETE /api/v1/resources/{id}      # Delete

# Nested resources
GET    /api/v1/parents/{id}/children
POST   /api/v1/parents/{id}/children
```

## HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (new resource) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors, malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Valid auth but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, state conflict |
| 422 | Unprocessable | Semantic errors |
| 500 | Server Error | Unexpected errors |

## Request/Response Design

### Collection Response

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 150,
    "totalPages": 8
  }
}
```

### Single Resource Response

```json
{
  "id": "uuid",
  "name": "Resource Name",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T11:00:00Z"
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Name is required",
    "details": [
      {"field": "name", "message": "must not be blank"}
    ]
  }
}
```

## Query Parameters

```
# Filtering
GET /api/v1/resources?status=active&type=premium

# Sorting
GET /api/v1/resources?sort=createdAt,desc

# Pagination
GET /api/v1/resources?page=1&pageSize=20

# Field selection
GET /api/v1/resources?fields=id,name,status

# Search
GET /api/v1/resources?search=query
```

## Idempotency

- POST with unique identifiers should return existing resource (200) if duplicate
- PUT/DELETE should be idempotent
- Use `Pair<Result, Boolean>` pattern to indicate created vs existing

## Versioning

- Use URL path versioning: `/api/v1/`, `/api/v2/`
- Version when making breaking changes
- Support old versions during migration period

## Security Considerations

- Always validate input at API boundary
- Use parameterized queries (JOOQ handles this)
- Check authorization in service layer
- Never expose internal IDs or sensitive data
- Rate limit public endpoints
