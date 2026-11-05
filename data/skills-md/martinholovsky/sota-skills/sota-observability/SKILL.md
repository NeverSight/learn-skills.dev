---
name: sota-observability
description: >-
  State-of-the-art observability and reliability engineering (2026). Use when
  instrumenting code (structured logging, metrics, distributed tracing with
  OpenTelemetry, SLOs, alerting, health endpoints) or auditing an existing
  codebase's observability posture (can on-call answer "why is this request
  slow?" and "what broke at 3am?"). Not for security detections, SIEM, or
  threat hunting — use sota-detection-engineering. Triggers: logging, metrics, tracing,
  monitoring, alerting, SLO, SLI, error budget, OpenTelemetry, OTel,
  Prometheus, Grafana, debugging production, incident, on-call, telemetry,
  instrumentation, health check, runbook, Sentry, crash reporting, profiling.
---

# SOTA Observability & Reliability

## Purpose

Make every production system answerable. Two questions define success:

1. **"Why is this request slow/failing?"** — answerable for any single request
   from a trace ID, without adding new instrumentation.
2. **"What broke at 3am?"** — answerable from symptom-based alerts that page
   only when users are hurt, each linked to a runbook and a dashboard that
   narrows cause in minutes.

This skill covers structured logging, metrics, distributed tracing, SLOs and
alerting, and operational readiness — both how to **build** them correctly and
how to **audit** them adversarially. Telemetry is a product with users
(on-call engineers) and costs (storage, cardinality, attention). Treat both.

## BUILD mode

When writing or modifying code, apply the rules files as design constraints,
not afterthoughts. Workflow:

1. **Identify the signal need before coding.** For each new endpoint, job, or
   consumer: which SLI does it affect, what one wide event describes a unit of
   work, what spans bound its external calls.
2. **Instrument with OpenTelemetry API** (not vendor SDKs) in libraries;
   configure SDK/exporters only at the application entry point. Follow OTel
   semantic conventions for names and attributes.
3. **Emit one canonical wide event per request/job** at completion, carrying
   trace_id, outcome, durations, and business context. Debug logs are
   supplementary, sampled, and disposable.
4. **Propagate context everywhere**: W3C `traceparent` over HTTP, injected
   into queue message headers, restored in consumers and scheduled jobs.
5. **Redact at the logger**, never at call sites. Denylist+allowlist
   serializers for PII/secrets; fail closed on unknown object dumps.
6. **Budget cardinality.** Every metric label must have a known, bounded
   value set. No IDs, no URLs, no user input in labels.
7. **Ship the operational surface with the feature**: health endpoints with
   correct liveness/readiness semantics, dashboard panels answering the
   questions the feature raises, burn-rate alerts wired to the SLO, runbook
   entry for each new alert.
8. **Verify by simulation**: kill a dependency, send a slow request, trigger
   an error — confirm the trace, the wide event, the metric, and the alert
   all show it, and that they cross-link (exemplars, trace_id in logs).

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

Assess an existing codebase/deployment. Read [`rules/06`](rules/06-audit-playbook.md) first for the full
playbook; sample real code paths, do not trust README claims.

**Severity conventions:**

| Severity | Meaning | Examples |
|----------|---------|----------|
| CRITICAL | Blind during incidents, or telemetry is itself a hazard | Secrets/PII in logs; no error visibility at all; liveness check hits the database (restart storms); unauthenticated debug endpoints that return memory, env or config (profiles alone: HIGH, rules/05 §3) |
| HIGH | Materially slows MTTR or breaks at scale | No correlation/trace IDs; unbounded label cardinality; cause-based paging alerts with no runbooks; readiness == liveness; percentiles averaged across instances |
| MEDIUM | Degrades signal quality or cost discipline | Wrong log levels (ERROR for expected events); no exemplars; head-only sampling losing all error traces; dashboards as vanity walls; no log sampling on hot paths |
| LOW | Hygiene and polish | Inconsistent field names; missing OTel semantic conventions; unpinned dashboard queries; noisy Sentry grouping |

**Finding format** (one per finding):

```
[SEVERITY] <short title>
Where: <file:line, config path, or dashboard/alert name>
Evidence: <exact code/config snippet or observed behavior>
Impact: <what fails during an incident or at scale, concretely>
Fix: <specific change, with code/config if short>
Effort: <S/M/L>
```

Conclude every audit with the two-question verdict: can on-call currently
answer "why is this request slow?" and "what broke at 3am?" — YES/PARTIAL/NO,
with the shortest path to YES.

## Rules index

| File | Read this when... |
|------|-------------------|
| [`rules/01-structured-logging.md`](rules/01-structured-logging.md) | Writing or reviewing log statements, choosing levels, designing wide events/canonical log lines, configuring redaction, sampling, controlling log spend, clock sync and event-vs-receive time, log-level governance, protecting the log store (read auditing, file placement, authenticated transport), or hardening the logging path against flooding and sink failure |
| [`rules/02-metrics.md`](rules/02-metrics.md) | Adding Prometheus/OTel metrics, choosing counter vs gauge vs histogram, designing labels, computing percentiles, applying RED/USE, linking metrics to traces via exemplars |
| [`rules/03-tracing.md`](rules/03-tracing.md) | Instrumenting with OpenTelemetry, deciding what gets a span, propagating context across HTTP/queues/jobs, choosing head vs tail sampling, using (or avoiding) baggage |
| [`rules/04-slos-alerting.md`](rules/04-slos-alerting.md) | Defining SLIs/SLOs, error budgets, writing burn-rate alerts, reviewing alert quality, fighting alert fatigue, deciding page vs ticket |
| [`rules/05-operational-readiness.md`](rules/05-operational-readiness.md) | Implementing health endpoints, exposing graceful degradation, securing debug endpoints, continuous profiling, Sentry-style error tracking, shutdown and crash telemetry (the last 10 seconds), synthetic monitoring, building dashboards, **edge access logs as a decision-grade signal**, keeping test-written telemetry out of the sink production writes — and the question with no instrument, where a proxy measurement silently answers a different one |
| [`rules/06-audit-playbook.md`](rules/06-audit-playbook.md) | Auditing a codebase's observability posture end-to-end; common gaps catalog; scoring and reporting |

## Top 10 non-negotiables

1. **Every log line carries a trace/correlation ID.** A log you cannot join
   to a request is gossip, not evidence.
2. **ERROR means a human must act.** If nobody should be woken or ticketed,
   it is WARN or below. Level discipline is alert discipline upstream.
3. **No secrets or PII in telemetry — enforced at the logger/exporter**, not
   by call-site vigilance. Redaction is infrastructure, not convention.
4. **One wide event per unit of work** (request/job/message) with outcome,
   duration, and business context — the canonical log line you grep at 3am.
5. **Metric labels are bounded.** No user IDs, emails, raw URLs, or free
   text. Cardinality explosions take down the monitoring you need most.
6. **Never average percentiles.** Aggregate histograms, then compute
   quantiles. A dashboard of avg(p99) is fiction.
7. **OpenTelemetry API in libraries, SDK only at the edge.** W3C
   `traceparent` propagated across every HTTP hop, queue, and async job.
8. **Liveness checks process health only; readiness checks dependencies.**
   Conflating them turns one slow dependency into a cluster-wide restart storm.
9. **Every page is actionable, symptom-based, and runbook-linked.** Alert on
   user pain (SLO burn rate, multi-window), not on causes (CPU, pod restarts).
10. **Telemetry has a budget.** Sample debug logs and traces deliberately
    (tail-sample to keep errors/slow), review cost monthly, delete signals
    nobody queries.
