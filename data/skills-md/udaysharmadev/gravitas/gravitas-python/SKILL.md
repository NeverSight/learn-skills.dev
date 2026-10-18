---
name: gravitas-python
description: >
  GRAVITAS extension for Python projects. Adds Python-specific recon,
  type checking with mypy/pyright, ruff/flake8 lint, pytest patterns,
  and common Python failure modes.
  Load in addition to the base GRAVITAS skill.
triggers:
  - "python"
  - "py"
  - "django"
  - "fastapi"
  - "flask"
  - "pytest"
  - "mypy"
---

# GRAVITAS — Python Extension

Extends the base GRAVITAS skill with Python-specific patterns.
Load `skills/gravitas/SKILL.md` first, then this file.

---

## Python Recon Additions

```
□ pyproject.toml — [tool.mypy], [tool.ruff], [tool.pytest.ini_options]
□ setup.py / setup.cfg — legacy config
□ requirements.txt / requirements-dev.txt — dependency versions
□ conftest.py — pytest fixtures (critical for understanding test patterns)
□ __init__.py — package structure
□ Type stubs — are there py.typed markers? stub packages installed?
```

### Read pyproject.toml for type strictness
```bash
cat pyproject.toml | grep -A 10 "\[tool.mypy\]"
cat pyproject.toml | grep -A 10 "\[tool.ruff\]"
```

---

## Python Verification Chain

```bash
# Full chain — in this order
mypy . --strict                          # type correctness
ruff check .                             # lint (fast, Rust-based)
ruff format --check .                    # format check
pytest -v --tb=short                     # all tests

# With coverage
pytest --cov=src --cov-report=term-missing -v

# Type coverage
mypy . --strict 2>&1 | tail -5           # summary line shows error count
```

---

## Python-Specific Anti-Patterns

### Never use bare `except`
```python
BAD:  except:
GOOD: except ValueError as e:
GOOD: except (TypeError, ValueError) as e:
```

### Never shadow builtins
```python
BAD:  list = [1, 2, 3]     # shadows list()
BAD:  id = user.id         # shadows id()
GOOD: items = [1, 2, 3]
GOOD: user_id = user.id
```

### Type annotations required (with mypy strict)
```python
BAD:  def process(data):
GOOD: def process(data: dict[str, Any]) -> ProcessResult:
```

### Use dataclasses or Pydantic over dicts for structured data
```python
BAD:  return {"user_id": 1, "name": "Alice"}   # no type safety
GOOD: return UserResponse(user_id=1, name="Alice")
```

---

## Common Python Failure Modes

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| `Optional[X] has no attribute Y` | None not handled | Add `if x is not None:` guard |
| `Incompatible return value type` | Wrong return type | Check function signature |
| `Missing return statement` | Not all paths return | Add explicit return |
| `Module has no attribute X` | Wrong import | Check module with `dir(module)` |
| `Cannot find implementation for X` | Missing stub | Install `types-X` package |
| Circular import | Import at module level | Move to function level or restructure |

---

## Test Patterns (pytest)

### Fixture pattern
```python
# conftest.py
import pytest
from myapp.db import get_db

@pytest.fixture
def db():
    conn = get_db(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def client(db):
    from myapp import create_app
    app = create_app({"TESTING": True})
    with app.test_client() as c:
        yield c
```

### Standard test structure
```python
class TestUserAuth:
    def test_login_success(self, client, db):
        # Arrange
        db.execute("INSERT INTO users VALUES (1, 'alice', 'hash')")
        # Act
        response = client.post("/login", json={"username": "alice", "password": "pw"})
        # Assert
        assert response.status_code == 200
        assert response.json["token"] is not None

    def test_login_wrong_password(self, client, db):
        response = client.post("/login", json={"username": "alice", "password": "wrong"})
        assert response.status_code == 401
```

### Parametrize for edge cases
```python
@pytest.mark.parametrize("input,expected", [
    ("", ValueError),
    (None, TypeError),
    ("valid@email.com", None),
    ("not-an-email", ValueError),
])
def test_validate_email(input, expected):
    if expected:
        with pytest.raises(expected):
            validate_email(input)
    else:
        validate_email(input)  # should not raise
```

---

## Framework-Specific Notes

### FastAPI
```python
# Always test with TestClient, not raw function calls
from fastapi.testclient import TestClient
client = TestClient(app)

# Type all path/query params and bodies
@router.post("/users", response_model=UserResponse)
async def create_user(body: CreateUserRequest) -> UserResponse:
    ...
```

### Django
```python
# Use pytest-django
# settings for tests
@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username="test", password="pass")
    assert user.id is not None
```

---

## Quick Reference

```bash
# Run single test file
pytest src/auth/test_session.py -v

# Run single test
pytest src/auth/test_session.py::TestSession::test_timeout -v

# Run with pdb on failure
pytest --pdb

# Show slowest tests
pytest --durations=10

# Type check single file
mypy src/auth/session.py --strict
```
