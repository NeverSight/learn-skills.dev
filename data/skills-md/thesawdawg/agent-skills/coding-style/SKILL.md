---
name: coding-style
description: Enforce consistent coding style, conventions, and best practices across all projects. Automatically applies PEP 8 for Python, Conventional Commits for version control, clean code principles, Flask-specific patterns, and secure development guidelines. Use whenever writing, reviewing, or refactoring code; generating commit messages; or creating documentation.
---

# Coding Style & Rules

## Commit Messages — Conventional Commits

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types (choose one)
| Type | Use case |
|------|----------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, linting — no logic change |
| `refactor` | Code restructuring — no functional change |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system, dependencies, packaging |
| `ci` | CI/CD configuration |
| `chore` | Maintenance tasks that don't fit above |

### Format Rules
- **Scope:** include in parentheses when applicable — `feat(auth)`, `fix(db)`, `docs(api)`
- **Subject:** imperative mood, max 72 characters, no trailing period
- **Body:** wrap at 72 chars; explain **why** the change is needed, not what it does
- **Footer:** use `BREAKING CHANGE:` for breaking changes; `Closes #123` or `Refs PROJ-456` for issue tracking

### Examples
```
feat(auth): add JWT token refresh middleware

Handle expired tokens transparently by refreshing
access tokens before they expire.

Closes #247
```

```
fix(db): resolve connection pool exhaustion under load

Increase max pool size and add idle timeout to prevent
connection leaks during peak traffic.
```

## Python Style — PEP 8 + Modern Practices

### Naming Conventions
| Category | Convention | Example |
|----------|-----------|---------|
| Variables / functions | `snake_case` | `user_name`, `fetch_data()` |
| Classes | `PascalCase` | `DatabaseConnection` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 3` |
| Private members | `_single_leading` or `__double` | `_internal()`, `__config` |
| Modules / packages | `lowercase_with_underscores` | `user_auth.py` |
| Class constants | `UPPER_SNAKE_CASE` | `MAX_SIZE = 100` |

### Code Formatting
- **Indentation:** 4 spaces (never tabs)
- **Line length:** max 88 chars for code, 72 chars for docstrings and comments
- **Blank lines:** 2 between top-level definitions, 1 between methods in a class
- **Spacing:** around operators (`x = 1 + 2`), after commas (`f(a, b)`)
- **Trailing whitespace:** never
- **Line endings:** Unix LF

### Imports — Strict Order
1. Standard library (sorted alphabetically)
2. Third-party packages (sorted alphabetically)
3. Local application imports (sorted alphabetically)

Each group separated by one blank line. Always use absolute imports.

```python
# Standard library
import os
import sys

# Third party
import requests
from flask import Blueprint, jsonify

# Local
from tools.lib.config import get_config
from tools.lib.models import User
```

### Type Hints
- Add type hints for all function signatures and class attributes
- Use built-in generics for Python 3.10+ (`list[str]`, `str | None`) or `typing` module for older versions
- Document exceptions in docstrings when non-obvious

```python
from datetime import datetime
from typing import Optional

def fetch_user(user_id: int) -> dict | None:
    """Fetch a user by ID.
    
    Args:
        user_id: The unique user identifier.
        
    Returns:
        User dict if found, None otherwise.
    """
    ...
```

### Docstrings — Google Style
```python
def process_data(raw_input: str, validate: bool = True) -> Result:
    """Process raw input data and return validated results.

    Args:
        raw_input: The input string to process.
        validate: Whether to enforce validation rules. Defaults to True.

    Returns:
        A Result object containing the processed data.

    Raises:
        ValueError: If input is empty and validation is enabled.
        TypeError: If input is not a string.
    """
```

### Error Handling
- **Never** use bare `except:` — always catch specific exceptions
- Use context managers (`with`) for resources (files, connections, locks)
- Document expected exceptions in docstrings
- Provide meaningful error messages that aid debugging

```python
try:
    connection = connect_db(host, port)
except (ConnectionRefusedError, TimeoutError) as e:
    logger.error("Database connection failed: %s", e)
    raise ServiceUnavailable("Unable to reach database") from e
finally:
    if connection:
        connection.close()
```

## Flask-Specific Patterns

### Application Structure
- Use **Blueprints** for modular routing — never route directly in `__init__.py`
- Initialize extensions via factory pattern (`init_app`)
- Split config: base settings, environment-specific overrides, secrets from env vars
- Register error handlers at both app and blueprint levels

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/users/<int:user_id>')
def get_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return jsonify(data=user.to_dict())
```

### API Conventions
- **Endpoint naming:** plural nouns (`/api/v1/users`, not `/getUser`)
- **Response format (always consistent):**
  ```json
  {
      "status": "success",
      "data": { ... },
      "message": "Optional message"
  }
  ```
- **Error response:**
  ```json
  {
      "status": "error",
      "errors": [{"field": "email", "message": "Invalid email"}]
  }
  ```
- Proper HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Internal Server Error)

### Security Checklist
- Secrets in environment variables only — never in code
- CSRF protection on all forms (`flask-wtf` configured)
- CORS scoped to allowed origins only
- Validate and sanitize all user input at the boundary
- Use parameterized queries — never string interpolation for SQL

## General Clean Code Principles

### Functions
- Single responsibility — one thing, done well
- Max ~20 lines before considering refactoring into smaller functions
- Early returns / guard clauses to reduce nesting depth
- Descriptive, expressive parameter names
- Avoid side effects; prefer pure functions where possible

### Classes
- High cohesion (related responsibilities together)
- Low coupling (minimize dependencies on other classes)
- One reason to change per class
- Prefer composition over inheritance

### Tests
- Arrange / Act / Assert structure
- Test names describe the scenario: `test_user_with_invalid_email_raises_validation_error`
- Mock external services; test your own logic directly
- Aim for meaningful coverage — every test should catch a real bug if removed

### Documentation
- Inline comments explain **why**, not **what** (the code already shows what)
- Prefer readable, self-documenting code over clever tricks
- Update docstrings when behavior changes — never let docs rot
- Keep README.md and CHANGELOG.md current

## Git Workflow

- Commit frequently with small, focused changes
- Use the commit message rules above
- Branch by feature or fix: `feat/add-login`, `fix/db-timeout`
- Squash meaningless commits before merging
- Write clear PR descriptions linking issues with `Closes #123`
