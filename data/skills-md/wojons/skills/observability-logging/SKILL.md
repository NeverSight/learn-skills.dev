---
name: observability-logging
description: Use logs as part of comprehensive observability strategy including metrics, traces, alerts, and dashboards for system understanding and operational excellence
license: MIT
compatibility: opencode
metadata:
  audience: SREs, DevOps engineers, platform engineers
  category: observability
---

# Observability Logging

Use logs as a core component of comprehensive observability strategy, integrating with metrics, traces, alerts, and dashboards to achieve deep system understanding and operational excellence.

## When to use me

Use this skill when:
- Building comprehensive observability platforms
- Integrating logs with metrics and tracing for full observability
- Designing alerting and monitoring systems based on log patterns
- Creating dashboards that combine log-derived insights with other telemetry
- Implementing SLO/SLA monitoring using log data
- Building incident response workflows based on log analysis
- Establishing operational excellence practices
- Designing on-call procedures and runbooks
- Implementing predictive maintenance using log patterns
- Building self-healing systems based on observability signals

## What I do

### 1. Log-Driven Metrics
- **Extract metrics from logs** (error rates, latency percentiles, throughput)
- **Create derived metrics** from log patterns and correlations
- **Implement log-based counters** for business and operational events
- **Calculate Service Level Indicators (SLIs)** from log data
- **Monitor Service Level Objectives (SLOs)** using log-derived metrics
- **Implement burn rate alerts** for error budget consumption
- **Create trend analysis** from historical log patterns

### 2. Log-Enhanced Tracing
- **Enrich traces with log context** for deeper insights
- **Correlate trace spans with log events** for complete request understanding
- **Implement log-based span creation** for legacy or untraced systems
- **Use logs to fill tracing gaps** in distributed systems
- **Create unified observability views** combining logs and traces
- **Implement log-to-trace linking** for seamless investigation
- **Use trace context in logs** for correlation and analysis

### 3. Alerting & Monitoring
- **Design log-based alerts** for critical patterns and anomalies
- **Implement alert deduplication** and correlation across log sources
- **Create escalation policies** based on log pattern severity
- **Design alert routing** to appropriate teams and individuals
- **Implement alert enrichment** with log context for faster diagnosis
- **Create suppression rules** for known issues and maintenance windows
- **Monitor alert effectiveness** and adjust thresholds based on historical data

### 4. Dashboard & Visualization
- **Create operational dashboards** combining logs, metrics, and traces
- **Design service health dashboards** with log-derived health indicators
- **Implement real-time log streaming** visualizations
- **Create trend dashboards** showing log pattern evolution
- **Design incident investigation dashboards** with correlated data
- **Implement customizable views** for different stakeholder needs
- **Create predictive dashboards** using machine learning on log data

### 5. Incident Response
- **Design log-driven runbooks** for common issues
- **Implement automated remediation** based on log patterns
- **Create incident timelines** from log correlation
- **Design post-mortem analysis** using comprehensive log data
- **Implement blameless retrospectives** with observability data
- **Create knowledge bases** from resolved incidents and log patterns
- **Design escalation procedures** based on observability signals

## Observability Pillars Integration

### Logs + Metrics + Traces = Full Observability

#### Example: API Service Observability
```
Logs (What happened):
- "API call to /api/users failed with 500 error"
- "Database connection timeout after 5000ms"
- "Cache miss for user:123"

Metrics (How much/how often):
- Error rate: 5.2%
- P95 latency: 245ms
- Throughput: 1,234 requests/second

Traces (Where in the flow):
- Request flow: API Gateway → Auth Service → User Service → Database
- Time spent: 45ms in Auth, 120ms in User Service, 80ms in Database
- Bottleneck identified: Database query in User Service
```

### Unified Data Model
```yaml
observability_data:
  logs:
    source: application, infrastructure, audit
    format: structured (JSON)
    fields: [timestamp, level, service, message, context]
    
  metrics:
    source: logs (derived), application (direct), infrastructure
    types: counter, gauge, histogram, summary
    dimensions: [service, endpoint, status_code, user_type]
    
  traces:
    source: instrumentation, log-derived
    context: trace_id, span_id, parent_span_id
    attributes: [service.name, operation.name, duration, status]
    
  correlations:
    log_to_metric: "error logs → error rate metric"
    log_to_trace: "trace_id field links logs to traces"
    metric_to_trace: "high latency metric → trace analysis"
```

