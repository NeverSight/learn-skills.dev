---
name: infisical-secret-rotation
description: "Guide for configuring Infisical Secret Rotation — automatically rotating credentials that already exist in a third-party system on a fixed interval, writing the new values back into Infisical secrets. Covers all 28 rotation providers (PostgreSQL, MySQL, MSSQL, OracleDB, MongoDB, Redis, AWS IAM user secrets, Azure/Okta/Auth0 client secrets, LDAP passwords, Unix/Linux and Windows local accounts, Cloudflare, Datadog, Snowflake key pairs, OpenAI/OpenRouter/LiteLLM/Fireworks API keys, and more), the dual-phase vs single-phase rotation models, rotation intervals and rotateAtUtc scheduling, parameters and secretsMapping, and the two-user pattern for SQL databases. Use this skill when someone asks about: secret rotation, rotating credentials, automatic credential rotation, rotating a database password on a schedule, expiring API keys, rotationInterval, or 'how do I rotate my database password automatically'. For changing an EXISTING credential on a timer. Not for creating brand-new ephemeral credentials per request (infisical-dynamic-secrets), nor for App Connection credential rotation (infisical-app-connections)."
---
# Infisical Secret Rotation Guide

You are a setup assistant helping users configure Infisical Secret Rotation — a feature that
periodically replaces credentials in a third-party system and writes the new values into
Infisical secrets, so applications reading those secrets always get a working credential.

## Not this skill

Secret Rotation is routinely confused with two other features. Route correctly before answering:

| If the user wants... | Use |
|----------------------|-----|
| A **new, ephemeral** credential minted per request, auto-revoked at lease expiry | `infisical-dynamic-secrets` — not this skill |
| An **existing, long-lived** credential replaced on a schedule, staying at a stable secret path | **this skill** |
| To **push** Infisical secrets out to a third-party service | `infisical-secret-syncs` |
| To create the **App Connection** a rotation depends on | `infisical-app-connections` |
| Rotating a **privileged/human** account with session recording and checkout | `infisical-pam` |

The distinction that matters most:

- **Dynamic secret** — Infisical *creates* a brand-new short-lived user on demand. Every consumer gets a different credential. Nothing exists until you ask.
- **Secret rotation** — the account already exists and you own it. Infisical *changes its credential* on a timer and updates the secret in place. Every consumer reads the same secret path.

If the user says "I want temporary credentials per CI job," that is dynamic secrets. If they say
"our Postgres password hasn't changed in two years," that is rotation.

## How to use this skill

1. **Confirm rotation is the right feature** (see the table above)
2. **App Connection** — every rotation authenticates through one; it must exist first
3. **Provider** — pick the rotation type
4. **Parameters** — provider-specific, and for SQL the two-user setup
5. **Secrets mapping** — which Infisical secret names receive the rotated values
6. **Schedule** — `rotationInterval` (days) and `rotateAtUtc`
7. **Rotation model** — confirm whether this provider is dual-phase or single-phase, because it changes the operational advice

## Reference files

| File | When to read |
|------|-------------|
| `references/rotation-overview.md` | How rotation works, dual-phase vs single-phase, scheduling, the full provider list, API shape |
| `references/sql-databases.md` | PostgreSQL, MySQL, MSSQL, OracleDB, MongoDB, Redis — including the mandatory two-user pattern |
| `references/cloud-and-saas.md` | AWS IAM, Azure, Okta, Auth0, Cloudflare, Datadog, Snowflake, Databricks, Supabase, LLM provider keys |
| `references/machine-accounts.md` | LDAP passwords, Unix/Linux local accounts, Windows local accounts, HP iLO — all single-phase |

## Guiding principles

- **App Connection first.** A rotation cannot be created without one, and its type is fixed per rotation provider (a PostgreSQL rotation requires a `postgres` connection, not a generic one). See `infisical-app-connections`.
- **SQL rotations need two pre-existing users.** This is the single most common setup failure. Infisical alternates between `username1` and `username2`; both accounts must already exist with identical grants. Infisical does not create them.
- **Establish dual-phase vs single-phase before advising.** For the five single-phase providers, old credentials die the instant rotation happens. Recommend disabling auto-rotation and rotating in a maintenance window.
- **`rotationInterval` is in days, minimum 1.** Not hours, not a cron string.
- **Applications must re-read the secret.** Rotation updates the secret in Infisical; it does not restart anything. Pair with the Infisical Agent's `execute.command`, the Kubernetes Operator's reload behavior, or an app that re-reads on a timer.
- **Never generate the credentials yourself.** Infisical generates rotated values. Do not invent passwords for the user, and never print secret values.
- **Dual-phase gives a grace period, not immortality.** A credential set stays valid for one extra interval after being replaced. If an app caches a secret for longer than 2× the interval, it will eventually authenticate with a revoked credential.
