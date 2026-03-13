---
name: nestjs-lgtm-metrics
description: Add application-level Prometheus metrics to a NestJS app using the OpenTelemetry SDK and an OTel Collector. Covers HTTP RED metrics, Node.js runtime metrics, business metrics, and advanced observability patterns. Use this skill whenever the user wants to add metrics, dashboards, or monitoring to a NestJS application, mentions Prometheus, Grafana metrics, OpenTelemetry metrics, OTel Collector, or asks about SLIs/SLOs, or application-level monitoring in a NestJS context. Also trigger when the user wants custom counters, histograms, gauges, or summaries in NestJS. This skill focuses exclusively on metrics the APPLICATION must emit. It does not cover logging, tracing, infra-level metrics from cAdvisor, node-exporter, postgres-exporter, or redis-exporter.
---

# NestJS Application Metrics via OpenTelemetry

## What This Skill Covers

This skill adds **application-level metrics** to a NestJS app using the **OpenTelemetry SDK**, pushing them through an **OTel Collector** into **Prometheus**. It is organized in progressive stages, from foundational to advanced.

**Scope boundary**: This skill covers metrics only. Not logging, not tracing. Infrastructure metrics (container resources, host stats, database server stats, Redis server stats) come from their respective exporters and community Grafana dashboards. This skill covers what those exporters **cannot see**: request-level behavior, business events, runtime internals, and domain-specific KPIs as observed from inside your application.

## Prerequisites

- NestJS application
- OpenTelemetry Collector running and reachable from the app
- Prometheus configured as an export target from the Collector
- Grafana connected to Prometheus as a data source

## Architecture

```
NestJS App (OTel SDK) ──OTLP/gRPC──▶ OTel Collector ──remote_write──▶ Prometheus ──▶ Grafana
```

The app never exposes a `/metrics` endpoint. It pushes metrics to the Collector via OTLP. The Collector handles export to Prometheus (via `prometheusremotewrite` exporter or a Prometheus scrape on the Collector itself).

Read `references/otel-setup.md` before writing any application metric code. It covers the SDK bootstrap, Collector pipeline config, and how to verify the pipeline is working end to end.

## Implementation Stages

Each stage builds on the previous. Read the corresponding reference file for full implementation code.

---

### Stage 1: Foundation (Day 1, any app)

> **Read**: `references/stage-1-foundation.md`

Non-negotiable. Every NestJS app in production needs these from the start.

**What you get:**

1. **HTTP RED metrics** (Rate, Errors, Duration) via a global interceptor
   - `http_request_duration_seconds` histogram, labeled by method, route, status_code
   - `http_requests_total` counter, labeled by method, route, status_code
   - `http_requests_in_flight` up/down counter
2. **Node.js runtime metrics** (what V8/libuv expose that no infra exporter can see)
   - `nodejs_eventloop_lag_seconds` histogram (not just mean. percentiles matter)
   - `nodejs_active_handles_total` observable gauge
   - `nodejs_active_requests_total` observable gauge
   - GC duration, heap size, external memory via `@opentelemetry/host-metrics`
3. **Health and readiness probe metrics**
   - `app_health_check_duration_seconds` histogram by check_name
   - `app_health_check_status` gauge (1=healthy, 0=unhealthy) by check_name

**Why these first**: HTTP RED gives you the ability to detect problems. Runtime metrics tell you whether the Node.js process itself is degraded. Health checks close the loop with your orchestrator. Together they answer: "Is the app working? How fast? For whom is it failing?"

**Histogram bucket strategy**: Use explicit bucket boundaries initially: `[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]`. Tune after you have real traffic data. Do not over-bucket. More buckets = more time series = more Prometheus storage cost.

---

### Stage 2: Application Intelligence (Week 1-2, pre-launch)

> **Read**: `references/stage-2-app-intelligence.md`

These metrics expose application behavior that sits between raw HTTP and business logic.

**What you get:**

1. **Database query metrics from the app's perspective**
   - `app_db_query_duration_seconds` histogram by operation (select, insert, update, delete), entity
   - `app_db_query_errors_total` counter by operation, error_type
   - `app_db_connection_pool_wait_seconds` histogram
   - Why this matters: postgres-exporter sees server-side query time. Your app sees ORM overhead + pool wait + serialization + network. The gap between these two is where bugs hide.

2. **Redis operation metrics from the app's perspective**
   - `app_redis_operation_duration_seconds` histogram by operation (get, set, del, etc.), key_prefix
   - `app_redis_operation_errors_total` counter
   - `app_cache_hit_total` / `app_cache_miss_total` counters by cache_name
   - Why this matters: redis-exporter sees `keyspace_hits/misses` globally. Your app knows WHICH cache strategy worked and which didn't.