## Log-Driven SLO Monitoring

### Error Budget Calculation from Logs
```python
def calculate_error_budget_from_logs(logs, slo_target, time_window):
    """
    Calculate error budget consumption from log data
    
    Args:
        logs: List of log entries with timestamp and success status
        slo_target: SLO target (e.g., 0.999 for 99.9%)
        time_window: Time window for calculation in seconds
    
    Returns:
        error_budget_consumption: Percentage of error budget consumed
    """
    total_requests = len(logs)
    successful_requests = sum(1 for log in logs if log.get('status') != 'error')
    
    success_rate = successful_requests / total_requests if total_requests > 0 else 1.0
    error_rate = 1.0 - success_rate
    
    # Calculate error budget consumption
    allowed_errors = (1.0 - slo_target) * total_requests
    actual_errors = total_requests - successful_requests
    error_budget_consumption = actual_errors / allowed_errors if allowed_errors > 0 else float('inf')
    
    return {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'success_rate': success_rate,
        'error_rate': error_rate,
        'slo_target': slo_target,
        'allowed_errors': allowed_errors,
        'actual_errors': actual_errors,
        'error_budget_consumption': error_budget_consumption,
        'error_budget_remaining': max(0, 1.0 - error_budget_consumption)
    }
```

### Burn Rate Alerting
```yaml
alerting:
  error_budget_burn_rate:
    # Alert when burning error budget too quickly
    - name: "high_error_budget_burn_rate"
      condition: "error_budget_burn_rate > 10"
      # Burning 10x faster than allowed
      window: "1h"
      severity: "critical"
    
    - name: "medium_error_budget_burn_rate"
      condition: "error_budget_burn_rate > 2"
      # Burning 2x faster than allowed
      window: "6h"
      severity: "warning"
    
  slo_violation:
    - name: "slo_violation_imminent"
      condition: "error_budget_remaining < 0.1"
      # Less than 10% error budget remaining
      window: "7d"
      severity: "warning"
    
    - name: "slo_violation_occurred"
      condition: "success_rate < slo_target"
      # Actual violation occurring
      window: "1h"
      severity: "critical"
```

## Examples

```bash
# Extract metrics from logs for SLO monitoring
npm run observability:extract-metrics -- --slo-target 0.999 --window 7d --output slo-metrics.json

# Create unified observability dashboard
npm run observability:create-dashboard -- --services "api,auth,db" --data-sources "logs,metrics,traces"

# Design log-based alerting rules
npm run observability:design-alerts -- --patterns "error_rate > 5%,latency_p95 > 1000ms" --escalation-policy "team-rotation"

# Implement incident response workflow
npm run observability:incident-workflow -- --trigger "error_spike" --actions "page,create-incident,notify-slack"

# Correlate logs with metrics and traces
npm run observability:correlate -- --time-range "last-1h" --output correlation-analysis.json
```

## Output format

