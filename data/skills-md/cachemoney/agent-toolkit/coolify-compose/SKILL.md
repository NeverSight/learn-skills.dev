---
name: coolify-compose
description: Convert Docker Compose files to Coolify templates. Use when creating Coolify services, converting docker-compose.yml for Coolify deployment, working with SERVICE_URL/SERVICE_PASSWORD magic variables, or troubleshooting Coolify compose errors.
---

# Coolify Docker Compose

Convert standard Docker Compose files into Coolify-compatible templates with automatic credential generation, dynamic URLs, and one-click deployment.

## Two Deployment Modes

Coolify supports two ways to deploy compose files with different capabilities:

### 1. Raw Compose (Paste Content)

Paste compose YAML directly into Coolify's UI. **Limited feature set:**

| Feature | Supported |
|---------|-----------|
| `image:` | ✅ Yes |
| `build:` | ❌ No - must use pre-built images |
| External config files | ❌ No - must use inline `content:` |
| YAML anchors (`&`, `*`) | ✅ Yes - resolved by YAML parser |
| Coolify magic variables | ✅ Yes |
| `content:` for inline files | ✅ Yes |

**Use when:** Quick deployments, simple services, no custom images needed.

### 2. Repository Mode (Git URL)

Point Coolify to a Git repository containing your compose file. **Full Docker Compose features:**

| Feature | Supported |
|---------|-----------|
| `image:` | ✅ Yes |
| `build:` | ✅ Yes - builds from Dockerfile in repo |
| External config files | ✅ Yes - relative paths work |
| Coolify magic variables | ✅ Yes |
| `content:` for inline files | ✅ Yes |

**Use when:** Custom images needed, complex multi-file setups, existing docker-compose.yml in a repo.

**Repository setup:**
```
my-service/
├── compose.yml          # or docker-compose.yml
├── custom-image/
│   ├── Dockerfile
│   └── config.sql
└── other-files/
```

```yaml
# compose.yml - can use build:
services:
  app:
    build:
      context: ./custom-image
      dockerfile: Dockerfile
```

### Which Mode to Use?

| Original compose has... | Recommended mode |
|------------------------|------------------|
| Only `image:` references | Either works |
| `build:` directives | Repository mode |
| External config files to mount | Repository mode (or use `content:` in raw) |
| Single simple service | Raw mode is faster |

## Quick Start

Every Coolify template needs a header and magic variables:

```yaml
# documentation: https://example.com/docs
# slogan: Brief description of the service
# category: backend
# tags: api, database, docker
# logo: svgs/myservice.svg
# port: 3000

services:
  app:
    image: myapp:latest
    environment:
      - SERVICE_URL_APP_3000           # Generates URL, routes proxy to port 3000
      - DATABASE_URL=postgres://${SERVICE_USER_POSTGRES}:${SERVICE_PASSWORD_POSTGRES}@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 5s
      timeout: 10s
      retries: 10

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=$SERVICE_USER_POSTGRES
      - POSTGRES_PASSWORD=$SERVICE_PASSWORD_POSTGRES
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 5s
      timeout: 10s
      retries: 10
```

## Conversion Checklist

When converting a standard `docker-compose.yml`:

### 0. Check for `build:` Directives

If the compose has `build:` entries:
- **Repository mode:** Keep them. Coolify will build from the Dockerfile.
- **Raw mode:** Replace with pre-built `image:` references or find equivalent images.

```yaml
# Original with build:
services:
  custom-db:
    build: ./custom-postgres

# Raw mode: find or create pre-built image
  custom-db:
    image: your-registry.com/custom-postgres:latest

# Repository mode: keep build:, include Dockerfile in repo
  custom-db:
    build:
      context: ./custom-postgres
      dockerfile: Dockerfile
```

### 1. Add Header Metadata

