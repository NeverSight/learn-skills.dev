---
name: retail-etl-pipeline-medallion
description: End-to-end retail ETL pipeline using PySpark, SQL Server, and Medallion Architecture (Bronze/Silver/Gold layers) for data warehousing
triggers:
  - set up a retail ETL pipeline with medallion architecture
  - build a bronze silver gold data warehouse for retail
  - create an ETL pipeline for retail sales and inventory data
  - implement medallion architecture for retail analytics
  - process retail data through bronze silver and gold layers
  - design a data pipeline for retail inventory and sales tracking
  - build a data warehouse following medallion architecture pattern
  - create stored procedures for retail ETL transformations
---

# Retail ETL Pipeline - Medallion Architecture Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection

## Overview

The Retail ETL Pipeline project implements a complete data engineering solution for retail operations using the **Medallion Architecture** pattern (Bronze → Silver → Gold layers). It handles complex retail scenarios including:

- **Inventory shrinkage** resolution
- **Recipe conversions** for meat/poultry products
- **Supplier rebate tier** tracking
- **Multi-branch sales** consolidation
- **Stock level** management across locations

The pipeline processes raw CSV data from CRM/ERP systems through three progressive quality layers, ultimately delivering a "Single Version of Truth" for business intelligence.

## Architecture Layers

### Bronze Layer (Raw Ingestion)
- Raw data ingestion from CSV files
- Minimal transformation, preserving source format
- Audit columns: `_loaded_at`, `_source_file`

### Silver Layer (Cleaned & Standardized)
- Data type enforcement
- Deduplication
- Standardization (dates, currencies, product codes)
- Business rule validation

### Gold Layer (Business-Ready Analytics)
- Aggregated metrics
- Calculated KPIs (inventory turnover, shrinkage %)
- Dimensional models for BI tools

## Installation & Setup

### Prerequisites

```bash
# Required tools
- Docker & Docker Compose
- SQL Server 2019+
- Python 3.8+
- PySpark 3.x
- Apache Airflow (optional, for orchestration)
```

### Infrastructure Setup

```bash
# Clone the repository
git clone https://github.com/EsraaSolimanMubarak/Retail-ETL-Pipeline.git
cd Retail-ETL-Pipeline

# Start SQL Server container
docker-compose up -d

# Wait for SQL Server to be ready
docker logs -f retail-sql-server
```

### Database Initialization

```bash
# Connect to SQL Server and run schema setup
sqlcmd -S localhost,1433 -U sa -P ${SQL_SERVER_PASSWORD} \
  -i sql_scripts/00_create_database_and_schemas.sql
```

## Key SQL Scripts Execution Order

The pipeline consists of 13+ SQL scripts that must be executed sequentially:

```bash
# 1. Create database and schemas
sql_scripts/00_create_database_and_schemas.sql

# 2. Bronze layer ingestion
sql_scripts/01_bronze_products.sql
sql_scripts/02_bronze_sales.sql
sql_scripts/03_bronze_stock.sql

# 3. Silver layer transformations
sql_scripts/04_silver_products.sql
sql_scripts/05_silver_sales.sql
sql_scripts/06_silver_stock.sql

# 4. Gold layer aggregations
sql_scripts/07_gold_sales_summary.sql
sql_scripts/08_gold_inventory_metrics.sql
sql_scripts/09_gold_product_performance.sql

# 5. Rebuild pipeline (if needed)
sql_scripts/12_rebuild_inventory_pipeline_final_fix.sql
```

## Core ETL Patterns

### Pattern 1: Bronze Layer Ingestion (Raw CSV → SQL)

```sql
-- Example: Bronze Products Table
CREATE TABLE bronze.products (
    product_id INT,
    product_name NVARCHAR(255),
    category NVARCHAR(100),
    unit_price DECIMAL(10,2),
    supplier_id INT,
    _loaded_at DATETIME2 DEFAULT GETDATE(),
    _source_file NVARCHAR(500)
);

-- Bulk insert from CSV
BULK INSERT bronze.products
FROM '/data_source/000.Hypermarket Products.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    TABLOCK
);
```

### Pattern 2: Silver Layer Cleansing

```sql
-- Example: Silver Products with Data Quality Rules
CREATE PROCEDURE silver.usp_transform_products
AS
BEGIN
    TRUNCATE TABLE silver.products;
    
    INSERT INTO silver.products (
        product_id,
        product_name,
        category,
        unit_price,
        supplier_id,
        is_active,
        processed_at
    )
    SELECT DISTINCT
        product_id,
        UPPER(TRIM(product_name)) AS product_name,
        COALESCE(category, 'UNCATEGORIZED') AS category,
        CASE 
            WHEN unit_price < 0 THEN 0 
            ELSE unit_price 
        END AS unit_price,
        supplier_id,
        1 AS is_active,
        GETDATE() AS processed_at
    FROM bronze.products
    WHERE product_id IS NOT NULL
      AND product_name IS NOT NULL;
END;
```

