---
name: log-management-system
description: Implement comprehensive log management including rotation, retention, forwarding, aggregation, storage, and lifecycle management
license: MIT
compatibility: opencode
metadata:
  audience: SREs, DevOps engineers, system administrators
  category: observability
---

# Log Management System

Design and implement comprehensive log management systems including rotation, retention policies, log forwarding, aggregation, storage strategies, and lifecycle management for scalable observability.

## When to use me

Use this skill when:
- Designing log management infrastructure for applications or services
- Implementing log rotation and retention policies
- Setting up log forwarding to centralized aggregation systems
- Planning log storage strategies for cost and performance optimization
- Establishing log lifecycle management (ingestion, processing, storage, archival, deletion)
- Troubleshooting log pipeline issues or performance problems
- Scaling log management for high-volume applications
- Ensuring compliance with data retention requirements

## What I do

### 1. Log Rotation & Retention
- **Design rotation policies** based on size, time, or both
- **Implement retention strategies** (time-based, size-based, event-based)
- **Configure compression** for rotated logs (gzip, zstd, lz4)
- **Establish archival procedures** for long-term storage
- **Implement deletion policies** for expired logs
- **Monitor rotation health** and alert on failures

### 2. Log Forwarding & Aggregation
- **Design forwarding architecture** (agent-based, daemon-based, library-based)
- **Implement reliable delivery** with retries and backoff
- **Configure batching and buffering** for efficiency
- **Handle network failures** and connection issues
- **Implement load balancing** across aggregation endpoints
- **Monitor forwarding latency** and throughput

### 3. Log Storage Strategies
- **Hot storage** for recent logs (fast query, high cost)
- **Warm storage** for medium-term logs (balanced cost/performance)
- **Cold storage** for archival logs (slow query, low cost)
- **Tiered storage** with automatic data movement between tiers
- **Compression optimization** per storage tier
- **Cost management** across storage classes

### 4. Lifecycle Management
- **Ingestion pipeline** design and optimization
- **Processing and enrichment** at ingestion time
- **Indexing strategies** for efficient querying
- **Retention enforcement** across storage tiers
- **Archival procedures** to long-term storage
- **Deletion processes** for compliance requirements

### 5. Performance & Scaling
- **Throughput optimization** for high-volume logs
- **Latency management** for real-time requirements
- **Resource utilization** monitoring and optimization
- **Scalability planning** for growth
- **Bottleneck identification** and resolution
- **Capacity planning** for storage and processing

## Log Rotation Patterns

### Size-Based Rotation
```
/var/log/app/app.log
/var/log/app/app.log.1.gz
/var/log/app/app.log.2.gz
/var/log/app/app.log.3.gz
...
```

Configuration:
- **Max file size**: 100MB, 1GB, etc.
- **Number of rotations**: 10, 100, 1000
- **Compression**: On rotation, on creation
- **Permissions**: Maintain appropriate file permissions

### Time-Based Rotation
```
/var/log/app/app-2026-02-26.log
/var/log/app/app-2026-02-25.log.gz
/var/log/app/app-2026-02-24.log.gz
...
```

Configuration:
- **Rotation interval**: Hourly, daily, weekly, monthly
- **Retention period**: 7 days, 30 days, 90 days, 1 year
- **Timezone handling**: UTC, local time, with offsets
- **Naming conventions**: Date-based, timestamp-based

### Hybrid Rotation
- **Primary rotation**: Size-based for active file
- **Secondary rotation**: Time-based for archived files
- **Tertiary compression**: Compression after time period
- **Quaternary archival**: Move to cold storage after retention

## Forwarding Architectures

### Agent-Based Forwarding
```
Application → Local File → Log Agent (Fluentd/Logstash) → Central Aggregation
```

**Advantages**:
- Decouples application from forwarding logic
- Can buffer during network outages
- Can process/enrich before forwarding
- Supports multiple input/output formats

**Disadvantages**:
- Additional resource consumption
- Configuration management overhead
- Potential single point of failure

### Library/Direct Forwarding
```
Application → Logging Library → Central Aggregation
```

**Advantages**:
- Simpler architecture
- Lower latency
- Fewer moving parts

**Disadvantages**:
- Coupled to application lifecycle
- Limited buffering during outages
- May lose logs during application crashes

### Sidecar Pattern (Containers)
```
Application Container → Sidecar Container → Central Aggregation
```

**Advantages**:
- Decoupled but co-located
- Shares container lifecycle
- Can use specialized sidecar images

**Disadvantages**:
- Additional container overhead
- Inter-container communication complexity

## Storage Tier Strategy

### Tier 1: Hot Storage (0-7 days)
- **Purpose**: Real-time debugging, recent issue investigation
- **Characteristics**: Fast query, full-text search, high availability
- **Examples**: Elasticsearch, Splunk, Cloud Logging
- **Retention**: 1-7 days typically
- **Cost**: Highest per GB

