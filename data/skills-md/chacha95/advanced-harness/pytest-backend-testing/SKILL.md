---
name: pytest-backend-testing
description: Comprehensive pytest testing guide for FastAPI backends. Covers unit testing, integration testing, async patterns, mocking, fixtures, coverage, and FastAPI-specific testing with TestClient. Use when writing or updating test code for backend services, repositories, or API routes.
---

# Pytest Backend Testing Guidelines

## Purpose

Complete guide for writing comprehensive tests for FastAPI backend applications using pytest, pytest-asyncio, and FastAPI TestClient. Emphasizes async testing, proper mocking, layered testing (repository → service → router), and achieving high test coverage.

## When to Use This Skill

- Writing new test files for backend code
- Testing repositories, services, or API routes
- Setting up test fixtures and mocks
- Debugging failing tests
- Improving test coverage
- Writing async tests with pytest-asyncio
- Testing database operations
- Using FastAPI TestClient for route testing

---

## Quick Start

### New Test File Checklist

Creating tests for new code? Follow this checklist:

- [ ] Create test file: `tests/unit/{domain}/test_{module}.py`
- [ ] Import pytest and pytest-asyncio
- [ ] Set up necessary fixtures (session, client, etc.)
- [ ] Use `@pytest.mark.asyncio` for async tests
- [ ] Follow AAA pattern: Arrange, Act, Assert
- [ ] Mock external dependencies
- [ ] Test both success and error cases
- [ ] Verify coverage meets 80% threshold
- [ ] Use descriptive test names: `test_<what>_<when>_<expected>`

### Test Coverage Checklist

Ensuring good coverage? Check these:

- [ ] Test all public methods/functions
- [ ] Test error handling and exceptions
- [ ] Test edge cases and boundary conditions
- [ ] Test validation logic
- [ ] Mock external dependencies (database, APIs)
- [ ] Verify async/await behavior
- [ ] Run `pytest --cov=backend --cov-report=term-missing`
- [ ] Check coverage report for gaps
- [ ] Aim for 80%+ coverage

---

## Project Testing Structure

Your qwarty backend testing structure:

```
backend/
  tests/
    conftest.py              # Global fixtures
    unit/
      domain/
        artist/
          test_artist_repository.py
          test_artist_service.py
        artwork/
        auth/
        ...
      middleware/
        test_error_handler.py
      utils/
        test_utils.py
    integration/             # End-to-end tests
      test_artist_api.py
      test_auth_flow.py
```

---

## Common Test Patterns Quick Reference

### Basic Async Test

```python
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

@pytest.mark.asyncio
async def test_get_artist_by_id(db_session: AsyncSession):
    # Arrange
    artist_id = "test-artist-id"

    # Act
    result = await repository.get_by_id(artist_id)

    # Assert
    assert result is not None
    assert result.id == artist_id
```

### Mocking Database Session

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_create_artist_success():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    # Act
    service = ArtistService(mock_session)
    result = await service.create_artist(data)

    # Assert
    assert mock_session.commit.called
```

### Testing FastAPI Routes

```python
from fastapi.testclient import TestClient
from backend.main import create_application

@pytest.fixture
def client():
    app = create_application()
    return TestClient(app)

def test_get_artist_endpoint(client):
    # Act
    response = client.get("/api/v1/artists/test-id")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == "test-id"
