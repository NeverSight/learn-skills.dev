---
name: mmt-api-best-practices
description: Best practices for building apps with the MMT real-time crypto market data API. Use when building trading bots, dashboards, analytics tools, or any application consuming MMT REST or WebSocket APIs. Covers connection management, rate limiting, data handling, multi-exchange aggregation, and performance optimization.
---

# MMT API Best Practices

Rules for building reliable, performant applications with the MMT market data API.

## Connection Management
- [WebSocket Lifecycle](rules/connection-websocket-lifecycle.md): connect/disconnect flow, heartbeat, connection states, cleanup
- [Authentication](rules/connection-authentication.md): API key via header (REST) vs query param (WS), server-side proxy for browser apps
- [Reconnection Strategy](rules/connection-reconnection-strategy.md): exponential backoff, resubscription, state recovery

## Rate Limiting
- [Weight Management](rules/rate-limit-weight-management.md): weight costs per endpoint, budget allocation, monitoring
- [Tier Awareness](rules/rate-limit-tier-awareness.md): Strict/Standard/Premium limits, feature gating
- [Burst Strategy](rules/rate-limit-burst-strategy.md): burst bucket mechanics, pre-flight checks, graceful degradation

## Data Handling
- [CBOR Optimization](rules/data-cbor-optimization.md): when and how to use CBOR, bandwidth savings, decoding
- [Symbol Normalization](rules/data-symbol-normalization.md): base/quote format, /markets discovery, inverse contracts
- [Timeframe Rules](rules/data-timeframe-rules.md): validation rules, calendar timeframes, UTC alignment
- [Type Handling](rules/data-type-handling.md): public type field maps for all data types

## WebSocket
- [Subscription Management](rules/websocket-subscription-management.md): sub/unsub protocol, limits, deduplication
- [Range Requests](rules/websocket-range-requests.md): historical data via WS, from/to params
- [Channel Selection](rules/websocket-channel-selection.md): channel guide and when to use each

## REST API
- [Endpoint Selection](rules/rest-endpoint-selection.md): endpoint decision tree, parameter reference
- [Caching Strategy](rules/rest-caching-strategy.md): cache /markets, TTLs, ETag patterns
- [Timeframe Alignment](rules/rest-timeframe-alignment.md): UTC boundary alignment, candle close semantics

## Multi-Exchange Aggregation
- [Multi-Exchange Queries](rules/aggregation-multi-exchange.md): colon-separated syntax, supported endpoints
- [Cost Optimization](rules/aggregation-cost-optimization.md): weight multipliers, tier restrictions

## Error Handling
- [Error Patterns](rules/error-handling-patterns.md): error code reference, structured format, recovery
- [Retry Strategy](rules/error-retry-strategy.md): retryable vs non-retryable, backoff, circuit breaker

## Performance
- [Memory & Batching](rules/performance-memory-batching.md): batch fetches, stream processing, avoid unbounded buffers
