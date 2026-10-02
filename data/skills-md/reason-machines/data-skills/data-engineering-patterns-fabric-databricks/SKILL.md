---
name: data-engineering-patterns-fabric-databricks
description: 600+ patterns and concepts for Azure Databricks, Microsoft Fabric, and PySpark data engineering - covering lakehouse architecture, Delta Lake, pipelines, and production best practices.
triggers:
  - show me data engineering patterns for Fabric
  - how do I implement Delta Lake best practices
  - what are the Azure Databricks cluster optimization patterns
  - help me with PySpark transformation patterns
  - show me lakehouse architecture patterns
  - what are the Microsoft Fabric pipeline patterns
  - help with Unity Catalog governance patterns
  - show me production data engineering best practices
---

# Data Engineering Patterns - Fabric & Databricks

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill provides access to 600+ field-tested data engineering patterns for Microsoft Fabric, Azure Databricks, and PySpark. These patterns cover everything from pipeline design and Delta Lake optimization to Unity Catalog governance and cost architecture.

## What This Project Provides

A comprehensive collection of patterns organized into 12 books covering:

**Microsoft Fabric (250 patterns):**
- Pipelines and Data Factory
- Lakehouse and PySpark
- Warehouse and SQL
- Power BI in Fabric
- Architecture Patterns

**Azure Databricks (350 patterns):**
- Clusters and Compute
- Delta Lake
- Workflows and Orchestration
- Structured Streaming and Auto Loader
- Unity Catalog
- Databricks SQL and Photon
- Platform and Cost Architecture

**PySpark:**
- 88 concepts for production Spark across both platforms

## Installation

Clone the repository to access all pattern PDFs:

```bash
git clone https://github.com/ssanjaychandra123/data-engineering-patterns.git
cd data-engineering-patterns
```

## Repository Structure

```
data-engineering-patterns/
├── Fabric Patterns/
│   ├── Fabric Engineering Patterns Book I - Pipelines and Data Factory.pdf
│   ├── Fabric Engineering Patterns Book II - Lakehouse and PySpark.pdf
│   ├── Fabric Engineering Patterns Book III - Warehouse and SQL.pdf
│   ├── Fabric Engineering Patterns Book IV - Power BI in Fabric.pdf
│   └── Fabric Engineering Patterns Book V - Architecture Patterns.pdf
├── Databricks Patterns/
│   ├── Azure Databricks Engineering Patterns Book I - Clusters and Compute.pdf
│   ├── Azure Databricks Engineering Patterns Book II - Delta Lake.pdf
│   ├── Azure Databricks Engineering Patterns Book III - Workflows and Orchestration.pdf
│   ├── Azure Databricks Engineering Patterns Book IV - Structured Streaming and Auto Loader.pdf
│   ├── Azure Databricks Engineering Patterns Book V - Unity Catalog.pdf
│   ├── Azure Databricks Engineering Patterns Book VI - Databricks SQL and Photon.pdf
│   └── Azure Databricks Engineering Patterns Book VII - Platform and Cost Architecture.pdf
└── PySpark/
    └── The PySpark Handbook for Fabric and Databricks.pdf
```

## Key Pattern Categories

### Microsoft Fabric Patterns

#### Pipeline and Data Factory Patterns

Common patterns include:
- Incremental data loading strategies
- Pipeline retry and error handling
- Parameter-driven pipeline design
- Activity dependencies and control flow
- Copy activity optimization
- Metadata-driven frameworks

Example incremental load pattern in Fabric Pipeline:

```python
# Notebook activity in Fabric pipeline
from datetime import datetime, timedelta

# Get pipeline parameters
watermark = spark.conf.get("pipeline.watermark")
table_name = spark.conf.get("pipeline.tableName")

# Read incremental data
df = spark.read.format("delta") \
    .load(f"abfss://source@storage.dfs.core.windows.net/{table_name}") \
    .filter(f"modified_date > '{watermark}'")

# Write to target
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(f"Tables/{table_name}")

# Return new watermark
new_watermark = df.agg({"modified_date": "max"}).collect()[0][0]
mssparkutils.notebook.exit(str(new_watermark))
```

