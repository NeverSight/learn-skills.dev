---
name: azure-data-explorer-kusto-queries
description: "Comprehensive guide for Azure Data Explorer (ADX) and Kusto Query Language (KQL); use when writing/optimizing KQL queries, setting up ingestion, building dashboards, doing time-series/ML analysis, configuring management/security, or when users mention Kusto, KQL, ADX, Azure Data Explorer, or log analytics queries."
---

# Azure Data Explorer & Kusto Query Language

Comprehensive skill for Azure Data Explorer (ADX) - Microsoft's fast, fully managed data analytics service for real-time analysis on large volumes of streaming data.

## Quick Reference

| Task | Go To |
|------|-------|
| Write a KQL query | [kql-query-language/](feature-area-skill-resources/kql-query-language/) |
| Ingest data into ADX | [data-ingestion/](feature-area-skill-resources/data-ingestion/) |
| Create dashboards | [visualization-dashboards/](feature-area-skill-resources/visualization-dashboards/) |
| Time series / ML | [time-series-ml/](feature-area-skill-resources/time-series-ml/) |
| Manage tables / policies | [management-commands/](feature-area-skill-resources/management-commands/) |

## KQL Essentials

### Query Structure

```kql
TableName
| where TimeGenerated > ago(1h)
| where Level == "Error"
| summarize Count = count() by bin(TimeGenerated, 5m), Source
| order by TimeGenerated desc
```

### Top 10 Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `where` | Filter rows | `where Status == 200` |
| `project` | Select columns | `project Name, Age` |
| `extend` | Add computed column | `extend Duration = EndTime - StartTime` |
| `summarize` | Aggregate | `summarize count() by Category` |
| `join` | Combine tables | `join kind=inner OtherTable on Key` |
| `order by` | Sort results | `order by Timestamp desc` |
| `take` | Limit rows | `take 100` |
| `distinct` | Unique values | `distinct UserName` |
| `parse` | Extract from string | `parse Message with * "error:" ErrorMsg` |
| `mv-expand` | Expand arrays | `mv-expand Tags` |

### Common Patterns

**Time filtering:**
```kql
| where TimeGenerated > ago(24h)
| where TimeGenerated between (datetime(2024-01-01) .. datetime(2024-01-31))
```

**Aggregation:**
```kql
| summarize
    Count = count(),
    AvgDuration = avg(Duration),
    P95 = percentile(Duration, 95)
  by bin(TimeGenerated, 1h)
```

**String searching (prefer `has` over `contains` for performance):**
```kql
| where Message has "error"        // Fast - word boundary match
| where Message contains "err"     // Slow - substring match
```

**Join:**
```kql
Table1
| join kind=leftouter (Table2) on CommonKey
```

## Feature Areas

### 1. KQL Query Language
645+ functions and operators for data analysis.

**Reference:** [feature-area-skill-resources/kql-query-language/reference.md](feature-area-skill-resources/kql-query-language/reference.md)
- Tabular operators (where, project, summarize, join, union, etc.)
- Scalar functions (string, datetime, math, conditional)
- Aggregation functions (count, sum, avg, dcount, percentile)
- Data types (string, datetime, dynamic, real, bool, etc.)

**Best Practices:** [feature-area-skill-resources/kql-query-language/best-practices.md](feature-area-skill-resources/kql-query-language/best-practices.md)
- Query optimization techniques
- String operator performance (`has` vs `contains`)
- Join strategies and hints

**Examples:** [feature-area-skill-resources/kql-query-language/examples.md](feature-area-skill-resources/kql-query-language/examples.md)

### 2. Data Ingestion
Multiple methods to get data into ADX.

**Reference:** [feature-area-skill-resources/data-ingestion/reference.md](feature-area-skill-resources/data-ingestion/reference.md)
- Streaming ingestion (low latency, <4MB)
- Queued/batched ingestion (high throughput)
- Connectors: Event Hubs, Event Grid, IoT Hub, Kafka, Spark
- Ingestion mappings (CSV, JSON, Parquet, Avro)

**Best Practices:** [feature-area-skill-resources/data-ingestion/best-practices.md](feature-area-skill-resources/data-ingestion/best-practices.md)
- Choosing streaming vs queued ingestion
- Batching policy tuning
- Error handling

**Examples:** [feature-area-skill-resources/data-ingestion/examples.md](feature-area-skill-resources/data-ingestion/examples.md)

### 3. Visualization & Dashboards
Native dashboards and external integrations.

**Reference:** [feature-area-skill-resources/visualization-dashboards/reference.md](feature-area-skill-resources/visualization-dashboards/reference.md)
- Native ADX dashboards
- `render` operator for inline visualization
- Power BI integration (DirectQuery, Import)
- Grafana integration

**Best Practices:** [feature-area-skill-resources/visualization-dashboards/best-practices.md](feature-area-skill-resources/visualization-dashboards/best-practices.md)
- Dashboard design principles
- Chart type selection
- Performance optimization

**Examples:** [feature-area-skill-resources/visualization-dashboards/examples.md](feature-area-skill-resources/visualization-dashboards/examples.md)

### 4. Time Series & Machine Learning
Advanced analytics for IoT, monitoring, and forecasting.

**Reference:** [feature-area-skill-resources/time-series-ml/reference.md](feature-area-skill-resources/time-series-ml/reference.md)
- `make-series` operator
- Decomposition: `series_decompose`, `series_decompose_anomalies`
- Forecasting: `series_decompose_forecast`
- Python/R plugins for custom ML
- ONNX model inference

**Best Practices:** [feature-area-skill-resources/time-series-ml/best-practices.md](feature-area-skill-resources/time-series-ml/best-practices.md)
- When to use time series analysis
- Anomaly detection tuning
- Native functions vs plugins

