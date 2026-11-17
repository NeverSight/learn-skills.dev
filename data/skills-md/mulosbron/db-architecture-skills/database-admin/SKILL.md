---
name: database-admin
description: "Database operations: backups and restore testing, roles and privileges, destructive commands, maintenance. Read when the task touches a running database rather than its schema design."
---

# Database Admin

## Boundaries

- Before suggesting `DROP`, `TRUNCATE`, `DELETE` without a tight `WHERE`, role removal, or `migrate reset`, state which environment the command targets and require an explicit confirmation. Assume any connection string you cannot prove is local is production.
- Never put credentials in prose or examples; read them from the environment.
- Prefer reversible operations: rename before drop, disable before delete, `NOT VALID` constraints before `VALIDATE`.

## Audit checklist for an existing instance

- Automated backups exist **and a restore has been tested** recently. An untested backup does not count.
- Point-in-time recovery enabled if the data cannot be recreated.
- Application connects as a role with only the privileges it needs; no app using the superuser or owner role.
- Separate roles for migrations (DDL) and runtime (DML).
- Postgres: autovacuum running, no tables with high dead-tuple ratios, `pg_stat_statements` enabled, connection limits matched to pooler settings. See `skills/postgres-best-practices/SKILL.md`.
- Encryption in transit enforced (`sslmode=require` or stronger).
- Slow query and error logging on; log destination known.
