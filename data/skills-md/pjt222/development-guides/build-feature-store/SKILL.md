---
name: build-feature-store
description: >
  Build a feature store using Feast for centralized feature management, configure
  offline and online stores for batch and real-time serving, define feature views
  with transformations, and implement point-in-time correct joins for ML pipelines.
  Use when managing features for multiple ML models, ensuring training-serving consistency,
  serving low-latency features for real-time inference, reusing feature definitions
  across projects, or building a feature catalog for discovery and governance.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: mlops
  complexity: advanced
  language: multi
  tags: feature-store, feast, offline-store, online-store, feature-engineering
---

# Build Feature Store


> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.

Implement centralized feature management with Feast for consistent feature serving across training and inference.

## When to Use

- Managing features for multiple ML models across teams
- Ensuring training-serving consistency for features
- Implementing point-in-time correct historical features
- Serving low-latency features for real-time inference
- Reusing feature definitions across projects
- Versioning feature transformations
- Building feature catalog for discovery and governance
- Preventing feature leakage in training pipelines

## Inputs

- **Required**: Raw data sources (databases, data lakes, data warehouses)
- **Required**: Python environment with Feast installed
- **Required**: Offline store backend (BigQuery, Snowflake, Redshift, or Parquet files)
- **Required**: Online store backend (Redis, DynamoDB, Cassandra, or SQLite for dev)
- **Optional**: Feature transformation logic (Python, SQL, Spark)
- **Optional**: Entity key definitions (user_id, product_id, etc.)
- **Optional**: Kubernetes cluster for Feast server deployment

## Procedure

### Step 1: Initialize Feast Feature Repository

Set up Feast project structure and configure storage backends.

```bash
# Install Feast with required extras
pip install 'feast[redis,postgres]'  # Add backends as needed

# Initialize new feature repository
feast init my_feature_repo
cd my_feature_repo

# Directory structure created:
# my_feature_repo/
# ├── feature_store.yaml       # Configuration
# ├── features.py              # Feature definitions
# └── data/                    # Sample data (dev only)
```

Configure `feature_store.yaml`:

```yaml
# feature_store.yaml
project: customer_analytics
registry: data/registry.db  # SQLite for dev, use S3/GCS for prod
provider: local

# Offline store for training data
offline_store:
  type: postgres
# ... (see EXAMPLES.md for complete implementation)
```

Production configuration with cloud backends:

```yaml
# feature_store.prod.yaml
project: customer_analytics
registry: s3://feast-registry/prod/registry.db
provider: aws

offline_store:
  type: bigquery
  project_id: my-gcp-project
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Feast repository initialized with config file, sample feature definitions created, offline and online stores configured, registry path accessible.

**On failure:** Verify database/Redis credentials (`psql -U feast_user -h localhost`), check connection strings format, ensure databases exist (`CREATE DATABASE feature_store`), verify cloud permissions for S3/BigQuery/DynamoDB, test connectivity to storage backends, check Feast version compatibility with backends (`feast version`).

### Step 2: Define Entities and Data Sources

Create entity definitions and connect to raw data sources.

```python
# entities.py
from feast import Entity, ValueType

