---
name: python-best-practices-async-context-manager
description: |
  Create async context managers for resource management using @asynccontextmanager decorator.
  Use when managing async resources, database sessions, file handles, connections, or any
  resource requiring automatic cleanup. Works with Python async/await patterns. Analyzes
  .py files with async with statements, AsyncIterator type hints, and try/finally patterns.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
---

# Implement Async Context Manager

## Purpose

Create async context managers for automatic resource lifecycle management (setup, use, cleanup) in async Python code using the `@asynccontextmanager` decorator pattern.


## When to Use This Skill

Use when managing async resources with "create context manager", "manage database session", "async with pattern", or "resource cleanup".

Do NOT use for synchronous resources (use regular context managers), simple try/finally (overkill), or testing (use pytest fixtures).
## When to Use

Use this skill when:
- Managing database sessions or connections (primary use case)
- Handling async file I/O operations requiring cleanup
- Managing network connections with automatic close
- Coordinating resource pools with acquire/release patterns
- Ensuring cleanup in async operations (preventing resource leaks)
- Converting synchronous context managers to async
- Implementing transaction management with automatic commit/rollback

## Quick Start

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def session(database: str) -> AsyncIterator[Session]:
    """Create a database session with automatic cleanup."""
    session = await create_session(database)
    try:
        yield session
    finally:
        await session.close()

# Usage
async with session("mydb") as s:
    await s.query("SELECT 1")
```

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Core purpose and when to use async context managers
- [Quick Start](#quick-start) - Minimal working example
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Identify Resource Management Needs](#step-1-identify-resource-management-needs) - When to use async context managers
  - [Step 2: Choose Implementation Pattern](#step-2-choose-implementation-pattern) - @asynccontextmanager vs __aenter__/__aexit__
  - [Step 3: Implement @asynccontextmanager Pattern](#step-3-implement-asynccontextmanager-pattern) - Primary implementation approach
  - [Step 4: Handle Error Cases](#step-4-handle-error-cases) - Comprehensive error handling patterns
  - [Step 5: Add Type Safety](#step-5-add-type-safety) - Type hints and generic patterns
  - [Step 6: Test Async Context Managers](#step-6-test-async-context-managers) - Testing strategies
- [Examples](#examples) - Production-ready implementations
  - [Example 1: Database Session Manager](#example-1-database-session-manager-primary-pattern) - Primary pattern from codebase
  - [Example 2: Resource Pool Manager](#example-2-resource-pool-manager) - Connection pool handling
  - [Example 3: Async File Manager](#example-3-async-file-manager) - File I/O with cleanup
- [Common Patterns](#common-patterns) - Reusable implementation patterns
  - [Pattern 1: State Tracking](#pattern-1-state-tracking) - Prevent double-cleanup
  - [Pattern 2: Statistics Tracking](#pattern-2-statistics-tracking) - Track active resources
  - [Pattern 3: Nested Context Managers](#pattern-3-nested-context-managers) - Composing context managers

### Project Integration
- [Integration with Project Patterns](#integration-with-project-patterns) - Clean Architecture, ServiceResult, Fail-Fast
- [Red Flags](#red-flags) - Common mistakes and best practices
- [Requirements](#requirements) - Dependencies and knowledge needed

### Supporting Resources
- [references/reference.md](./references/reference.md) - Technical details and advanced usage
- [templates/context-manager-template.py](./templates/context-manager-template.py) - Reusable template
- [Production Example](../../src/project_watch_mcp/infrastructure/neo4j/database.py) - Real-world implementation (line 517)

### Utility Scripts
- [Convert Sync to Async](./scripts/convert_sync_to_async_cm.py) - Automatically convert synchronous context managers to async
- [Generate Async Context Manager](./scripts/generate_async_context_manager.py) - Generate properly structured async context managers from template
- [Validate Context Managers](./scripts/validate_context_managers.py) - Check codebase for common anti-patterns and missing best practices

## Instructions

### Step 1: Identify Resource Management Needs

Async context managers are needed when:
- Managing database sessions/connections
- Handling file I/O with async operations
- Managing network connections
- Coordinating resource pools
- Ensuring cleanup in async operations

**Evidence from codebase**: 38 occurrences of `async with` patterns indicate resource management needs.

### Step 2: Choose Implementation Pattern

**Option A: @asynccontextmanager (Recommended)**
- Use for simple resource management
- Cleaner syntax with single function
- Automatic `__aenter__`/`__aexit__` generation
- Better for one-off context managers

**Option B: __aenter__/__aexit__ methods**
- Use for complex classes with state
- More control over lifecycle
- Better for reusable context manager classes

### Step 3: Implement @asynccontextmanager Pattern

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import TypeVar

T = TypeVar("T")

@asynccontextmanager
async def resource_manager(
    config: Config,
    resource_id: str
) -> AsyncIterator[Resource]:
    """Manage resource lifecycle with automatic cleanup.

    Args:
        config: Configuration for resource creation (required)
        resource_id: Unique identifier for resource

    Yields:
        Resource: Active resource instance

    Raises:
        ValueError: If config is None
        ResourceError: If resource creation fails
    """
    if not config:
        raise ValueError("Config is required")

    resource = None
    try:
        # Setup phase
        resource = await create_resource(config, resource_id)
        await resource.initialize()

        # Yield resource to caller
        yield resource

    finally:
        # Cleanup phase (always runs)
        if resource:
            await resource.cleanup()
            await resource.close()
```

