---
name: pgpm-docker
description: Manage PostgreSQL Docker containers for local development using pgpm docker commands. Use when asked to "start postgres", "run database locally", "set up local database", "stop postgres container", or when needing a PostgreSQL database for development/testing.
compatibility: Docker installed and running, Node.js 18+, pgpm CLI available
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PGPM Docker

Manage PostgreSQL Docker containers for local development using the `pgpm docker` command.

## When to Apply

Use this skill when:
- Setting up a local PostgreSQL database for development
- Starting or stopping PostgreSQL containers
- Recreating a fresh database container
- User asks to run tests that need a database
- Troubleshooting database connection issues

## Quick Start

### Start PostgreSQL Container

```bash
pgpm docker start
```

This starts a PostgreSQL 17 container with default settings:
- Container name: `postgres`
- Port: `5432`
- User: `postgres`
- Password: `password`

### Start with Custom Options

```bash
pgpm docker start --port 5433 --name my-postgres
```

### Recreate Container (Fresh Database)

```bash
pgpm docker start --recreate
```

### Stop Container

```bash
pgpm docker stop
```

## Command Reference

### pgpm docker start

Start a PostgreSQL Docker container.

| Option | Description | Default |
|--------|-------------|---------|
| `--name <name>` | Container name | `postgres` |
| `--image <image>` | Docker image | `pyramation/postgres:17` |
| `--port <port>` | Host port mapping | `5432` |
| `--user <user>` | PostgreSQL user | `postgres` |
| `--password <pass>` | PostgreSQL password | `password` |
| `--recreate` | Remove and recreate container | `false` |

### pgpm docker stop

Stop a running PostgreSQL container.

| Option | Description | Default |
|--------|-------------|---------|
| `--name <name>` | Container name to stop | `postgres` |

## Common Workflows

### Development Setup

```bash
# Start fresh database
pgpm docker start --recreate

# Load environment variables
eval "$(pgpm env)"

# Deploy your PGPM modules
pgpm deploy
```

### Running Tests

```bash
# Ensure database is running
pgpm docker start

# Run tests with environment
pgpm env pnpm test
```

### Multiple Databases

```bash
# Start main database on default port
pgpm docker start --name main-db

# Start test database on different port
pgpm docker start --name test-db --port 5433
```

## PostgreSQL Version

The default image `pyramation/postgres:17` includes PostgreSQL 17 which is required for:
- `security_invoker` views
- Latest PostgreSQL features used by Constructive

If you see errors like "unrecognized parameter security_invoker", ensure you're using PostgreSQL 17+.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Docker is not installed" | Install Docker Desktop or Docker Engine |
| "Port already in use" | Use `--port` to specify a different port, or stop the conflicting container |
| Container won't start | Check `docker logs postgres` for errors |
| "Container already exists" | Use `--recreate` to remove and recreate |
| Permission denied | Ensure Docker daemon is running and user has permissions |

## Environment Variables

After starting the container, use `pgpm env` to set up environment variables:

```bash
eval "$(pgpm env)"
```

This sets:
- `PGHOST=localhost`
- `PGPORT=5432`
- `PGUSER=postgres`
- `PGPASSWORD=password`
- `PGDATABASE=postgres`

## References

For related skills:
- Environment management: See `pgpm-env` skill
- Running tests: See `pgpm-testing` skill
