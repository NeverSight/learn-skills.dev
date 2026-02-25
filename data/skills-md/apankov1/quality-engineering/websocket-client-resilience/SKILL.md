---
name: websocket-client-resilience
description: "Client-side WebSocket resilience patterns: backoff with jitter, circuit breakers, heartbeat hysteresis, command acknowledgment, sequence gap detection, and mobile-aware timeouts."
---

# WebSocket Client Resilience

6 resilience patterns for WebSocket clients, extracted from real-world mobile network conditions.

Mobile WebSocket connections fail in ways that local development environments don't surface. P99 latency on 4G networks is 5-8 seconds. A 5-second health check timeout causes false positives on every slow network.

**When to use**: Implementing WebSocket client reconnection logic, building real-time features with persistent connections, mobile app WebSocket handling, any client that maintains long-lived server connections.

**When not to use**: Server-side WebSocket handlers, HTTP request/response patterns, Server-Sent Events (SSE).

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Our users are on fast networks" | Mobile users exist. Even desktop WiFi has transient blips. | Test with throttled networks |
| "Simple retry is enough" | Without jitter, all clients retry at once after an outage | Add randomized jitter |
| "One missed heartbeat means disconnected" | Network blips last 1-3 seconds. Single miss = false positive. | Use hysteresis (2+ misses) |
| "We'll add resilience later" | Reconnection logic is foundational. Retrofitting it is much harder. | Build it in from the start |
| "5 seconds is plenty of timeout" | Mobile P99 is 5-8s. That "timeout" is normal latency for mobile. | Use 10s+ for mobile |

---

## Included Utilities

```typescript
// WebSocket resilience pattern implementations (zero dependencies)
import {
  getBackoffDelay,
  circuitBreakerTransition,
  shouldDisconnect,
  CommandAckTracker,
  detectSequenceGap,
  classifyTimeout,
} from './resilience.ts';
```

## Quick Reference

| Pattern | Detect | Fix | Severity |
|---------|--------|-----|----------|
| Backoff without jitter | `Math.pow(2, attempt)` without `Math.random()` | Add +/- 25% jitter | must-fail |
| No circuit breaker | Reconnect without failure counter | Trip after 5 failures, 60s cooldown | must-fail |
| Single heartbeat miss | `setTimeout` disconnect without miss counter | Require 2+ missed heartbeats | should-fail |
| No command ack | `ws.send()` without commandId tracking | Track pending commands, timeout at 30s | nice-to-have |
| No sequence tracking | `onmessage` without sequence check | Track lastReceivedSequence, detect gaps | nice-to-have |
| Short mobile timeout | Health timeout < 10s | Use 10s+ for all health checks | must-fail |

## Coverage

| Pattern | Utility | Status |
|---------|---------|--------|
| 1. Backoff with jitter | `getBackoffDelay()` | Code + tests |
| 2. Circuit breaker | `circuitBreakerTransition()` | Code + tests |
| 3. Heartbeat hysteresis | `shouldDisconnect()` | Code + tests |
| 4. Command acknowledgment | `CommandAckTracker` | Code + tests |
| 5. Sequence gap detection | `detectSequenceGap()` | Code + tests |
| 6. Mobile-aware timeouts | `classifyTimeout()` | Code + tests |

All 6 patterns have executable utilities and tests.

## Framework Adaptation

These patterns are framework-agnostic. They work with:
- **Browser**: Native `WebSocket`, Socket.IO, ws library
- **React/Vue/Svelte**: Wrap in composable/hook
- **React Native / Flutter**: Same patterns, different APIs
- **Node.js**: `ws` library for server-to-server WebSocket clients

The core principle: **real-world network conditions are more variable than controlled environments. Design for mobile latency, not localhost.**

See [patterns.md](./references/patterns.md) for full before/after code examples and detection commands for each pattern.
