---
name: great-expectations
description: Data validation using Great Expectations. Expectation suites, checkpoints, and data docs for pipeline monitoring.
allowed-tools: Read Write Edit Bash
---

# Great Expectations

**Audience:** Data engineers building validated data pipelines.

**Goal:** Provide GX patterns for expectation-based validation and monitoring.

## Scripts

Execute GX functions from `scripts/expectations.py`:

```python
from scripts.expectations import (
    get_pandas_context,
    add_dataframe_asset,
    create_basic_suite,
    run_validation
)
```

## Usage Examples

### Quick Setup

```python
from scripts.expectations import get_pandas_context, add_dataframe_asset

context, datasource = get_pandas_context("my_datasource")
batch_request = add_dataframe_asset(datasource, "users", df)
```

### Create Expectation Suite

```python
from scripts.expectations import create_basic_suite

columns_config = {
    'user_id': {'not_null': True, 'unique': True, 'type': 'int'},
    'age': {'min': 0, 'max': 150},
    'status': {'values': ['active', 'inactive', 'pending']},
    'email': {'regex': r'^[\w\.-]+@[\w\.-]+\.\w+$'}
}

suite = create_basic_suite(context, "user_suite", columns_config)
```

### Run Validation

```python
from scripts.expectations import run_validation

results = run_validation(
    context,
    checkpoint_name="user_checkpoint",
    batch_request=batch_request,
    suite_name="user_suite"
)

if results['success']:
    print("All expectations passed!")
else:
    for failure in results['failures']:
        print(f"Failed: {failure['expectation']} on {failure['column']}")
```

## Common Expectations Reference

| Category | Expectation | Description |
|----------|-------------|-------------|
| Table | `ExpectTableRowCountToBeBetween` | Row count range |
| Existence | `ExpectColumnToExist` | Column must exist |
| Nulls | `ExpectColumnValuesToNotBeNull` | No null values |
| Range | `ExpectColumnValuesToBeBetween` | Value bounds |
| Set | `ExpectColumnValuesToBeInSet` | Allowed values |
| Pattern | `ExpectColumnValuesToMatchRegex` | Regex match |
| Unique | `ExpectColumnValuesToBeUnique` | No duplicates |

## Data Docs

```python
# Build and open HTML reports
context.build_data_docs()
context.open_data_docs()
```

## Directory Structure

```
great_expectations/
├── great_expectations.yml     # Config
├── expectations/              # Expectation suites (JSON)
├── checkpoints/               # Checkpoint definitions
├── plugins/                   # Custom expectations
└── uncommitted/
    ├── data_docs/            # Generated HTML docs
    └── validations/          # Validation results
```

## When to Use Great Expectations

| Use Case | GX | Alternative |
|----------|-----|-------------|
| Pipeline monitoring | ✓ | - |
| Data warehouse validation | ✓ | - |
| Automated data docs | ✓ | - |
| Simple DataFrame checks | - | Pandera |
| Record-level API validation | - | Pydantic |

## Dependencies

```
great_expectations>=0.18
pandas
```
