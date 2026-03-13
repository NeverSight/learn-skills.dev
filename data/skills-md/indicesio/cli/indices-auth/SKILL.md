---
name: indices-auth
description: Use this skill when the user needs to authenticate with the Indices CLI, verify auth state, or remove stored credentials.
---

# Indices Auth

## When To Use

Use this skill for:
- `indices login`
- `indices auth-test`
- `indices logout`
- API key verification and storage behavior

## Commands

### Login

```bash
indices login
indices login --api-key "<api-key>"
```

Behavior:
- If `--api-key` is omitted, CLI securely prompts for the key.
- API key is validated.
- Stores API key in local config.

### Auth Test

```bash
indices auth-test
```

Returns an authenticated probe response.

### Logout

```bash
indices logout
```

Removes stored API key.

## Useful Global Flags

```bash
indices auth-test --output json
indices login --api-base https://api.indices.io --timeout 30
```
