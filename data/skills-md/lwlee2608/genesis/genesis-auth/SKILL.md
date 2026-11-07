---
name: genesis-auth
description: Use when adding authentication to a project scaffolded with genesis — login, sessions, SSO, admin users, MFA, passkeys. Asks for an auth tier (basic/standard/strict), derives the mechanism from requirements, and implements it in place following the project's existing conventions.
user-invocable: true
disable-model-invocation: true
argument-hint: "[basic | standard | strict] [google | apple]... [passkey]"
---

# genesis-auth

Adds authentication to a genesis project. The user picks a tier and states requirements; the skill derives the mechanism — never quiz the user on implementation choices like JWT vs cookie — then writes the code directly into the target project.

This skill is a guideline, not a copy job. There is no reference implementation to clone: read the target project's existing code and write auth that matches it.

**Prerequisite:** the server needs the genesis DB layer — `internal/db` with goose migrations, sqlc, and the `users` table. The genesis CLI does not generate it. If it is missing, stop and tell the user to add it first with `/genesis sqlc`.

## Tiers

| Tier | Use case | Includes |
|---|---|---|
| `basic` | Internal tools | Single admin seeded from env var, password login, cookie session in Postgres. No signup, no email. |
| `standard` | Normal apps | Email+password users with email verification, optional Google/Apple SSO, sessions in Postgres, password reset, admin/user roles. |
| `strict` | Sensitive data | `standard` + MFA (TOTP, optionally a passkey instead), rate limiting + temporary lockout, session rotation on privilege change, audit log. Beyond this, recommend an external IdP (Keycloak, Auth0, WorkOS) instead of more homegrown code. |

## Question flow

1. **Read the arguments first.** `basic`/`standard`/`strict` answers the tier; `google`/`apple` answers SSO; `passkey` answers the second factor and implies `strict`. Ask only what is still missing.
2. **Ask remaining questions in ONE AskUserQuestion call**, with the recommended option first and marked "(Recommended)":
   - Tier: `basic` | `standard (Recommended)` | `strict`
   - Clients: `browser only (Recommended)` | `also mobile/API consumers`
   - SSO providers (multiSelect): `google` | `apple` — an empty selection means no SSO.
   - Second factor (`strict` only): `TOTP or passkey (Recommended)` | `TOTP only`. Passkeys resist phishing; TOTP codes do not.

   `basic` is browser-only with no SSO: when the arguments already say `basic`, skip Clients and SSO; if the user picks `basic` in the same call, ignore those answers. Ask Second factor only when the tier is or may become `strict`; ignore it if the user picks a lower tier. If the arguments combine `basic` with a provider, or `basic`/`standard` with `passkey`, flag the conflict in the confirmation.
3. **Derive the mechanism — do not ask about it:**
   - browser only → cookie (HttpOnly, Secure, SameSite=Lax) + server-side session token in Postgres. The web app reaches the API same-origin via the Vite proxy / nginx, so add no CORS. Lax still sends cookies on cross-site GETs: keep state changes off GET, and reject cookie-authenticated mutations with a foreign `Origin`.
   - mobile/API consumers → same cookie flow for the web, plus opaque bearer tokens from the same sessions table for mobile, and API keys for machine consumers. Not JWT: it cannot be revoked on logout, reset, or role change.
   - passkey → WebAuthn as a second factor next to TOTP, never passwordless login: the user signs in with password or SSO, then picks TOTP or a passkey at setup, and either one is enough. Passwordless adds a public login endpoint and account discovery; recommend an external IdP if the user insists.
4. **Confirm with the derived plan in prose, not more pickers.** Example: "basic tier: seeded admin, cookie sessions in Postgres, no SSO, server only (no web login UI) — proceed?" If the user overrides a mechanism (e.g. "actually JWT") or asks for the web UI, name the trade-off and honor it.

## Implementation rules

1. **Read the target project before writing anything.** Its router, config struct, migration numbering, and package layout decide the shape of the new code. Match them; do not impose a layout from this document.
2. **Extend the existing users table, don't invent a parallel one.** A genesis server already ships `internal/db/migrations/0001_create_users.sql` with a unique `username`, `password_hash`, and a `user_role` enum. Add columns and new tables in a new numbered migration. For `standard`+, add a unique `email` stored lowercased, log in by email, and set `username` to that email on signup. On a populated table, never assume usernames are emails: backfill before enforcing `NOT NULL`, and surface missing addresses and case collisions to the user instead of guessing.
3. **Follow the established layout** for a genesis server:
   - `internal/auth/` — password hashing, session/token issue and verify, provider clients. No gin types in here.
   - `internal/api/http/handler/auth.go` — login, logout, signup, reset endpoints.
   - `internal/api/http/dto/auth.go` — request/response structs.
   - `internal/api/http/middleware/auth.go` — session/bearer verification, role checks.
   - `internal/db/migrations/NNNN_*.sql` — goose `-- +goose Up` / `Down` blocks, both directions.
   - `internal/db/queries/*.sql` — sqlc named queries; run `make generate` after editing (`make dep` installs sqlc).
