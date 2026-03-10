---
name: python-best-practices
description:
  Modern Python 3.12+ patterns your AI agent should use. Type hints, async/await, Pydantic v2, uv,
  match statements, and project structure.
metadata:
  tags: python, type-hints, best-practices, async
---

## When to use

Use this skill when writing or reviewing Python code targeting Python 3.12+. It enforces modern type
hints, async patterns, Pydantic v2 API, project structure, and standard library usage. Agents
trained on older codebases often emit outdated patterns; this skill corrects that.

## Critical Rules

### 1. Use modern type hint syntax

**Wrong:**

```python
from typing import Union, List, Dict, Optional

def process(items: List[str]) -> Optional[Dict[str, Union[int, str]]]:
    ...
```

**Correct:**

```python
def process(items: list[str]) -> dict[str, int | str] | None:
    ...
```

**Why:** `list[str]` and `X | Y` are built-in in Python 3.9+ (PEP 585, PEP 604). Importing
`typing.List`, `typing.Union`, `typing.Optional` is verbose and deprecated for built-in generics.

### 2. Use type parameter syntax (PEP 695, Python 3.12+)

**Wrong:**

```python
from typing import TypeVar

T = TypeVar("T")

def max(args: list[T]) -> T:
    ...
```

**Correct:**

```python
def max[T](args: list[T]) -> T:
    ...
```

**Why:** PEP 695 type parameters are simpler and local to the function/class. Same for generic
classes: `class Bag[T]:` instead of `class Bag(Generic[T]):`.

### 3. Use match/case instead of if/elif chains for pattern matching

**Wrong:**

```python
def http_error(status: int) -> str:
    if status == 400:
        return "Bad request"
    elif status == 404:
        return "Not found"
    elif status == 418:
        return "I'm a teapot"
    else:
        return "Something's wrong"
```

**Correct:**

```python
def http_error(status: int) -> str:
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong"
```

**Why:** Structural pattern matching (PEP 634) is clearer for disjoint cases and supports
destructuring. Use `case 401 | 403 | 404:` for multiple literals.

### 4. Use Pydantic v2 API, never v1

**Wrong:**

```python
from pydantic import BaseModel, validator, root_validator

class Model(BaseModel):
    x: list[int]

    class Config:
        validate_assignment = True

    @validator("x", each_item=True)
    def validate_x(cls, v):
        return v * 2

    @root_validator
    def check_a_b(cls, values):
        ...
```

**Correct:**

```python
from pydantic import BaseModel, field_validator, model_validator, ConfigDict

class Model(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    x: list[int]

    @field_validator("x", mode="each")
    @classmethod
    def validate_x(cls, v: int) -> int:
        return v * 2

    @model_validator(mode="after")
    def check_a_b(self) -> "Model":
        ...
        return self
```

**Why:** Pydantic v1 decorators and `class Config` are deprecated. v2 uses `model_config`,
`field_validator`, `model_validator` with explicit modes.

### 5. Use uv for package management in new projects

**Wrong:**

```bash
pip install -r requirements.txt
poetry init
```

**Correct:**

```bash
uv init
uv add requests pydantic
uv sync
```

**Why:** uv is fast, has a modern lockfile, and supports pyproject.toml natively. Prefer it for new
projects.

### 6. Use pyproject.toml for project configuration

**Wrong:**

```python
# setup.py
from setuptools import setup
setup(name="myapp", version="0.1", ...)
```

**Correct:**

```toml
# pyproject.toml
[project]
name = "myapp"
version = "0.1"
dependencies = ["requests"]
```

**Why:** setup.py and setup.cfg are legacy. pyproject.toml (PEP 517/518) is the standard.

### 7. Use pathlib.Path instead of os.path

**Wrong:**

```python
import os
path = os.path.join(os.getcwd(), "data", "file.txt")
if os.path.exists(path):
    with open(path) as f:
        ...
```

**Correct:**

```python
from pathlib import Path
path = Path.cwd() / "data" / "file.txt"
if path.exists():
    path.read_text()
```

**Why:** pathlib is object-oriented, clearer, and cross-platform. Prefer
`Path.read_text()`/`write_text()` over `open()` for simple reads/writes.

### 8. Use f-strings instead of .format() or % formatting

**Wrong:**

