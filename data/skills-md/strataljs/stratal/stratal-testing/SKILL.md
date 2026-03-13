---
name: stratal-testing
description: >-
  Use when writing tests for Stratal applications — TestingModule, HTTP testing,
  mocks, fakes, and auth testing utilities. Trigger on: test, TestingModule,
  TestHttpClient, TestResponse, mock, fake, FakeStorageService, createFetchMock,
  createMock, ActingAs, @stratal/testing.
user-invocable: false
license: MIT
metadata:
  author: Temitayo Fadojutimi
  version: "2.0"
---

# @stratal/testing

Test utilities for Stratal applications: module compilation with provider overrides, fluent HTTP client, storage fakes, fetch mocking, and auth testing helpers. Full documentation at [stratal.dev/testing](https://stratal.dev/testing/overview).

## Setup

Docs: [Overview](https://stratal.dev/testing/overview)

```ts
// vitest.setup.ts
import 'reflect-metadata';
import { Test } from '@stratal/testing';
Test.setBaseModules([CoreModule]);
```

Test file convention: `src/**/__tests__/**/*.spec.ts`. Always call `module.close()` in `afterEach`.

## Creating Test Modules

Docs: [Testing Module](https://stratal.dev/testing/testing-module)

```ts
const module = await Test.createTestingModule({
  imports: [UsersModule],
})
  .overrideProvider(EMAIL_TOKEN)
  .useValue(mockEmailService)
  .withEnv({ DATABASE_URL: 'test-url' })
  .compile();
```

Access services: `module.get(TOKEN)`. Access HTTP client: `module.http`. Access container: `module.container`.

## Provider Overrides

Chain overrides before `.compile()`:

```ts
Test.createTestingModule({ imports: [AppModule] })
  .overrideProvider(TOKEN_A).useValue(mockA)
  .overrideProvider(TOKEN_B).useClass(FakeB)
  .overrideProvider(TOKEN_C).useFactory(() => stub)
  .compile();
```

Use `.withEnv()` to set environment variables. Use `Test.setBaseModules()` for modules shared across all tests.

## HTTP Testing

Docs: [HTTP Testing](https://stratal.dev/testing/http-testing)

```ts
const response = await module.http
  .post('/api/v1/users')
  .withBody({ email: 'test@example.com' })
  .withHeaders({ 'X-Custom': 'value' })
  .send();

response.assertCreated();
await response.assertJsonPath('data.email', 'test@example.com');
```

Assertion methods: `assertOk()`, `assertCreated()`, `assertNotFound()`, `assertUnauthorized()`, `assertForbidden()`, `assertStatus(code)`, `assertJsonPath(path, value)`, `assertJsonStructure(shape)`.

## FakeStorageService

Docs: [Mocks & Fakes](https://stratal.dev/testing/mocks-and-fakes)

Auto-registered in test modules. Access via `module.storage`. Assertions: `assertExists(path)`, `assertMissing(path)`, `assertEmpty()`, `assertCount(n)`. Utility: `getStoredPaths()`, `getFile(path)`, `clear()`.

## Fetch Mocking

Docs: [Mocks & Fakes](https://stratal.dev/testing/mocks-and-fakes)

```ts
import { createFetchMock } from '@stratal/testing';

const mock = createFetchMock();
// In beforeEach: mock.activate(); mock.disableNetConnect()
// In afterEach:  mock.reset()

mock.mockJsonResponse('https://api.example.com/data', { result: 'ok' });
mock.mockError('https://api.example.com/fail', 503, 'Service Unavailable');
```

## Deep Mocks

Docs: [Mocks & Fakes](https://stratal.dev/testing/mocks-and-fakes)

```ts
import { createMock } from '@stratal/testing/mocks';

const mockEmailService = createMock<EmailService>();
mockEmailService.send.mockResolvedValueOnce(undefined);
```

Use with `overrideProvider(TOKEN).useValue(mockEmailService)`.

## Auth Testing (ActingAs)

```ts
import { ActingAs } from '@stratal/testing';

const actingAs = new ActingAs(module.get(AUTH_SERVICE));
const headers = await actingAs.createSessionForUser({ id: 'user-1' });
const response = await module.http
  .withHeaders(headers)
  .get('/api/v1/profile')
  .send();
```

## Database Testing

```ts
// Truncate tables between tests
await module.truncateDb();

// Seed test data
await module.seed(new UserSeeder());

// Database assertions
await module.assertDatabaseHas('user', { email: 'test@example.com' });
await module.assertDatabaseMissing('user', { email: 'deleted@example.com' });
await module.assertDatabaseCount('user', 5);
```

## Test Patterns

- Create module in `beforeEach`, call `module.close()` in `afterEach`
- Override external services (email, storage, external APIs) with mocks/fakes
- Use `module.runInRequestScope()` to test request-scoped services
- Use factories for test data, seeders for complex test setup
- Assert HTTP responses with fluent assertion chains
- Use `module.getDb()` for direct database access in tests
