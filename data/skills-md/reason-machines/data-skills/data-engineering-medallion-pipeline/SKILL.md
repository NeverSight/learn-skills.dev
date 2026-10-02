---
name: data-engineering-medallion-pipeline
description: End-to-end data engineering pipeline using MinIO, Airbyte, PostgreSQL, DBT, and Airflow with medallion architecture (Bronze/Silver/Gold layers)
triggers:
  - "set up a medallion architecture data pipeline"
  - "configure airbyte with minio and postgres"
  - "create dbt bronze silver gold models"
  - "orchestrate data pipeline with airflow"
  - "implement data quality tests in dbt"
  - "build an elt pipeline with docker compose"
  - "create a data lakehouse with medallion layers"
  - "deploy data engineering stack locally"
---

# Data Engineering Medallion Pipeline Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to work with a complete data engineering pipeline implementing the Medallion Architecture (Bronze → Silver → Gold) using modern open-source tools: MinIO (S3-compatible storage), Airbyte (data ingestion), PostgreSQL (data warehouse), DBT (transformations), Apache Airflow (orchestration), and Grafana (monitoring).

## What This Project Does

The data-engineering-medallion project provides a complete end-to-end data pipeline that:

1. **Ingests** raw data from MinIO object storage into PostgreSQL using Airbyte
2. **Transforms** data through three layers (Bronze/Silver/Gold) using DBT
3. **Orchestrates** the entire pipeline with Apache Airflow DAGs
4. **Validates** data quality with automated DBT tests
5. **Monitors** infrastructure health with Prometheus and Grafana
6. **Visualizes** business metrics in Power BI dashboards

The architecture follows ELT (Extract-Load-Transform) pattern with clear separation of concerns:
- **Bronze**: Raw immutable data from sources (JSONB format)
- **Silver**: Cleaned, validated, and typed data
- **Gold**: Business-ready aggregated metrics and KPIs

## Installation & Setup

### Prerequisites

```bash
# Required
docker --version  # 20.10+
docker-compose --version  # 2.0+
# 8GB RAM minimum, 16GB recommended
```

### Clone and Initialize

```bash
git clone https://github.com/LucasGoulartCouto/data-engineering-medallion.git
cd data-engineering-medallion

# Setup environment and start all services
make setup
make start

# Verify all containers are healthy
make status
```

### Service URLs

After startup, access these interfaces:

- **Airflow**: http://localhost:8080 (admin/admin)
- **MinIO**: http://localhost:9001 (minioadmin/[from .env])
- **Airbyte**: http://localhost:8000 (create account on first visit)
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **DBT Docs**: http://localhost:8085 (after `make dbt-docs`)

## Key Commands (Makefile)

```bash
# Infrastructure
make setup          # Create .env, directories, install dependencies
make start          # Start all Docker services
make stop           # Stop all services
make restart        # Restart all services
make status         # Check container health
make logs SERVICE=airflow  # View logs for specific service

# DBT Operations
make dbt-run        # Run all DBT models (bronze → silver → gold)
make dbt-test       # Run data quality tests
make dbt-docs       # Generate and serve documentation
make dbt-snapshot   # Capture SCD Type 2 snapshots
make dbt-clean      # Clean compiled artifacts

# Data Pipeline
make upload-data    # Upload sample data to MinIO
make trigger-dag DAG_ID=bronze_ingestion_dag  # Manually trigger Airflow DAG

# Development
make lint           # Lint Python and SQL code
make format         # Format Python code with black
make validate       # Validate Airflow DAGs and DBT models

# Cleanup
make clean          # Remove volumes and stop services
make clean-all      # Full cleanup including Docker images
```

## Project Structure

