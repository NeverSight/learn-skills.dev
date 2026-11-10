---
name: digitalocean-databases
description: >-
  Provision and operate Managed Databases: users, firewall rules, configs,
  backups, resize. Never echo credentials. Use for "Postgres cluster", "managed
  database", "DB user", or "trusted sources".
---
# Managed Databases (MCP)

Connector: **digitalocean-databases** — connect on first use.

1. Load **digitalocean-safety**.
1. Read: `db-cluster-list`, `db-cluster-get`, `db-cluster-list-options`.
1. **Never** paste passwords, connection strings, or CA certificates into chat.
   Summarize that credentials exist and point to the control panel if needed.

## Writes

- **Create / resize:** show price and plan before apply (Tier 4 style).
- **Delete cluster or user:** Tier 3 named confirmation.
- **Firewall / trusted sources:** confirm sources; avoid locking out the app's egress.

## Tools

Use `db-cluster-*` tools from the databases MCP server. Exact tool names follow
upstream mcp-digitalocean registry.
