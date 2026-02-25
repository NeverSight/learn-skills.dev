---
name: implement-value-object
description: |
  Creates immutable domain value objects using frozen dataclass pattern with validation.
  Use when implementing domain value objects, creating immutable data structures, or
  adding validation to values. Covers @dataclass(frozen=True), object.__setattr__()
  pattern in __post_init__, factory methods (from_string, from_dict, from_content),
  and validation in frozen context. Triggers on "create value object for X", "implement
  immutable Y value", "add validation to Z value", or "build value object".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
---

Works with Python dataclasses in domain/value_objects/ and domain/values/ directories.
# implement-value-object

## Purpose

Create immutable domain value objects using the frozen dataclass pattern with proper validation, factory methods, and immutability guarantees enforced at the type system level.

## When to Use

Use this skill when:
- **Implementing domain value objects** - Creating validated, immutable domain concepts
- **Creating immutable data structures** - Building type-safe value containers
- **Adding validation to values** - Ensuring domain constraints are enforced

**Trigger phrases:**
- "Create a value object for X"
- "Implement immutable Y value"
- "Add validation to Z value"
- "Build value object with validation"

## Quick Start

Create immutable domain value objects using the frozen dataclass pattern with proper validation, factory methods, and immutability guarantees enforced at the type system level.

**Most common use case:**

For a simple validated value object:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EmailAddress:
    """Immutable email address value object."""

    value: str

    def __post_init__(self) -> None:
        """Validate email format."""
        if not self.value:
            raise ValueError("Email address cannot be empty")
        if "@" not in self.value:
            raise ValueError(f"Invalid email format: {self.value}")
```

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Immutable domain value objects with frozen dataclass pattern
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Define Frozen Dataclass](#step-1-define-frozen-dataclass) - Basic immutable structure
  - [Step 2: Add Validation in __post_init__](#step-2-add-validation-in-__post_init__) - Validation while respecting immutability
  - [Step 3: Add Factory Methods](#step-3-add-factory-methods) - Convenient constructors for different input types
  - [Step 4: Add String Representations](#step-4-add-string-representations) - Useful string representations
  - [Step 5: Add Domain Behavior](#step-5-add-domain-behavior) - Methods expressing domain operations
  - [Step 6: Add Type Hints and Documentation](#step-6-add-type-hints-and-documentation) - Full type safety
- [Examples](#examples) - 4 production-ready patterns
  - [Example 1: Simple String Value Object](#example-1-simple-string-value-object) - Basic validation pattern
  - [Example 2: Path Value Object with Normalization](#example-2-path-value-object-with-normalization) - Type coercion in frozen context
  - [Example 3: Hash Value Object with Factory](#example-3-hash-value-object-with-factory) - Computing values from content
  - [Example 4: Multi-Field Value Object with Validation](#example-4-multi-field-value-object-with-validation) - Complex constraints

### Advanced Topics
- [Requirements](#requirements) - Dependencies and environment setup
- [Common Patterns](#common-patterns) - Reusable implementation patterns
  - [Pattern: Computed Properties](#pattern-computed-properties) - Derived values with @property
  - [Pattern: Type Coercion in Frozen Context](#pattern-type-coercion-in-frozen-context) - Ensuring type consistency
  - [Pattern: Validation with Custom Errors](#pattern-validation-with-custom-errors) - Clear error messages
  - [Pattern: Serialization](#pattern-serialization) - Dictionary conversion support
- [Testing Value Objects](#testing-value-objects) - Test strategies for validation, immutability, equality, factories, serialization
- [File Locations](#file-locations) - Domain layer placement conventions
- [See Also](#see-also) - Templates, examples, architecture references

### Utility Scripts
- [Convert to Value Object](./scripts/convert_to_value_object.py) - Analyze codebase to suggest value object candidates
- [Generate Value Object](./scripts/generate_value_object.py) - Generate value objects with validation, factory methods, and tests
- [Validate Value Objects](./scripts/validate_value_objects.py) - Validate value object patterns in the codebase

## Purpose

Create immutable domain value objects using the frozen dataclass pattern with proper validation, factory methods, and immutability guarantees enforced at the type system level.

## Instructions

### Step 1: Define Frozen Dataclass

Create the basic immutable structure:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class YourValueObject:
    """Immutable value object representing [domain concept].

    Encapsulates [what logic/behavior].
    """

    value: str  # Primary value
    # Optional additional fields for metadata
```

