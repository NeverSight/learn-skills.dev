---
name: docker-project-foundations
description: Use this skill when setting up, initializing, or Dockerizing a project, even if the user doesn't explicitly mention Docker but describes a need for containerized local development, adding a database or cache dependency, or running services without host-level installs. Covers Dockerfile, compose.yaml, and .dockerignore creation with Docker best practices.
license: Apache-2.0
compatibility: Requires Docker 20.10+ and Docker Compose v2.
---

# Docker Project Foundations

## Overview

This skill guides you in Dockerizing a project from scratch. It focuses on creating the initial Docker file set, choosing a sane layout, and preferring containerized dependencies over host-level installs.

## When to use this skill

Activate this skill when:

- A user asks you to set up, initialize, or Dockerize a project
- A project needs an initial `Dockerfile`, `compose.yaml`, or `.dockerignore` and does not have one
- A user wants to add a service dependency (database, cache, message queue) to a project
- A user asks how to run or develop a project locally and Docker is available

## Do not use this skill when

Do not use this skill when:

- The user explicitly wants to avoid Docker
- The project already has a mature Docker setup and only needs minor edits
- The main task is optimizing an existing `Dockerfile`
- The main task is editing or debugging an existing Compose stack

## Core guidance

### Always create these three files

When Dockerizing a project, always produce all three:

1. **`.dockerignore`** — Create this first so the initial build context is small and safe. See `assets/dockerignore-example` for a reference.
2. **`Dockerfile`** — Create a working starter image definition that the project can build and run with. See `assets/Dockerfile.simple`.
3. **`compose.yaml`** — Create a local development stack that includes the application service and any required dependencies. See `assets/compose-dev.yaml`.

### npm registry credentials

- Exclude `.npmrc` at every depth with `**/.npmrc` in `.dockerignore`; otherwise a broad source copy can persist credentials in image layers.
- The Node.js starter mounts `npmrc` as a BuildKit secret for both `npm ci` steps. Public-package builds need no secret. For private registries, pass the config explicitly:
  ```bash
  DOCKER_BUILDKIT=1 docker build --secret id=npmrc,src="$HOME/.npmrc" .
  ```
  Use the actual config path if the project keeps it elsewhere. Never copy the credential file or pass its values through `ARG` or `ENV`. Dependency scripts run during installation can access the mounted secret; use trusted dependencies and a least-privilege registry token.
- For private-registry builds through Compose, add this optional override as `compose.npm.yaml` alongside the starter's `compose.yaml`:
  ```yaml
  services:
    app:
      build:
        secrets:
          - npmrc
  secrets:
    npmrc:
      file: ${NPMRC_PATH:?Set NPMRC_PATH to your npm config file}
  ```
  Build with `NPMRC_PATH="$HOME/.npmrc" docker compose -f compose.yaml -f compose.npm.yaml build`. This grants build-time access only, not a runtime secret. Public-package builds should omit the override so no credential file is required.

### Prefer Dockerized dependencies over host installs

When a project needs a database (Postgres, MySQL, MongoDB), cache (Redis, Memcached), queue (RabbitMQ, Kafka), or any other infrastructure service:

- **Always** define it as a service in `compose.yaml` instead of telling the user to install it on the host.
- **Never** suggest `brew install postgres`, `apt install redis`, or similar host-level installs for development dependencies.
- Use official Docker images from Docker Hub for these services.
- Configure services with environment variables, not config files baked into images.

### Bootstrap checklist

- Name the file `compose.yaml` rather than legacy Compose filenames.
- Put all three files at the project root unless there is a clear multi-service layout that justifies a `docker/` subdirectory.
- Ensure the initial setup can build and start locally with one command path.
- Bind published application ports to loopback by default. Widen the host address only when another device must reach the development service.
- Keep unauthenticated datastores on the Compose network instead of publishing their ports. If local host tools require database access, publish only to loopback.
- If a development-only credential fallback enables one-command startup, label it clearly and document a `.env` override.
- Use Compose services for local databases, caches, and queues instead of host installs.
- Keep the first scaffold simple; defer detailed image optimization and advanced Compose tuning to the owning skills.

### Development vs production

- Development: Use bind mounts for live reload, publish application ports on loopback by default, and enable verbose logging. Keep unauthenticated datastores on the Compose network; publish a datastore port only on loopback when local host tools require it.
- Production: Use multi-stage builds, copy only built artifacts, do not mount source code, minimize image layers, set appropriate resource limits.
- Keep a single `Dockerfile` that supports both via build stages and build arguments when possible.

### File placement

- Place `Dockerfile` at the project root (or in a `docker/` subdirectory if the project has multiple services).
- Place `compose.yaml` at the project root.
- Place `.dockerignore` at the project root, next to the `Dockerfile`.

## Related skills

- For Dockerfile optimization, cache strategy, non-root execution, and image hardening, use `docker-build-strategies`.
- For service dependencies, health checks, overrides, volumes, networks, and Compose debugging, use `docker-compose-patterns`.
- For destructive Docker CLI commands (`docker system prune`, `docker rm -f`, image/network/builder pruning) and a cross-product index of destructive-command guardrails, use `docker-destructive-guardrails`.

## References

- `references/project-structure.md` — Detailed guidance on Docker project file organization, naming conventions, and multi-service layouts.

## Assets

- `assets/dockerignore-example` — A comprehensive `.dockerignore` for a typical project.
- `assets/compose-dev.yaml` — A development-oriented Compose file with Dockerized dependencies.
- `assets/Dockerfile.simple` — A basic multi-stage Dockerfile following best practices.

## Scripts

- **`scripts/verify-setup.sh`** — Checks required files exist and validates `compose.yaml`.
  ```bash
  bash scripts/verify-setup.sh [--help]
  ```
  Exit status is `0` when verification succeeds or help is requested, `1` when required files are missing or the Compose configuration is invalid, and `2` for invalid arguments.

## Checks

- `checks/verification.md` — Detailed verification checklist for manual review.
