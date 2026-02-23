---
name: pytest-coder
description: Write pytest tests with fixtures, parametrization, mocking, async testing, and modern patterns. Use when creating or updating Python test files. Not for unittest — use standard library patterns instead.
allowed-tools: Read Write Edit Grep Glob Bash WebSearch
---

# Pytest Coder

## Core Philosophy

| Principle | Application |
|-----------|-------------|
| **AAA Pattern** | Arrange-Act-Assert for every test |
| **Behavior over Implementation** | Test what code does, not how |
| **Isolation** | Tests must be independent |
| **Fast Tests** | Mock I/O, minimize database hits |
| **Descriptive Names** | Test name explains the scenario |
| **Coverage** | Test happy paths AND edge cases |

## Project Structure

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Unit tests (fast, isolated)
│   ├── test_models.py
│   └── test_services.py
├── integration/         # Integration tests (real dependencies)
│   └── test_api.py
└── fixtures/            # Test data files
    └── sample_data.json
```

## Essential Patterns

### Basic Test Structure

```python
import pytest
from myapp.services import UserService

class TestUserService:
    """Tests for UserService."""

    def test_create_user_with_valid_data(self, user_service):
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test User"}

        # Act
        result = user_service.create(user_data)

        # Assert
        assert result.email == "test@example.com"
        assert result.id is not None

    def test_create_user_with_duplicate_email_raises_error(self, user_service, existing_user):
        # Arrange
        user_data = {"email": existing_user.email, "name": "Another User"}

        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            user_service.create(user_data)
```

### Fixtures

```python
# conftest.py
import pytest
from myapp.database import get_db
from myapp.services import UserService

@pytest.fixture
def db():
    """Provide a clean database session."""
    session = get_db()
    yield session
    session.rollback()

@pytest.fixture
def user_service(db):
    """Provide UserService instance."""
    return UserService(db)

@pytest.fixture
def sample_user():
    """Provide sample user data."""
    return {"email": "test@example.com", "name": "Test User", "password": "secret123"}

@pytest.fixture
def existing_user(db, sample_user):
    """Create and return an existing user."""
    from myapp.models import User
    user = User(**sample_user)
    db.add(user)
    db.commit()
    return user
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input_email,expected_valid", [
    ("valid@example.com", True),
    ("also.valid@domain.co.uk", True),
    ("invalid-email", False),
    ("missing@domain", False),
    ("", False),
])
def test_email_validation(input_email, expected_valid):
    from myapp.validators import is_valid_email
    assert is_valid_email(input_email) == expected_valid

@pytest.mark.parametrize("status,expected_message", [
    ("pending", "Order is being processed"),
    ("shipped", "Order has been shipped"),
    ("delivered", "Order has been delivered"),
], ids=["pending-status", "shipped-status", "delivered-status"])
def test_order_status_message(status, expected_message):
    from myapp.orders import get_status_message
    assert get_status_message(status) == expected_message
```

### Mocking

```python
from unittest.mock import Mock, patch, AsyncMock

def test_send_email_calls_smtp(user_service):
    # Mock external dependency
    with patch("myapp.services.smtp_client") as mock_smtp:
        mock_smtp.send.return_value = True

        user_service.send_welcome_email("test@example.com")

        mock_smtp.send.assert_called_once_with(
            to="test@example.com",
            subject="Welcome!",
        )

def test_payment_processing_handles_failure():
    mock_gateway = Mock()
    mock_gateway.charge.side_effect = PaymentError("Card declined")

    service = PaymentService(gateway=mock_gateway)

    with pytest.raises(PaymentError):
        service.process_payment(amount=100)
```

### Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch_user(user_service):
    # Arrange
    user_id = 1

    # Act
    user = await user_service.get_by_id(user_id)

    # Assert
    assert user.id == user_id

@pytest.fixture
async def async_db():
    """Async database session fixture."""
    from myapp.database import async_session
    async with async_session() as session:
        yield session
        await session.rollback()

# Mock async functions
@pytest.mark.asyncio
async def test_async_external_api():
    with patch("myapp.client.fetch_data", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"status": "ok"}

        result = await fetch_and_process()

        assert result["status"] == "ok"
```

### Testing Exceptions

```python
import pytest

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_input_raises_with_message():
    with pytest.raises(ValueError, match="must be positive"):
        process_amount(-100)

def test_exception_attributes():
    with pytest.raises(CustomError) as exc_info:
        risky_operation()

    assert exc_info.value.code == "E001"
    assert "failed" in str(exc_info.value)
```

## Fixture Scopes

| Scope | Lifecycle | Use Case |
|-------|-----------|----------|
| `function` | Per test (default) | Most fixtures |
| `class` | Per test class | Shared setup within class |
| `module` | Per module | Expensive setup shared by module |
| `session` | Entire test run | Database connections, servers |

```python
@pytest.fixture(scope="session")
def database_engine():
    """Create engine once for entire test session."""
    engine = create_engine(TEST_DATABASE_URL)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(database_engine):
    """Create fresh session per test."""
    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

## Markers

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "unit: marks unit tests",
]

# Usage
@pytest.mark.slow
def test_complex_calculation():
    ...

@pytest.mark.integration
def test_database_connection():
    ...

# Run specific markers
# pytest -m "not slow"
# pytest -m "unit"
```

## Quality Checklist

- [ ] AAA pattern (Arrange-Act-Assert) in every test
- [ ] Descriptive test names explaining the scenario
- [ ] Fixtures for common setup
- [ ] Parametrized tests for multiple inputs
- [ ] Mocks for external dependencies
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases covered
- [ ] Async tests use `@pytest.mark.asyncio`
- [ ] No test interdependencies
- [ ] Coverage >90%

## Anti-Patterns

| Anti-Pattern | Why Bad | Fix |
|--------------|---------|-----|
| Tests depend on order | Flaky, hard to debug | Use fixtures, isolate |
| Testing implementation | Brittle tests | Test behavior |
| Too many assertions | Hard to identify failure | One assertion per test |
| No error case tests | Missing coverage | Test exceptions explicitly |
| Slow unit tests | Slow feedback | Mock I/O, use in-memory DB |
