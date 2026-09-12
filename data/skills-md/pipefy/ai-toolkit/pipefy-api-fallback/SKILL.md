---
name: pipefy-api-fallback
description: >
  Use this skill when an MCP tool fails AND the introspection skill could
  not resolve the problem. This is the last-resort fallback (Tier 3):
  call the Pipefy GraphQL API directly using curl or httpx, authenticating
  with the Service Account (OAuth2) or a Personal Access Token (PAT)
  available as env var. Follow the 3-tier resolution strategy before
  reaching this point.
tags: [pipefy, graphql, api, fallback, troubleshooting, curl]
---

# Pipefy API Fallback (Tier 3 — Last Resort)

This skill activates only after Tiers 1 and 2 have failed. Call the Pipefy GraphQL API directly, bypassing the MCP server.

---

## 3-tier resolution strategy (always follow in order)

| Tier | Method | When |
|------|--------|------|
| **1** | Dedicated MCP tool (`create_card`, `get_phase_cards`, `get_phase_allowed_move_targets`, `update_pipe`, etc.) | Always try first. For card/phase seeding and inventory, see [Seed pipe across phases](../../pipes-and-cards/pipefy-pipes-and-cards/SKILL.md#seed-pipe-across-phases). |
| **2** | Introspection + `execute_graphql` | When no dedicated tool exists or a tool fails unexpectedly. See [skills/introspection/pipefy-introspection/SKILL.md](../../introspection/pipefy-introspection/SKILL.md). |
| **3** | Direct HTTP via curl / httpx (this skill) | When the MCP server itself is unavailable, or `execute_graphql` fails with an infrastructure error. |

**Do not jump to Tier 3 after a single tool failure.** Follow the tiers in order.

---

## Authentication

Two options (use whichever is available in the environment). Prefer the Service Account when both exist.

**Option A — OAuth2 Client Credentials (preferred):**

```bash
TOKEN=$(curl -s -X POST https://app.pipefy.com/oauth/token \
  -H "Content-Type: application/json" \
  -d "{\"grant_type\":\"client_credentials\",\"client_id\":\"$PIPEFY_SERVICE_ACCOUNT_CLIENT_ID\",\"client_secret\":\"$PIPEFY_SERVICE_ACCOUNT_CLIENT_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

**Option B — Personal Access Token (PAT):**

```bash
TOKEN="$PIPEFY_PAT"   # or $PIPEFY_TOKEN
```

PATs are deprecated for new integrations but may still exist in the environment.

### Token rules

- The `Bearer ` prefix is **mandatory** — Pipefy rejects requests without it.
- Never expose `PIPEFY_SERVICE_ACCOUNT_CLIENT_ID`, `PIPEFY_SERVICE_ACCOUNT_CLIENT_SECRET`, `PIPEFY_PAT`, or `PIPEFY_TOKEN` in responses to the user or in logs.
- Service Account tokens are reused while valid; only re-fetch on expiry (401).

---

## Endpoints

| Purpose | URL |
|---------|-----|
| All queries and mutations | `https://api.pipefy.com/graphql` |
| Schema introspection only | `https://app.pipefy.com/graphql` |
| OAuth2 token | `https://app.pipefy.com/oauth/token` |

Real operations go to `api.pipefy.com`; introspection goes to `app.pipefy.com`. The MCP server and CLI route between the two automatically (both derived from `PIPEFY_BASE_URL`); raw-API users must distinguish them by hand.

---

## Execute a GraphQL query

```bash
curl -s -X POST https://api.pipefy.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ me { id name } }"}' | jq .
```

## Execute a GraphQL mutation

```bash
curl -s -X POST https://api.pipefy.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation CreateCard($input: CreateCardInput!) { createCard(input: $input) { card { id } } }",
    "variables": {
      "input": {
        "pipe_id": 67890,
        "title": "Fallback Card"
      }
    }
  }' | jq .
```

---

## When to use direct API vs MCP tools

| Situation | Use |
|-----------|-----|
| MCP server running normally | MCP tools (Tier 1 or 2) |
| MCP server down / unreachable | Direct API (Tier 3) |
| `execute_graphql` returns 500 error | Direct API (Tier 3) |
| Testing a new mutation before MCP tool exists | `execute_graphql` (Tier 2) — not direct API |

---

## Introspection via raw API

When you need to discover schema without MCP tools, call `app.pipefy.com/graphql`:

```bash
# All queries and mutations
curl -s -X POST https://app.pipefy.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { fields { name description } } mutationType { fields { name description } } } }"}'

# Type details
curl -s -X POST https://app.pipefy.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __type(name: \"CreateCardInput\") { inputFields { name description type { name kind ofType { name kind } } } } }"}'
```

---

## Error code → cause

GraphQL always returns HTTP 200, even on errors. Check the `errors` array, not the HTTP status code.

| Code | Likely cause | Recovery |
|-------|--------------|----------|
| UNAUTHORIZED | Token missing, expired, or `Bearer ` omitted | Re-fetch token (Option A) or fix the header. |
| PERMISSION_DENIED | Service Account not a member of this pipe/table | Add SA via `invite_members` or ask user. |
| resource_not_found | ID does not exist or SA cannot see it | Verify ID; check pipe/table membership. |
| invalid_input | Wrong argument name or type | Run `introspect_type` (Tier 2) to recheck the input shape. |
| INTERNAL_SERVER_ERROR | API bug or unsupported payload | **Do NOT retry the same payload.** Try an alternative mutation or workaround. |
| missingRequiredInputObjectAttribute | A required field is missing from the input | Compare the payload against `__type(name: …InputType)`. |
| Ambiguous write failure (`success: false`, empty or unclear message) | Mutation may already have applied (side effects on the server) | **Re-read before any retry** — see [Ambiguous write failure](#ambiguous-write-failure-re-read-before-retry). |

---

## Ambiguous write failure (re-read before retry)

Write tools and `execute_graphql` can report failure even when the mutation already applied. Blind retry duplicates customer data (e.g. many cards created despite `success: false`).

1. **Do not** immediately re-run the same create/mutation.
2. **Re-read** first: `get_cards` / `get_phase_cards_count` / returned ids / `cards_count` on the pipe or phase you targeted. Prefer comparing to a count or id set you recorded **before** the write when available.
3. Retry **only** if the re-read clearly shows the write did not land.
4. If the re-read is **inconclusive** (no pre-write baseline, pagination truncates results, or counts cannot prove absence), **stop** — report the ambiguous failure and the re-read evidence to the user. Do not guess-retry.
5. **Hard stop — no client-side idempotency:** `CreateCardInput` has no `idempotency_key` (only `clientMutationId`, which is not create-idempotency). Do not invent client-side keys or assume retries are safe. Re-read is the only safe path until the API adds real idempotency.

---

## Known workarounds

### Cross-pipe `create_card` via automation
- Do NOT use `createAutomation` with `action: create_card` + `field_map` — returns `INTERNAL_SERVER_ERROR` (confirmed API bug).
- Instead, use `createCard` with the `throughConnectors` parameter. Prerequisite: a connector field with `canCreateNewConnected: true` must exist.

### Pipe listing shorter than `pipesCount`
- `pipesCount` is the org-wide total; `organization { pipes { ... } }` and `search_pipes` return only the pipes the calling identity is a member of. A shorter listing, or an empty one, is expected behavior and not an error. Role does not widen it: a `super_admin` gets the same membership-scoped result. Detail and workarounds: [`docs/mcp/tools/organization.md`](../../../docs/mcp/tools/organization.md#why-counts-disagree).
- `organization { pipes(include_publics: true) }` widens the listing with pipes that are public inside the org. It still normally returns fewer than `pipesCount`.
- Service accounts hit this most often: an SA starts as a member of nothing.
- Pipes created via API are automatically visible to the SA.
- Pipes created in the UI require the SA to be added as an admin.
- Workaround: get pipe IDs from the user once and query `pipe(id: "...")` directly.

### `invite_members` accepts unknown emails silently
- Pipefy mints a new `user_id` for typo addresses without rejecting the invite. Sanity-check email syntax before calling.

---

## External resources (when raw API also fails)

- Pipefy developer portal:
  - https://developers.pipefy.com/reference/cards
  - https://developers.pipefy.com/reference/pipes
  - https://developers.pipefy.com/reference/automation-creation
  - https://developers.pipefy.com/reference/how-to-handle-errors
- API reference:
  - https://api-docs.pipefy.com/reference/mutations/overview/
  - https://api-docs.pipefy.com/reference/queries/overview/
- Community + changelog:
  - https://community.pipefy.com/api-76
  - https://developers.pipefy.com/changelog
- Status page: https://status.pipefy.com

Search for the exact error message + "Pipefy GraphQL", or the mutation name + "example Pipefy API".

---

## Escalation to the user (absolute last resort)

Only after all 3 tiers and external resources have failed:

1. State exactly what was tried (MCP tool, introspection, raw API).
2. Show the verbatim error response.
3. Propose a concrete workaround (e.g., "create via the Pipefy UI, then continue via API with the resulting ID").
4. Stop — do not loop.

---

## Success criteria

- The operation completes without an HTTP 4xx/5xx error.
- The response contains a `data` key and `errors` is null or absent.

## Failure modes

- **401 Unauthorized** — token expired or `Bearer ` prefix omitted. Re-fetch the OAuth token (Option A).
- **400 Bad Request** — GraphQL syntax error. Validate the query string and escape quotes properly when embedding via shell.
- **500 / service unavailable** — Pipefy API outage. Check [status.pipefy.com](https://status.pipefy.com) and retry later. Do not loop.
- **`INTERNAL_SERVER_ERROR` in `errors` array** — do NOT retry the same payload; pick a different mutation path.
- **Ambiguous write failure** — reported error with empty/unclear message after a create or other write: re-read counts/ids before retrying; never blind-retry creates ([Ambiguous write failure](#ambiguous-write-failure-re-read-before-retry)).

## Security notes

- Never log or print tokens in plain text.
- Prefer environment variables over inline credentials.
- Use `PIPEFY_TOKEN` / `PIPEFY_PAT` only for personal/development use; use service-account credentials (`PIPEFY_SERVICE_ACCOUNT_CLIENT_ID` + `PIPEFY_SERVICE_ACCOUNT_CLIENT_SECRET`) for service accounts.

## See also

- [skills/introspection/pipefy-introspection/SKILL.md](../../introspection/pipefy-introspection/SKILL.md) — Tier 2: use `execute_graphql` and introspection tools through the MCP server before falling back to direct HTTP.
