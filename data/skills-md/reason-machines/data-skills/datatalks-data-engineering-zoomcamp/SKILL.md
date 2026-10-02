---
name: datatalks-data-engineering-zoomcamp
description: Free 9-week data engineering course covering Docker, Terraform, Kestra, BigQuery, dbt, Spark, and Kafka with hands-on projects
triggers:
  - "help me with the data engineering zoomcamp"
  - "how do I set up the DE zoomcamp environment"
  - "show me how to complete zoomcamp homework"
  - "what are the data engineering zoomcamp modules"
  - "help with zoomcamp docker setup"
  - "configure terraform for zoomcamp GCP"
  - "run zoomcamp spark exercises"
  - "complete data engineering course project"
---

# DataTalks Data Engineering Zoomcamp

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

The Data Engineering Zoomcamp is a comprehensive 9-week free course covering production-ready data pipeline development. It includes hands-on modules on containerization (Docker), infrastructure as code (Terraform), workflow orchestration (Kestra), data warehousing (BigQuery), analytics engineering (dbt), data platforms (Bruin), batch processing (Spark), and streaming (Kafka).

The course operates in cohorts (next starts January 2026) but all materials are available for self-paced learning.

## Prerequisites

- Basic coding experience
- SQL familiarity
- Python knowledge (helpful but not required)
- Git installed
- Docker Desktop or Docker Engine
- Google Cloud Platform (GCP) account (free tier)

## Course Structure

### Module 1: Docker & Terraform

**Set up containerized PostgreSQL database:**

```bash
# Create network
docker network create pg-network

# Run PostgreSQL
docker run -d \
  --name pg-database \
  --network pg-network \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=ny_taxi \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

# Run pgAdmin
docker run -d \
  --name pgadmin \
  --network pg-network \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=root \
  -p 8080:80 \
  dpage/pgadmin4
```

**Docker Compose for entire stack:**

```yaml
# docker-compose.yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - ./ny_taxi_postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
```

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down
```

**Terraform GCP setup:**

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

# Data Lake Bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}"
  location      = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }

  force_destroy = true
}

# BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}
```

```hcl
# variables.tf
locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources"
  default     = "europe-west6"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset"
  type        = string
  default     = "trips_data_all"
}
```

```bash
# Initialize Terraform
terraform init

# Plan infrastructure
terraform plan

# Apply infrastructure
terraform apply

# Destroy infrastructure
terraform destroy
```

### Module 2: Workflow Orchestration (Kestra)

**Example Kestra workflow for data ingestion:**

```yaml
# flows/ingest_data.yaml
id: ingest_ny_taxi_data
namespace: zoomcamp

tasks:
  - id: download_data
    type: io.kestra.core.tasks.scripts.Bash
    commands:
      - wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
      - gunzip yellow_tripdata_2021-01.csv.gz

  - id: python_ingest
    type: io.kestra.plugin.scripts.python.Script
    docker:
      image: python:3.9
    script: |
      import pandas as pd
      from sqlalchemy import create_engine
      import os
      
      df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100000)
      
      engine = create_engine(os.getenv('POSTGRES_CONNECTION'))
      df.to_sql('yellow_taxi_data', engine, if_exists='replace', chunksize=10000)
      
      print(f"Inserted {len(df)} rows")

  - id: log_completion
    type: io.kestra.core.tasks.log.Log
    message: "Data ingestion completed successfully"
```

**Python data ingestion script:**

```python
# ingest_data.py
import pandas as pd
from sqlalchemy import create_engine
import argparse
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # Download CSV
    csv_name = 'output.csv'
    os.system(f"wget {url} -O {csv_name}")
    
    # Create engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Read CSV in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    
    df = next(df_iter)
    
    # Convert datetime columns
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    # Create table
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    
    # Insert first chunk
    df.to_sql(name=table_name, con=engine, if_exists='append')
    
    # Insert remaining chunks
    while True:
        try:
            t_start = time()
            df = next(df_iter)
            
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            print(f'Inserted another chunk, took %.3f seconds' % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table')
    parser.add_argument('--url', required=True, help='url of the csv file')
    
    args = parser.parse_args()
    
    main(args)
```

