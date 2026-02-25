---
name: docker
description: |
  Docker containerization for development and production. Covers Dockerfiles, multi-stage builds, layer caching, Compose services, networking, volumes, health checks, security hardening, and production deployment patterns.

  Use when writing Dockerfiles, optimizing image size, configuring Compose services, debugging container networking, setting up health checks, hardening containers for production, or troubleshooting build cache issues.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://docs.docker.com'
user-invocable: false
---

# Docker

## Overview

Docker packages applications into isolated containers that run consistently across environments. A Dockerfile defines the image build steps, Compose orchestrates multi-container services, and production patterns ensure small, secure, performant images.

**When to use:** Containerizing applications, creating reproducible dev environments, orchestrating multi-service stacks, deploying to container platforms (ECS, Kubernetes, Fly.io, Railway, Coolify).

**When NOT to use:** Simple static sites with no backend (use CDN deploy), single-binary CLI tools (distribute the binary), or when the target platform has native buildpacks (Heroku, Vercel) and you don't need container control.

## Quick Reference

| Pattern              | Approach                                       | Key Points                                           |
| -------------------- | ---------------------------------------------- | ---------------------------------------------------- |
| Multi-stage build    | Separate `builder` and `production` stages     | 80%+ image size reduction, no dev deps in production |
| Layer caching        | Copy lockfile first, install, then copy source | Dependency layer cached across builds                |
| Non-root user        | `RUN adduser` + `USER` in final stage          | Never run production containers as root              |
| Health check         | `HEALTHCHECK CMD curl` or node/python check    | Enables orchestrator restart on failure              |
| `.dockerignore`      | Exclude `node_modules`, `.git`, `.env`         | Smaller build context, faster builds                 |
| Compose services     | `compose.yaml` with service definitions        | Dev environment in one command                       |
| Compose override     | `compose.prod.yaml` with production settings   | Environment-specific config without duplication      |
| Named volumes        | `volumes:` in Compose for persistent data      | Survives container recreation                        |
| Build cache mount    | `RUN --mount=type=cache,target=/root/.npm`     | Persistent cache across builds                       |
| Secrets in build     | `RUN --mount=type=secret,id=token`             | Never bake secrets into image layers                 |
| Image pinning        | Pin to major.minor or digest                   | Reproducible builds, avoid surprise breakage         |
| Container networking | Custom bridge networks with service discovery  | Containers resolve each other by service name        |
| Compose watch        | `develop.watch` with sync/rebuild actions      | Live reload without volume mounts                    |
| Init process         | `--init` flag or `tini` entrypoint             | Proper signal handling and zombie reaping            |
| Multi-platform       | `docker buildx build --platform`               | ARM (Apple Silicon, Graviton) + x86 in one image     |
| Monorepo prune       | `turbo prune app --docker`                     | Minimal build context from workspace dependencies    |
| CI layer caching     | `cache-from`/`cache-to` with GHA or registry   | Avoid full rebuilds in CI pipelines                  |
| Debug containers     | `docker exec`, `docker logs`, `dive`           | Inspect running containers and image layers          |

## Common Mistakes

| Mistake                                         | Correct Pattern                                                  |
| ----------------------------------------------- | ---------------------------------------------------------------- |
| Installing dev dependencies in production image | Multi-stage build: install in builder, copy artifacts to runtime |
| Copying source before installing dependencies   | Copy lockfile first, `npm ci`, then copy source for cache reuse  |
| Running as root in production                   | Create non-root user, `USER` directive in final stage            |
| Hardcoding secrets in Dockerfile or ENV         | Use build secrets (`--mount=type=secret`) or runtime env         |
| Using `latest` tag for base images              | Pin to specific version (`node:24-alpine`)                       |
| No `.dockerignore` file                         | Exclude `node_modules`, `.git`, `.env`, build artifacts          |
| Using `npm install` instead of `npm ci`         | `npm ci` for deterministic, lockfile-based installs              |
| HEALTHCHECK missing                             | Add health check for orchestrator integration                    |
| Large base images (`node:24`)                   | Use alpine variants (`node:24-alpine`) for smaller images        |
| Ignoring `.env` file precedence in Compose      | `environment:` in Compose overrides `.env` file values           |
| Building entire monorepo for one service        | Use `turbo prune --docker` for minimal build context             |
| No layer caching in CI                          | Use `cache-from`/`cache-to` with GHA or registry backend         |
| Building only for x86 when deploying to ARM     | Use `docker buildx` with `--platform linux/amd64,linux/arm64`    |

## Delegation

- **Dockerfile review**: Use `Task` agent to audit Dockerfiles for size, security, and caching
- **Compose exploration**: Use `Explore` agent to discover existing Docker configurations
- **Architecture decisions**: Use `Plan` agent for container orchestration strategy

> If the `ci-cd-architecture` skill is available, delegate CI/CD pipeline and deployment strategy to it.
> If the `application-security` skill is available, delegate container security scanning and hardening review to it.

## References

- [Dockerfile patterns: multi-stage builds, layer caching, and image optimization](references/dockerfile-patterns.md)
- [Compose: services, networking, volumes, and environment management](references/compose.md)
- [Security: non-root users, secrets, scanning, and production hardening](references/security.md)
- [Buildx: multi-platform builds for ARM and x86](references/buildx-and-multiplatform.md)
- [CI: GitHub Actions caching, registry push, and automated builds](references/ci-caching.md)
- [Monorepo: Turborepo prune, pnpm workspaces, and selective builds](references/monorepo-builds.md)
- [Debugging: logs, exec, inspect, layer analysis, and network troubleshooting](references/debugging.md)
