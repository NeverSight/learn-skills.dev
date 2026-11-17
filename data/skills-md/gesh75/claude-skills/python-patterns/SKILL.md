---
name: python-patterns
description: Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications.
origin: ECC
---

# Python Development Patterns

Idiomatic Python patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Python code
- Reviewing Python code
- Refactoring existing Python code
- Designing Python packages/modules

## Core Principles

### 1. Readability Counts

Python prioritizes readability. Code should be obvious and easy to understand.

```python
# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    """Return only active users from the provided list."""
    return [user for user in users if user.is_active]


# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

### 2. Explicit is Better Than Implicit

Avoid magic; be clear about what your code does.

```python
# Good: Explicit configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Bad: Hidden side effects
import some_module
some_module.setup()  # What does this do?
```

### 3. EAFP - Easier to Ask Forgiveness Than Permission

Python prefers exception handling over checking conditions.

```python
# Good: EAFP style
def get_value(dictionary: dict, key: str) -> Any:
    try:
        return dictionary[key]
    except KeyError:
        return default_value

# Bad: LBYL (Look Before You Leap) style
def get_value(dictionary: dict, key: str) -> Any:
    if key in dictionary:
        return dictionary[key]
    else:
        return default_value
```

## Most-Used Patterns

### Type Hints (basics)

```python
from typing import Optional, Dict, Any

def process_user(
    user_id: str,
    data: Dict[str, Any],
    active: bool = True
) -> Optional[User]:
    """Process a user and return the updated User or None."""
    if not active:
        return None
    return User(user_id, data)
```

Prefer built-in generics on Python 3.9+ (`list[str]`, `dict[str, int]`). For type aliases, TypeVar/generics, and Protocol-based duck typing, see `reference/type-hints.md`.

### Specific Exception Handling

```python
# Good: Catch specific exceptions
def load_config(path: str) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {path}") from e
```

For exception chaining and custom exception hierarchies, see `reference/error-handling.md`.

### Context Managers for Resource Management

```python
# Good: Using context managers
def process_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()
```

For `@contextmanager` and context manager classes, see `reference/context-managers.md`.

### Comprehensions and Generators

```python
# Good: List comprehension for simple transformations
names = [user.name for user in users if user.is_active]

# Good: Generator for lazy evaluation
total = sum(x * x for x in range(1_000_000))
```

For generator functions and when to expand complex comprehensions, see `reference/comprehensions-generators.md`.

## Quick Reference: Python Idioms

| Idiom | Description |
|-------|-------------|
| EAFP | Easier to Ask Forgiveness than Permission |
| Context managers | Use `with` for resource management |
| List comprehensions | For simple transformations |
| Generators | For lazy evaluation and large datasets |
| Type hints | Annotate function signatures |
| Dataclasses | For data containers with auto-generated methods |
| `__slots__` | For memory optimization |
| f-strings | For string formatting (Python 3.6+) |
| `pathlib.Path` | For path operations (Python 3.4+) |
| `enumerate` | For index-element pairs in loops |

## Anti-Patterns to Avoid

```python
# Bad: Mutable default arguments
def append_to(item, items=[]):
    items.append(item)
    return items

# Good: Use None and create new list
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad: Checking type with type()
if type(obj) == list:
    process(obj)

# Good: Use isinstance
if isinstance(obj, list):
    process(obj)

# Bad: Comparing to None with ==
if value == None:
    process()

# Good: Use is
if value is None:
    process()

# Bad: from module import *
from os.path import *

# Good: Explicit imports
from os.path import join, exists

# Bad: Bare except
try:
    risky_operation()
except:
    pass

# Good: Specific exception
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

__Remember__: Python code should be readable, explicit, and follow the principle of least surprise. When in doubt, prioritize clarity over cleverness.

## Reference Files

- `reference/type-hints.md` — read when working with type hints beyond basics: typing module vs built-in generics, type aliases, TypeVar/generics, and Protocol-based duck typing.
- `reference/error-handling.md` — read when handling errors: specific exception handling, exception chaining (`raise ... from e`), and custom exception hierarchies.
- `reference/context-managers.md` — read when managing resources with `with`, writing `@contextmanager` functions, or context manager classes (`__enter__`/`__exit__`).
- `reference/comprehensions-generators.md` — read when writing list/generator comprehensions, generator expressions, or generator functions, and deciding when to expand complex comprehensions.
- `reference/dataclasses.md` — read when defining data containers with `@dataclass` (including validation via `__post_init__`) or `NamedTuple`.
- `reference/decorators.md` — read when writing function decorators, parameterized decorators, or class-based decorators.
- `reference/concurrency.md` — read when choosing concurrency: threading (I/O-bound), multiprocessing (CPU-bound), or async/await for concurrent I/O.
- `reference/packaging.md` — read when organizing packages: standard project layout, import conventions/ordering, and `__init__.py` exports.
- `reference/performance.md` — read when optimizing memory/performance: `__slots__`, generators for large data, and avoiding string concatenation in loops.
- `reference/tooling.md` — read when setting up tooling: black/isort/ruff/pylint/mypy/bandit commands and pyproject.toml configuration.
