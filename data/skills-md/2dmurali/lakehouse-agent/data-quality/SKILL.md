---
name: data-quality
description: Profile data, detect schema evolution/drift, and implement enterprise-grade data quality checks (Soda/Great Expectations).
---

# Skill: Enterprise Lakehouse Data Quality & Schema Drift

## Description
Enables the agent to profile data, detect schema evolution/drift over time, and implement enterprise-grade data quality checks using frameworks like Soda Core or Great Expectations.

## Context
Lakehouse architectures enforce schema on write. However, schemas evolve over time. Data quality issues like sudden drops in row counts, increased nulls, or delayed data arrivals can silently break downstream analytics.

## Instructions

### 1. Schema Drift Detection
Compare the schema of the earliest available snapshot/commit with the latest snapshot.
- List **Added Columns**.
- List **Removed Columns**.
- List **Type Changes** (e.g., `INT` to `LONG`).

*For Delta Lake:* Use `.history()` to find schema changes or parse the transaction log.
*For Iceberg:* Use the catalog to compare schemas across `table.history()`.

### 2. Enterprise Data Quality Frameworks
If asked to build data quality checks, prefer industry-standard frameworks over raw SQL where applicable.

**Soda Core YAML Pattern:**
Provide the user with a `.yml` definition for Soda:
```yaml
checks for catalog.database.table_name:
  - row_count > 0
  - freshness(updated_at) < 1h
  - duplicate_count(transaction_id) = 0
  - missing_count(user_id) = 0
  - schema:
      fail: when required column missing [id, user_id, updated_at]
```

**Great Expectations Pattern:**
```python
import great_expectations as gx

context = gx.get_context()
validator = context.sources.pandas_default.read_parquet("s3://bucket/path")

validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_unique("transaction_id")
validator.expect_table_row_count_to_be_between(min_value=1000)
```

### 3. Anomaly Detection (Statistical Bounds)
If the user wants advanced quality checks, suggest statistical anomaly detection using moving averages or Z-scores in SQL.

**Example Statistical Check:**
```sql
WITH daily_counts AS (
  SELECT date_trunc('day', created_at) as dt, COUNT(*) as cnt
  FROM my_table GROUP BY 1
),
stats AS (
  SELECT AVG(cnt) as mean, STDDEV(cnt) as stddev FROM daily_counts
)
SELECT dt, cnt, (cnt - mean) / stddev as z_score
FROM daily_counts, stats
WHERE abs((cnt - mean) / stddev) > 3; -- Flags days > 3 standard deviations
```

## Output Format: Quality Profiling Report
```markdown
### 📉 Data Quality & Schema Profile: `[Table Name]`

#### 🔄 Schema Evolution
- **Initial Version:** 34 columns
- **Current Version:** 36 columns
- **Changes:**
  - `+` `user_segment` (STRING)
  - `~` `transaction_id` (INT -> BIGINT)

#### ✅ Quality Metrics (Soda Profile)
| Check | Threshold | Result | Status |
|-------|-----------|--------|--------|
| **Freshness** | `< 1h` | 2 mins ago | 🟢 Pass |
| **Duplicates** | `= 0` | 5 records | 🔴 Fail |
| **Null Rate** | `= 0%` | 0% | 🟢 Pass |
```
