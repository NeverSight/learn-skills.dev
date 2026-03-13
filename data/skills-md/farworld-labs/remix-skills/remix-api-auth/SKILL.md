---
name: remix-api-auth
description: Configure and verify bearer API key authentication for Remix APIs
metadata:
  tags: remix, auth, api-key, authentication
---

# Remix API Key Setup

Use this skill when a user needs to authenticate an external service/agent for Remix server APIs.

## Steps

1. Log in to your Remix account.
2. Go to `https://remix.gg/api-keys`.
3. Create a new API key.
4. Store it as a secret in your service runtime.
5. Send:
   - `Authorization: Bearer <api_key>`
6. Use base URL `https://api.remix.gg`.

## Verification

Run a cheap authenticated call first (for example, `POST /v1/games` in a test project) to verify the key works.

## Troubleshooting Invalid API Key

- Check `Authorization` is formatted as `Bearer <api_key>`.
- Re-copy the key from `https://remix.gg/api-keys` and rotate if needed.
- Verify your service is reading the expected secret/env var in the current runtime.
- Confirm the request is server-side and not exposed through browser code.
- If behavior seems inconsistent with local docs, use `https://api.remix.gg/docs` as source of truth.

## Current Auth Model

Server API base URL: `https://api.remix.gg`

Remix server API uses bearer API keys generated from Remix account settings.

Supported auth header:
- `Authorization: Bearer <api_key>` (required)

The backend resolves the key to a user and enforces ownership checks on game/version mutations.

## How to Get an API Key

1. Log in to your Remix account.
2. Go to `https://remix.gg/api-keys`.
3. Generate a new API key.
4. Copy it once and store it in your server-side secret manager.

## Required Headers

```http
Authorization: Bearer <api_key>
Content-Type: application/json
```

## Security Notes

- Never expose API keys in client-side browser code.
- Store in server env vars or secret manager.
- Revoke and rotate keys from `https://remix.gg/api-keys`.
- Usage updates `lastUsed` automatically.

## API Authentication Rules

- Use API keys created from `https://remix.gg/api-keys`.
- Use `Authorization: Bearer <api_key>`.
- Send requests to `https://api.remix.gg`.
- Do not place keys in browser-side code.
- Rotate keys immediately if leaked.
- Account must not be banned or deleted.
