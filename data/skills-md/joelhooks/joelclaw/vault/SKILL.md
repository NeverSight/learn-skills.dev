---
name: vault
displayName: Vault CLI Operations
description: "Operate Joel's Obsidian Vault through the joelclaw CLI. Use when reading ADRs/projects, searching notes, listing PARA sections, or auditing ADR hygiene with `vault adr` commands. Triggers on: 'check the vault', 'read ADR', 'find this note', 'vault search', 'ADR collisions', 'ADR audit', 'decision inventory', or any Vault command task."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, vault, adr, cli, para, governance]
---

# Vault CLI Operations

Use `joelclaw vault` as the canonical interface for Vault reads and ADR governance checks.

## When to Use

Trigger this skill when the request involves:

- Reading ADRs by number/reference
- Searching Vault markdown
- Listing projects/decisions/inbox/resources
- ADR hygiene checks (status drift, collisions, index drift)
- Decision inventory/gardening workflows

## Command Tree

```bash
joelclaw vault
├── read <ref>
├── search <query> [--semantic] [--limit <limit>]
├── ls [section]
├── tree
└── adr
    ├── list [--status <status>] [--limit <limit>]
    ├── collisions
    ├── audit
    └── rank [--band <band>] [--unscored] [--all]
```

## Core Workflows

### 1) Read ADRs or notes

```bash
joelclaw vault read "ADR-0168"
joelclaw vault read "project 12"
joelclaw vault read "~/Vault/Projects/12-example/index.md"
```

### 2) Search vault content

```bash
joelclaw vault search "talon watchdog"
joelclaw vault search "content lifecycle" --semantic --limit 5
```

### 3) ADR governance checks

```bash
joelclaw vault adr list --status proposed --limit 50
joelclaw vault adr collisions
joelclaw vault adr audit
joelclaw vault adr rank
joelclaw vault adr rank --band do-now
joelclaw vault adr rank --unscored
```

`vault adr audit` is the canonical pre-flight for ADR grooming. It reports:

- canonical status counts
- missing/non-canonical statuses
- duplicate ADR number collisions
- broken `superseded-by` targets
- ADR README index drift

`vault adr rank` is the daily prioritization pass. It enforces NRC scoring and applies a novelty/cool-factor facet (`priority-novelty`, alias `priority-interest`) with a neutral default of `3` when missing.

## Rules

1. **CLI-first only**: Do not grep random vault files when `joelclaw vault` can answer directly.
2. **Use audit before ADR surgery**: Run `joelclaw vault adr audit` first, then patch.
3. **Canonical statuses only**: `proposed|accepted|shipped|superseded|deprecated|rejected`.
4. **Keep index synced**: After ADR renames/additions, update `~/Vault/docs/decisions/README.md`.
5. **Respect collisions as bugs**: Any duplicate ADR numeric prefix is a governance bug to resolve.

## References

- ADR-0081: Vault CLI & Agent Tool Access
- ADR-0173: ADR Number Collision Remediation
- ADR-0174: Vault Command Tree + ADR Audit CLI
- CLI docs: `~/Code/joelhooks/joelclaw/docs/cli.md`
