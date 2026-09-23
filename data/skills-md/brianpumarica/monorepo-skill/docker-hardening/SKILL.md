---
name: docker-hardening
description: Production-grade security hardening, performance optimization, resource containment, and network diagnostics for Docker & Compose environments on Raspberry Pi 5 and Linux servers. Use whenever securing containerized backends and databases, dropping Linux capabilities, enforcing non-root users, setting CPU/memory limits, optimizing BuildKit cache layers, or troubleshooting container networking and healthchecks.
---

# Docker Production Hardening & Optimization Runbook

This skill provides mandatory security hardening, low-overhead resource optimization, and operational diagnostic patterns for Docker and Docker Compose on Raspberry Pi 5, edge devices, and Linux VPS.

---

## 1. Container Security Hardening Matrix

Apply these security controls in `docker-compose.prod.yml` to prevent privilege escalation and container breakout attacks:

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: apps/api/Dockerfile
      target: production
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true       # Prevents setuid binaries from escalating privileges
    cap_drop:
      - ALL                         # Drops all Linux kernel capabilities
    cap_add:
      - NET_BIND_SERVICE            # Only add back strictly necessary capabilities (if binding <1024)
    deploy:
      resources:
        limits:
          cpus: '2.0'               # Prevent CPU exhaustion on Raspberry Pi
          memory: 512M              # Memory cap to prevent OOM killing the OS
        reservations:
          memory: 128M
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://127.0.0.1:3004/health || exit 1"]
      interval: 15s
      timeout: 3s
      retries: 3
      start_period: 10s
    networks:
      - app-net
```

---

## 2. Dockerfile Hardening Standard (Non-Root & Minimal Attack Surface)

Every production Dockerfile stage MUST drop root permissions:

### Node.js (Alpine) Standard:
```dockerfile
FROM node:20-alpine AS production
RUN apk add --no-cache dumb-init
WORKDIR /app
ENV NODE_ENV=production
COPY --chown=node:node apps/api/dist ./dist
COPY --chown=node:node apps/api/package.json ./
# Run as non-root user built into Alpine
USER node
EXPOSE 3004
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/main.js"]
```

### Python (Slim) Standard:
```dockerfile
FROM python:3.11-slim AS production
# Create non-root system user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin -d /app appuser
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY --chown=appuser:appgroup apps/api /app
USER appuser
EXPOSE 3004
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3004", "--workers", "2"]
```

---

## 3. Raspberry Pi 5 Resource Sizing & Storage Guidelines

| Service | CPU Limit | Memory Limit | Storage Strategy |
| :--- | :--- | :--- | :--- |
| **PostgreSQL / pgvector** | `1.5` | `512M - 1GB` | Named Docker volume on NVMe/fast SSD (Avoid slow SD cards for DB) |
| **Backend (Node / Python)** | `2.0` | `256M - 512M` | Stateless, non-root, ephemeral container layer |
| **Cloudflare Tunnel** | `0.5` | `64M` | Ultra-lightweight daemon |
| **Static Frontend (Nginx)** | `0.5` | `32M` | Single worker process, gzip enabled |

---

## 4. BuildKit Layer Caching Optimization

Speed up builds on ARM64 / Raspberry Pi by caching package manager caches across builds:

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY apps/api/package.json apps/api/
COPY packages/types/package.json packages/types/

# Mount BuildKit persistent cache
RUN --mount=type=cache,id=pnpm,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
```

---

## 5. Network Troubleshooting & Diagnostics Runbook

When containers cannot communicate within `app-net`:

### Test 1: Verify DNS Resolution Between Containers
```bash
# Check if backend can resolve database hostname
docker compose -f docker-compose.prod.yml exec backend getent hosts database
# Or using nslookup if available
docker compose -f docker-compose.prod.yml exec backend nslookup database
```

### Test 2: Verify PostgreSQL Connectivity
```bash
docker compose -f docker-compose.prod.yml exec database pg_isready -U postgres -h 127.0.0.1
```

### Test 3: Inspect Container Health & Resource Usage
```bash
# Check real-time RAM/CPU on Raspberry Pi
docker stats --no-stream

# View health check transition logs
docker inspect --format='{{json .State.Health}}' $(docker compose ps -q backend)
```

---

## 6. Centralized `.dockerignore` Template

Ensure confidential files, build artifacts, and local environments never enter the build context:

```dockerignore
**/.git
**/.github
**/.agent*
**/.gemini
**/node_modules
**/dist
**/.next
**/build
**/.venv
**/__pycache__
**/*.pyc
.env*
!.env.example
*.log
docker-compose*.yml
README.md
docs/
```

---

## 7. Self-Hosted Runner & Production Host Hardening

When deploying via a **GitHub Self-Hosted Runner** on Raspberry Pi / Linux Server:

1. **Strict File Permissions**: Ensure `.env` is locked down to the runner user:
   ```bash
   chmod 600 .env
   ```
2. **Workspace Isolation**: The runner operates in an isolated folder per repository:
   `/home/github-runner/actions-runner/_work/<repository-name>/<repository-name>/`
   Do not mix shared `.env` files across different repository folders.
3. **Container State Re-creation**: Always deploy with `--force-recreate --remove-orphans` so configuration or environment updates are forcefully picked up:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build --force-recreate --remove-orphans
   ```
4. **Remove Unused SSH Secrets**: Self-hosted runners execute locally inside the machine. Remove external SSH secrets (`RASPI_SSH_KEY`, `RASPI_HOST`, `RASPI_USER`) to minimize the attack surface.

---

## 8. Deep-Dive Reference Guides

- [Docker Security Audit & Production Hardening Benchmarks](./references/security-audit-and-benchmarks.md) (CIS benchmarks, kernel sysctls tuning, and Trivy image scanning).

