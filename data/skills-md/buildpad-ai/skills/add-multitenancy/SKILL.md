---
name: add-multitenancy
description: Multi-tenancy for DaaS applications — delegates to /manage-scope, the standard approach.
argument-hint: "[levels: e.g. tenant / region/branch] [use-case]"
---

# Add Multitenancy

> **This skill delegates to `/manage-scope`.**
>
> DaaS implements multi-tenancy through its native scope system — no junction tables, no custom FK columns, built-in hierarchical permission enforcement. Load the `/manage-scope` skill to proceed.
>
> On an Engine project the project is one tenant. Every scope hierarchy begins below the project's tenant node: create no scope type without a parent and no scope item without a parent. Scope types, items and collection settings are managed through `/api/scope/types`, `/api/scope/items` and `/api/scope/collection-config` with an administrator's session; the MCP `scope` tool, served to an administrator only, assigns a role to a user at a scope (`assign_user_role`) and registers a collection as tenanted (`create_config`, the body of `POST /api/scope/collection-config`).
>
> On an Engine project a scoped collection's scope column is a many-to-one field to `daas_scope_items` (`meta.options.related_collection: daas_scope_items`, `meta.options.related_field: uri_path`), which gives it a foreign key to `daas_scope_items(uri_path)`.

See `/manage-scope` for the complete setup guide.