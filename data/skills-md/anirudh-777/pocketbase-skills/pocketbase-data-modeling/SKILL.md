---
name: pocketbase-data-modeling
description: Use when you specifically need deeper collection design, relation strategy, indexes, or migration sequencing beyond the orchestrator quick actions
---

# PocketBase Data Modeling (Advanced)

## Overview
Use this only for deeper schema/migration design. Default to `pocketbase-agent-orchestrator` for common management tasks.

## Focus
- Collection boundaries and relation modeling
- Index strategy for filters/sorts
- Safe schema evolution and staged migrations

## Minimal Workflow
1. Capture expected read/write/query patterns.
2. Design schema + relations + indexes.
3. Plan additive migration, backfill, and cleanup phases.
4. Validate against auth rules and API usage.

## References
- [schema-patterns.md](references/schema-patterns.md)
- [migration-playbook.md](references/migration-playbook.md)
- [index-guidelines.md](references/index-guidelines.md)
