---
name: testing-patterns
description: Pytest templates and patterns for ETL pipeline testing - unit, integration, data quality.
---

# Testing Patterns

Pytest templates for comprehensive ETL pipeline testing.

## Unit Tests - Transform Functions

```python
# tests/test_transforms.py
import pytest
import pandas as pd
from pipeline.transforms import clean_email, calculate_total, categorize_customer

class TestCleanEmail:
    def test_lowercase(self):
        assert clean_email("John@Example.COM") == "john@example.com"

    def test_strip_whitespace(self):
        assert clean_email("  john@example.com  ") == "john@example.com"

    def test_invalid_returns_none(self):
        assert clean_email("not-an-email") is None

    def test_null_input(self):
        assert clean_email(None) is None


class TestCalculateTotal:
    @pytest.fixture
    def order_items(self):
        return pd.DataFrame({
            'order_id': [1, 1, 2],
            'quantity': [2, 3, 1],
            'unit_price': [10.0, 5.0, 100.0]
        })

    def test_sums_correctly(self, order_items):
        result = calculate_total(order_items)
        assert result.loc[result['order_id'] == 1, 'total'].values[0] == 35.0

    def test_handles_empty(self):
        empty = pd.DataFrame(columns=['order_id', 'quantity', 'unit_price'])
        result = calculate_total(empty)
        assert len(result) == 0


class TestCategorizeCustomer:
    @pytest.mark.parametrize("total_spent,expected", [
        (0, 'bronze'),
        (99, 'bronze'),
        (100, 'silver'),
        (999, 'silver'),
        (1000, 'gold'),
        (9999, 'gold'),
        (10000, 'platinum'),
    ])
    def test_tiers(self, total_spent, expected):
        assert categorize_customer(total_spent) == expected
```

## Integration Tests - Full Pipeline

```python
# tests/test_pipeline.py
import pytest
from pipeline import OrdersPipeline
from tests.fixtures import generate_orders_fixture

class TestOrdersPipeline:
    @pytest.fixture
    def pipeline(self, tmp_path):
        return OrdersPipeline(
            source_path=tmp_path / "source",
            target_path=tmp_path / "target"
        )

    @pytest.fixture
    def source_data(self, tmp_path):
        df = generate_orders_fixture(100)
        path = tmp_path / "source" / "orders.csv"
        path.parent.mkdir(parents=True)
        df.to_csv(path, index=False)
        return df

    def test_row_count_preserved(self, pipeline, source_data):
        """Verify no rows lost in transformation."""
        pipeline.run()
        result = pd.read_parquet(pipeline.target_path / "orders.parquet")
        assert len(result) == len(source_data)

    def test_all_columns_present(self, pipeline, source_data):
        """Verify output has expected columns."""
        pipeline.run()
        result = pd.read_parquet(pipeline.target_path / "orders.parquet")
        expected_columns = ['order_id', 'customer_id', 'total', 'tier', 'processed_at']
        assert all(col in result.columns for col in expected_columns)

    def test_no_null_required_fields(self, pipeline, source_data):
        """Verify required fields are populated."""
        pipeline.run()
        result = pd.read_parquet(pipeline.target_path / "orders.parquet")
        assert result['order_id'].notna().all()
        assert result['customer_id'].notna().all()

    def test_idempotent(self, pipeline, source_data):
        """Running twice produces same result."""
        pipeline.run()
        first_result = pd.read_parquet(pipeline.target_path / "orders.parquet")

        pipeline.run()
        second_result = pd.read_parquet(pipeline.target_path / "orders.parquet")

        pd.testing.assert_frame_equal(first_result, second_result)
```

## Data Quality Tests (dbt-style)

```python
# tests/test_data_quality.py
import pytest
from sqlalchemy import create_engine, text

@pytest.fixture
def db_connection():
    engine = create_engine("postgresql://...")
    with engine.connect() as conn:
        yield conn

class TestOrdersTable:
    def test_unique_order_id(self, db_connection):
        result = db_connection.execute(text("""
            SELECT order_id, COUNT(*) as cnt
            FROM orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        """))
        duplicates = result.fetchall()
        assert len(duplicates) == 0, f"Found duplicate order_ids: {duplicates[:5]}"

    def test_valid_status(self, db_connection):
        result = db_connection.execute(text("""
            SELECT DISTINCT status
            FROM orders
            WHERE status NOT IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')
        """))
        invalid = result.fetchall()
        assert len(invalid) == 0, f"Found invalid statuses: {invalid}"

    def test_positive_amounts(self, db_connection):
        result = db_connection.execute(text("""
            SELECT COUNT(*) FROM orders WHERE total < 0
        """))
        negative_count = result.scalar()
        assert negative_count == 0, f"Found {negative_count} orders with negative totals"
```

## Golden File Testing

```python
def test_transform_matches_golden(self):
    """Compare output to known-good result."""
    input_df = pd.read_csv("tests/fixtures/input.csv")
    expected = pd.read_csv("tests/golden/expected_output.csv")

    result = transform(input_df)

    pd.testing.assert_frame_equal(result, expected)
```

## Snapshot Testing

```python
def test_schema_snapshot(self, snapshot):
    """Ensure schema hasn't changed unexpectedly."""
    result = transform(input_df)
    schema = {col: str(dtype) for col, dtype in result.dtypes.items()}
    snapshot.assert_match(json.dumps(schema, indent=2), "schema.json")
```

## Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=0, max_value=1e9))
def test_total_always_positive(amount):
    """Total should never go negative."""
    result = calculate_tax(amount)
    assert result >= 0

@given(st.lists(st.integers(min_value=1, max_value=100), min_size=1))
def test_sum_equals_parts(values):
    """Aggregation should equal sum of parts."""
    df = pd.DataFrame({'amount': values})
    result = aggregate(df)
    assert result == sum(values)
```
