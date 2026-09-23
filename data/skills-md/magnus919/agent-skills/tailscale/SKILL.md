---
name: tailscale
description: >-
  Deploy and manage the self-hosted Tailscale/Headscale ecosystem: a Headscale control
  server, tailscale clients, ACL policies, node lifecycle, subnet routing, DERP relays,
  and backup/migration. Use when the user mentions Tailscale, Headscale, tailnet, mesh
  VPN, WireGuard mesh, or self-hosted VPN infrastructure. Do not use this skill for
  unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Requires bash, Python 3.8+, jq, curl, and access to a Headscale server
  or the `headscale` CLI. Tailscale client (`tailscale`) must be installed on target
  machines.
metadata:
  tags: tailscale, headscale, vpn, wireguard, mesh, networking, homelab
  spec-version: '1.0'
---

# Tailscale + Headscale Skill Bundle

This umbrella skill covers the self-hosted Tailscale ecosystem using [Headscale](https://headscale.net)
as the open-source control server. It provides 7 sub-skills that are auto-loaded by context.

## Auto-Loading by Context

When the user's message matches a trigger keyword, the corresponding sub-skill's SKILL.md
is loaded. Multiple sub-skills can load together when triggers overlap.

| Trigger Keywords | Sub-Skill(s) Loaded |
|---|---|
| "deploy headscale", "install headscale", "setup headscale server", "headscale config" | `headscale-deploy` |
| "ACL", "policy file", "tailnet policy", "access control", "grant", "tag owners" | `tailnet-policy` |
| "install tailscale", "connect to headscale", "tailscale client", "tailscale up", "tailscale status", "diagnose tailscale", "connectivity" | `tailscale-client` |
| "auth key", "preauthkey", "register node", "approve node", "tag node", "node list", "decommission node" | `headscale-node-lifecycle` |
| "subnet router", "exit node", "advertise route", "approve route" | `headscale-routing` |
| "DERP", "relay", "peer relay", "STUN" | `headscale-derp` |
| "backup headscale", "restore headscale", "migrate headscale", "headscale backup" | `headscale-backup` |
| "Tailscale", "Headscale", "tailnet", "mesh VPN", "WireGuard mesh", "self-hosted VPN" | Loads this umbrella SKILL.md for navigation |

## Sub-Skill Ordering & Dependencies

```
headscale-deploy ─────┬──> tailnet-policy ───> headscale-routing
                       │
                       ├──> headscale-node-lifecycle
                       │
                       ├──> tailscale-client
                       │
                       ├──> headscale-derp
                       │
                       └──> headscale-backup (prerequisite: a running headscale instance)
```

- **headscale-deploy** must be completed first — the others require a running Headscale server
- **tailnet-policy** (configures ACLs) is recommended before opening the tailnet to other users
- **headscale-derp** is optional but recommended for reliability across NATs
- **headscale-backup** should be run regularly on any production deployment

## Root Scripts (Shared Utilities)

These live in `scripts/` at the bundle root and are available to all sub-skills.

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/headscale-health-check.sh` | Probe Headscale server health: version, node count, and DB integrity. Run it after any control-server change and as the first diagnostic when nodes or clients misbehave. | `scripts/headscale-health-check.sh --json` |
| `scripts/headscale-backup.sh` | Full backup of the Headscale server (sqlite + config + policy + certs) to a restorable archive. Run it on a schedule for any production deployment and before upgrades or migrations; `--dry-run` previews without writing. | `scripts/headscale-backup.sh --dry-run` |
| `scripts/headscale-restore.sh` | Restore a Headscale server from a backup archive. Run it during disaster recovery or migration onto a fresh host; always verify node list and policy afterwards. | `scripts/headscale-restore.sh --backup headscale-backup-2026-01-01.tar.gz` |
| `scripts/tailscale-status-json.sh` | Structured wrapper around `tailscale status --json` with peer diagnostics. Run it from any client to check connectivity, peers, and relay/direct paths in machine-readable form. | `scripts/tailscale-status-json.sh` |
| `scripts/test-all.sh` | Smoke test across all bundle scripts (`--help`, syntax, executability) without requiring a running Headscale. Run it after modifying any bundled script; CI runs it via `scripts/check-skill-tests.py`. | `bash scripts/test-all.sh` |

## Templates

Templates live in `templates/` and cover common deployment patterns:

- `templates/docker-compose-headscale.yaml` — Headscale + embedded DERP + Traefik TLS
- `templates/headscale-config.yaml` — Annotated full headscale configuration
- `templates/policy-allow-all.json` — Minimal allow-all policy
- `templates/policy-deny-all.json` — Locked-down deny-all policy
- `templates/policy-tagged-segmented.json` — Tag-based access model
- `templates/derp-map.json` — Custom DERP relay map

## Environment Variables

| Variable | Used By | Purpose |
|---|---|---|
| `HEADSCALE_URL` | All | Headscale server URL (e.g. `https://headscale.example.com`) |
| `HEADSCALE_API_KEY` | All | Headscale API key (created via `headscale apikeys create`) |
| `TAILSCALE_AUTHKEY` | tailscale-client | Pre-authenticated key for non-interactive client setup |

## Use the CLI tools

All scripts use `--json`, `--dry-run`, and have informative `--help` output.
Scripts relative to bundle root: `scripts/<tool>` or `skills/<sub-skill>/scripts/<tool>`.

See the individual sub-skill SKILL.md for detailed usage.

## Prerequisites

- bash, Python 3.8+, `jq`, and `curl` on the host running the scripts (per `compatibility`).
- A running Headscale server with `HEADSCALE_URL` and `HEADSCALE_API_KEY` set for server-side operations (API key created via `headscale apikeys create`); `TAILSCALE_AUTHKEY` for non-interactive client enrollment.
- The `tailscale` client installed on target machines for status and routing sub-skills; the `headscale` CLI (or API access) for control-server administration.
- For headscale-backup/restore: filesystem access to the server's sqlite DB, config, policy, and cert paths, plus storage for archives off the control-server host.

## Limitations

- This bundle assumes a self-hosted Headscale control plane — it does not manage Tailscale's hosted SaaS (see When not to use).
- Scripts check environment variables at runtime and error helpfully when missing; they do not create credentials themselves.
- Backup/restore operates on the files present on the control-server host; it cannot recover data that was never backed up, and a restore should always be followed by health verification.
- Sub-skill scripts live under `skills/<sub-skill>/scripts/` and are documented in their own SKILL.md files, not here.

## When not to use

Do not load this umbrella when a task maps to a single sub-skill — load the matching sub-skill directly (e.g. `headscale-deploy`, `tailnet-policy`, `tailscale-client`). It assumes a self-hosted Headscale control server; for Tailscale's hosted SaaS control plane, or for non-Tailscale VPN tooling, use the appropriate network skill instead.
