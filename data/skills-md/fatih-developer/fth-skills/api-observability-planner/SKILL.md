---
name: api-observability-planner
description: Architects which metrics to collect, how logs should be formatted, and how distributed tracing should be implemented across boundaries.
---

# API Observability Planner Protocol

This skill ensures that when an API goes down, the team knows exactly *why* before the users even notice. It shifts telemetry from "just log the errors" to a structured observability pipeline.

**Core assumption:** If you can't measure it, you can't manage it. Blind APIs cause prolonged outages.

---

## 1. The Three Pillars Strategy (Static)

Define exactly what your framework will emit:
- **Logs (Events):** Structured JSON logging. Never use raw text strings (`"User 123 failed login"` vs `{"event": "login_failed", "user_id": 123, "reason": "bad_password"}`).
- **Metrics (Aggregations):** Implement the RED Method:
  - **Rate:** Requests per second.
  - **Errors:** Failed request rate (4xx vs 5xx).
  - **Duration:** Latency percentiles (p50, p90, p99).
- **Traces (Workflows):** Distributed tracing (`W3C Trace Context`). Ensure `trace_id` and `span_id` propagate across microservices and database calls.

## 2. Health & Alerting Design

Define what constitutes "Healthy" and when pagers should go off.
- **Deep Health Checks:** `/healthz` shouldn't just return `200 OK`. It should verify DB connection, Redis reachability, and critical downstreams.
- **Alert Rules:** 
  - *Warning:* p99 latency > 500ms for 5 minutes.
  - *Critical:* 5xx error rate > 5% for 2 minutes.

## 3. Output Generation

**Required Outputs (Must write BOTH to `docs/api-report/`):**

1. **Human-Readable Markdown (`docs/api-report/api-observability-report.md`)**
```markdown
### 🔭 API Observability Blueprint

**Instrumentation Strategy:** OpenTelemetry (OTel)
**Log Format:** Structured JSON

#### 📊 Core Metrics (RED Method)
1. **Rate:** Tracked via Prometheus `http_requests_total`.
2. **Errors:** Alerting on HTTP 500-599. (4xx are client problems, track but don't wake up on-call).
3. **Duration:** Tracked via `http_request_duration_seconds` (Buckets: 50ms, 100ms, 500ms, 1s, 5s).

#### 🚨 Alert Configuration (PagerDuty / Slack)
- **High Severity:** Order Creation 5xx Rate > 1% over 5m.
- **Low Severity:** Database Disk Space < 20%.

#### 🆔 Tracing Propagation
Inject `traceparent` and `tracestate` headers into all outgoing upstream HTTP/gRPC requests.
```

2. **Machine-Readable JSON (`docs/api-report/api-observability-output.json`)**
```json
{
  "skill": "api-observability-planner",
  "framework": "OpenTelemetry",
  "metrics": {
    "latency_thresholds_ms": {"p95": 200, "p99": 500}
  },
  "alerts": [
    {"name": "High 5xx Rate", "condition": "error_rate > 1%", "duration": "5m", "severity": "High"}
  ]
}
```

---

## Guardrails
- **Log Forging / Injection:** Ensure log sanitization is implemented to prevent multiline log spoofing.
- **PII in Logs:** Explicitly call out that `passwords`, `tokens`, `credit_cards`, and `emails` must be masked or scrubbed before being written to `stdout` or log aggregators.
