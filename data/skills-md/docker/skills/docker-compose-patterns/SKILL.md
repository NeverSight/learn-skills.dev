---
name: docker-compose-patterns
description: Use this skill when creating, modifying, or debugging Docker Compose configurations, even if the user just says they need to wire services together, add a database to their stack, or set up a local development environment with multiple containers. Covers service definitions, health checks, dependency ordering, volumes, networks, environment variables, and development overrides.
license: Apache-2.0
compatibility: Requires Docker Compose v2 (compose.yaml format).
---

# Docker Compose Patterns

## Overview

This skill provides rules for creating, reviewing, and debugging Docker Compose configurations. Use it when the main artifact is `compose.yaml` or `compose.override.yaml` and the task is about service wiring rather than image-build internals.

## When to use this skill

Activate this skill when:

- Creating a new `compose.yaml` for a project
- Adding or modifying services in an existing Compose file
- Setting up development overrides with `compose.override.yaml`
- Debugging service startup ordering or connectivity issues

## Do not use this skill when

Do not use this skill when:

- The project has no Docker setup yet and the main need is an initial scaffold
- The main task is writing or optimizing a `Dockerfile`
- The main task is improving build caching, image size, or runtime user configuration

## Core guidance

### File naming

Use `compose.yaml` as the canonical filename. Do not use `docker-compose.yml` or `docker-compose.yaml` — those are legacy names.

### Service definitions

- Give services clear, lowercase names that reflect their role: `web`, `db`, `cache`, `worker`.
- Always pin image tags to a specific version. Never use `latest` or omit the tag.
- Set `restart: unless-stopped` for long-running infrastructure services and non-development deployments.
- Add `container_name` only when external tools need a predictable name. Otherwise, let Compose generate names.

### Dependency modeling

- Use `depends_on` with `condition: service_healthy` for services that must be ready before dependents start.
- Every service listed in `depends_on` with a health condition must have a `healthcheck` defined.
- Do not rely on `depends_on` without conditions — it only guarantees container start, not readiness.

### Health checks

- Always add a `healthcheck` to database services (Postgres, MySQL, Redis, MongoDB).
- Use the service's native client tool for health checks when available (e.g., `pg_isready`, `redis-cli ping`, `mysqladmin ping`).
- Set reasonable `interval`, `timeout`, `retries`, and `start_period` values. Start with: `interval: 5s`, `timeout: 3s`, `retries: 3`, `start_period: 10s`.

#### Health checks for distroless or scratch images

Distroless, scratch-based, and hardened images contain no shell, curl, or wget. Do not bake tools into these images — that defeats their purpose. Instead, use a **healthcheck sidecar** that shares the application's network namespace:

```yaml
services:
  api:
    build:
      context: .
      target: runtime          # distroless / hardened image
    ports:
      - "8080:8080"
    # No healthcheck here — the image has no tools to run one

  api-health:
    image: curlimages/curl:8
    network_mode: "service:api"   # shares api's localhost
    entrypoint: ["sleep", "infinity"]  # keep sidecar alive for healthcheck
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 45s
    deploy:
      resources:
        limits:
          memory: 32M
```

Key points:
- The sidecar must stay alive with `entrypoint: ["sleep", "infinity"]` so Compose can execute the healthcheck inside it.
- `network_mode: "service:api"` makes `localhost` inside the sidecar resolve to the api container's loopback — no extra networking needed.
- Keep the sidecar lightweight with a resource limit (32MB is sufficient for curl).
- Services that depend on `api` being ready should reference the **sidecar**, not the api directly:

```yaml
  worker:
    depends_on:
      api-health:
        condition: service_healthy
```

### Volumes

- Use named volumes for data that must persist across container recreations (database data, uploaded files).
- Use bind mounts only for development-time source code syncing.
- Define all named volumes in the top-level `volumes:` key.
- Do not mount the Docker socket unless the service genuinely requires it.

### Networks

