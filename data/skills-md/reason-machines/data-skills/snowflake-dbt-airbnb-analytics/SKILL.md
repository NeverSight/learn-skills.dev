---
name: snowflake-dbt-airbnb-analytics
description: Inside Airbnb data warehouse built with Snowflake and dbt, demonstrating modern analytics engineering patterns with staging, intermediate, and mart layers.
triggers:
  - set up snowflake dbt project with inside airbnb data
  - create dbt models for airbnb listings and calendar
  - build incremental fact tables in snowflake with dbt
  - write dbt tests for data quality validation
  - configure dbt profiles for snowflake connection
  - add streamlit dashboard to dbt snowflake project
  - implement analytics engineering layered architecture
  - create monthly aggregates from airbnb calendar data
---

# Snowflake dbt Airbnb Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project demonstrates a complete analytics engineering workflow using Snowflake, dbt, and Streamlit. It loads Inside Airbnb open data into Snowflake, transforms it through a layered dbt architecture (staging → intermediate → marts), validates data quality with tests, and serves insights via a Streamlit dashboard.

## What This Project Does

- **Raw data ingestion**: Loads CSV/GZIP files from Inside Airbnb into Snowflake internal stages
- **Layered transformations**: Implements staging (clean/cast), intermediate (joins/enrichment), and mart (dimensions/facts) layers
- **Incremental modeling**: Uses Snowflake merge strategy for fact tables
- **Data quality**: Generic and singular dbt tests validate uniqueness, relationships, and business rules
- **Analytics dashboard**: Streamlit app queries marts for neighbourhood and listing performance

**Data sources**: `listings.csv.gz`, `calendar.csv.gz`, `reviews.csv.gz`, `neighbourhoods.csv` from [Inside Airbnb](https://insideairbnb.com/get-the-data/)

## Installation

```bash
# Clone and set up environment
git clone https://github.com/analyticsdurgesh/Snowflake_DBT_Project.git
cd Snowflake_DBT_Project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### 1. Snowflake Credentials

Create local-only credential files (ignored by git):

```bash
cp profiles.yml.example profiles.yml
cp config/local_credentials.example.json config/local_credentials.json
```

**`profiles.yml`** (dbt connection):

```yaml
airbnb_snowflake:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: YOUR_ACCOUNT
      user: YOUR_USER
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: YOUR_ROLE
      database: AIRBNB_DB
      warehouse: COMPUTE_WH
      schema: ANALYTICS
      threads: 4
      client_session_keep_alive: False
```

**`config/local_credentials.json`** (Streamlit connection):

```json
{
  "account": "YOUR_ACCOUNT",
  "user": "YOUR_USER",
  "password": "YOUR_PASSWORD",
  "role": "YOUR_ROLE",
  "warehouse": "COMPUTE_WH",
  "database": "AIRBNB_DB",
  "schema": "ANALYTICS"
}
```

Use environment variables in production:

```bash
export SNOWFLAKE_PASSWORD="your_password"
```

### 2. Download Inside Airbnb Data

Place raw files in `data/raw/`:

```text
data/raw/listings.csv.gz
data/raw/calendar.csv.gz
data/raw/reviews.csv.gz
data/raw/neighbourhoods.csv
```

Recommended dataset: New York City from [Inside Airbnb](https://insideairbnb.com/get-the-data/).

## Loading Raw Data

The Python loader creates Snowflake objects and stages data:

```bash
python scripts/load_inside_airbnb_to_snowflake.py
```

**What it does**:
1. Executes `setup/snowflake_setup.sql` to create database, schemas, and stage
2. Uploads raw files to `INSIDE_AIRBNB_STAGE`
3. Creates raw tables with headers from CSV files
4. Copies staged data into `RAW` schema tables

**Key loader code patterns**:

```python
import snowflake.connector
import json

# Load credentials
with open('config/local_credentials.json') as f:
    creds = json.load(f)

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=creds['account'],
    user=creds['user'],
    password=creds['password'],
    role=creds['role'],
    warehouse=creds['warehouse']
)

# Upload to stage
conn.cursor().execute(f"PUT file://data/raw/listings.csv.gz @INSIDE_AIRBNB_STAGE")

