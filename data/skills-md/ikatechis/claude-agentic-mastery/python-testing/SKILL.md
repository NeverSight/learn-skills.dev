---
name: python-testing
description: Generate pytest tests for Python modules with parametrization, shared fixtures in conftest.py, and minimal mocking. Use when creating unit tests, test suites, or improving test coverage. Follows 1-1 file correspondence and real object testing principles.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Python Testing Skill

Generate high-quality pytest tests following best practices for this project.

## Core Principles

1. **Minimal Mocking**: Only mock external dependencies (APIs, databases, file I/O). Test with real Python objects whenever possible. Mocking internal logic can hide breaking changes.

2. **Parametrization**: Use `@pytest.mark.parametrize` for testing multiple cases instead of writing separate test functions. Keeps tests DRY and readable.

3. **Shared Fixtures in conftest.py**: Place reusable fixtures in `conftest.py` to avoid duplication. Fixtures are automatically discovered by pytest.

4. **1-1 File Correspondence**: Each source file has a corresponding test file (`src/game.py` → `tests/test_game.py`).

## Instructions

### Step 1: Analyze the Module

Use the Read tool to understand:
- Function signatures and parameters
- Return types and expected behavior
- Dependencies (what needs mocking vs what can be real)
- Error conditions and edge cases
- Existing patterns in the codebase

### Step 2: Identify Fixtures and Parametrization

**Check existing conftest.py**:
- Read `tests/conftest.py` to see what fixtures already exist
- Identify what new fixtures are needed
- Decide if fixtures should be in conftest.py (reusable) or local (test-specific)

**Plan parametrization**:
- Group similar test cases that vary by input/output
- Identify boundary conditions (0, None, empty, negative, max)
- Consider happy path + error cases

### Step 3: Determine What to Mock

**Mock ONLY these**:
- External HTTP/API calls (use `mocker.patch` or `requests_mock`)
- Database connections
- File I/O when not using `tmp_path`
- System calls and environment variables
- Time-dependent operations

**Do NOT mock**:
- Pure functions (calculations, transformations)
- Internal helper functions
- Data classes and models
- Business logic
- Other modules in your project (integration is good!)

### Step 4: Write Tests

Follow this structure:

```python
"""Tests for <module_name> (src/<path>/<module>.py)"""

import pytest
# Import what you're testing
# Import any mocking utilities if absolutely needed


class Test<ClassName>:
    """Test <ClassName> functionality"""

    def test_basic_happy_path(self, fixture_from_conftest):
        """Test normal operation"""
        # Arrange
        # Act
        # Assert

    @pytest.mark.parametrize("input,expected", [
        (case1_in, case1_out),
        (case2_in, case2_out),
        (edge_case, expected),
    ])
    def test_with_various_inputs(self, input, expected):
        """Test behavior with multiple inputs"""
        assert function(input) == expected

    def test_error_condition(self):
        """Test exception handling"""
        with pytest.raises(SpecificException):
            function_that_should_fail()
```

### Step 5: Update conftest.py

If you created reusable fixtures, add them to `tests/conftest.py`:

```python
@pytest.fixture
def descriptive_name():
    """Clear docstring explaining what this provides"""
    # Setup
    obj = create_object()
    yield obj
    # Teardown (if needed)
```

## Quality Checklist

Before finishing:
- [ ] All public methods/functions have tests
- [ ] Edge cases tested (None, 0, empty, max, negative)
- [ ] Error conditions raise expected exceptions
- [ ] Similar tests are parametrized (not duplicated)
- [ ] Reusable fixtures in conftest.py
- [ ] Mocking limited to external dependencies only
- [ ] Test names describe behavior clearly
- [ ] Each test checks one specific behavior
- [ ] Tests run in isolation (no shared state between tests)

## Current Project Structure

```
tests/
├── conftest.py              # Shared fixtures
├── entities/
│   ├── test_player.py      # Tests for src/entities/player.py
│   └── test_zombie.py      # Tests for src/entities/zombie.py
├── test_config.py           # Tests for src/config.py
└── test_game.py             # Tests for src/game.py
```

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed examples.