```
data-engineering-medallion/
├── airflow/
│   └── dags/
│       ├── bronze_ingestion_dag.py      # Triggers Airbyte sync
│       ├── silver_transformation_dag.py  # Runs DBT silver models
│       └── gold_aggregation_dag.py       # Runs DBT gold models
├── dbt/
│   ├── models/
│   │   ├── bronze/         # Extract JSONB → columnar
│   │   ├── silver/         # Clean, validate, dedupe
│   │   └── gold/           # Business metrics
│   ├── macros/             # Reusable SQL functions
│   ├── snapshots/          # SCD Type 2 history
│   └── tests/              # Custom data quality tests
├── scripts/
│   ├── upload_to_minio.py  # Upload CSV/JSON to MinIO
│   └── test_connections.py # Verify service connectivity
├── postgres/init/          # Database initialization SQL
├── monitoring/
│   ├── grafana/provisioning/
│   └── prometheus/
├── docker-compose.yml
├── Makefile
└── .env                    # Configuration (create from .env.example)
```

## DBT Model Development

### Bronze Layer (Raw Extraction)

Bronze models extract JSONB data from Airbyte into typed columns:

```sql
-- dbt/models/bronze/bronze_orders.sql
{{ config(
    materialized='view',
    schema='bronze'
) }}

SELECT
    _airbyte_ab_id,
    _airbyte_emitted_at,
    _airbyte_data->>'order_id' AS order_id,
    _airbyte_data->>'customer_id' AS customer_id,
    _airbyte_data->>'order_date' AS order_date,
    _airbyte_data->>'total_amount' AS total_amount,
    _airbyte_data->>'status' AS status,
    _airbyte_data AS raw_data
FROM {{ source('airbyte_raw', '_airbyte_raw_orders') }}
```

### Silver Layer (Cleaned & Validated)

Silver models clean, cast types, deduplicate, and add calculated fields:

```sql
-- dbt/models/silver/silver_orders.sql
{{ config(
    materialized='table',
    schema='silver',
    unique_key='order_id'
) }}

WITH deduplicated AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY order_id 
               ORDER BY _airbyte_emitted_at DESC
           ) AS rn
    FROM {{ ref('bronze_orders') }}
)

SELECT
    order_id::INTEGER,
    customer_id::INTEGER,
    order_date::DATE,
    total_amount::DECIMAL(10,2),
    UPPER(TRIM(status)) AS status,
    CASE 
        WHEN total_amount::DECIMAL > 1000 THEN 'high_value'
        WHEN total_amount::DECIMAL > 500 THEN 'medium_value'
        ELSE 'low_value'
    END AS order_value_segment,
    _airbyte_emitted_at AS ingested_at,
    CURRENT_TIMESTAMP AS transformed_at
FROM deduplicated
WHERE rn = 1
    AND order_id IS NOT NULL
    AND order_date::DATE <= CURRENT_DATE
```

### Gold Layer (Business Metrics)

Gold models aggregate data for business consumption:

```sql
-- dbt/models/gold/gold_product_performance.sql
{{ config(
    materialized='table',
    schema='gold'
) }}

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.supplier,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.line_total) AS total_revenue,
    SUM(oi.quantity * p.cost) AS total_cost,
    SUM(oi.line_total) - SUM(oi.quantity * p.cost) AS total_profit,
    ROUND(
        (SUM(oi.line_total) - SUM(oi.quantity * p.cost)) / 
        NULLIF(SUM(oi.line_total), 0) * 100, 
        2
    ) AS profit_margin_percentage,
    AVG(oi.unit_price) AS avg_unit_price,
    MAX(o.order_date) AS last_sale_date
FROM {{ ref('silver_products') }} p
INNER JOIN {{ ref('silver_order_items') }} oi 
    ON p.product_id = oi.product_id
INNER JOIN {{ ref('silver_orders') }} o 
    ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name, p.category, p.supplier
```

## DBT Testing & Data Quality

### Schema Tests (schema.yml)

```yaml
# dbt/models/silver/schema.yml
version: 2

models:
  - name: silver_orders
    description: "Cleaned and validated orders"
    columns:
      - name: order_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "Foreign key to customers"
        tests:
          - not_null
          - relationships:
              to: ref('silver_customers')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ['PENDING', 'COMPLETED', 'CANCELLED', 'REFUNDED']
      - name: total_amount
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

### Custom Tests

```sql
-- dbt/tests/assert_no_future_dates_in_sales.sql
SELECT order_id, order_date
FROM {{ ref('silver_orders') }}
WHERE order_date > CURRENT_DATE
```

```sql
-- dbt/tests/assert_no_negative_profit.sql
SELECT product_id, total_profit
FROM {{ ref('gold_product_performance') }}
WHERE total_profit < 0
```

### Running Tests

```bash
# Run all tests
make dbt-test

