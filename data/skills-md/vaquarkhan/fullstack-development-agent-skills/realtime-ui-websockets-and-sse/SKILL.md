---
name: realtime-ui-websockets-and-sse
description: Build reliable realtime UI using WebSockets, SSE, and fallback polling with reconnect and backpressure strategies.
disable-model-invocation: true
---

# Realtime Ui Websockets And Sse

## Use When

- Live dashboards, notifications, or collaboration features
- Users expect near-real-time updates

## Workflow

1. Choose transport by directionality and browser support
2. Define reconnect, heartbeat, and backoff policy
3. Implement server-side fan-out and rate limits
4. Handle stale state and conflict resolution rules
5. Load test connection churn and burst traffic

## Required Checks

- Reconnect behavior is deterministic
- Auth validated on connection and messages
- Backpressure prevents memory exhaustion
- Degraded mode exists when realtime path fails

## Decision Framework

- Prefer SSE for server-to-client streams when bidirectional not required
- Use WebSockets when low-latency bidirectional needed
- Avoid unbounded in-memory fan-out per instance
- Provide polling fallback for critical data

## Common Rationalizations And Rebuttals

- "Realtime can be added without server changes." -> Connection auth and scale need backend design.
- "No heartbeat needed." -> Dead connections accumulate silently.
- "Broadcast everything to all users." -> Privacy and cost issues follow.

## Evidence Pack

- Reconnect storm test results
- Auth failure test evidence
- Latency and drop-rate metrics under load
- Fallback UX validation notes

## Exit Criteria

- Realtime features remain usable under network instability
- Operational limits and alerts are defined
