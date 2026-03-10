---
name: docker-vps-2026
description: >
  Docker best practices for VPS deployments in 2026. Use this skill when writing Dockerfiles,
  docker-compose.yml, or managing containers on a Linux VPS. Covers multi-stage builds,
  uv-based Python images, Xvfb/virtual display containers, volume management, security
  hardening, and service orchestration with Docker Compose v2. NEVER use legacy
  docker-compose v1 (hyphenated), old Python base images, or root containers.
---

# Docker + VPS 2026 — Best Practices

## Docker Compose v2 (2026 Standard)
```bash
# ✅ 2026 — Docker Compose v2 (built into Docker)
docker compose up -d
docker compose build
docker compose logs -f service-name

# ❌ Legacy v1 (deprecated, removed in 2024)
docker-compose up   # hyphenated — never use
```

## Python Container (uv-based, 2026)
```dockerfile
FROM python:3.12-slim-bookworm

# Copy uv from official image — always pin the version tag
COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /uvx /bin/

WORKDIR /app

# Layer cache: install deps before copying app code
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
# Never run as root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "api.main"]
```

## Browser Automation Container (Xvfb + Camoufox)
```dockerfile
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /uvx /bin/

# System deps for Firefox + virtual display
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc \
    libgtk-3-0 libdbus-glib-1-2 libxt6 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libasound2 libpangocairo-1.0-0 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 \
    curl procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Download Camoufox Firefox binary
# ⚠️  Verify the expected version in pyproject.toml; camoufox fetch downloads
#    a pre-built Firefox binary — pin the camoufox package version in uv.lock
#    and validate the download hash when possible.
RUN uv run python -m camoufox fetch

COPY . .
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

## Docker Compose — Full Stack
```yaml
# docker-compose.yml
services:
  browser:
    build:
      context: ./browser
      dockerfile: Dockerfile
    container_name: threads-browser
    restart: unless-stopped
    environment:
      DISPLAY: ":99"
      SCREEN_RES: "1920x1080x24"
    ports:
      - "127.0.0.1:5900:5900"  # VNC — bind to localhost only!
    volumes:
      - ./sessions:/sessions
      - /dev/shm:/dev/shm     # shared memory for Firefox
    shm_size: "2gb"

  api:
    build:
      context: ./api
    container_name: threads-api
    restart: unless-stopped
    environment:
      SESSION_DIR: /sessions
    ports:
      - "127.0.0.1:8000:8000"  # bind to localhost only — Nginx handles external
    volumes:
      - ./sessions:/sessions
    depends_on:
      - browser

  dashboard:
    build:
      context: ./dashboard
    container_name: threads-dashboard
    restart: unless-stopped
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "127.0.0.1:3000:3000"

  nginx:
    image: nginx:1.28.2-alpine3.23  # pin stable — never use bare :alpine/:latest
    container_name: threads-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl:ro
```

## Security Rules (2026)
```yaml
# ✅ Never expose internal services directly to internet
ports:
  - "127.0.0.1:8000:8000"  # only localhost — Nginx proxies externally

# ❌ Never do this
ports:
  - "8000:8000"  # exposes to all interfaces
```

> [!CAUTION]
> The commands below **modify host-level firewall rules** and require root
> privileges. Never run them unattended in CI or automated scripts. Review
> and execute manually on the target VPS only.

```bash
# UFW rules on VPS (manual — requires human review)
sudo ufw default deny incoming
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw deny 5900      # Block VNC from outside after first use
sudo ufw enable
```

## Volume Strategy
```yaml
volumes:
  - ./sessions:/sessions      # named bind mount — survives container rebuild
  - /dev/shm:/dev/shm         # shared memory — required for Firefox stability
```

```bash
# Never lose sessions: backup before any docker operations
tar -czf sessions-backup-$(date +%Y%m%d).tar.gz ./sessions/
```

## Useful Commands (2026)
```bash
# Build and start all services
docker compose up -d --build

# Tail logs for a specific service
docker compose logs -f browser

# Shell into running container
docker exec -it threads-browser bash

# Check resource usage
docker stats

# Restart single service without rebuilding
docker compose restart api

# Full teardown (preserves volumes)
docker compose down

# Full teardown including volumes — DANGER, deletes sessions
docker compose down -v
```

## Health Checks
```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

## .dockerignore
```
.venv/
__pycache__/
*.pyc
.env
.git/
node_modules/
sessions/
*.log
```

## Anti-Patterns
```dockerfile
# ❌ Never run as root in production
CMD ["python", "app.py"]  # without USER directive — runs as root

# ❌ Never use latest tag for base images in production
FROM python:latest

# ❌ Never install pip packages globally in 2026 Dockerfiles
RUN pip install fastapi  # use uv instead

# ❌ Never copy all files before installing deps (kills layer cache)
COPY . .
RUN uv sync  # every code change invalidates dep cache
```

## References
- Docker Compose v2: https://docs.docker.com/compose/
- uv Docker: https://docs.astral.sh/uv/guides/integration/docker/