# Run tests for specific model
docker-compose exec dbt dbt test --select silver_orders

# Run specific test type
docker-compose exec dbt dbt test --select test_type:generic
docker-compose exec dbt dbt test --select test_type:singular
```

## Airflow DAG Development

### Bronze Ingestion DAG

```python
# airflow/dags/bronze_ingestion_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'bronze_ingestion_dag',
    default_args=default_args,
    description='Ingest data from MinIO to PostgreSQL Bronze layer',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['bronze', 'ingestion', 'airbyte'],
) as dag:

    trigger_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id='trigger_airbyte_orders_sync',
        airbyte_conn_id='airbyte_default',
        connection_id='{{ var.value.airbyte_connection_id }}',
        asynchronous=False,
        timeout=3600,
    )

    def validate_ingestion(**context):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        
        # Check row count
        result = pg_hook.get_first(
            "SELECT COUNT(*) FROM airbyte_raw._airbyte_raw_orders"
        )
        if result[0] == 0:
            raise ValueError("No data ingested to bronze layer")
        
        print(f"Validated {result[0]} rows in bronze layer")

    validate_task = PythonOperator(
        task_id='validate_bronze_ingestion',
        python_callable=validate_ingestion,
    )

    trigger_airbyte_sync >> validate_task
```

### Silver Transformation DAG

```python
# airflow/dags/silver_transformation_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.dbt.cloud.operators.dbt import DbtRunOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    'silver_transformation_dag',
    default_args=default_args,
    description='Transform bronze to silver layer with DBT',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['silver', 'transformation', 'dbt'],
) as dag:

    run_silver_models = BashOperator(
        task_id='run_dbt_silver_models',
        bash_command='cd /opt/dbt && dbt run --select silver.*',
    )

    test_silver_models = BashOperator(
        task_id='test_dbt_silver_models',
        bash_command='cd /opt/dbt && dbt test --select silver.*',
    )

    run_silver_models >> test_silver_models
```

### Gold Aggregation DAG

```python
# airflow/dags/gold_aggregation_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    'gold_aggregation_dag',
    default_args=default_args,
    description='Build gold layer business metrics',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['gold', 'aggregation', 'metrics'],
) as dag:

    run_gold_models = BashOperator(
        task_id='run_dbt_gold_models',
        bash_command='cd /opt/dbt && dbt run --select gold.*',
    )

    test_gold_models = BashOperator(
        task_id='test_dbt_gold_models',
        bash_command='cd /opt/dbt && dbt test --select gold.*',
    )

    snapshot_gold = BashOperator(
        task_id='snapshot_gold_metrics',
        bash_command='cd /opt/dbt && dbt snapshot',
    )

    run_gold_models >> test_gold_models >> snapshot_gold
```

## Data Upload to MinIO

```python
# scripts/upload_to_minio.py
import os
from minio import Minio
from minio.error import S3Error
import pandas as pd
from pathlib import Path

def upload_data_to_minio():
    """Upload sample CSV data to MinIO bucket"""
    
    # Initialize MinIO client
    client = Minio(
        os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
        access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )
    
    bucket_name = os.getenv('MINIO_BUCKET', 'raw-data')
    
    # Create bucket if not exists
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
    except S3Error as e:
        print(f"Error creating bucket: {e}")
        return
    
    # Upload files from data directory
    data_dir = Path('data/raw')
    for file_path in data_dir.glob('*.csv'):
        try:
            client.fput_object(
                bucket_name,
                file_path.name,
                str(file_path),
                content_type='text/csv'
            )
            print(f"Uploaded: {file_path.name}")
        except S3Error as e:
            print(f"Error uploading {file_path.name}: {e}")

