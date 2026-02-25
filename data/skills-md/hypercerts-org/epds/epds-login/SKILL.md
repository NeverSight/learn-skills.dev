---
name: epds-login
description: Implement AT Protocol OAuth login against an ePDS instance. Use when building passwordless OTP login flows, PAR requests, DPoP proofs, token exchange against ePDS (extended PDS from Certified). Covers Flow 1 (app has email form, passes login_hint) and Flow 2 (auth server collects email).
---

# Implementing ePDS Login

ePDS lets your users sign in to [AT Protocol](https://atproto.com/) apps — like
[Bluesky](https://bsky.app/) — using familiar login methods: **email OTP**, **Google**,
**GitHub**, or any other provider [Better Auth](https://www.better-auth.com/) supports.
Under the hood it is a standard AT Protocol PDS wrapped with a pluggable authentication
layer. Users just sign in with their email or social account and get a presence in the
AT Protocol universe (a DID, a handle, a data repository) automatically provisioned.

From your app's perspective, ePDS uses standard AT Protocol OAuth (PAR + PKCE + DPoP).
The reference implementation is `packages/demo` in the [ePDS repository](https://github.com/hypercerts-org/ePDS).

## Two Flows

|                         | Flow 1                | Flow 2           |
| ----------------------- | --------------------- | ---------------- |
| **App collects email?** | Yes                   | No               |
| **PAR includes**        | Nothing extra         | Nothing extra    |
| **Auth server shows**   | OTP input directly    | Email form first |
| **Redirect includes**   | `&login_hint=<email>` | Nothing extra    |

> **Important:** `login_hint` must **never** go in the PAR body when the value is an
> email address. The PDS core (AT Protocol layer) validates `login_hint` as an ATProto
> identity (handle like `user.bsky.social` or DID like `did:plc:…`) and rejects email
> addresses with `Invalid login_hint`. Put `login_hint` only on the **auth redirect URL**
> — that request goes to the ePDS auth service (Better Auth layer), which accepts emails
> and uses them to skip the email-collection step.

## Quick Start

### 1. Client Metadata

Host at your `client_id` URL (must be HTTPS in production):

```json
{
  "client_id": "https://yourapp.example.com/client-metadata.json",
  "client_name": "Your App",
  "redirect_uris": ["https://yourapp.example.com/api/oauth/callback"],
  "scope": "atproto transition:generic",
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "dpop_bound_access_tokens": true
}
```

Optional branding fields: `logo_uri`, `email_template_uri`, `email_subject_template`,
`brand_color`, `background_color`.

### 2. Login Handler

```typescript
// GET /api/oauth/login?email=user@example.com  (Flow 1)
// GET /api/oauth/login                         (Flow 2)

const { privateKey, publicJwk, privateJwk } = generateDpopKeyPair()
const codeVerifier = generateCodeVerifier()
const codeChallenge = generateCodeChallenge(codeVerifier)
const state = generateState()

const parBody = new URLSearchParams({
  client_id: clientId,
  redirect_uri: redirectUri,
  response_type: 'code',
  scope: 'atproto transition:generic',
  state,
  code_challenge: codeChallenge,
  code_challenge_method: 'S256',
})

// PAR always requires a DPoP nonce retry — handle it:
let parRes = await fetch(PAR_ENDPOINT, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    DPoP: createDpopProof({
      privateKey,
      jwk: publicJwk,
      method: 'POST',
      url: PAR_ENDPOINT,
    }),
  },
  body: parBody.toString(),
})
if (!parRes.ok) {
  const nonce = parRes.headers.get('dpop-nonce')
  if (nonce && parRes.status === 400) {
    parRes = await fetch(PAR_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        DPoP: createDpopProof({
          privateKey,
          jwk: publicJwk,
          method: 'POST',
          url: PAR_ENDPOINT,
          nonce,
        }),
      },
      body: parBody.toString(),
    })
  }
}

const { request_uri } = await parRes.json()

// Save state in signed HttpOnly cookie (maxAge: 600 to match request_uri lifetime)
const loginHintParam = email ? `&login_hint=${encodeURIComponent(email)}` : ''
const authUrl = `${AUTH_ENDPOINT}?client_id=${encodeURIComponent(clientId)}&request_uri=${encodeURIComponent(request_uri)}${loginHintParam}`
// redirect to authUrl
```

### 3. Callback Handler

```typescript
// GET /api/oauth/callback?code=...&state=...

const {
  codeVerifier,
  dpopPrivateJwk,
  state: savedState,
} = getSessionFromCookie()
if (params.state !== savedState) throw new Error('state mismatch')

const { privateKey, publicJwk } = restoreDpopKeyPair(dpopPrivateJwk)

// Token exchange — also requires DPoP nonce retry:
let tokenRes = await fetch(TOKEN_ENDPOINT, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    DPoP: createDpopProof({
      privateKey,
      jwk: publicJwk,
      method: 'POST',
      url: TOKEN_ENDPOINT,
    }),
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code,
    redirect_uri: redirectUri,
    client_id: clientId,
    code_verifier: codeVerifier,
  }).toString(),
})
if (!tokenRes.ok) {
  const nonce = tokenRes.headers.get('dpop-nonce')
  if (nonce) {
    tokenRes = await fetch(TOKEN_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        DPoP: createDpopProof({
          privateKey,
          jwk: publicJwk,
          method: 'POST',
          url: TOKEN_ENDPOINT,
          nonce,
        }),
      },
      body: /* same body */ '',
    })
  }
}

const { sub: userDid } = await tokenRes.json()
// sub is a DID e.g. "did:plc:abc123..." — resolve to handle via PLC directory
```

## Common Pitfalls

| Pitfall                        | Fix                                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| Flash of email form            | Include `login_hint` on the **auth redirect URL only** (never in the PAR body)                 |
| `Invalid login_hint` from PAR  | Remove `login_hint` from the PAR body — PDS core only accepts ATProto handles/DIDs, not emails |
| `auth_failed` immediately      | Check Caddy logs — likely a DNS/upstream name mismatch                                         |
| DPoP rejected                  | Always implement the nonce retry loop (ePDS always demands a nonce)                            |
| `Cannot find package` in tests | Run `pnpm build` before `pnpm test` — vitest needs `dist/`                                     |
| Token exchange fails           | Restore the DPoP key pair from the session cookie, don't generate a new one                    |
| Double OTP email               | Normal on duplicate GET — `otpAlreadySent` flag suppresses auto-send on reload                 |

## Handles

ePDS generates random handles, not email-derived ones. When a user signs up
with `alice@example.com`, their handle will be something like `a3x9kf.pds.example`
(random prefix + PDS hostname), not `alice.pds.example`. Resolve the handle
from the DID via the PLC directory after login (shown in the callback handler).

## ePDS Endpoints (defaults)

```
PAR:   https://<pds-hostname>/oauth/par
Auth:  https://auth.<pds-hostname>/oauth/authorize
Token: https://<pds-hostname>/oauth/token
```

## Reference Files

- [PKCE and DPoP helpers](references/dpop-pkce.md) — full TypeScript implementations
- [Client metadata fields](references/client-metadata.md) — all supported fields including email branding
- [Full flow walkthrough](references/flows.md) — sequence diagrams and step-by-step for both flows
