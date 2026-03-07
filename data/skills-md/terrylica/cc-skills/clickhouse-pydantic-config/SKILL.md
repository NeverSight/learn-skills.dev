---
name: clickhouse-pydantic-config
description: Generate DBeaver config from Pydantic ClickHouse models. TRIGGERS - DBeaver config, ClickHouse connection, database client config.
allowed-tools: Read, Bash, Grep
---

# ClickHouse Pydantic Config

<!-- ADR: 2025-12-09-clickhouse-pydantic-config-skill -->

Generate DBeaver database client configurations from Pydantic v2 models using mise `[env]` as Single Source of Truth (SSoT).

## When to Use This Skill

Use this skill when:

- Setting up DBeaver connections for ClickHouse databases
- Generating database client configurations from environment variables
- Managing local vs cloud ClickHouse connection profiles
- Integrating ClickHouse with mise-based development workflows
- Automating DBeaver data-sources.json generation

## Critical Design Principle: Semi-Prescriptive Adaptation

**This skill is NOT a rigid template.** It provides a SSoT pattern that MUST be adapted to each repository's structure and local database situation.

### Why This Matters

Each repository has unique:

- Directory layouts (`.dbeaver/` location may vary)
- Environment variable naming conventions
- Existing connection management patterns
- Local vs cloud database mix

**The SSoT principle is the constant; the implementation details are the variables.**

## Quick Start

```bash
# Generate local connection config
mise run db-client-generate

# Generate cloud connection config
mise run db-client:cloud

# Preview without writing
mise run db-client:dry-run

# Launch DBeaver
mise run dbeaver
```

## Credential Prerequisites (Cloud Mode)

<!-- ADR: 2025-12-10-clickhouse-skill-documentation-gaps -->

Before using cloud mode, obtain credentials via the skill chain:

1. **Create/retrieve user**: Use `clickhouse-cloud-management` skill to create read-only users or retrieve existing credentials from 1Password
2. **Store in .env**: Add to `.env` file (gitignored):

```bash
CLICKHOUSE_USER_READONLY=your_user
CLICKHOUSE_PASSWORD_READONLY=your_password
```

1. **Generate config**: Run `mise run db-client:cloud`

**Skill chain**: `clickhouse-cloud-management` → `.env` → `clickhouse-pydantic-config`

## mise `[env]` as Single Source of Truth

All configurable values live in `.mise.toml`:

```toml
[env]
CLICKHOUSE_NAME = "clickhouse-local"
CLICKHOUSE_MODE = "local"  # "local" or "cloud"
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = "8123"
CLICKHOUSE_DATABASE = "default"
```

Scripts read from `os.environ.get()` with backward-compatible defaults—works with or without mise installed.

## Credential Handling by Mode

| Mode      | Approach                                | Rationale                                       |
| --------- | --------------------------------------- | ----------------------------------------------- |
| **Local** | Hardcode `default` user, empty password | Zero friction, no security concern              |
| **Cloud** | Pre-populate from `.env`                | Read from environment, write to gitignored JSON |

**Key principle**: The generated `data-sources.json` is gitignored anyway. Pre-populating credentials trades zero security risk for maximum developer convenience.

### Cloud Credentials Setup

```bash
# .env (gitignored)
CLICKHOUSE_USER_READONLY=readonly_user
CLICKHOUSE_PASSWORD_READONLY=your-secret-password
```

## Repository Adaptation Workflow

### Pre-Implementation Discovery (Phase 0)

Before writing any code, the executor MUST:

```bash
# 1. Discover existing configuration patterns
fd -t f ".mise.toml" .
fd -t f ".env*" .
fd -t d ".dbeaver" .

# 2. Test ClickHouse connectivity (local)
clickhouse-client --host localhost --port 9000 --query "SELECT 1"

# 3. Check for existing connection configs
fd -t f "data-sources.json" .
fd -t f "dataSources.xml" .
```

### Adaptation Decision Matrix

