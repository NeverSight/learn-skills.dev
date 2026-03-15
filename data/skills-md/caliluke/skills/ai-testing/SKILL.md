---
name: ai-testing
description: Guidelines for writing effective, robust, and maintainable tests. Use when writing unit tests, integration tests, debugging test failures, or setting up test doubles. Covers test design, assertions, fakes vs mocks, and debugging strategies.
---

# AI Testing Guidelines

Principles for writing tests that are reliable, maintainable, and actually catch bugs.

---

## 1. Test Design

### Define Purpose and Scope

Each test should have a clear, singular purpose:

- **Unit test**: Isolated function logic
- **Integration test**: Component interactions
- **Error path test**: Specific failure handling
- **Success path test**: Happy path behavior

Don't mix concerns. A test that checks both success and error handling is two tests.

### Test Behaviors, Not Methods

Focus each test on a single, specific behavior:

```python
# Good: Tests one behavior
def test_withdrawal_with_insufficient_funds_raises_error():
    account = Account(balance=50)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(100)

# Bad: Tests multiple behaviors
def test_account():
    account = Account(balance=100)
    account.withdraw(50)
    assert account.balance == 50
    with pytest.raises(InsufficientFundsError):
        account.withdraw(100)
    account.deposit(200)
    assert account.balance == 250
```

### Test the Right Layer

| Layer            | Test Type        | Test Double Strategy      |
| ---------------- | ---------------- | ------------------------- |
| Business logic   | Unit test        | Fake or mock all I/O      |
| API endpoints    | Integration test | Fake external services    |
| Database queries | Integration test | Use test database or fake |
| Full workflows   | E2E test         | Minimal faking            |

### Test via Public APIs

Exercise code through its intended public interface:

```python
# Good: Uses public API
result = service.process_order(order)
assert result.status == "completed"

# Bad: Testing private implementation
service._validate_order(order)  # Don't test private methods
service._internal_cache["key"]  # Don't inspect internals
```

If a private method needs testing, refactor it into its own component with a public API.

### Verify Assumptions Explicitly

Don't assume framework behavior. If you expect validation to reject bad input, write a test that proves it.

---

## 2. Test Structure

### Arrange, Act, Assert

Organize every test into three distinct phases:

```python
def test_create_user_success():
    # Arrange: Set up preconditions
    user_data = {"name": "Alice", "email": "alice@example.com"}
    service = UserService(fake_database)

    # Act: Execute the operation
    user = service.create_user(user_data)

    # Assert: Verify outcomes
    assert user.id is not None
    assert user.name == "Alice"
    assert fake_database.get_user(user.id) == user
```

Keep phases distinct. Don't do more setup after the Act phase.

### No Logic in Tests

Tests should be trivially correct upon inspection:

```python
# Good: Explicit expected value
assert calculate_total(items) == 150.00

# Bad: Logic that could have bugs
expected = sum(item.price * item.quantity for item in items)
assert calculate_total(items) == expected
```

Avoid loops, conditionals, and calculations in test bodies. If you need complex setup, extract it to a helper function (and test that helper).

### Clear Naming

Test names should describe the behavior and expected outcome:

```text
test_[method_name_]context_expected_result

test_withdraw_insufficient_funds_raises_error
test_create_user_duplicate_email_returns_conflict
test_get_order_not_found_returns_none
```

### Setup Methods and Fixtures

Use fixtures for implicit, safe defaults shared by many tests:

```python
@pytest.fixture
def fake_database():
    return FakeDatabase()

@pytest.fixture
def user_service(fake_database):
    return UserService(fake_database)
```

**Critical**: Tests must not rely on specific values from fixtures. If a test cares about a specific value, set it explicitly in the test.

---

## 3. Test Doubles: Prefer Fakes Over Mocks

### The Test Double Hierarchy

1. **Real implementations** - Use when fast, deterministic, simple
2. **Fakes** - Lightweight working implementations (preferred)
3. **Stubs** - Predetermined return values (use sparingly)
4. **Mocks** - Record interactions (use as last resort)

### Why Fakes Beat Mocks