### Pattern 3: Gold Layer Aggregations

```sql
-- Example: Sales Summary by Branch and Product
CREATE PROCEDURE gold.usp_sales_summary
AS
BEGIN
    TRUNCATE TABLE gold.sales_summary;
    
    INSERT INTO gold.sales_summary (
        branch_name,
        product_category,
        total_quantity_sold,
        total_revenue,
        avg_unit_price,
        transaction_count,
        report_date
    )
    SELECT 
        s.branch_name,
        p.category AS product_category,
        SUM(s.quantity) AS total_quantity_sold,
        SUM(s.quantity * s.unit_price) AS total_revenue,
        AVG(s.unit_price) AS avg_unit_price,
        COUNT(DISTINCT s.transaction_id) AS transaction_count,
        CAST(GETDATE() AS DATE) AS report_date
    FROM silver.sales s
    INNER JOIN silver.products p ON s.product_id = p.product_id
    GROUP BY s.branch_name, p.category;
END;
```

### Pattern 4: Inventory Shrinkage Calculation

```sql
-- Complex business logic: Detect inventory discrepancies
CREATE PROCEDURE gold.usp_inventory_shrinkage
AS
BEGIN
    WITH StockLevels AS (
        SELECT 
            product_id,
            branch_name,
            SUM(quantity_on_hand) AS current_stock
        FROM silver.stock
        GROUP BY product_id, branch_name
    ),
    ExpectedStock AS (
        SELECT 
            s.product_id,
            s.branch_name,
            sl.current_stock - COALESCE(SUM(s.quantity), 0) AS expected_stock
        FROM StockLevels sl
        LEFT JOIN silver.sales s 
            ON sl.product_id = s.product_id 
            AND sl.branch_name = s.branch_name
        GROUP BY s.product_id, s.branch_name, sl.current_stock
    )
    INSERT INTO gold.inventory_shrinkage (
        product_id,
        branch_name,
        current_stock,
        expected_stock,
        shrinkage_qty,
        shrinkage_percent,
        calculated_at
    )
    SELECT 
        sl.product_id,
        sl.branch_name,
        sl.current_stock,
        es.expected_stock,
        sl.current_stock - es.expected_stock AS shrinkage_qty,
        CASE 
            WHEN es.expected_stock > 0 
            THEN ((sl.current_stock - es.expected_stock) * 100.0 / es.expected_stock)
            ELSE 0 
        END AS shrinkage_percent,
        GETDATE() AS calculated_at
    FROM StockLevels sl
    INNER JOIN ExpectedStock es 
        ON sl.product_id = es.product_id 
        AND sl.branch_name = es.branch_name;
END;
```

## PySpark Integration (Optional)

For large-scale data processing, integrate PySpark for Silver/Gold transformations:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RetailETL-Silver") \
    .config("spark.sql.warehouse.dir", "/data/warehouse") \
    .getOrCreate()

# Read Bronze layer (Parquet or Delta)
bronze_sales_df = spark.read.parquet("/data/bronze/sales/")

# Silver transformations
silver_sales_df = bronze_sales_df \
    .dropDuplicates(["transaction_id"]) \
    .filter(col("quantity") > 0) \
    .withColumn("unit_price", 
                when(col("unit_price") < 0, 0).otherwise(col("unit_price"))) \
    .withColumn("total_amount", col("quantity") * col("unit_price"))

# Write to Silver layer
silver_sales_df.write \
    .mode("overwrite") \
    .partitionBy("branch_name", "sale_date") \
    .parquet("/data/silver/sales/")

# Gold aggregations
gold_sales_summary = silver_sales_df \
    .groupBy("branch_name", "product_category") \
    .agg(
        sum("quantity").alias("total_quantity"),
        sum("total_amount").alias("total_revenue"),
        avg("unit_price").alias("avg_unit_price"),
        count("transaction_id").alias("transaction_count")
    )

gold_sales_summary.write \
    .mode("overwrite") \
    .parquet("/data/gold/sales_summary/")