# Copy into raw table
conn.cursor().execute("""
    COPY INTO RAW.LISTINGS
    FROM @INSIDE_AIRBNB_STAGE/listings.csv.gz
    FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')
""")
```

## dbt Model Architecture

### Layer Structure

| Layer | Path | Purpose | Example |
|-------|------|---------|---------|
| **Sources** | `models/staging/sources.yml` | Define raw tables | `RAW.LISTINGS` |
| **Staging** | `models/staging/stg_*.sql` | Clean, cast, standardize | `stg_airbnb__listings` |
| **Intermediate** | `models/intermediate/int_*.sql` | Joins, enrichment, business logic | `int_airbnb__listing_enriched` |
| **Marts** | `models/marts/` | Dimensions, facts, aggregates | `dim_listings`, `fct_listing_calendar` |

### Staging Layer Example

**`models/staging/stg_airbnb__listings.sql`**:

```sql
with source as (
    select * from {{ source('airbnb_raw', 'listings') }}
),

cleaned as (
    select
        id::bigint as listing_id,
        name::varchar as listing_name,
        host_id::bigint as host_id,
        host_name::varchar as host_name,
        neighbourhood_cleansed::varchar as neighbourhood,
        room_type::varchar as room_type,
        price::varchar as price_raw,
        minimum_nights::int as minimum_nights,
        number_of_reviews::int as number_of_reviews,
        last_review::date as last_review_date,
        reviews_per_month::float as reviews_per_month,
        availability_365::int as availability_365
    from source
)

select * from cleaned
```

**Key patterns**:
- Use `{{ source() }}` for raw table references
- Cast types explicitly with `::`
- Standardize column names (snake_case)
- Preserve raw columns when cleaning needed downstream

### Intermediate Layer Example

**`models/intermediate/int_airbnb__calendar_enriched.sql`**:

```sql
with calendar as (
    select * from {{ ref('stg_airbnb__calendar') }}
),

listings as (
    select * from {{ ref('int_airbnb__listing_enriched') }}
),

enriched as (
    select
        c.listing_id,
        c.calendar_date,
        c.available,
        c.price,
        c.adjusted_price,
        c.minimum_nights,
        c.maximum_nights,
        l.listing_name,
        l.neighbourhood,
        l.room_type,
        l.host_id,
        l.host_name,
        -- Revenue proxy: price when unavailable
        case
            when c.available = false and c.price > 0
            then c.price
            else 0
        end as estimated_revenue
    from calendar c
    left join listings l
        on c.listing_id = l.listing_id
)

select * from enriched
```

**Key patterns**:
- Use `{{ ref() }}` for model dependencies
- Join staging/intermediate models
- Add calculated business logic (revenue proxy)
- Keep intermediate models focused on reusable logic

### Incremental Fact Table Example

**`models/marts/fct_listing_calendar.sql`**:

```sql
{{
    config(
        materialized='incremental',
        unique_key=['listing_id', 'calendar_date'],
        merge_update_columns=['available', 'price', 'estimated_revenue']
    )
}}

with calendar_enriched as (
    select * from {{ ref('int_airbnb__calendar_enriched') }}
)

select
    listing_id,
    calendar_date,
    available,
    price,
    adjusted_price,
    minimum_nights,
    maximum_nights,
    neighbourhood,
    room_type,
    host_id,
    estimated_revenue
from calendar_enriched

{% if is_incremental() %}
    where calendar_date > (select max(calendar_date) from {{ this }})
{% endif %}
```

**Key patterns**:
- `materialized='incremental'` for large fact tables
- `unique_key` for merge strategy (update existing, insert new)
- `merge_update_columns` specifies which columns to update
- `is_incremental()` filters new records only on subsequent runs
- Use `--full-refresh` flag to rebuild from scratch

### Aggregate Mart Example

**`models/marts/agg_neighbourhood_monthly_performance.sql`**:

```sql
with listing_monthly as (
    select * from {{ ref('agg_listing_monthly_performance') }}
)

select
    neighbourhood,
    year_month,
    count(distinct listing_id) as total_listings,
    sum(total_days) as total_days,
    sum(available_days) as total_available_days,
    sum(unavailable_days) as total_unavailable_days,
    round(avg(availability_rate), 2) as avg_availability_rate,
    round(sum(estimated_revenue), 2) as total_estimated_revenue,
    round(avg(avg_price), 2) as avg_listing_price
from listing_monthly
group by neighbourhood, year_month
order by neighbourhood, year_month
```

**Key patterns**:
- Aggregate from lower-level marts
- Use `round()` for clean reporting metrics
- Group by dimensions for dashboards

## dbt Commands

```bash
# Test connection
dbt debug --profiles-dir .