3. **External API call metrics**
   - `app_external_api_duration_seconds` histogram by service, endpoint, status_code
   - `app_external_api_errors_total` counter by service, error_type
   - `app_circuit_breaker_state` gauge (0=closed, 0.5=half-open, 1=open) by service

4. **Authentication and authorization metrics**
   - `app_auth_attempts_total` counter by method (password, oauth, api_key), result (success, failure, locked)
   - `app_auth_token_operations_total` counter by operation (issue, refresh, revoke, expire)
   - `app_authorization_denied_total` counter by resource, action

5. **Background job / queue metrics** (Bull, BullMQ, or similar)
   - `app_job_duration_seconds` histogram by queue, job_type
   - `app_job_completed_total` counter by queue, job_type, status (completed, failed, stalled)
   - `app_job_queue_depth` gauge by queue
   - `app_job_attempts_total` counter by queue, job_type (tracks retry behavior)

---

### Stage 3: Business Metrics (Launch, real users)

> **Read**: `references/stage-3-business-metrics.md`

Once users arrive, technical metrics aren't enough. You need to observe the business through the same system.

**What you get:**

1. **User lifecycle events**
   - `app_user_signups_total` counter by source, plan
   - `app_user_logins_total` counter by method
   - `app_user_actions_total` counter by action_type (generic, high-cardinality-safe pattern)

2. **Transaction / conversion metrics**
   - `app_transactions_total` counter by type, status
   - `app_transaction_value_total` counter (sum of monetary values) by currency
   - `app_conversion_funnel_step_total` counter by funnel, step

3. **Feature usage metrics**
   - `app_feature_usage_total` counter by feature_name, variant (useful for A/B tests)
   - `app_feature_errors_total` counter by feature_name

4. **SLI metrics for SLO tracking**
   - `app_sli_request_availability` counter (successful requests / total requests, partitioned)
   - `app_sli_request_latency` histogram (tighter buckets around your SLO threshold)

**Cardinality warning**: Business metrics are where cardinality explosions happen. Never use user_id, session_id, or any unbounded value as an attribute. Use bucketed categories. Read the cardinality section in `references/stage-3-business-metrics.md`.

---

### Stage 4: Advanced Patterns (Scaled app, mature team)

> **Read**: `references/stage-4-advanced.md`

For apps serving real traffic at scale, handling complex flows, or needing tight operational control.

**What you get:**

1. **WebSocket / real-time connection metrics**
   - `app_ws_connections_active` gauge by namespace
   - `app_ws_messages_total` counter by namespace, direction (in/out), event_type
   - `app_ws_connection_duration_seconds` histogram

2. **Rate limiter observability**
   - `app_rate_limit_hits_total` counter by limiter, route
   - `app_rate_limit_remaining` gauge by limiter (sampled, not per-request)

3. **Multi-tenant metrics**
   - `app_tenant_requests_total` counter by tenant_tier (not tenant_id. cardinality.)
   - `app_tenant_resource_usage` gauge by tenant_tier, resource_type

4. **Graceful shutdown and lifecycle**
   - `app_shutdown_duration_seconds` histogram
   - `app_startup_duration_seconds` gauge

5. **Deployment version tracking**
   - `app_info` gauge with version, commit_sha, environment attributes for canary analysis

---

## Grafana Dashboard Templates

Import-ready Grafana dashboard JSON files, one per stage. Each uses `${DS_PROMETHEUS}` as the data source variable, so Grafana will prompt you to select your Prometheus data source on import.

**How to import**: Grafana → Dashboards → New → Import → Upload JSON file → Select your Prometheus data source.

| Template | Panels | Description |
|---|---|---|
| `templates/stage-1-service-overview.json` | 14 | Golden signals (stat), request rate by route, error rate, latency percentiles, P99 by route, event loop lag, heap memory, active handles, health check status and duration. |
| `templates/stage-2-dependency-health.json` | 15 | DB query P95 by operation, pool wait time, DB errors, cache hit ratio by strategy, Redis op latency, Redis errors, external API P95, circuit breaker state, API errors, auth failure rate, token ops, authz denials, queue depth, job duration, job failure rate. |
| `templates/stage-3-business-metrics.json` | 14 | Signups/revenue/success rate big numbers, signups by source, logins by method, revenue rate, transaction failure rate, funnel step totals, feature usage by variant, feature errors, 30-day SLO availability, SLI latency percentiles, error budget burn rate. |
| `templates/stage-4-operational.json` | 10 | Running versions table, startup/shutdown duration, active WS connections, WS message throughput, WS connection duration, rate limit rejections by route, remaining tokens, request volume by tenant tier, resource usage by tier. |

