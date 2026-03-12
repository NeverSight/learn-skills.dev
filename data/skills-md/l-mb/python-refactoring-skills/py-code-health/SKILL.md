---
name: py-code-health
description: Detect and remove dead code, duplicate code, and unused imports. Consolidate similar code patterns into parametrized functions.
status: stable
---

# Python Code Health Maintenance

Remove dead code and consolidate duplication to keep codebase clean and maintainable.

## Objectives

1. Detect unused code (functions, classes, variables)
2. Find and remove dead code with high confidence
3. Identify duplicate code across files
4. Consolidate similar code into parametrized functions
5. Remove redundant imports and commented-out code

## Required Tools

**Add to `[dependency-groups]` dev**: `"vulture"`, `"pylint"`

- **vulture**: AST-based dead code detection
- **pylint**: Duplicate code detection

**Permissions**: Run py-quality-setup first to configure `.claude/settings.local.json` with all needed tool permissions.

## Dead Code Detection

### Find Unused Code

```bash
# Using vulture (primary tool)
vulture .                              # Find all unused code
vulture . --min-confidence 80          # High confidence only
vulture . --min-confidence 80 --sort-by-size  # Largest dead code first
vulture . --exclude=tests/,venv/,.venv/ # Exclude directories

# Generate report
vulture . --min-confidence 80 > dead_code_report.txt
```

### Interpret Vulture Output

```
unused function 'calculate_tax' (80% confidence)
src/billing.py:45

unused class 'LegacyProcessor' (90% confidence)
src/processors.py:123

unused variable 'debug_mode' (60% confidence)
src/config.py:12
```

**Confidence levels**:
- **60-70%**: May be false positive (dynamic imports, metaclasses, etc.)
- **80-89%**: Likely unused, verify before removing
- **90-100%**: Almost certainly unused

### Handle False Positives

Vulture may flag code that's actually used:

**1. Dynamic imports/calls**:
```python
# Flagged as unused but called dynamically
def plugin_handler():
    pass

# Called via: getattr(module, 'plugin_handler')()
```

**2. Framework conventions**:
```python
# Django models - fields used by ORM
class User(models.Model):
    email = models.EmailField()  # May be flagged but used by Django
```

**3. Public API**:
```python
# Part of library's public API, used by external code
def public_function():
    pass
```

**Solutions**:
- Add to whitelist file: `vulture . whitelist.py`
- Add comment: `# pragma: no cover` or custom marker
- Accept false positives for public APIs

4. Code that *should* be used, but isn't:

For example, constants, magic numbers, type definitions, or even functions may appear unused. But this may in 
fact be the issue! (Consider partial refactoring, or other causes.)

Before eliminating apparently dead code, validate that no similar patterns that should reference it exist. If they do, instead fix the call/use sites.

### Remove Dead Code

```python
# BEFORE - Unused functions cluttering codebase
def old_calculate_price(item):  # Last used 2 years ago
    return item.cost * 1.1

def deprecated_handler(data):  # Replaced by new_handler
    pass

# AFTER - Clean, only active code remains
# (Dead code completely removed)
```

## Duplicate Code Detection

### Find Duplicates

```bash
# Using pylint (detects similar code blocks)
pylint --disable=all --enable=duplicate-code --recursive=y .

# Configure minimum similar lines (default: 4)
pylint --disable=all --enable=duplicate-code --duplicate-code-min-lines=6 --recursive=y .

# JSON output for parsing
pylint --disable=all --enable=duplicate-code --output-format=json --recursive=y . > duplication.json
```

### Interpret Pylint Output

```
Similar lines in 2 files
src/auth.py:45-60
src/admin.py:123-138

def validate_credentials(username, password):
    if not username or not password:
        return False
    user = db.get_user(username)
    if not user:
        return False
    return check_password(password, user.password_hash)
```

## Consolidation Patterns

### Parametrize Similar Functions

```python
# BEFORE - Duplicate code with slight variations
def process_user(data: dict) -> User:
    if not data.get("email"):
        raise ValueError("Missing email")
    if not data.get("name"):
        raise ValueError("Missing name")
    return User(email=data["email"], name=data["name"])

def process_admin(data: dict) -> Admin:
    if not data.get("email"):
        raise ValueError("Missing email")
    if not data.get("name"):
        raise ValueError("Missing name")
    return Admin(email=data["email"], name=data["name"])

# AFTER - Single parametrized function
T = TypeVar('T', User, Admin)

def process_entity(data: dict, entity_class: type[T]) -> T:
    if not data.get("email"):
        raise ValueError("Missing email")
    if not data.get("name"):
        raise ValueError("Missing name")
    return entity_class(email=data["email"], name=data["name"])

# Usage
user = process_entity(data, User)
admin = process_entity(data, Admin)
```

