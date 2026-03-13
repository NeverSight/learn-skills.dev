---
name: typescript:testing
description: TypeScript testing patterns with Vitest and MSW. Use when writing unit tests, mocking APIs, creating typed mocks for dependency injection, or using snapshot testing.
user-invocable: false
---

# TypeScript Testing Patterns

Comprehensive testing patterns using Vitest for unit testing, MSW for API mocking, and snapshot testing for complex object validation.

## Quick Start

### Installation

```bash
# Core testing dependencies
bun add -d vitest @vitest/ui

# MSW for API mocking
bun add -d msw

# Optional: coverage reporting
bun add -d @vitest/coverage-v8
```

### Basic Test Structure

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('UserService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('creates user with valid data', async () => {
    const result = await userService.create({ name: 'Alice' })
    expect(result).toMatchObject({ name: 'Alice' })
  })
})
```

## Typed Mock Objects

Create type-safe mocks for dependency injection using `vi.mocked()`:

```typescript
import { vi } from 'vitest'
import type { UserRepository } from './user-repository'

// Mock the entire module
vi.mock('./user-repository')

// Get typed mock instance
const mockUserRepo = vi.mocked<UserRepository>({
  findById: vi.fn(),
  save: vi.fn(),
  delete: vi.fn(),
})

// Type-safe mock return values
mockUserRepo.findById.mockResolvedValue({
  id: '123',
  name: 'Alice',
  email: 'alice@example.com',
})

// Assertions with full type safety
expect(mockUserRepo.findById).toHaveBeenCalledWith('123')
```

### Mock Return Values

```typescript
// Single return value
mockRepo.findById.mockResolvedValue(user)

// Multiple calls, different returns
mockRepo.findById
  .mockResolvedValueOnce(null)
  .mockResolvedValueOnce(user)

// Conditional logic
mockRepo.findById.mockImplementation(async (id) => {
  if (id === '123') return user
  return null
})

// Throw errors
mockRepo.save.mockRejectedValue(new Error('Database error'))
```

### Spy on Real Implementations

```typescript
import { vi } from 'vitest'
import { emailService } from './email-service'

// Spy on method without replacing it
vi.spyOn(emailService, 'send')

// Call real implementation
await emailService.send({ to: 'alice@example.com', subject: 'Test' })

// Assert it was called
expect(emailService.send).toHaveBeenCalledOnce()

// Temporarily override return value
emailService.send.mockResolvedValueOnce({ messageId: 'test-123' })
```

See [references/mocking.md](./references/mocking.md) for comprehensive mocking patterns including module mocks, class mocks, stateful handlers, and dependency injection.

## API Mocking with MSW

Mock HTTP requests at the network level for integration tests:

```typescript
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { afterAll, afterEach, beforeAll } from 'vitest'

// Define handlers
const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Alice',
      email: 'alice@example.com',
    })
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({ id: '123', ...body }, { status: 201 })
  }),
]

// Setup server
const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

See [references/msw.md](./references/msw.md) for advanced MSW patterns including error simulation, delays, and per-test overrides.

## Snapshot Testing

Validate complex objects and output without manual assertions:

```typescript
import { it, expect } from 'vitest'

it('generates correct user profile', () => {
  const profile = generateUserProfile(user)

  // Snapshot entire object
  expect(profile).toMatchSnapshot()
})

// Handle dynamic values (dates, IDs)
it('creates order with timestamp', () => {
  const order = createOrder(items)

  expect(order).toMatchSnapshot({
    id: expect.any(String),
    createdAt: expect.any(Date),
  })
})

// Inline snapshots for small objects
it('formats error message', () => {
  const error = formatError(new Error('Failed'))
  expect(error).toMatchInlineSnapshot(`
    {
      "message": "Failed",
      "code": "UNKNOWN_ERROR",
    }
  `)
})
```

See [references/snapshot-testing.md](./references/snapshot-testing.md) for snapshot maintenance, custom serializers, and best practices.

## Testing Async Code

