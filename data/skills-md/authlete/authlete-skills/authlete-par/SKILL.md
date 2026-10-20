---
name: authlete-par
description: >-
  Add Pushed Authorization Requests (PAR, RFC 9126) to an Authlete-based OAuth/OIDC server. Use when a
  developer wants PAR, a pushed-authorization endpoint, `request_uri`, or FAPI request integrity. Works
  with the authlete-oauth-server base skill (Go, Ruby, or TypeScript).
---

# Add PAR to your Authlete server

**What this adds:** a `POST /oauth/par` endpoint. Clients push their authorization request to your
server *first* and get back a short-lived `request_uri`; they then send the browser to `/oauth/authorize`
with just that `request_uri`. This is RFC 9126, and FAPI 2.0 requires it.

## How it works (the short version)

Your server stays thin. It takes the pushed request, hands it to Authlete, and returns Authlete's
answer. **Authlete** generates the `request_uri`, enforces its one-time use, expiry, and client binding.
**You** just forward the request and relay the response — no protocol logic.

## Step 1 — add the endpoint

`POST /oauth/par`:

1. Read the raw form body (don't parse it) and the client's credentials (Basic header / form).
2. Call Authlete's pushed-authorization method, passing the raw parameters + client credentials
   (+ the DPoP proof if you also use [authlete-dpop](../authlete-dpop/SKILL.md)).
3. Turn Authlete's `action` into an HTTP response:

   | Authlete action | You return |
   |---|---|
   | `CREATED` | **201** + the JSON body (`{ request_uri, expires_in }`) |
   | `BAD_REQUEST` | **400** + the JSON error |
   | `UNAUTHORIZED` | **401** + a `WWW-Authenticate` challenge |
   | `FORBIDDEN` | **403** |
   | `PAYLOAD_TOO_LARGE` | **413** |
   | `INTERNAL_SERVER_ERROR` | **500** |

In TypeScript that's `authlete.pushedAuthorization.create({ serviceId, pushedAuthorizationRequest: { parameters, clientId, clientSecret, dpop, htm } })`.
(Go/Ruby: the pushed-authorization "create" method — check `reference/` in the base skill for exact names.)

## Step 2 — configure the service (the easy-to-miss half)

Your server serves its discovery document straight from Authlete. If the **Authlete service** doesn't
have its PAR endpoint URL set, discovery won't advertise `pushed_authorization_request_endpoint` — and
clients that rely on discovery won't find your endpoint, even though it works.

**So: set the PAR endpoint URL on the Authlete service** (to `<your-server>/oauth/par`). This is a
one-time console/API change, not code. It's the single most common thing people forget.

## What you don't build

Authlete owns everything about the `request_uri`: generating it, its one-time use, expiry, and binding
it to the client. You never implement those — you forward the request and relay the result.

## Verify it works

Run the checks in [`conformance/spec.md`](conformance/spec.md). Quick smoke test (needs a registered
client — see [authlete-dcr](../authlete-dcr/SKILL.md)):

```bash
curl -u "$CLIENT_ID:$CLIENT_SECRET" -X POST "$BASE/oauth/par" \
  -d "response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT&scope=openid&state=xyz"
# → 201  {"expires_in":600,"request_uri":"urn:ietf:params:oauth:request_uri:..."}
```
