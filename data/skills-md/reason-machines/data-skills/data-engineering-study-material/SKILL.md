---
name: data-engineering-study-material
description: Comprehensive study guide covering data engineering concepts, tools, and best practices for learning and reference
triggers:
  - explain data engineering concepts
  - show me data engineering study materials
  - what are data engineering best practices
  - help me learn data engineering
  - guide me through data engineering topics
  - data engineering interview preparation
  - overview of data engineering tools
  - data engineering learning resources
---

# Data Engineering Study Material

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project is a comprehensive study guide and reference repository for data engineering concepts, tools, and practices. It serves as a centralized resource for learning core data engineering principles, understanding modern data stack components, and preparing for data engineering roles.

The repository covers:
- Data engineering fundamentals and architecture patterns
- ETL/ELT pipeline design and implementation
- Data warehousing and lake architectures
- Streaming and batch processing frameworks
- Cloud data platforms (AWS, GCP, Azure)
- Data quality, governance, and observability
- Infrastructure as Code and orchestration tools
- Interview preparation and best practices

## Installation

This is a study material repository, not an installable package. Clone it to access the materials:

```bash
git clone https://github.com/Ahmeduddin3403/data-engineering-study-material.git
cd data-engineering-study-material
```

## Repository Structure

The materials are typically organized by topic area:

```
data-engineering-study-material/
├── fundamentals/          # Core concepts and principles
├── tools/                 # Tool-specific guides
├── architectures/         # Design patterns and architectures
├── pipelines/             # ETL/ELT examples
├── cloud-platforms/       # Cloud-specific implementations
├── streaming/             # Real-time processing
├── batch-processing/      # Batch job patterns
├── data-quality/          # Testing and validation
├── orchestration/         # Workflow management
├── interview-prep/        # Interview questions and answers
└── projects/              # Hands-on project examples
```

## Core Data Engineering Concepts

### ETL Pipeline Example (Python)

```python
import pandas as pd
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:
    """Simple ETL pipeline for extracting, transforming, and loading data"""
    
    def __init__(self, source_path, target_conn_string):
        self.source_path = source_path
        self.engine = create_engine(target_conn_string)
    
    def extract(self):
        """Extract data from source"""
        logger.info(f"Extracting data from {self.source_path}")
        df = pd.read_csv(self.source_path)
        logger.info(f"Extracted {len(df)} rows")
        return df
    
    def transform(self, df):
        """Transform data: clean, deduplicate, enrich"""
        logger.info("Transforming data")
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna({
            'numeric_column': 0,
            'string_column': 'Unknown'
        })
        
        # Add derived columns
        df['created_date'] = pd.to_datetime(df['timestamp']).dt.date
        
        # Data validation
        df = df[df['amount'] > 0]
        
        logger.info(f"Transformed to {len(df)} rows")
        return df
    
    def load(self, df, table_name):
        """Load data to target database"""
        logger.info(f"Loading data to {table_name}")
        df.to_sql(table_name, self.engine, if_exists='append', index=False)
        logger.info("Load complete")
    
    def run(self, table_name):
        """Execute full ETL pipeline"""
        try:
            df = self.extract()
            df_transformed = self.transform(df)
            self.load(df_transformed, table_name)
            logger.info("ETL pipeline completed successfully")
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            raise

# Usage
if __name__ == "__main__":
    pipeline = ETLPipeline(
        source_path='data/raw/sales.csv',
        target_conn_string='postgresql://user:pass@localhost:5432/warehouse'
    )
    pipeline.run('sales_fact')
```

### Data Quality Checks

```python
import great_expectations as ge

def validate_data_quality(df):
    """Implement data quality checks using Great Expectations"""
    
    # Convert pandas DataFrame to GE DataFrame
    ge_df = ge.from_pandas(df)
    
    # Define expectations
    expectations = {
        'id': lambda col: col.expect_column_values_to_be_unique(),
        'email': lambda col: col.expect_column_values_to_match_regex(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
        'amount': lambda col: col.expect_column_values_to_be_between(min_value=0, max_value=1000000),
        'created_at': lambda col: col.expect_column_values_to_not_be_null(),
        'status': lambda col: col.expect_column_values_to_be_in_set(['active', 'inactive', 'pending'])
    }
    
    # Run validations
    results = []
    for column, expectation_func in expectations.items():
        if column in ge_df.columns:
            result = expectation_func(ge_df[column])
            results.append(result)
    
    # Check if all validations passed
    all_passed = all(r.success for r in results)
    
    return all_passed, results
```

### Apache Airflow DAG Example

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