**Key points:**
- Always use `@dataclass(frozen=True)` for immutability
- Add comprehensive docstring explaining domain meaning
- Use `value` as primary field name for simple value objects
- All fields are immutable after construction

### Step 2: Add Validation in __post_init__

Validate constraints while respecting immutability:

```python
def __post_init__(self) -> None:
    """Validate value object constraints."""
    # Validation checks (raise ValueError on failure)
    if not self.value:
        raise ValueError("Value cannot be empty")

    # For type coercion or normalization in frozen context:
    if not isinstance(self.value, ExpectedType):
        object.__setattr__(self, "value", ExpectedType(self.value))

    # For normalization (e.g., path resolution):
    object.__setattr__(self, "value", self.normalize(self.value))
```

**CRITICAL: Modifying Frozen Dataclass Fields**

Since `frozen=True` prevents normal attribute assignment, use `object.__setattr__()` to modify fields during `__post_init__`:

```python
# ❌ WRONG - Will raise FrozenInstanceError
def __post_init__(self) -> None:
    self.value = self.value.lower()  # FAILS with frozen=True

# ✅ CORRECT - Use object.__setattr__()
def __post_init__(self) -> None:
    object.__setattr__(self, "value", self.value.lower())
```

**Validation patterns:**
- Empty checks: `if not self.value: raise ValueError(...)`
- Format validation: `if not re.match(pattern, self.value): raise ValueError(...)`
- Type coercion: `object.__setattr__(self, "field", Type(field))`
- Normalization: `object.__setattr__(self, "value", normalized_value)`

### Step 3: Add Factory Methods

Provide convenient constructors for different input types:

```python
@classmethod
def from_string(cls, value_str: str) -> "YourValueObject":
    """Create from string representation.

    Args:
        value_str: String to parse

    Returns:
        YourValueObject instance
    """
    return cls(value=value_str)

@classmethod
def from_dict(cls, data: dict) -> "YourValueObject":
    """Create from dictionary representation.

    Args:
        data: Dictionary with value object data

    Returns:
        YourValueObject instance
    """
    return cls(value=data["value"])

@classmethod
def from_content(cls, content: str) -> "YourValueObject":
    """Create from raw content (e.g., compute hash).

    Args:
        content: Raw content to process

    Returns:
        YourValueObject instance
    """
    # Process content (e.g., hash it)
    processed = process(content)
    return cls(value=processed)
```

**Common factory method patterns:**
- `from_string()` - Parse string representation
- `from_dict()` - Deserialize from dictionary
- `from_content()` - Compute value from content (hashes)
- `from_components()` - Build from multiple parts
- `from_bytes()` - Create from binary data

### Step 4: Add String Representations

Provide useful string representations:

```python
def __str__(self) -> str:
    """User-friendly string representation.

    Returns:
        The value as a string
    """
    return str(self.value)

def __repr__(self) -> str:
    """Developer-friendly representation.

    Returns:
        String showing class and value
    """
    return f"YourValueObject('{self.value}')"
```

**For long values (like hashes), truncate in __repr__:**

```python
def __repr__(self) -> str:
    """Developer-friendly representation."""
    if len(self.value) > 8:
        return f"FileHash('{self.value[:8]}...')"
    return f"FileHash('{self.value}')"
```

### Step 5: Add Domain Behavior

Add methods that express domain operations:

```python
@property
def short_version(self) -> str:
    """Get shortened version for display."""
    return self.value[:8]

def matches_pattern(self, pattern: str) -> bool:
    """Check if value matches a pattern."""
    import fnmatch
    return fnmatch.fnmatch(self.value, pattern)

def to_dict(self) -> dict:
    """Convert to dictionary representation."""
    return {
        "value": self.value,
        # Include computed properties
        "short": self.short_version,
    }
```

