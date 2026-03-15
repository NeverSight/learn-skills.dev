---
name: plop-upload
description: Upload files to plop.so and get public URLs. Use when sharing files, uploading to plop, or getting a public link.
---

# Plop API

All endpoints require `Authorization: Bearer $TOKEN`. Get token: `TOKEN=$(jq -r '.access_token' ~/.plop/config.json)`

## Login (if no token or expired)

1. Request device code:
```bash
curl -s -X POST https://dev-q4qag76qq7ai5we8.us.auth0.com/oauth/device/code \
  -d "client_id=dDnceSVZAPSIYd2nZtt31FkCqpx8HTTl&audience=https://plop.so&scope=openid"
```
Response has `verification_uri_complete`, `device_code`, and `interval`.

2. Open `verification_uri_complete` in the user's browser with `open` (macOS) or `xdg-open` (Linux). Then poll for token:
```bash
curl -s -X POST https://dev-q4qag76qq7ai5we8.us.auth0.com/oauth/token \
  -d "grant_type=urn:ietf:params:oauth:grant-type:device_code&client_id=dDnceSVZAPSIYd2nZtt31FkCqpx8HTTl&device_code=DEVICE_CODE"
```
Poll every `interval` seconds until response has `access_token`. Save to `~/.plop/config.json` as `{"access_token":"...","expires_at":...}`.

## Upload

```bash
curl -s -X POST https://plop.so/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@path/to/file" \
  -F "alias=ccar.se/optional-path"
```

`alias` is optional. Response JSON: `id`, `url`, optionally `alias_url`. Alias formats: `/path` (user's subdomain), `domain.com/path`, `sub.plop.so/path`. Re-uploading to same alias replaces it.

## Other operations (read the relevant file when needed)

- **claim.md** — Claim a username subdomain (username.plop.so)
- **domains.md** — List, add, remove custom domains
