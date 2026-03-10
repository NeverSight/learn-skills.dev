---
name: build-grafana-dashboards
description: >
  Create production-ready Grafana dashboards with reusable panels, template variables,
  annotations, and provisioning for version-controlled dashboard deployment. Use when
  creating visual representations of Prometheus, Loki, or other data source metrics,
  building operational dashboards for SRE teams, migrating from manual dashboard creation
  to version-controlled provisioning, or establishing executive-level SLO compliance
  reporting.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: observability
  complexity: intermediate
  language: multi
  tags: grafana, dashboards, visualization, panels, provisioning
---

# Build Grafana Dashboards

Design and deploy Grafana dashboards with best practices for maintainability, reusability, and version control.

## When to Use

- Creating visual representations of Prometheus, Loki, or other data source metrics
- Building operational dashboards for SRE teams and incident responders
- Establishing executive-level reporting dashboards for SLO compliance
- Migrating dashboards from manual creation to version-controlled provisioning
- Standardizing dashboard layouts across teams with template variables
- Creating drill-down experiences from high-level overviews to detailed metrics

## Inputs

- **Required**: Data source configuration (Prometheus, Loki, Tempo, etc.)
- **Required**: Metrics or logs to visualize with their query patterns
- **Optional**: Template variables for multi-service or multi-environment views
- **Optional**: Existing dashboard JSON for migration or modification
- **Optional**: Annotation queries for event correlation (deployments, incidents)

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Design Dashboard Structure

Plan dashboard layout and organization before building panels.

Create a dashboard specification document:

```markdown
# Service Overview Dashboard

## Purpose
Real-time operational view for on-call engineers monitoring the API service.

## Rows
1. High-Level Metrics (collapsed by default)
   - Request rate, error rate, latency (RED metrics)
   - Service uptime, instance count
2. Detailed Metrics (expanded by default)
   - Per-endpoint latency breakdown
   - Error rate by status code
   - Database connection pool status
3. Resource Utilization
   - CPU, memory, disk usage per instance
   - Network I/O rates
4. Logs (collapsed by default)
   - Recent errors from Loki
   - Alert firing history

## Variables
- `environment`: production, staging, development
- `instance`: all instances or specific instance selection
- `interval`: aggregation window (5m, 15m, 1h)

## Annotations
- Deployment events from CI/CD system
- Alert firing/resolving events
```

Key design principles:
- **Most important metrics first**: Critical metrics at the top, details below
- **Consistent time ranges**: Synchronize time across all panels
- **Drill-down paths**: Link from high-level to detailed dashboards
- **Responsive layout**: Use rows and panel widths that work on various screens

**Expected:** Clear dashboard structure documented, stakeholders aligned on metrics and layout priorities.

**On failure:**
- Conduct dashboard design review with end users (SREs, developers)
- Benchmark against industry standards (USE method, RED method, Four Golden Signals)
- Review existing dashboards in team for consistency patterns

### Step 2: Create Dashboard with Template Variables

Build the dashboard foundation with reusable variables for filtering.

Create dashboard JSON structure (or use UI, then export):

```json
{
  "dashboard": {
    "title": "API Service Overview",
    "uid": "api-service-overview",
    "version": 1,
    "timezone": "browser",
    "editable": true,
    "graphTooltip": 1,
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "refresh": "30s",
    "templating": {
      "list": [
        {
          "name": "environment",
          "type": "query",
          "datasource": "Prometheus",
          "query": "label_values(up{job=\"api-service\"}, environment)",
          "multi": false,
          "includeAll": false,
          "refresh": 1,
          "sort": 1,
          "current": {
            "selected": false,
            "text": "production",
            "value": "production"
          }
        },
        {
          "name": "instance",
          "type": "query",
          "datasource": "Prometheus",
          "query": "label_values(up{job=\"api-service\",environment=\"$environment\"}, instance)",
          "multi": true,
          "includeAll": true,
          "refresh": 1,
          "allValue": ".*",
          "current": {
            "selected": true,
            "text": "All",
            "value": "$__all"
          }
        },
        {
          "name": "interval",
          "type": "interval",
          "options": [
            {"text": "1m", "value": "1m"},
            {"text": "5m", "value": "5m"},
            {"text": "15m", "value": "15m"},
            {"text": "1h", "value": "1h"}
          ],
          "current": {
            "text": "5m",
            "value": "5m"
          },
          "auto": false
        }
      ]
    },
    "annotations": {
      "list": [
        {
          "name": "Deployments",
          "datasource": "Prometheus",
          "enable": true,
          "expr": "changes(app_version{job=\"api-service\",environment=\"$environment\"}[5m]) > 0",
          "step": "60s",
          "iconColor": "rgba(0, 211, 255, 1)",
          "tagKeys": "version"
        }
      ]
    }
  }
}
```