```bash
# Run ingestion script
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

### Module 3: Data Warehouse (BigQuery)

**Create partitioned and clustered table:**

```sql
-- Create external table
CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 
          'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
);

-- Create partitioned table
CREATE OR REPLACE TABLE `trips_data_all.yellow_tripdata_partitioned`
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM `trips_data_all.external_yellow_tripdata`;

-- Create partitioned and clustered table
CREATE OR REPLACE TABLE `trips_data_all.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `trips_data_all.external_yellow_tripdata`;

-- Query comparison
SELECT DISTINCT(VendorID)
FROM `trips_data_all.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2020-06-01' AND '2020-06-30';
-- This query will process less data vs non-partitioned
```

**Load data from GCS to BigQuery:**

```python
# load_to_bq.py
from google.cloud import bigquery
import os

# Set credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

# Initialize client
client = bigquery.Client()

# Define table
table_id = 'your-project.trips_data_all.yellow_tripdata'

# Configure load job
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

uri = 'gs://your-bucket/yellow_tripdata_2021-01.parquet'

# Load data
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)

load_job.result()  # Wait for job to complete

print(f"Loaded {load_job.output_rows} rows to {table_id}")
```

### Module 4: Analytics Engineering (dbt)

**Project structure:**

```
dbt_project/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/
│   │   ├── stg_yellow_tripdata.sql
│   │   └── schema.yml
│   └── core/
│       ├── fact_trips.sql
│       └── dim_zones.sql
└── macros/
    └── get_payment_type_description.sql
```

**dbt_project.yml:**

```yaml
name: 'taxi_rides_ny'
version: '1.0.0'
config-version: 2

profile: 'default'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  taxi_rides_ny:
    staging:
      +materialized: view
    core:
      +materialized: table
```

**profiles.yml:**

```yaml
default:
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: "{{ env_var('GCP_PROJECT_ID') }}"
      dataset: dbt_dev
      threads: 4
      keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}"
      location: EU
      
    prod:
      type: bigquery
      method: service-account
      project: "{{ env_var('GCP_PROJECT_ID') }}"
      dataset: production
      threads: 4
      keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}"
      location: EU
      
  target: dev
```

**Staging model (models/staging/stg_yellow_tripdata.sql):**

```sql
{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, tpep_pickup_datetime) as rn
  from {{ source('staging','yellow_tripdata') }}
  where vendorid is not null 
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'tpep_pickup_datetime']) }} as tripid,
    cast(vendorid as integer) as vendorid,
    cast(ratecodeid as integer) as ratecodeid,
    cast(pulocationid as integer) as pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,
    
    -- timestamps
    cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    store_and_fwd_flag,
    cast(passenger_count as integer) as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    
    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    cast(payment_type as integer) as payment_type,
    {{ get_payment_type_description('payment_type') }} as payment_type_description
from tripdata
where rn = 1
```

**Core model (models/core/fact_trips.sql):**

```sql
{{ config(materialized='table') }}

with green_data as (
    select *, 
        'Green' as service_type 
    from {{ ref('stg_green_tripdata') }}
), 

yellow_data as (
    select *, 
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
), 

trips_unioned as (
    select * from green_data
    union all
    select * from yellow_data
), 

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select 
    trips_unioned.tripid, 
    trips_unioned.vendorid, 
    trips_unioned.service_type,
    trips_unioned.ratecodeid, 
    trips_unioned.pickup_locationid, 
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    trips_unioned.dropoff_locationid,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    trips_unioned.pickup_datetime, 
    trips_unioned.dropoff_datetime, 
    trips_unioned.store_and_fwd_flag, 
    trips_unioned.passenger_count, 
    trips_unioned.trip_distance, 
    trips_unioned.fare_amount, 
    trips_unioned.extra, 
    trips_unioned.mta_tax, 
    trips_unioned.tip_amount, 
    trips_unioned.tolls_amount, 
    trips_unioned.total_amount, 
    trips_unioned.payment_type, 
    trips_unioned.payment_type_description
