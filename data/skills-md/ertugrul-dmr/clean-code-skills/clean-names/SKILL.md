---
name: clean-names
description: Use when naming, renaming, or fixing names of variables, functions, classes, or modules in Python. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names

## N1: Choose Descriptive Names

Names should reveal intent. If a name requires a comment, it doesn't reveal its intent.

```python
# Bad - what is d?
d = 86400

# Good - obvious meaning
SECONDS_PER_DAY = 86400

# Bad - what does this function do?
def proc(lst):
    return [x for x in lst if x > 0]

# Good - intent is clear
def filter_positive_numbers(numbers):
    return [n for n in numbers if n > 0]
```

## N2: Choose Names at the Appropriate Level of Abstraction

Don't pick names that communicate implementation; choose names that reflect the level of abstraction of the class or function.

```python
# Bad - too implementation-specific
def get_dict_of_user_ids_to_names():
    ...

# Good - abstracts the data structure
def get_user_directory():
    ...
```

## N3: Use Standard Nomenclature Where Possible

Use terms from the domain, design patterns, or well-known conventions.

```python
# Good - uses pattern name
class UserFactory:
    def create(self, data): ...

# Good - uses domain term
def calculate_amortization(principal, rate, term): ...
```

## N4: Unambiguous Names

Choose names that make the workings of a function or variable unambiguous.

```python
# Bad - ambiguous
def rename(old, new):
    ...

# Good - clear what's being renamed
def rename_file(old_path: Path, new_path: Path):
    ...
```

## N5: Use Longer Names for Longer Scopes

Short names are fine for tiny scopes. Longer scopes need longer, more descriptive names.

```python
# Good - short name for tiny scope
total = sum(x for x in numbers)

# Good - longer name for module-level constant
MAX_RETRY_ATTEMPTS_BEFORE_FAILURE = 5

# Bad - short name at module level
MAX = 5
```

## N6: Avoid Encodings

Don't encode type or scope information into names. Modern editors make this unnecessary.

```python
# Bad - Hungarian notation
str_name = "Alice"
lst_users = []
i_count = 0

# Good - clean names
name = "Alice"
users = []
count = 0

# Bad - interface prefix
class IUserRepository:
    ...

# Good - just name it
class UserRepository:
    ...
```

## N7: Names Should Describe Side Effects

If a function does something beyond what its name suggests, the name is misleading.

```python
# Bad - name doesn't mention file creation
def get_config():
    if not config_path.exists():
        config_path.write_text("{}")  # Hidden side effect!
    return json.loads(config_path.read_text())

# Good - name reveals behavior
def get_or_create_config():
    if not config_path.exists():
        config_path.write_text("{}")
    return json.loads(config_path.read_text())
```

## Quick Reference

| Rule | Principle | Example |
|------|-----------|---------|
| N1 | Descriptive names | `SECONDS_PER_DAY` not `d` |
| N2 | Right abstraction level | `get_user_directory()` not `get_dict_of_...` |
| N3 | Standard nomenclature | `UserFactory`, `calculate_amortization` |
| N4 | Unambiguous | `rename_file(old_path, new_path)` |
| N5 | Length matches scope | Short for loops, long for globals |
| N6 | No encodings | `users` not `lst_users` |
| N7 | Describe side effects | `get_or_create_config()` |
