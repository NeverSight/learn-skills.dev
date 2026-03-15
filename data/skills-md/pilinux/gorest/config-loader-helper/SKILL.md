---
name: config-loader-helper
description: Diagnose configuration-related failures, enumerate required env vars, and guide safe local test setup (no secrets).
license: MIT
metadata:
  mode: diagnostics
  purpose: config
---

# Config Loader Helper

## When to Use

- Tests or local runs fail due to missing or mis-set environment variables or toggles.

## Rules

- Never ask for or print real secrets.
- Use the authoritative sources listed below for env var discovery.

## Authoritative Sources

- `setTestEnv.sh` (test environment)
- `.env.sample` (root), `example/.env.sample`, `example2/cmd/app/.env.sample`
- `config/*.go` (feature checks via `os.Getenv`)
- `llms.txt` (complete env var reference tables)

## Workflow

1. **Enumerate required keys:** inspect `setTestEnv.sh`, `.env.sample` files, and `config/*.go` for `os.Getenv` calls and feature checks.
2. **Group by feature:** present keys grouped by feature toggle (JWT, RDBMS, Redis, MongoDB, Email, 2FA, CORS, Firewall, etc.).
3. **Provide minimal local setup:** recommend `source setTestEnv.sh` and any per-test overrides.

## Key Feature Toggles

- `gconfig.IsRDBMS()`, `gconfig.IsRedis()`, `gconfig.IsMongo()`
- `gconfig.IsJWT()`, `gconfig.Is2FA()`, `gconfig.IsCORS()`, `gconfig.IsWAF()`
- `gconfig.IsEmailService()`, `gconfig.IsEmailVerificationService()`
- `gconfig.IsHashPass()`, `gconfig.IsCipher()`
- See `llms.txt` for the complete list.

## Output

- Required keys (grouped by feature).
- Quick checklist of toggles that enable/disable features.
- Minimal commands to get tests running locally.

## Examples

- "Which env vars are needed to run password-recovery tests?"
- "Why is the JWT middleware not activating?"

## Related Skills

- `test-runner`, `source-search`, `code-navigation`
