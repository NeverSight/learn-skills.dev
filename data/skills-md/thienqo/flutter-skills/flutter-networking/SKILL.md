---
name: flutter-networking
description: Build or review Flutter remote data and transport boundaries across HTTP, GraphQL, WebSocket, SSE, or Socket.IO. Use for API contracts, authenticated request transport, pagination, retries, reconnection, caching, and error mapping; route sign-in and session semantics to flutter-authentication and local storage ownership to flutter-persistence.
---

# Flutter Networking

Keep transport concerns at the service boundary and expose domain-meaningful results to the rest of the app.

## Select the mode

- Handle ordinary HTTP request-response work with the rules below.
- For GraphQL operations, generated models, normalized caches, optimistic writes, or subscriptions, read [GraphQL clients](references/graphql.md).
- For WebSocket, SSE, Socket.IO, connection recovery, or live event delivery, read [Realtime transports](references/realtime-transports.md).
- For REST or HTTP response debugging, undocumented fields, decoding drift, or comparing Swagger/OpenAPI with deployed behavior, read [HTTP response evidence](references/http-response-evidence.md).
- Read both references for GraphQL subscriptions. Route stream races or subscription leaks to `dart-concurrency`, durable offline queues to `flutter-persistence`, and terminated-app alerts to `flutter-notifications`.

## Inspect

Read current client, generated API code, interceptors, model generation, authentication, environment configuration, and tests. Preserve `http`, Dio, generated clients, or another established choice when it meets the requirement.

## Rules

- Centralize base URLs, headers, timeouts, and environment selection without committing secrets.
- Decode untrusted responses and messages defensively and distinguish transport, protocol, decoding, authentication, and domain failures.
- Map wire models to domain models at an explicit boundary.
- Retry or reconnect only when the operation and protocol make recovery safe; bound backoff, queues, and cancellation.
- Refresh credentials through one coordinated path to avoid request storms.
- Define pagination identity, ordering, duplicate handling, terminal conditions, and refresh behavior.
- Apply cache policy deliberately; do not silently return stale data as fresh.
- Avoid logging tokens, personal data, or full sensitive payloads.
- Keep documented schema, documentation examples, controlled fixtures, and observed server responses as separate evidence. Do not present one observed payload as the complete contract or a mock as proof of deployed behavior.

## Verification

Use deterministic fake servers or mock transports to cover success, malformed data, timeouts, cancellation, unauthorized refresh, retry exhaustion, pagination boundaries, reconnect and resume behavior, and offline behavior. Run integration tests against a real service only when credentials and environment are explicitly in scope. Report the execution surface and data source separately.

## Sources

- [Flutter networking](https://docs.flutter.dev/data-and-backend/networking)
- [JSON serialization](https://docs.flutter.dev/data-and-backend/serialization/json)
