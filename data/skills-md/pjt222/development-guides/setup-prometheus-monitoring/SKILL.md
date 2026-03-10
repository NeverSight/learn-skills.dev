---
name: setup-prometheus-monitoring
description: >
  Configure Prometheus for time-series metrics collection, including scrape configurations,
  service discovery, recording rules, and federation patterns for multi-cluster deployments.
  Use when setting up centralized metrics collection for microservices, implementing time-series
  monitoring for application and infrastructure, establishing a foundation for SLO/SLI tracking
  and alerting, or migrating from legacy monitoring solutions to a modern observability stack.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: observability
  complexity: intermediate
  language: multi
  tags: prometheus, monitoring, metrics, scrape, recording-rules
---

# Setup Prometheus Monitoring

Configure a production-ready Prometheus deployment with scrape targets, recording rules, and federation.

## When to Use

- Setting up centralized metrics collection for microservices or distributed systems
- Implementing time-series monitoring for application and infrastructure metrics
- Establishing a foundation for SLO/SLI tracking and alerting
- Consolidating metrics from multiple Prometheus instances via federation
- Migrating from legacy monitoring solutions to modern observability stack

## Inputs

- **Required**: List of scrape targets (services, exporters, endpoints)
- **Required**: Retention period and storage requirements
- **Optional**: Existing service discovery mechanism (Kubernetes, Consul, EC2)
- **Optional**: Recording rules for pre-aggregated metrics
- **Optional**: Federation hierarchy for multi-cluster setups

## Procedure

### Step 1: Install and Configure Prometheus

Create the base Prometheus configuration with global settings and scrape intervals.

```bash
# Create Prometheus directory structure
mkdir -p /etc/prometheus/{rules,file_sd}
mkdir -p /var/lib/prometheus

# Download Prometheus (adjust version as needed)
cd /tmp
wget https://github.com/prometheus/prometheus/releases/download/v2.48.0/prometheus-2.48.0.linux-amd64.tar.gz
tar xvf prometheus-2.48.0.linux-amd64.tar.gz
sudo cp prometheus-2.48.0.linux-amd64/{prometheus,promtool} /usr/local/bin/
```

Create `/etc/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - localhost:9093

# Load recording and alerting rules
rule_files:
  - "rules/*.yml"

# Scrape configurations
scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
        labels:
          env: 'production'

  # Node exporter for host metrics
  - job_name: 'node'
    static_configs:
      - targets:
          - 'node1:9100'
          - 'node2:9100'
        labels:
          env: 'production'

  # Application metrics with file-based service discovery
  - job_name: 'app-services'
    file_sd_configs:
      - files:
          - '/etc/prometheus/file_sd/services.json'
        refresh_interval: 30s
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
      - source_labels: [env]
        target_label: environment
```

**Expected:** Prometheus starts successfully, web UI accessible at `http://localhost:9090`, targets listed under Status > Targets.

**On failure:**
- Check syntax with `promtool check config /etc/prometheus/prometheus.yml`
- Verify file permissions: `sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus`
- Check logs: `journalctl -u prometheus -f`

### Step 2: Configure Service Discovery

Set up dynamic target discovery to avoid manual target management.

For **Kubernetes** environments, add to `scrape_configs`:

```yaml
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods with prometheus.io/scrape annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # Use custom port if specified
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
      # Add namespace as label
      - source_labels: [__meta_kubernetes_namespace]
        target_label: kubernetes_namespace
      # Add pod name as label
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: kubernetes_pod_name
```

For **file-based** service discovery, create `/etc/prometheus/file_sd/services.json`:

```json
[
  {
    "targets": ["web-app-1:8080", "web-app-2:8080"],
    "labels": {
      "job": "web-app",
      "env": "production",
      "team": "platform"
    }
  },
  {
    "targets": ["api-service-1:9090", "api-service-2:9090"],
    "labels": {
      "job": "api-service",
      "env": "production",
      "team": "backend"
    }
  }
]
```

For **Consul** service discovery:

```yaml
  - job_name: 'consul-services'
    consul_sd_configs:
      - server: 'consul.example.com:8500'
        services: []  # Empty list means discover all services
    relabel_configs:
      - source_labels: [__meta_consul_service]
        target_label: job
      - source_labels: [__meta_consul_tags]
        regex: '.*,monitoring,.*'
        action: keep
```

**Expected:** Dynamic targets appear in Prometheus UI, automatically updated when services scale or change.

