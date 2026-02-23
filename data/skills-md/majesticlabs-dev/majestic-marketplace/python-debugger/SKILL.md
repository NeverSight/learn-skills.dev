---
name: python-debugger
description: Debug Python errors, exceptions, and unexpected behavior. Analyzes tracebacks, reproduces issues, identifies root causes, and provides fixes.
allowed-tools: Read Write Edit Grep Glob Bash WebSearch
---

# Python Debugger

## Debugging Process

1. Understand the Error -> 2. Reproduce -> 3. Isolate -> 4. Identify Root Cause -> 5. Fix -> 6. Verify

## Step 1: Understand the Error

### Reading Tracebacks

```
Traceback (most recent call last):        <- Read bottom to top
  File "app.py", line 45, in main         <- Entry point
    result = process_data(data)           <- Call chain
  File "processor.py", line 23, in process_data
    return transform(item)                <- Getting closer
  File "transformer.py", line 12, in transform
    return item["value"] / item["count"]  <- Error location
ZeroDivisionError: division by zero       <- The actual error
```

Common error types: see [references/python-error-types.md](references/python-error-types.md)

## Step 2: Reproduce the Issue

Create a minimal test case that triggers the error. Answer these questions:
- What input triggered this?
- Is it consistent or intermittent?
- When did it start happening?
- What changed recently?

## Step 3: Isolate the Problem

### Print Debugging

```python
def process_data(data):
    print(f"DEBUG: data type = {type(data)}")
    print(f"DEBUG: data = {data}")

    for i, item in enumerate(data):
        print(f"DEBUG: processing item {i}: {item}")
        result = transform(item)
        print(f"DEBUG: result = {result}")

    return results
```

### Using pdb

```python
import pdb

def problematic_function(x):
    pdb.set_trace()  # Execution stops here
    # Or use: breakpoint()  # Python 3.7+
    result = x * 2
    return result
```

pdb commands: see [references/pdb-commands.md](references/pdb-commands.md)

### Using icecream

```python
from icecream import ic

def calculate(x, y):
    ic(x, y)  # Prints: ic| x: 5, y: 0
    result = x / y
    ic(result)
    return result
```

## Step 4: Common Root Causes

- **None values**: Check return values before accessing attributes. Guard with `if x is None: raise ValueError(...)`
- **Type mismatches**: Add type hints, cast inputs explicitly. `int(a) + int(b)` not `a + b`
- **Mutable default arguments**: Use `def f(items=None):` then `items = items or []` inside
- **Circular imports**: Use lazy imports inside functions: `from .module import Class`
- **Async/await**: Missing `await` returns coroutine instead of result
- **Key/Index errors**: Use `.get(key, default)` for dicts, check `len()` for lists
- **Scope issues**: `global`/`nonlocal` declarations, closure variable capture in loops
- **Encoding**: Specify `encoding="utf-8"` in `open()` calls
- **Float precision**: Use `decimal.Decimal` or `math.isclose()` for comparisons
- **Resource leaks**: Use `with` statements for files, connections, locks

## Step 5: Fix Patterns

### Defensive Programming

```python
def safe_divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def safe_get(data: dict, key: str, default=None):
    return data.get(key, default)
```

### Input Validation

```python
def process_user(user_id: int, data: dict) -> dict:
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")

    required_fields = ["name", "email"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
```

### Exception Handling

```python
import logging

logger = logging.getLogger(__name__)

def fetch_user_data(user_id: int) -> dict:
    try:
        response = api_client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"HTTP error fetching user {user_id}: {e}")
        raise
    except requests.ConnectionError:
        logger.error(f"Connection failed for user {user_id}")
        raise ServiceUnavailableError("API unavailable")
```

## Step 6: Verify the Fix

```python
import pytest

def test_transform_handles_zero_count():
    """Verify fix for ZeroDivisionError."""
    data = {"value": 10, "count": 0}

    with pytest.raises(ValueError, match="count cannot be zero"):
        transform(data)

def test_transform_normal_case():
    """Verify normal operation still works."""
    data = {"value": 10, "count": 2}
    result = transform(data)
    assert result == 5
```

## Debugging Tools

### Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(),
    ],
)
```

### Profiling

```python
# Time profiling
import cProfile
cProfile.run("main()", "output.prof")

# Memory profiling
from memory_profiler import profile

@profile
def memory_heavy_function():
    # ...
```

### Using rich for better output

```python
from rich.traceback import install
install(show_locals=True)  # Enhanced tracebacks
```

## References

- [Debug Checklist](references/debug-checklist.md)
- [Common Error Types](references/python-error-types.md)
- [pdb Commands](references/pdb-commands.md)

## When to Use WebSearch

- Cryptic error messages
- Library-specific errors
- Version compatibility issues
- Undocumented behavior
