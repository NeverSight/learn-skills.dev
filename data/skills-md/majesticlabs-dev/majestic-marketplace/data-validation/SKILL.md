---
name: data-validation
description: Data validation patterns and pipeline helpers. Custom validation functions, schema evolution, and test assertions.
allowed-tools: Read Write Edit Bash
---

# Data Validation

**Audience:** Data engineers building validation pipelines.

**Goal:** Provide validation patterns for custom business rules.

**Framework-specific skills:**
- `pydantic-validation` - Record-level validation with Pydantic
- `pandera-validation` - DataFrame schema validation
- `great-expectations` - Pipeline expectations and monitoring

## Scripts

Execute validation functions from `scripts/validators.py`:

```python
from scripts.validators import (
    ValidationResult,
    DataValidator,
    validate_no_duplicates,
    validate_referential_integrity,
    validate_date_range,
    validate_value_in_set,
    run_validation_pipeline,
    validate_with_schema_version,
    assert_schema_match,
    assert_no_nulls,
    assert_unique,
    assert_values_in_set
)
```

## Framework Selection

| Use Case | Framework |
|----------|-----------|
| API request/response | Pydantic |
| Record-by-record ETL | Pydantic |
| DataFrame validation | Pandera |
| Type hints for DataFrames | Pandera |
| Pipeline monitoring | Great Expectations |
| Data warehouse checks | Great Expectations |
| Custom business rules | Custom functions (this skill) |

## Usage Examples

### Basic Validation

```python
from scripts.validators import validate_no_duplicates, validate_referential_integrity

# Check duplicates
result = validate_no_duplicates(df, cols=['id'])
if not result.passed:
    print(f"Error: {result.message}")
    print(result.failed_rows)

# Check referential integrity
result = validate_referential_integrity(df, 'user_id', users_df, 'id')
```

### Validation Pipeline

```python
from scripts.validators import DataValidator, validate_no_duplicates, validate_date_range

validator = DataValidator()
validator.add_check(lambda df: validate_no_duplicates(df, ['id']))
validator.add_check(lambda df: validate_date_range(df, 'created_at', '2020-01-01', '2025-12-31'))

results = validator.validate(df)
if not results['passed']:
    for check in results['checks']:
        if not check['passed']:
            print(f"Failed: {check['message']}")
```

### Config-Driven Pipeline

```python
from scripts.validators import run_validation_pipeline

config = {
    'unique_columns': ['id'],
    'date_ranges': {
        'created_at': ('2020-01-01', '2025-12-31'),
        'updated_at': ('2020-01-01', '2025-12-31')
    }
}

clean_df, results = run_validation_pipeline(df, config)
```

### Test Assertions

```python
from scripts.validators import assert_schema_match, assert_no_nulls, assert_unique

# In pytest
def test_data_quality():
    assert_schema_match(df, {'id': 'int64', 'email': 'object'})
    assert_no_nulls(df, ['id', 'email'])
    assert_unique(df, ['id'])
```

## Dependencies

```
pandas
```