**On failure:**
- Kubernetes: Verify RBAC permissions with `kubectl auth can-i list pods --as=system:serviceaccount:monitoring:prometheus`
- File SD: Validate JSON syntax with `python -m json.tool /etc/prometheus/file_sd/services.json`
- Consul: Test connectivity with `curl http://consul.example.com:8500/v1/catalog/services`

### Step 3: Create Recording Rules

Pre-aggregate expensive queries for dashboard performance and alerting efficiency.

Create `/etc/prometheus/rules/recording_rules.yml`:

```yaml
groups:
  - name: api_aggregations
    interval: 30s
    rules:
      # Calculate request rate per endpoint (5m window)
      - record: job:http_requests:rate5m
        expr: |
          sum by (job, endpoint, method) (
            rate(http_requests_total[5m])
          )

      # Calculate error rate percentage
      - record: job:http_errors:rate5m
        expr: |
          sum by (job) (
            rate(http_requests_total{status=~"5.."}[5m])
          ) / sum by (job) (
            rate(http_requests_total[5m])
          ) * 100

      # P95 latency by endpoint
      - record: job:http_request_duration_seconds:p95
        expr: |
          histogram_quantile(0.95,
            sum by (job, endpoint, le) (
              rate(http_request_duration_seconds_bucket[5m])
            )
          )

  - name: resource_aggregations
    interval: 1m
    rules:
      # CPU usage by instance
      - record: instance:cpu_usage:ratio
        expr: |
          1 - avg by (instance) (
            rate(node_cpu_seconds_total{mode="idle"}[5m])
          )

      # Memory usage percentage
      - record: instance:memory_usage:ratio
        expr: |
          1 - (
            node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
          )

      # Disk usage by mount point
      - record: instance:disk_usage:ratio
        expr: |
          1 - (
            node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*"}
            / node_filesystem_size_bytes{fstype!~"tmpfs|fuse.*"}
          )
```

Validate and reload:

```bash
# Validate rules syntax
promtool check rules /etc/prometheus/rules/recording_rules.yml

# Reload Prometheus configuration (without restart)
curl -X POST http://localhost:9090/-/reload

# Or send SIGHUP signal
sudo killall -HUP prometheus
```

**Expected:** Recording rules evaluate successfully, new metrics visible in Prometheus with `job:` prefix, query performance improved for dashboards.

**On failure:**
- Check rule syntax with `promtool check rules`
- Verify evaluation interval matches data availability
- Check for missing source metrics: `curl http://localhost:9090/api/v1/targets`
- Review logs for evaluation errors: `journalctl -u prometheus | grep -i error`

### Step 4: Configure Storage and Retention

Optimize storage for retention requirements and query performance.

Edit `/etc/systemd/system/prometheus.service`:

```ini
[Unit]
Description=Prometheus Monitoring System
Documentation=https://prometheus.io/docs/introduction/overview/
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --storage.tsdb.retention.time=30d \
  --storage.tsdb.retention.size=50GB \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=:9090 \
  --web.enable-lifecycle \
  --web.enable-admin-api

Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

Key storage flags:
- `--storage.tsdb.retention.time=30d`: Keep 30 days of data
- `--storage.tsdb.retention.size=50GB`: Limit storage to 50GB (whichever limit hits first)
- `--storage.tsdb.wal-compression`: Enable WAL compression (reduces disk I/O)
- `--web.enable-lifecycle`: Allow config reload via HTTP POST
- `--web.enable-admin-api`: Enable snapshot and delete APIs

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl status prometheus
```

**Expected:** Prometheus retains metrics according to policy, disk usage stays within limits, old data automatically pruned.

**On failure:**
- Monitor disk usage: `du -sh /var/lib/prometheus`
- Check TSDB stats: `curl http://localhost:9090/api/v1/status/tsdb`
- Verify retention settings: `curl http://localhost:9090/api/v1/status/runtimeinfo | jq .data.storageRetention`
- Force cleanup: `curl -X POST http://localhost:9090/api/v1/admin/tsdb/delete_series?match[]={__name__=~".+"}`

### Step 5: Set Up Federation (Multi-Cluster)

Configure hierarchical Prometheus for aggregating metrics across clusters.

On **edge Prometheus** instances (in each cluster), ensure external labels are set:

```yaml
global:
  external_labels:
    cluster: 'production-east'
    datacenter: 'us-east-1'
```

On **central Prometheus** instance, add federation scrape config:

```yaml
scrape_configs:
  - job_name: 'federate-production'
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        # Aggregate only pre-computed recording rules
        - '{__name__=~"job:.*"}'
        # Include alert states
        - '{__name__=~"ALERTS.*"}'
        # Include critical infrastructure metrics
        - 'up{job=~".*"}'
    static_configs:
      - targets:
          - 'prometheus-east.example.com:9090'
          - 'prometheus-west.example.com:9090'
        labels:
          env: 'production'
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
      - source_labels: [__address__]
        regex: 'prometheus-(.*).example.com.*'
        target_label: cluster
        replacement: '$1'
```