```yaml
# documentation: https://...    # Required: URL to official docs
# slogan: ...                   # Required: One-line description  
# category: ...                 # Required: backend, cms, monitoring, etc.
# tags: ...                     # Required: Comma-separated search terms
# logo: svgs/....svg            # Required: Path in Coolify's svgs/ folder
# port: ...                     # Recommended: Main service port
```

### 2. Replace Hardcoded Credentials

```yaml
# ❌ Before
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_USER=admin

# ✅ After  
POSTGRES_PASSWORD=$SERVICE_PASSWORD_POSTGRES
POSTGRES_USER=$SERVICE_USER_POSTGRES
```

### 3. Replace URLs with Magic Variables

```yaml
# ❌ Before
APP_URL=https://myapp.example.com

# ✅ After
- SERVICE_URL_APP_3000    # Declares URL + proxy routing
- APP_URL=$SERVICE_URL_APP  # References it
```

### 4. Remove `ports:` for Proxied Services

Coolify's Traefik proxy handles routing. Only keep `ports:` for SSH, UDP, or proxy bypass.

```yaml
# ❌ Before
ports:
  - "3000:3000"

# ✅ After
environment:
  - SERVICE_URL_APP_3000  # Proxy routes to container port 3000
# No ports: needed
```

### 5. Add Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 5s
  timeout: 10s
  retries: 10
```

### 6. Use `depends_on` with Conditions

```yaml
depends_on:
  db:
    condition: service_healthy
```

## Magic Variables Reference

Coolify generates values using `SERVICE_<TYPE>_<IDENTIFIER>`:

| Type | Example | Result |
|------|---------|--------|
| `PASSWORD` | `SERVICE_PASSWORD_DB` | Random password |
| `PASSWORD_64` | `SERVICE_PASSWORD_64_KEY` | 64-char password |
| `USER` | `SERVICE_USER_ADMIN` | Random 16-char string |
| `BASE64_64` | `SERVICE_BASE64_64_SECRET` | 64-char random string |
| `REALBASE64_64` | `SERVICE_REALBASE64_64_JWT` | Actual base64-encoded string |
| `HEX_32` | `SERVICE_HEX_32_KEY` | 64-char hex string |
| `URL` | `SERVICE_URL_APP_3000` | `https://app-uuid.example.com` + proxy |
| `FQDN` | `SERVICE_FQDN_APP` | `app-uuid.example.com` (no scheme, no port suffix) |

### Declaration vs Reference (Critical)

For `SERVICE_URL`, the port suffix configures proxy routing but is **not part of the variable name**:

```yaml
# Declare WITH port suffix (configures proxy to route to port 3000)
- SERVICE_URL_MYAPP_3000

# Reference WITHOUT port suffix (gets the URL value)
- APP_URL=$SERVICE_URL_MYAPP
- WEBHOOK_URL=${SERVICE_URL_MYAPP}/webhooks
```

`SERVICE_FQDN` is automatically available when `SERVICE_URL` is declared — no separate declaration needed:

```yaml
# This single declaration...
- SERVICE_URL_MYAPP_3000

# ...makes BOTH of these available:
- FULL_URL=$SERVICE_URL_MYAPP           # https://myapp-uuid.example.com
- HOSTNAME=${SERVICE_FQDN_MYAPP}        # myapp-uuid.example.com
```

**⚠️ Important:** Use hyphens, not underscores, before port numbers:
```yaml
SERVICE_URL_MY_SERVICE_3000  # ❌ Breaks parsing
SERVICE_URL_MY-SERVICE_3000  # ✅ Works
```

See [references/magic-variables.md](references/magic-variables.md) for complete list.

## Coolify-Specific Extensions

### Create Directory

```yaml
volumes:
  - type: bind
    source: ./data
    target: /app/data
    is_directory: true  # Coolify creates this
```

### Create File with Content

Useful in **raw mode** when you can't reference external files. In **repository mode**, you can just mount files normally.

