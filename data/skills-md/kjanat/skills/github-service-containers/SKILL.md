---
name: github-service-containers
description: Configure Docker service containers (Redis, PostgreSQL, etc.) as sidecar services in GitHub Actions workflows for integration testing. Use when adding databases, caches, or message queues to CI workflows, or debugging service container networking and health checks.
license: MIT
metadata:
  author: kjanat
  version: "1.0"
---

# GitHub Actions Service Containers

Run Docker containers (Redis, PostgreSQL, etc.) alongside workflow jobs for
integration testing.

> **Not what you need?** For building Docker container *actions*
> (Dockerfile + action.yml), see the `github-docker-action` skill.

## Prerequisites

- Linux runners only (`ubuntu-latest` or self-hosted Linux with Docker)
- Service containers cannot be used inside composite actions
- Each service is created fresh per job and destroyed when the job completes

## Job Type Decision Tree

Networking depends on whether your job runs in a container or on the runner:

```tree
Where does your job run?
├─ In a container (`container:` key set)
│   ├─ Hostname: service label name (e.g., `redis`, `postgres`)
│   ├─ Port mapping: NOT needed (Docker bridge network)
│   └─ See reference files → "Container Job" sections
│
└─ Directly on runner (no `container:` key)
    ├─ Hostname: `localhost`
    ├─ Port mapping: REQUIRED (e.g., `ports: ['6379:6379']`)
    └─ See reference files → "Runner Job" sections
```

## Quick Reference

| Setting          | Container Job                       | Runner Job                                    |
| ---------------- | ----------------------------------- | --------------------------------------------- |
| `container:`     | Set (e.g., `node:20-bookworm-slim`) | Omitted                                       |
| Service hostname | Label name (`redis`)                | `localhost`                                   |
| `ports:`         | Not needed                          | Required (`'6379:6379'`)                      |
| Dynamic port     | N/A                                 | `${{ job.services.<label>.ports['<port>'] }}` |
| Network          | Docker bridge (automatic)           | Host network via mapped ports                 |

## Minimal Service Definition

```yaml
services:
  redis:
    image: redis
    ports:
      - 6379:6379
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

### Service fields

| Field          | Purpose                                          |
| -------------- | ------------------------------------------------ |
| `image:`       | Docker Hub image (or `ghcr.io/...` for private)  |
| `ports:`       | Host:container port mapping (runner jobs only)   |
| `options:`     | Docker `--health-*` flags for readiness checks   |
| `env:`         | Environment variables passed to the container    |
| `credentials:` | `username:` / `password:` for private registries |

### Port mapping syntax

| Value         | Description                                      |
| ------------- | ------------------------------------------------ |
| `8080:80`     | Maps container TCP port 80 to host port 8080     |
| `8080:80/udp` | Maps container UDP port 80 to host port 8080     |
| `8080/udp`    | Maps random host port to container UDP port 8080 |

## Private Registry Authentication

```yaml
services:
  db:
    image: ghcr.io/org/private-image:latest
    credentials:
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
  cache:
    image: redis
    credentials:
      username: ${{ secrets.DOCKERHUB_USERNAME }}
      password: ${{ secrets.DOCKERHUB_PASSWORD }}
```

## Health Checks

Always define health checks — without them, job steps start before the
service is ready.

| Service    | Health command       | Reference                                             |
| ---------- | -------------------- | ----------------------------------------------------- |
| Redis      | `redis-cli ping`     | [redis-service.md](references/redis-service.md)       |
| PostgreSQL | `pg_isready`         | [postgres-service.md](references/postgres-service.md) |
| Generic    | `curl -f http://...` | Adapt per service                                     |

Common health check options:

```yaml
options: >-
  --health-cmd "<command>"
  --health-interval 10s
  --health-timeout 5s
  --health-retries 5
```

## Reading Order

| Task                        | Files to Read                        |
| --------------------------- | ------------------------------------ |
| Add Redis to CI             | SKILL.md + redis-service.md          |
| Add PostgreSQL to CI        | SKILL.md + postgres-service.md       |
| Debug networking issues     | SKILL.md (decision tree + quick ref) |
| Add other service (generic) | SKILL.md (minimal definition)        |

## In This Reference

| File                                                  | Purpose                                |
| ----------------------------------------------------- | -------------------------------------- |
| [redis-service.md](references/redis-service.md)       | Redis config, health checks, test      |
| [postgres-service.md](references/postgres-service.md) | PostgreSQL config, health checks, test |

## Gotchas

- **Windows/macOS runners**: Service containers are Linux-only
- **Missing health checks**: Steps start immediately; service may not be ready
- **Port conflicts**: Two services mapping the same host port fail silently
- **`container:` + `ports:`**: Port mapping is ignored in container jobs (bridge handles it)
- **Dynamic ports**: Omit host port (`- 6379`) then read via `job.services.<label>.ports['6379']`
- **Composite actions**: Service containers cannot be created inside composite actions
