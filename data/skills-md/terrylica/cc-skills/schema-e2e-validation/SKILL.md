---
name: schema-e2e-validation
description: Earthly E2E validation for YAML schema contracts. TRIGGERS - schema validation, YAML schema, schema contracts, regenerate types.
allowed-tools: Read, Bash, Grep
---

# Schema E2E Validation

## When to Use This Skill

Use this skill when:

- Validating schema changes before commit
- Verifying YAML schema matches live ClickHouse Cloud
- Regenerating Python types, DDL, or docs
- Running full schema workflow validation

## Prerequisites

### Docker Runtime (Required)

Earthly requires Docker. Start Colima before running:

```bash
colima start
```

**Check if running:**

```bash
docker ps  # Should not error
```

### Doppler Access (For validation targets)

Required for `+test-schema-validate` and `+test-schema-e2e`:

```bash
doppler configure set token <token_from_1password>
doppler setup --project gapless-network-data --config prd
```

### Earthly Installation

```bash
brew install earthly
```

---

## Quick Commands

### Generation only (no secrets)

```bash
cd ~/eon/gapless-network-data
colima start  # If not already running
earthly +test-schema-generate
```

### Full E2E with validation (requires Doppler)

```bash
cd ~/eon/gapless-network-data
colima start  # If not already running
./scripts/earthly-with-doppler.sh +test-schema-e2e
```

### All non-secret targets

```bash
cd ~/eon/gapless-network-data
earthly +all
```

---

## Artifacts

After running `+test-schema-generate` or `+test-schema-e2e`, check `./earthly-artifacts/`:

| Path                       | Contents                    |
| -------------------------- | --------------------------- |
| `types/blocks.py`          | Pydantic + TypedDict models |
| `types/__init__.py`        | Package init                |
| `ddl/ethereum_mainnet.sql` | ClickHouse DDL              |
| `docs/ethereum_mainnet.md` | Markdown documentation      |

For E2E, artifacts are under `e2e/types/`, `e2e/ddl/`, `e2e/docs/`.

---

## Earthfile Targets Reference

| Target                  | Secrets | Purpose                    |
| ----------------------- | ------- | -------------------------- |
| `+deps`                 | No      | Install uv + dependencies  |
| `+build`                | No      | Copy source files          |
| `+test-unit`            | No      | Run pytest                 |
| `+test-schema-generate` | No      | Generate types/DDL/docs    |
| `+test-schema-validate` | Yes     | Validate vs ClickHouse     |
| `+test-schema-e2e`      | Yes     | Full workflow + artifacts  |
| `+all`                  | No      | Run all non-secret targets |

---

## Troubleshooting

### "could not determine buildkit address - is Docker or Podman running?"

**Cause**: Docker/Colima not running

**Fix**:

```bash
colima start
# Wait for "done" message, then retry
earthly +test-schema-generate
```

### "unable to parse --secret-file argument"

**Cause**: Wrong flag name or malformed secrets file

**Fix**: The correct flag is `--secret-file-path` (NOT `--secret-file`). The wrapper script handles this, but if running manually:

```bash
# WRONG
earthly --secret-file=/path/to/secrets +target

# CORRECT
earthly --secret-file-path=/path/to/secrets +target
```

Also ensure secrets file has no quotes around values:

```bash
# WRONG format
CLICKHOUSE_HOST="host.cloud"

# CORRECT format
CLICKHOUSE_HOST=host.cloud
```

### "OSError: Readme file does not exist: README.md"

**Cause**: hatchling build backend requires README.md in container

**Fix**: Ensure Earthfile copies README.md in deps target:

```earthfile
deps:
    COPY pyproject.toml uv.lock README.md ./  # README.md required!
```

### "missing secret" during validation

**Cause**: Doppler not configured or secrets not passed

**Fix**:

```bash
# Verify Doppler has the secrets
doppler secrets --project gapless-network-data --config prd | grep CLICKHOUSE

# Use the wrapper script (handles secret injection)
./scripts/earthly-with-doppler.sh +test-schema-validate
```

### Cache Issues

Force rebuild without cache:

```bash
earthly --no-cache +test-schema-e2e
```

---

## Implementation Details

### Doppler Secret Injection

The wrapper script `scripts/earthly-with-doppler.sh`:

1. Downloads secrets from Doppler
2. Filters for `CLICKHOUSE_*` variables
3. Strips quotes (Doppler outputs `KEY="value"`, Earthly needs `KEY=value`)
4. Passes via `--secret-file-path` flag
5. Cleans up temp file on exit

### Secrets Required

| Secret                         | Purpose               |
| ------------------------------ | --------------------- |
| `CLICKHOUSE_HOST_READONLY`     | ClickHouse Cloud host |
| `CLICKHOUSE_USER_READONLY`     | Read-only user        |
| `CLICKHOUSE_PASSWORD_READONLY` | Read-only password    |

---

## Related Files

| File                                                                   | Purpose                  |
| ---------------------------------------------------------------------- | ------------------------ |
| `~/eon/gapless-network-data/Earthfile`                                 | Main build file          |
| `~/eon/gapless-network-data/scripts/earthly-with-doppler.sh`           | Secret injection wrapper |
| `~/eon/gapless-network-data/schema/clickhouse/ethereum_mainnet.yaml`   | SSoT schema              |
| `~/eon/gapless-network-data/docs/adr/2025-12-03-earthly-schema-e2e.md` | ADR                      |

---

## Validation History

- **2025-12-03**: Created and validated with full E2E run against ClickHouse Cloud
- **Lessons Learned**:
  - `--secret-file-path` not `--secret-file` (Earthly v0.8.16)
  - Doppler `--format env` outputs quotes, must strip with `sed 's/"//g'`
  - README.md must be copied for hatchling build backend
  - Colima must be started before Earthly runs

---

## Design Authority

<!-- ADR: 2025-12-10-clickhouse-skill-delegation -->

This skill validates schemas but does not design them. For schema design guidance (ORDER BY, compression, partitioning), invoke **`quality-tools:clickhouse-architect`** first.

## Related Skills

| Skill                                      | Purpose                         |
| ------------------------------------------ | ------------------------------- |
| `quality-tools:clickhouse-architect`       | Schema design before validation |
| `devops-tools:clickhouse-cloud-management` | Cloud credentials for E2E tests |
| `devops-tools:clickhouse-pydantic-config`  | Client configuration            |
