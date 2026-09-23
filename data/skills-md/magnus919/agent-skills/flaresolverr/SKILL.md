---
name: flaresolverr
description: >-
  Use the minimal FlareSolverr wrapper for a one-off health check or browser-backed
  GET/POST when ordinary retrieval is blocked by Cloudflare or DDoS-GUARD. Choose
  flaresolverr-cli instead for named session lifecycle, cookie-only returns, dry-run
  planning, or the full operational command surface. Do not use this skill for unrelated
  requests; route to the nearest named specialist.
---

# FlareSolverr

## Quick Start

```sh
python3 scripts/flaresolverr --server http://localhost:8191 health
```

Use this skill when ordinary HTTP retrieval is blocked by a browser challenge. FlareSolverr must already be running; this skill does not bypass authentication or authorize access to restricted content.

## When not to use

Use [flaresolverr-cli](../flaresolverr-cli/SKILL.md) when the task names that CLI, requires creating/listing/destroying named sessions, needs cookie-only responses or dry-run planning, or needs the full operational command surface. Keep this skill for the smaller one-off health, GET, or POST path.

## Mutation Gate

The health command is read-only discovery. GET and POST send traffic to an external target, and POST may change target state.

> Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

A POST or any request intended to change target state requires an explicit user directive. This skill does not authorize deletion, privilege changes, authentication bypass, or irreversible cleanup.

## CLI

```text
python3 flaresolverr/scripts/flaresolverr --server http://localhost:8191 health
python3 flaresolverr/scripts/flaresolverr --server http://localhost:8191 get https://example.com
python3 flaresolverr/scripts/flaresolverr session create
python3 flaresolverr/scripts/flaresolverr session list
python3 flaresolverr/scripts/flaresolverr session destroy SESSION_ID
```

Every command emits JSON. `get` and `post` use FlareSolverr's `/v1` API and preserve the returned status, URL, headers, and response body. Use `--timeout` to bound a request and `--session` when a site needs cookie continuity.

## Setup

Run FlareSolverr separately, commonly with Docker:

```yaml
services:
  flaresolverr:
    image: ghcr.io/flaresolverr/flaresolverr:latest
    ports: ["8191:8191"]
    environment:
      LOG_LEVEL: info
```

Do not expose the service publicly. Prefer a pinned image tag in production and use the vendor's documentation for browser and platform compatibility.

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/flaresolverr` | Minimal JSON CLI for the FlareSolverr API: `health`, `get`, `post`, and `session` subcommands with `--server` and `--timeout` options. Run it for the one-off health check or challenge-solving GET/POST described above, and for short-lived session create/list/destroy when a site needs cookie continuity. | `python3 scripts/flaresolverr --server http://localhost:8191 get https://example.com` |
| `scripts/test-flaresolverr.sh` | Shell smoke test: verifies `--help` output and byte-compiles the CLI. Run it after modifying `scripts/flaresolverr` or when auditing the bundled script; CI runs it via `scripts/check-skill-tests.py`. | `sh scripts/test-flaresolverr.sh` |

## Prerequisites

- Python 3 with the standard library only; the CLI has no third-party dependencies.
- A reachable FlareSolverr instance (commonly via Docker, per Setup above) — the CLI is a client and starts nothing itself.
- Network access from the FlareSolverr instance to the target site; this skill does not bypass authentication or grant access to content you are not otherwise entitled to retrieve.

## Limitations

- The wrapper covers only the one-off `health`, `get`, `post`, and `session` paths; named-session lifecycle management, cookie-only returns, and dry-run planning belong to `flaresolverr-cli` (see When not to use).
- Every command emits JSON and reports what FlareSolverr returned; it does not parse, extract, or rank page content for you.
- Solving a browser challenge is not a guarantee: sites may still block, captcha, or rate-limit the underlying browser, and `--timeout` bounds only the request, not the target's behavior.