| Aspect             | Fakes                    | Mocks                            |
| ------------------ | ------------------------ | -------------------------------- |
| State verification | ✅ Check actual state    | ❌ Only verify calls made        |
| Brittleness        | Low - tests the contract | High - coupled to implementation |
| Readability        | Clear state setup        | Complex mock configuration       |
| Realism            | Behaves like real thing  | May hide real issues             |
| Maintenance        | Centralized, reusable    | Scattered across tests           |

### Fake Example

```python
class FakeUserRepository:
    def __init__(self):
        self._users = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def get(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

# Test using fake - can verify actual state
def test_create_user_saves_to_repository():
    fake_repo = FakeUserRepository()
    service = UserService(fake_repo)

    user = service.create_user({"name": "Alice"})

    # State verification - check actual result
    saved_user = fake_repo.get(user.id)
    assert saved_user is not None
    assert saved_user.name == "Alice"
```

### When Mocks Are Acceptable

- No fake exists and creating one is disproportionate effort
- Testing specific interaction order is critical (e.g., caching behavior)
- The SUT's contract is defined by interactions (e.g., event emission)

### Mock Anti-Patterns

**Don't mock types you don't own:**

```python
# Bad: Mocking external library directly
mock_requests = MagicMock()
mock_requests.get.return_value.json.return_value = {"data": "value"}

# Good: Create a wrapper you own, mock that
class HttpClient:
    def get_json(self, url: str) -> dict:
        return requests.get(url).json()

# Now mock your wrapper
mock_client = MagicMock(spec=HttpClient)
mock_client.get_json.return_value = {"data": "value"}
```

**Don't mock value objects:**

```python
# Bad: Mocking simple data
mock_date = MagicMock()
mock_date.year = 2024

# Good: Use real value
real_date = date(2024, 1, 15)
```

**Don't mock indirect dependencies:**

```python
# Bad: Mocking a dependency of a dependency
mock_connection = MagicMock()  # Used by repository, not by service
service = UserService(UserRepository(mock_connection))

# Good: Mock or fake the direct dependency
fake_repo = FakeUserRepository()
service = UserService(fake_repo)
```

---

## 4. Assertions

### Assert Observable Behavior

Base assertions on actual outputs and side effects:

```python
# Good: Assert observable result
assert result.status == "completed"
assert len(result.items) == 3

# Bad: Assert implementation detail
assert service._internal_cache["key"] == expected
```

### Prefer State Verification Over Interaction Verification

```python
# Good: Verify the actual state change
user = service.create_user(data)
assert fake_repo.get(user.id) is not None

# Avoid: Only verifying a call was made
mock_repo.save.assert_called_once()  # Doesn't prove it worked
```

### Only Verify State-Changing Interactions

If you must use mocks, verify calls that change external state:

```python
# Good: Verify state-changing call
mock_email_service.send.assert_called_once_with(
    to="user@example.com",
    subject="Welcome"
)

# Bad: Verify read-only call
mock_repo.get_user.assert_called_with(user_id)  # Who cares?
```

### Make Assertions Resilient

```python
# Brittle: Exact string match
assert error.message == "Failed to connect to database at localhost:5432"

# Robust: Essential content
assert "Failed to connect" in error.message
assert isinstance(error, ConnectionError)
```

**Critical**: Avoid asserting exact log messages. They change constantly.

---

## 5. Mocking Techniques (When Necessary)

### Match Real Signatures Exactly

```python
# Real function
async def fetch_user(user_id: str, include_profile: bool = False) -> User:
    ...

# Mock must match
mock_fetch = AsyncMock()  # Not MagicMock for async
mock_fetch.return_value = User(id="123", name="Test")
```

### Understand Before Mocking

Never guess at behavior. Inspect real objects first:

```python
# Write a temporary script to inspect real behavior
from external_api import Client

client = Client()
response = client.get_user("123")
print(type(response))      # <class 'User'>
print(dir(response))       # ['id', 'name', 'email', ...]
print(repr(response))      # User(id='123', name='Alice', ...)
```

Base your mock on observed reality, not assumptions.

### Patch Where Used, Not Where Defined

```python
# src/services/user_service.py
from external_api import Client  # Imported here

class UserService:
    def __init__(self):
        self.client = Client()

# In tests - patch where it's used
@patch("src.services.user_service.Client")  # Not "external_api.Client"
def test_user_service(mock_client_class):
    mock_client_class.return_value = fake_client
    ...
```