| Discovery Finding                  | Adaptation Action                                      |
| ---------------------------------- | ------------------------------------------------------ |
| Existing `.mise.toml` at repo root | Extend existing `[env]` section, don't create new file |
| Existing `.dbeaver/` directory     | Merge connections, preserve existing entries           |
| Non-standard CLICKHOUSE\_\* vars   | Map to repository's naming convention                  |
| Multiple databases (local + cloud) | Generate multiple connection entries                   |
| No ClickHouse available            | Warn and generate placeholder config                   |

### Validation Checklist (Post-Generation)

The executor MUST verify:

- [ ] Generated JSON is valid (`jq . .dbeaver/data-sources.json`)
- [ ] DBeaver can import the config (launch and verify connection appears)
- [ ] mise tasks execute without error (`mise run db-client-generate`)
- [ ] `.dbeaver/` added to `.gitignore`

## Pydantic Model

The `ClickHouseConnection` model provides:

- **Type-safe configuration** with Pydantic v2 validation
- **Computed fields** for JDBC URL and connection ID
- **Mode-aware defaults** (cloud auto-enables SSL on port 8443)
- **Environment loading** via `from_env()` class method

See [references/pydantic-model.md](./references/pydantic-model.md) for complete model documentation.

## DBeaver Format

DBeaver uses `.dbeaver/data-sources.json` with this structure:

```json
{
  "folders": {},
  "connections": {
    "clickhouse-jdbc-{random-hex}": {
      "provider": "clickhouse",
      "driver": "com_clickhouse",
      "name": "Connection Name",
      "configuration": { ... }
    }
  }
}
```

**Important**: DBeaver does NOT support `${VAR}` substitution—values must be pre-populated at generation time.

See [references/dbeaver-format.md](./references/dbeaver-format.md) for complete format specification.

## macOS Notes

1. **DBeaver binary**: Use `/Applications/DBeaver.app/Contents/MacOS/dbeaver` (NOT `open -a`)
2. **Gitignore**: Add `.dbeaver/` to `.gitignore`

## Related Skills

| Skill                                      | Integration                         |
| ------------------------------------------ | ----------------------------------- |
| `devops-tools:clickhouse-cloud-management` | Credential retrieval for cloud mode |
| `quality-tools:clickhouse-architect`       | Schema design context               |
| `itp:mise-configuration`                   | SSoT environment variable patterns  |

## Python Driver Policy

For Python application code connecting to ClickHouse (not DBeaver), use `clickhouse-connect` (official HTTP driver). See [`clickhouse-architect`](../../../quality-tools/skills/clickhouse-architect/SKILL.md#python-driver-policy) for:

- Recommended code patterns
- Why NOT to use `clickhouse-driver` (community)
- Performance vs maintenance trade-offs

## Additional Resources

| Reference                                                      | Content                      |
| -------------------------------------------------------------- | ---------------------------- |
| [references/pydantic-model.md](./references/pydantic-model.md) | Complete model documentation |
| [references/dbeaver-format.md](./references/dbeaver-format.md) | DBeaver JSON format spec     |

---

## Troubleshooting

| Issue                   | Cause                        | Solution                                          |
| ----------------------- | ---------------------------- | ------------------------------------------------- |
| DBeaver can't connect   | Port mismatch (8123 vs 9000) | HTTP uses 8123, native uses 9000 - check config   |
| Credentials not loading | .env not sourced             | Run `mise trust` or source .env manually          |
| JSON validation fails   | Invalid data-sources.json    | Validate with `jq . .dbeaver/data-sources.json`   |
| Cloud SSL error         | Missing SSL on port 8443     | Cloud mode auto-enables SSL - verify port is 8443 |
| mise task not found     | Missing task definition      | Add task to mise.toml `[tasks]` section           |
| .dbeaver/ in git        | Missing gitignore entry      | Add `.dbeaver/` to `.gitignore`                   |
| Connection ID conflict  | Duplicate connection names   | Each connection needs unique ID (random hex)      |
| Config not updating     | DBeaver caching              | Restart DBeaver to reload data-sources.json       |