#### Lakehouse and PySpark Patterns

Key patterns for Fabric Lakehouse:

```python
# Pattern: Upsert (merge) operation in Fabric Lakehouse
from delta.tables import DeltaTable

# Source data
updates_df = spark.read.format("parquet").load("Files/updates/")

# Target Delta table
target_table = DeltaTable.forPath(spark, "Tables/customers")

# Merge logic
target_table.alias("target").merge(
    updates_df.alias("updates"),
    "target.customer_id = updates.customer_id"
).whenMatchedUpdate(set={
    "name": "updates.name",
    "email": "updates.email",
    "updated_at": "updates.updated_at"
}).whenNotMatchedInsert(values={
    "customer_id": "updates.customer_id",
    "name": "updates.name",
    "email": "updates.email",
    "created_at": "updates.created_at",
    "updated_at": "updates.updated_at"
}).execute()
```

Pattern: Optimize Delta tables in Fabric:

```python
# Optimize with Z-ordering for common query patterns
spark.sql(f"""
    OPTIMIZE lakehouse.customers
    ZORDER BY (customer_id, signup_date)
""")

# Vacuum old files (default 7 days retention)
spark.sql(f"""
    VACUUM lakehouse.customers RETAIN 168 HOURS
""")
```

#### Warehouse and SQL Patterns

Pattern: Create warehouse tables with proper partitioning:

```sql
-- Create partitioned warehouse table in Fabric
CREATE TABLE dw.fact_sales (
    sale_id BIGINT,
    customer_id BIGINT,
    product_id BIGINT,
    sale_amount DECIMAL(18,2),
    sale_date DATE,
    created_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (sale_date);

-- Insert with partition optimization
INSERT INTO dw.fact_sales
SELECT 
    sale_id,
    customer_id,
    product_id,
    sale_amount,
    CAST(sale_date AS DATE) as sale_date,
    created_at
FROM staging.sales
WHERE sale_date >= CURRENT_DATE - INTERVAL 7 DAYS;
```

### Azure Databricks Patterns

#### Cluster and Compute Patterns

Pattern: Configure autoscaling cluster for cost optimization:

```python
# Databricks cluster configuration (JSON)
{
  "cluster_name": "production-etl",
  "spark_version": "13.3.x-scala2.12",
  "node_type_id": "Standard_DS3_v2",
  "autoscale": {
    "min_workers": 2,
    "max_workers": 8
  },
  "autotermination_minutes": 30,
  "spark_conf": {
    "spark.databricks.delta.preview.enabled": "true",
    "spark.databricks.delta.properties.defaults.autoOptimize.optimizeWrite": "true",
    "spark.databricks.delta.properties.defaults.autoOptimize.autoCompact": "true"
  },
  "aws_attributes": {
    "availability": "SPOT_WITH_FALLBACK",
    "spot_bid_price_percent": 100
  }
}
```

#### Delta Lake Patterns

Pattern: Time travel and versioning:

```python
# Read historical version of Delta table
df_version_10 = spark.read.format("delta") \
    .option("versionAsOf", 10) \
    .load("/mnt/delta/customers")

# Read table as of timestamp
df_yesterday = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-15 00:00:00") \
    .load("/mnt/delta/customers")

# Describe history
history_df = spark.sql("DESCRIBE HISTORY delta.`/mnt/delta/customers`")
history_df.select("version", "timestamp", "operation", "operationMetrics").show()
```

Pattern: Change Data Feed (CDF) for incremental processing:

```python
# Enable CDF on table
spark.sql("""
    ALTER TABLE delta.customers 
    SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Read changes between versions
changes_df = spark.read.format("delta") \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 10) \
    .option("endingVersion", 20) \
    .table("delta.customers")

# Process different change types
inserts = changes_df.filter("_change_type = 'insert'")
updates = changes_df.filter("_change_type = 'update_postimage'")
deletes = changes_df.filter("_change_type = 'delete'")
```

