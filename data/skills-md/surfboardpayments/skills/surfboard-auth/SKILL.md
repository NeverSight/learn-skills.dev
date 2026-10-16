---
name: surfboard-auth
description: "Surfboard Payments credentials and authentication: getting Demo API keys from the developer console, the API-KEY/API-SECRET/MERCHANT-ID header model, client auth tokens for browsers and mobile apps, and where each scheme is and is not allowed. Use when setting up Surfboard credentials, debugging a 401 or 403, or calling the API from client-side code."
---

# Surfboard authentication

Read `surfboard-payments` first for the shared conventions.

## Getting credentials

Credentials are issued through the Developer Portal. A human does this once:

1. <https://developers.surfboardpayments.com/sign-up> to create a developer account
2. <https://developers.surfboardpayments.com/console/api-keys> to copy the **Demo** key,
   secret, merchant ID, and base URL

Demo credentials are issued immediately on signup. Live credentials come only after
certification (`surfboard-go-live`).

Ask the user to write the values into `.env` themselves. Do not ask for them in chat,
do not echo them, do not commit them.

```
SURFBOARD_API_URL=
SURFBOARD_API_KEY=
SURFBOARD_API_SECRET=
SURFBOARD_MERCHANT_ID=
```

Add `.env` to `.gitignore` before writing anything else.

## Server-to-server: key and secret

```
API-KEY:      YOUR_API_KEY
API-SECRET:   YOUR_API_SECRET
MERCHANT-ID:  YOUR_MERCHANT_ID
Content-Type: application/json
```

Partner-level endpoints, such as merchant onboarding, logistics, and billing plans, carry
`partnerId` in the path and often need no `MERCHANT-ID` at all. Where it is optional
and you send it anyway, it **must** match the `:merchantId` in the path, or the call
fails in a way that reads like a permissions problem.

## Client-side: auth tokens

**A key in client code is a key in public.** Anything running in a browser or on a
customer's device uses a short-lived token minted by your backend.

```
POST /partners/:partnerId/token
{
  "providerId": "YOUR_PROVIDER_ID",
  "providerCertificate": "YOUR_PROVIDER_CERTIFICATE",
  "externalUserId": "user_12345"
}
```

Returns `{ "token": "eyJ...", "validUntil": "3600" }`, in seconds rather than a timestamp. Mint
a new one when it expires; do not try to refresh it.

Send it as a bearer token:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### What client tokens can and cannot do

| Can | Cannot |
|---|---|
| Orders, payments, transactions | Create merchants |
| Tips, reporting, receipts | Manage stores |
| Branding | Any administrative operation |

Administrative work always needs the full key and secret, from your backend.

> `providerId` and `providerCertificate` are not self-serve. They come from
> <mailto:integrations@surfboard.se>. If the user does not have them, say so and
> continue with the server-side flow rather than stalling.

## Other schemes

| Scheme | Header | Used by |
|---|---|---|
| Bearer JWT | `Authorization` | Server integrations holding a session |
| API token | `X-Surfboard-Api-Token` | Scoped machine access |
| Nonce | `X-Surfboard-Nonce` | Self-hosted checkout, issued per order |

## Debugging auth failures

| Symptom | Cause to check first |
|---|---|
| 401 on every call | Key/secret pair belongs to the other environment |
| 401 after it worked | Base URL and credentials are from different environments |
| 403 with valid keys | `MERCHANT-ID` header does not match `:merchantId` in the path |
| 403 from the browser | Using key/secret client-side instead of a client token |
| 404 on a partner route | Sending `MERCHANT-ID` on a partner-level endpoint |

Check `status` in the body, not just the HTTP code.

## Bundled guides

`references/guides/` holds: client auth tokens, tokens, API conventions.