Variable types and use cases:
- **Query variables**: Dynamic lists from data source (`label_values()`, `query_result()`)
- **Interval variables**: Aggregation windows for queries
- **Custom variables**: Static lists for non-metric selections
- **Constant variables**: Shared values across panels (data source names, thresholds)
- **Text box variables**: Free-form input for filtering

**Expected:** Variables populate correctly from data source, cascading filters work (environment filters instances), default selections appropriate.

**On failure:**
- Test variable queries independently in Prometheus UI
- Check for circular dependencies (variable A depends on B depends on A)
- Verify regex patterns in `allValue` field for multi-select variables
- Review variable refresh settings (on dashboard load vs on time range change)

### Step 3: Build Visualization Panels

Create panels for each metric with appropriate visualization types.

**Time series panel** (request rate):

```json
{
  "type": "timeseries",
  "title": "Request Rate",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{job=\"api-service\",environment=\"$environment\",instance=~\"$instance\"}[$interval])) by (method)",
      "legendFormat": "{{method}}",
      "refId": "A"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "color": {
        "mode": "palette-classic"
      },
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "smooth",
        "fillOpacity": 10,
        "spanNulls": true
      },
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": null, "color": "green"},
          {"value": 1000, "color": "yellow"},
          {"value": 5000, "color": "red"}
        ]
      }
    }
  },
  "options": {
    "tooltip": {
      "mode": "multi",
      "sort": "desc"
    },
    "legend": {
      "displayMode": "table",
      "placement": "right",
      "calcs": ["mean", "max", "last"]
    }
  }
}
```

**Stat panel** (error rate):

```json
{
  "type": "stat",
  "title": "Error Rate",
  "gridPos": {"h": 4, "w": 6, "x": 12, "y": 0},
  "targets": [
    {
# ... (see EXAMPLES.md for complete configuration)
```

**Heatmap panel** (latency distribution):

```json
{
  "type": "heatmap",
  "title": "Request Duration Heatmap",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
  "targets": [
    {
# ... (see EXAMPLES.md for complete configuration)
```

Panel selection guide:
- **Time series**: Trends over time (rates, counts, durations)
- **Stat**: Single current value with threshold coloring
- **Gauge**: Percentage values (CPU, memory, disk usage)
- **Bar gauge**: Comparing multiple values at a point in time
- **Heatmap**: Distribution of values over time (latency percentiles)
- **Table**: Detailed breakdown of multiple metrics
- **Logs**: Raw log lines from Loki with filtering

**Expected:** Panels render correctly with data, visualizations match intended metric types, legends descriptive, thresholds highlight problems.

**On failure:**
- Test queries in Explore view with same time range and variables
- Check for metric name typos or incorrect label filters
- Verify aggregation functions match metric type (rate for counters, avg for gauges)
- Review unit configurations (bytes, seconds, requests per second)
- Enable "Show query inspector" to debug empty results

### Step 4: Configure Rows and Layout

Organize panels into collapsible rows for logical grouping.

```json
{
  "panels": [
    {
      "type": "row",
      "title": "High-Level Metrics",
      "collapsed": false,
# ... (see EXAMPLES.md for complete configuration)
```

Layout best practices:
- Grid is 24 units wide, each panel specifies `w` (width) and `h` (height)
- Use rows to group related panels, collapse less critical sections by default
- Place most critical metrics in first visible area (y=0-8)
- Maintain consistent panel heights within rows (typically 4, 8, or 12 units)
- Use full width (24) for time series, half width (12) for comparisons

**Expected:** Dashboard layout organized logically, rows collapse/expand correctly, panels align visually without gaps.

**On failure:**
- Validate gridPos coordinates don't overlap
- Check that row panels array contains panels (not null)
- Verify y-coordinates increment logically down the page
- Use Grafana UI "Edit JSON" to inspect grid positions

### Step 5: Add Links and Drill-Downs

Create navigation paths between related dashboards.

Dashboard-level links in JSON:

```json
{
  "links": [
    {
      "title": "Service Details",
      "type": "link",
      "icon": "external link",
# ... (see EXAMPLES.md for complete configuration)
```