```

---

## Test Organization Principles

### Test Structure (AAA Pattern)

1. **Arrange**: Set up test data, mocks, fixtures
2. **Act**: Execute the code under test
3. **Assert**: Verify the expected outcome

### Test Naming Convention

```python
# Pattern: test_<what>_<when>_<expected>
def test_create_artist_with_valid_data_returns_artist()
def test_get_artist_when_not_found_raises_not_found_error()
def test_update_artist_with_duplicate_name_raises_conflict_error()
```

### Test Organization

- **Unit tests**: Test individual functions/methods in isolation
- **Integration tests**: Test multiple components working together
- **Group related tests**: Use test classes for related functionality

---

## Topic Guides

### 🏗️ Testing Architecture

**Three-Layer Testing Strategy:**
1. **Repository Layer**: Test database queries, CRUD operations
2. **Service Layer**: Test business logic, orchestration
3. **Router Layer**: Test API endpoints, request/response handling

**Key Concepts:**
- Mock dependencies at layer boundaries
- Test each layer independently
- Use integration tests for end-to-end flows
- Maintain test isolation

**[📖 Complete Guide: resources/testing-architecture.md](resources/testing-architecture.md)**

---

### 🧪 Unit Testing

**Unit Test Best Practices:**
- Test single responsibility
- Mock external dependencies
- Fast execution (no database, no network)
- Independent and isolated
- Test both success and failure paths

**Unit Test Pattern:**
```python
@pytest.mark.asyncio
async def test_artist_service_create():
    # Mock repository
    mock_repo = AsyncMock()
    mock_repo.create = AsyncMock(return_value=artist_model)

    # Test service logic
    service = ArtistService(mock_repo)
    result = await service.create_artist(data)

    assert result.name == data.name
```

**[📖 Complete Guide: resources/unit-testing.md](resources/unit-testing.md)**

---

### 🔗 Integration Testing

**Integration Test Focus:**
- Test multiple components together
- Use real database (test database)
- Verify end-to-end workflows
- Test API contracts

**Integration Test Pattern:**
```python
@pytest.mark.asyncio
async def test_create_artist_flow(db_session, client):
    # Full flow: API → Service → Repository → DB
    response = client.post("/api/v1/artists", json=artist_data)
    assert response.status_code == 201

    # Verify in database
    artist = await db_session.get(Artist, response.json()["id"])
    assert artist is not None
```

**[📖 Complete Guide: resources/integration-testing.md](resources/integration-testing.md)**

---

### ⚡ Async Testing

**Async Test Patterns:**
- Use `@pytest.mark.asyncio` decorator
- Configure pytest-asyncio in conftest.py
- Mock async functions with AsyncMock
- Test async context managers
- Handle async exceptions

**Async Mock Pattern:**
```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_function():
    mock_func = AsyncMock(return_value="result")
    result = await mock_func()
    assert result == "result"
    mock_func.assert_awaited_once()
```

**[📖 Complete Guide: resources/async-testing.md](resources/async-testing.md)**

---

### 🎭 Mocking & Fixtures

**Mocking Strategy:**
- Mock external dependencies (database, APIs, S3)
- Use pytest fixtures for reusable test data
- Mock at layer boundaries
- Use MagicMock for sync, AsyncMock for async

**Fixture Pattern:**
```python
import pytest

@pytest.fixture
def sample_artist():
    return Artist(
        id="test-id",
        name="Test Artist",
        bio="Test bio"
    )

@pytest.fixture
async def db_session():
    # Setup test database session
    async with get_test_session() as session:
        yield session
        await session.rollback()
```

**[📖 Complete Guide: resources/mocking-fixtures.md](resources/mocking-fixtures.md)**

---

### 📊 Coverage Best Practices

**Coverage Strategy:**
- Aim for 80%+ coverage (project requirement)
- Focus on critical business logic
- Test error paths and edge cases
- Use coverage reports to find gaps
- Exclude non-testable code (config, main.py)

**Coverage Commands:**
```bash
# Run tests with coverage
pytest --cov=backend --cov-report=term-missing

# Generate HTML report
pytest --cov=backend --cov-report=html

# Check coverage threshold
pytest --cov=backend --cov-fail-under=80
```

**[📖 Complete Guide: resources/coverage-best-practices.md](resources/coverage-best-practices.md)**

---

### 🚀 FastAPI Testing

**FastAPI Test Patterns:**
- Use TestClient for route testing
- Test request validation
- Test response serialization
- Test authentication/authorization
- Test error handling middleware

**TestClient Pattern:**
```python
from fastapi.testclient import TestClient

