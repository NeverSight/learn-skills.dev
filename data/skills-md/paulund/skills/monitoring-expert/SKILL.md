---
name: monitoring-expert
description: Use when setting up monitoring solutions, logging, metrics, tracing, and alerting for applications and infrastructure.
---

# Monitoring Expert

## Core Workflow

1. **Analysis**: Understand the monitoring requirements for the application or infrastructure.
2. **Design**: Design a monitoring solution that includes logging, metrics, tracing, and alerting.
3. **Implementation**: Implement the monitoring solution using appropriate tools and technologies.
4. **Configuration**: Configure dashboards and alerts for effective monitoring.
5. **Optimization**: Continuously optimize the monitoring solution for performance and reliability.
6. **Alerting**: Set up alerting mechanisms to notify relevant stakeholders of potential issues.

## Reference Guide

Load the detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Alerting Rules | `references/alerting-rules.md` | When configuring alerting systems |
| Capacity Planning | `references/capacity-planning.md` | When planning for resource growth or scaling |
| Dashboards | `references/dashboards.md` | When building or reviewing monitoring dashboards |
| OpenTelemetry | `references/opentelemetry.md` | When implementing distributed tracing or OTel instrumentation |
| Performance Testing | `references/performance-testing.md` | When load testing or benchmarking systems |
| Prometheus Metrics | `references/prometheus-metrics.md` | When defining or querying Prometheus metrics |
| Structured Logging | `references/structured-logging.md` | When implementing application logging |

## Constraints

### MUST DO

- Use structured JSON logging for better log management.
- Include request IDs in logs for traceability.
- Collect key performance metrics such as latency, error rates, and throughput.
- Set up alerts for critical paths.
- Use appropriate metrics aggregation methods (e.g., rate, histogram) based on the metric type.
- Implement healthcheck endpoints for services to monitor their availability.

### MUST NOT DO

- Avoid logging sensitive information such as passwords or personal data.
- Do not set up alerts for non-critical issues that can lead to alert fatigue.
- Avoid using default configurations without customization for the specific application or infrastructure.
- Do not ignore monitoring data when troubleshooting issues.
- Avoid over-instrumentation that can lead to performance overhead.
