---
name: graceful-shutdown-drain
description: >-
  Implement, review, or test graceful shutdown for HTTP servers, worker pools,
  consumers, streaming services, or scheduled jobs. Use whenever the user
  mentions SIGTERM, shutdown, restart, scale-in, draining a queue, or jobs being
  lost during deploy—even if they ask directly for a code change. Determine the
  framework lifecycle and durability guarantees; do not promise that volatile
  queued work survives forced termination.
---

# Graceful shutdown and drain

Treat shutdown as a bounded state transition, not a call to stop the process.
The service should stop receiving new work, finish or safely release work it
already owns, and exit before the orchestrator's termination deadline.

## Map lifecycle and ownership

Inspect how the application receives termination signals, serves health/readiness,
accepts jobs, owns workers/consumers, and closes clients. Identify which work is
waiting, in flight, streaming, leased from a broker, or persisted durably. Follow
the framework's shutdown sequence; do not assume closing the HTTP listener also
stops background consumers.

## Design the shutdown sequence

1. On the termination signal, mark the instance unready and stop accepting new
   requests/jobs. Allow routing/load balancers time to stop sending traffic
   when the platform needs propagation time.
2. Stop or pause message intake and new worker scheduling without discarding
   already accepted work.
3. Drain in-flight work and, if appropriate, queued work within an explicit
   deadline shorter than the platform's hard termination timeout.
4. Propagate cancellation/deadlines to downstream operations; release permits,
   leases, and tenant reservations correctly.
5. Flush/close required clients and exit with a status that reports whether the
   drain completed or timed out.

Do not wait forever for a stuck dependency. If the deadline expires, follow the
delivery guarantee: safely requeue/release a durable message, persist resumable
state, or clearly report that volatile work may be lost. Never claim a local
memory queue survives `SIGKILL`, host loss, or a forced orchestrator stop.

Coordinate the application's drain deadline with systemd, containers, and
orchestrator termination grace periods. Do not modify production timeout values
without understanding the deployment configuration and obtaining approval when
the change has operational impact.

## Test the state transitions

Add tests or a repeatable integration scenario that sends termination while
work is queued and while work is in flight. Verify no new work is accepted after
draining begins, accepted work completes or follows its recovery path, duplicate
processing is safe, the timeout is bounded, and shutdown exits correctly on
both success and timeout. Observe queue depth, in-flight count, drain duration,
and remaining work without logging sensitive payloads.

When the workflow also needs durable retries or recovery, use
`resilient-async-workflows`; for queue limits and overload behavior, use
`backpressure-and-admission-control`.