# Run all models
dbt run --profiles-dir .

# Run specific model and downstream dependencies
dbt run --select dim_listings+ --profiles-dir .

# Run incremental models with full refresh
dbt run --full-refresh --select fct_listing_calendar+ --profiles-dir .

# Run tests
dbt test --profiles-dir .

# Test specific model
dbt test --select stg_airbnb__listings --profiles-dir .

# Generate and serve documentation
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

**Common workflows**:

```bash
# New data load workflow
python scripts/load_inside_airbnb_to_snowflake.py
dbt run --full-refresh --select fct_listing_calendar+ --profiles-dir .
dbt test --profiles-dir .

# Development workflow (iterative)
dbt run --select +fct_reviews --profiles-dir .  # Run model and upstream deps
dbt test --select fct_reviews --profiles-dir .
```

## Data Quality Tests

### Generic Tests in Schema Files

**`models/staging/schema.yml`**:

```yaml
version: 2

models:
  - name: stg_airbnb__listings
    columns:
      - name: listing_id
        tests:
          - unique
          - not_null
      - name: room_type
        tests:
          - accepted_values:
              values: ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
      - name: price
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"

  - name: stg_airbnb__calendar
    columns:
      - name: listing_id
        tests:
          - relationships:
              to: ref('stg_airbnb__listings')
              field: listing_id
```

### Singular Tests

**`tests/no_duplicate_listing_dates.sql`**:

```sql
-- Test for duplicate listing-date combinations in fact table
select
    listing_id,
    calendar_date,
    count(*) as record_count
from {{ ref('fct_listing_calendar') }}
group by listing_id, calendar_date
having count(*) > 1
```

**Key patterns**:
- Generic tests in `schema.yml` for standard validations
- Singular tests in `tests/` for custom business rules
- Tests return records that FAIL the condition
- Use `dbt_utils` package for advanced tests

**Install dbt packages** (`packages.yml`):

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```

```bash
dbt deps --profiles-dir .
```

## Streamlit Dashboard

**`dashboard/streamlit_app.py`**:

```python
import streamlit as st
import snowflake.connector
import pandas as pd
import json

# Load credentials
with open('config/local_credentials.json') as f:
    creds = json.load(f)

@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=creds['account'],
        user=creds['user'],
        password=creds['password'],
        role=creds['role'],
        warehouse=creds['warehouse'],
        database=creds['database'],
        schema=creds['schema']
    )

