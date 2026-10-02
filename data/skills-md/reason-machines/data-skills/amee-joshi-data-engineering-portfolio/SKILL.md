---
name: amee-joshi-data-engineering-portfolio
description: Reference portfolio demonstrating Azure data engineering patterns, Medallion architecture, and end-to-end analytics solutions
triggers:
  - show me data engineering portfolio examples
  - how to build azure data pipelines
  - what is medallion architecture implementation
  - data engineering project structure examples
  - how to design lakehouse architecture
  - azure databricks end-to-end patterns
  - data warehouse modeling examples
  - ETL pipeline design patterns
---

# Amee Joshi Data Engineering Portfolio

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This portfolio showcases production-grade data engineering patterns and architectures for building scalable, cloud-native data platforms. It demonstrates end-to-end solutions covering data ingestion, transformation, modeling, and analytics using Azure services, Databricks, SQL Server, and BI tools.

## What This Portfolio Demonstrates

This is a reference collection showing:

- **Medallion Architecture (Bronze-Silver-Gold)** implementations
- **Azure cloud data platforms** (ADF, ADLS Gen2, Databricks, Synapse Analytics)
- **Data lakehouse patterns** with Delta Lake
- **Dimensional modeling** (Star Schema, SCD Type 1 & 2)
- **Metadata-driven ingestion frameworks**
- **Analytics-ready datasets** for BI consumption
- **ETL/ELT pipeline design** with incremental loading
- **Power BI and Tableau** reporting solutions

## Key Portfolio Projects

### 1. Azure Databricks Retail Lakehouse

**Repository:** `azure-databricks-end-to-end-retail-lakehouse`

**Pattern:** Enterprise Medallion Architecture with Delta Lake

**Architecture:**
```
Bronze (Raw) → Silver (Cleansed) → Gold (Analytics-Ready)
```

**Key Implementation Concepts:**

```python
# Bronze Layer - Raw Ingestion
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# Ingest raw data with metadata
df_raw = (spark.read
    .format("parquet")
    .load(f"{bronze_path}/source_data/")
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file", input_file_name())
)

# Write to Bronze Delta table
(df_raw.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .save(f"{bronze_path}/retail_transactions")
)
```

```python
# Silver Layer - Data Quality & Transformation
from pyspark.sql.functions import col, when, trim, upper

# Cleanse and standardize
df_silver = (df_bronze
    .filter(col("transaction_id").isNotNull())
    .withColumn("customer_name", trim(upper(col("customer_name"))))
    .withColumn("transaction_amount", 
                when(col("transaction_amount") < 0, 0)
                .otherwise(col("transaction_amount")))
    .dropDuplicates(["transaction_id"])
    .select("transaction_id", "customer_id", "product_id", 
            "transaction_amount", "transaction_date")
)

# Write with schema enforcement
(df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "false")
    .save(f"{silver_path}/transactions")
)
```

```python
# Gold Layer - SCD Type 2 Dimension
def apply_scd_type2(target_table, source_df, key_columns, scd_columns):
    """
    Implements Slowly Changing Dimension Type 2
    """
    from delta.tables import DeltaTable
    from pyspark.sql.functions import lit, current_timestamp
    
    # Prepare source with SCD metadata
    source_prepared = (source_df
        .withColumn("effective_date", current_timestamp())
        .withColumn("end_date", lit(None).cast("timestamp"))
        .withColumn("is_current", lit(True))
    )
    
    # Read existing target
    target_delta = DeltaTable.forPath(spark, target_table)
    
    # Identify changes
    merge_condition = " AND ".join([f"target.{k} = source.{k}" for k in key_columns])
    
    # Perform SCD Type 2 merge
    (target_delta.alias("target")
        .merge(source_prepared.alias("source"), merge_condition)
        .whenMatchedUpdate(
            condition = "target.is_current = true AND " + 
                       " OR ".join([f"target.{c} != source.{c}" for c in scd_columns]),
            set = {
                "is_current": "false",
                "end_date": "current_timestamp()"
            }
        )
        .whenNotMatchedInsertAll()
        .execute()
    )
```

### 2. Metadata-Driven Ingestion Framework