### Tier 2: Warm Storage (8-30 days)
- **Purpose**: Trend analysis, weekly/monthly reporting
- **Characteristics**: Slower query, aggregated views, good availability
- **Examples**: Compressed files on fast storage, warmed indices
- **Retention**: 8-30 days typically
- **Cost**: Medium per GB

### Tier 3: Cold Storage (31-365 days)
- **Purpose**: Compliance, occasional investigations, historical analysis
- **Characteristics**: Very slow query, batch processing, lower availability
- **Examples**: Object storage (S3, GCS), tape backup
- **Retention**: 31-365+ days
- **Cost**: Lowest per GB

### Tier 4: Archival Storage (1+ years)
- **Purpose**: Legal requirements, historical records
- **Characteristics**: Extremely slow retrieval, write-once-read-rarely
- **Examples**: Glacier, deep archival services
- **Retention**: Years to decades
- **Cost**: Minimal but retrieval costs may apply

## Examples

```bash
# Configure log rotation policy
npm run log-management:configure-rotation -- --max-size 100MB --keep-files 10 --compress gzip

# Set up log forwarding
npm run log-management:configure-forwarding -- --agent fluentd --destination elasticsearch --batch-size 1000

# Design storage strategy
npm run log-management:design-storage -- --hot-days 7 --warm-days 30 --cold-days 365 --archive-years 7

# Analyze current log management
npm run log-management:analyze -- --path /var/log --output analysis.json

# Implement lifecycle policy
npm run log-management:lifecycle -- --ingestion-kafka --processing-flink --storage-s3 --retention-90d
```

## Output format

### Log Management Configuration:
```yaml
log_management:
  rotation:
    strategy: "size_and_time"
    max_size_mb: 100
    max_age_days: 7
    compress_on_rotation: true
    compression_algorithm: "gzip"
    keep_rotated: 10
  
  forwarding:
    method: "agent_based"
    agent: "fluentd"
    configuration:
      buffer:
        type: "file"
        path: "/var/log/fluentd-buffer"
        flush_interval: 5
        retry_limit: 10
      destination:
        type: "elasticsearch"
        hosts: ["elasticsearch:9200"]
        index: "app-logs-%Y.%m.%d"
  
  storage:
    tiers:
      hot:
        type: "elasticsearch"
        retention_days: 7
        replication: 2
      warm:
        type: "s3"
        retention_days: 30
        compression: "zstd"
      cold:
        type: "glacier"
        retention_days: 365
        retrieval_time: "3-5 hours"
    
  lifecycle:
    ingestion_rate_limit: "10000/s"
    processing_enrichment: true
    indexing_strategy: "daily_index"
    retention_enforcement: "automated"
    archival_schedule: "daily"
    deletion_procedure: "secure_delete"
  
  monitoring:
    metrics:
      - log_volume_per_second
      - rotation_success_rate
      - forwarding_latency
      - storage_utilization
    alerts:
      - rotation_failed
      - forwarding_stopped
      - storage_90_percent_full
      - retention_violation
```

### Log Management Assessment:
```
Log Management System Assessment
───────────────────────────────
System: payment-platform
Assessment Date: 2026-02-26
Score: 65/100

Current State:
✅ Log rotation implemented (size-based, 100MB)
✅ Basic forwarding to centralized system
✅ Hot storage configured (7 days retention)

Areas for Improvement:
⚠️  No tiered storage strategy (all logs in hot storage)
⚠️  Limited buffering during network outages (lose logs after 100MB)
⚠️  No lifecycle management (manual archival/deletion)
⚠️  No compression for rotated logs
⚠️  Inconsistent retention across services

Critical Issues:
❌ No monitoring of log management system itself
❌ Single point of failure in forwarding pipeline
❌ No disaster recovery for log data
❌ Compliance risks with retention policies

Storage Cost Analysis:
- Current: $2,500/month (all logs in hot storage)
- Optimized: $850/month (with tiered strategy)
- Savings potential: 66% with proper tiering

Recommendations:
1. Implement tiered storage strategy immediately
2. Add buffering and retry logic to forwarding
3. Automate lifecycle management
4. Set up comprehensive monitoring
5. Create disaster recovery plan for log data

Implementation Timeline:
- Week 1-2: Tiered storage implementation
- Week 3-4: Forwarding reliability improvements
- Week 5-6: Lifecycle automation
- Week 7-8: Monitoring and alerting
- Ongoing: Regular review and optimization
```

## Notes

- **Log management is not "set and forget"** - requires ongoing maintenance
- **Cost optimization is critical** - log storage can become expensive quickly
- **Reliability matters** - lost logs mean lost observability
- **Compliance requirements** vary by industry and region
- **Scalability planning** should anticipate 10x-100x growth
- **Disaster recovery** for logs is often overlooked but critical
- **Security considerations** include access control and encryption
- **Performance monitoring** of the log management system itself is essential
- **Regular review** of policies and configurations as needs evolve
- **Document everything** - rotation policies, retention rules, procedures