```yaml
# Raw mode: embed file content inline
volumes:
  - type: bind
    source: ./config.json
    target: /app/config.json
    content: |
      {"key": "${SERVICE_PASSWORD_APP}"}

# Repository mode: reference actual file in repo
volumes:
  - ./config/settings.json:/app/config.json:ro
```

### Exclude from Health Checks

For migration/init containers that exit after running:

```yaml
services:
  migrate:
    command: ["npm", "run", "migrate"]
    exclude_from_hc: true
```

## Common Patterns

### Database Connection

```yaml
environment:
  - DATABASE_URL=postgres://${SERVICE_USER_POSTGRES}:${SERVICE_PASSWORD_POSTGRES}@db:5432/${POSTGRES_DB:-myapp}
```

### Shared Credentials

Same `SERVICE_PASSWORD_*` identifier = same value across all services:

```yaml
services:
  app:
    environment:
      - DB_PASS=$SERVICE_PASSWORD_POSTGRES
  db:
    environment:
      - POSTGRES_PASSWORD=$SERVICE_PASSWORD_POSTGRES  # Same value
```

### Multi-Service URLs

```yaml
services:
  frontend:
    environment:
      - SERVICE_URL_FRONTEND_3000
      - API_URL=$SERVICE_URL_API
  api:
    environment:
      - SERVICE_URL_API_8080=/api  # Path suffix
```

## Health Check Patterns

```yaml
# HTTP
test: ["CMD", "wget", "--spider", "-q", "http://localhost:8080"]

# PostgreSQL
test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]

# MySQL/MariaDB  
test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]

# Redis
test: ["CMD", "redis-cli", "ping"]

# Always pass (use sparingly)
test: ["CMD", "echo", "ok"]
```

## Environment Variable Syntax

```yaml
environment:
  - NODE_ENV=production           # Hardcoded, hidden from UI
  - API_KEY=${API_KEY}            # Editable in UI (empty)
  - LOG_LEVEL=${LOG_LEVEL:-info}  # Editable with default
  - SECRET=${SECRET:?}            # Required - blocks deploy if empty
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No Available Server" error | Check `docker ps` for unhealthy containers; verify healthcheck passes |
| Variables not in Coolify UI | Use `${VAR}` syntax; hardcoded `VAR=value` won't appear |
| Magic variables not generating | Check spelling; ensure `SERVICE_` prefix; verify Coolify v4.0.0-beta.411+ |
| Port routing broken | Use `SERVICE_URL_NAME_PORT`; avoid underscores before port; remove `ports:` |

## Examples

**First, check for an official template:** Many popular services have official Coolify templates at [github.com/coollabsio/coolify/tree/main/templates/compose](https://github.com/coollabsio/coolify/tree/main/templates/compose). If one exists, use it as the reference for correct patterns.

When converting a compose file without an official template, analyze it and use the matching example:

| Compose file has... | Use example |
|---------------------|-------------|
| 1 service, no database | [examples/simple/](examples/simple/) |
| 2 services: app + database (postgres/mysql/mariadb) | [examples/with-database/](examples/with-database/) |
| 3+ services, or mounted config files, or multiple databases | [examples/multi-service/](examples/multi-service/) |

**Quick analysis:**
- Count the `services:` — if just 1, use `simple/`
- Look for `postgres`, `mysql`, `mariadb`, `mongo` images — if 1 database, use `with-database/`
- Look for mounted `.xml`, `.json`, `.yml` config files — if present, use `multi-service/`
- Look for `clickhouse`, `redis`, multiple databases — use `multi-service/`

## References

- [references/magic-variables.md](references/magic-variables.md) — Complete variable type reference
- [references/categories.md](references/categories.md) — Valid category values
- [Official Coolify Compose Docs](https://coolify.io/docs/knowledge-base/docker/compose) — Authoritative documentation
- [Official Service Templates](https://github.com/coollabsio/coolify/tree/main/templates/compose) — Reference implementations for correct patterns
