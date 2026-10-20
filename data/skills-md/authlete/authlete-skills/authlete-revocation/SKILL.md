---
name: authlete-revocation
description: >-
  Add RFC 7009 token revocation to an Authlete-based OAuth/OIDC server. Use when a developer wants a
  revocation endpoint so clients can revoke access or refresh tokens. Works with the authlete-oauth-server
  base skill.
---

# Add Token Revocation to your Authlete server

**What this adds:** a `POST /oauth/revoke` endpoint so a client can revoke a token it was issued. This is
RFC 7009.

## How it works (the short version)

Pure forward-and-relay. The client authenticates, sends the token, and Authlete revokes it.

## The route — `POST /oauth/revoke`

1. Authenticate the client — **401** if credentials are missing/invalid.
2. Read the form body (`token`, optionally `token_type_hint`) and forward it to Authlete.
3. On success return **200** with an empty body.

Note: revoking an **unknown** token still returns **200** — revocation is deliberately forgiving and must
never reveal whether a token was real.

In TypeScript: `authlete.revocation(...)` (the standard revocation call).

## Important: JWT access tokens can't be revoked before they expire

If your service issues **self-contained JWT access tokens**, revoking one returns 200 but the token keeps
working until it expires — because nothing checks a revocation list to validate a JWT. This surprises
people ("I revoked it but it still works"). To actually cut off access:

- revoke the **refresh token** (it's stateful, so this works), and/or
- keep access-token lifetimes short.

Tell the developer this up front — it's the #1 revocation support question.

## What you don't build

The revocation itself and any cascade to related tokens — Authlete owns it.

## Verify it works

Run [`conformance/spec.md`](conformance/spec.md):

```bash
curl -i -u "$CLIENT_ID:$CLIENT_SECRET" -X POST "$BASE/oauth/revoke" -d "token=$TOKEN"   # → 200
```
