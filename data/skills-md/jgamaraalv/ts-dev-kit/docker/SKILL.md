---
name: docker

description: "Docker containerization reference — multi-stage builds, Compose configs, image optimization, and container security for Yarn 4 monorepos. Use when: (1) creating or optimizing Dockerfiles, (2) configuring docker-compose for dev or production, (3) reducing image size with multi-stage builds, (4) hardening container security, or (5) setting up health checks and resource limits."
---

# Docker — Containerization for Monorepos

Docker best practices for Node.js monorepos with Yarn 4 Berry.

## When to Load References

| Need                                               | Reference file                                                         |
| -------------------------------------------------- | ---------------------------------------------------------------------- |
| Writing or reviewing a Dockerfile for the monorepo | [references/monorepo-dockerfile.md](references/monorepo-dockerfile.md) |
| Configuring docker-compose for dev or production   | [references/compose-configs.md](references/compose-configs.md)         |

## Key Principles

- **Minimal images**: Alpine-based, only runtime dependencies in final stage
- **Layer caching order**: system deps → package manifests → install → source → build
- **Non-root users**: Create `app` user, never run as root in production
- **One process per container**: Compose multiple containers, not multiple processes
- **Health checks on every service**: Use the existing `/health` endpoint

## Image Optimization Quick Reference

- Use `node:22-alpine` as base
- Multi-stage builds: exclude build tools from final image
- `yarn cache clean` after install
- `.dockerignore`: exclude `.git`, `node_modules`, `*.md`, `.env*`, `.claude`, `__tests__`, `coverage`, `.turbo`
- `--production` flag for runtime dependencies only
- Pin base image versions (not just `latest`)

## Container Security Quick Reference

- Run as non-root user (`addgroup --system app && adduser --system --ingroup app app`)
- Don't store secrets in images — use env vars or secrets management
- Scan images: `docker scout cves <image>`
- Set resource limits in compose: `mem_limit`, `cpus`
- Read-only filesystem where possible: `read_only: true`
- Drop capabilities: `cap_drop: [ALL]`

## Useful Commands

```bash
docker compose build api          # Build specific service
docker compose up -d              # Start all services
docker compose logs -f api        # Follow logs
docker compose exec api sh        # Shell into container
docker images | grep myapp    # Check image sizes
docker system df                  # View cache usage
docker system prune -a            # Prune unused images
docker stats                      # Resource usage
```