#### Structured Streaming Patterns

Pattern: Auto Loader with schema evolution:

```python
# Auto Loader with schema inference and evolution
checkpoint_path = "/mnt/checkpoints/raw_files"
target_path = "/mnt/delta/bronze/raw_data"

df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", checkpoint_path + "/schema") \
    .option("cloudFiles.inferColumnTypes", "true") \
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
    .load("/mnt/landing/raw_files/")

# Write to Delta with checkpointing
query = df.writeStream \
    .format("delta") \
    .option("checkpointLocation", checkpoint_path) \
    .option("mergeSchema", "true") \
    .trigger(availableNow=True) \
    .start(target_path)

query.awaitTermination()
```

Pattern: Streaming aggregations with watermarking:

```python
from pyspark.sql.functions import window, col

# Read streaming data
stream_df = spark.readStream.format("delta") \
    .table("events")

# Windowed aggregation with watermark
aggregated = stream_df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("user_id")
    ) \
    .agg({
        "event_id": "count",
        "amount": "sum"
    })

# Write to Delta table
query = aggregated.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/checkpoints/aggregations") \
    .toTable("event_aggregations")
```

#### Unity Catalog Patterns

Pattern: Create governed table with row-level security:

```python
# Create schema with Unity Catalog
spark.sql("""
    CREATE SCHEMA IF NOT EXISTS main.finance
    COMMENT 'Finance department data'
    LOCATION 'abfss://data@storage.dfs.core.windows.net/finance'
""")

# Create managed table
spark.sql("""
    CREATE TABLE IF NOT EXISTS main.finance.transactions (
        transaction_id BIGINT,
        account_id BIGINT,
        amount DECIMAL(18,2),
        region STRING,
        transaction_date DATE
    )
    USING DELTA
    TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true')
""")

# Apply row filter for data access control
spark.sql("""
    CREATE FUNCTION main.finance.region_filter(region STRING)
    RETURN IF(
        IS_MEMBER('data_engineers'), 
        TRUE, 
        region = current_user()
    )
""")

spark.sql("""
    ALTER TABLE main.finance.transactions 
    SET ROW FILTER main.finance.region_filter ON (region)
""")
```

Pattern: Column masking with Unity Catalog:

```python
# Create masking function
spark.sql("""
    CREATE FUNCTION main.finance.mask_ssn(ssn STRING)
    RETURN CASE 
        WHEN IS_MEMBER('finance_managers') THEN ssn
        ELSE CONCAT('XXX-XX-', RIGHT(ssn, 4))
    END
""")

# Apply column mask
spark.sql("""
    ALTER TABLE main.finance.customers 
    ALTER COLUMN ssn 
    SET MASK main.finance.mask_ssn
""")
```

#### Workflows and Orchestration Patterns

Pattern: Create parameterized Databricks job:

```python
# In notebook: Get job parameters
dbutils.widgets.text("date", "")
dbutils.widgets.text("environment", "prod")

processing_date = dbutils.widgets.get("date")
env = dbutils.widgets.get("environment")

# Use parameters in processing
df = spark.read.format("delta") \
    .load(f"/mnt/{env}/data") \
    .filter(f"date = '{processing_date}'")

# Process and write results
result_df = df.groupBy("category").count()
result_df.write.format("delta").mode("overwrite") \
    .save(f"/mnt/{env}/results/{processing_date}")

# Return status for orchestration
dbutils.notebook.exit(f"Processed {result_df.count()} records")
```

Pattern: Job definition with retry logic:

