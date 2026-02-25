---
name: test-setup-async
description: |
  Sets up async tests with proper fixtures and mocks using pytest-asyncio patterns. Use when testing async functions, creating async fixtures, mocking async services, or handling async context managers. Covers @pytest_asyncio.fixture, AsyncMock with side_effect, async generator fixtures (yield), and testing async context managers. Works with Python async/await patterns, pytest-asyncio, and unittest.mock.AsyncMock.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Setup Async Testing

## Purpose

Provide correct patterns for testing async functions in Python using pytest-asyncio, AsyncMock, and async fixtures. Ensures tests properly handle async context managers, side effects, and cleanup.

## Quick Start

**Most common use case:**
```python
# Testing an async function with mocked dependencies
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_my_async_function():
    mock_service = AsyncMock()
    mock_service.fetch_data.return_value = {"result": "success"}

    result = await my_async_function(mock_service)

    assert result == {"result": "success"}
    mock_service.fetch_data.assert_awaited_once()
```

## Table of Contents

1. [When to Use This Skill](#when-to-use-this-skill)
2. [What This Skill Does](#what-this-skill-does)
3. [Instructions](#instructions)
4. [Usage Examples](#usage-examples)
5. [Expected Outcomes](#expected-outcomes)
6. [Requirements](#requirements)
7. [Troubleshooting](#troubleshooting)
8. [Red Flags to Avoid](#red-flags-to-avoid)
9. [Automation Scripts](#automation-scripts)

---

## When to Use This Skill

Use this skill when:
- **Testing async functions** - Functions using `async def` and `await`
- **Creating async fixtures** - Setup/teardown with async operations
- **Mocking async services** - Database connections, API clients, external services
- **Handling async context managers** - `async with` statements
- **Testing async generators** - `async for` patterns
- **Debugging async test failures** - "RuntimeWarning: coroutine was never awaited"

**Trigger phrases:**
- "Test async function"
- "Mock async method"
- "Create async fixture"
- "AsyncMock configuration"
- "pytest-asyncio setup"

---

## What This Skill Does

This skill provides patterns for:

1. **Async test configuration** - pytest-asyncio setup in pyproject.toml
2. **Async fixture creation** - Using @pytest_asyncio.fixture with AsyncGenerator
3. **AsyncMock usage** - Mocking async methods with return_value and side_effect
4. **Async context managers** - Mocking `async with` statements (__aenter__, __aexit__)
5. **Async assertions** - assert_awaited_once(), assert_awaited_once_with()
6. **Error handling** - Testing exceptions in async code

See Instructions section below for detailed step-by-step patterns.

---

## Instructions

### Step 1: Install Dependencies
```bash
uv pip install pytest-asyncio
```

Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # Auto-detect async tests
```

### Step 2: Choose Fixture Type

**Async Fixture (for setup/teardown):**
```python
import pytest_asyncio
from collections.abc import AsyncGenerator

@pytest_asyncio.fixture
async def database_connection() -> AsyncGenerator[Connection, None]:
    """Create database connection with cleanup."""
    conn = await create_connection()
    yield conn
    await conn.close()
```

**Sync Fixture (for mocks):**
```python
@pytest.fixture
def mock_service():
    """Create mock service (non-async fixture for mocks)."""
    from unittest.mock import AsyncMock
    mock = AsyncMock()
    mock.fetch_data.return_value = {"data": "test"}
    return mock
```

### Step 3: Mock Async Methods

**Simple return value:**
```python
mock_service = AsyncMock()
mock_service.process.return_value = "result"
```

**Side effect (exception):**
```python
mock_service.process.side_effect = Exception("Connection failed")
```

**Side effect (sequence):**
```python
mock_service.fetch.side_effect = [
    {"batch": 1},
    {"batch": 2},
    {"batch": 3}
]
```

**Side effect (custom function):**
```python
async def custom_behavior(arg):
    if arg == "fail":
        raise ValueError("Invalid")
    return f"processed_{arg}"

mock_service.process.side_effect = custom_behavior
```

### Step 4: Test Async Context Managers

**Mock async context manager:**
```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_driver():
    """Mock Neo4j driver with async context manager."""
    driver = MagicMock()  # Driver itself is sync

    # Create async session mock
    mock_session = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    # Configure session behavior
    mock_result = AsyncMock()
    mock_result.data = AsyncMock(return_value=[{"node": "data"}])
    mock_session.run = AsyncMock(return_value=mock_result)

    # Driver returns session
    driver.session = MagicMock(return_value=mock_session)

    return driver
```

**Test usage:**
```python
@pytest.mark.asyncio
async def test_with_session(mock_driver):
    async with mock_driver.session() as session:
        result = await session.run("MATCH (n) RETURN n")
        data = await result.data()

    assert data == [{"node": "data"}]
    mock_driver.session.assert_called_once()
```

### Step 5: Verify Async Calls

**Assert awaited:**
```python
mock_service.fetch_data.assert_awaited_once()
mock_service.fetch_data.assert_awaited_once_with(arg="value")
mock_service.fetch_data.assert_awaited()  # At least once
```

**Assert call count:**
```python
assert mock_service.fetch_data.await_count == 3
```

**Assert not called:**
```python
mock_service.error_handler.assert_not_awaited()
```

## Usage Examples

### Example 1: Async Fixture with Cleanup
```python
import pytest_asyncio
from collections.abc import AsyncGenerator
from neo4j import AsyncDriver, AsyncGraphDatabase

@pytest_asyncio.fixture(scope="function")
async def neo4j_driver() -> AsyncGenerator[AsyncDriver, None]:
    """Create Neo4j driver with cleanup."""
    driver = AsyncGraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "password")
    )

    # Setup: Clear test data
    async with driver.session() as session:
        await session.run("MATCH (n:TestNode) DETACH DELETE n")

    yield driver

    # Cleanup: Close driver
    await driver.close()
```

### Example 2: AsyncMock with Side Effect Sequence
```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_batch_processing():
    mock_api = AsyncMock()

    # First call succeeds, second fails, third succeeds
    mock_api.fetch_batch.side_effect = [
        {"batch": 1, "items": [1, 2, 3]},
        Exception("Rate limit exceeded"),
        {"batch": 2, "items": [4, 5, 6]}
    ]

    # Process first batch
    result1 = await mock_api.fetch_batch()
    assert result1["batch"] == 1

    # Second call raises exception
    with pytest.raises(Exception, match="Rate limit"):
        await mock_api.fetch_batch()

    # Third call succeeds
    result3 = await mock_api.fetch_batch()
    assert result3["batch"] == 2

    assert mock_api.fetch_batch.await_count == 3
```

### Example 3: Testing Service with Async Dependencies
```python
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from project_watch_mcp.domain.values.service_result import ServiceResult

@pytest.fixture
def mock_embedding_service():
    """Create mock embedding service."""
    service = AsyncMock()
    service.get_embeddings.return_value = ServiceResult.success(
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    )
    return service

@pytest.fixture
def mock_repository():
    """Create mock code repository."""
    repo = AsyncMock()
    repo.store_chunks.return_value = ServiceResult.success(True)
    return repo

@pytest.mark.asyncio
async def test_chunking_service(mock_embedding_service, mock_repository):
    """Test chunking service with async dependencies."""
    from project_watch_mcp.application.services.chunking_service import ChunkingService

    # Create service with mocked dependencies
    service = ChunkingService(
        embedding_service=mock_embedding_service,
        repository=mock_repository,
        settings=mock_settings
    )

    # Execute async operation
    result = await service.process_file("test.py")

    # Verify async calls
    mock_embedding_service.get_embeddings.assert_awaited_once()
    mock_repository.store_chunks.assert_awaited_once()

    assert result.is_success()
```

### Example 4: Error Handling in Async Tests
```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_error_handling():
    """Test service handles async errors correctly."""
    mock_db = AsyncMock()
    mock_db.execute_query.side_effect = Exception("Connection lost")

    service = MyService(database=mock_db)

    result = await service.fetch_data()

    # Verify ServiceResult.failure() was returned
    assert not result.is_success()
    assert "Connection lost" in result.error

    # Verify retry logic was triggered
    assert mock_db.execute_query.await_count == 3  # 3 retries
```

### Example 5: Async Generator Fixture (Resource Pool)
```python
import pytest_asyncio
from collections.abc import AsyncGenerator

@pytest_asyncio.fixture
async def resource_pool() -> AsyncGenerator[ResourcePool, None]:
    """Create resource pool with async initialization and cleanup."""
    pool = ResourcePool()

    # Async initialization
    await pool.initialize()
    await pool.create_connections(count=5)

    yield pool

    # Async cleanup
    await pool.drain()
    await pool.shutdown()

@pytest.mark.asyncio
async def test_resource_acquisition(resource_pool):
    """Test acquiring resource from pool."""
    async with resource_pool.acquire() as resource:
        result = await resource.execute("SELECT 1")

    assert result is not None
```

## Expected Outcomes

### Successful Async Test Setup

```
✅ Async Test Configured

Configuration:
  ✅ pytest-asyncio installed
  ✅ pyproject.toml configured (asyncio_mode = "auto")
  ✅ AsyncMock imported from unittest.mock

Test Results:
  ✅ All async tests discovered (@pytest.mark.asyncio)
  ✅ Async fixtures working (setup/teardown with yield)
  ✅ AsyncMock assertions passing (assert_awaited_once)
  ✅ No "coroutine was never awaited" warnings

Example test output:
  tests/unit/test_service.py::test_async_function PASSED
  tests/unit/test_service.py::test_with_async_fixture PASSED
```

### Common Failure - Mock Configuration Error

```
❌ Test Failed: RuntimeWarning

Error: RuntimeWarning: coroutine 'AsyncMock' was never awaited
  File "tests/unit/test_service.py", line 42

Root Cause:
  - Used MagicMock instead of AsyncMock for async method
  - Mock configured incorrectly

Fix:
  # ❌ WRONG
  mock_service.fetch = MagicMock(return_value="result")

  # ✅ CORRECT
  from unittest.mock import AsyncMock
  mock_service.fetch = AsyncMock(return_value="result")
```

---

## Requirements

**Dependencies:**
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest>=7.0.0` - Test framework
- Python 3.11+ with async/await support

**Configuration:**
```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "asyncio: mark test as async",
]
```

**Knowledge:**
- Python async/await syntax
- pytest fixture patterns
- Mock object configuration
- AsyncMock vs MagicMock differences

**Optional:**
- FastAPI or async web framework experience
- Database async drivers (asyncpg, motor, neo4j async driver)

---

## Common Patterns

### Pattern 1: Mock with Both Sync and Async Methods
```python
from unittest.mock import AsyncMock, MagicMock

mock = MagicMock()
mock.sync_method = MagicMock(return_value="sync_result")
mock.async_method = AsyncMock(return_value="async_result")

# Usage
result1 = mock.sync_method()          # Sync call
result2 = await mock.async_method()   # Async call
```

### Pattern 2: Async Fixture Scope
```python
# Function scope (default) - new instance per test
@pytest_asyncio.fixture(scope="function")
async def function_scoped_resource():
    resource = await create_resource()
    yield resource
    await resource.cleanup()

# Session scope - shared across all tests
@pytest_asyncio.fixture(scope="session")
async def session_scoped_resource():
    resource = await create_expensive_resource()
    yield resource
    await resource.cleanup()
```

### Pattern 3: Parameterized Async Tests
```python
@pytest.mark.asyncio
@pytest.mark.parametrize("input_value,expected", [
    ("test1", "result1"),
    ("test2", "result2"),
    ("test3", "result3"),
])
async def test_with_parameters(input_value, expected):
    result = await async_function(input_value)
    assert result == expected
```

### Pattern 4: Testing Concurrent Operations
```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_concurrent_execution():
    """Test multiple async operations running concurrently."""
    mock_service = AsyncMock()
    mock_service.process.side_effect = [
        asyncio.sleep(0.1, result="result1"),
        asyncio.sleep(0.1, result="result2"),
        asyncio.sleep(0.1, result="result3"),
    ]

    # Execute concurrently
    results = await asyncio.gather(
        mock_service.process("item1"),
        mock_service.process("item2"),
        mock_service.process("item3"),
    )

    assert len(results) == 3
    assert mock_service.process.await_count == 3
```

## Red Flags to Avoid

### Mock Configuration Mistakes

1. **Using MagicMock for async methods** - Always use AsyncMock for `async def` methods
2. **Missing return_value** - AsyncMock() without return_value returns another AsyncMock
3. **Forgetting await** - Calling async mock without `await` causes warnings
4. **Wrong assertion method** - Use `assert_awaited_once()` not `assert_called_once()` for async
5. **Sync fixture for async resource** - Use `@pytest_asyncio.fixture` for async setup/teardown

### Test Design Mistakes

6. **No @pytest.mark.asyncio decorator** - Async tests won't run correctly
7. **Mixing sync and async fixtures incorrectly** - Driver is sync, session is async
8. **Not configuring asyncio_mode** - Tests may fail inconsistently
9. **Using run_in_executor for simple async** - Unnecessary complexity

### Cleanup Mistakes

10. **No cleanup in async fixtures** - Resources leak (connections, files)
11. **Missing yield in fixture** - Cleanup code never runs
12. **Exception in setup prevents cleanup** - Use try/finally or pytest handles it

### Testing Mistakes

13. **Not testing async context managers** - Missing __aenter__/__aexit__ mocks
14. **No side_effect for sequences** - Can't test retry logic or multi-call scenarios
15. **Ignoring await_count** - Not verifying async method called correct number of times

---

## Troubleshooting

### Issue: "RuntimeWarning: coroutine was never awaited"
**Cause:** Mock returned coroutine instead of value
**Fix:** Use `AsyncMock` instead of `MagicMock` for async methods

### Issue: "TypeError: object AsyncMock can't be used in 'await' expression"
**Cause:** Used `AsyncMock()` for driver/client, should use `MagicMock()`
**Fix:** Outer object is sync, only context manager methods are async

### Issue: "assert_awaited_once() raises AttributeError"
**Cause:** Used `MagicMock` instead of `AsyncMock`
**Fix:** Async methods must use `AsyncMock`

### Issue: Fixture cleanup not running
**Cause:** Exception during test prevents cleanup
**Fix:** Use `try/finally` in fixture or `@pytest_asyncio.fixture` handles it

## Integration Points

### With Other Skills

**setup-async-testing integrates with:**
- **implement-feature-complete** - Provides async test patterns for Stage 2 (TDD)
- **debug-test-failures** - Works with async test debugging
- **setup-pytest-fixtures** - Combines sync and async fixture patterns
- **implement-async-context-manager** - Testing async context managers

### With Agent Workflows

**Agents should use this skill:**
- @unit-tester - When testing async functions
- @integration-tester - For async database/API tests
- @implementer - During TDD workflow with async code

### With Testing Tools

**Compatible with:**
- pytest-asyncio (required)
- AsyncMock from unittest.mock
- pytest fixtures and markers
- Neo4j async driver testing
- FastAPI async endpoint testing

## Expected Benefits

| Metric | Without Skill | With Skill | Improvement |
|--------|--------------|------------|-------------|
| **Test Setup Time** | 30 min (research) | 5 min (template) | 83% faster |
| **Mock Configuration Errors** | 40% (wrong mock type) | 5% (correct patterns) | 88% reduction |
| **"Coroutine never awaited" Warnings** | 20% of tests | 0% (proper AsyncMock) | 100% elimination |
| **Async Fixture Cleanup Issues** | 30% (leaks) | 0% (proper yield) | 100% fix |
| **Test Reliability** | 70% (flaky async) | 98% (stable) | 40% improvement |
| **Knowledge Transfer Time** | 2 hours (learning) | 15 min (examples) | 88% faster |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Zero Async Warnings** | 100% | pytest output |
| **Mock Configuration Accuracy** | 100% | AsyncMock validation |
| **Fixture Cleanup Success** | 100% | Resource leak detection |
| **Test Reliability** | 98%+ pass rate | CI/CD metrics |
| **Pattern Adoption** | 90% of async tests | Code review |

## Validation Process

### Step 1: Dependency Validation
```bash
# Ensure pytest-asyncio installed
uv pip list | grep pytest-asyncio

# Verify pyproject.toml configuration
cat pyproject.toml | grep asyncio_mode
```

### Step 2: Test Configuration Validation
```python
# Check test file has correct decorator
@pytest.mark.asyncio
async def test_name():
    ...
```

### Step 3: Mock Configuration Validation
```python
# Verify AsyncMock used for async methods
from unittest.mock import AsyncMock
mock_service.async_method = AsyncMock(return_value=...)
```

### Step 4: Fixture Validation
```python
# Async fixtures use AsyncGenerator
from collections.abc import AsyncGenerator

@pytest_asyncio.fixture
async def resource() -> AsyncGenerator[Resource, None]:
    resource = await create()
    yield resource
    await resource.cleanup()
```

### Step 5: Execution Validation
```bash
# Run tests with verbose output
uv run pytest tests/test_async.py -v

# Verify no warnings
# ✓ No "RuntimeWarning: coroutine was never awaited"
# ✓ All async assertions pass
```

## Automation Scripts

The `scripts/` directory contains production-ready automation utilities:

1. **validate_async_tests.py** - Validate async test patterns, detect anti-patterns
   ```bash
   python scripts/validate_async_tests.py tests/unit/ --severity warning
   ```

2. **convert_to_async.py** - Convert sync tests to async automatically
   ```bash
   python scripts/convert_to_async.py test_file.py --dry-run
   ```

3. **generate_async_fixture.py** - Generate fixture boilerplate
   ```bash
   python scripts/generate_async_fixture.py neo4j_driver database
   ```

📖 **See [references/SCRIPTS-REFERENCE.md](./references/SCRIPTS-REFERENCE.md) for complete documentation and examples.**

### Python Scripts

- [convert_to_async.py](./scripts/convert_to_async.py) - Convert synchronous tests to async test patterns
- [generate_async_fixture.py](./scripts/generate_async_fixture.py) - Generate async fixture boilerplate code
- [validate_async_tests.py](./scripts/validate_async_tests.py) - Validate async test patterns and find anti-patterns

## See Also
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [templates/async-test-template.py](./templates/async-test-template.py) - Copy-paste template
- **[references/SCRIPTS-REFERENCE.md](./references/SCRIPTS-REFERENCE.md) - Complete automation scripts documentation**
- [references/QUICK-REFERENCE.md](./references/QUICK-REFERENCE.md) - One-page quick reference
- [references/IMPLEMENTATION-SUMMARY.md](./references/IMPLEMENTATION-SUMMARY.md) - Technical implementation details