**Common domain behaviors:**
- Comparison operations (equality is automatic with dataclass)
- Pattern matching
- Format conversion
- Computed properties
- Dictionary serialization

### Step 6: Add Type Hints and Documentation

Ensure full type safety:

```python
from typing import Optional

@dataclass(frozen=True)
class ComplexValueObject:
    """Detailed docstring."""

    value: str
    metadata: Optional[str] = None  # Optional fields need defaults

    def operation(self, param: str) -> "ComplexValueObject":
        """Return type hints use string for forward reference."""
        # Operations that return new instances (immutability)
        return ComplexValueObject(value=f"{self.value}:{param}")
```

## Examples


See [examples/detailed-examples.md](./examples/detailed-examples.md) for comprehensive examples including:
- Simple string value objects with validation
- Path value objects with normalization and type coercion
- Hash value objects with factory methods
- Multi-field value objects with complex validation


## Requirements

- Python 3.10+ (for `dataclasses` and type union syntax `X | None`)
- No external dependencies for basic value objects
- Optional: `xxhash` for fast hashing (`uv pip install xxhash`)

## Common Patterns

### Pattern: Computed Properties

Use `@property` for derived values:

```python
@property
def short_id(self) -> str:
    """Get shortened version of identity."""
    parts = self.value.split(":")
    return parts[-1] if parts else self.value
```

### Pattern: Type Coercion in Frozen Context

When you need to ensure type consistency:

```python
def __post_init__(self) -> None:
    """Ensure value is correct type."""
    if not isinstance(self.value, Path):
        object.__setattr__(self, "value", Path(self.value))
```

### Pattern: Validation with Custom Errors

Provide clear error messages:

```python
def __post_init__(self) -> None:
    """Validate with descriptive errors."""
    if not self.value:
        raise ValueError(f"{self.__class__.__name__} value cannot be empty")
    if len(self.value) < 3:
        raise ValueError(f"{self.__class__.__name__} must be at least 3 characters")
```

### Pattern: Serialization

Support dictionary conversion:

```python
def to_dict(self) -> dict:
    """Convert to dictionary for serialization."""
    return {
        "value": self.value,
        # Include any metadata or computed properties
    }

@classmethod
def from_dict(cls, data: dict) -> "YourValueObject":
    """Deserialize from dictionary."""
    return cls(value=data["value"])
```

## Testing Value Objects

Value objects should be tested for:

1. **Validation**: Ensure invalid inputs raise `ValueError`
2. **Immutability**: Verify frozen behavior
3. **Equality**: Test value-based equality (automatic with dataclass)
4. **Factory methods**: Test all construction paths
5. **Serialization**: Test to_dict/from_dict round-trip

```python
def test_value_object_validation():
    """Test validation raises on invalid input."""
    with pytest.raises(ValueError, match="cannot be empty"):
        YourValueObject(value="")

def test_value_object_immutability():
    """Test frozen behavior."""
    obj = YourValueObject(value="test")
    with pytest.raises(FrozenInstanceError):
        obj.value = "changed"

def test_factory_method():
    """Test factory method construction."""
    obj = YourValueObject.from_string("test")
    assert obj.value == "test"

def test_serialization_round_trip():
    """Test to_dict/from_dict round-trip."""
    obj = YourValueObject(value="test")
    data = obj.to_dict()
    restored = YourValueObject.from_dict(data)
    assert restored == obj
```

## File Locations

Value objects belong in the domain layer:

- **Simple value objects**: `src/project_watch_mcp/domain/value_objects/`
- **Complex value objects**: `src/project_watch_mcp/domain/values/`

**Naming convention**: `{concept_name}.py` (e.g., `file_path.py`, `identity.py`)

## See Also

- [templates/value-object-template.py](./templates/value-object-template.py) - Starter template
- [ARCHITECTURE.md](/Users/dawiddutoit/projects/play/project-watch-mcp/ARCHITECTURE.md) - Domain layer patterns
