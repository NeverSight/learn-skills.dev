---
name: testing-api
description: Test API endpoints and contracts
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# API Testing

Test REST, GraphQL, gRPC, and other API endpoints for functionality, performance, and reliability.

## When to use me

Use this skill when:
- Developing or consuming API services
- Testing API contracts and schemas
- Validating request/response formats
- Testing authentication and authorization
- Checking rate limiting and quotas
- Verifying error responses and status codes
- Performing contract testing between services

## What I do

- Test API endpoints with various HTTP methods
- Validate request/response schemas and formats
- Test authentication mechanisms (OAuth, JWT, API keys)
- Verify error handling and status codes
- Check rate limiting and throttling behavior
- Test payload validation and error messages
- Perform contract testing with OpenAPI/Swagger
- Test API versioning and backward compatibility

## Examples

```bash
# Test APIs with common tools
npx newman run collection.json    # Postman collections
curl -X GET https://api.example.com/users
http GET https://api.example.com/users Authorization:"Bearer token"

# Run API tests with frameworks
npm run test:api                 # Supertest, Jest
pytest tests/api/                # Python requests/pytest
go test ./api/                   # Go httptest

# Test with schema validation
npx ajv validate -s schema.json -d data.json
openapi-test --spec openapi.yaml --base-url https://api.example.com

# Load test APIs
npx autocannon -c 10 -d 30 https://api.example.com/users
wrk -t2 -c100 -d30s https://api.example.com/users
```

## Output format

```
API Test Results:
──────────────────────────────
✅ GET /api/users
  ✓ Returns 200 OK
  ✓ Returns JSON array
  ✓ Includes pagination headers
  ✓ Respects limit parameter

❌ POST /api/users
  ✗ Missing required fields returns 400
    Expected: {"error": "Missing email"}
    Received: {"error": "Validation failed"}

⚠️ PUT /api/users/{id}
  ⚠️ Authentication required but not tested

Authentication Tests:
  ✓ Valid token returns 200
  ✗ Invalid token returns 401 (should return 403)

Summary: 15 endpoints tested, 12 passed, 2 failed, 1 skipped
```

## Notes

- Test all HTTP methods supported by endpoints
- Validate response schemas against OpenAPI specs
- Test edge cases: empty arrays, null values, large payloads
- Verify CORS headers if applicable
- Test authentication flows thoroughly
- Consider contract testing for microservices
- Monitor API response times and latency
