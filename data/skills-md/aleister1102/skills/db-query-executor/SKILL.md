---
name: db-query-executor
description: Use when executing database queries in development containers for data operations, migrations, cleanup, or maintenance tasks. Helps inspect, modify, and troubleshoot database contents across any database type.
---

# Db Query Executor

## Overview

Execute database queries directly in development containers to perform data operations, migrations, cleanup, and maintenance tasks. This skill provides tools to inspect, modify, and troubleshoot database contents for PostgreSQL, MySQL, MongoDB, and Redis.

## Quick Start

1. Identify the target container (database service name)
2. Set database connection environment variables
3. Execute queries to inspect or modify data
4. Verify changes

## Common Tasks

### Execute Raw SQL/Commands
- "Run a SQL query against the postgres container"
- "Execute a query to list all tables in the database"
- "Get all records from a specific collection"

### Data Inspection
- "Show me all records in the users table"
- "List all collections in the MongoDB database"
- "Check Redis keys matching a pattern"

### Data Modification
- "Update all records in a table"
- "Delete orphaned records from the database"
- "Reset a specific field value"

### Data Cleanup
- "Clean up test data for a specific environment"
- "Remove expired sessions from the database"
- "Delete duplicate records"

## Usage

### Prerequisites
- Docker or container runtime access
- Database credentials (stored in environment variables)
- Container name or service identifier

### Environment Variables
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432 for PostgreSQL)
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `CONTAINER_NAME`: Target container name (optional, auto-detected if not specified)

### Supported Databases
- PostgreSQL
- MySQL
- MongoDB
- Redis

## Scripts

### scripts/db_query.py
Execute database queries against running containers.

**Usage:**
```bash
python scripts/db_query.py --container <name> --query "<sql>" [--type <db_type>] [--output <format>]
```

**Options:**
- `--container`: Target container name
- `--query`: SQL query or database command to execute
- `--type`: Database type (postgres, mysql, mongodb, redis)
- `--output`: Output format (table, json, csv)

### scripts/db_inspect.py
Inspect database structure and contents.

**Usage:**
```bash
python scripts/db_inspect.py --container <name> [--type <db_type>] [--list-tables] [--list-collections] [--sample <table>]
```

**Options:**
- `--container`: Target container name
- `--type`: Database type (postgres, mysql, mongodb, redis)
- `--list-tables`: List all tables (PostgreSQL/MySQL)
- `--list-collections`: List all collections (MongoDB)
- `--sample <table>`: Show sample records from a table/collection

### scripts/db_cleanup.py
Clean up data based on patterns or conditions.

**Usage:**
```bash
python scripts/db_cleanup.py --container <name> [--type <db_type>] [--dry-run] [--pattern <regex>] [--older-than <days>]
```

**Options:**
- `--container`: Target container name
- `--type`: Database type (postgres, mysql, mongodb, redis)
- `--dry-run`: Show what would be deleted without making changes
- `--pattern <regex>`: Delete records matching a pattern
- `--older-than <days>`: Delete records older than specified days

## Examples

### Execute Raw Query
```bash
# List all tables
python scripts/db_query.py \
  --container postgres \
  --query "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"

# Get sample data
python scripts/db_query.py \
  --container postgres \
  --query "SELECT * FROM users LIMIT 10;"
```

### Inspect Database
```bash
# List all tables
python scripts/db_inspect.py --container postgres --type postgres --list-tables

# Show sample from a table
python scripts/db_inspect.py \
  --container postgres \
  --type postgres \
  --sample users
```

### Cleanup Data
```bash
# Dry run to see what would be deleted
python scripts/db_cleanup.py \
  --container postgres \
  --type postgres \
  --pattern "test_.*" \
  --dry-run

# Actually delete
python scripts/db_cleanup.py \
  --container postgres \
  --type postgres \
  --pattern "test_.*"
```

### Redis Operations
```bash
# List all keys
python scripts/db_query.py \
  --container redis \
  --type redis \
  --query "KEYS *"

# Get value by key
python scripts/db_query.py \
  --container redis \
  --type redis \
  --query "GET user:123"

# Delete keys matching pattern
python scripts/db_query.py \
  --container redis \
  --type redis \
  --query "DEL user:*"
```

## Troubleshooting

### Connection Issues
- Verify container is running: `docker ps | grep <container>`
- Check environment variables are set correctly
- Ensure database port is exposed

### Query Errors
- Verify syntax for your database type
- Check table/collection names exist
- Ensure proper permissions for the database user

### Permission Denied
- Verify database user has necessary permissions
- Check container network access
- Review database authentication configuration

## Resources

### references/database-schemas.md
Database schema documentation and common table structures.

### references/faq.md
Frequently asked questions and troubleshooting tips.

### references/best-practices.md
Best practices for database maintenance and data integrity.

### references/command-reference.md
Database-specific command reference for each supported database type.
