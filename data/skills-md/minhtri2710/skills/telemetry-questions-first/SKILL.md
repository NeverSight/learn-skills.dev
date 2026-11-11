---
name: telemetry-questions-first
description: Instrument a code path starting from the questions on-call will ask, map each log, metric, and span to one of them, and prove the telemetry works by diagnosing an induced failure from it alone. Use when adding logging, metrics, or tracing to a new endpoint, worker, job, or external call, or when an incident showed the existing signals could not answer what happened. Do not use for alert routing, paging policy, or dashboards without a question behind them.
---

# Telemetry Questions First

Telemetry without a question is noise that costs money to store. Before adding a
line of instrumentation, write down two to four questions an on-call engineer will
ask about this path ("is the export failing, for whom, and at which step?"), and
map every signal to one of them. Metrics say *that* something is wrong, traces
say *where*, logs say *why*; a question matched to the wrong signal type gets an
answer that arrives too late or too vague.

## Logs say why

- Structured, with stable event names, never free-form strings.
- Every line carries a correlation id created or accepted at the boundary and
  propagated on every outbound call and async hop; a stream written by more than
  one entry point (scheduler, replay, manual run) also carries the entry point.
- Levels mean something: `error` is a broken invariant someone may act on,
  `warn` is degraded but handled, `info` is a significant business event,
  `debug` is off outside development.
- Fields are allowlisted. No bodies, no auth headers, no secrets, no unredacted
  personal data; external calls log endpoint, status, latency, attempt count, and
  sanitized identifiers only.

## Metrics say that

- Rate, errors, and duration for every endpoint and every external dependency;
  utilization, saturation, and errors for every queue, pool, and host.
- Latency is a histogram with p50, p95, and p99 queryable, never an average.
- Labels come from small fixed sets: route template, status class (`5xx`, not
  `503`), provider name. Never a user id, tenant id, email, raw URL, request id,
  or error message text as a label; each one is an unbounded series and a bill.

## Traces say where

- Context propagates on every outbound call in the standard headers and is
  extracted from every inbound request; queue messages carry it across the
  async boundary.
- Manual spans only around meaningful units of work, carrying the attributes
  on-call will filter by, and no secrets or personal data.

## Prove the telemetry

Instrumentation is code and can be wrong. Before the work is done:

1. Force an error and find it in the logs by correlation id.
2. Send test traffic and see the series appear with the expected labels and sane
   values.
3. Follow one request end to end in the tracing view with no broken span.
4. Induce a failure and diagnose it from the telemetry alone, without reading the
   source. If that needs the code, the on-call questions are not yet answered.
