---
name: monitoring-setup
description: Adds structured observability to services including health check endpoints (liveness, readiness, startup), metrics collection (latency, error rates, throughput), distributed tracing with correlation IDs, alert threshold configuration with escalation policies, and runbook links. Use when adding monitoring, setting up observability, creating health checks, configuring alerts, or when the user needs production readiness instrumentation.
---

# Monitoring Setup

## Overview

Add production-grade observability to any service by instrumenting health
checks, metrics, tracing, and alerts as a cohesive system. The skill treats
monitoring as structured output — not ad-hoc logging — producing files that
integrate with standard observability stacks (Prometheus, Grafana,
OpenTelemetry, PagerDuty/OpsGenie).

## When to use

- When adding monitoring or observability to a service
- When creating health check endpoints for Kubernetes or load balancers
- When instrumenting metrics (latency, error rates, throughput)
- When setting up distributed tracing across services
- When configuring alert thresholds and escalation policies
- When the user mentions "production readiness", "SLOs", "SLIs", or "runbooks"
- When deploying a service and needing operational instrumentation

**Do NOT use when:**

- The user needs to debug an existing monitoring setup (use
  systematic-debugging)
- The task is configuring a specific vendor dashboard (just follow vendor docs)
- The user needs log aggregation only (logging is not this skill's focus)

## Workflow

### 1. Add health check endpoints

Create three distinct health check endpoints. Each serves a different purpose in
orchestration systems like Kubernetes:

| Endpoint      | Path            | Purpose                            | What to check                                            |
| ------------- | --------------- | ---------------------------------- | -------------------------------------------------------- |
| **Liveness**  | `GET /healthz`  | "Is the process alive?"            | Process is running, not deadlocked. Minimal checks only. |
| **Readiness** | `GET /readyz`   | "Can this instance serve traffic?" | Database connected, cache warm, dependencies reachable.  |
| **Startup**   | `GET /startupz` | "Has initialization completed?"    | Migrations run, config loaded, initial data seeded.      |

**Critical distinction:** Liveness should NEVER check external dependencies. If
your liveness probe checks the database and the DB goes down, Kubernetes will
restart your healthy pods — making an outage worse. Liveness = "is this process
fundamentally broken?" Readiness = "should traffic be routed here?"

**Response format:**

```json
{
  "status": "ok",
  "checks": {
    "database": { "status": "ok", "latency_ms": 2 },
    "cache": { "status": "ok", "latency_ms": 1 },
    "external_api": { "status": "degraded", "latency_ms": 450 }
  },
  "version": "1.2.3",
  "uptime_seconds": 84321
}
```

Return HTTP 200 for healthy, 503 for unhealthy. Include individual check
statuses so operators can see which dependency is failing.

### 2. Instrument metrics collection

Use the RED and USE methods to ensure comprehensive coverage:

**RED method** (for request-driven services):

| Metric       | What to measure              | Prometheus type | Example                                       |
| ------------ | ---------------------------- | --------------- | --------------------------------------------- |
| **Rate**     | Requests per second          | Counter         | `http_requests_total{method, path, status}`   |
| **Errors**   | Failed requests per second   | Counter         | `http_errors_total{method, path, code}`       |
| **Duration** | Request latency distribution | Histogram       | `http_request_duration_seconds{method, path}` |

**USE method** (for resource-driven components):

| Metric          | What to measure               | Prometheus type | Example                      |
| --------------- | ----------------------------- | --------------- | ---------------------------- |
| **Utilization** | % of resource capacity in use | Gauge           | `db_pool_utilization_ratio`  |
| **Saturation**  | Queue depth / backpressure    | Gauge           | `request_queue_length`       |
| **Errors**      | Resource-level error count    | Counter         | `db_connection_errors_total` |

**Implementation requirements:**

- Use Prometheus client library for the service's language
- Expose metrics at `GET /metrics` in Prometheus exposition format
- Use histogram buckets appropriate for the service:
  `[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]` seconds for HTTP
- Label metrics with `method`, `path` (normalized), and `status_code`
- Add a metrics middleware that instruments ALL requests automatically
- Include process metrics (memory, CPU, GC, event loop lag where applicable)

### 3. Add distributed tracing

Implement OpenTelemetry-compatible tracing with correlation ID propagation:

**Trace context propagation:**

- Generate a unique `trace-id` (128-bit hex) for each incoming request without
  one
- Propagate via W3C Trace Context headers: `traceparent`, `tracestate`
- Also support `X-Correlation-ID` / `X-Request-ID` for backward compatibility
- Pass trace context to ALL downstream HTTP calls, message queue publishes, and
  async jobs

**Span creation:**

- Create a root span for each incoming request
- Create child spans for: database queries, external HTTP calls, cache
  operations, message queue operations
- Include span attributes: `http.method`, `http.url`, `http.status_code`,
  `db.system`, `db.statement`
- Set span status to ERROR on failures with error message

**Configuration output** — generate a trace config file:

```javascript
// tracing.js - OpenTelemetry configuration
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { getNodeAutoInstrumentations } = require(
  "@opentelemetry/auto-instrumentations-node",
);
const { OTLPTraceExporter } = require(
  "@opentelemetry/exporter-trace-otlp-http",
);

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ||
      "http://localhost:4318/v1/traces",
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: process.env.OTEL_SERVICE_NAME || "my-service",
});

sdk.start();
```

### 4. Configure alert thresholds

Define alerts based on SLOs (Service Level Objectives), not arbitrary values.
The process:

1. **Define SLOs** — e.g., "99.9% of requests complete in < 500ms"
2. **Derive SLIs** — the metric that measures the SLO (e.g.,
   `http_request_duration_seconds`)
3. **Set burn rate alerts** — alert when you're consuming error budget too fast

**Alert threshold guidelines:**

| SLO Target | Burn Rate 1h | Burn Rate 6h | Burn Rate 24h |
| ---------- | ------------ | ------------ | ------------- |
| 99.9%      | 14.4x        | 6x           | 3x            |
| 99.5%      | 14.4x        | 6x           | 3x            |
| 99.0%      | 14.4x        | 6x           | 3x            |

**Alert rule format** (Prometheus alerting rules):

```yaml
groups:
  - name: slo-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > (1 - 0.999) * 14.4
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Error rate burning through SLO budget at 14.4x"
          description: "Current error rate: {{ $value | humanizePercentage }}"
          runbook: "https://runbooks.example.com/high-error-rate"
          dashboard: "https://grafana.example.com/d/slo-overview"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
          > 0.5
        for: 5m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "P99 latency exceeds 500ms SLO target"
          runbook: "https://runbooks.example.com/high-latency"
```

**Escalation policy:**

| Severity | Response Time | Notification Channel | Escalation After |
| -------- | ------------- | -------------------- | ---------------- |
| critical | 5 minutes     | PagerDuty page       | 15 min to lead   |
| warning  | 30 minutes    | Slack #alerts        | 2 hours to team  |
| info     | Next business | Slack #monitoring    | None             |

Every alert MUST include a `runbook` annotation linking to resolution steps.

### 5. Create runbook templates

Generate a runbook for each alert with this structure:

```markdown
# Runbook: [Alert Name]

## Alert Details

- **Severity:** critical/warning/info
- **SLO:** Which SLO this protects
- **Dashboard:** Link to relevant Grafana dashboard

## Symptoms

What the operator will observe when this fires.

## Diagnosis Steps

1. Check [specific metric/dashboard]
2. Look for [specific log pattern]
3. Verify [specific dependency]

## Resolution

### If caused by [root cause A]

1. Step-by-step fix

### If caused by [root cause B]

1. Step-by-step fix

## Escalation

- If not resolved in [time]: escalate to [team/person]
- If customer-facing: notify [channel]
```

### 6. Generate dashboard configuration

Produce a Grafana dashboard JSON or config covering:

- **Overview row:** Request rate, error rate, latency P50/P95/P99
- **Health row:** Health check status, uptime, version
- **Resources row:** CPU, memory, DB pool utilization, queue depth
- **SLO row:** Error budget remaining, burn rate, SLO compliance

## Checklist

- [ ] Liveness endpoint at `/healthz` — checks process only, NOT dependencies
- [ ] Readiness endpoint at `/readyz` — checks all dependencies with individual
      status
- [ ] Startup endpoint at `/startupz` — checks initialization completion
- [ ] Health responses include status, individual checks, version, uptime
- [ ] Metrics endpoint at `/metrics` in Prometheus exposition format
- [ ] RED metrics: request rate, error rate, duration histogram
- [ ] USE metrics: utilization, saturation, errors for resources
- [ ] Metrics middleware instruments all requests automatically
- [ ] Trace context propagation via W3C headers (traceparent)
- [ ] Correlation ID generated for requests without trace context
- [ ] Child spans for DB queries, HTTP calls, cache, message queues
- [ ] Alert thresholds derived from SLOs, not arbitrary values
- [ ] Every alert has severity, team label, runbook link, and dashboard link
- [ ] Escalation policy defined per severity level
- [ ] Runbook template generated for each alert
- [ ] Dashboard config covers request metrics, health, resources, and SLOs

## Example

**Input:** "Add monitoring to our Express.js order service"

**Output files produced:**

| File              | Contents                                            |
| ----------------- | --------------------------------------------------- |
| `health.js`       | Liveness, readiness, startup route handlers         |
| `metrics.js`      | Prometheus client setup + metrics middleware        |
| `tracing.js`      | OpenTelemetry SDK configuration                     |
| `alert-rules.yml` | Prometheus alerting rules with SLO-based thresholds |
| `runbooks/`       | One markdown file per alert                         |
| `dashboard.json`  | Grafana dashboard configuration                     |

**Example health endpoint implementation:**

```javascript
// health.js
const express = require("express");
const router = express.Router();
const { Pool } = require("pg");

const startTime = Date.now();
let startupComplete = false;

// Liveness - process alive, no dependency checks
router.get("/healthz", (req, res) => {
  res.status(200).json({
    status: "ok",
    uptime_seconds: Math.floor((Date.now() - startTime) / 1000),
  });
});

// Readiness - can serve traffic
router.get("/readyz", async (req, res) => {
  const checks = {};
  let healthy = true;

  // Check database
  try {
    const start = Date.now();
    await pool.query("SELECT 1");
    checks.database = { status: "ok", latency_ms: Date.now() - start };
  } catch (err) {
    checks.database = { status: "error", error: err.message };
    healthy = false;
  }

  // Check Redis
  try {
    const start = Date.now();
    await redis.ping();
    checks.cache = { status: "ok", latency_ms: Date.now() - start };
  } catch (err) {
    checks.cache = { status: "error", error: err.message };
    healthy = false;
  }

  res.status(healthy ? 200 : 503).json({
    status: healthy ? "ok" : "unhealthy",
    checks,
    version: process.env.APP_VERSION || "unknown",
    uptime_seconds: Math.floor((Date.now() - startTime) / 1000),
  });
});

// Startup - initialization complete
router.get("/startupz", (req, res) => {
  res.status(startupComplete ? 200 : 503).json({
    status: startupComplete ? "ok" : "starting",
    uptime_seconds: Math.floor((Date.now() - startTime) / 1000),
  });
});

function markStartupComplete() {
  startupComplete = true;
}

module.exports = { router, markStartupComplete };
```

## Common mistakes

| Mistake                                   | Fix                                                                                                                              |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Liveness checks database/external deps    | Liveness = process health only. Move dependency checks to readiness. DB down + liveness fail = cascading restarts.               |
| Using `console.log` instead of metrics    | Logs are for debugging, metrics are for monitoring. Use counters/histograms for anything you'd alert on.                         |
| Arbitrary alert thresholds ("error > 10") | Derive thresholds from SLOs and burn rates. "10 errors" means nothing without knowing request volume.                            |
| No correlation ID propagation             | Generate trace ID on ingress, propagate to ALL downstream calls. Without this, distributed debugging is impossible.              |
| Missing runbook links on alerts           | Every alert must link to a runbook. An alert without a runbook is just noise that trains operators to ignore alerts.             |
| Single health endpoint for everything     | Separate liveness/readiness/startup. Kubernetes uses them differently; conflating them causes incorrect pod lifecycle decisions. |
| Metrics without labels                    | Always label with method, path, status. Aggregate metrics hide the signal — you need to slice by dimension.                      |
| No histogram buckets for latency          | Use histograms, not averages. P99 latency matters more than mean. Configure buckets for your expected range.                     |

## Quick reference

| Component     | Output file          | Format                         |
| ------------- | -------------------- | ------------------------------ |
| Health checks | `health.{js,ts,py}`  | Express/Fastify/Flask routes   |
| Metrics       | `metrics.{js,ts,py}` | Prometheus client + middleware |
| Tracing       | `tracing.{js,ts,py}` | OpenTelemetry SDK config       |
| Alert rules   | `alert-rules.yml`    | Prometheus alerting rules      |
| Runbooks      | `runbooks/*.md`      | Markdown per alert             |
| Dashboard     | `dashboard.json`     | Grafana dashboard JSON         |

## Key principles

1. **Liveness is sacred** — Never put dependency checks in liveness probes. A
   liveness failure triggers a pod restart. If your DB is down and liveness
   checks the DB, Kubernetes restarts all pods, making recovery harder. Liveness
   answers only: "is this process fundamentally broken?"

2. **SLOs drive alerts** — Every alert threshold must trace back to a Service
   Level Objective. "Error rate > 1%" is meaningless without knowing the SLO.
   Use burn rate alerting: alert when you're consuming error budget faster than
   sustainable.

3. **Metrics over logs** — Anything you would alert on must be a metric, not a
   log line. Metrics are aggregatable, queryable, and cheap. Log-based alerting
   is fragile, expensive, and misses patterns that counters catch naturally.

4. **Trace everything cross-service** — Every request entering the system gets a
   trace ID. Every downstream call propagates it. Without end-to-end tracing,
   debugging distributed systems requires correlating timestamps across log
   streams — which doesn't scale.

5. **Alerts without runbooks are noise** — Every alert must link to a runbook
   with diagnosis steps and resolution procedures. Operators receiving alerts
   without context will either ignore them or waste time investigating from
   scratch. Runbooks encode institutional knowledge.
