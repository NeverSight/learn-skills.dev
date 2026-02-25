---
name: textual-test-fixtures
description: |
  Pytest fixture patterns for Textual TUI application testing. Creates reusable test
  setup code including app factories, Pilot wrappers, mock fixtures, and async patterns.
  Use when: setting up test infrastructure for Textual apps, creating reusable test
  fixtures, mocking external dependencies (APIs, databases, time), organizing conftest.py,
  or reducing test boilerplate. Covers async fixtures, factory patterns, and mock strategies.

---

# Textual Test Fixtures

Reusable pytest fixtures for efficient Textual application testing.

## Quick Reference

```python
# conftest.py
import pytest
from typing import AsyncIterator

@pytest.fixture
async def app_pilot() -> AsyncIterator[tuple[MyApp, Pilot]]:
    """Provide app with pilot for testing."""
    app = MyApp()
    async with app.run_test() as pilot:
        yield app, pilot
```

## pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # No @pytest.mark.asyncio needed
testpaths = ["tests"]
```

## Core Fixture Patterns

### 1. App Factory Fixture

Create app instances with pilot access:

```python
@pytest.fixture
async def calculator_app() -> AsyncIterator[tuple[CalculatorApp, Pilot]]:
    """Provide calculator app with pilot."""
    app = CalculatorApp()
    async with app.run_test() as pilot:
        yield app, pilot

async def test_addition(calculator_app):
    app, pilot = calculator_app
    await pilot.press(*"2+2", "enter")
    await pilot.pause()
    assert app.query_one("#result").renderable == "4"
```

### 2. Parametrized App Factory

Support multiple app configurations:

```python
@pytest.fixture
async def app_with_config(request) -> AsyncIterator[tuple[MyApp, Pilot]]:
    """Parametrized app fixture."""
    config = getattr(request, "param", {})
    app = MyApp(**config)
    async with app.run_test() as pilot:
        yield app, pilot

@pytest.mark.parametrize("app_with_config", [
    {"theme": "dark"},
    {"theme": "light"},
], indirect=True)
async def test_themed_app(app_with_config):
    app, pilot = app_with_config
    # Test with different themes
```

### 3. Custom Terminal Size Fixture

Test responsive layouts:

```python
@pytest.fixture
async def large_terminal() -> AsyncIterator[tuple[MyApp, Pilot]]:
    """App with large terminal for testing sidebar visibility."""
    app = MyApp()
    async with app.run_test(size=(120, 40)) as pilot:
        yield app, pilot

@pytest.fixture
async def small_terminal() -> AsyncIterator[tuple[MyApp, Pilot]]:
    """App with small terminal for testing compact layout."""
    app = MyApp()
    async with app.run_test(size=(60, 20)) as pilot:
        yield app, pilot
```

### 4. Snapshot Fixture with Common Setup

Disable animations for stable snapshots:

```python
@pytest.fixture
def snap_compare_stable(snap_compare):
    """snap_compare with animations disabled."""
    def wrapper(app, **kwargs):
        original_run_before = kwargs.get("run_before")

        async def run_before(pilot):
            # Disable animations
            for widget in pilot.app.query("*"):
                widget.can_animate = False
            # Run user's setup
            if original_run_before:
                await original_run_before(pilot)

        kwargs["run_before"] = run_before
        return snap_compare(app, **kwargs)
    return wrapper

def test_stable_snapshot(snap_compare_stable):
    assert snap_compare_stable(MyApp())
