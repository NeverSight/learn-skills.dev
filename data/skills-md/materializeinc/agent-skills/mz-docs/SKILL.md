---
name: mz-docs
description: Materialize documentation for SQL syntax, data ingestion, concepts, and best practices. Use when users ask about Materialize queries, sources, sinks, views, or clusters.
---

# Materialize Documentation

This skill provides comprehensive documentation for Materialize, a streaming database for real-time analytics.

## How to Use This Skill

When a user asks about Materialize:

1. **For SQL syntax/commands**: Read files in the `sql/` directory
2. **For core concepts**: Read files in the `fundamentals/concepts/` directory
3. **For data ingestion**: Read files in the `ingest-data/` directory
4. **For transformations**: Read files in the `transform-data/` directory

## Documentation Sections

### Clusters
Guidance for configuring and operating Materialize clusters.

- **Autoscaling for hydration**: `clusters/autoscaling/index.md`
- **M.1 to cc size mapping**: `clusters/m1-cc-mapping/index.md`
- **Operational guidelines**: `clusters/operational-guidelines/index.md`
- **Optimize hydration requirements**: `clusters/optimize-hydration-requirements/index.md`
- **Size clusters for hydration**: `clusters/sizing/index.md`
- **System clusters**: `clusters/system-clusters/index.md`
- **Troubleshoot clusters**: `clusters/troubleshoot-clusters/index.md`

### Developer tools
Tools for developing, deploying, and managing Materialize.

- **Download and run Materialize Emulator**: `developer-tools/install-materialize-emulator/index.md`
- **Manage Materialize**: `developer-tools/manage/index.md`
- **Materialize console**: `developer-tools/console/index.md`
- **MCP Servers and agent skills**: `developer-tools/mcp-server/index.md`
- **mz-debug**: `developer-tools/mz-debug/index.md`
- **Tools and integrations**: `developer-tools/integrations/index.md`
- **Use dbt to manage Materialize**: `developer-tools/dbt/index.md`
- **Use mz-deploy to manage Materialize**: `developer-tools/mz-deploy/index.md`
- **Use Terraform to manage Materialize**: `developer-tools/terraform/index.md`

### Ingest data
Best practices for ingesting data into Materialize from external systems.

- **Amazon EventBridge**: `ingest-data/webhooks/amazon-eventbridge/index.md`
- **AWS PrivateLink connections (Cloud-only)**: `ingest-data/network-security/privatelink/index.md`
- **Change a webhook source's included headers**: `ingest-data/webhooks/change-included-headers/index.md`
- **CockroachDB CDC using Kafka and Changefeeds**: `ingest-data/cdc-cockroachdb/index.md`
- **Debezium**: `ingest-data/debezium/index.md`
- **Fivetran**: `ingest-data/fivetran/index.md`
- **HubSpot**: `ingest-data/webhooks/hubspot/index.md`
- **Ingestion performance**: `ingest-data/performance/index.md`
- **Kafka**: `ingest-data/kafka/index.md`
- **MongoDB**: `ingest-data/mongodb/index.md`
- _(and 16 more files in this section)_

### Materialize Cloud
Guidance for operating Materialize Cloud.

- **Customer responsibility model (Cloud)**: `materialize-cloud/customer-responsibilities/index.md`
- **Disaster recovery (Cloud)**: `materialize-cloud/disaster-recovery/index.md`
- **Free Trials**: `materialize-cloud/free-trials/index.md`
- **Usage & billing (Cloud)**: `materialize-cloud/billing/index.md`

### Monitoring and alerting
Monitor the performance of your Materialize region with Datadog and Grafana.

- **Appendix: Metrics**: `observability/appendix-metrics/index.md`
- **Cloud**: `observability/cloud/index.md`
- **Essential metrics**: `observability/essential-metrics/index.md`
- **Replica resource usage**: `observability/replica-resource-usage/index.md`
- **Self-Managed**: `observability/self-managed/index.md`

### Overview
Learn how to efficiently transform data using Materialize SQL.

- **Dataflow troubleshooting**: `transform-data/dataflow-troubleshooting/index.md`
- **Dictionary compression**: `transform-data/dictionary-compression/index.md`
- **FAQ: Indexes**: `transform-data/faq/index.md`
- **Freshness troubleshooting**: `transform-data/freshness-troubleshooting/index.md`
- **How to monitor freshness in Materialize**: `transform-data/monitor-freshness/index.md`
- **Idiomatic Materialize SQL**: `transform-data/idiomatic-materialize-sql/index.md`
- **Optimization**: `transform-data/optimization/index.md`
- **Patterns**: `transform-data/patterns/index.md`
- **Updating materialized views**: `transform-data/updating-materialized-views/index.md`