from trips_unioned
inner join dim_zones as pickup_zone
on trips_unioned.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on trips_unioned.dropoff_locationid = dropoff_zone.locationid
```

**Macro (macros/get_payment_type_description.sql):**

```sql
{#
    This macro returns the description of the payment_type 
#}

{% macro get_payment_type_description(payment_type) -%}

    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end

{%- endmacro %}
```

**Schema and tests (models/staging/schema.yml):**

```yaml
version: 2

sources:
  - name: staging
    database: "{{ env_var('GCP_PROJECT_ID') }}"
    schema: trips_data_all

    tables:
      - name: yellow_tripdata
      - name: green_tripdata

models:
  - name: stg_yellow_tripdata
    description: >
      Trip made by yellow taxis.
    columns:
      - name: tripid
        description: Primary key for this table, generated with a concatenation of vendorid+pickup_datetime
        tests:
          - unique:
              severity: warn
          - not_null:
              severity: warn
      - name: vendorid
        description: >
          A code indicating the TPEP provider that provided the record.
        tests:
          - accepted_values:
              values: [1, 2]
      - name: pickup_datetime
        description: The date and time when the meter was engaged.
        tests:
          - not_null:
              severity: warn
      - name: passenger_count
        description: The number of passengers in the vehicle.
        tests:
          - accepted_values:
              values: [1, 2, 3, 4, 5, 6]
              severity: warn
```

**dbt commands:**

```bash
# Install dependencies
dbt deps

# Run models
dbt run

# Run specific model
dbt run --select stg_yellow_tripdata

# Test models
dbt test

# Generate documentation
dbt docs generate

# Serve documentation
dbt docs serve

# Run models and tests
dbt build

# Run with specific target
dbt run --target prod
```

### Module 6: Batch Processing (Spark)

**PySpark setup:**

```python
# Download Spark
wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar xzfv spark-3.3.2-bin-hadoop3.tgz
rm spark-3.3.2-bin-hadoop3.tgz

# Set environment variables
export SPARK_HOME="${HOME}/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```

**PySpark script for data processing:**

```python
# spark_processing.py
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F

# Create Spark session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

# Define schema
schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True),
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True),
    types.StructField('DOLocationID', types.IntegerType(), True),
    types.StructField('SR_Flag', types.StringType(), True)
])

# Read CSV
df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-01.csv')

# Show schema
df.printSchema()

# Repartition and save as parquet
df.repartition(24) \
    .write.parquet('fhvhv/2021/01/', mode='overwrite')

# Read parquet
df = spark.read.parquet('fhvhv/2021/01/')

# SQL transformations
df.registerTempTable('fhvhv_2021_01')

spark.sql("""
SELECT 
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month,
    COUNT(1) AS number_of_trips
FROM 
    fhvhv_2021_01
WHERE 
    hvfhs_license_num = 'HV0003'
GROUP BY 
    1, 2
ORDER BY 
    1, 2
""").show()

# DataFrame API
df_result = df \
    .withColumn('revenue_month', F.date_trunc('month', 'pickup_datetime')) \
    .filter(F.col('hvfhs_license_num') == 'HV0003') \
    .groupBy('PULocationID', 'revenue_month') \
    .agg(F.count('*').alias('number_of_trips')) \
    .orderBy('PULocationID', 'revenue_month')

df_result.show()

# Write results
df_result.coalesce(1).write.parquet('tmp/revenue-zones', mode='overwrite')
```

**Spark with Google Cloud Storage:**

```python
import pyspark
from pyspark.sql import SparkSession

# Configure Spark for GCS
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar") \
    .getOrCreate()

spark._jsc.hadoopConfiguration().set("google.cloud.auth.service.account.json.keyfile", 
                                      "path/to/credentials.json")

# Read from GCS
df_green = spark.read.parquet('gs://your-bucket/pq/green/*/*')

# Write to BigQuery
df_green.write.format('bigquery') \
    .option('table', 'trips_data_all.green_tripdata') \
    .option('temporaryGcsBucket', 'your-temp-bucket') \
    .mode('overwrite') \
    .save()
```

### Module 7: Streaming (Kafka)

**Docker Compose for Kafka:**

```yaml
# docker-compose-kafka.yml
version: '3.6'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.2.0
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  broker:
    image: confluentinc/cp-kafka:7.2.0
    hostname: broker
    container_name: broker
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "9101:9101"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_SCHEMA_REGISTRY_URL: http://schema-registry:8081

  schema-registry:
    image: confluentinc/cp-schema-registry:7.2.0
    hostname: schema-registry
    container_name: schema-registry
    depends_on:
      - broker
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: 'broker:29092'

  control-center:
    image: confluentinc/cp-enterprise-control-center:7.2.0
    hostname: control-center
    container_name: control-center
    depends_on:
      - broker
      - schema-registry
    ports:
      - "9021:9021"
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: 'broker:29092'
      CONTROL_CENTER_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      CONTROL_CENTER_REPLICATION_FACTOR: 1
      PORT: 9021
```

```bash
# Start Kafka
docker-compose -f docker-compose-kafka.yml up -d
```

**Python Kafka producer:**

```python
# producer.py
from kafka import KafkaProducer
import json
import time
from datetime import datetime

# Create producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send messages
for i in range(100):
    message = {
        'trip_id': i,
        'vendor_id': 1,
        'pickup_datetime': datetime.now().isoformat(),
        'passenger_count': 1,
        'trip_distance': 5.2
    }
    
    producer.send('rides', value=message)
    print(f"Sent message {i}")
    time.sleep(1)

producer.flush()
```

**Python Kafka consumer:**

```python
# consumer.py
from kafka import KafkaConsumer
import json

# Create consumer
consumer = KafkaConsumer(
    'rides',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages
for message in consumer:
    print(f"Received: {message.value}")
    
    # Process message
    trip_id = message.value['trip_id']
    trip_distance = message.value['trip_distance']
    print(f"Trip {trip_id}: {trip_distance} miles")
```

**Kafka Streams example:**

```python
# streams_processing.py
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import json

# Create topics
admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

topic_list = [
    NewTopic(name="rides", num_partitions=2, replication_factor=1),
    NewTopic(name="rides-pulocationid", num_partitions=2, replication_factor=1)
]

try:
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
except Exception as e:
    print(f"Topics might already exist: {e}")

# Stream processing (aggregation)
from collections import defaultdict

consumer = KafkaConsumer(
    'rides',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Count rides by location
location_counts = defaultdict(int)

for message in consumer:
    ride = message.value
    location = ride.get('PULocationID', 'unknown')
    location_counts[location] += 1
    
    # Send aggregated results
    result = {
        'location': location,
        'count': location_counts[location]
    }
    
    producer.send('rides-pulocationid', value=result)
    print(f"Location {location}: {location_counts[location]} rides")
```

## Common Workflows

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git
cd data-engineering-zoomcamp

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
export GCP_PROJECT_ID="your-project-id"
```

### Complete Module Workflow

```bash
# 1. Start Docker infrastructure
docker-compose up -d

# 2. Run Terraform
cd 01-docker-terraform/terraform
terraform init
terraform apply

# 3. Ingest data
python ingest_data.py --params...

# 4. Run dbt models
cd 04-analytics-engineering
dbt run
dbt test

# 5. Run Spark job
spark-submit \
  --master local[*] \
  spark_processing.py

# 6. Clean up
terraform destroy
docker-compose down
```

### Homework Submission Pattern

```bash
# Navigate to cohort folder
cd cohorts/2026/01-docker-terraform

# Complete homework in Jupyter notebook
jupyter notebook homework.ipynb

# Export answers
# Submit through course platform
```

## Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Find process using