### Step 4: Handle Error Cases

**Critical patterns**:
- Validate inputs before setup
- Track resource state (None check before cleanup)
- Use try/finally for guaranteed cleanup
- Handle cleanup errors gracefully
- Log cleanup failures but don't raise

```python
@asynccontextmanager
async def safe_resource_manager(
    settings: Settings
) -> AsyncIterator[Resource]:
    """Resource manager with comprehensive error handling."""
    if not settings:
        raise ValueError("Settings is required")

    resource = None
    try:
        resource = await create_resource(settings)
        yield resource
    except Exception as e:
        logger.error(f"Resource operation failed: {e}")
        raise
    finally:
        if resource:
            try:
                await resource.close()
            except Exception as cleanup_error:
                # Log but don't raise - cleanup errors shouldn't hide original error
                logger.warning(f"Cleanup failed: {cleanup_error}")
```

### Step 5: Add Type Safety

**Required type hints**:
- Return type: `AsyncIterator[T]` where T is yielded type
- Parameter types: All parameters must be typed
- Generic types: Use TypeVar for reusable managers

```python
from collections.abc import AsyncIterator
from typing import TypeVar

T = TypeVar("T")

@asynccontextmanager
async def typed_manager(
    config: Config,
    factory: Callable[[Config], T]
) -> AsyncIterator[T]:
    """Generic resource manager with type safety."""
    resource = factory(config)
    try:
        yield resource
    finally:
        if hasattr(resource, 'close'):
            await resource.close()
```

### Step 6: Test Async Context Managers

```python
import pytest

@pytest.mark.asyncio
async def test_context_manager_cleanup():
    """Test cleanup happens even on error."""
    cleanup_called = False

    @asynccontextmanager
    async def test_resource() -> AsyncIterator[str]:
        nonlocal cleanup_called
        try:
            yield "resource"
        finally:
            cleanup_called = True

    # Test normal flow
    async with test_resource() as r:
        assert r == "resource"
    assert cleanup_called is True

    # Test error flow
    cleanup_called = False
    with pytest.raises(ValueError):
        async with test_resource():
            raise ValueError("Test error")
    assert cleanup_called is True  # Cleanup still happened
```

## Examples

### Example 1: Database Session Manager (Primary Pattern)

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from neo4j import AsyncSession, AsyncDriver

@asynccontextmanager
async def session(
    driver: AsyncDriver,
    database: str | None = None,
    fetch_size: int | None = None
) -> AsyncIterator[AsyncSession]:
    """Create a database session with automatic resource management.

    This is the primary pattern from database.py (line 517-549).
    """
    session = None
    try:
        session = driver.session(
            database=database,
            fetch_size=fetch_size or 1000,
        )
        yield session
    finally:
        if session:
            await session.close()

# Usage
async with session(driver, "mydb") as s:
    result = await s.run("MATCH (n) RETURN n LIMIT 10")