### Observability Platform Configuration:
```yaml
observability:
  data_sources:
    logs:
      collection: [filebeat, fluentd, otel-collector]
      processing: [parsing, enrichment, correlation]
      storage: [elasticsearch, s3]
      
    metrics:
      collection: [prometheus, otel-collector]
      processing: [aggregation, derivation]
      storage: [prometheus, thanos]
      
    traces:
      collection: [otel-collector, jaeger-agent]
      processing: [sampling, enrichment]
      storage: [jaeger, tempo]
  
  correlation:
    fields:
      trace_id: ["trace_id", "trace.id", "X-Trace-Id"]
      service: ["service", "service.name", "component"]
      user_id: ["user_id", "user.id", "userId"]
    
    rules:
      - when: "log.level == 'ERROR'"
        then: "increment_metric('errors_total', labels=log.labels)"
      - when: "trace.duration > 1000"
        then: "log.warning('slow_trace', trace_attributes)"
      - when: "metric.name == 'error_rate' and metric.value > 0.05"
        then: "create_alert('high_error_rate', severity='warning')"
  
  dashboards:
    - name: "Service Health"
      panels:
        - type: "timeseries"
          title: "Error Rate"
          query: "rate(error_logs_total[5m])"
        - type: "histogram"
          title: "Request Latency"
          query: "histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))"
        - type: "log_stream"
          title: "Recent Errors"
          query: "level:ERROR"
    
    - name: "Business Metrics"
      panels:
        - type: "counter"
          title: "User Signups"
          query: "log.message:'User signed up'"
        - type: "timeseries"
          title: "Payment Success Rate"
          query: "successful_payments / total_payments"
  
  alerting:
    rules:
      - alert: "HighErrorRate"
        expr: "rate(error_logs_total[5m]) > 0.05"
        for: "5m"
        labels:
          severity: "critical"
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} which is above 5% threshold"
        
      - alert: "SLOErrorBudgetBurn"
        expr: "error_budget_burn_rate > 10"
        for: "1h"
        labels:
          severity: "warning"
        annotations:
          summary: "Error budget burning too fast"
          description: "Error budget burn rate is {{ $value }}x faster than allowed"
  
  incident_response:
    workflows:
      - trigger: "alert.severity == 'critical'"
        actions:
          - "create_incident"
          - "page_on_call"
          - "notify_slack('#alerts')"
          - "start_zoom_war_room"
      
      - trigger: "incident.created"
        actions:
          - "gather_observability_data"
          - "correlate_logs_metrics_traces"
          - "suggest_runbooks"
          - "update_status_page"
```

### Observability Maturity Assessment:
```
Observability Maturity Assessment
────────────────────────────────
Organization: Example Corp
Assessment Date: 2026-02-26
Overall Score: 72/100

Pillar Scores:
- Logging: 85/100 (Structured, correlated, well-managed)
- Metrics: 65/100 (Basic metrics, limited derivation)
- Tracing: 56/100 (Partial implementation, gaps in coverage)
- Alerting: 70/100 (Effective but could be smarter)
- Visualization: 74/100 (Good dashboards, could be more unified)

Integration Assessment:
✅ Logs include trace context (trace_id, span_id)
✅ Metrics derived from logs (error rates, throughput)
⚠️  Traces not fully correlated with logs (60% coverage)
⚠️  Alerting not using derived SLO metrics
✅ Dashboards combine multiple data sources

Gap Analysis:
1. Missing: Unified observability data model
2. Missing: Automated correlation across pillars
3. Missing: Predictive analytics on observability data
4. Missing: Self-healing based on observability signals
5. Missing: Comprehensive SLO monitoring

Observability ROI Analysis:
- Current MTTR (Mean Time To Resolution): 45 minutes
- Target MTTR with improved observability: 15 minutes
- Estimated reduction in incident impact: $15,000/month
- Estimated improvement in developer productivity: 20%
- Estimated reduction in on-call burden: 30%

Recommendations:
1. HIGH PRIORITY: Implement unified observability data model
2. HIGH PRIORITY: Improve trace coverage and correlation
3. MEDIUM PRIORITY: Implement SLO-based alerting
4. MEDIUM PRIORITY: Add predictive analytics capabilities
5. LOW PRIORITY: Explore self-healing automation

Implementation Roadmap:
- Phase 1 (1 month): Unified data model and correlation
- Phase 2 (2 months): SLO monitoring and alerting
- Phase 3 (3 months): Predictive analytics
- Phase 4 (6 months): Self-healing capabilities
- Ongoing: Continuous improvement and optimization
```

## Notes

- **Observability is a journey, not a destination** - continuous improvement is essential
- **Start with the questions you need to answer** - design observability around those
- **Correlation across data sources is more valuable than individual source depth**
- **Consider the cost of observability** - balance value with expense
- **Involve all stakeholders** - developers, operators, business teams, executives
- **Measure observability effectiveness** - track MTTR, incident frequency, etc.
- **Document observability practices** - runbooks, dashboards, alert definitions
- **Regularly review and refine** - observability needs evolve with the system
- **Balance automation with human insight** - don't automate away necessary human judgment
- **Security and compliance considerations** - observability data may contain sensitive information