```

## Airflow DAG Example

Orchestrate the entire pipeline with Apache Airflow:

```python
from airflow import DAG
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'retail_etl_medallion',
    default_args=default_args,
    description='Daily Retail ETL Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Bronze ingestion
    ingest_products = MsSqlOperator(
        task_id='bronze_ingest_products',
        mssql_conn_id='retail_sql_server',
        sql='sql_scripts/01_bronze_products.sql',
    )
    
    ingest_sales = MsSqlOperator(
        task_id='bronze_ingest_sales',
        mssql_conn_id='retail_sql_server',
        sql='sql_scripts/02_bronze_sales.sql',
    )
    
    ingest_stock = MsSqlOperator(
        task_id='bronze_ingest_stock',
        mssql_conn_id='retail_sql_server',
        sql='sql_scripts/03_bronze_stock.sql',
    )
    
    # Silver transformations
    transform_products = MsSqlOperator(
        task_id='silver_transform_products',
        mssql_conn_id='retail_sql_server',
        sql='EXEC silver.usp_transform_products;',
    )
    
    transform_sales = MsSqlOperator(
        task_id='silver_transform_sales',
        mssql_conn_id='retail_sql_server',
        sql='EXEC silver.usp_transform_sales;',
    )
    
    # Gold aggregations
    aggregate_sales_summary = MsSqlOperator(
        task_id='gold_sales_summary',
        mssql_conn_id='retail_sql_server',
        sql='EXEC gold.usp_sales_summary;',
    )
    
    aggregate_inventory_shrinkage = MsSqlOperator(
        task_id='gold_inventory_shrinkage',
        mssql_conn_id='retail_sql_server',
        sql='EXEC gold.usp_inventory_shrinkage;',
    )
    
    # Define dependencies
    [ingest_products, ingest_sales, ingest_stock] >> transform_products
    [ingest_sales] >> transform_sales
    [transform_products, transform_sales] >> aggregate_sales_summary
    [transform_products, ingest_stock] >> aggregate_inventory_shrinkage
```

## Configuration

### Environment Variables

```bash
# SQL Server connection
export SQL_SERVER_HOST=localhost
export SQL_SERVER_PORT=1433
export SQL_SERVER_USER=sa
export SQL_SERVER_PASSWORD=${YOUR_SECURE_PASSWORD}
export SQL_SERVER_DATABASE=RetailDataWarehouse

# Data paths
export DATA_SOURCE_PATH=/data_source
export BRONZE_LAYER_PATH=/data/bronze
export SILVER_LAYER_PATH=/data/silver
export GOLD_LAYER_PATH=/data/gold

# Airflow (if used)
export AIRFLOW_CONN_RETAIL_SQL_SERVER="mssql://${SQL_SERVER_USER}:${SQL_SERVER_PASSWORD}@${SQL_SERVER_HOST}:${SQL_SERVER_PORT}/${SQL_SERVER_DATABASE}"
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2019-latest
    container_name: retail-sql-server
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=${SQL_SERVER_PASSWORD}
      - MSSQL_PID=Developer
    ports:
      - "1433:1433"
    volumes:
      - ./data_source:/data_source
      - ./sql_scripts:/sql_scripts
      - sqlserver_data:/var/opt/mssql

volumes:
  sqlserver_data:
```

## Common Patterns & Use Cases

### Use Case 1: Multi-Branch Sales Consolidation

```sql
-- Combine sales from Alex, Cairo, and Giza branches
CREATE VIEW gold.vw_consolidated_sales AS
SELECT 
    'Alexandria' AS branch_name,
    * 
FROM bronze.alex_sales
UNION ALL
SELECT 
    'Cairo' AS branch_name,
    * 
FROM bronze.cairo_sales
UNION ALL
SELECT 
    'Giza' AS branch_name,
    * 
FROM bronze.giza_sales;
```

### Use Case 2: Recipe Yield Tracking (Meat/Poultry)

```sql
-- Track conversion rates for processed meat products
CREATE TABLE silver.recipe_conversions (
    recipe_id INT PRIMARY KEY,
    raw_product_id INT,
    finished_product_id INT,
    conversion_ratio DECIMAL(5,2), -- e.g., 0.85 (15% waste)
    effective_date DATE
);

-- Calculate actual yield vs. expected
SELECT 
    rc.recipe_id,
    SUM(s.quantity * rc.conversion_ratio) AS expected_yield,
    SUM(stock.quantity_on_hand) AS actual_yield,
    (SUM(stock.quantity_on_hand) - SUM(s.quantity * rc.conversion_ratio)) AS yield_variance
