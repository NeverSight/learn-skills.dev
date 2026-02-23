---
name: api-testing
description: |
  API testing patterns with supertest, MSW, and Vitest. Covers integration testing for REST APIs, HTTP request mocking with Mock Service Worker v2, response assertions, schema validation, test organization, and framework-specific patterns for Express, Fastify, and Hono.

  Use when writing integration tests for REST APIs, mocking HTTP requests, or testing API endpoints. Use for api-test, supertest, msw, mock-service-worker, integration-test, http-mock, endpoint-test, request-test.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://mswjs.io/docs'
---

# API Testing

## Overview

API testing validates HTTP endpoints by sending requests and asserting responses, covering status codes, headers, body content, and error handling. Supertest provides a fluent chainable API for integration testing against Express, Fastify, and Hono apps without starting a real server. MSW (Mock Service Worker) v2 intercepts outgoing HTTP requests at the network level, enabling realistic mocking of external services in both Node.js tests and browser environments.

**When to use:** Integration tests for REST APIs, testing middleware pipelines, validating request/response contracts, mocking third-party APIs in tests, testing error handling and edge cases.

**When NOT to use:** Unit testing pure functions (use direct assertions), E2E browser testing (use Playwright/Cypress), load/performance testing (use k6/Artillery), testing static file serving.

## Quick Reference

| Pattern               | API                                        | Key Points                                  |
| --------------------- | ------------------------------------------ | ------------------------------------------- |
| GET request           | `request(app).get('/path')`                | Returns supertest `Test` object             |
| POST with body        | `request(app).post('/path').send(body)`    | Automatically sets Content-Type             |
| Auth header           | `.set('Authorization', 'Bearer token')`    | Chain before `.expect()`                    |
| Status assertion      | `.expect(200)`                             | Chainable with body assertions              |
| Body assertion        | `.expect({ key: 'value' })`                | Deep equality check                         |
| Header assertion      | `.expect('Content-Type', /json/)`          | Accepts string or regex                     |
| MSW HTTP handler      | `http.get('/api/users', resolver)`         | Intercepts matching requests                |
| MSW GraphQL handler   | `graphql.query('GetUser', resolver)`       | Intercepts by operation name                |
| MSW response          | `HttpResponse.json(data, { status })`      | v2 response format                          |
| MSW error simulation  | `HttpResponse.error()`                     | Simulates network failure                   |
| MSW one-time handler  | `http.get(path, resolver, { once: true })` | Auto-removed after first match              |
| MSW per-test override | `server.use(handler)`                      | Override default handlers in specific tests |
| Schema validation     | `schema.parse(response.body)`              | Validates response structure with Zod       |
| Cookie persistence    | `const agent = request.agent(app)`         | Maintains cookies across requests           |
| Fastify inject        | `app.inject({ method, url })`              | Built-in testing without supertest          |
| Hono test client      | `testClient(app)`                          | Type-safe request builder                   |

## Common Mistakes

| Mistake                                    | Correct Pattern                                             |
| ------------------------------------------ | ----------------------------------------------------------- |
| Not awaiting supertest requests            | Always `await request(app).get('/path')`                    |
| Sharing server state between tests         | Reset handlers with `server.resetHandlers()` in `afterEach` |
| Mocking fetch/axios directly               | Use MSW to intercept at the network level                   |
| Forgetting `server.listen()` in setup      | Call in `beforeAll`, `resetHandlers` in `afterEach`         |
| Passing Fastify instance to supertest      | Use `fastify.server` (the underlying Node server)           |
| Asserting before response completes        | Use `await` or return the supertest chain                   |
| Hardcoding test data across many tests     | Use factories or fixtures for test data                     |
| Not testing error responses                | Test 4xx and 5xx paths alongside happy paths                |
| Using `server.close()` in `afterEach`      | Use `afterAll` for close, `afterEach` for reset only        |
| Ignoring response headers in assertions    | Validate Content-Type, Cache-Control, CORS headers          |
| Not using `onUnhandledRequest: 'error'`    | Catch unhandled requests to prevent silent test gaps        |
| Testing implementation instead of behavior | Assert on response shape, not internal function calls       |

## Delegation

- **Test structure review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent
- **Pattern discovery**: Use `Explore` agent

> If the `vitest-testing` skill is available, delegate general Vitest configuration and patterns to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill vitest-testing`

## References

- [Supertest integration testing patterns for Express, Fastify, and Hono](references/supertest-patterns.md)
- [MSW request handlers, response resolvers, and server setup](references/msw-handlers.md)
- [Test organization, fixtures, factories, and setup/teardown](references/test-organization.md)
- [Response assertions, status codes, headers, and schema validation](references/assertion-patterns.md)