```

### Example 2: Resource Pool Manager

```python
@asynccontextmanager
async def pooled_connection(
    pool: ConnectionPool,
    timeout: float = 30.0
) -> AsyncIterator[Connection]:
    """Acquire connection from pool with automatic return."""
    conn = await pool.acquire(timeout=timeout)
    try:
        yield conn
    finally:
        await pool.release(conn)
```

### Example 3: Async File Manager

```python
@asynccontextmanager
async def async_file_writer(
    path: Path,
    mode: str = "w"
) -> AsyncIterator[AsyncTextIOWrapper]:
    """Async file writer with guaranteed close."""
    file = await aiofiles.open(path, mode)
    try:
        yield file
    finally:
        await file.close()
```

See [references/reference.md](./references/reference.md) for more variations and patterns.

## Requirements

- Python 3.9+ (for `collections.abc.AsyncIterator`)
- `contextlib.asynccontextmanager` decorator
- Understanding of async/await syntax
- Type hints: `AsyncIterator[T]` from `collections.abc`

**Installation**: Standard library (no additional packages)

## Common Patterns

### Pattern 1: State Tracking
```python
@asynccontextmanager
async def tracked_resource() -> AsyncIterator[Resource]:
    """Track resource state to prevent double-cleanup."""
    resource = None  # Track if resource was created
    try:
        resource = await create_resource()
        yield resource
    finally:
        if resource:  # Only cleanup if created
            await resource.cleanup()
```

### Pattern 2: Statistics Tracking
```python
@asynccontextmanager
async def session_with_stats(
    driver: AsyncDriver,
    stats: QueryStats
) -> AsyncIterator[AsyncSession]:
    """Track active session count."""
    session = None
    try:
        stats.active_sessions += 1
        session = driver.session()
        yield session
    finally:
        stats.active_sessions -= 1
        if session:
            await session.close()
```

### Pattern 3: Nested Context Managers
```python
@asynccontextmanager
async def transaction(database: str) -> AsyncIterator[Transaction]:
    """Nested context: session contains transaction."""
    async with session(database) as sess:
        tx = await sess.begin_transaction()
        try:
            yield tx
            await tx.commit()
        except Exception:
            await tx.rollback()
            raise
```

## Red Flags

❌ **Avoid These Mistakes:**

1. **Missing finally block** - cleanup may not run
2. **Raising errors in finally** - hides original exception
3. **Not tracking resource state** - may cleanup None
4. **Optional config parameters** - violates fail-fast
5. **Forgetting AsyncIterator type** - type safety lost
6. **Not validating inputs** - errors happen in wrong phase

✅ **Follow These Rules:**

1. Always use try/finally for cleanup
2. Check resource is not None before cleanup
3. Log cleanup errors, don't raise them
4. Validate config at entry, not in setup
5. Use AsyncIterator[T] type hint
6. Make config parameters required

## Integration with Project Patterns

### Clean Architecture
- **Infrastructure Layer**: Database session managers
- **Application Layer**: Service-level resource coordination
- **Domain Layer**: Domain resource abstractions

### ServiceResult Pattern
```python
@asynccontextmanager
async def safe_operation() -> AsyncIterator[ServiceResult[Resource]]:
    """Combine context manager with ServiceResult."""
    try:
        resource = await create_resource()
        yield ServiceResult.ok(resource)
    except Exception as e:
        yield ServiceResult.fail(str(e))
    finally:
        if resource:
            await resource.cleanup()
```

### Fail-Fast Principle
```python
@asynccontextmanager
async def strict_manager(settings: Settings) -> AsyncIterator[Resource]:
    """Fail fast at construction, not during usage."""
    if not settings:
        raise ValueError("Settings required")  # Fail immediately

    # All validation before try block
    if not settings.database_url:
        raise ValueError("Database URL required")

    resource = None
    try:
        resource = await create_resource(settings)
        yield resource
    finally:
        if resource:
            await resource.close()
```

## See Also

- [references/reference.md](./references/reference.md) - Technical details and advanced usage
- [templates/context-manager-template.py](./templates/context-manager-template.py) - Reusable template
- [Production Example](../../src/project_watch_mcp/infrastructure/neo4j/database.py) - Real-world implementation (line 517)