```json
{
  "name": "daily-etl-pipeline",
  "tasks": [
    {
      "task_key": "extract",
      "notebook_task": {
        "notebook_path": "/Workflows/extract",
        "base_parameters": {
          "date": "{{job.start_time.date}}",
          "environment": "prod"
        }
      },
      "existing_cluster_id": "{{cluster_id}}",
      "max_retries": 2,
      "timeout_seconds": 3600
    },
    {
      "task_key": "transform",
      "depends_on": [{"task_key": "extract"}],
      "notebook_task": {
        "notebook_path": "/Workflows/transform",
        "base_parameters": {
          "date": "{{job.start_time.date}}"
        }
      },
      "existing_cluster_id": "{{cluster_id}}",
      "max_retries": 1
    },
    {
      "task_key": "load",
      "depends_on": [{"task_key": "transform"}],
      "notebook_task": {
        "notebook_path": "/Workflows/load"
      },
      "existing_cluster_id": "{{cluster_id}}"
    }
  ],
  "schedule": {
    "quartz_cron_expression": "0 0 2 * * ?",
    "timezone_id": "UTC"
  }
}
```

### PySpark Production Patterns

#### Broadcast Join Pattern

```python
from pyspark.sql.functions import broadcast

# Small dimension table (< 10GB)
dim_products = spark.table("dim.products")

# Large fact table
fact_sales = spark.table("fact.sales")

# Use broadcast join to avoid shuffle
result = fact_sales.join(
    broadcast(dim_products),
    fact_sales.product_id == dim_products.product_id,
    "left"
)
```

#### Partitioning and Bucketing Pattern

```python
# Write with optimal partitioning
df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .option("maxRecordsPerFile", 1000000) \
    .save("/mnt/delta/partitioned_data")

# Create bucketed table for join optimization
df.write.format("delta") \
    .mode("overwrite") \
    .bucketBy(100, "customer_id") \
    .sortBy("transaction_date") \
    .saveAsTable("bucketed_transactions")
```

#### Error Handling Pattern

```python
from pyspark.sql.functions import col, when, lit
from pyspark.sql.utils import AnalysisException

try:
    # Attempt to read data with schema enforcement
    df = spark.read.format("delta") \
        .option("enforceSchema", "true") \
        .load("/mnt/delta/source")
    
    # Data quality checks
    valid_df = df.filter(col("amount") > 0) \
        .filter(col("customer_id").isNotNull())
    
    invalid_df = df.filter(
        (col("amount") <= 0) | 
        (col("customer_id").isNull())
    ).withColumn("error_reason", 
        when(col("amount") <= 0, lit("Invalid amount"))
        .when(col("customer_id").isNull(), lit("Missing customer_id"))
    )
    
    # Write valid records
    valid_df.write.format("delta").mode("append") \
        .save("/mnt/delta/target")
    
    # Write invalid records to quarantine
    if invalid_df.count() > 0:
        invalid_df.write.format("delta").mode("append") \
            .save("/mnt/delta/quarantine")
        
except AnalysisException as e:
    print(f"Schema mismatch: {str(e)}")
    # Handle schema evolution
    df = spark.read.format("delta") \
        .option("mergeSchema", "true") \
        .load("/mnt/delta/source")
```

#### Performance Optimization Pattern

```python
from pyspark.sql.functions import col, current_timestamp

# Cache frequently accessed data
df_cached = spark.table("dimension.products") \
    .filter(col("is_active") == True) \
    .cache()

# Use persist for complex operations
from pyspark.storagelevel import StorageLevel
df_persisted = large_df.repartition(200, "partition_key") \
    .persist(StorageLevel.MEMORY_AND_DISK)

# Adaptive Query Execution settings
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Dynamic partition pruning
spark.conf.set("spark.sql.optimizer.dynamicPartitionPruning.enabled", "true")
```

## Common Use Cases

### Medallion Architecture Pattern

```python
# Bronze layer: Raw data ingestion
bronze_df = spark.read.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .load("/mnt/landing/") \
    .withColumn("ingestion_time", current_timestamp())

bronze_df.write.format("delta") \
    .mode("append") \
    .save("/mnt/delta/bronze/raw_events")

# Silver layer: Cleaned and conformed
from pyspark.sql.functions import col, to_timestamp

silver_df = spark.read.format("delta") \
    .load("/mnt/delta/bronze/raw_events") \
    .filter(col("event_type").isNotNull()) \
    .withColumn("event_timestamp", to_timestamp("timestamp")) \
    .dropDuplicates(["event_id"]) \
    .select("event_id", "event_type", "user_id", "event_timestamp", "properties")

silver_df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/mnt/delta/silver/events")

# Gold layer: Business aggregates
gold_df = spark.read.format("delta") \
    .load("/mnt/delta/silver/events") \
    .groupBy("user_id", "event_type") \
    .agg({
        "event_id": "count",
        "event_timestamp": "max"
    })

gold_df.write.format("delta") \
    .mode("overwrite") \
    .save("/mnt/delta/gold/user_event_summary")
```

