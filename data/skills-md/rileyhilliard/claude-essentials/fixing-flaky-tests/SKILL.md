---
name: fixing-flaky-tests
description: Diagnose and fix tests that pass in isolation but fail when run concurrently. Covers shared state isolation and resource conflicts. References condition-based-waiting for timing issues.
---

# Fixing Flaky Tests

**Target symptom:** Tests pass when run alone, fail when run with other tests.

## Diagnose first

```
Test passes alone, fails with others?
    │
    ├─ Same error every time → Shared state
    │   └─ Database, globals, files, singletons
    │
    ├─ Random/timing failures → Race condition
    │   └─ Use `condition-based-waiting` skill
    │
    └─ Resource errors (port, file lock) → Resource conflict
        └─ Need unique resources per test/worker
```

**Quick diagnosis:**
1. Run failing test 10x alone - does it always pass?
2. Run failing test 10x with the suite - same error or different?
3. Check error message - mentions port/file/connection?

## Shared state (deterministic failures)

Tests pollute state that other tests depend on. Fix by isolating state per test.

| State Type | Isolation Pattern |
|------------|-------------------|
| **Database** | Transaction rollback, savepoints, worker-specific DBs |
| **Global variables** | Reset in `beforeEach`/`afterEach` |
| **Singletons** | Provide fresh instance per test |
| **Module state** | `jest.resetModules()` or equivalent |
| **Files** | Unique paths per test, temp directories |
| **Environment vars** | Save/restore in setup/teardown |

**Database isolation (most common):**

```python
# Python: Savepoint rollback - each test gets rolled back
@pytest.fixture
async def db_session(db_engine):
    async with db_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()  # Savepoint
        # ... yield session ...
        await conn.rollback()  # All changes vanish
```

```typescript
// Jest: Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks()
  jest.resetModules()  // Clear module cache before test
})

afterEach(() => {
  jest.restoreAllMocks()  // Restore spied functions
})
```

See language-specific references for complete patterns.

## Race conditions (random failures)

Tests don't wait for async operations to complete.

**Use the `condition-based-waiting` skill** for detailed patterns on:
- Framework-specific waiting (Testing Library `findBy`, Playwright auto-wait)
- Custom polling helpers
- When arbitrary timeouts are acceptable

**Quick summary:** Wait for conditions, not time:

```typescript
// Bad
await sleep(500)

// Good
await waitFor(() => expect(result).toBe('done'))
```

## Resource conflicts (port/file errors)

Multiple tests or workers compete for same resource.

**Worker-specific resources:**

```python
# Python pytest-xdist: unique DB per worker
@pytest.fixture(scope="session")
def database_url(worker_id):
    if worker_id == "master":
        return "postgresql://localhost/test"
    return f"postgresql://localhost/test_{worker_id}"
```

```typescript
// Jest/Node: dynamic port allocation
const server = app.listen(0)  // OS assigns available port
const port = server.address().port
```

**File conflicts:**

```python
import tempfile

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d
```

## Language-specific isolation patterns

| Stack | Reference |
|-------|-----------|
| Python (pytest, SQLAlchemy) | [references/python.md](references/python.md) |
| Jest / Testing Library | [references/jest.md](references/jest.md) |
| Playwright E2E | [references/playwright.md](references/playwright.md) |

## Verification

After fixing, verify the fix worked:

```bash
# Run the specific test many times
pytest tests/test_flaky.py -x --count=20

# Run with parallelism
pytest -n auto

# Jest equivalent
jest --runInBand  # First verify serial works
jest              # Then verify parallel works
```
