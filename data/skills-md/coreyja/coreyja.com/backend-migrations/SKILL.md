---
name: Backend Migrations
description: Create and manage database migrations with proper rollback methods, focused changes, and zero-downtime deployment considerations. Use this skill when creating new database migration files, modifying table schemas, adding or removing columns, creating or dropping indexes, or managing database version control. When working with migration directories, schema definition files, or database change scripts. When implementing backwards-compatible database changes for production deployments. When separating schema changes from data migrations.
---

# Backend Migrations

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend migrations.

## When to use this skill

- When creating new database migration files
- When modifying existing table schemas (adding/removing columns, changing types)
- When adding or removing database indexes
- When creating or modifying foreign key constraints
- When implementing database schema versioning
- When working with migration directories (e.g., `migrations/`, `db/migrate/`)
- When writing rollback/down migration methods
- When planning zero-downtime deployments with backwards-compatible schema changes
- When separating schema changes from data transformation scripts
- When naming migration files with descriptive, clear names

## Instructions

For details, refer to the information provided in this file:
[backend migrations](../../../agent-os/standards/backend/migrations.md)
