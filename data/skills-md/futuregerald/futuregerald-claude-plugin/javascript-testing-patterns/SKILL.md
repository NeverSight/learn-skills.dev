---
name: javascript-testing-patterns
description: Comprehensive JavaScript/TypeScript testing patterns for Jest, Vitest, and AdonisJS/Japa. Use when writing tests, reviewing test code, or debugging test failures.
tags: [testing, javascript]
---

# JavaScript Testing Patterns

Comprehensive testing patterns for modern JavaScript/TypeScript applications.

## Core Principle: AAA Pattern

Every test follows **Arrange, Act, Assert**:

```typescript
test('calculates total with discount', () => {
  // Arrange - Set up test data
  const cart = { items: [{ price: 100 }], discount: 0.1 }

  // Act - Execute the code under test
  const total = calculateTotal(cart)

  // Assert - Verify the result
  expect(total).toBe(90)
})
```

---

## Framework Quick Reference

| Framework     | Run Tests       | Watch Mode            | Coverage                   |
| ------------- | --------------- | --------------------- | -------------------------- |
| Jest          | `npm test`      | `npm test -- --watch` | `npm test -- --coverage`   |
| Vitest        | `npx vitest`    | `npx vitest --watch`  | `npx vitest --coverage`    |
| AdonisJS/Japa | `node ace test` | N/A                   | `node ace test --coverage` |

---

## Part 1: Jest/Vitest Patterns

### Configuration

**Jest (jest.config.js)**

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
  setupFilesAfterEnv: ['./jest.setup.ts'],
}
```

**Vitest (vitest.config.ts)**

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: { provider: 'v8', reporter: ['text', 'json', 'html'] },
  },
})
```

### Unit Testing Pure Functions

```typescript
import { describe, it, expect } from 'vitest' // or jest

describe('calculateDiscount', () => {
  it('returns 0 for amounts below threshold', () => {
    expect(calculateDiscount(50)).toBe(0)
  })

  it('applies 10% discount for amounts over 100', () => {
    expect(calculateDiscount(200)).toBe(20)
  })

  it('handles edge case at threshold', () => {
    expect(calculateDiscount(100)).toBe(0)
    expect(calculateDiscount(100.01)).toBeCloseTo(10.001)
  })

  it('throws for negative amounts', () => {
    expect(() => calculateDiscount(-50)).toThrow('Amount cannot be negative')
  })
})
```

### Testing Classes

```typescript
describe('UserService', () => {
  let service: UserService

  beforeEach(() => {
    service = new UserService()
  })

  it('creates user with valid data', async () => {
    const user = await service.create({ email: 'test@example.com', name: 'Test' })

    expect(user.id).toBeDefined()
    expect(user.email).toBe('test@example.com')
  })

  it('throws for duplicate email', async () => {
    await service.create({ email: 'test@example.com', name: 'First' })

    await expect(service.create({ email: 'test@example.com', name: 'Second' })).rejects.toThrow(
      'Email already exists'
    )
  })
})
```

### Mocking Strategies

**Module Mocking**

```typescript
import { vi, describe, it, expect, beforeEach } from 'vitest'
import { sendEmail } from './email-service'
import { UserService } from './user-service'

vi.mock('./email-service', () => ({
  sendEmail: vi.fn().mockResolvedValue({ sent: true }),
}))

describe('UserService with mocked email', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('sends welcome email on registration', async () => {
    const service = new UserService()
    await service.register({ email: 'new@test.com' })

    expect(sendEmail).toHaveBeenCalledWith({
      to: 'new@test.com',
      template: 'welcome',
    })
  })
})
```

**Dependency Injection (Preferred)**

```typescript
interface EmailSender {
  send(to: string, template: string): Promise<void>
}

class UserService {
  constructor(private emailSender: EmailSender) {}

  async register(data: { email: string }) {
    // ... create user
    await this.emailSender.send(data.email, 'welcome')
  }
}

// In tests - easy to mock
describe('UserService', () => {
  it('sends welcome email', async () => {
    const mockSender = { send: vi.fn().mockResolvedValue(undefined) }
    const service = new UserService(mockSender)

    await service.register({ email: 'test@example.com' })

    expect(mockSender.send).toHaveBeenCalledWith('test@example.com', 'welcome')
  })
})
```

**Spying on Methods**

```typescript
it('logs errors to console', async () => {
  const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

  await service.handleError(new Error('test error'))

  expect(consoleSpy).toHaveBeenCalledWith('Error occurred:', expect.any(Error))
  consoleSpy.mockRestore()
})
```

### Async Testing

```typescript
describe('API client', () => {
  it('fetches data successfully', async () => {
    const data = await fetchUser(123)
    expect(data.id).toBe(123)
  })

  it('handles timeout', async () => {
    vi.useFakeTimers()

    const promise = fetchWithTimeout('/slow-endpoint', 1000)
    vi.advanceTimersByTime(1500)

    await expect(promise).rejects.toThrow('Request timeout')
    vi.useRealTimers()
  })

  it('retries on failure', async () => {
    const mockFetch = vi
      .fn()
      .mockRejectedValueOnce(new Error('Network error'))
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValueOnce({ data: 'success' })

    const result = await fetchWithRetry(mockFetch, 3)

    expect(result.data).toBe('success')
    expect(mockFetch).toHaveBeenCalledTimes(3)
  })
})
```

