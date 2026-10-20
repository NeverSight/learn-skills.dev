---
name: authlete-dcr
description: >-
  Add Dynamic Client Registration + management (RFC 7591 / 7592) to an Authlete-based OAuth/OIDC server.
  Use when a developer wants self-service client registration, a registration endpoint, or clients that
  register themselves (e.g. MCP clients). Works with the authlete-oauth-server base skill.
---

# Add Dynamic Client Registration to your Authlete server

**What this adds:** a `/api/register` endpoint where clients register themselves and get a `client_id`
(and, for confidential clients, a `client_secret`). Plus the management routes to read, update, and
delete a registration. This is RFC 7591 (register) and RFC 7592 (manage).

## How it works (the short version)

All four routes are thin: read the body, forward it to Authlete, relay the response. **Authlete** checks
the metadata, issues the credentials, and keeps all client state. **You** hold nothing. And unlike PAR,
there's **no extra service configuration** — the registration endpoint is advertised automatically.

## The four routes

Each reads the JSON body (and the bearer token, when present) and forwards to Authlete:

| Route | What it's for | Success |
|---|---|---|
| `POST /api/register` | register a new client (RFC 7591) | **201** + metadata |
| `GET /api/register/:id` | read the current registration (RFC 7592) | **200** |
| `PUT /api/register/:id` | update the registration | **200** |
| `DELETE /api/register/:id` | delete the registration | **204**, no body |

For GET/PUT/DELETE, the bearer token is the **registration access token** that was handed back at
registration time. A bad token → **401**. Invalid metadata on register → **400** `invalid_client_metadata`.

Return Authlete's response body as-is — it already contains `client_id`, `client_secret` (confidential
clients), `registration_access_token`, and `registration_client_uri`.

In TypeScript: `authlete.dynamicClientRegistration.{register,get,update,delete}(...)`.

## Open vs. protected registration

Whether a caller needs an initial access token to register is an **Authlete service setting**, not your
code. Your server always forwards the bearer token and lets Authlete accept or reject it.

## What you don't build

Metadata validation, credential issuance, the registration access token, and all client state —
Authlete owns every bit of it.

## Verify it works

Run [`conformance/spec.md`](conformance/spec.md). Quick smoke test:

```bash
curl -X POST "$BASE/api/register" -H 'Content-Type: application/json' \
  -d '{"client_name":"demo","redirect_uris":["https://example.org/cb"],"grant_types":["authorization_code"],"response_types":["code"],"token_endpoint_auth_method":"client_secret_basic"}'
# → 201  {"client_id":"...","client_secret":"...","registration_access_token":"...","registration_client_uri":"..."}
```
