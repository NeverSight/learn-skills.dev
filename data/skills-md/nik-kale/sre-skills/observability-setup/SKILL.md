---
name: observability-setup
description: Guide for implementing metrics, logs, and traces in applications. Use when setting up monitoring, adding instrumentation, configuring dashboards, implementing distributed tracing, or designing alerts and SLOs.
---

# Observability Setup

Comprehensive guide to implementing the three pillars of observability.

## When to Use This Skill

- Setting up monitoring for a new service
- Adding metrics instrumentation
- Implementing structured logging
- Setting up distributed tracing
- Designing dashboards
- Configuring alerts

## The Three Pillars

| Pillar      | What It Answers                 | Tools                           |
| ----------- | ------------------------------- | ------------------------------- |
| **Metrics** | What is happening? (aggregated) | Prometheus, Datadog, CloudWatch |
| **Logs**    | What happened? (detailed)       | ELK, Loki, CloudWatch Logs      |
| **Traces**  | How did it happen? (flow)       | Jaeger, Zipkin, X-Ray           |

## Metrics

### Essential Metrics (Minimum Viable Observability)

Every service needs these metrics:

#### RED Method (Request-driven services)

```
Rate:    requests_total (counter)
Errors:  requests_failed_total (counter)
Duration: request_duration_seconds (histogram)
```

#### USE Method (Resources)

```
Utilization: resource_usage_percent (gauge)
Saturation:  queue_depth (gauge)
Errors:      resource_errors_total (counter)
```

### Metric Types

| Type      | Use For                           | Example                        |
| --------- | --------------------------------- | ------------------------------ |
| Counter   | Cumulative values (only increase) | requests_total, errors_total   |
| Gauge     | Values that go up and down        | connections_active, queue_size |
| Histogram | Distribution of values            | request_duration_seconds       |
| Summary   | Pre-calculated percentiles        | response_time (p50, p99)       |

### Prometheus Instrumentation

**Python**:

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

# Use in request handler
@app.route('/api/users')
def get_users():
    with REQUEST_LATENCY.labels(method='GET', endpoint='/api/users').time():
        result = fetch_users()
        REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status='200').inc()
        return result
```

**Go**:

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    requestCount = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    requestLatency = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request latency",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)
```

### Metric Naming Conventions

```
# Format: namespace_subsystem_name_unit

# Good
http_requests_total
http_request_duration_seconds
db_connections_active
cache_hits_total

# Bad
requests          # Missing namespace
httpRequestsTotal # Wrong format (use snake_case)
latency           # Missing unit
```

### Dashboard Design

Essential panels for service dashboard:

```
Service Dashboard Layout:

Row 1: Overview
- Request Rate (requests/sec)
- Error Rate (%)
- Latency p50, p95, p99

Row 2: Resources
- CPU Usage
- Memory Usage
- Goroutines/Threads

Row 3: Dependencies
- Database latency
- Cache hit rate
- External API latency

Row 4: Business Metrics
- Active users
- Transactions/min
- Revenue (if applicable)
```

---

## Logging

### Structured Logging

Always use structured (JSON) logs:

**Bad**:

```
User login failed for user123 at 2024-01-15 10:30:00
```

**Good**:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "warn",
  "message": "User login failed",
  "user_id": "user123",
  "reason": "invalid_password",
  "ip_address": "192.168.1.1",
  "trace_id": "abc123def456",
  "service": "auth-service"
}
```

### Log Levels

| Level | Use For                      | Example                    |
| ----- | ---------------------------- | -------------------------- |
| ERROR | Failures requiring attention | Database connection failed |
| WARN  | Potential issues             | High memory usage          |
| INFO  | Normal operations            | Request processed          |
| DEBUG | Development details          | Query parameters           |

### Essential Log Fields

```
Required Fields:
- timestamp     ISO 8601 format
- level         error/warn/info/debug
- message       Human-readable description
- service       Service name
- trace_id      Correlation ID