def test_create_artist_endpoint(client: TestClient):
    response = client.post(
        "/api/v1/artists",
        json={"name": "Artist", "bio": "Bio"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Artist"
```

**[📖 Complete Guide: resources/fastapi-testing.md](resources/fastapi-testing.md)**

---

## Navigation Guide

| Need to... | Read this resource |
|------------|-------------------|
| Understand test structure | [testing-architecture.md](resources/testing-architecture.md) |
| Write unit tests | [unit-testing.md](resources/unit-testing.md) |
| Write integration tests | [integration-testing.md](resources/integration-testing.md) |
| Test async code | [async-testing.md](resources/async-testing.md) |
| Use mocks and fixtures | [mocking-fixtures.md](resources/mocking-fixtures.md) |
| Improve coverage | [coverage-best-practices.md](resources/coverage-best-practices.md) |
| Test FastAPI routes | [fastapi-testing.md](resources/fastapi-testing.md) |

---

## Core Principles

1. **Test Isolation**: Each test runs independently, no shared state
2. **AAA Pattern**: Arrange, Act, Assert for clear test structure
3. **Async Testing**: Use pytest-asyncio for async code
4. **Mock Dependencies**: Mock external systems (database, APIs)
5. **Layered Testing**: Test each layer (repository, service, router) separately
6. **Coverage Goals**: Aim for 80%+ coverage, focus on business logic
7. **Descriptive Names**: Clear test names explain what, when, expected
8. **Error Testing**: Test both success and failure paths
9. **Fast Tests**: Unit tests should be fast (no real database)
10. **Fixtures**: Use fixtures for reusable test data and setup

---

## Quick Reference: Test Template

```python
"""Tests for Artist domain."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.domain.artist.service import ArtistService
from backend.domain.artist.repository import ArtistRepository
from backend.domain.artist.model import Artist
from backend.dtos.artist import ArtistRequestDto
from backend.error import NotFoundError


@pytest.fixture
def sample_artist():
    """Fixture for sample artist data."""
    return Artist(
        id="test-artist-id",
        name="Test Artist",
        bio="Test bio"
    )


@pytest.fixture
def mock_session():
    """Fixture for mocked database session."""
    return AsyncMock(spec=AsyncSession)


class TestArtistRepository:
    """Test suite for ArtistRepository."""

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, mock_session, sample_artist):
        """Test get_by_id returns artist when found."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_artist
        mock_session.execute = AsyncMock(return_value=mock_result)

        repository = ArtistRepository(mock_session)

        # Act
        result = await repository.get_by_id("test-artist-id")

        # Assert
        assert result is not None
        assert result.id == sample_artist.id
        assert result.name == sample_artist.name

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, mock_session):
        """Test get_by_id returns None when not found."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        repository = ArtistRepository(mock_session)

        # Act
        result = await repository.get_by_id("nonexistent-id")

        # Assert
        assert result is None


class TestArtistService:
    """Test suite for ArtistService."""

    @pytest.mark.asyncio
    async def test_create_artist_success(self, mock_session, sample_artist):
        """Test create_artist creates and returns artist."""
        # Arrange
        mock_repo = AsyncMock()
        mock_repo.create = AsyncMock(return_value=sample_artist)

        service = ArtistService(mock_session)
        service._repository = mock_repo

        request_dto = ArtistRequestDto(
            name="Test Artist",
            bio="Test bio"
        )

        # Act
        result = await service.create_artist(request_dto)

        # Assert
        assert result.name == request_dto.name
        mock_repo.create.assert_awaited_once()
```

---

## Current Project Configuration

Your qwarty backend test setup:

**pytest.ini (in pyproject.toml):**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
filterwarnings = ["ignore::DeprecationWarning"]
markers = [
    "security: marks tests as security tests (SQL injection, etc.)",
    "performance: marks tests as performance benchmarks",
]
addopts = [
    "--cov=backend",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]
```

**Test Dependencies:**
- pytest 8.4.2+
- pytest-asyncio 0.24.0+
- pytest-cov 6.0.0+

**Coverage Exclusions:**
- Tests themselves (`tests/*`)
- `__init__.py` files
- Main application entry (`backend/main.py`)
- Some routers and specific domains (see pyproject.toml)

---

## Related Skills

- **fastapi-backend-guidelines**: Backend development patterns (what you're testing)
- **error-tracking**: Error handling patterns to test

---

**Skill Status**: Modular structure with progressive loading for optimal context management
