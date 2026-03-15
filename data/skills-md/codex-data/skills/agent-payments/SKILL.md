---
name: agent-payments
description: >-
  Machine Payment Protocol (MPP) for keyless, pay-per-query access to the Codex
  Supergraph GraphQL API. Use when the user has no API key and wants to pay per
  query via the 402 challenge flow at https://graph.codex.io/graphql.
metadata:
  author: codex-data
  version: "1.0"
---

# Codex Machine Payment Protocol (MPP)

Use this skill to access the Codex Supergraph without an API key via the MPP challenge flow.

|                       |                                                                 |
| --------------------- | --------------------------------------------------------------- |
| HTTP endpoint         | `https://graph.codex.io/graphql`                                |
| Opt-in header         | `X-Codex-Payment: mpp`                                         |
| Credential header     | `Authorization: Payment <base64url-credential>`                 |

## How it works

1. Send a GraphQL query with `X-Codex-Payment: mpp` (no credential).
2. Server returns `402 Payment Required` with `WWW-Authenticate: Payment ...` challenges.
3. Client solves one challenge and retries with `Authorization: Payment <credential>`.
4. Server returns GraphQL data + `Payment-Receipt` header.

## Constraints

- **Query only.** Mutations and subscriptions return `403` in MPP mode.
- If a valid API key or bearer token is also present, API auth takes precedence.
- Do not reference legacy dashboard onboarding/top-up/balance payment endpoints.

## Challenge flow

1. First request (no credential yet):

```bash
curl -i -sS https://graph.codex.io/graphql \
  -H "Content-Type: application/json" \
  -H "X-Codex-Payment: mpp" \
  --data-binary '{"query":"query GetNetworks { getNetworks { id name } }"}'
```

Expected: `402 Payment Required` with multiple `WWW-Authenticate: Payment ...` challenges.

2. Retry with solved credential:

```bash
curl -i -sS https://graph.codex.io/graphql \
  -H "Content-Type: application/json" \
  -H "X-Codex-Payment: mpp" \
  -H "Authorization: Payment <base64url-credential>" \
  --data-binary '{"query":"query GetNetworks { getNetworks { id name } }"}'
```

Expected: GraphQL data + `Payment-Receipt` header.

## Rules

- Never print raw credentials.
- Only use MPP for `query` operations.
- For available GraphQL operations and endpoint selection heuristics, see the `codex-supergraph` skill.

## References

| File | Purpose |
| ---- | ------- |
| [references/mpp-flow.md](references/mpp-flow.md) | Auth matrix, challenge details, error codes |
| [references/mpp-templates.md](references/mpp-templates.md) | MPP curl templates |
| [references/wallets.md](references/wallets.md) | Wallet setup: tempo wallet/request (Tempo) and awal (Base) |