**Pattern:** Dynamic, configuration-based pipeline generation

**Configuration Schema:**

```json
{
  "pipeline_config": {
    "source_system": "SQL_SERVER",
    "target_layer": "bronze",
    "ingestion_type": "incremental",
    "watermark_column": "modified_date",
    "tables": [
      {
        "schema_name": "sales",
        "table_name": "orders",
        "partition_column": "order_date",
        "primary_key": ["order_id"],
        "target_path": "/bronze/sales/orders"
      }
    ]
  }
}
```

**Azure Data Factory Pattern:**

```python
# Dynamic pipeline parameter processing
# This represents the logic implemented in ADF

def generate_copy_activity(table_config):
    """
    Generates ADF copy activity from metadata
    """
    return {
        "name": f"Copy_{table_config['table_name']}",
        "type": "Copy",
        "inputs": [{
            "referenceName": "SourceDataset",
            "type": "DatasetReference",
            "parameters": {
                "schemaName": table_config['schema_name'],
                "tableName": table_config['table_name']
            }
        }],
        "outputs": [{
            "referenceName": "SinkDataset",
            "type": "DatasetReference",
            "parameters": {
                "targetPath": table_config['target_path']
            }
        }],
        "typeProperties": {
            "source": {
                "type": "SqlServerSource",
                "sqlReaderQuery": f"""
                    SELECT * FROM {table_config['schema_name']}.{table_config['table_name']}
                    WHERE {table_config['watermark_column']} > '@{{pipeline().parameters.watermarkValue}}'
                """
            },
            "sink": {
                "type": "ParquetSink",
                "storeSettings": {
                    "type": "AzureBlobFSWriteSettings",
                    "copyBehavior": "PreserveHierarchy"
                }
            }
        }
    }
```

### 3. Star Schema Data Warehouse

**Pattern:** Dimensional Modeling with SQL Server

**Dimension Table (SCD Type 1):**

```sql
-- Dimension: Product (SCD Type 1)
CREATE TABLE dim_product (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    product_name NVARCHAR(100),
    category NVARCHAR(50),
    subcategory NVARCHAR(50),
    unit_price DECIMAL(10,2),
    modified_date DATETIME DEFAULT GETDATE(),
    CONSTRAINT uk_product UNIQUE (product_id)
);

-- ETL Merge (SCD Type 1 - Overwrite)
MERGE INTO dim_product AS target
USING (
    SELECT 
        product_id,
        product_name,
        category,
        subcategory,
        unit_price
    FROM staging.products
) AS source
ON target.product_id = source.product_id
WHEN MATCHED AND (
    target.product_name != source.product_name OR
    target.category != source.category OR
    target.unit_price != source.unit_price
)
THEN UPDATE SET
    target.product_name = source.product_name,
    target.category = source.category,
    target.subcategory = source.subcategory,
    target.unit_price = source.unit_price,
    target.modified_date = GETDATE()
WHEN NOT MATCHED BY TARGET
THEN INSERT (product_id, product_name, category, subcategory, unit_price)
VALUES (source.product_id, source.product_name, source.category, 
        source.subcategory, source.unit_price);
```

**Dimension Table (SCD Type 2):**

```sql
-- Dimension: Customer (SCD Type 2)
CREATE TABLE dim_customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_name NVARCHAR(100),
    email NVARCHAR(100),
    city NVARCHAR(50),
    state NVARCHAR(50),
    effective_date DATETIME NOT NULL,
    end_date DATETIME NULL,
    is_current BIT DEFAULT 1,
    CONSTRAINT uk_customer_current UNIQUE (customer_id, is_current)
);

-- ETL for SCD Type 2
-- Step 1: Expire changed records
UPDATE dim_customer
SET 
    end_date = GETDATE(),
    is_current = 0
WHERE customer_id IN (
    SELECT s.customer_id
    FROM staging.customers s
    INNER JOIN dim_customer d ON s.customer_id = d.customer_id
    WHERE d.is_current = 1
    AND (s.city != d.city OR s.state != d.state)
);

-- Step 2: Insert new versions
INSERT INTO dim_customer (
    customer_id, customer_name, email, city, state, 
    effective_date, end_date, is_current
)
SELECT 
    s.customer_id,
    s.customer_name,
    s.email,
    s.city,
    s.state,
    GETDATE() AS effective_date,
    NULL AS end_date,
    1 AS is_current
FROM staging.customers s
LEFT JOIN dim_customer d ON s.customer_id = d.customer_id AND d.is_current = 1
WHERE d.customer_key IS NULL
   OR s.city != d.city
   OR s.state != d.state;
```