Each dashboard is standalone. Combine panels across dashboards as your needs evolve. All dashboards include `$job` and `$instance` template variables for filtering. Stage 3 additionally includes `$funnel` and `$sli` selectors.

---

## Grafana Dashboard Strategy

Read `references/grafana-dashboards.md` for dashboard panel definitions and provisioning.

**Dashboard hierarchy:**

1. **Service Overview** (Stage 1): RED metrics, runtime health, up/down status. One dashboard per service.
2. **Dependency Health** (Stage 2): DB latency, Redis hit rates, external API status. Shows how your app EXPERIENCES its dependencies.
3. **Business Dashboard** (Stage 3): Conversion funnels, feature adoption, revenue metrics. Non-engineers should be able to read this.
4. **Operational Dashboard** (Stage 4): Rate limits, circuit breakers, tenant resource usage, deployment comparison.

**Alert hierarchy** (pair with dashboards):

- Stage 1: Error rate spike, latency P99 breach, event loop lag > 100ms
- Stage 2: DB query latency drift, cache hit rate drop, external API circuit open
- Stage 3: Conversion rate drop, signup anomaly
- Stage 4: Rate limiter saturation, tenant quota breach

---

## Infrastructure Exporters and Community Dashboards

> **Read**: `references/infra-exporters.md`

Your app metrics (Stages 1-4) show how the application experiences its dependencies. Infrastructure exporters show how those services perform internally. You need both. The gap between them is where most production issues hide.

This reference covers exporter setup (docker-compose), Prometheus scrape config, and community Grafana dashboard IDs for: PostgreSQL, Redis, RabbitMQ, MongoDB, Qdrant, Elasticsearch, Nginx, MinIO, plus node-exporter and cAdvisor for host/container metrics.

Each entry includes the key metrics the exporter provides and, critically, what it does NOT tell you (which your app-level metrics fill).

---

## Common Mistakes to Avoid

1. **High-cardinality attributes**: Never use userId, requestId, IP, or full URL path as a metric attribute. Use route patterns. If you need per-user data, that's a log or trace, not a metric.
2. **Metric name collisions**: Prefix everything with `app_`. Infra exporters use `node_`, `pg_`, `redis_`, `container_`.
3. **Too many buckets**: Every unique attribute combination x every bucket = one time series. 10 routes x 5 methods x 11 buckets = 550 series just for HTTP duration. That's fine. 500 routes x 11 buckets = not fine.
4. **Forgetting the MeterProvider**: If your OTel SDK setup doesn't register a MeterProvider, all `meter.create*` calls silently return no-op instruments. Nothing fails, nothing records. Verify by checking the Collector's own metrics or the Prometheus targets page.
5. **Measuring inside try/catch only**: Always record duration and count in a `finally` block so errors are measured too.
6. **Ignoring pool wait time**: The time your request spends waiting for a DB connection from the pool is invisible to both your query timer and the postgres-exporter. Instrument it separately.

---

## File Reference

| File | When to read |
|---|---|
| `references/otel-setup.md` | Before starting. OTel SDK bootstrap and Collector config. |
| `references/stage-1-foundation.md` | Implementing foundation metrics. Full code. |
| `references/stage-2-app-intelligence.md` | Adding dependency and internal behavior metrics. |
| `references/stage-3-business-metrics.md` | Adding business event tracking and SLIs. |
| `references/stage-4-advanced.md` | WebSockets, rate limiters, multi-tenancy, lifecycle. |
| `references/infra-exporters.md` | Exporter setup for Postgres, Redis, RabbitMQ, MongoDB, Qdrant, Elasticsearch, Nginx, MinIO, node-exporter, cAdvisor. Docker-compose, scrape configs, community dashboard IDs. |
| `references/grafana-dashboards.md` | App dashboard structure, alert rules, provisioning. |
| `templates/stage-1-service-overview.json` | Import into Grafana for HTTP RED, runtime, health check panels. |
| `templates/stage-2-dependency-health.json` | Import into Grafana for DB, Redis, external API, auth, job panels. |
| `templates/stage-3-business-metrics.json` | Import into Grafana for signups, revenue, funnels, SLO panels. |
| `templates/stage-4-operational.json` | Import into Grafana for WebSocket, rate limiter, multi-tenant panels. |
