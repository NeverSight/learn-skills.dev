---
name: pandera-validation
description: DataFrame schema validation using pandera. Schema definitions, column checks, and decorator-based validation.
allowed-tools: Read Write Edit Bash
---

# Pandera Validation

**Audience:** Data engineers validating pandas DataFrames.

**Goal:** Provide pandera patterns for schema validation and type checking.

## Scripts

Execute schema functions from `scripts/schemas.py`:

```python
from scripts.schemas import (
    create_user_schema,
    create_nullable_schema,
    create_date_range_schema,
    UserSchema,
    validate_with_errors,
    infer_and_export_schema
)
```

## Usage Examples

### Basic Schema Validation

```python
from scripts.schemas import create_user_schema

schema = create_user_schema()
validated_df = schema.validate(df)
```

### Collect All Errors

```python
from scripts.schemas import create_user_schema, validate_with_errors

schema = create_user_schema()
validated_df, errors = validate_with_errors(df, schema)

if errors:
    for err in errors:
        print(f"{err['column']}: {err['check']} - {err['failure_case']}")
```

### Class-Based Schema

```python
from scripts.schemas import UserSchema

# Validate with type hints
UserSchema.validate(df)

# Use as function type hint
def process_users(df: pa.typing.DataFrame[UserSchema]) -> pd.DataFrame:
    return df.query("status == 'active'")
```

### Infer Schema from DataFrame

```python
from scripts.schemas import infer_and_export_schema

schema_export = infer_and_export_schema(df)
print(schema_export['python_code'])  # Python schema definition
print(schema_export['yaml'])         # YAML schema
```

## Built-in Checks Reference

| Check Type | Example | Description |
|------------|---------|-------------|
| Numeric | `Check.gt(0)`, `Check.in_range(0, 100)` | Comparisons |
| String | `Check.str_matches(r'pattern')` | Regex match |
| Set membership | `Check.isin(['A', 'B'])` | Allowed values |
| Uniqueness | `unique=True` on Column | No duplicates |
| Nullable | `nullable=True` on Column | Allow nulls |

## Decorator-Based Validation

```python
import pandera as pa

@pa.check_output(schema)
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@pa.check_input(schema, "df")
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(processed=True)

@pa.check_io(df=input_schema, out=output_schema)
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.transform(...)
```

## When to Use Pandera

| Use Case | Pandera | Alternative |
|----------|---------|-------------|
| DataFrame validation | ✓ | - |
| Type hints for DataFrames | ✓ | - |
| ETL pipeline checks | ✓ | Great Expectations |
| Record-level validation | - | Pydantic |

## Dependencies

```
pandera>=0.18
pandas
```