**Fact Table:**

```sql
-- Fact: Sales Transactions
CREATE TABLE fact_sales (
    sales_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    store_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_date FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    CONSTRAINT fk_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_product FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    CONSTRAINT fk_store FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- Create columnstore index for analytics
CREATE NONCLUSTERED COLUMNSTORE INDEX idx_fact_sales_cs
ON fact_sales (date_key, customer_key, product_key, store_key, 
               quantity, unit_price, total_amount);

-- ETL Load
INSERT INTO fact_sales (
    date_key, customer_key, product_key, store_key,
    quantity, unit_price, discount_amount, tax_amount, total_amount
)
SELECT 
    dd.date_key,
    dc.customer_key,
    dp.product_key,
    ds.store_key,
    st.quantity,
    st.unit_price,
    st.discount_amount,
    st.tax_amount,
    st.total_amount
FROM staging.transactions st
INNER JOIN dim_date dd ON CAST(st.transaction_date AS DATE) = dd.date
INNER JOIN dim_customer dc ON st.customer_id = dc.customer_id AND dc.is_current = 1
INNER JOIN dim_product dp ON st.product_id = dp.product_id
INNER JOIN dim_store ds ON st.store_id = ds.store_id;
```

### 4. Incremental Data Loading Pattern

**Watermark-Based Incremental Load:**

```python
# Databricks notebook - Incremental load with watermark

from pyspark.sql.functions import col, max as spark_max
from delta.tables import DeltaTable

# Configuration
source_table = "source_database.transactions"
target_path = "/mnt/silver/transactions"
watermark_table = "control.watermark"
watermark_column = "modified_date"

# Get last watermark
last_watermark = (spark.table(watermark_table)
    .filter(col("table_name") == source_table)
    .select("watermark_value")
    .first()[0]
)

# Read incremental data
df_incremental = (spark.table(source_table)
    .filter(col(watermark_column) > last_watermark)
)

# Check if target exists
if DeltaTable.isDeltaTable(spark, target_path):
    # Merge into existing table
    target_table = DeltaTable.forPath(spark, target_path)
    
    (target_table.alias("target")
        .merge(
            df_incremental.alias("source"),
            "target.transaction_id = source.transaction_id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
else:
    # Initial load
    (df_incremental.write
        .format("delta")
        .mode("overwrite")
        .save(target_path)
    )

# Update watermark
new_watermark = df_incremental.agg(spark_max(watermark_column)).first()[0]

spark.sql(f"""
    UPDATE {watermark_table}
    SET watermark_value = '{new_watermark}',
        last_updated = current_timestamp()
    WHERE table_name = '{source_table}'
""")
```

### 5. Data Quality Framework

**Quality Checks Pattern:**

