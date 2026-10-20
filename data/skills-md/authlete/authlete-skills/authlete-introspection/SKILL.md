---
name: authlete-introspection
description: >-
  Add RFC 7662 token introspection to an Authlete-based OAuth/OIDC server. Use when a developer wants an
  introspection endpoint, or a resource server that needs to check whether an access token is valid and
  read its metadata. Works with the authlete-oauth-server base skill.
---

# Add Token Introspection to your Authlete server

**What this adds:** a `POST /oauth/introspect` endpoint. A resource server sends it a token and gets back
whether the token is active, plus its metadata (scope, subject, expiry, client). This is RFC 7662.

## How it works (the short version)

Pure forward-and-relay. **Authlete** decides whether the token is `active` and returns all its metadata.
**You** authenticate the caller, pass the token along, and return the answer.

## The route — `POST /oauth/introspect`

1. Require the caller to authenticate (per your service's configured method) — **401** if they don't.
2. Read the form body (`token`, and optionally `token_type_hint`) and forward it to Authlete.
3. Return Authlete's response: **200** JSON (or `application/jwt` if configured).

Note: an unknown or expired token is **not an error** — Authlete returns `{ "active": false }` with a
**200**. Only reject (401) when the *caller* isn't authorized.

In TypeScript: `authlete.introspection(...)` (the standard introspection call).

## What you don't build

The `active` decision and all the token metadata — Authlete owns them.

## Verify it works

Run [`conformance/spec.md`](conformance/spec.md). You'll need an access token (shared login driver) and
caller credentials:

```bash
curl -u "$CLIENT_ID:$CLIENT_SECRET" -X POST "$BASE/oauth/introspect" -d "token=$ACCESS_TOKEN"
# → 200  {"active":true,"scope":"openid","sub":"...", ...}
```