if __name__ == '__main__':
    upload_data_to_minio()
```

Run the upload:

```bash
make upload-data
# or
python scripts/upload_to_minio.py
```

## Configuration

### Environment Variables (.env)

```bash
# PostgreSQL
POSTGRES_USER=dataeng
POSTGRES_PASSWORD=<your-secure-password>
POSTGRES_DB=datawarehouse
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=<your-secure-password>
MINIO_ENDPOINT=minio:9000
MINIO_BUCKET=raw-data

# Airflow
AIRFLOW_UID=50000
AIRFLOW_GID=0
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/airflow
AIRFLOW__CORE__FERNET_KEY=<generate-with-python-cryptography>

# Airbyte
AIRBYTE_VERSION=0.50.0

# DBT
DBT_PROFILES_DIR=/opt/dbt
DBT_PROJECT_DIR=/opt/dbt

# Grafana
GF_SECURITY_ADMIN_PASSWORD=<your-secure-password>
```

### DBT Profile Configuration

```yaml
# dbt/profiles.yml
datawarehouse:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('POSTGRES_HOST') }}"
      port: "{{ env_var('POSTGRES_PORT') | int }}"
      user: "{{ env_var('POSTGRES_USER') }}"
      password: "{{ env_var('POSTGRES_PASSWORD') }}"
      dbname: "{{ env_var('POSTGRES_DB') }}"
      schema: public
      threads: 4
      keepalives_idle: 0
```

### Airbyte Connection Setup

1. Access Airbyte UI: http://localhost:8000
2. Create MinIO source:
   - Connector: S3
   - Endpoint: http://minio:9000
   - Bucket: raw-data
   - Access Key: ${MINIO_ROOT_USER}
   - Secret Key: ${MINIO_ROOT_PASSWORD}

3. Create PostgreSQL destination:
   - Host: postgres
   - Port: 5432
   - Database: datawarehouse
   - Schema: bronze
   - Username: ${POSTGRES_USER}
   - Password: ${POSTGRES_PASSWORD}

4. Create connection with sync mode: Full Refresh | Overwrite

## Common Patterns

### Incremental Model Pattern

```sql
-- dbt/models/silver/silver_orders_incremental.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    schema='silver',
    on_schema_change='append_new_columns'
) }}

SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    _airbyte_emitted_at AS ingested_at
FROM {{ ref('bronze_orders') }}
{% if is_incremental() %}
WHERE _airbyte_emitted_at > (SELECT MAX(ingested_at) FROM {{ this }})
{% endif %}
```

### Macro for Common Transformations

```sql
-- dbt/macros/clean_string.sql
{% macro clean_string(column_name) %}
    UPPER(TRIM(REGEXP_REPLACE({{ column_name }}, '\s+', ' ', 'g')))
{% endmacro %}

-- Usage in model
SELECT {{ clean_string('customer_name') }} AS customer_name
FROM {{ ref('bronze_customers') }}
```

### Snapshot (SCD Type 2)

```sql
-- dbt/snapshots/snapshot_customer_segments.sql
{% snapshot snapshot_customer_segments %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at',
    )
}}

SELECT * FROM {{ ref('gold_customer_metrics') }}

