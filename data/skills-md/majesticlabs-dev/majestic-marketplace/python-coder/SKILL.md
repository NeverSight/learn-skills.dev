---
name: python-coder
description: Modern Python 3.12+ development with uv, ruff, and production-ready practices. Routes to specialized skills for frameworks and testing.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Python-Coder

Modern Python 3.12+ development patterns.

## Related Skills (Use for Specific Needs)

| Skill | Use When |
|-------|----------|
| `fastapi-coder` | Building FastAPI services |
| `django-coder` | Django web applications |
| `pytest-coder` | Writing comprehensive tests |
| `python-debugger` | Debugging Python code |

## Modern Tooling Quick Reference

### Package Management (uv)

```bash
# Project setup
uv init my-project
uv add fastapi pydantic
uv add --dev pytest ruff mypy

# Run commands
uv run python main.py
uv run pytest
```

### Code Quality (ruff)

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.ruff.format]
quote-style = "double"
```

### Type Checking (pyright/mypy)

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

## Python 3.12+ Patterns

### Pattern Matching

```python
match command:
    case {"action": "create", "item": item}:
        create(item)
    case {"action": "delete", "id": int(id)}:
        delete(id)
    case _:
        raise ValueError("Unknown command")
```

### Modern Async

```python
async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### Type Hints

```python
from typing import TypeVar, Protocol

T = TypeVar("T")

class Repository(Protocol[T]):
    def get(self, id: int) -> T | None: ...
    def save(self, entity: T) -> T: ...
```

## Behavioral Standards

- PEP 8 + ruff formatting
- Type hints throughout
- Tests with pytest (>90% coverage target)
- Prefer stdlib before external deps
- Comprehensive error handling with custom exceptions
