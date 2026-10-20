---
name: authlete-userinfo
description: >-
  Add the OIDC UserInfo endpoint (OpenID Connect Core §5.3) to an Authlete-based server. Use when a
  developer wants a userinfo endpoint or to return a user's profile/email claims for an access token.
  Works with the authlete-oauth-server base skill (which already includes a basic userinfo).
---

# Add the UserInfo endpoint to your Authlete server

**What this adds:** a `/oauth/userinfo` endpoint that, given a valid access token, returns the user's
claims (`sub`, and whatever profile/email claims the user consented to). This is OpenID Connect Core §5.3.

> The base `authlete-oauth-server` skill already includes a basic userinfo. Use this skill when you're
> adding it to a server that doesn't have it, or want the full contract spelled out.

## How it works (the short version)

UserInfo is almost thin, with **one real job**: supplying the claim *values*. Authlete decides *which*
claims are allowed for this token; your server looks those up for the user and returns them.

## The route — `GET` and `POST /oauth/userinfo`

1. Read the access token from the `Authorization` header (accept both `Bearer` and, if you use
   [authlete-dpop](../authlete-dpop/SKILL.md), `DPoP`).
2. **First Authlete call** — validate the token. Authlete returns the user's `subject` and the list of
   claims this token is allowed to see. If the token is bad, relay Authlete's response (status +
   `WWW-Authenticate`) and stop.
3. **Look up** those claims for that subject in your identity source.
4. **Second Authlete call** — hand back the claim values; return Authlete's response (JSON, or a signed
   JWT if the client asked for one).

In TypeScript: `authlete.userinfo.process(...)` then `authlete.userinfo.issue(...)`.

## What you don't build

Token validation and the decision about which claims are allowed — Authlete owns both. You only supply
claim values for the subject it gives you.

## Verify it works

Run [`conformance/spec.md`](conformance/spec.md). You'll need an access token — get one with the shared
login driver ([`../../conformance/login-drivers/`](../../conformance/login-drivers/)):

```bash
curl "$BASE/oauth/userinfo" -H "Authorization: Bearer $ACCESS_TOKEN"
# → 200  {"sub":"...", "name":"...", "email":"..."}   (claims limited to what was granted)
```
