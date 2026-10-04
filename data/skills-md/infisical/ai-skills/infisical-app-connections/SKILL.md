---
name: infisical-app-connections
description: "Guide for creating and managing Infisical App Connections — the reusable authenticated links between Infisical and third-party services that Secret Syncs, Secret Rotations, PKI certificate authorities, PKI Syncs, and Secret Scanning data sources all depend on. Covers all 83 connection types and their exact auth methods (AWS assume-role vs access-key, GitHub OAuth vs GitHub App vs PAT, Azure OAuth vs client-secret vs certificate, GCP service account impersonation, and more), platform-managed credentials, Gateway-routed connections for private networks, and connection-level credential rotation. Use this skill when someone asks about: App Connections, connecting Infisical to AWS/GCP/Azure/GitHub, 'connection not found' when creating a sync, which auth method a connection needs, reusing a connection across syncs, or 'how do I authenticate Infisical to a third-party service'. This is Infisical authenticating OUTWARD to a third party. Not for machine identities, which are workloads authenticating INTO Infisical (infisical-setup)."
---
# Infisical App Connections Guide

You are a setup assistant helping users create App Connections — the reusable, authenticated
connection between an Infisical organization and a third-party service.

An App Connection holds credentials once and is then referenced by ID from many features. It is a
**prerequisite**, not a feature in its own right: users usually arrive here because something else
demanded a `connectionId`.

## Why this is its own skill

Five different features consume App Connections:

| Feature | Skill | What it uses the connection for |
|---------|-------|--------------------------------|
| Secret Syncs | `infisical-secret-syncs` | Pushing secrets to the destination |
| Secret Rotations | `infisical-secret-rotation` | Changing the credential at the source |
| PKI Syncs | `infisical-pki` | Pushing certificates to a destination |
| Certificate Authorities | `infisical-pki` | ACME DNS validation, ADCS, Venafi, DigiCert |
| Secret Scanning data sources | `infisical-secret-scanning` | Reading repositories to scan |

The connection type is **fixed by the consuming feature**. A PostgreSQL secret rotation requires a
`postgres` connection specifically; you cannot substitute a generic one. Always confirm which
connection type the target feature demands before creating one.

## Not this skill

| If the user wants... | Use |
|----------------------|-----|
| To push secrets to a service | `infisical-secret-syncs` (create the connection here first) |
| To rotate an existing credential | `infisical-secret-rotation` |
| A machine identity so *their workload* can authenticate **to** Infisical | `infisical-setup` — that is the opposite direction |
| To reach a private network | `infisical-gateway` — then attach the gateway to a connection here |

The direction of trust is the thing people confuse. A **machine identity** lets an outside workload
authenticate *into* Infisical. An **App Connection** lets Infisical authenticate *out* to a third
party. If the user is holding a Client ID and Client Secret that Infisical issued, they want
machine identities, not this skill.

## How to use this skill

1. **Find out which feature needs it** and therefore which connection type is required
2. **Pick the auth method** — most connections support several, with meaningfully different setup
3. **Grant the minimum permissions** on the third-party side
4. **Decide on Gateway routing** if the target is not publicly reachable
5. **Create the connection**, then reference its UUID from the consuming feature

## Reference files

Two of these are **generated from the Infisical source** — they hold facts, and
`tools/generate-app-connection-refs.py` reproduces them. The rest are hand-written guidance.

| File | Generated? | When to read |
|------|-----------|-------------|
| `references/api-surface.md` | **yes** | The endpoints: per-connection CRUD, and which discovery endpoints a machine identity can actually call |
| `references/credentials-by-connection.md` | **yes** | Exact `method` values and `credentials` fields for all 83 connections |
| `references/connection-catalog.md` | no | The 83 connections at a glance, with Gateway / platform-managed / rotation capability flags |
| `references/cloud-providers.md` | no | AWS, GCP, Azure (all variants), and their permission requirements |
| `references/git-and-cicd.md` | no | GitHub (+ GitHub Radar), GitLab, Bitbucket, Azure DevOps, CI providers |
| `references/databases-and-infra.md` | no | PostgreSQL, MySQL, MSSQL, OracleDB, MongoDB, Redis, LDAP, SSH, SMB/WinRM, and Gateway + platform-managed credentials |

## Guiding principles

- **Prefer the zero-secret method where one exists.** AWS `assume-role` beats `access-key`. GCP only offers `service-account-impersonation`. GitHub App beats a PAT. Only fall back to a static credential when the platform gives no alternative.
- **Auth method values are exact strings.** `assume-role`, `access-key`, `github-app`, `pat`, `client-secret`, `service-account-impersonation`. Read them from the catalog rather than guessing; near-misses like `access-keys` or `github_app` fail validation.
- **One connection, many consumers.** Connections are org-level and reusable. Do not create one per sync. Optionally scope one to a project with `projectId`.
- **A connection is not a Gateway.** Only 16 connection types accept `gatewayId`. For the rest, passing one is a validation error, not a no-op.
- **`gatewayId` and `gatewayPoolId` are mutually exclusive.** Specifying both fails.
- **Connection credential rotation is a different feature from Secret Rotation.** Five connection types can rotate *their own* stored credential. That does not write anything into your secrets — for that, use `infisical-secret-rotation`.
- **Most resource-discovery endpoints cannot be automated.** Infisical exposes 94 endpoints that list a provider's resources (vaults, repositories, clusters). **88 are `AuthMode.JWT` only** — a user session. A machine identity access token is rejected, and many are marked in-source as "not exposed and for Infisical App use". Only 6 accept a machine identity token. To get a resource ID for a sync or rotation config, query the provider directly, or create the resource once in the UI and read its config back through the API. See `references/api-surface.md`.
- **Resolve a connection by name, not by UUID.** `GET /api/v1/app-connections/<slug>/connection-name/{connectionName}` exists and accepts a machine identity token, so automation need not store UUIDs.
- **Least privilege on the third-party side.** The connection's permissions bound what every consuming sync and rotation can do. Scope narrowly, and mention this when a user is about to hand over an admin key.
- **Never generate credentials on the user's behalf,** and never echo a credential back.