**Examples:** [feature-area-skill-resources/time-series-ml/examples.md](feature-area-skill-resources/time-series-ml/examples.md)

### 5. Management Commands
297+ commands for schema, policies, and security.

**Reference:** [feature-area-skill-resources/management-commands/reference.md](feature-area-skill-resources/management-commands/reference.md)
- Schema management (tables, columns, functions)
- 30+ policy types (retention, caching, partitioning, RLS)
- Materialized views
- Security roles and access control

**Best Practices:** [feature-area-skill-resources/management-commands/best-practices.md](feature-area-skill-resources/management-commands/best-practices.md)
- Policy configuration patterns
- Schema design guidelines
- Access control best practices

**Examples:** [feature-area-skill-resources/management-commands/examples.md](feature-area-skill-resources/management-commands/examples.md)

### 6. API & SDK Integration
Programmatic access via REST API and client SDKs.

**Reference:** [feature-area-skill-resources/api-sdk-integration/reference.md](feature-area-skill-resources/api-sdk-integration/reference.md)
- REST API endpoints and authentication
- .NET, Python, Java, Node.js, Go SDKs
- Connection string formats

**Best Practices:** [feature-area-skill-resources/api-sdk-integration/best-practices.md](feature-area-skill-resources/api-sdk-integration/best-practices.md)

**Examples:** [feature-area-skill-resources/api-sdk-integration/examples.md](feature-area-skill-resources/api-sdk-integration/examples.md)

### 7. Security & Access Control
Authentication, authorization, and data protection.

**Reference:** [feature-area-skill-resources/security-access-control/reference.md](feature-area-skill-resources/security-access-control/reference.md)
- Microsoft Entra ID authentication
- RBAC roles and row-level security
- Network security and private endpoints
- Customer-managed keys (CMK)

**Best Practices:** [feature-area-skill-resources/security-access-control/best-practices.md](feature-area-skill-resources/security-access-control/best-practices.md)

**Examples:** [feature-area-skill-resources/security-access-control/examples.md](feature-area-skill-resources/security-access-control/examples.md)

### 8. Cluster Management
Cluster operations, scaling, and monitoring.

**Reference:** [feature-area-skill-resources/cluster-management/reference.md](feature-area-skill-resources/cluster-management/reference.md)
- SKU selection and sizing
- Auto-scale configuration
- Monitoring and diagnostics

**Best Practices:** [feature-area-skill-resources/cluster-management/best-practices.md](feature-area-skill-resources/cluster-management/best-practices.md)

**Examples:** [feature-area-skill-resources/cluster-management/examples.md](feature-area-skill-resources/cluster-management/examples.md)

### 9. Business Continuity
High availability and disaster recovery.

**Reference:** [feature-area-skill-resources/business-continuity/reference.md](feature-area-skill-resources/business-continuity/reference.md)
- Follower databases
- Cross-region replication
- Backup and restore

**Best Practices:** [feature-area-skill-resources/business-continuity/best-practices.md](feature-area-skill-resources/business-continuity/best-practices.md)

**Examples:** [feature-area-skill-resources/business-continuity/examples.md](feature-area-skill-resources/business-continuity/examples.md)

### 10. Integration Services
Azure service integrations.

**Reference:** [feature-area-skill-resources/integration-services/reference.md](feature-area-skill-resources/integration-services/reference.md)
- Azure Monitor, Synapse, Data Factory
- Logic Apps, Power Automate
- Cross-product queries

**Best Practices:** [feature-area-skill-resources/integration-services/best-practices.md](feature-area-skill-resources/integration-services/best-practices.md)

**Examples:** [feature-area-skill-resources/integration-services/examples.md](feature-area-skill-resources/integration-services/examples.md)

### 11. UDF Functions Library
Pre-built user-defined functions for advanced analytics.

**Reference:** [feature-area-skill-resources/udf-functions-library/reference.md](feature-area-skill-resources/udf-functions-library/reference.md)
- Statistical tests (t-test, KS test, normality)
- ML functions (K-means, DBSCAN)
- Time series and text analytics UDFs

**Best Practices:** [feature-area-skill-resources/udf-functions-library/best-practices.md](feature-area-skill-resources/udf-functions-library/best-practices.md)

**Examples:** [feature-area-skill-resources/udf-functions-library/examples.md](feature-area-skill-resources/udf-functions-library/examples.md)

### 12. Tools & Clients
Desktop, CLI, and web tools.

**Reference:** [feature-area-skill-resources/tools-clients/reference.md](feature-area-skill-resources/tools-clients/reference.md)
- Kusto.Explorer (desktop IDE)
- Kusto.Cli (command line)
- Web UI and Emulator

**Best Practices:** [feature-area-skill-resources/tools-clients/best-practices.md](feature-area-skill-resources/tools-clients/best-practices.md)

**Examples:** [feature-area-skill-resources/tools-clients/examples.md](feature-area-skill-resources/tools-clients/examples.md)

## Resources

### Official Documentation
The complete Microsoft documentation is available as a submodule at:
`submodules/dataexplorer-docs/`

### Investigation Reports
Detailed analysis from the skill creation process:
- `investigation-reports/repository-layout/` - Repo structure analysis
- `investigation-reports/feature-overview/` - Feature taxonomy and mapping
- `investigation-reports/feature-in-depth/` - Comprehensive research per feature

## See Also

- [Azure Data Explorer Documentation](https://learn.microsoft.com/en-us/azure/data-explorer/)
- [KQL Quick Reference](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/kql-quick-reference)
- [KQL Cheat Sheet](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/sqlcheatsheet)