### Security

- **Appendix**: `security/appendix/index.md`
- **Cloud**: `security/cloud/index.md`
- **Patterns**: `security/patterns/index.md`
- **Self-managed**: `security/self-managed/index.md`

### Self-Managed Deployments
Learn about the key components and architecture of self-managed Materialize deployments.

- **Appendix**: `self-managed-deployments/appendix/index.md`
- **Configure single sign-on**: `self-managed-deployments/sso/index.md`
- **Configuring System Parameters**: `self-managed-deployments/configuration-system-parameters/index.md`
- **Deployment guidelines**: `self-managed-deployments/deployment-guidelines/index.md`
- **FAQ**: `self-managed-deployments/faq/index.md`
- **Installation**: `self-managed-deployments/installation/index.md`
- **Materialize CRD Field Descriptions**: `self-managed-deployments/materialize-crd-field-descriptions/index.md`
- **Materialize Operator Configuration**: `self-managed-deployments/operator-configuration/index.md`
- **Query History**: `self-managed-deployments/query-history/index.md`
- **Self-managed release versions**: `self-managed-deployments/release-versions/index.md`
- _(and 3 more files in this section)_

### Serve results
Serving results from Materialize

- **`SELECT` and `SUBSCRIBE`**: `serve-results/query-results/index.md`
- **ADBC (Arrow Database Connectivity)**: `serve-results/adbc/index.md`
- **Client libraries**: `serve-results/client-libraries/index.md`
- **Connect to Materialize via HTTP**: `serve-results/http-api/index.md`
- **Connect to Materialize via WebSocket**: `serve-results/websocket-api/index.md`
- **Connection Pooling**: `serve-results/connection-pooling/index.md`
- **Durable subscriptions**: `serve-results/durable-subscriptions/index.md`
- **Foreign data wrapper (FDW) **: `serve-results/fdw-setup/index.md`
- **Isolation levels**: `serve-results/isolation-level/index.md`
- **SQL clients**: `serve-results/sql-clients/index.md`
- _(and 3 more files in this section)_

### Sink results
Sinking results from Materialize to external systems.

- **Amazon S3**: `export-data/s3/index.md`
- **Apache Iceberg**: `export-data/iceberg/index.md`
- **AWS S3 Tables**: `export-data/iceberg-aws/index.md`
- **Census**: `export-data/census/index.md`
- **Consume from Snowflake on AWS S3 Tables**: `export-data/iceberg-aws-snowflake/index.md`
- **Databricks Unity Catalog**: `export-data/iceberg-databricks/index.md`
- **Elasticsearch**: `export-data/elasticsearch/index.md`
- **GCP BigLake**: `export-data/iceberg-gcp/index.md`
- **Kafka and Redpanda**: `export-data/kafka/index.md`
- **OpenSearch**: `export-data/opensearch/index.md`
- _(and 5 more files in this section)_

### SQL commands
SQL commands reference.

- **Namespaces**: `sql/namespaces/index.md`
- **ALTER CLUSTER**: `sql/alter-cluster/index.md`
- **ALTER CLUSTER REPLICA**: `sql/alter-cluster-replica/index.md`
- **ALTER CONNECTION**: `sql/alter-connection/index.md`
- **ALTER DATABASE**: `sql/alter-database/index.md`
- **ALTER DEFAULT PRIVILEGES**: `sql/alter-default-privileges/index.md`
- **ALTER INDEX**: `sql/alter-index/index.md`
- **ALTER MATERIALIZED VIEW**: `sql/alter-materialized-view/index.md`
- **ALTER NETWORK POLICY (Cloud)**: `sql/alter-network-policy/index.md`
- **ALTER ROLE**: `sql/alter-role/index.md`
- _(and 111 more files in this section)_

### What is Materialize?
Learn more about Materialize

- **Architecture Patterns**: `fundamentals/architecture-patterns/index.md`
- **Concepts**: `fundamentals/concepts/index.md`

## Quick Reference

### Common SQL Commands

| Command | Description |
|---------|-------------|
| `CREATE SOURCE` | Connect to external data sources (Kafka, PostgreSQL, MySQL) |
| `CREATE MATERIALIZED VIEW` | Create incrementally maintained views |
| `CREATE INDEX` | Create indexes on views for faster queries |
| `CREATE SINK` | Export data to external systems |
| `SELECT` | Query data from sources, views, and tables |

### Key Concepts

- **Sources**: Connections to external data systems that stream data into Materialize
- **Materialized Views**: Views that are incrementally maintained as source data changes
- **Indexes**: Arrangements of data in memory for fast point lookups
- **Clusters**: Isolated compute resources for running dataflows
- **Sinks**: Connections that export data from Materialize to external systems
