---
name: authlete-dpop
description: >-
  Add DPoP (sender-constrained tokens, RFC 9449) to an Authlete-based OAuth/OIDC server. Use when a
  developer wants DPoP, proof-of-possession, `jkt`-bound tokens, or a DPoP-Nonce flow. This is a
  cross-cutting add-on that layers onto existing endpoints. Works with the authlete-oauth-server base skill.
---

# Add DPoP to your Authlete server

**What this adds:** DPoP (RFC 9449) binds a token to a key the client holds, so a stolen token is
useless without the matching private key. It's required by FAPI 2.0 and increasingly common elsewhere.

Unlike the other add-ons, DPoP is **not a new endpoint** — it layers a little extra onto the token, PAR,
and userinfo handlers you already have.

## How it works (the short version)

The client sends a signed "DPoP proof" header with each request. Your server just **passes that proof
through to Authlete**, which does all the cryptographic checking. You never verify a signature yourself.

## What to change on each endpoint

Add a small helper that reads two things from the request: the `DPoP` header (the proof) and the HTTP
method. Then, on the **token, PAR, and userinfo** handlers:

1. Include the proof and the method in the Authlete call.
2. **Don't send the URL (`htu`)** — Authlete derives it from service config; the proof carries its own.
3. **Echo back the `DPoP-Nonce`** header Authlete returns, so the client can retry when asked.
4. At **userinfo**, also accept a token sent with the `DPoP` scheme (not just `Bearer`).

In TypeScript the base skill already has a `dpopParams(request)` helper shape — spread it into the
token / PAR / userinfo request payloads.

## Turn it on in the service

Enable DPoP on the **Authlete service**. Once on, discovery advertises
`dpop_signing_alg_values_supported` automatically — no code needed for that.

## What you don't build

Everything cryptographic: validating the proof's signature, timestamps, and replay (`jti`); issuing and
checking the nonce; binding the token to the proof's key (`jkt`). Authlete does all of it. You forward
the proof and relay the result.

## Verify it works

Run [`conformance/spec.md`](conformance/spec.md). The most telling check: send a proof with a **wrong**
URL and confirm it's **rejected** — that proves your server is really forwarding the proof rather than
ignoring it. A ready-made proof minter is in
[`../../conformance/login-drivers/dpop-proof.mjs`](../../conformance/login-drivers/dpop-proof.mjs).
