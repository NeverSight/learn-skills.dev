---
name: pgpm-env
description: Manage PostgreSQL environment variables with profile support using pgpm env commands. Use when asked to "set up database environment", "load postgres env vars", "run command with database connection", "use supabase locally", or when needing to configure database connection for commands.
compatibility: Node.js 18+, pgpm CLI available
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PGPM Env

Manage PostgreSQL environment variables with profile support using the `pgpm env` command.

## When to Apply

Use this skill when:
- Setting up environment variables for database connections
- Running commands that need PostgreSQL connection info
- Switching between local Postgres and Supabase profiles
- Deploying PGPM modules with correct database settings
- Running tests or scripts that need database access

## Quick Start

### Load Environment Variables

```bash
eval "$(pgpm env)"
```

This sets the following environment variables:
- `PGHOST=localhost`
- `PGPORT=5432`
- `PGUSER=postgres`
- `PGPASSWORD=password`
- `PGDATABASE=postgres`

### Run Command with Environment

```bash
pgpm env pgpm deploy --database mydb
```

This runs `pgpm deploy --database mydb` with the PostgreSQL environment variables automatically set.

## Profiles

### Default Profile (Local Postgres)

```bash
eval "$(pgpm env)"
```

| Variable | Value |
|----------|-------|
| `PGHOST` | `localhost` |
| `PGPORT` | `5432` |
| `PGUSER` | `postgres` |
| `PGPASSWORD` | `password` |
| `PGDATABASE` | `postgres` |

### Supabase Profile

```bash
eval "$(pgpm env --supabase)"
```

| Variable | Value |
|----------|-------|
| `PGHOST` | `localhost` |
| `PGPORT` | `54322` |
| `PGUSER` | `supabase_admin` |
| `PGPASSWORD` | `postgres` |
| `PGDATABASE` | `postgres` |

## Command Reference

### Print Environment Exports

```bash
pgpm env                    # Default Postgres profile
pgpm env --supabase         # Supabase profile
```

Output (for shell evaluation):
```bash
export PGHOST="localhost"
export PGPORT="5432"
export PGUSER="postgres"
export PGPASSWORD="password"
export PGDATABASE="postgres"
```

### Execute Command with Environment

```bash
pgpm env <command> [args...]
pgpm env --supabase <command> [args...]
```

Examples:
```bash
pgpm env createdb mydb
pgpm env pgpm deploy --database mydb
pgpm env psql -c "SELECT 1"
pgpm env --supabase pgpm deploy --database mydb
```

## Common Workflows

### Development Setup

```bash
# Start database container
pgpm docker start

# Load environment into current shell
eval "$(pgpm env)"

# Now all commands have database access
createdb myapp
pgpm deploy --database myapp
```

### Running Tests

```bash
# Run tests with database environment
pgpm env pnpm test

# Or load into shell first
eval "$(pgpm env)"
pnpm test
```

### PGPM Deployment

```bash
# Deploy to a specific database
pgpm env pgpm deploy --database constructive

# Verify deployment
pgpm env pgpm verify --database constructive
```

### Supabase Local Development

```bash
# Start Supabase locally (using supabase CLI)
supabase start

# Load Supabase environment
eval "$(pgpm env --supabase)"

# Deploy modules to Supabase
pgpm deploy --database postgres
```

## Shell Integration

### Bash/Zsh

Add to your shell profile for automatic loading:

```bash
# ~/.bashrc or ~/.zshrc
alias pgenv='eval "$(pgpm env)"'
alias pgenv-supa='eval "$(pgpm env --supabase)"'
```

Then use:
```bash
pgenv          # Load default Postgres env
pgenv-supa     # Load Supabase env
```

### One-liner Commands

```bash
# Create database and deploy in one command
pgpm env bash -c "createdb mydb && pgpm deploy --database mydb"
```

## Environment Variables Reference

The `pgpm env` command sets standard PostgreSQL environment variables that are recognized by:
- `psql` and other PostgreSQL CLI tools
- Node.js `pg` library
- PGPM CLI commands
- Any tool using libpq

| Variable | Description |
|----------|-------------|
| `PGHOST` | Database server hostname |
| `PGPORT` | Database server port |
| `PGUSER` | Database username |
| `PGPASSWORD` | Database password |
| `PGDATABASE` | Default database name |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Ensure database container is running with `pgpm docker start` |
| Wrong database | Check `PGDATABASE` or specify `--database` flag |
| Auth failed | Verify password matches container settings |
| Supabase not connecting | Ensure Supabase is running on port 54322 |
| Env vars not persisting | Use `eval "$(pgpm env)"` to load into current shell |

## References

For related skills:
- Docker container management: See `pgpm-docker` skill
- Running tests: See `pgpm-testing` skill
