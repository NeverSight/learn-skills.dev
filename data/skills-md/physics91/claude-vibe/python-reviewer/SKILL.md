---
name: python-reviewer
description: |
  WHEN: General Python code review, PEP8 compliance, type hints, Pythonic patterns
  WHAT: PEP8/style check + Type hint validation + Pythonic idioms + Error handling + Documentation
  WHEN NOT: FastAPI → fastapi-reviewer, Django → django-reviewer, Data science → python-data-reviewer
---

# Python Reviewer Skill

## Purpose
Reviews Python code for style, idioms, type safety, and best practices.

## When to Use
- Python code review requests
- PEP8 compliance check
- Type hint review
- "Is this Pythonic?" questions
- General Python project review

## Project Detection
- `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`
- `.py` files in project
- `__init__.py` module structure

## Workflow

### Step 1: Analyze Project
```
**Python Version**: 3.11+
**Package Manager**: pip/poetry/uv
**Type Checking**: mypy/pyright
**Linter**: ruff/flake8/pylint
**Formatter**: black/ruff
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full Python review (recommended)
- PEP8/Style compliance
- Type hints and safety
- Error handling patterns
- Performance and idioms
multiSelect: true
```

## Detection Rules

### PEP8 & Style
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Line > 88 chars | Break line or refactor | LOW |
| Missing docstring | Add module/function docstring | MEDIUM |
| Import order wrong | Use isort or ruff | LOW |
| Inconsistent naming | snake_case for functions/vars | MEDIUM |

```python
# BAD: Inconsistent naming
def getUserName(userId):
    pass

# GOOD: PEP8 naming
def get_user_name(user_id: int) -> str:
    pass
```

### Type Hints
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing return type | Add -> ReturnType | MEDIUM |
| Any type overuse | Use specific types | MEDIUM |
| Optional without None check | Add None handling | HIGH |
| Missing generic types | Use list[T], dict[K,V] | LOW |

```python
# BAD: No type hints
def process(data):
    return data.get("name")

# GOOD: Full type hints
def process(data: dict[str, Any]) -> str | None:
    return data.get("name")
```

### Pythonic Idioms
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Manual loop for list | Use list comprehension | LOW |
| if x == True | Use if x | LOW |
| Manual dict iteration | Use .items(), .keys(), .values() | LOW |
| try/except pass | Handle or log exception | HIGH |
| Mutable default arg | Use None default | CRITICAL |

```python
# BAD: Mutable default argument
def append_to(item, target=[]):
    target.append(item)
    return target

# GOOD: None default
def append_to(item, target: list | None = None) -> list:
    if target is None:
        target = []
    target.append(item)
    return target

# BAD: Manual loop
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# GOOD: List comprehension
result = [x * 2 for x in items if x > 0]
```

### Error Handling
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Bare except | Catch specific exceptions | HIGH |
| except Exception | Be more specific | MEDIUM |
| No logging in except | Add logging | MEDIUM |
| Missing finally | Add cleanup if needed | LOW |

```python
# BAD: Bare except
try:
    process()
except:
    pass

# GOOD: Specific exception with logging
try:
    process()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except IOError as e:
    logger.warning(f"IO error: {e}")
    return None
```

### Modern Python (3.10+)
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Union[X, Y] | Use X \| Y | LOW |
| Optional[X] | Use X \| None | LOW |
| Dict, List from typing | Use dict, list builtin | LOW |
| No match statement | Consider match for complex branching | LOW |

```python
# OLD: typing imports
from typing import Optional, Union, List, Dict

def func(x: Optional[int]) -> Union[str, None]:
    pass

# MODERN: Built-in syntax (3.10+)
def func(x: int | None) -> str | None:
    pass

# Match statement (3.10+)
match status:
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case _:
        return "Unknown"
```

## Response Template
```
## Python Code Review Results

**Project**: [name]
**Python**: 3.11 | **Tools**: ruff, mypy, pytest

### Style & PEP8
| Status | File | Issue |
|--------|------|-------|
| LOW | utils.py:45 | Line exceeds 88 characters |

### Type Hints
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | service.py:23 | Missing return type annotation |

### Pythonic Idioms
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | models.py:12 | Mutable default argument |

### Error Handling
| Status | File | Issue |
|--------|------|-------|
| HIGH | api.py:67 | Bare except clause |

### Recommended Actions
1. [ ] Fix mutable default arguments
2. [ ] Add specific exception handling
3. [ ] Add type hints to public functions
4. [ ] Run ruff --fix for style issues
```

## Best Practices
1. **Type Hints**: Use for all public APIs
2. **Docstrings**: Google or NumPy style
3. **Error Handling**: Specific exceptions, always log
4. **Testing**: pytest with fixtures
5. **Tooling**: ruff (lint+format), mypy (types)

## Integration
- `fastapi-reviewer`: FastAPI specific patterns
- `django-reviewer`: Django specific patterns
- `python-data-reviewer`: Pandas/NumPy patterns
- `security-scanner`: Python security checks