- For single-application stacks, the default network is sufficient. Do not create custom networks unless you need isolation between service groups.
- When creating custom networks, prefer bridge driver and give networks descriptive names.
- Use the top-level `networks:` key to define all custom networks.

### Environment variables

- Use `environment:` for non-sensitive values that are few in number.
- Use `env_file:` pointing to a `.env` file for longer lists of variables.
- Never hardcode secrets (passwords, API keys) directly in `compose.yaml`. Use `env_file:` or Docker secrets.
- When defaults are needed in the `environment:` block for local development, use variable substitution with fallbacks: `${DB_PASSWORD:-postgres}`. Never write bare plaintext values for password fields.
- Add `.env` to `.gitignore`.

### Development overrides

- Use `compose.override.yaml` for development-only settings. Compose loads it automatically alongside `compose.yaml`.
- Put bind mounts for source code, debug ports, and development environment variables in the override file.
- Use `develop.watch` for file-syncing and auto-rebuild in development when supported.
- Keep production-oriented settings in the base `compose.yaml` and override only what changes for development.

### Compose Watch

- Prefer `develop.watch` over manual bind mounts for development workflows.
- Use `action: sync` for files that should be copied into the container on change (source code).
- Use `action: rebuild` for files that require a full image rebuild (dependency files like `package.json`, `requirements.txt`).
- Use `action: sync+restart` for configuration files that need a process restart.

### Destructive commands

Some Compose commands delete data irreversibly. Before running any of the following, state exactly which data will be deleted and get explicit confirmation from the user — do not run them as a side effect of debugging, restarting, or "cleaning up" a stack:

- `docker compose down -v` / `docker compose down --volumes` — deletes named volumes, including database data.
- `docker volume rm` / `docker volume prune` run against a Compose project's volumes — deletes volumes directly. For the standalone case (no Compose project in play), see `docker-destructive-guardrails` instead. A volume referenced via `external: true` isn't managed by the Compose project either (`down -v` won't touch it) — treat it as the standalone case too: run `docker volume rm` without `-f` first, and get explicit confirmation before deleting it.
- `docker compose rm -v` — deletes anonymous volumes attached to removed containers.

If the goal is only to restart services or reclaim containers/networks, use `docker compose down` (no `-v`) or `docker compose restart` instead — these leave named volumes intact.

## Related skills

- For first-time Docker project scaffolding and baseline file creation, use `docker-project-foundations`.
- For Dockerfile internals, build caching, multi-stage builds, and `.dockerignore`, use `docker-build-strategies`.
- For destructive Docker CLI commands outside Compose (`docker system prune`, `docker rm -f`, image/network/builder pruning, standalone volume deletion) and a cross-product index of destructive-command guardrails, use `docker-destructive-guardrails`.

## References

- `references/service-dependencies.md` — Detailed guidance on `depends_on`, health check patterns for common databases, and startup ordering strategies.
- `references/volumes-and-networks.md` — Patterns for volume mounts, named volumes, bind mounts, and network configuration.

## Assets

- `assets/compose-web-app.yaml` — Complete multi-service web app (app + Postgres + Redis) with health checks, dependencies, and named volumes.
- `assets/compose-dev-override.yaml` — Development override showing bind mounts, debug ports, and Compose Watch configuration.
- `assets/bad-vs-good.md` — Before/after comparisons of common Compose mistakes and their fixes.

## Scripts

- **`scripts/verify-compose.sh`** — Validates `compose.yaml` with `docker compose config --quiet`, without printing resolved configuration.
  ```bash
  bash scripts/verify-compose.sh [--help]
  ```
  Exit status is `0` when the Compose configuration is valid or help is requested, the non-zero status from `docker compose config --quiet` when validation fails, and `2` for invalid arguments. Plain `docker compose config` can expose interpolated and `env_file` credentials in tool output or logs; use quiet validation by default. Compose warnings and errors are still emitted and may contain sensitive details.

## Checks

- `checks/verification.md` — Detailed verification runbook for manual review.
