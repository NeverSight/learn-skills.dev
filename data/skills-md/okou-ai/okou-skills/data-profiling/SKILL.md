---
name: data-profiling
description: Profile datasets for schema, distributions, nulls, cardinality, outliers, relationships, and data quality.
---

## Structural Reconnaissance

### Table-Level Inventory

Start every new dataset encounter by answering these questions:

- What is the total row and column count?
- What does each row represent (the grain)?
- Which column or columns uniquely identify a row?
- When was the most recent data loaded?
- What is the earliest date in the dataset?

### Classifying Columns by Role

Assign every column to one of these categories:

- **Key**: Primary keys, foreign keys, entity identifiers
- **Attribute**: Categorical fields used for grouping or filtering (region, status, plan_type)
- **Measure**: Numeric fields intended for aggregation (revenue, duration, score)
- **Timestamp**: Date or datetime fields (created_at, processed_on, event_date)
- **Free-text**: Unstructured strings (descriptions, comments, names)
- **Flag**: Binary true/false indicators
- **Nested**: JSON blobs, arrays, or embedded structures

## Column-Level Inspection

### Universal Checks (All Column Types)

- Null count and null percentage
- Count of distinct values and cardinality ratio (distinct / total rows)
- Top 5-10 most frequent values with their occurrence counts
- Bottom 5 least frequent values (useful for spotting anomalies)

### Numeric Measures

```
Minimum, maximum, mean, median
Standard deviation
Percentile ladder: p1, p5, p25, p75, p95, p99
Count of zeros
Count of negatives (flag if unexpected)
```

### Text and Categorical Fields

```
Shortest length, longest length, average length
Count of empty strings
Format regularity (do values follow a consistent pattern?)
Case consistency (uniform upper, uniform lower, or mixed?)
Count of values with leading or trailing whitespace
```

### Date and Timestamp Fields

```
Earliest date, latest date
Count of nulls
Count of future dates (flag if the domain forbids them)
Distribution across months or weeks
Gaps in expected daily/weekly cadence
```

### Boolean Fields

```
True count, false count, null count
True proportion
```

## Discovering Relationships

After examining columns individually, look for connections:

- **Foreign key candidates**: ID columns whose values likely reference another table
- **Hierarchical dimensions**: Columns that nest naturally (country > region > city)
- **Correlated measures**: Numeric columns that trend together
- **Computed columns**: Fields that appear derived from other columns in the same table
- **Duplicated information**: Columns that carry identical or near-identical content

## Evaluating Data Quality

### Completeness Ratings

Assign each column a tier:

- **Full** (>99% populated): No action needed
- **Mostly full** (95-99%): Investigate the missing values
- **Gaps present** (80-95%): Determine whether the gaps are systematic and whether the column is still usable
- **Sparse** (<80%): Likely unusable without imputation or supplemental data

### Consistency Checks

Scan for:
- **Value normalization failures**: The same concept spelled multiple ways ("USA", "US", "United States", "us")
- **Type mismatches**: Numerics stored as text, dates in inconsistent formats
- **Broken references**: Foreign key values with no matching parent record
- **Rule violations**: Negative quantities, end dates preceding start dates, percentages outside 0-100
- **Cross-column contradictions**: status = 'shipped' while ship_date is null

### Accuracy Warning Signs

Patterns that suggest the data may be unreliable:
- **Sentinel values**: 0, -1, 999999, "N/A", "TBD", "test", "xxx"
- **Suspiciously dominant defaults**: One value appearing far more often than expected
- **Stale records**: The updated_at column shows no recent activity in an active system
- **Physically impossible values**: Ages above 150, dates decades in the future, negative durations
- **Rounding artifacts**: Disproportionate clustering on multiples of 5 or 10 (implies estimation)

### Freshness Assessment

- What is the timestamp of the most recent row?
- How often should this table refresh?
- Is there measurable lag between event occurrence and warehouse arrival?
- Are there missing days or hours in the time series?

## Recognizing Patterns

### Distribution Shapes

When profiling a numeric column, classify its shape:
- **Bell-shaped**: Mean and median nearly equal; symmetric tails
- **Right-skewed**: Long right tail with a few very large values (typical for revenue, session length)
- **Left-skewed**: Long left tail with a few very small values (less common)
- **Bimodal**: Two distinct peaks (suggests two merged populations)
- **Power-law**: A handful of enormous values dominating; many near-zero values (user engagement metrics)
- **Uniform**: Roughly flat across the range (often synthetic or randomly generated)

### Time-Based Patterns

For any temporal data, investigate:
- **Trend**: Persistent upward or downward drift
- **Seasonality**: Recurring cycles — weekly, monthly, quarterly, annual
- **Weekday effects**: Systematic weekday vs. weekend differences
- **Holiday impacts**: Spikes or dips around known holidays
- **Level shifts**: Abrupt, sustained changes in the baseline
- **Isolated anomalies**: Single data points that break the prevailing pattern

### Segment Discovery

Surface natural groupings by:
- Identifying categorical columns with 3 to 20 distinct values
- Comparing metric distributions across each segment value
- Highlighting segments whose behavior diverges meaningfully from the overall
- Checking whether apparent segments contain meaningful sub-segments

### Correlation Scanning

Across numeric columns:
- Build a pairwise correlation matrix
- Highlight strong associations (|r| > 0.7)
- Remember that correlation never establishes causation — note this explicitly
- Probe for non-linear relationships (quadratic, logarithmic) that Pearson r would miss

## Documenting What You Find

### Dataset Summary Template

```markdown

## Table: [schema.table_name]

**Purpose**: [What this table captures]
**Grain**: [One row per...]
**Primary Key**: [column(s)]
**Approximate Rows**: [count, as of date]
**Refresh Cadence**: [real-time / hourly / daily / weekly]
**Responsible Team**: [owner]

### Important Columns

| Column | Type | Meaning | Sample Values | Notes |
|--------|------|---------|---------------|-------|
| user_id | STRING | Unique user handle | "usr_abc123" | References users.id |
| event_type | STRING | Action category | "click", "view", "purchase" | 15 distinct values |
| revenue | DECIMAL | USD transaction amount | 29.99, 149.00 | Null for non-purchases |
| created_at | TIMESTAMP | Event occurrence time | 2024-01-15 14:23:01 | Partition column |

### Join Paths
- Links to `users` via `user_id`
- Links to `products` via `product_id`
- Parent of `event_details` (one-to-many on event_id)

### Known Caveats
- [Document any quality issues]
- [Note analytical gotchas]

### Typical Query Use Cases
- [List common analytical patterns against this table]
```

### Schema Discovery Queries

When working directly against a warehouse, use these patterns:

```sql
-- Enumerate tables in a schema (PostgreSQL)
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Inspect column metadata (PostgreSQL)
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'target_table'
ORDER BY ordinal_position;

-- Rank tables by storage footprint (PostgreSQL)
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Row count per table (general approach)
-- Execute individually: SELECT COUNT(*) FROM table_name
```

### Tracing Data Lineage

When navigating an unfamiliar warehouse:

1. Begin at the consumption layer — identify which tables power reports and dashboards
2. Follow dependencies upstream: what feeds those tables?
3. Map the raw / staging / mart architecture
4. Track where transformations enrich, filter, or roll up the data
5. Record any points where data is joined with external sources