4. **Wire everything.** Register handlers and middleware in `SetupRoute`, add any new dependency to the `Services` struct, and construct it in `main.go`. Auth code that compiles but is never mounted looks done and isn't.
5. **Config goes through the existing mechanism.** Define `auth.Config` in `internal/auth` and compose it into the struct in `cmd/<app>/config.go`, like `db.Config`. Put non-secret defaults in `application.yml` and every key in `.env.example` using the `.` → `_` upper-case form (`auth.sessionTtl` → `AUTH_SESSIONTTL`). Keep secrets (seed password, client secrets, SMTP password, keys) out of `application.yml` and tag them `mask:"true"`: the loader dumps the whole config at debug, the default level. Match the loader's field binding (see the `adder` skill); never read `os.Getenv` directly.
6. **Use the standard library and existing deps first.** `golang.org/x/crypto/bcrypt` for passwords, `crypto/rand` for tokens. Add a dependency only when the tier genuinely needs it (OIDC, TOTP, WebAuthn), and run `go mod tidy`.
7. **Never log or return secrets.** No password, hash, session token, or reset token in logs or error responses. Store only SHA-256 hashes of session, reset, verification, and API tokens (32 bytes from `crypto/rand`); bcrypt is for passwords only, since token hashes must be indexable for lookup. Don't reveal whether an account exists: return the same error for an unknown user and a wrong password (compare against a dummy hash so timing matches), and the same response to every reset request.
8. **Reset atomically.** Validate/consume the reset token, update the password, and revoke sessions in one transaction. Lock or conditionally consume the token so concurrent requests cannot both succeed.
9. **Use `TIMESTAMPTZ` for every timestamp column.** The genesis `users` table already uses it (`created_at`, `updated_at`), and sqlc maps it to `pgtype.Timestamptz`. Do the same for session/reset expiry and lifecycle columns; never mix in plain `TIMESTAMP`, which drops the offset and breaks expiry checks on a non-UTC database.
10. **Expiry is not cleanup.** Wire bounded periodic deletion of expired sessions and expired/used reset records, with suitable indexes.
11. **Validate bcrypt's byte limit.** Reject passwords over 72 bytes with a client-validation error on signup/reset; character-count validators are insufficient.
12. **Send email through a `Mailer` interface** in `internal/auth` with an SMTP implementation. When SMTP is not configured, reset and verification requests return 503 and write no token rows; never log the link as stand-in delivery. Startup must not depend on the log level.
13. **Follow [sso.md](sso.md) for SSO** when Google or Apple is chosen.
14. **Seed the first admin from config, in every tier.** Create it only when no `Admin` user exists and never overwrite one; if none exists and the seed password is empty, fail startup with a clear error. Signup always creates `User`; never accept `role` from the request.
15. **Strict extras.** Keep rate-limit and lockout state in Postgres (in-memory breaks with replicas), and make `ClientIP()` trustworthy. Genesis `main.go` already calls `SetTrustedProxies` with the private ranges, which covers nginx on the VM and Railway; behind a public proxy (GKE load balancer, Cloudflare), add its ranges or set `TrustedPlatform`. Older projects may lack the call, and then gin trusts everyone and reads a spoofable `X-Forwarded-For` — add it, never a second one. Lockouts expire and back off; a permanent one lets anyone lock out the admin.
16. **Follow [mfa.md](mfa.md) for MFA** in the `strict` tier: pending sessions, enrollment, recovery, and passkeys.

## Verification procedure

1. `make build` passes in the target server.
2. `make generate` is clean and the generated code is in the tree.
3. A migration file exists — up *and* down — for every new table or column the code queries.
4. Every new config key appears in `.env.example`, non-secret ones also in `application.yml`, and secret fields carry `mask:"true"`.
5. For cookie sessions: the cookie is set with `HttpOnly`, `Secure`, and `SameSite`.
6. Session tokens are stored hashed, with an expiry column, and logout deletes the row.
7. Run it — a passing build or `[no test files]` is not verification. Start the project's docker-compose Postgres, run the server with `LOG_LEVEL=info`, and curl the flows: login, logout, a protected route, a role check. Migrate both a fresh database and one with existing users (they can still log in), and recheck expiry after `ALTER DATABASE ... SET timezone = 'Asia/Singapore'`.
8. `strict`: run the checks in [mfa.md](mfa.md).
9. `standard`+: of two concurrent resets with one token, exactly one succeeds; a failed reset rolls back; 40 × `é` (80 bytes) is rejected with a 4xx; expired rows get cleaned up.