### Handle Dependency Injection Caching

```python
# If the app caches clients, clear the cache in tests
import src.dependencies as deps

def test_with_mock_client(monkeypatch):
    mock_client = MagicMock()

    # Patch the class where instantiated
    monkeypatch.setattr(deps, "ExternalClient", lambda: mock_client)

    # Clear any cached instance
    if hasattr(deps, "_cached_client"):
        deps._cached_client = None
```

---

## 6. Debugging Test Failures

### Investigate Internal Code First

When a test fails, assume the bug is in your code:

1. Check logic errors in the code under test
2. Verify assumptions about data
3. Look for unexpected interactions between components
4. Trace the call flow

Only blame external libraries after exhausting internal causes.

### Add Granular Logging

```python
# Temporarily add detailed logging to understand flow
import logging
log = logging.getLogger(__name__)

def process_order(self, order):
    log.debug(f"[process_order] Entry: order={repr(order)}")

    validated = self._validate(order)
    log.debug(f"[process_order] After validate: {repr(validated)}")

    result = self._save(validated)
    log.debug(f"[process_order] After save: {repr(result)}")

    return result
```

Use `repr()` to reveal hidden characters in strings.

### Verify Library Interfaces

When you get `TypeError` from library calls, read the source:

```python
# Error: TypeError: fetch() got unexpected keyword argument 'timeout'

# Don't guess. Check the actual signature in the library:
# def fetch(self, url: str, *, max_retries: int = 3) -> Response:
#                           ^
#                           No timeout parameter!
```

### Systematic Configuration Debugging

For logging/config issues, verify each step:

1. Config loading (env vars, arguments)
2. Logger setup (handlers, levels)
3. File paths and permissions
4. Execution environment (CWD, potential redirection)

Test in isolation before blaming the framework.

---

## 7. Test Organization

### Split Large Test Files

```text
tests/
  users/
    test_create_user.py
    test_update_user.py
    test_delete_user.py
    test_user_errors.py
  orders/
    test_create_order.py
    test_order_workflow.py
```

### Verify All Parameterized Variants

```python
@pytest.mark.parametrize("backend", ["asyncio", "trio"])
async def test_connection(backend):
    # Fix must work for ALL variants
    ...
```

### Re-run After Every Change

**Critical**: After any modification—including linter fixes, formatting, or "trivial" changes—re-run tests. Linter fixes are not behaviorally neutral.

---

## 8. Testing Fakes Themselves

Fakes need tests to ensure fidelity with real implementations:

```python
# Contract test - runs against both real and fake
class UserRepositoryContract:
    """Tests that run against any UserRepository implementation."""

    def test_save_and_retrieve(self, repo):
        user = User(id="1", name="Alice")
        repo.save(user)
        assert repo.get("1") == user

    def test_get_nonexistent_returns_none(self, repo):
        assert repo.get("nonexistent") is None

# Run against fake
class TestFakeUserRepository(UserRepositoryContract):
    @pytest.fixture
    def repo(self):
        return FakeUserRepository()

# Run against real (in integration tests)
class TestRealUserRepository(UserRepositoryContract):
    @pytest.fixture
    def repo(self, database):
        return UserRepository(database)
```

---

## 9. Common Pitfalls

| Pitfall                        | Solution                          |
| ------------------------------ | --------------------------------- |
| Asserting exact error messages | Assert error type + key substring |
| Mocking with wrong signature   | Copy signature from real code     |
| Using MagicMock for async      | Use AsyncMock                     |
| Testing implementation details | Test observable behavior only     |
| Mocking types you don't own    | Create wrapper, mock wrapper      |
| Mocking value objects          | Use real instances                |
| Mocking indirect dependencies  | Mock direct dependencies only     |
| Verifying read-only calls      | Only verify state-changing calls  |
| Complex mock setup             | Switch to fakes                   |
| Skipping re-run after changes  | Always re-run tests               |
| Blaming framework first        | Exhaust internal causes first     |
| Guessing at library behavior   | Inspect real objects first        |
| Scope creep during test fixes  | Stick to defined scope            |