```

## Mock Fixtures

### Mock API Client

```python
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_api():
    """Mock external API calls."""
    with patch("myapp.api.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"users": [{"name": "Alice"}]}
        yield mock

async def test_data_loading(app_pilot, mock_api):
    app, pilot = app_pilot
    await pilot.press("r")  # Trigger refresh
    await pilot.app.workers.wait_for_complete()

    mock_api.assert_called_once()
    assert len(app.query(".user-item")) == 1
```

### Mock Database

```python
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    """Mock database connection."""
    mock = MagicMock()
    mock.query.return_value = [
        {"id": 1, "name": "Task 1"},
        {"id": 2, "name": "Task 2"},
    ]
    with patch("myapp.db.get_connection", return_value=mock):
        yield mock
```

### Mock Time (Stable Timestamps)

```python
from unittest.mock import patch
from datetime import datetime

@pytest.fixture
def frozen_time():
    """Freeze time for deterministic tests."""
    fixed = datetime(2025, 1, 1, 12, 0, 0)
    with patch("myapp.datetime") as mock_dt:
        mock_dt.now.return_value = fixed
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        yield fixed
```

### Mock Environment Variables

```python
import os
from unittest.mock import patch

@pytest.fixture
def mock_env():
    """Set test environment variables."""
    env = {
        "API_KEY": "test-key",
        "DEBUG": "true",
    }
    with patch.dict(os.environ, env):
        yield env
```

## conftest.py Organization

```python
# tests/conftest.py
"""Shared fixtures for all tests."""

import pytest
from typing import AsyncIterator
from unittest.mock import AsyncMock, patch

from myapp import MyApp
from textual.pilot import Pilot


# === App Fixtures ===

@pytest.fixture
async def app_pilot() -> AsyncIterator[tuple[MyApp, Pilot]]:
    """Standard app with pilot."""
    app = MyApp()
    async with app.run_test() as pilot:
        yield app, pilot


@pytest.fixture
async def app_large() -> AsyncIterator[tuple[MyApp, Pilot]]:
    """App with large terminal."""
    app = MyApp()
    async with app.run_test(size=(120, 40)) as pilot:
        yield app, pilot


# === Mock Fixtures ===

@pytest.fixture
def mock_api():
    """Mock API client."""
    with patch("myapp.api.client", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_settings():
    """Mock settings/config."""
    with patch("myapp.settings") as mock:
        mock.debug = True
        mock.api_url = "http://test"
        yield mock


# === Snapshot Fixtures ===

@pytest.fixture
def snap_compare_stable(snap_compare):
    """Snapshot comparison with animations disabled."""
    def wrapper(app, **kwargs):
        async def setup(pilot):
            for w in pilot.app.query("*"):
                w.can_animate = False
        kwargs.setdefault("run_before", setup)
        return snap_compare(app, **kwargs)
    return wrapper
```

## Test File Organization

```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── conftest.py          # Unit-specific fixtures
│   ├── test_widgets.py
│   └── test_models.py
├── integration/
│   ├── conftest.py          # Integration-specific fixtures
│   └── test_workflows.py
└── snapshot/
    ├── conftest.py          # Snapshot-specific fixtures
    ├── test_layouts.py
    └── __snapshots__/       # Committed SVG baselines
```

## Advanced Patterns

### Fixture Composition

```python
@pytest.fixture
async def authenticated_app(app_pilot, mock_api):
    """App with authenticated user."""
    app, pilot = app_pilot
    mock_api.login.return_value = {"token": "test-token"}

    # Perform login
    await pilot.press(*"testuser", "tab", *"password", "enter")
    await pilot.pause()

    return app, pilot
```

### Async Context Manager Fixture

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_context(config=None):
    """Reusable app context manager."""
    app = MyApp(**(config or {}))
    async with app.run_test() as pilot:
        yield app, pilot

@pytest.fixture
async def default_app():
    async with app_context() as (app, pilot):
        yield app, pilot

@pytest.fixture
async def debug_app():
    async with app_context({"debug": True}) as (app, pilot):
        yield app, pilot
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Fixture not async | Use `async def` for fixtures using `run_test()` |
| Missing `yield` | Use `yield` not `return` in async context fixtures |
| Fixture scope wrong | Default to `function` scope for Textual apps |
| Mock not cleaned up | Use context managers (`with patch(...)`) |

## See Also

- [textual-testing](../textual-testing) - Core testing with Pilot
- [textual-snapshot-testing](../textual-snapshot-testing) - Visual regression testing
- [textual-test-patterns](../textual-test-patterns) - Testing recipes by scenario