# Define entities (primary keys for features)
customer = Entity(
    name="customer",
    description="Customer entity",
    value_type=ValueType.INT64,
# ... (see EXAMPLES.md for complete implementation)
```

Define data sources:

```python
# data_sources.py
from feast import FileSource, BigQuerySource, RedshiftSource
from feast.data_format import ParquetFormat
from datetime import timedelta

# Development: File-based source
customer_transactions_source = FileSource(
    path="data/customer_transactions.parquet",
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Entity definitions reference correct ID columns, data sources connect to raw data successfully, event_timestamp_column exists in source data, created_timestamp_column allows point-in-time queries.

**On failure:** Verify source data files exist and are readable, check BigQuery/Redshift credentials and table access, ensure timestamp columns have correct format (Unix timestamp or ISO8601), verify Kafka connectivity and topic existence, check schema compatibility between sources and entities.

### Step 3: Define Feature Views with Transformations

Create feature views that define how raw data becomes ML-ready features.

```python
# feature_views.py
from feast import FeatureView, Field
from feast.types import Float32, Int64, String, Bool
from datetime import timedelta
from entities import customer, product
from data_sources import customer_features_source

# Simple feature view without transformations
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Feature views registered successfully, schema matches source data, transformations execute without errors, TTL values appropriate for use case, on-demand views combine batch and request features.

**On failure:** Verify field names match source columns exactly, check dtype compatibility (Int64 vs Int32), ensure entity references exist, validate transformation logic with sample data, check for division by zero in calculations, verify request source schema matches inference payload.

### Step 4: Apply Feature Definitions and Materialize Features

Deploy feature definitions to registry and materialize to online store.

```bash
# Apply feature definitions to registry
feast apply

# Expected output:
# Created entity customer
# Created feature view customer_stats
# Created on demand feature view customer_segments

# ... (see EXAMPLES.md for complete implementation)
```

Programmatic materialization:

```python
# materialize_features.py
from feast import FeatureStore
from datetime import datetime, timedelta

# Initialize feature store
fs = FeatureStore(repo_path=".")

# Materialize all feature views
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Feature definitions applied to registry without conflicts, materialization job completes successfully, online store populated with features, feature freshness within configured TTL.

**On failure:** Check offline store query succeeds (`feast feature-views describe customer_stats`), verify time range has data, ensure online store writable (Redis/DynamoDB permissions), check for duplicate feature names across views, verify entity keys exist in source data, monitor materialization job logs for errors, check disk space for local stores.

### Step 5: Retrieve Features for Training

Fetch point-in-time correct historical features for model training.

```python
# get_training_data.py
from feast import FeatureStore
import pandas as pd
from datetime import datetime

# Initialize feature store
fs = FeatureStore(repo_path=".")

# ... (see EXAMPLES.md for complete implementation)
```

Point-in-time correctness validation:

```python
# validate_pit_correctness.py
import pandas as pd
from datetime import datetime, timedelta

def validate_point_in_time_correctness(training_df, entity_df):
    """
    Ensure features don't leak future information.
    """
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Historical features retrieved successfully, entity_df timestamps preserved, no NaN values for materialized features, point-in-time correctness guaranteed (no future data leakage), feature service groups features logically.

**On failure:** Check entity_df has required columns (entity names + event_timestamp), verify feature view names match registry, ensure offline store has data for requested time range, check for timezone mismatches (use UTC), verify entity IDs exist in source data, inspect logs for SQL query errors, validate feature view TTL covers requested time range.

### Step 6: Serve Features for Real-Time Inference

Retrieve low-latency features from online store for model serving.

```python
# serve_features.py
from feast import FeatureStore
import time

# Initialize feature store
fs = FeatureStore(repo_path=".")

def get_inference_features(customer_ids: list, request_data: dict = None):
# ... (see EXAMPLES.md for complete implementation)
```

FastAPI integration:

```python
# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from feast import FeatureStore
import mlflow

app = FastAPI()
fs = FeatureStore(repo_path=".")
# ... (see EXAMPLES.md for complete implementation)
```

**Expected:** Online features retrieved in <10ms for single entity, batch retrieval scales efficiently, on-demand transformations execute correctly, request-time features merged with batch features, API responds quickly (<50ms end-to-end).

**On failure:** Check online store populated (run materialize if empty), verify Redis/DynamoDB connectivity and latency, ensure entity keys exist in online store, check for cold start issues (warm up cache), verify on-demand transformation logic, monitor online store memory/CPU usage, check network latency between service and online store.

## Validation

- [ ] Feast repository initialized and configured
- [ ] Offline and online stores connected successfully
- [ ] Entity definitions match source data
- [ ] Feature views registered in registry
- [ ] On-demand transformations execute correctly
- [ ] Materialization completes without errors
- [ ] Historical features retrieved with point-in-time correctness
- [ ] Online features served with low latency (<10ms)
- [ ] Feature freshness within configured TTL
- [ ] Training-serving consistency verified
- [ ] Feature catalog accessible for discovery

## Common Pitfalls

- **Feature leakage**: Using future data in historical features - always validate point-in-time correctness, use created_timestamp column
- **Inconsistent transformations**: Different logic for training vs serving - use Feast on-demand views for consistency
- **Stale features**: Online store not materialized regularly - set up scheduled materialization jobs (cron/Airflow)
- **Missing entity keys**: Entities in training set not in online store - ensure comprehensive materialization, handle missing keys gracefully
- **Type mismatches**: Schema types don't match source data - validate dtypes before apply, use explicit Field definitions
- **Slow online retrieval**: Network latency or overloaded online store - co-locate feature store with inference service, use connection pooling
- **Large feature views**: Materializing millions of entities is slow - partition by date, use incremental materialization, optimize offline queries
- **No feature versioning**: Breaking changes affect production models - version feature views, maintain backward compatibility
- **Timezone confusion**: Mixing timezones causes incorrect joins - always use UTC for timestamps
- **Ignoring TTL**: Serving expired features - set appropriate TTL values, monitor feature freshness

## Related Skills

- `track-ml-experiments` - Log feature metadata in MLflow experiments
- `orchestrate-ml-pipeline` - Schedule feature materialization jobs
- `version-ml-data` - Version raw data sources for feature engineering
- `deploy-ml-model-serving` - Integrate feature store with model serving
- `serialize-data-formats` - Choose efficient storage formats for features
- `design-serialization-schema` - Design schemas for feature sources