```python
from pyspark.sql.functions import col, count, sum as spark_sum, when

class DataQualityChecker:
    """
    Data quality validation framework
    """
    
    def __init__(self, dataframe, table_name):
        self.df = dataframe
        self.table_name = table_name
        self.quality_results = []
    
    def check_null_values(self, columns):
        """Check for null values in critical columns"""
        for column in columns:
            null_count = self.df.filter(col(column).isNull()).count()
            total_count = self.df.count()
            
            self.quality_results.append({
                "check_type": "null_check",
                "column": column,
                "null_count": null_count,
                "total_count": total_count,
                "null_percentage": (null_count / total_count * 100) if total_count > 0 else 0,
                "passed": null_count == 0
            })
        return self
    
    def check_duplicates(self, key_columns):
        """Check for duplicate records"""
        duplicate_count = (self.df
            .groupBy(key_columns)
            .count()
            .filter(col("count") > 1)
            .count()
        )
        
        self.quality_results.append({
            "check_type": "duplicate_check",
            "key_columns": key_columns,
            "duplicate_count": duplicate_count,
            "passed": duplicate_count == 0
        })
        return self
    
    def check_referential_integrity(self, foreign_key, reference_df, reference_key):
        """Check referential integrity"""
        missing_references = (self.df
            .select(foreign_key)
            .distinct()
            .join(reference_df.select(reference_key), 
                  col(foreign_key) == col(reference_key), 
                  "left_anti")
            .count()
        )
        
        self.quality_results.append({
            "check_type": "referential_integrity",
            "foreign_key": foreign_key,
            "missing_references": missing_references,
            "passed": missing_references == 0
        })
        return self
    
    def check_value_range(self, column, min_value=None, max_value=None):
        """Check if values are within expected range"""
        out_of_range = self.df.filter(
            (col(column) < min_value if min_value is not None else False) |
            (col(column) > max_value if max_value is not None else False)
        ).count()
        
        self.quality_results.append({
            "check_type": "range_check",
            "column": column,
            "min_value": min_value,
            "max_value": max_value,
            "out_of_range_count": out_of_range,
            "passed": out_of_range == 0
        })
        return self
    
    def get_results(self):
        """Return quality check results"""
        return self.quality_results

# Usage example
df_transactions = spark.read.format("delta").load("/mnt/silver/transactions")
df_customers = spark.read.format("delta").load("/mnt/gold/dim_customer")

quality_checker = DataQualityChecker(df_transactions, "transactions")

results = (quality_checker
    .check_null_values(["transaction_id", "customer_id", "transaction_date"])
    .check_duplicates(["transaction_id"])
    .check_referential_integrity("customer_id", df_customers, "customer_id")
    .check_value_range("transaction_amount", min_value=0, max_value=100000)
    .get_results()
)

# Log results
for result in results:
    print(f"{result['check_type']}: {'PASSED' if result['passed'] else 'FAILED'}")
```

## Power BI Analytics Patterns

**DAX Measures for KPIs:**

```dax
// Total Sales
Total Sales = SUM(fact_sales[total_amount])

// Year-over-Year Growth
Sales YoY Growth = 
VAR CurrentYearSales = [Total Sales]
VAR PreviousYearSales = 
    CALCULATE(
        [Total Sales],
        DATEADD(dim_date[Date], -1, YEAR)
    )
RETURN
    DIVIDE(
        CurrentYearSales - PreviousYearSales,
        PreviousYearSales,
        0
    )

// Customer Lifetime Value
Customer LTV = 
CALCULATE(
    [Total Sales],
    ALLEXCEPT(dim_customer, dim_customer[customer_id])
)

// Moving Average (3 months)
Sales 3M MA = 
CALCULATE(
    [Total Sales],
    DATESINPERIOD(
        dim_date[Date],
        LASTDATE(dim_date[Date]),
        -3,
        MONTH
    )
) / 3

// Rank by Sales
Product Sales Rank = 
RANKX(
    ALL(dim_product[product_name]),
    [Total Sales],
    ,
    DESC,
    DENSE
)
```

## Common Architectural Patterns

### Medallion Architecture Best Practices

**Bronze Layer:**
- Raw data ingestion with minimal transformation
- Add audit columns (ingestion_timestamp, source_file)
- Preserve source schema with schema evolution enabled
- Partition by ingestion date for performance

**Silver Layer:**
- Data cleansing and standardization
- Deduplication based on business keys
- Data type conversions and validations
- Enforce schema constraints
- Join related datasets

**Gold Layer:**
- Business-aggregated datasets
- Dimensional models (Star/Snowflake schema)
- Pre-calculated metrics and KPIs
- Optimized for BI tool consumption

### Delta Lake Optimization

```python
# Optimize Delta tables
from delta.tables import DeltaTable

# Optimize with Z-ordering
deltaTable = DeltaTable.forPath(spark, "/mnt/gold/fact_sales")

# Optimize files and Z-order by common filter columns
deltaTable.optimize().executeZOrderBy("date_key", "customer_key")

# Vacuum old files (retention 168 hours = 7 days)
deltaTable.vacuum(168)

# Update table statistics
spark.sql("ANALYZE TABLE gold.fact_sales COMPUTE STATISTICS FOR ALL COLUMNS")
```