### SCD Type 2 Pattern

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import col, current_timestamp, lit

# Source changes
source_df = spark.read.format("parquet").load("/mnt/staging/customers")

# Target dimension
target_table = DeltaTable.forPath(spark, "/mnt/delta/dim_customers")

# Identify changed records
changes = source_df.alias("source") \
    .join(
        target_table.toDF().filter("is_current = true").alias("target"),
        "customer_id",
        "left"
    ) \
    .filter(
        col("target.customer_id").isNull() |  # New records
        (col("source.name") != col("target.name")) |  # Changed records
        (col("source.email") != col("target.email"))
    )

# Expire old records
target_table.alias("target").merge(
    changes.alias("changes"),
    "target.customer_id = changes.customer_id AND target.is_current = true"
).whenMatchedUpdate(set={
    "is_current": lit(False),
    "end_date": current_timestamp()
}).execute()

# Insert new versions
new_records = changes.select(
    col("customer_id"),
    col("name"),
    col("email"),
    current_timestamp().alias("start_date"),
    lit(None).alias("end_date"),
    lit(True).alias("is_current")
)

new_records.write.format("delta").mode("append") \
    .save("/mnt/delta/dim_customers")
```

## Configuration Best Practices

### Fabric Configuration

```python
# Set Fabric notebook session configuration
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")

# Access Fabric environment variables
from notebookutils import mssparkutils

# Get secrets from Key Vault
storage_key = mssparkutils.credentials.getSecret(
    "https://keyvault.vault.azure.net/",
    "storage-account-key"
)

# Access workspace identity
workspace_id = mssparkutils.env.getWorkspaceId()
```

### Databricks Configuration

```python
# Access Databricks secrets
storage_account_key = dbutils.secrets.get(
    scope="azure-key-vault",
    key="storage-account-key"
)

# Mount storage with managed identity
dbutils.fs.mount(
    source=f"abfss://data@{storage_account}.dfs.core.windows.net/",
    mount_point="/mnt/data",
    extra_configs={
        "fs.azure.account.auth.type": "OAuth",
        "fs.azure.account.oauth.provider.type": 
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        "fs.azure.account.oauth2.client.id": dbutils.secrets.get("azure-sp", "client-id"),
        "fs.azure.account.oauth2.client.secret": storage_account_key,
        "fs.azure.account.oauth2.client.endpoint": 
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    }
)

# Optimize cluster for specific workload
spark.conf.set("spark.sql.shuffle.partitions", "200")
spark.conf.set("spark.sql.files.maxPartitionBytes", "134217728")  # 128 MB
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
```

## Troubleshooting

### Performance Issues

**Problem:** Slow joins causing job timeouts

```python
# Check partition distribution
df.rdd.getNumPartitions()  # Should be 200-2000 for most workloads

# Identify data skew
df.groupBy("partition_key").count().orderBy(col("count").desc()).show()

# Solution: Repartition with salt for skewed keys
from pyspark.sql.functions import rand, concat

df_balanced = df.withColumn("salt", (rand() * 10).cast("int")) \
    .withColumn("salted_key", concat(col("partition_key"), lit("_"), col("salt"))) \
    .repartition(200, "salted_key")
```

**Problem:** Small file problem in Delta tables

```python
# Check file sizes
spark.sql("DESCRIBE DETAIL delta.`/mnt/delta/table`").select("numFiles", "sizeInBytes").show()

# Solution: Compact small files
spark.sql("OPTIMIZE delta.`/mnt/delta/table`")

