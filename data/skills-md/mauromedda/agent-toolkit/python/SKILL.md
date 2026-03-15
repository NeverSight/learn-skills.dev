---
name: python
description: >-
  Guide for writing clean, efficient, idiomatic Python 3.11+ code. Enforces type hints,
  Pydantic v2 for APIs, comprehensions over loops, EAFP error handling. Triggers on
  "python", "pythonic", ".py file", "write python", "python script", "python function",
  "python class", "pydantic", "fastapi", "pytest", "type hint", "typing", "dataclass",
  "async def", "asyncio", "aiohttp", "comprehension", "generator", "decorator",
  "context manager", "with statement", "exception handling", "try except", "raise",
  "logging python", "argparse", "click", "typer", "__init__", "__main__", "import",
  "from import", "python module", "python package", "requirements.txt", "pyproject.toml",
  "ruff", "mypy", "black", "isort", "python testing", "fixture", "parametrize",
  "edit .py", "modify .py", "update .py", "change .py", "fix .py", "refactor .py",
  "edit python", "modify python", "update python", "change python", "fix python code".
  PROACTIVE: MUST invoke BEFORE using Write OR Edit on ANY .py file.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Comprehensive skill for idiomatic Python best practices
# ABOUTME: Covers loops, dicts, comprehensions, typing, Pydantic v2, error handling

# Idiomatic Python Best Practices

**Target**: Python 3.11+ with modern tooling (uv, Pydantic v2, type hints).

**Detailed patterns**: See `references/pydantic-patterns.md` and `references/advanced-patterns.md`

---

## Quick Reference

| Pattern | Pythonic Way | Avoid |
|---------|--------------|-------|
| Iteration | `for item in items:` | `for i in range(len(items)):` |
| Index + Value | `for i, v in enumerate(seq):` | Manual counter |
| Dict Access | `d.get("key", default)` | `if "key" in d: d["key"]` |
| Dict Iteration | `for k, v in d.items():` | `for k in d: v = d[k]` |
| Swap Variables | `a, b = b, a` | `temp = a; a = b; b = temp` |
| Build Strings | `"".join(parts)` | `s += part` in loop |
| Membership | `x in set_or_dict` | `x in list` (for large) |
| File I/O | `with open(...) as f:` | Manual `f.close()` |
| Truthiness | `if items:` | `if len(items) > 0:` |
| None Check | `if x is None:` | `if x == None:` |

---

## 🛑 FILE OPERATION CHECKPOINT (BLOCKING)

**Before EVERY `Write` or `Edit` tool call on a `.py` file:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🛑 STOP - PYTHON SKILL CHECK                                    ║
║                                                                  ║
║  You are about to modify a .py file.                             ║
║                                                                  ║
║  QUESTION: Is /python skill currently active?                    ║
║                                                                  ║
║  If YES → Proceed with the edit                                  ║
║  If NO  → STOP! Invoke /python FIRST, then edit                  ║
║                                                                  ║
║  This check applies to:                                          ║
║  ✗ Write tool with file_path ending in .py                       ║
║  ✗ Edit tool with file_path ending in .py                        ║
║  ✗ ANY Python file, regardless of conversation topic             ║
║                                                                  ║
║  Examples that REQUIRE this skill:                               ║
║  - "update the schemas" (edits schemas.py)                       ║
║  - "fix the import" (edits any .py file)                         ║
║  - "add logging" (edits Python code)                             ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why this matters:** In session 1ea73ffd, Claude edited 3+ Python files without
invoking the Python skill, leading to potential style/pattern inconsistencies.

---

## 🔄 RESUMED SESSION CHECKPOINT

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - PYTHON SKILL VERIFICATION                │
│                                                             │
│  Before continuing:                                         │
│  1. Type hints on all functions?                            │
│  2. Pydantic v2 for API validation?                         │
│  3. ABOUTME headers on new files?                           │
│  4. Run: ruff check <file>.py && mypy <file>.py             │
│  5. Re-invoke /python if skill context was lost             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Patterns

### Iteration

```python
# Direct iteration
for item in items:
    process(item)

# With index
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Parallel iteration
for name, score in zip(names, scores, strict=True):
    process(name, score)

# Reversed/sorted (no copy)
for item in reversed(items):
    process(item)
```

### Dictionaries

