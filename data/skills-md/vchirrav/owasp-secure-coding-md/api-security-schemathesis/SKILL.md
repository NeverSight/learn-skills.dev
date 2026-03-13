---
name: api-security-schemathesis
description: Run Schemathesis for property-based API security testing. Generates test cases from OpenAPI/GraphQL schemas to find crashes, 500 errors, and spec violations.
---

# API Security Testing with Schemathesis

You are a security engineer running property-based API security testing using **Schemathesis** to automatically generate test cases from API schemas.

## When to use

Use this skill when asked to test REST APIs or GraphQL endpoints for security issues using their OpenAPI/Swagger or GraphQL schema.

## Prerequisites

- Schemathesis installed (`pip install schemathesis`)
- API must be running with an accessible OpenAPI spec or GraphQL endpoint
- Verify: `schemathesis --version`

## Instructions

1. **Identify the target** — Confirm the API schema URL and base URL.
2. **Run the scan:**

   **OpenAPI:**
   ```bash
   schemathesis run <openapi-url> --report > schemathesis-report.txt
   ```

   **GraphQL:**
   ```bash
   schemathesis run <graphql-url> --report
   ```

   - With authentication: `schemathesis run <url> --auth user:pass`
   - Bearer token: `schemathesis run <url> --header "Authorization: Bearer <token>"`
   - Specific endpoints: `schemathesis run <url> --endpoint "/api/users"`
   - Stateful testing: `schemathesis run <url> --stateful=links`

3. **Parse the results** — Present findings:

```
| # | Endpoint | Method | Issue Type | Status Code | Finding | Reproduction |
|---|----------|--------|------------|-------------|---------|-------------|
```

4. **Summarize** — Provide:
   - Total endpoints tested and test cases generated
   - Server errors (5xx) found with reproduction steps
   - Schema violations and inconsistencies
   - Security-relevant findings (auth bypass, injection success, etc.)

## Issue Types Detected

| Type | Description |
|------|-------------|
| Server Error (5xx) | Unhandled exceptions / crashes |
| Schema Violation | Response doesn't match schema |
| Status Code Mismatch | Undocumented response codes |
| Content Type Mismatch | Wrong content type returned |
| Missing Auth | Endpoints accessible without credentials |
| Injection Patterns | SQL/NoSQL injection via fuzz inputs |