### Integration Testing with Supertest

```typescript
import request from 'supertest'
import { app } from '../app'
import { db } from '../database'

describe('POST /api/users', () => {
  beforeAll(async () => {
    await db.migrate.latest()
  })

  afterEach(async () => {
    await db('users').truncate()
  })

  afterAll(async () => {
    await db.destroy()
  })

  it('creates user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'secure123' })
      .expect(201)

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      email: 'test@example.com',
    })
  })

  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', password: 'secure123' })
      .expect(400)

    expect(response.body.errors).toContainEqual(expect.objectContaining({ field: 'email' }))
  })
})
```

### React Component Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    await userEvent.type(screen.getByLabelText('Email'), 'test@example.com')
    await userEvent.type(screen.getByLabelText('Password'), 'password123')
    await userEvent.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      })
    })
  })

  it('shows validation error for empty email', async () => {
    render(<LoginForm onSubmit={vi.fn()} />)

    await userEvent.click(screen.getByRole('button', { name: /login/i }))

    expect(screen.getByText('Email is required')).toBeInTheDocument()
  })

  it('disables submit button while loading', async () => {
    render(<LoginForm onSubmit={vi.fn()} isLoading />)

    expect(screen.getByRole('button', { name: /login/i })).toBeDisabled()
  })
})
```

### Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(6)
  })

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10))

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(10)
  })
})
```

### Test Factories with Faker

```typescript
import { faker } from '@faker-js/faker'

// factories/user.ts
export const createTestUser = (overrides = {}) => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  createdAt: faker.date.past(),
  ...overrides
})

export const createTestUsers = (count: number, overrides = {}) =>
  Array.from({ length: count }, () => createTestUser(overrides))

// In tests
describe('UserList', () => {
  it('displays all users', () => {
    const users = createTestUsers(5)
    render(<UserList users={users} />)

    users.forEach(user => {
      expect(screen.getByText(user.name)).toBeInTheDocument()
    })
  })
})
```

---

## Part 2: AdonisJS/Japa Patterns

### Running Tests

```bash
# Run all tests
node ace test

# Run specific suite
node ace test functional
node ace test unit

# Run specific file
node ace test functional --files="user_auth"

# Run with coverage
node ace test --coverage
```

### Test Structure

```typescript
import { test } from '@japa/runner'

test.group('Feature | Description', (group) => {
  group.each.setup(() => {
    // runs before each test
  })

  group.each.teardown(() => {
    // runs after each test
  })

  test('specific behavior', async ({ assert }) => {
    const result = someFunction()
    assert.equal(result, expected)
  })
})
```

### Database Testing with Transactions

```typescript
import { test } from '@japa/runner'
import testUtils from '@adonisjs/core/services/test_utils'
import User from '#models/user'

test.group('Database tests', (group) => {
  // Wrap each test in a transaction that rolls back
  group.each.setup(() => testUtils.db().withGlobalTransaction())

  test('creates a record', async ({ assert }) => {
    const user = await User.create({ email: 'test@example.com' })
    assert.isNotNull(user.id)
    // Transaction rolls back - no cleanup needed
  })
})
```

### HTTP Testing

**Basic Request**

```typescript
test.group('API | Users', (group) => {
  group.each.setup(() => testUtils.db().withGlobalTransaction())

  test('GET /users returns list', async ({ client, assert }) => {
    const response = await client.get('/users')

    response.assertStatus(200)
    assert.isArray(response.body())
  })
})
```

**Authenticated Requests**

```typescript
test('authenticated endpoint', async ({ client }) => {
  const user = await User.create({
    /* ... */
  })

  // Web session auth
  const response = await client.get('/dashboard').loginAs(user)

  // API token auth
  const apiResponse = await client.get('/api/v1/me').loginAs(user, 'api')

  response.assertStatus(200)
})
```

**Testing Redirects**

```typescript
test('redirects after action', async ({ client }) => {
  const user = await User.create({
    /* ... */
  })

  const response = await client
    .post('/logout')
    .redirects(0) // Don't follow redirects
    .loginAs(user)

  response.assertStatus(302)
  response.assertHeader('location', '/login')
})
```

**Form and JSON Submissions**

```typescript
// Form data
const response = await client
  .post('/posts')
  .form({ title: 'My Post', description: 'A test post' })
  .loginAs(user)

// JSON API
const response = await client
  .post('/api/v1/posts')
  .json({ title: 'My Post', description: 'A test post' })
  .loginAs(user, 'api')

// AJAX request
const response = await client
  .post('/comments')
  .header('X-Requested-With', 'XMLHttpRequest')
  .form({ content: 'Test comment' })
  .loginAs(user)
```

### Japa Assertions