def run_query(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

st.title("Inside Airbnb Analytics Dashboard")

# Neighbourhood performance
st.header("Top Neighbourhoods by Estimated Revenue")
query = """
    SELECT
        neighbourhood,
        total_estimated_revenue,
        avg_availability_rate,
        total_listings
    FROM agg_neighbourhood_monthly_performance
    WHERE year_month = (SELECT MAX(year_month) FROM agg_neighbourhood_monthly_performance)
    ORDER BY total_estimated_revenue DESC
    LIMIT 10
"""
df = run_query(query)
st.dataframe(df)
st.bar_chart(df.set_index('NEIGHBOURHOOD')['TOTAL_ESTIMATED_REVENUE'])

# Room type pricing
st.header("Average Price by Room Type")
query = """
    SELECT
        room_type,
        ROUND(AVG(price), 2) as avg_price
    FROM dim_listings
    WHERE price > 0
    GROUP BY room_type
    ORDER BY avg_price DESC
"""
df = run_query(query)
st.bar_chart(df.set_index('ROOM_TYPE')['AVG_PRICE'])
```

**Run dashboard**:

```bash
streamlit run dashboard/streamlit_app.py
```

**Key patterns**:
- Use `@st.cache_resource` for connection pooling
- Query marts directly for performance
- Filter to latest snapshot with `MAX(year_month)`
- Keep credentials in separate JSON file

## Common Patterns

### Adding a New Staging Model

1. Define source in `models/staging/sources.yml`:

```yaml
sources:
  - name: airbnb_raw
    database: AIRBNB_DB
    schema: RAW
    tables:
      - name: new_table
```

2. Create staging model `models/staging/stg_airbnb__new_table.sql`:

```sql
with source as (
    select * from {{ source('airbnb_raw', 'new_table') }}
),

cleaned as (
    select
        id::bigint as record_id,
        field::varchar as clean_field
    from source
)

select * from cleaned
```

3. Add tests in `models/staging/schema.yml`:

```yaml
models:
  - name: stg_airbnb__new_table
    columns:
      - name: record_id
        tests:
          - unique
          - not_null
```

### Creating a Dimension Table

**`models/marts/dim_hosts.sql`**:

```sql
with listings as (
    select * from {{ ref('int_airbnb__listing_enriched') }}
),

host_agg as (
    select
        host_id,
        max(host_name) as host_name,
        count(*) as total_listings,
        round(avg(price), 2) as avg_listing_price,
        sum(number_of_reviews) as total_reviews
    from listings
    group by host_id
)

select * from host_agg
```

**Key patterns**:
- Aggregate from enriched intermediate layer
- Use `max()` to select representative values
- Include business metrics (counts, averages)

### Monthly Aggregation Pattern

```sql
with daily_facts as (
    select * from {{ ref('fct_listing_calendar') }}
)

select
    listing_id,
    to_char(calendar_date, 'YYYY-MM') as year_month,
    count(*) as total_days,
    sum(case when available then 1 else 0 end) as available_days,
    sum(case when not available then 1 else 0 end) as unavailable_days,
    round(avg(case when available then 1.0 else 0.0 end), 2) as availability_rate,
    round(sum(estimated_revenue), 2) as estimated_revenue,
    round(avg(price), 2) as avg_price
from daily_facts
group by listing_id, to_char(calendar_date, 'YYYY-MM')
```

**Key patterns**:
- Use `to_char(date, 'YYYY-MM')` for month grouping in Snowflake
- Calculate rates with `avg(case when condition then 1.0 else 0.0 end)`
- Aggregate revenue as sum, prices as average

## Troubleshooting

### dbt Connection Issues

**Error**: `Database Error in model [...] (...)  250001 (08001): Failed to connect to DB`

**Solution**:
1. Verify `profiles.yml` has correct Snowflake account identifier
2. Test connection: `dbt debug --profiles-dir .`
3. Check Snowflake credentials and network access
4. Ensure warehouse is running

### Incremental Model Not Updating

**Error**: New data not appearing in incremental fact table

**Solution**:
```bash
# Force full rebuild
dbt run --full-refresh --select fct_listing_calendar --profiles-dir .
```

Check `unique_key` matches grain in config:
```sql
{{
    config(
        unique_key=['listing_id', 'calendar_date']  -- Must match table grain
    )
}}
```

### Test Failures on Price Data

**Error**: `dbt_utils.expression_is_true` fails on price column

**Solution**: Raw price data may contain non-numeric values or currency symbols.

Clean in staging layer:

```sql
-- Remove $ and commas, cast to numeric
replace(replace(price, '$', ''), ',', '')::decimal(10,2) as price
```

### Streamlit Connection Timeout

**Error**: `OperationalError: 250001 (08001): Failed to connect`

**Solution**:
1. Check `config/local_credentials.json` credentials
2. Verify Snowflake warehouse is running
3. Add timeout config:

```python
conn = snowflake.connector.connect(
    ...,
    login_timeout=30,
    network_timeout=30
)
```

### Missing Stage Files

**Error**: `File not found` when running loader script

**Solution**:
1. Verify raw files exist in `data/raw/`
2. Check file names match loader script expectations
3. Ensure files are compressed (`.gz`) where expected

### dbt Model Dependency Errors

**Error**: `Compilation Error: Model 'X' depends on a node named 'Y' which was not found`

**Solution**:
1. Check `{{ ref('model_name') }}` matches actual model file name
2. Run `dbt deps --profiles-dir .` to install packages
3. Verify model exists in `models/` directory

## Environment Variables for Production

Use environment variables instead of local credential files:

**dbt `profiles.yml`**:

```yaml
airbnb_snowflake:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
      schema: ANALYTICS
      threads: 4
```

**Streamlit connection**:

```python
import os

conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    role=os.getenv('SNOWFLAKE_ROLE'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema='ANALYTICS'
)
```

## Project Resources

- **GitHub**: [analyticsdurgesh/Snowflake_DBT_Project](https://github.com/analyticsdurgesh/Snowflake_DBT_Project)
- **Inside Airbnb**: [insideairbnb.com](https://insideairbnb.com/get-the-data/)
- **dbt Docs**: [docs.getdbt.com](https://docs.getdbt.com/)
- **Snowflake Docs**: [docs.snowflake.com](https://docs.snowflake.com/)