Panel-level data links:

```json
{
  "fieldConfig": {
    "defaults": {
      "links": [
        {
          "title": "View Logs for ${__field.labels.instance}",
# ... (see EXAMPLES.md for complete configuration)
```

Link variables:
- `$service`, `$environment`: Dashboard template variables
- `${__field.labels.instance}`: Label value from clicked data point
- `${__from}`, `${__to}`: Current dashboard time range
- `$__url_time_range`: Encoded time range for URL

**Expected:** Clicking panel elements or dashboard links navigates to related views with context preserved (time range, variables).

**On failure:**
- URL encode special characters in query parameters
- Test links with various variable selections (All vs specific value)
- Verify target dashboard UIDs exist and are accessible
- Check that `includeVars` and `keepTime` flags work as expected

### Step 6: Set Up Dashboard Provisioning

Version control dashboards as code for reproducible deployments.

Create provisioning directory structure:

```bash
mkdir -p /etc/grafana/provisioning/{dashboards,datasources}
```

Datasource provisioning (`/etc/grafana/provisioning/datasources/prometheus.yml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
# ... (see EXAMPLES.md for complete configuration)
```

Dashboard provisioning (`/etc/grafana/provisioning/dashboards/default.yml`):

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'Services'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

Store dashboard JSON files in `/var/lib/grafana/dashboards/`:

```bash
/var/lib/grafana/dashboards/
├── api-service/
│   ├── overview.json
│   └── details.json
├── database/
│   └── postgres.json
└── infrastructure/
    ├── nodes.json
    └── kubernetes.json
```

Using Docker Compose:

```yaml
version: '3.8'
services:
  grafana:
    image: grafana/grafana:10.2.0
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
```

**Expected:** Dashboards automatically loaded on Grafana startup, changes to JSON files reflected after update interval, version control tracks dashboard changes.

**On failure:**
- Check Grafana logs: `docker logs grafana | grep -i provisioning`
- Verify JSON syntax: `python -m json.tool dashboard.json`
- Ensure file permissions allow Grafana to read: `chmod 644 *.json`
- Test with `allowUiUpdates: false` to prevent UI modifications
- Validate provisioning config: `curl http://localhost:3000/api/admin/provisioning/dashboards/reload -X POST -H "Authorization: Bearer $GRAFANA_API_KEY"`

## Validation

- [ ] Dashboard loads without errors in Grafana UI
- [ ] All template variables populate with expected values
- [ ] Variable cascading works (selecting environment filters instances)
- [ ] Panels display data for configured time ranges
- [ ] Panel queries use variables correctly (no hardcoded values)
- [ ] Thresholds highlight problem states appropriately
- [ ] Legend formatting descriptive and not cluttered
- [ ] Annotations appear for relevant events
- [ ] Links navigate to correct dashboards with context preserved
- [ ] Dashboard provisioned from JSON file (version controlled)
- [ ] Responsive layout works on different screen sizes
- [ ] Tooltip and hover interactions provide useful context

## Common Pitfalls

- **Variable not updating panels**: Ensure queries use `$variable` syntax, not hardcoded values. Check variable refresh settings.
- **Empty panels with correct query**: Verify time range includes data points. Check scrape interval vs aggregation window (5m rate needs >5m of data).
- **Legend too verbose**: Use `legendFormat` to show only relevant labels, not full metric name. Example: `{{method}} - {{status}}` instead of default.
- **Inconsistent time ranges**: Set dashboard time sync so all panels share the same time window. Use "Sync cursor" for correlated investigation.
- **Performance issues**: Avoid queries returning high cardinality series (>1000). Use recording rules or pre-aggregation. Limit time ranges for expensive queries.
- **Dashboard drift**: Without provisioning, manual UI changes create version control conflicts. Use `allowUiUpdates: false` in production.
- **Missing data links**: Data links require exact label names. Use `${__field.labels.labelname}` carefully, verify label exists in query result.
- **Annotation overload**: Too many annotations clutter the view. Filter annotations by importance or use separate annotation tracks.

## Related Skills

- `setup-prometheus-monitoring` - Configure Prometheus data sources that feed Grafana dashboards
- `configure-log-aggregation` - Set up Loki for log panel queries and log-based annotations
- `define-slo-sli-sla` - Visualize SLO compliance and error budgets with Grafana stat and gauge panels
- `instrument-distributed-tracing` - Add trace ID links from metrics panels to Tempo trace views
