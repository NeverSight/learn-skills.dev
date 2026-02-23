---
name: altinity-expert-clickhouse-grants
description: Diagnose and resolve ClickHouse grant and authentication errors, especially after upgrades. Use when queries fail with ACCESS_DENIED/NOT_ENOUGH_PRIVILEGES, AUTHENTICATION_FAILED/WRONG_PASSWORD/REQUIRED_PASSWORD, or ON CLUSTER privilege errors; when system.* or INFORMATION_SCHEMA access is denied; or when grant behavior changes after version upgrades.
---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

## Propose Minimal Grants
Provide the smallest set of `GRANT` statements that match observed `needed_grant` values. Prefer role-based grants when the user already uses roles.

Example pattern:
```sql
-- Direct grants
GRANT SELECT ON system.processes TO user_x;
GRANT SELECT ON INFORMATION_SCHEMA.COLUMNS TO svc_y;
GRANT CLUSTER ON *.* TO svc_z;

-- Role-based grants (preferred)
GRANT SELECT ON system.processes TO role_analytics;
GRANT role_analytics TO user_x;
```

## Post-Upgrade Compatibility Checks
Verify `access_control_improvements` settings, which can change privilege requirements:

- `select_from_system_db_requires_grant`
- `select_from_information_schema_requires_grant`
- `on_cluster_queries_require_cluster_grant`

If these are enabled post-upgrade, users may require new explicit grants for `system.*`, `INFORMATION_SCHEMA.*`, or `CLUSTER`.