def extract_from_api(**context):
    """Extract data from external API"""
    import requests
    import json
    
    response = requests.get('https://api.example.com/data')
    data = response.json()
    
    # Save to S3
    s3_path = f"s3://my-bucket/raw/{context['ds']}/data.json"
    # Upload logic here
    
    return s3_path

def transform_data(**context):
    """Transform extracted data"""
    import pandas as pd
    
    # Read from S3
    s3_path = context['ti'].xcom_pull(task_ids='extract_task')
    df = pd.read_json(s3_path)
    
    # Transformations
    df_transformed = df.drop_duplicates()
    df_transformed['load_date'] = context['ds']
    
    # Write back to S3
    output_path = f"s3://my-bucket/processed/{context['ds']}/data.parquet"
    df_transformed.to_parquet(output_path)
    
    return output_path

with DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for data processing',
    schedule_interval='0 2 * * *',  # Run at 2 AM daily
    catchup=False,
    tags=['etl', 'daily']
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_from_api,
        provide_context=True
    )
    
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        provide_context=True
    )
    
    load_task = S3ToRedshiftOperator(
        task_id='load_to_redshift',
        s3_bucket='my-bucket',
        s3_key='processed/{{ ds }}/data.parquet',
        schema='analytics',
        table='fact_table',
        copy_options=['FORMAT AS PARQUET']
    )
    
    data_quality_check = PostgresOperator(
        task_id='quality_check',
        postgres_conn_id='redshift_conn',
        sql="""
            SELECT COUNT(*) as row_count 
            FROM analytics.fact_table 
            WHERE load_date = '{{ ds }}';
        """
    )
    
    extract_task >> transform_task >> load_task >> data_quality_check
```

### Spark Batch Processing Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum, avg, count, to_date
from pyspark.sql.window import Window

def process_batch_data():
    """Process large-scale batch data with Apache Spark"""
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("BatchDataProcessing") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    # Read data from data lake
    df = spark.read \
        .format("parquet") \
        .load("s3a://data-lake/raw/transactions/")
    
    # Transformations
    df_transformed = df \
        .withColumn("transaction_date", to_date(col("timestamp"))) \
        .filter(col("amount") > 0) \
        .dropDuplicates(["transaction_id"])
    
    # Aggregations
    daily_summary = df_transformed.groupBy("transaction_date", "category") \
        .agg(
            count("transaction_id").alias("transaction_count"),
            sum("amount").alias("total_amount"),
            avg("amount").alias("avg_amount")
        )
    
    # Window functions for ranking
    window_spec = Window.partitionBy("transaction_date").orderBy(col("total_amount").desc())
    
    ranked_summary = daily_summary \
        .withColumn("rank", dense_rank().over(window_spec)) \
        .filter(col("rank") <= 10)
    
    # Write to data warehouse
    ranked_summary.write \
        .format("parquet") \
        .mode("overwrite") \
        .partitionBy("transaction_date") \
        .save("s3a://data-warehouse/analytics/daily_summary/")
    
    spark.stop()

if __name__ == "__main__":
    process_batch_data()
```

### Streaming Pipeline Example (Kafka + Spark Structured Streaming)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

def create_streaming_pipeline():
    """Real-time data processing with Spark Structured Streaming"""
    
    spark = SparkSession.builder \
        .appName("RealTimeStreaming") \
        .getOrCreate()
    
    # Define schema for incoming data
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("timestamp", TimestampType(), True)
    ])
    
    # Read from Kafka
    df_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "events") \
        .option("startingOffsets", "latest") \
        .load()
    
    # Parse JSON data
    df_parsed = df_stream.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Windowed aggregations
    df_windowed = df_parsed \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window(col("timestamp"), "5 minutes", "1 minute"),
            col("event_type")
        ) \
        .agg(
            count("event_id").alias("event_count"),
            sum("amount").alias("total_amount")
        )
    
    # Write to sink
    query = df_windowed.writeStream \
        .outputMode("append") \
        .format("parquet") \
        .option("path", "s3a://streaming-output/events/") \
        .option("checkpointLocation", "s3a://checkpoints/events/") \
        .trigger(processingTime="1 minute") \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    create_streaming_pipeline()
```

## Common Patterns

### Incremental Data Loading

```python
def incremental_load(table_name, watermark_column, last_watermark):
    """Load only new/updated records since last run"""
    
    query = f"""
        SELECT *
        FROM {table_name}
        WHERE {watermark_column} > '{last_watermark}'
        ORDER BY {watermark_column}
    """
    
    # Execute query and get new data
    new_data = pd.read_sql(query, source_conn)
    
    if not new_data.empty:
        # Get new watermark
        new_watermark = new_data[watermark_column].max()
        
        # Load to target
        new_data.to_sql('target_table', target_conn, if_exists='append', index=False)
        
        # Update watermark
        save_watermark(table_name, new_watermark)
        
    return len(new_data)