### Extract Common Logic

```python
# BEFORE - Duplicated validation in multiple functions
def create_user(email: str, age: int) -> User:
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    if age < 0 or age > 150:
        raise ValueError("Invalid age")
    return User(email=email, age=age)

def update_user(user_id: int, email: str, age: int) -> User:
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    if age < 0 or age > 150:
        raise ValueError("Invalid age")
    user = get_user(user_id)
    user.email = email
    user.age = age
    return user

# AFTER - Extract common validation
def validate_email(email: str) -> None:
    if not email or "@" not in email:
        raise ValueError("Invalid email")

def validate_age(age: int) -> None:
    if age < 0 or age > 150:
        raise ValueError("Invalid age")

def create_user(email: str, age: int) -> User:
    validate_email(email)
    validate_age(age)
    return User(email=email, age=age)

def update_user(user_id: int, email: str, age: int) -> User:
    validate_email(email)
    validate_age(age)
    user = get_user(user_id)
    user.email = email
    user.age = age
    return user
```

### Use Configuration Over Duplication

```python
# BEFORE - Similar handlers with different values
def process_csv_file(path: str) -> list:
    return parse_file(path, delimiter=",", encoding="utf-8", skip_header=True)

def process_tsv_file(path: str) -> list:
    return parse_file(path, delimiter="\t", encoding="utf-8", skip_header=True)

def process_psv_file(path: str) -> list:
    return parse_file(path, delimiter="|", encoding="utf-8", skip_header=True)

# AFTER - Configuration-driven
FILE_CONFIGS = {
    "csv": {"delimiter": ",", "encoding": "utf-8", "skip_header": True},
    "tsv": {"delimiter": "\t", "encoding": "utf-8", "skip_header": True},
    "psv": {"delimiter": "|", "encoding": "utf-8", "skip_header": True},
}

def process_file(path: str, file_type: str) -> list:
    config = FILE_CONFIGS[file_type]
    return parse_file(path, **config)
```

## Remove Commented Code

Commented-out code is a form of dead code:

```python
# BEFORE - Cluttered with old code
def calculate_total(items: list) -> float:
    # Old implementation - kept for reference
    # total = 0
    # for item in items:
    #     total += item.price * item.quantity
    # return total

    # Another old version
    # return sum(item.price * item.quantity for item in items)

    # Current implementation
    return sum(item.total_price() for item in items)

# AFTER - Clean, rely on git history
def calculate_total(items: list) -> float:
    return sum(item.total_price() for item in items)
```

**Rationale**: Git history preserves old implementations. Commented code creates noise.


## Verification Checklist

- [ ] `vulture . --min-confidence 80` reports no dead code (or only accepted false positives)
- [ ] `pylint --disable=all --enable=duplicate-code` reports no duplicate blocks >6 lines
- [ ] No commented-out code blocks remain
- [ ] All tests pass after removals
- [ ] Code coverage maintained or improved
- [ ] Whitelist file created for intentional false positives (if needed)

## Examples

**Example: Code health cleanup workflow**
```
1. Scan: vulture . --min-confidence 80; pylint --disable=all --enable=duplicate-code --recursive=y .
2. Found: 5 unused functions (67 lines), 3 duplicate blocks (45 lines)
3. Remove: Verify unused code with Explore agent, delete confirmed dead code
4. Consolidate: Extract duplicates to shared utilities
5. Result: -112 lines total, tests pass, coverage improved to 86%
```

**Example: Handle false positives**
```
1. Scan: vulture . --min-confidence 80
2. Found: public_api_function flagged as unused (actually part of library API)
3. Create whitelist.py with: public_api_function  # Used by external consumers
4. Re-scan: vulture . whitelist.py --min-confidence 80
5. Result: False positive suppressed, real dead code still detected
```

**Example: Consolidate duplicate validation**
```
1. Scan: pylint --disable=all --enable=duplicate-code --recursive=y .
2. Found: Same validation logic in create_user() and update_user()
3. Extract: Create validate_user_data() helper function
4. Update: Both functions now call validate_user_data()
5. Result: -15 lines, single source of truth for validation
```

## Related Skills

- **Prerequisites**: py-quality-setup (tool configuration), py-test-quality (safety net before removing code)
- **Next steps**: py-complexity (reduce complexity after cleanup)
- **See also**: py-security (check security before major changes)