{% endsnapshot %}
```

### Custom Test Macro

```sql
-- dbt/macros/test_no_orphans.sql
{% test no_orphan_records(model, column_name, parent_model, parent_column) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND {{ column_name }} NOT IN (
      SELECT {{ parent_column }}
      FROM {{ parent_model }}
  )

{% endtest %}
```

## Querying the Data Warehouse

### Bronze Layer Query

```sql
-- Raw JSONB data from Airbyte
SELECT 
    _airbyte_ab_id,
    _airbyte_emitted_at,
    _airbyte_data->>'order_id' AS order_id,
    _airbyte_data
FROM airbyte_raw._airbyte_raw_orders
LIMIT 10;
```

### Silver Layer Query

```sql
-- Cleaned typed data
SELECT 
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    order_value_segment
FROM silver.silver_orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY order_date DESC;
```

### Gold Layer Query

```sql
-- Business metrics
SELECT 
    product_name,
    category,
    total_revenue,
    total_profit,
    profit_margin_percentage,
    total_quantity_sold
FROM gold.gold_product_performance
WHERE profit_margin_percentage > 20
ORDER BY total_revenue DESC
LIMIT 10;

-- Customer segmentation
SELECT 
    customer_segment,
    COUNT(*) AS customer_count,
    AVG(total_spent) AS avg_lifetime_value,
    AVG(recency_days) AS avg_recency
FROM gold.gold_customer_metrics
GROUP BY customer_segment
ORDER BY avg_lifetime_value DESC;
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
make logs SERVICE=postgres
make logs SERVICE=airflow-webserver

# Verify resource allocation
docker system df
docker system prune  # Clean up if needed

# Reset specific service
docker-compose restart postgres
```

### Airbyte Connection Failing

```bash
# Test MinIO connectivity
docker-compose exec airbyte-worker curl http://minio:9000/minio/health/live

# Test PostgreSQL connectivity
docker-compose exec airbyte-worker \
  psql -h postgres -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1"

# Check Airbyte logs
docker-compose logs airbyte-worker | grep ERROR
```

### DBT Model Failing

```bash
# Run with debug logging
docker-compose exec dbt dbt run --select silver_orders --debug

# Check compiled SQL
cat dbt/target/compiled/datawarehouse/models/silver/silver_orders.sql

# Test single model
docker-compose exec dbt dbt run --select silver_orders --full-refresh

# Validate syntax without execution
docker-compose exec dbt dbt parse
```

### Airflow DAG Not Appearing

```bash
# Check DAG parsing errors
docker-compose exec airflow-webserver airflow dags list-import-errors

# Validate DAG Python syntax
python -m py_compile airflow/dags/bronze_ingestion_dag.py

# Refresh DAGs
docker-compose exec airflow-webserver airflow dags trigger <dag_id>
```

### PostgreSQL Connection Refused

```bash
# Wait for PostgreSQL to be ready
docker-compose exec postgres pg_isready -U ${POSTGRES_USER}

# Check connection from within container
docker-compose exec dbt psql -h postgres -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Verify connection string in .env
grep POSTGRES .env
```

### Data Quality Test Failures

```bash
# Run tests with detailed output
docker-compose exec dbt dbt test --select silver_orders --store-failures

# Query failed test results
SELECT * FROM silver.test_failures 
WHERE test_name = 'unique_order_id';

# Run specific test
docker-compose exec dbt dbt test --select test_name:unique_order_id
```

### MinIO Upload Failing

```bash
# Check MinIO service status
docker-compose ps minio

# Test MinIO API directly
docker-compose exec minio mc alias set local http://localhost:9000 \
  ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

docker-compose exec minio mc ls local/${MINIO_BUCKET}

# Upload test file
docker-compose exec minio mc cp /tmp/test.csv local/${MINIO_BUCKET}/
```

## Monitoring & Observability

### Check Pipeline Health

```bash
# Airflow task status
docker-compose exec airflow-webserver \
  airflow tasks state bronze_ingestion_dag trigger_airbyte_orders_sync 2024-01-01

# DBT run results
docker-compose exec dbt dbt run-operation log_run_results

# PostgreSQL query performance
docker-compose exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c \
  "SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

### Grafana Dashboard Access

1. Access http://localhost:3000
2. Default dashboard: PostgreSQL Overview
3. Key metrics:
   - Cache hit rate (should be >95%)
   - Active connections
   - TPS (transactions per second)
   - Query duration percentiles

### Custom Alerts

Add to `monitoring/prometheus/alerts.yml`:

```yaml
groups:
  - name: dbt_pipeline
    rules:
      - alert: DBTModelFailed
        expr: dbt_model_run_status{status="error"} > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "DBT model {{ $labels.model }} failed"
```

This skill covers the complete data-engineering-medallion pipeline from setup through production operations, enabling AI agents to assist with implementation, troubleshooting, and extension of medallion architecture data pipelines.
