---
name: connect-query
description: Build typed ConnectRPC data flows with Connect Query and Protobuf v2. Use for API calls, mutations, query hooks, transports, invalidation, or generated clients.
paths:
  - "**/*_connectquery*"
  - "**/*_pb*"
  - "**/gen/**"
---

Run `/read-the-damn-docs` before current ConnectRPC/Connect Query/Protobuf API guidance.

## Enforce

- In ConnectRPC files, ban raw TanStack `useQuery`/`useMutation`; use Connect Query, except `useTransport`/`callUnaryMethod`.
- `invalidateQueries()` needs a query key.
- Prefer ConnectRPC transport over `axios`/`fetch`.
- Protobuf v2: `create(Schema)`, not `new Message()`; `MessageShape`/`MessageInitShape`, not `PlainMessage`/`PartialMessage`; no manual `$typeName`.

Escape: `// allow: direct-query [reason]`.

## Query discipline

- Define 2-3 semantic cache constants centrally; `Infinity` only when own invalidation is exclusive. QueryClient owns retry: retry network/5xx, never 4xx.
- Hook `transform`/`select` returns display-ready data and enforces page size; components do not parse.
- Invalidate rather than refetch and always await it. Keys are service/method broad but cardinality-aware.
- Loader and hook use identical query keys; test parity to prevent double fetches.
- One hook per RPC; split multi-RPC pages. Mutation names end `Mutation`, or `WithToast` when owning toasts.
- Client protovalidate checks sent data, not server-validated responses.
- Proto optionals use `undefined`, never `null`; unbounded lists use infinite query/load-more; polling uses `refetchInterval`.

Timestamp, Duration, Any, caches: [REFERENCE.md](REFERENCE.md). Install: [SETUP.md](SETUP.md).