# For partitioned tables
spark.sql("OPTIMIZE delta.`/mnt/delta/table` WHERE date >= '2024-01-01'")
```

### Schema Evolution Issues

**Problem:** Schema mismatch errors when appending data

```python
# Enable automatic schema merging
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/mnt/delta/table")

# Or allow schema overwrite
df.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("/mnt/delta/table")

# Check current schema
spark.read.format("delta").load("/mnt/delta/table").printSchema()
```

### Memory Issues

**Problem:** Out of memory errors during processing

```python
# Solution 1: Increase partition count to reduce partition size
df_repartitioned = df.repartition(400)

# Solution 2: Use iterative processing for large aggregations
from pyspark.sql.window import Window

window_spec = Window.partitionBy("category").orderBy("date")
df_windowed = df.withColumn("row_num", row_number().over(window_spec))

# Solution 3: Spill to disk instead of memory
spark.conf.set("spark.memory.fraction", "0.6")
spark.conf.set("spark.memory.storageFraction", "0.3")
```

### Streaming Issues

**Problem:** Checkpoint directory conflicts

```python
# Always use unique checkpoint locations per stream
checkpoint_base = "/mnt/checkpoints"
stream_id = "user_events_stream"

query = df.writeStream \
    .format("delta") \
    .option("checkpointLocation", f"{checkpoint_base}/{stream_id}") \
    .start("/mnt/delta/target")

# To restart stream from beginning, delete checkpoint
# dbutils.fs.rm(f"{checkpoint_base}/{stream_id}", True)
```

**Problem:** Watermark not advancing

```python
# Ensure event time column is properly formatted
from pyspark.sql.functions import to_timestamp

df_with_timestamp = df.withColumn(
    "event_time",
    to_timestamp(col("timestamp_string"), "yyyy-MM-dd HH:mm:ss")
)

# Set appropriate watermark delay
stream_df = df_with_timestamp.withWatermark("event_time", "30 minutes")
```

## Cost Optimization Patterns

### Databricks Cost Optimization

```python
# Use cluster pools for faster startup
cluster_config = {
    "instance_pool_id": "pool-abc123",
    "autotermination_minutes": 15,
    "autoscale": {
        "min_workers": 1,
        "max_workers": 10
    }
}

# Use spot instances for non-critical workloads
aws_attributes = {
    "availability": "SPOT_WITH_FALLBACK",
    "zone_id": "us-west-2a",
    "spot_bid_price_percent": 100
}

# Optimize table for reduced storage and faster queries
spark.sql("""
    OPTIMIZE prod.sales_transactions
    ZORDER BY (customer_id, transaction_date)
""")

# Remove old versions to reduce storage costs
spark.sql("VACUUM prod.sales_transactions RETAIN 168 HOURS")
```

### Fabric Cost Optimization

```python
# Use on-demand capacity for variable workloads
# Set idle timeout for capacity auto-pause

# Optimize pipeline runs
# - Use copy activity instead of foreach + copy for bulk operations
# - Batch small files before processing
# - Use incremental loads instead of full refreshes

# Compress data at rest
df.write.format("delta") \
    .option("compression", "zstd") \
    .mode("overwrite") \
    .save("Tables/compressed_data")
```

## Resources

- **Pattern PDFs:** All 12 books are available in the repository under `Fabric Patterns/`, `Databricks Patterns/`, and `PySpark/`
- **Microsoft Fabric Documentation:** https://learn.microsoft.com/fabric/
- **Azure Databricks Documentation:** https://learn.microsoft.com/azure/databricks/
- **Delta Lake Documentation:** https://docs.delta.io/
- **PySpark API Reference:** https://spark.apache.org/docs/latest/api/python/

## Author

Sanjay Chandra - Enterprise data platform architect and advisor
- LinkedIn: https://www.linkedin.com/in/ssanjaychandra/
- Website: http://www.ssanjaychandra.com

---

*These patterns are compiled from real production implementations across Microsoft Fabric and Azure Databricks platforms. The material is continuously updated as platforms evolve.*
