---
name: monitoring-observability
description: Observability patterns and monitoring best practices. Use when user asks to "set up monitoring", "structured logging", "distributed tracing", "metrics collection", "observability", "APM setup", "log aggregation", "metrics dashboards", "error tracking", "performance monitoring", or mentions observability stack and monitoring strategy.
---

# Monitoring & Observability

Comprehensive monitoring, observability, and alerting strategies for production systems.

## Three Pillars of Observability

### Metrics
- Quantitative measurements (counters, gauges, histograms)
- Time-series data (Prometheus, InfluxDB, Datadog)
- Examples: request latency, error rate, CPU usage

### Logs
- Structured event records
- Searchable and filterable
- Examples: application logs, access logs, error logs

### Traces
- Request flow through system
- Distributed tracing (Jaeger, Zipkin)
- Shows dependencies and bottlenecks

## Implementation Approaches

### Metrics Collection
```python
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total requests')
latency = Histogram('http_request_duration_seconds', 'Request latency')

@app.route('/api/users')
def get_users():
    request_count.inc()
    with latency.time():
        return fetch_users()
```

### Structured Logging
```json
{
  "timestamp": "2025-02-07T10:30:00Z",
  "level": "ERROR",
  "service": "user-service",
  "request_id": "req_12345",
  "user_id": "user_789",
  "error_code": "DB_CONNECTION_FAILED",
  "message": "Failed to connect to database",
  "duration_ms": 1500
}
```

### Distributed Tracing
- Instrument application code
- Propagate trace IDs across services
- Collect traces centrally (Jaeger, Zipkin)
- Visualize service dependencies

## Popular Tools

| Category | Tools |
|----------|-------|
| Metrics | Prometheus, Grafana, Datadog, New Relic |
| Logging | ELK Stack, Splunk, CloudWatch, Loki |
| Tracing | Jaeger, Zipkin, DataDog APM |
| APM | New Relic, DataDog, Dynatrace |

## Best Practices

1. **Structured Logging** - JSON format with context
2. **Contextual Data** - Request IDs, user IDs, service names
3. **Sampling** - Don't log everything to save costs
4. **Retention Policy** - Balance cost and retention needs
5. **Alerts** - On error rates, latency, resource usage
6. **Dashboards** - Visualize key metrics
7. **Runbooks** - Document how to respond to alerts

## Key Metrics to Monitor

- Request rate and latency (p50, p95, p99)
- Error rate and error types
- Resource usage (CPU, memory, disk)
- Database query performance
- Cache hit rates
- Queue depths
- User session counts

## References

- Prometheus Monitoring Best Practices
- Observability Engineering (O'Reilly)
- Google SRE Book
- ELK Stack Documentation
- OpenTelemetry Project