Federation best practices:
- Use `honor_labels: true` to preserve original labels
- Federate only recording rules and aggregates (not raw metrics)
- Set appropriate scrape intervals (longer than edge Prometheus evaluation)
- Use `match[]` to filter metrics (avoid federating everything)

**Expected:** Central Prometheus shows federated metrics from all clusters, queries can span multiple regions, minimal data duplication.

**On failure:**
- Verify federation endpoint accessibility: `curl http://prometheus-east.example.com:9090/federate?match[]={__name__=~"job:.*"} | head -20`
- Check for label conflicts (central vs edge external labels)
- Monitor federation lag: compare timestamp differences
- Review match patterns: `curl http://localhost:9090/api/v1/label/__name__/values | jq .data | grep "job:"`

### Step 6: Implement High Availability (Optional)

Deploy redundant Prometheus instances with identical configurations for failover.

Use **Thanos** or **Cortex** for true HA, or simple load-balanced setup:

```yaml
# prometheus-1.yml and prometheus-2.yml (identical configs)
global:
  scrape_interval: 15s
  external_labels:
    prometheus: 'prometheus-1'  # Different per instance
    replica: 'A'

# Use --web.external-url flag for each instance
# prometheus-1: --web.external-url=http://prometheus-1.example.com:9090
# prometheus-2: --web.external-url=http://prometheus-2.example.com:9090
```

Configure Grafana to query both instances:

```json
{
  "name": "Prometheus-HA",
  "type": "prometheus",
  "url": "http://prometheus-lb.example.com",
  "jsonData": {
    "httpMethod": "POST",
    "timeInterval": "15s"
  }
}
```

Use HAProxy or nginx for load balancing:

```nginx
upstream prometheus_backend {
    server prometheus-1.example.com:9090 max_fails=3 fail_timeout=30s;
    server prometheus-2.example.com:9090 max_fails=3 fail_timeout=30s;
}

server {
    listen 9090;
    location / {
        proxy_pass http://prometheus_backend;
        proxy_set_header Host $host;
    }
}
```

**Expected:** Query requests balanced across instances, automatic failover if one instance down, no data loss during single instance failure.

**On failure:**
- Verify both instances scraping same targets (slight time skew acceptable)
- Check for configuration drift between instances
- Monitor deduplication in queries (Grafana shows duplicate series)
- Review load balancer health checks

## Validation

- [ ] Prometheus web UI accessible at expected endpoint
- [ ] All configured scrape targets showing as UP in Status > Targets
- [ ] Service discovery dynamically adding/removing targets as expected
- [ ] Recording rules evaluating successfully (no errors in logs)
- [ ] Metrics retention matching configured time/size limits
- [ ] Federation (if configured) pulling metrics from edge instances
- [ ] Queries returning expected metric cardinality (not excessive)
- [ ] Disk usage stable and within allocated storage budget
- [ ] Configuration reload working via HTTP endpoint or SIGHUP
- [ ] Prometheus self-monitoring metrics available (up, scrape duration, etc.)

## Common Pitfalls

- **High cardinality metrics**: Avoid labels with unbounded values (user IDs, timestamps, UUIDs). Use recording rules to aggregate before storage.
- **Scrape interval mismatch**: Recording rules should evaluate at intervals equal to or greater than scrape intervals to avoid gaps.
- **Federation overload**: Federating all metrics creates massive data duplication. Only federate aggregated recording rules.
- **Missing relabel configs**: Without proper relabeling, service discovery can create confusing or duplicate labels.
- **Retention too short**: Set retention longer than your longest dashboard time window to avoid "no data" gaps.
- **No resource limits**: Prometheus can consume excessive memory with high cardinality. Set `--storage.tsdb.max-block-duration` and monitor heap usage.
- **Disabled lifecycle endpoint**: Without `--web.enable-lifecycle`, config reloads require full restarts causing scrape gaps.

## Related Skills

- `configure-alerting-rules` - Define alerting rules based on Prometheus metrics and route to Alertmanager
- `build-grafana-dashboards` - Visualize Prometheus metrics with Grafana dashboards and panels
- `define-slo-sli-sla` - Establish SLO/SLI targets using Prometheus recording rules and error budget tracking
- `instrument-distributed-tracing` - Complement metrics with distributed tracing for deeper observability
