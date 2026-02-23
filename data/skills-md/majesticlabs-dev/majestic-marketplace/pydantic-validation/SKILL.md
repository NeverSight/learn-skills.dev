---
name: pydantic-validation
description: Record-level data validation using Pydantic models. Field validators, model validators, and batch validation patterns.
allowed-tools: Read Write Edit Bash
---

# Pydantic Validation

**Audience:** Data engineers validating records in ETL pipelines.

**Goal:** Provide reusable Pydantic patterns for record-level validation.

## Scripts

Execute validation functions from `scripts/validators.py`:

```python
from scripts.validators import (
    UserRecord,
    Customer,
    Order,
    Address,
    validate_records,
    print_validation_errors,
    PositiveInt,
    Email
)
```

## Usage Examples

### Basic Model Validation

```python
from scripts.validators import UserRecord

# Validate single record
user = UserRecord(
    id=1,
    email="USER@example.com",
    status="active",
    created_at="2024-01-15",
    age=25
)
print(user.email)  # user@example.com (lowercased)
```

### Batch Validation

```python
from scripts.validators import validate_records, print_validation_errors

raw_data = [
    {"id": 1, "email": "a@b.com", "status": "active", "created_at": "2024-01-01", "age": 25},
    {"id": -1, "email": "invalid", "status": "bad", "created_at": "2024-01-01", "age": 200},
]

valid, invalid = validate_records(raw_data)
if invalid:
    print_validation_errors(invalid)
```

### Nested Models

```python
from scripts.validators import Customer, Address

customer = Customer(
    id=1,
    name="John Doe",
    billing_address=Address(
        street="123 Main St",
        city="NYC",
        postal_code="10001"
    )
)
# shipping_address defaults to billing_address
```

## Field Constraints Reference

| Constraint | Example | Description |
|------------|---------|-------------|
| `gt`, `ge` | `Field(gt=0)` | Greater than / greater-equal |
| `lt`, `le` | `Field(le=100)` | Less than / less-equal |
| `pattern` | `Field(pattern=r'^\d+$')` | Regex match |
| `min_length`, `max_length` | `Field(min_length=1)` | String length |

## JSON/Dict Conversion

```python
# Parse from dict
customer = Customer(**data_dict)

# Parse from JSON
customer = Customer.model_validate_json(json_string)

# Export to dict/JSON
data = customer.model_dump()
json_str = customer.model_dump_json()
```

## When to Use Pydantic

| Use Case | Pydantic | Alternative |
|----------|----------|-------------|
| API request/response | ✓ | FastAPI integration |
| Record-by-record ETL | ✓ | - |
| Full DataFrame validation | - | pandera |
| Pipeline expectations | - | Great Expectations |

## Dependencies

```
pydantic>=2.0
pydantic-settings  # For config validation
```