```

### SCD Type 2 Implementation

```python
def scd_type2_merge(source_df, target_table, business_key, effective_date):
    """Implement Slowly Changing Dimension Type 2"""
    
    from datetime import datetime
    
    # Read current dimension table
    current_df = pd.read_sql(f"SELECT * FROM {target_table} WHERE is_current = 1", conn)
    
    # Identify changes
    merged = source_df.merge(
        current_df,
        on=business_key,
        how='left',
        suffixes=('_new', '_old')
    )
    
    # Records that changed
    changed = merged[
        (merged.apply(lambda row: row_has_changes(row), axis=1))
    ]
    
    # Expire old records
    if not changed.empty:
        expire_query = f"""
            UPDATE {target_table}
            SET is_current = 0,
                end_date = '{effective_date}'
            WHERE {business_key} IN ({','.join(map(str, changed[business_key].tolist()))})
            AND is_current = 1
        """
        conn.execute(expire_query)
    
    # Insert new versions
    new_records = source_df[source_df[business_key].isin(changed[business_key])]
    new_records['start_date'] = effective_date
    new_records['end_date'] = '9999-12-31'
    new_records['is_current'] = 1
    
    new_records.to_sql(target_table, conn, if_exists='append', index=False)
```

## Configuration

### Database Connection Configuration

```python
# config.py
import os

DATABASE_CONFIG = {
    'source': {
        'host': os.getenv('SOURCE_DB_HOST'),
        'port': os.getenv('SOURCE_DB_PORT', 5432),
        'database': os.getenv('SOURCE_DB_NAME'),
        'user': os.getenv('SOURCE_DB_USER'),
        'password': os.getenv('SOURCE_DB_PASSWORD')
    },
    'warehouse': {
        'host': os.getenv('WAREHOUSE_HOST'),
        'port': os.getenv('WAREHOUSE_PORT', 5439),
        'database': os.getenv('WAREHOUSE_DB'),
        'user': os.getenv('WAREHOUSE_USER'),
        'password': os.getenv('WAREHOUSE_PASSWORD')
    }
}

SPARK_CONFIG = {
    'spark.executor.memory': '4g',
    'spark.driver.memory': '2g',
    'spark.sql.adaptive.enabled': 'true',
    'spark.sql.adaptive.coalescePartitions.enabled': 'true'
}

AIRFLOW_CONFIG = {
    'concurrency': 16,
    'max_active_runs': 3,
    'dagbag_import_timeout': 30
}
```

## Troubleshooting

### Common Issues and Solutions

**Issue: Out of Memory in Spark Jobs**
```python
# Solution: Optimize memory usage
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.default.parallelism", "200") \
    .getOrCreate()

# Use broadcast joins for small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")
```

**Issue: Slow Incremental Loads**
```python
# Solution: Use partition pruning and indexing
# Add indexes on watermark columns
# Partition target tables by date

# Use partition pruning in Spark
df = spark.read.parquet("s3://data/table/") \
    .where(f"partition_date >= '{start_date}'")
```

**Issue: Data Quality Failures**
```python
# Solution: Implement comprehensive validation
def validate_and_quarantine(df, rules):
    """Separate valid and invalid records"""
    
    valid_df = df
    invalid_records = []
    
    for rule_name, rule_func in rules.items():
        mask = rule_func(valid_df)
        invalid = valid_df[~mask].copy()
        invalid['failed_rule'] = rule_name
        invalid_records.append(invalid)
        valid_df = valid_df[mask]
    
    # Save invalid records for review
    if invalid_records:
        pd.concat(invalid_records).to_sql(
            'data_quality_quarantine',
            conn,
            if_exists='append'
        )
    
    return valid_df
```

## Best Practices

1. **Idempotency**: Ensure pipelines can be re-run safely
2. **Monitoring**: Implement comprehensive logging and alerting
3. **Data Quality**: Validate data at every stage
4. **Partitioning**: Use appropriate partitioning strategies for performance
5. **Documentation**: Document data lineage and transformations
6. **Version Control**: Track schema changes and pipeline versions
7. **Testing**: Test pipelines with sample data before production
8. **Security**: Use IAM roles, encryption, and secure credential management

## Interview Preparation

Common data engineering interview topics covered:
- SQL optimization and query tuning
- Distributed systems concepts
- Data modeling (star schema, snowflake, Data Vault)
- ETL vs ELT trade-offs
- CAP theorem and consistency models
- Data quality frameworks
- Cloud platform services (S3, Redshift, BigQuery, Databricks)
- Orchestration tools (Airflow, Prefect, Dagster)
- Streaming architectures (Kafka, Kinesis, Pub/Sub)
