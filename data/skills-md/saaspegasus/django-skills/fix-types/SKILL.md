---
name: fix-types
description: Interactively fix any type checking issues in Python code
allowed-tools: [
    Bash(uv run mypy *),
]
---

## Your task

To fix types, do the following.

1. First run the type checker to see what the issues are:
    ```
    uv run mypy .
    ```
2. Group the errors you find in to logical buckets.
3. For each bucket of errors, go through the errors one at a time, tell me the fix you want to apply, and then ask if
   I have any questions or suggestions before proceeding.
4. Only once I approve, apply the fix and move onto the next error in the bucket.
5. Once you've completed a bucket, ask me if I'd like to move on to the next bucket.

#### Prefer `cast()` over `type: ignore`

When mypy can't infer the correct type, prefer using `cast()` over `# type: ignore`:

```python
# Preferred - documents the expected type
choices = cast(list[tuple[str, str]], field.choices)

# Avoid when cast is possible - just silences the error
choices = list(field.choices)  # type: ignore[arg-type]
```

**Why:** `cast()` explicitly documents what type you expect, making the code more readable and maintainable. It also doesn't silence other potential errors on the same line.

#### Prefer proper errors over assertions for null checks

When adding null checks to satisfy mypy, prefer raising proper exceptions over using `assert`:

```python
# Preferred - proper error handling
if obj.related_field is None:
    raise ValueError("Object must have a related field")
result = obj.related_field.some_method()

# Avoid - assertions can be disabled with -O flag
assert obj.related_field is not None
result = obj.related_field.some_method()
```

**Why:** Assertions can be disabled in production with `python -O`, making them unreliable for runtime validation. Proper exceptions ensure the check always runs and provides better error handling.

#### When using `type: ignore`, add a comment

If `type: ignore` is necessary (e.g., mypy limitation with valid code), always add a short explanation:

```python
# Good - explains why the ignore is needed
self.tier = tier  # type: ignore[misc]  # mypy can't handle Enum tuple values with custom __init__

# Bad - no explanation
self.tier = tier  # type: ignore[misc]
```

#### Type Hints for Django Lazy Translation Strings

When using type hints with Django's lazy translation strings (`gettext_lazy`), use the following pattern to avoid mypy errors while keeping the code working in production (where `django-stubs-ext` is not installed):

```python
from __future__ import annotations  # Must be the first import

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise

# Then use StrOrPromise in type hints
def my_function(name: StrOrPromise) -> StrOrPromise:
    ...

class MyData:
    title: StrOrPromise
    description: StrOrPromise
```

**Why this pattern:**
- `from __future__ import annotations` makes type annotations strings at runtime (not evaluated)
- `if TYPE_CHECKING:` ensures the import only happens during type checking, not at runtime
- `django-stubs-ext` is a dev dependency and won't be available in production
- This pattern allows both regular strings and lazy translation strings to be accepted
