---
name: read-only-postgres
description: "Execute read-only SQL queries against PostgreSQL databases. Use when: (1) querying PostgreSQL data, (2) exploring schemas/tables, (3) running SELECT queries for analysis, (4) checking database contents. Supports multiple database connections with descriptions for auto-selection. Blocks all write operations (INSERT, UPDATE, DELETE, DROP, etc.) for safety."
---

# PostgreSQL Read-Only Query Skill

Execute safe, read-only queries against configured PostgreSQL databases.

## Requirements

- Python 3.8+
- psycopg2-binary: `pip install -r requirements.txt`

## Setup

Create `connections.json` in the skill directory or `~/.config/claude/read-only-postgres-connections.json`.

**Security**: Set file permissions to `600` since it contains credentials:
```bash
chmod 600 connections.json
```

```json
{
  "databases": [
    {
      "name": "app-db-dev",
      "description": "Primary app database (public schema: users, organizations, orders, order_items, events)",
      "host": "localhost",
      "port": 5432,
      "database": "app_dev",
      "user": "app_user",
      "password": "app_password",
      "sslmode": "disable"
    },
    {
      "name": "app-db-staging",
      "description": "Staging database (same schema as primary app)",
      "host": "localhost",
      "port": 5432,
      "database": "app_staging",
      "user": "app_user",
      "password": "app_password",
      "sslmode": "disable"
    }
  ]
}
```

### Config Fields

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Identifier for the database (case-insensitive) |
| description | Yes | What data this database contains (used for auto-selection) |
| host | Yes | Database hostname |
| port | No | Port number (default: 5432) |
| database | Yes | Database name |
| user | Yes | Username |
| password | Yes | Password |
| sslmode | No | SSL mode: disable, allow, prefer (default), require, verify-ca, verify-full |

## Usage

### List configured databases
```bash
python3 scripts/query.py --list
```

### Query a database
```bash
python3 scripts/query.py --db app-db-dev --query "SELECT id, email, created_at FROM users LIMIT 10"
```

### List tables
```bash
python3 scripts/query.py --db app-db-dev --tables
```

### Show schema
```bash
python3 scripts/query.py --db app-db-dev --schema
```

### Limit results
```bash
python3 scripts/query.py --db app-db-dev --query "SELECT id, status, total_amount FROM orders" --limit 100
```

## Database Selection

Match user intent to database `description`:

| User asks about | Look for description containing |
|-----------------|--------------------------------|
| users, accounts | users, accounts |
| organizations, teams | organizations, teams |
| orders, payments | orders, payments |
| events, audit logs | events, audit, logs |
| analytics or reporting | analytics, reporting |
| background jobs or queues | jobs, queue, outbox |

If unclear, run `--list` and ask user which database.

## Safety Features

- **Read-only session**: Connection uses PostgreSQL `readonly=True` mode (primary protection)
- **Query validation**: Only SELECT, SHOW, EXPLAIN, WITH queries allowed (comments/literals stripped; DDL/DML keywords, data-modifying CTEs, SELECT INTO, and sequence mutation functions blocked)
- **Single statement**: Multiple statements per query rejected
- **SSL support**: Configurable SSL mode for encrypted connections
- **Query timeout**: 30-second statement timeout enforced
- **Memory protection**: Max 10,000 rows per query to prevent OOM
- **Column width cap**: 100 char max per column for readable output
- **Credential sanitization**: Error messages don't leak passwords

## Troubleshooting

| Error | Solution |
|-------|----------|
| Config not found | Create `connections.json` in skill directory |
| Authentication failed | Check username/password in config |
| Connection timeout | Verify host/port, check firewall/VPN |
| SSL error | Try `"sslmode": "disable"` for local databases |
| Permission warning | Run `chmod 600 connections.json` |

## Exit Codes

- **0**: Success
- **1**: Error (config missing, auth failed, invalid query, database error)

## Workflow

1. Run `--list` to show available databases
2. Match user intent to database description
3. Run `--tables` or `--schema` to explore structure
4. Execute query with appropriate LIMIT