FROM silver.sales s
INNER JOIN silver.recipe_conversions rc ON s.product_id = rc.raw_product_id
INNER JOIN silver.stock stock ON rc.finished_product_id = stock.product_id
GROUP BY rc.recipe_id;
```

### Use Case 3: Supplier Rebate Tier Tracking

```sql
-- Track purchase volume for supplier rebate calculations
CREATE TABLE gold.supplier_rebate_tiers (
    supplier_id INT,
    total_purchases DECIMAL(15,2),
    rebate_tier VARCHAR(20),
    rebate_percentage DECIMAL(5,2),
    calculated_at DATETIME2
);

INSERT INTO gold.supplier_rebate_tiers
SELECT 
    p.supplier_id,
    SUM(s.quantity * s.unit_price) AS total_purchases,
    CASE 
        WHEN SUM(s.quantity * s.unit_price) > 100000 THEN 'Platinum'
        WHEN SUM(s.quantity * s.unit_price) > 50000 THEN 'Gold'
        WHEN SUM(s.quantity * s.unit_price) > 25000 THEN 'Silver'
        ELSE 'Bronze'
    END AS rebate_tier,
    CASE 
        WHEN SUM(s.quantity * s.unit_price) > 100000 THEN 5.0
        WHEN SUM(s.quantity * s.unit_price) > 50000 THEN 3.5
        WHEN SUM(s.quantity * s.unit_price) > 25000 THEN 2.0
        ELSE 1.0
    END AS rebate_percentage,
    GETDATE() AS calculated_at
FROM silver.sales s
INNER JOIN silver.products p ON s.product_id = p.product_id
GROUP BY p.supplier_id;
```

## Troubleshooting

### Issue 1: CSV Bulk Insert Fails

```sql
-- Check file path permissions
EXEC xp_cmdshell 'dir C:\data_source\*.csv';

-- Use ERRORFILE to capture bad rows
BULK INSERT bronze.products
FROM '/data_source/000.Hypermarket Products.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    ERRORFILE = '/data_source/errors/products_errors.csv',
    MAXERRORS = 10
);
```

### Issue 2: Duplicate Records in Silver Layer

```sql
-- Add deduplication logic with ROW_NUMBER
WITH DeduplicatedSales AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY transaction_id 
            ORDER BY _loaded_at DESC
        ) AS rn
    FROM bronze.sales
)
INSERT INTO silver.sales
SELECT * 
FROM DeduplicatedSales
WHERE rn = 1;
```

### Issue 3: Performance Optimization

```sql
-- Create indexes on frequently joined columns
CREATE NONCLUSTERED INDEX idx_sales_product_id 
    ON silver.sales(product_id) INCLUDE (quantity, unit_price);

CREATE NONCLUSTERED INDEX idx_stock_product_branch 
    ON silver.stock(product_id, branch_name) INCLUDE (quantity_on_hand);

-- Partition large tables by date
CREATE PARTITION FUNCTION pf_sales_date (DATE)
AS RANGE RIGHT FOR VALUES (
    '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01'
);
```

### Issue 4: Rebuild Entire Pipeline

```bash
# Use the rebuild script to reset and reprocess all layers
sqlcmd -S ${SQL_SERVER_HOST},${SQL_SERVER_PORT} \
  -U ${SQL_SERVER_USER} -P ${SQL_SERVER_PASSWORD} \
  -d RetailDataWarehouse \
  -i sql_scripts/12_rebuild_inventory_pipeline_final_fix.sql
```

## Testing Data Quality

```sql
-- Data quality checks for Silver layer
SELECT 'Products' AS layer,
    COUNT(*) AS total_records,
    COUNT(DISTINCT product_id) AS unique_products,
    SUM(CASE WHEN unit_price < 0 THEN 1 ELSE 0 END) AS negative_prices,
    SUM(CASE WHEN product_name IS NULL THEN 1 ELSE 0 END) AS null_names
FROM silver.products

UNION ALL

SELECT 'Sales' AS layer,
    COUNT(*) AS total_records,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS invalid_quantity,
    SUM(CASE WHEN product_id NOT IN (SELECT product_id FROM silver.products) THEN 1 ELSE 0 END) AS orphaned_products
FROM silver.sales;
```

## Best Practices

1. **Always process through layers sequentially**: Bronze → Silver → Gold
2. **Use stored procedures** for reusable transformations
3. **Add audit columns** (`_loaded_at`, `_source_file`, `processed_at`)
4. **Implement idempotency**: Truncate-and-load or upsert patterns
5. **Partition large tables** by date or branch for performance
6. **Create comprehensive indexes** on join and filter columns
7. **Use CTEs** for complex business logic readability
8. **Test data quality** at each layer transition
9. **Version control** all SQL scripts and configurations
10. **Monitor pipeline execution** with Airflow or equivalent orchestrator