```python
"User %s has %d items" % (name, count)
"User {} has {} items".format(name, count)
```

**Correct:**

```python
f"User {name} has {count} items"
```

**Why:** f-strings are faster and more readable.

### 9. Use dataclasses or Pydantic for structured data, not plain dicts

**Wrong:**

```python
def get_user() -> dict:
    return {"name": "Alice", "age": 30}
```

**Correct:**

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

def get_user() -> User:
    return User(name="Alice", age=30)
```

**Why:** Structured types give type safety and IDE support. Use Pydantic when you need validation.

### 10. Use asyncio.TaskGroup instead of asyncio.gather (Python 3.11+)

**Wrong:**

```python
import asyncio
results = await asyncio.gather(f1(), f2(), f3())
```

**Correct:**

```python
import asyncio
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(f1())
    t2 = tg.create_task(f2())
    t3 = tg.create_task(f3())
results = (t1.result(), t2.result(), t3.result())
```

**Why:** TaskGroup propagates exceptions correctly and cancels other tasks on failure.

### 11. Use exception groups and except\* (Python 3.11+)

**Wrong:**

```python
try:
    ...
except (ValueError, TypeError) as e:
    ...
```

**Correct (when dealing with ExceptionGroup from concurrency):**

```python
try:
    ...
except* TypeError as e:
    print(f"caught {type(e)} with nested {e.exceptions}")
except* OSError as e:
    ...
```

**Why:** `except*` handles ExceptionGroups from asyncio and concurrent tasks. Use when catching from
TaskGroup or similar.

### 12. Use tomllib for TOML parsing (Python 3.11+ stdlib)

**Wrong:**

```python
import toml
data = toml.load("pyproject.toml")
```

**Correct:**

```python
import tomllib
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
```

**Why:** tomllib is built-in; no extra dependency. Read in binary mode.

### 13. Use typing.override decorator (Python 3.12+)

**Wrong:**

```python
class Child(Parent):
    def method(self) -> str:
        return "child"
```

**Correct:**

```python
from typing import override

class Child(Parent):
    @override
    def method(self) -> str:
        return "child"
```

**Why:** @override makes intent explicit and catches typos in method names.

### 14. Use structural pattern matching with guards

**Wrong:**

```python
match x:
    case (a, b):
        if a > b:
            ...
```

**Correct:**

```python
match x:
    case (a, b) if a > b:
        ...
```

**Why:** Guards (`if`) keep logic in the pattern and avoid nested conditionals.

### 15. Prefer collections.abc over typing for abstract types

**Wrong:**

```python
from typing import Iterable, Mapping
```

**Correct:**

```python
from collections.abc import Iterable, Mapping
```

**Why:** collections.abc is the canonical source for ABCs. typing re-exports them but
collections.abc is preferred for runtime checks.

## Patterns

### Generic class with type parameter

```python
class Bag[T]:
    def __iter__(self) -> Iterator[T]:
        ...
    def add(self, arg: T) -> None:
        ...
```

### Generic type alias

```python
type ListOrSet[T] = list[T] | set[T]
```

### Pydantic model_validator before mode

```python
@model_validator(mode="before")
@classmethod
def check_card_number_not_present(cls, data: Any) -> Any:
    if isinstance(data, dict) and "card_number" in data:
        raise ValueError("'card_number' should not be included")
    return data
```

### Match with multiple literals

```python
case 401 | 403 | 404:
    return "Not allowed"
```

## Anti-Patterns

- Never use `from typing import List, Dict, Union, Optional` for built-in generics; use `list`,
  `dict`, `X | Y`, `X | None`.
- Never use `@validator` or `@root_validator` or `class Config` with Pydantic; use v2 API.
- Never use `os.path` for new code; use `pathlib.Path`.
- Never use `setup.py` or `setup.cfg`; use `pyproject.toml`.
- Never use `%` or `.format()` when f-strings are available.
- Never use `toml` package; use stdlib `tomllib` (Python 3.11+).
- Never use `TypeVar` for simple generics when Python 3.12+ type parameter syntax applies.
- Never use `asyncio.gather` for structured concurrency when TaskGroup is available (3.11+).
- Never use plain dicts for typed structured data when dataclasses or Pydantic models fit.
- Never use `from typing import Iterable, Mapping`; use `from collections.abc import ...`.