```typescript
test('assertions example', async ({ assert }) => {
  // Equality
  assert.equal(actual, expected)
  assert.deepEqual(obj1, obj2)

  // Truthiness
  assert.isTrue(value)
  assert.isFalse(value)
  assert.isNull(value)
  assert.isNotNull(value)

  // Types
  assert.isString(value)
  assert.isArray(value)
  assert.isObject(value)

  // Arrays/Objects
  assert.lengthOf(array, 3)
  assert.include(array, item)
  assert.property(obj, 'key')
  assert.containsSubset(obj, { key: 'value' })

  // Exceptions
  assert.throws(() => throwingFn(), Error)
  await assert.rejects(async () => asyncThrowingFn(), Error)
})
```

### Response Assertions

```typescript
response.assertStatus(200)
response.assertHeader('content-type', 'application/json')
response.assertHeader('location', '/dashboard')
response.assertBody({ success: true })
response.assertBodyContains({ id: 1 })
response.assertTextIncludes('Welcome')
```

### Testing with Sinon Mocks

```typescript
import sinon from 'sinon'
import EmailService from '#services/email_service'

test.group('With mocks', (group) => {
  group.each.teardown(() => {
    sinon.restore()
  })

  test('sends email on registration', async ({ assert }) => {
    const sendStub = sinon.stub(EmailService, 'send').resolves()

    await UserService.register({ email: 'test@example.com' })

    assert.isTrue(sendStub.calledOnce)
    assert.equal(sendStub.firstCall.args[0], 'test@example.com')
  })
})
```

### Common Test Patterns

**Auth Required Routes**

```typescript
test('requires authentication', async ({ client }) => {
  const response = await client.get('/dashboard').redirects(0)
  response.assertStatus(302)
  response.assertHeader('location', '/login')
})

test('API returns 401 without auth', async ({ client }) => {
  const response = await client.get('/api/v1/me')
  response.assertStatus(401)
})
```

**Validation Errors**

```typescript
test('validates required fields', async ({ client }) => {
  const user = await User.create({
    /* ... */
  })

  const response = await client.post('/api/v1/posts').json({}).loginAs(user, 'api')

  response.assertStatus(422)
  response.assertBodyContains({ code: 'E_VALIDATION' })
})
```

**Authorization**

```typescript
test('denies access to other user resources', async ({ client }) => {
  const owner = await User.create({ email: 'owner@test.com' })
  const other = await User.create({ email: 'other@test.com' })
  const resource = await Resource.create({ ownerId: owner.id })

  const response = await client
    .patch(`/api/v1/resources/${resource.id}`)
    .json({ title: 'Hacked' })
    .loginAs(other, 'api')

  response.assertStatus(403)
})
```

---

## Anti-Patterns to Avoid

### Don't Test Implementation Details

```typescript
// BAD
test('calls internal method', async () => {
  const spy = vi.spyOn(service, '_internalHelper')
  await service.doThing()
  expect(spy).toHaveBeenCalled()
})

// GOOD - Test observable behavior
test('produces correct output', async () => {
  const result = await service.doThing()
  expect(result).toEqual(expected)
})
```

### Don't Over-Mock

```typescript
// BAD - Testing mock, not real code
test('calls database', async () => {
  const mockDb = { query: vi.fn().mockResolvedValue([]) }
  const service = new UserService(mockDb)
  await service.getUsers()
  expect(mockDb.query).toHaveBeenCalled()
})

// GOOD - Test real behavior with test database
test('returns users from database', async () => {
  await User.create({ name: 'Test' })
  const users = await service.getUsers()
  expect(users).toHaveLength(1)
})
```

### Don't Forget Cleanup

```typescript
// BAD - Pollutes database
test.group('Tests', () => {
  test('creates record', async () => {
    await User.create({
      /* ... */
    }) // Persists!
  })
})

// GOOD - Uses transaction rollback
test.group('Tests', (group) => {
  group.each.setup(() => testUtils.db().withGlobalTransaction())

  test('creates record', async () => {
    await User.create({
      /* ... */
    }) // Rolls back
  })
})
```

---

## File Organization

```
tests/
├── functional/           # HTTP/integration tests
│   ├── auth.spec.ts
│   ├── users.spec.ts
│   └── api/
│       └── users.spec.ts
├── unit/                 # Unit tests
│   └── services/
│       └── user_service.spec.ts
├── factories/            # Test data factories
│   └── user.ts
└── bootstrap.ts          # Test setup
```

---

## Quick Reference

| Action         | Jest/Vitest                    | AdonisJS/Japa                  |
| -------------- | ------------------------------ | ------------------------------ |
| Run tests      | `npm test`                     | `node ace test`                |
| Run file       | `npm test -- path/to/file`     | `node ace test --files="name"` |
| Coverage       | `--coverage`                   | `--coverage`                   |
| Mock function  | `vi.fn()` / `jest.fn()`        | `sinon.stub()`                 |
| Spy            | `vi.spyOn()`                   | `sinon.spy()`                  |
| Auth request   | N/A (manual)                   | `.loginAs(user)`               |
| Don't redirect | N/A                            | `.redirects(0)`                |
| Form data      | `.send()`                      | `.form()`                      |
| JSON data      | `.send()`                      | `.json()`                      |
| Assert status  | `expect(res.status).toBe(200)` | `response.assertStatus(200)`   |