```python
# Safe access with default
port = config.get("port", 8080)

# Initialize-if-missing
groups: dict[str, list[str]] = {}
groups.setdefault(category, []).append(item)

# Merge dicts (Python 3.9+)
merged = defaults | overrides

# Dict comprehension
squares = {n: n**2 for n in range(10)}
```

### Comprehensions

```python
# List comprehension
squared = [x**2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

# Generator expression (memory efficient)
total = sum(x**2 for x in range(1_000_000))
any_match = any(item.is_valid for item in items)

# Set comprehension
unique_domains = {email.split("@")[1] for email in emails}
```

### Unpacking

```python
# Basic
x, y, z = coordinates
first, *rest = items
a, b = b, a  # Swap

# Dict unpacking
combined = {**defaults, **overrides}
connect(**config)  # Pass as kwargs
```

---

## Type Hints

### Basic Types

```python
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times

def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

### Optional and Union

```python
def find_user(user_id: int) -> User | None:
    return db.get(user_id)

def process(value: int | str | None) -> str:
    if value is None:
        return "none"
    return str(value)
```

### Generic Collections

```python
from collections.abc import Sequence, Mapping, Iterable, Callable

def process_items(items: Sequence[str]) -> list[str]:
    return [item.upper() for item in items]

def apply_func(data: Iterable[int], func: Callable[[int], int]) -> list[int]:
    return [func(x) for x in data]
```

---

## Pydantic v2 (Quick Reference)

Use Pydantic for API validation and serialization. **Full patterns**: `references/pydantic-patterns.md`

```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    is_active: bool = True

# Parse and validate
user = User.model_validate({"id": 1, "email": "test@example.com", "name": "Alice"})

# Serialize
user.model_dump()       # To dict
user.model_dump_json()  # To JSON
```

### When to Use What

| Data Type | Use |
|-----------|-----|
| API request/response | Pydantic BaseModel |
| External JSON/dict shape | TypedDict (type hints only) |
| Internal data container | dataclass |
| Configuration | pydantic-settings |

---

## Error Handling

### Catch Specific Exceptions

```python
try:
    value = int(user_input)
except ValueError:
    print("Invalid number")
except TypeError:
    print("Wrong type")

# DON'T: bare except
try:
    value = int(user_input)
except:  # Catches KeyboardInterrupt too!
    pass
```

### EAFP (Pythonic)

```python
# EAFP: Easier to Ask Forgiveness than Permission
try:
    value = mapping[key]
except KeyError:
    value = default

# vs LBYL: Look Before You Leap
if key in mapping:
    value = mapping[key]
else:
    value = default
```

### Custom Exceptions

```python
class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

def validate_email(email: str) -> str:
    if "@" not in email:
        raise ValidationError("email", "Must contain @")
    return email.lower()
```

---

## Context Managers

```python
# File handling (always use with)
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Multiple files
with open("in.txt") as infile, open("out.txt", "w") as outfile:
    outfile.write(infile.read().upper())
```

---

## String Handling

```python
# f-strings
name = "Alice"
score = 95.678
print(f"Score: {score:.2f}")  # 95.68
print(f"{1000000:,}")  # 1,000,000
print(f"{x=}")  # Debug: x=42

# String building (use join, not +=)
result = " ".join(parts)
```

---

## Best Practices

### DO

- Use meaningful variable names
- Prefer composition over inheritance
- Keep functions small and focused
- Use type hints consistently
- Use `pathlib.Path` for file paths
- Use `logging` instead of print

### DON'T

- Use mutable default arguments: `def f(items=[]):`
- Modify lists while iterating
- Use `from module import *`
- Catch bare `except:`
- Use `eval()` with untrusted input

---

## Quality Tools

```bash
# Linting
ruff check .
ruff check --fix .

# Type checking
mypy src/

# Formatting
ruff format .
```

---

## Advanced Patterns

See `references/advanced-patterns.md` for:
- itertools (chain, islice, groupby, product)
- functools (partial, lru_cache, cached_property)
- collections (defaultdict, Counter, deque)
- Custom context managers
- Generator functions
- Dataclasses
- Enumerations
- TypedDict for data contracts

---

## References

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Real Python - Idiomatic Python](https://realpython.com/learning-paths/writing-idiomatic-python/)