```typescript
// Promises
it('loads user data', async () => {
  const user = await userService.findById('123')
  expect(user).toBeDefined()
})

// Callbacks
it('calls callback on completion', () => {
  return new Promise<void>((resolve) => {
    processData(data, (result) => {
      expect(result).toBe(expected)
      resolve()
    })
  })
})

// Timers
it('retries after delay', async () => {
  vi.useFakeTimers()

  const promise = retryOperation()
  vi.advanceTimersByTime(1000)

  const result = await promise
  expect(result).toBe('success')

  vi.useRealTimers()
})
```

## Test Organization

```typescript
// Group related tests
describe('UserService', () => {
  describe('create', () => {
    it('succeeds with valid data', () => {})
    it('throws on duplicate email', () => {})
  })

  describe('update', () => {
    it('updates existing user', () => {})
    it('throws on not found', () => {})
  })
})

// Shared setup
describe('authenticated requests', () => {
  beforeEach(() => {
    mockAuth.isAuthenticated.mockReturnValue(true)
  })

  it('allows user creation', () => {})
  it('allows user deletion', () => {})
})
```

## Guidelines

1. **Test behavior, not implementation** - Focus on what the code does, not how it does it
2. **One assertion per test when possible** - Makes failures clearer and tests more focused
3. **Use typed mocks** - `vi.mocked<T>()` provides type safety for mock setup and assertions
4. **Mock at boundaries** - Mock external dependencies (APIs, databases), not internal functions
5. **Use MSW for API tests** - Mock at the network level for realistic integration tests
6. **Snapshots for complex output** - Use snapshots for large objects, explicit assertions for critical values
7. **Property matchers for dynamic values** - Handle dates, IDs, timestamps with `expect.any()`
8. **Clear test names** - Describe the scenario and expected outcome: "creates user with valid data"
9. **Setup/teardown for state** - Use `beforeEach`/`afterEach` to ensure test isolation
10. **Async/await over callbacks** - Prefer `async`/`await` for cleaner async test code
11. **Fake timers for time-based code** - Use `vi.useFakeTimers()` to control time in tests
12. **Test error cases** - Verify error handling with `expect().rejects.toThrow()`

## Related Skills

- **build-tools** - Vitest configuration, test scripts, coverage setup
- **api-design** - Testing REST API contracts and error responses
- **fastify** - Testing Fastify routes and plugins
- **drizzle-orm** - Testing database queries (use MSW or in-memory DB)
- **dynamodb-toolbox** - Testing DynamoDB entities and queries

## Common Patterns

### Testing with Dependency Injection

```typescript
class UserService {
  constructor(
    private repo: UserRepository,
    private email: EmailService,
  ) {}

  async create(data: CreateUserInput) {
    const user = await this.repo.save(data)
    await this.email.sendWelcome(user.email)
    return user
  }
}

// Test with mocks
it('sends welcome email on create', async () => {
  const mockRepo = vi.mocked<UserRepository>({
    save: vi.fn().mockResolvedValue(savedUser),
  })
  const mockEmail = vi.mocked<EmailService>({
    sendWelcome: vi.fn().mockResolvedValue(undefined),
  })

  const service = new UserService(mockRepo, mockEmail)
  await service.create(userData)

  expect(mockEmail.sendWelcome).toHaveBeenCalledWith('alice@example.com')
})
```

### Testing Error Boundaries

```typescript
it('handles repository errors gracefully', async () => {
  mockRepo.save.mockRejectedValue(new Error('Database error'))

  await expect(
    service.create(userData)
  ).rejects.toThrow('Failed to create user')

  // Verify cleanup or rollback occurred
  expect(mockEmail.sendWelcome).not.toHaveBeenCalled()
})
```

### Testing Race Conditions

```typescript
it('handles concurrent requests correctly', async () => {
  const promises = [
    service.processOrder(order1),
    service.processOrder(order2),
    service.processOrder(order3),
  ]

  const results = await Promise.all(promises)

  expect(results).toHaveLength(3)
  expect(new Set(results.map(r => r.id)).size).toBe(3)
})
```

## Debugging Tests

```bash
# Run single test file
vitest run path/to/test.spec.ts

# Run tests matching pattern
vitest run -t "creates user"

# Watch mode for TDD
vitest watch

# UI mode for debugging
vitest --ui

# Coverage report
vitest run --coverage
```
