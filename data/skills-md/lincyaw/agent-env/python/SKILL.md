---
name: python
description: Advanced Python development with architecture expertise and automated code quality enforcement. Use when developing Python applications, libraries, or scripts that require high code quality, type safety, best practices, and professional architecture patterns. Includes automated linting with Ruff, type checking with MyPy, security scanning with Bandit, and comprehensive testing. Apply for tasks involving Python code creation, refactoring, quality checks, project initialization, or implementing design patterns.
---

# Python Development Expert

Expert-level Python development skill with senior architect capabilities, automated code quality tools, and comprehensive best practices.

## Core Capabilities

### 1. Code Quality Automation
Use bundled scripts to enforce code quality:

**Run all quality checks:**
```bash
uv run python scripts/check_quality.py [target_directory]
```

This runs:
- **Ruff lint**: Fast linting for code quality issues
- **Ruff format**: Code formatting checks
- **MyPy**: Static type checking
- **Pytest**: Test execution with coverage
- **Bandit**: Security vulnerability scanning

**Auto-fix common issues:**
```bash
uv run python scripts/autofix.py [target_directory]
```

Auto-fixes:
- Code formatting (line length, indentation, quotes)
- Import sorting
- Common linting issues (unused imports, etc.)

### 2. Project Initialization
Create new Python projects with best practices:

```bash
uv run python scripts/init_project.py <project-name> [path]
```

Creates:
- Modern project structure (`src/` layout)
- Configured `pyproject.toml` with Ruff, MyPy, Pytest
- Git ignore file
- Test structure
- README template

### 3. Code Quality Standards
See [code_quality.md](references/code_quality.md) for detailed standards on:
- Linting and formatting configuration
- Type hints and annotations
- Modern Python patterns (match statements, walrus operator, etc.)
- Error handling best practices
- Documentation with comprehensive docstrings
- Testing with pytest
- Dependencies management with uv

### 4. Architecture Patterns
See [architecture_patterns.md](references/architecture_patterns.md) for:
- Project organization (feature-based structure)
- Dependency injection with protocols
- Design patterns (Factory, Strategy, Repository, Unit of Work)
- API design with FastAPI
- Async patterns
- Error handling architecture
- Performance optimization

## Development Workflow

### When Writing New Code

1. **Use type hints everywhere:**
```python
def process_data(
    items: Sequence[dict[str, Any]],
    max_count: int = 100,
) -> list[ProcessedItem]:
    ...
```

2. **Follow modern Python idioms:**
```python
# Use match statements (3.10+)
match status:
    case 200:
        return response.json()
    case 404:
        raise NotFoundError()
    case _:
        raise APIError(status)
```

3. **Add comprehensive docstrings:**
```python
def calculate_metrics(data: pd.DataFrame) -> dict[str, float]:
    """Calculate statistical metrics from data.
    
    Args:
        data: Input DataFrame with numeric columns
    
    Returns:
        Dictionary mapping metric names to values
    
    Raises:
        ValueError: If data is empty
    """
```

### Before Committing

1. **Run auto-fix:** `uv run python scripts/autofix.py`
2. **Run quality checks:** `uv run python scripts/check_quality.py`
3. **Ensure all checks pass** before committing

### Code Review Checklist

- ✅ All functions have type hints
- ✅ Docstrings follow Google style
- ✅ No lint warnings from Ruff
- ✅ MyPy type checking passes
- ✅ No security issues from Bandit
- ✅ Test coverage > 80%
- ✅ Code follows architecture patterns

## Tool Configuration

All tools are configured via `pyproject.toml`:

**Ruff:** Line length 100, Python 3.12+, comprehensive rule set
**MyPy:** Strict mode with no untyped definitions
**Pytest:** Coverage reporting with missing lines
**Coverage:** Excludes test files and common patterns

## Common Patterns

### Dependency Injection
```python
from typing import Protocol

class Repository(Protocol):
    def save(self, item: Item) -> None: ...

class Service:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
```

### Configuration with Pydantic
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    
    model_config = {"env_file": ".env"}
```

### Error Handling
```python
class DomainError(Exception):
    """Base for all domain errors."""
    pass

class ValidationError(DomainError):
    """Invalid input data."""
    pass
```

### Async Operations
```python
async def fetch_all(urls: list[str]) -> list[Response]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

## Quick Reference

**Install dev dependencies:**
```bash
uv add --dev ruff mypy pytest pytest-cov bandit
```

**Run single tool:**
```bash
uv run ruff check .
uv run mypy .
uv run pytest
uv run bandit -r .
```

**Format code:**
```bash
uv run ruff format .
```

**Type check:**
```bash
uv run mypy --strict .
```

## Best Practices Summary

1. **Always use type hints** for function signatures and class attributes
2. **Run quality checks** before committing code
3. **Follow modern Python patterns** (match, protocols, dataclasses)
4. **Use dependency injection** for testability
5. **Write comprehensive docstrings** with examples
6. **Organize by feature** not by layer
7. **Prefer composition** over inheritance
8. **Use async** for I/O-bound operations
9. **Cache expensive** computations
10. **Test with pytest** and maintain >80% coverage