### Unity Catalog Security

```sql
-- Create catalog and schema
CREATE CATALOG IF NOT EXISTS retail_analytics;
CREATE SCHEMA IF NOT EXISTS retail_analytics.gold;

-- Grant permissions
GRANT USE CATALOG ON CATALOG retail_analytics TO `data_analysts`;
GRANT USE SCHEMA ON SCHEMA retail_analytics.gold TO `data_analysts`;
GRANT SELECT ON TABLE retail_analytics.gold.fact_sales TO `data_analysts`;

-- Row-level security
CREATE FUNCTION retail_analytics.gold.customer_filter(customer_region STRING)
RETURN customer_region = current_user_region();

ALTER TABLE retail_analytics.gold.fact_sales 
SET ROW FILTER retail_analytics.gold.customer_filter ON (region);
```

## Environment Setup

**Azure Configuration:**

```bash
# Set Azure environment variables
export AZURE_SUBSCRIPTION_ID=your_subscription_id
export AZURE_RESOURCE_GROUP=rg-data-platform
export AZURE_STORAGE_ACCOUNT=datalakestorage
export AZURE_DATABRICKS_WORKSPACE=databricks-workspace

# ADF connection
export ADF_FACTORY_NAME=adf-data-ingestion
export ADF_LINKED_SERVICE_NAME=ls-sqlserver-source
```

**Databricks Configuration:**

```python
# Mount ADLS Gen2 in Databricks
configs = {
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope="keyvault", key="client-id"),
    "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="keyvault", key="client-secret"),
    "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{dbutils.secrets.get(scope='keyvault', key='tenant-id')}/oauth2/token"
}

dbutils.fs.mount(
    source = "abfss://bronze@datalakestorage.dfs.core.windows.net/",
    mount_point = "/mnt/bronze",
    extra_configs = configs
)
```

## Troubleshooting

**Issue: Delta Lake merge taking too long**

```python
# Solution: Optimize before merge
from delta.tables import DeltaTable

target_table = DeltaTable.forPath(spark, target_path)

# Compact small files first
target_table.optimize().executeCompaction()

# Enable auto-optimize and auto-compaction
spark.sql(f"""
    ALTER TABLE delta.`{target_path}`
    SET TBLPROPERTIES (
        delta.autoOptimize.optimizeWrite = true,
        delta.autoOptimize.autoCompact = true
    )
""")
```

**Issue: ADF pipeline timeout**

```json
// Increase timeout in ADF pipeline activity
{
  "typeProperties": {
    "timeout": "0.12:00:00"
  },
  "policy": {
    "timeout": "7.00:00:00",
    "retry": 2,
    "retryIntervalInSeconds": 30
  }
}
```

**Issue: Power BI slow refresh**

```dax
// Use incremental refresh configuration
// In Power BI Desktop: Table Tools > Incremental Refresh

// Or optimize DAX measures
Optimized Total Sales = 
CALCULATE(
    SUM(fact_sales[total_amount]),
    KEEPFILTERS(dim_date[Date])  // Reduce context transition overhead
)
```

**Issue: Schema evolution conflicts**

```python
# Enable schema merging in Delta writes
(df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .save(target_path)
)

# Or explicitly allow schema overwrite
(df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(target_path)
)
```

## Reference Architecture

This portfolio demonstrates a typical enterprise data platform architecture:

```
┌─────────────────┐
│  Source Systems │
│  (SQL Server,   │
│   APIs, Files)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Azure Data     │
│  Factory (ADF)  │ ◄──── Metadata-driven ingestion
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ADLS Gen2      │
│  Bronze Layer   │ ◄──── Raw data landing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Databricks     │
│  Silver Layer   │ ◄──── Cleansing & transformation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Databricks     │
│  Gold Layer     │ ◄──── Analytics-ready datasets
└────────┬────────┘
         │
         ├──────────────────┐
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│  Power BI       │  │  Synapse        │
│  Reporting      │  │  Analytics      │
└─────────────────┘  └─────────────────┘
```

This skill provides patterns and code examples for building production-grade data platforms following industry best practices demonstrated across the portfolio projects.
