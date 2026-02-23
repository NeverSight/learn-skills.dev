---
name: test-fixture-generator
description: Generate synthetic test data with edge cases for ETL pipeline testing.
---

# Test Fixture Generator

Generate test fixtures matching schema specifications with automatic edge case injection.

## Core Generator

```python
def generate_fixtures(
    schema: dict,
    count: int = 100,
    edge_cases: bool = True
) -> pd.DataFrame:
    """Generate test data matching schema."""
    data = {}

    for col, spec in schema.items():
        if spec['type'] == 'integer':
            data[col] = generate_integers(count, spec)
        elif spec['type'] == 'string':
            data[col] = generate_strings(count, spec)
        elif spec['type'] == 'date':
            data[col] = generate_dates(count, spec)
        elif spec['type'] == 'float':
            data[col] = generate_floats(count, spec)
        elif spec['type'] == 'boolean':
            data[col] = generate_booleans(count)
        elif spec['type'] == 'enum':
            data[col] = generate_enums(count, spec['values'])

    df = pd.DataFrame(data)

    if edge_cases:
        df = add_edge_cases(df, schema)

    return df
```

## Edge Case Injection

```python
def add_edge_cases(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """Add rows with boundary and edge case values."""
    edge_rows = []

    # Null row (where nullable)
    null_row = {
        col: None if spec.get('nullable', True) else df[col].iloc[0]
        for col, spec in schema.items()
    }
    edge_rows.append(null_row)

    # Boundary values per column
    for col, spec in schema.items():
        base_row = df.iloc[0].to_dict()

        if spec['type'] == 'integer':
            edge_rows.append({**base_row, col: spec.get('min', 0)})
            edge_rows.append({**base_row, col: spec.get('max', 2147483647)})

        elif spec['type'] == 'string':
            edge_rows.append({**base_row, col: ''})  # Empty string
            edge_rows.append({**base_row, col: 'a' * spec.get('max_length', 255)})  # Max length

        elif spec['type'] == 'float':
            edge_rows.append({**base_row, col: 0.0})
            edge_rows.append({**base_row, col: spec.get('min', -1e9)})
            edge_rows.append({**base_row, col: spec.get('max', 1e9)})

        elif spec['type'] == 'date':
            edge_rows.append({**base_row, col: datetime(1970, 1, 1)})
            edge_rows.append({**base_row, col: datetime.now()})

    return pd.concat([df, pd.DataFrame(edge_rows)], ignore_index=True)
```

## Type Generators

```python
import random
import string
from datetime import datetime, timedelta

def generate_integers(count: int, spec: dict) -> list:
    min_val = spec.get('min', 0)
    max_val = spec.get('max', 1000000)
    return [random.randint(min_val, max_val) for _ in range(count)]

def generate_floats(count: int, spec: dict) -> list:
    min_val = spec.get('min', 0.0)
    max_val = spec.get('max', 1000000.0)
    precision = spec.get('precision', 2)
    return [round(random.uniform(min_val, max_val), precision) for _ in range(count)]

def generate_strings(count: int, spec: dict) -> list:
    min_len = spec.get('min_length', 1)
    max_len = spec.get('max_length', 50)
    pattern = spec.get('pattern', None)

    if pattern == 'email':
        return [f"user{i}@example.com" for i in range(count)]
    elif pattern == 'phone':
        return [f"+1{random.randint(1000000000, 9999999999)}" for i in range(count)]
    else:
        return [
            ''.join(random.choices(string.ascii_letters, k=random.randint(min_len, max_len)))
            for _ in range(count)
        ]

def generate_dates(count: int, spec: dict) -> list:
    start = spec.get('min', datetime(2020, 1, 1))
    end = spec.get('max', datetime.now())
    delta = (end - start).days
    return [start + timedelta(days=random.randint(0, delta)) for _ in range(count)]

def generate_booleans(count: int) -> list:
    return [random.choice([True, False]) for _ in range(count)]

def generate_enums(count: int, values: list) -> list:
    return [random.choice(values) for _ in range(count)]
```

## Schema Definition Format

```yaml
# fixtures/orders_schema.yml
columns:
  order_id:
    type: integer
    min: 1
    nullable: false

  customer_email:
    type: string
    pattern: email
    nullable: false

  total_amount:
    type: float
    min: 0.01
    max: 100000.00
    precision: 2

  status:
    type: enum
    values: [pending, confirmed, shipped, delivered, cancelled]

  created_at:
    type: date
    min: 2023-01-01
    nullable: false
```

## Usage

```python
import yaml

# Load schema
with open('fixtures/orders_schema.yml') as f:
    schema = yaml.safe_load(f)['columns']

# Generate fixtures
df = generate_fixtures(schema, count=100, edge_cases=True)

# Save for test use
df.to_csv('tests/fixtures/orders_fixture.csv', index=False)
```
