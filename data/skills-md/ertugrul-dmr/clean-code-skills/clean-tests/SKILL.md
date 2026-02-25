---
name: clean-tests
description: Use when writing, fixing, editing, or refactoring Python tests. Enforces Clean Code principles—fast tests, boundary coverage, one assert per test.
---

# Clean Tests

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```python
# Bad - only tests happy path
def test_divide():
    assert divide(10, 2) == 5

# Good - tests edge cases too
def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_negative():
    assert divide(-10, 2) == -5
```

## T2: Use a Coverage Tool

Coverage tools report gaps in your testing strategy. Don't ignore them.

```bash
# Run with coverage
pytest --cov=myproject --cov-report=term-missing

# Aim for meaningful coverage, not 100%
```

## T3: Don't Skip Trivial Tests

Trivial tests document behavior and catch regressions. They're worth more than their cost.

```python
# Worth having - documents expected behavior
def test_user_default_role():
    user = User(name="Alice")
    assert user.role == "member"
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `@pytest.mark.skip` to hide problems. Either fix the test or delete it.

```python
# Bad - hiding a problem
@pytest.mark.skip(reason="flaky, fix later")
def test_async_operation():
    ...

# Good - either fix it or document why it's skipped
@pytest.mark.skip(reason="Requires Redis, see CONTRIBUTING.md for setup")
def test_cache_invalidation():
    ...
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```python
def test_pagination_boundaries():
    items = list(range(100))
    
    # First page
    assert paginate(items, page=1, size=10) == items[0:10]
    
    # Last page
    assert paginate(items, page=10, size=10) == items[90:100]
    
    # Beyond last page
    assert paginate(items, page=11, size=10) == []
    
    # Page zero (invalid)
    with pytest.raises(ValueError):
        paginate(items, page=0, size=10)
    
    # Empty list
    assert paginate([], page=1, size=10) == []
```

## T6: Exhaustively Test Near Bugs

When you find a bug, write tests for all similar cases. Bugs cluster.

```python
# Found bug: off-by-one in date calculation
# Now test ALL date boundaries
def test_month_boundaries():
    assert last_day_of_month(2024, 1) == 31  # January
    assert last_day_of_month(2024, 2) == 29  # Leap year February
    assert last_day_of_month(2023, 2) == 28  # Non-leap February
    assert last_day_of_month(2024, 4) == 30  # 30-day month
    assert last_day_of_month(2024, 12) == 31 # December
```

## T7: Patterns of Failure Are Revealing

When tests fail, look for patterns. They often point to deeper issues.

```python
# If all async tests fail intermittently,
# the problem isn't the tests—it's the async handling
```

## T8: Test Coverage Patterns Can Be Revealing

Look at which code paths are untested. Often they reveal design problems.

```python
# If you can't easily test a function, it probably does too much
# Refactor for testability
```

## T9: Tests Should Be Fast

Slow tests don't get run. Keep unit tests under 100ms each.

```python
# Bad - hits real database
def test_user_creation():
    db = connect_to_database()  # Slow!
    user = db.create_user("Alice")
    assert user.name == "Alice"

# Good - uses mock or in-memory
def test_user_creation():
    db = InMemoryDatabase()
    user = db.create_user("Alice")
    assert user.name == "Alice"
```

## Test Organization

### F.I.R.S.T. Principles

- **Fast**: Tests should run quickly
- **Independent**: Tests shouldn't depend on each other
- **Repeatable**: Same result every time, any environment
- **Self-Validating**: Pass or fail, no manual inspection
- **Timely**: Written before or with the code, not after

### One Concept Per Test

```python
# Bad - testing multiple things
def test_user():
    user = User("Alice", "alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.is_valid()
    user.activate()
    assert user.is_active

# Good - one concept each
def test_user_stores_name():
    user = User("Alice", "alice@example.com")
    assert user.name == "Alice"

def test_user_stores_email():
    user = User("Alice", "alice@example.com")
    assert user.email == "alice@example.com"

def test_new_user_is_valid():
    user = User("Alice", "alice@example.com")
    assert user.is_valid()

def test_user_can_be_activated():
    user = User("Alice", "alice@example.com")
    user.activate()
    assert user.is_active
```

## Quick Reference

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (<100ms) |
