---
name: constructive-deployment
description: Deploy the Constructive platform locally and to production using Docker Compose, pgpm, and the Constructive CLI. Use when asked to "deploy constructive", "set up docker compose", "run constructive locally", "deploy to production", or when working with the constructive monorepo's Docker and infrastructure files.
compatibility: Docker, Docker Compose, pgpm CLI, Node.js 22+, PostgreSQL 17+
metadata:
  author: constructive-io
---

# Constructive Deployment

How to deploy the Constructive platform — local development with Docker Compose, database migrations with pgpm, and production container builds.

## When to Apply

Use this skill when:
- Setting up the Constructive monorepo for local development
- Running Docker Compose services (Postgres, MinIO, API servers)
- Building the Constructive Docker image
- Deploying database migrations to local or remote Postgres
- Understanding the Makefile targets and service architecture

## Local Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 22+ with pnpm
- pgpm CLI (available from the constructive monorepo)

### Quick Start

```bash
# 1. Start Postgres and MinIO containers
make up
# OR: docker-compose up -d

# 2. Bootstrap database roles (ensure PG env vars are loaded — see pgpm-env skill)
pgpm admin-users bootstrap --yes

# 3. Deploy all database modules
pgpm deploy --createdb --workspace --all --yes
```

### Stopping

```bash
# Stop and remove containers + volumes
make down
# OR: docker-compose down -v
```

## Docker Compose Services

### Core Services (docker-compose.yml)

| Service | Container | Image | Port | Purpose |
|---------|-----------|-------|------|---------|
| `postgres` | `postgres` | `ghcr.io/constructive-io/docker/postgres-plus:17` | 5432 | PostgreSQL database |
| `minio` | `minio` | `minio/minio` | 9000 | S3-compatible object storage |

**Postgres credentials:** `postgres` / `password` (local dev only)

### Application Services (docker-compose.jobs.yml)

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| `constructive-admin-server` | `constructive-admin-server` | 3002 | Internal admin GraphQL API (header-based routing) |
| `constructive-server` | `constructive-server` | 3000 | Public GraphQL API (domain-based routing) |
| `send-email-link` | `send-email-link` | — | Email function (invite, password reset, verification) |

### Running Application Services

The application services require a built Docker image:

```bash
# Build the constructive image
docker-compose -f docker-compose.jobs.yml build

# Start all application services
docker-compose -f docker-compose.jobs.yml up -d
```

## Postgres Images

| Image | Use Case |
|-------|----------|
| `ghcr.io/constructive-io/docker/postgres-plus:17` | **Recommended** — includes all extensions needed by constructive |
| `pyramation/postgres:17` | Lightweight alternative with common extensions |

**PostgreSQL 17+ is required** for `security_invoker` views. Older images will fail with "unrecognized parameter security_invoker" errors.

## Database Deployment

### Deploy to Local Database

> **Prerequisite:** Ensure PostgreSQL is running and PG env vars are loaded. See `pgpm-docker` and `pgpm-env` skills.

```bash
pgpm deploy --createdb --workspace --all --yes
```

### Deploy to Remote Database

Point pgpm at a remote Postgres instance via environment variables:

```bash
export PGHOST=remote-host.example.com
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=secure-password
export PGDATABASE=constructive

pgpm deploy --workspace --all --yes
```

### Verify Deployment

```bash
pgpm verify
```

### Revert (Rollback)

```bash
# Revert last change
pgpm revert --yes

# Revert to a tagged release
pgpm revert --to @v1.0.0 --yes

# Revert everything
pgpm revert --all --yes
```

## Docker Image Build

The Constructive monorepo builds a multi-stage Docker image:

### Build Stages

1. **`build` stage** — Node.js 22, installs pnpm, runs `pnpm install --frozen-lockfile` and `pnpm run build`
2. **`constructive` stage** — Runtime image with built artifacts, PostgreSQL client, and CLI shims

### CLI Shims

The Docker image exposes three CLI commands:

| Command | Maps To |
|---------|---------|
| `constructive` | `node /app/packages/cli/dist/index.js` |
| `cnc` | `node /app/packages/cli/dist/index.js` |
| `pgpm` | `node /app/pgpm/pgpm/dist/index.js` |

### Building Locally

```bash
docker build -t constructive:dev .
```

## Makefile Targets

| Target | Command | Purpose |
|--------|---------|---------|
| `make up` | `docker-compose up -d` | Start Postgres + MinIO |
| `make down` | `docker-compose down -v` | Stop and clean up |
| `make ssh` | `docker exec -it postgres /bin/bash` | Shell into Postgres container |
| `make roles` | `pgpm admin-users bootstrap/add` | Bootstrap database roles |
| `make install` | `docker exec postgres /sql-bin/install.sh` | Run install script in container |

## Environment Variables

### Server Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `API_IS_PUBLIC` | `true` for public API, `false` for admin (header-based) | `true` |
| `API_EXPOSED_SCHEMAS` | Comma-separated schemas to expose via GraphQL | `metaschema_public,services_public` |
| `API_ANON_ROLE` | PostgreSQL role for unauthenticated requests | `anonymous` |
| `API_ROLE_NAME` | PostgreSQL role for authenticated requests | `authenticated` |
| `API_ENABLE_SERVICES` | Enable services schema (admin only) | `true` |
| `API_META_SCHEMAS` | Meta schemas for validation and routing | `metaschema_public,services_public` |
| `SERVER_HOST` | Server bind address | `0.0.0.0` |
| `SERVER_ORIGIN` | CORS origin | `*` |
| `SERVER_TRUST_PROXY` | Trust reverse proxy headers | `true` |
| `SERVER_STRICT_AUTH` | Enforce strict authentication | `false` |

### Database Connection

| Variable | Description | Default |
|----------|-------------|---------|
| `PGHOST` | PostgreSQL host | `localhost` |
| `PGPORT` | PostgreSQL port | `5432` |
| `PGUSER` | PostgreSQL user | `postgres` |
| `PGPASSWORD` | PostgreSQL password | `password` |
| `PGDATABASE` | Target database name | — |

### Admin vs Public API

The Constructive platform runs two API servers:

- **Admin server** (`API_IS_PUBLIC=false`, port 3002) — uses header-based routing (`X-Api-Name`, `X-Database-Id`, `X-Meta-Schema`). Used internally by the Constructive admin UI.
- **Public server** (`API_IS_PUBLIC=true`, port 3000) — uses domain-based routing. Serves external client applications.

## Networking

All Docker Compose services share the `constructive-net` network, allowing inter-service communication by container name (e.g., `postgres:5432` from within the `constructive-server` container).

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Port 5432 in use | Another Postgres instance running | Stop it or change the port in `docker-compose.yml` |
| `security_invoker` error | Postgres version < 17 | Use `postgres-plus:17` or `pyramation/postgres:17` image |
| `role "authenticated" does not exist` | Missing bootstrap | Run `pgpm admin-users bootstrap --yes` |
| Container not on network | Network mismatch | Check `docker network ls` for `constructive-net` |
| Build fails at `pnpm install` | Lockfile mismatch | Run `pnpm install` locally first to update lockfile |
