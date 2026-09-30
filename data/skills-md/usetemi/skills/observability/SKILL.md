---
name: observability
description: >-
  Opinionated judgment for instrumentation, logging, tracing, alerting, and
  production feedback. Use when deciding what telemetry to capture, designing
  a log record or event vocabulary, choosing operation boundaries, evaluating
  sampling and aggregation, designing alerts or service objectives, choosing
  or adding a telemetry tool, investigating a production outcome, or when a
  change adds or alters an operation whose outcome matters in production,
  even if nobody asked for telemetry.
---
# Observability

**The goal is explainability. The evidence needed to explain a production
outcome exists, and a fresh investigator can find it.** The investigator did not
write the code. Without the author's memory and without reading the source, they
must establish three things: what happened, whom it affected, and what separated
the failed work from the work that succeeded. Load `references/vocabulary.md`
when you define an SLI or SLO, or choose among metrics, records, and traces.

## Every record is structured

**Use the project's existing logger; do not add a second one.** If there is
none, use the language's standard structured logger, writing JSON to stdout or
stderr. **Never write an unstructured log line**: interpolated values are data
thrown away. A record has a literal event name, typed fields, a time, and a
severity. **Fix each field's meaning, type, and unit across the codebase.**

`result` is one of `succeeded`, `failed`, `skipped`, `retried`, `degraded`,
`unknown`. A **reason code** comes from a closed list declared in one place:
`payment.failure.reason_code: card_declined`. Often the domain's event names are
that list, so the domain event names the cause. Scope field names:
`payment.result`.

**Bind context to a logger object as the request evolves**: the request or job
id first, the user id after authentication, the operation id when the operation
starts. Later records carry them; never repeat them per call site.

## Preserve the operation

**Instrument the owner of a unit of work** (a request, a job, or a durable
business operation), not every wrapper it passes through. A **terminal record**
is the last record an operation writes before it exits, with its outcome,
duration, and reason code. **Write one on every exit path, including a throw**:
a missing path is where the question lands.

**Unknown is its own outcome**: a side effect that timed out is `unknown`. Check
the downstream state before retrying, or risk a duplicate. Write one record per
attempt, with its attempt number, plus one terminal record for the whole
operation. Long-running work emits progress records at a fixed interval, so slow
and dead runs differ.

Add what automatic instrumentation cannot: the decision, the state, the caller's
outcome. Carry the **operation id** (request or job id) across calls, queues,
and retries through the existing context propagation; invent no new one.

## Make the evidence countable

A count is a filter plus a group-by, never a parse. Ask the question first: "How
many sends fell back to fax last week, by cause?" names the event, filter, and
group-by. **Batch counts sum to the total**, so zero means idle work and a
mismatch means a bug. **Log every run of a scheduled sweep, including empty
runs**, or an empty sweep looks stopped.

## Severity is an alert decision

| Level | Use |
| --- | --- |
| `debug` | Diagnostic detail. Off in production; on for an investigation. |
| `info` | A decision taken, an outcome, an audit fact. |
| `warn` | A recovered or expected failure, or a threshold reached. |
| `error` | Unexpected terminal failure, exhausted recovery, broken invariant. |

`error` spends a person's attention now, so it alerts. **Every uncaught
exception reaches an alert.** A catch rethrows or writes the terminal record. If
unhandled errors reach no alert yet, add that path in the same change, emitting
an `error` record.

**Alert per event name, not per stack trace**: one wrapper's stack mixes
unrelated failures. The alert, log record, and any Slack post for one event come
from one emit call, not from separate calls in business logic.

## Choose tools by the question

**Metrics count; events explain.** Ids and URLs go in the record, not metric
labels. **The terminal record is primary; a trace is secondary.** Put the trace
id on the record to reach the trace. **Correlation is a contract.** Propagated
ids, not a shared backend, connect records; missing ids are a defect.

## The pipeline is code too

This applies when the project owns a shipper, collector, or transform. **A drop
or a prune writes a payload-free record saying so and how much.** **A transform
that errors drops the record**, so an unredacted payload cannot leak, and a
scheduled heartbeat record that stops arriving is an alert.

## Measure what was promised

**Derive the SLI from terminal records of the promised outcome**, like a
delivered message, not HTTP status or CPU, which look healthy during failed
journeys.

## Bound the cost

**Record opaque ids and reason codes, never personal, clinical, or secret
content.** Truncating, hashing, or redacting a forbidden value still records it;
a downstream scrubber is a backstop, not the rule. **Cap record size at the
source**, pruning in a fixed order that keeps the event name, result, reason
code, and ids.

## Close the feedback loop

**Ship instrumentation in the same change as the behavior**, with a test per
exit path asserting exactly one terminal record. After release, run the record's
question in production and confirm a hit; if you cannot, say so in the PR.
Missing evidence is design feedback, fixed in code. Never infer a missing
record: say it is absent.