Contextual Fields:
- user_id       If user context available
- request_id    Per-request identifier
- endpoint      API endpoint
- method        HTTP method
- duration_ms   Request duration
- status_code   HTTP status
```

### Python Logging Setup

```python
import structlog
import logging

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage
logger.info("request_processed",
    endpoint="/api/users",
    method="GET",
    duration_ms=45,
    status_code=200,
    trace_id=request.trace_id
)
```

---

## Distributed Tracing

### Key Concepts

```
Trace: End-to-end request journey
  └── Span: Single operation within trace
       ├── Operation name
       ├── Start/end time
       ├── Tags (key-value metadata)
       ├── Logs (timestamped events)
       └── Parent span ID (for nesting)
```

### OpenTelemetry Setup

**Python**:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Create spans
with tracer.start_as_current_span("process_order") as span:
    span.set_attribute("order_id", order_id)
    span.set_attribute("user_id", user_id)

    # Nested span
    with tracer.start_as_current_span("validate_inventory"):
        check_inventory(order)

    with tracer.start_as_current_span("charge_payment"):
        process_payment(order)
```

### What to Instrument

```
Must Trace:
- [ ] HTTP server (incoming requests)
- [ ] HTTP client (outgoing requests)
- [ ] Database queries
- [ ] Cache operations
- [ ] Message queue operations

Should Trace:
- [ ] External API calls
- [ ] File operations
- [ ] Business-critical operations
- [ ] Long-running tasks
```

### Context Propagation

Ensure trace context flows across services:

```
HTTP Headers for Propagation:
- traceparent: 00-<trace-id>-<span-id>-<flags>
- tracestate: vendor-specific data

Example:
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
```

---

## Alerting

### Alert Design Principles

1. **Alert on symptoms, not causes**
   - Good: "Error rate > 1%"
   - Bad: "CPU > 80%"

2. **Every alert must be actionable**
   - Link to runbook
   - Clear remediation steps

3. **Use SLO-based alerting**
   - Alert on error budget burn rate
   - Multi-window burn rate for severity

### Alert Template

```yaml
alert: ServiceHighErrorRate
expr: |
  (
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m]))
  ) > 0.01
for: 5m
labels:
  severity: critical
  team: platform
annotations:
  summary: 'High error rate on {{ $labels.service }}'
  description: 'Error rate is {{ $value | humanizePercentage }}'
  runbook: 'https://wiki/runbooks/high-error-rate'
  dashboard: 'https://grafana/d/service-health'
```

### Alert Severity Levels

| Severity | Response                   | Example                             |
| -------- | -------------------------- | ----------------------------------- |
| critical | Page immediately           | Service down, data loss risk        |
| warning  | Page during business hours | Elevated errors, approaching limits |
| info     | Create ticket              | Anomaly detected, non-urgent        |

---

## Quick Implementation Checklist

```
Observability Checklist:

Metrics:
- [ ] RED metrics exposed (Rate, Errors, Duration)
- [ ] Resource metrics (CPU, memory, connections)
- [ ] Custom business metrics
- [ ] Prometheus endpoint at /metrics

Logging:
- [ ] Structured JSON logging
- [ ] Trace ID in all logs
- [ ] Appropriate log levels
- [ ] No sensitive data logged

Tracing:
- [ ] OpenTelemetry SDK added
- [ ] HTTP server/client instrumented
- [ ] Database calls traced
- [ ] Context propagation configured

Dashboards:
- [ ] Service health dashboard
- [ ] Key metrics visualized
- [ ] Historical data (30 days min)

Alerting:
- [ ] SLO-based alerts configured
- [ ] Runbooks linked to alerts
- [ ] Alert routing to on-call
```

## Additional Resources

- [Metrics Design Guide](references/metrics-guide.md)
- [Alert Examples](references/alert-examples.md)
