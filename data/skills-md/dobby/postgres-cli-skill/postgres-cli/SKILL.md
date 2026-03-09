---
name: postgres-cli
version: 2.3.1
description: Execute PostgreSQL queries and introspection with named project connections using `postgres-cli` V2. Use when the user asks to inspect data, run SQL, debug schema, validate config, or build schema cache artifacts.
---

# Postgres CLI (V2)

Use `postgres-cli` to query PostgreSQL through named connection targets.

## Platform Support

- `scripts/postgres-cli` is a launcher script.
- Prebuilt binaries are expected in `scripts/bin/` for:
  - macOS arm64 (`postgres-cli-darwin-arm64`)
  - Linux x86_64 (`postgres-cli-linux-x86_64`)
  - Windows x86_64 (`postgres-cli-windows-x86_64.exe`)
- If no compatible binary exists and source + Cargo are available, launcher falls back to `cargo run --release`.

## Available Scripts

- `scripts/postgres-cli` - Launcher that selects a platform binary.
- `scripts/build-release-binary.sh` - Builds and places a binary for current host into `scripts/bin/`.
- `scripts/refresh-binaries-from-release.sh <tag>` - Downloads release binaries into `scripts/bin/`.

## When To Use

- The user asks to inspect Postgres data.
- The user asks to run SQL against a configured target.
- The user asks for schema introspection.
- The user asks to validate DB CLI config or debug connectivity.
- The user asks to refresh schema cache for agent context.

## Setup

Read [Setup Guide](references/SETUP.md).

## V2 Command Contract

Global flags (before subcommand):

- `--project-root <path>` (optional; default cwd)
- `--target <name>` (optional if `default_target` set)
- `--format <json|text|csv|tsv>` (default `json`)
- `--output <path>` (optional output file)
- `--no-summary` (suppresses text summary)

Subcommands:

- `query`
  - input: exactly one of `--sql`, `--sql-file`, `--stdin`
  - flags: `--mode <read|write>` (default `read`), `--timeout-ms`
- `explain`
  - input: exactly one of `--sql`, `--sql-file`, `--stdin`
  - flags: `--analyze`, `--verbose`, `--buffers`, `--settings`, `--wal`, `--timeout-ms`
- `introspect`
  - required: `--kind <schemas|tables|columns|indexes|constraints|views|materialized-views|functions|triggers|enums|rowcounts|rowcounts-exact>`
  - optional filters: `--schema` (repeatable), `--table schema.table` (repeatable)
- `schema-cache update`
  - flags: `--all-tables`, `--with-markdown`, `--table-file-naming <table|schema-table>`, `--timeout-ms`
- `targets list`
- `config validate`
- `doctor`

## Safety Rules

- Prefer read targets for normal data inspection.
- `query --mode read` blocks mutating SQL.
- Mutating SQL requires `query --mode write` and `allow_write=true` on target.
- `explain --analyze` on mutating SQL requires write-enabled target.

## Operational Guardrails

- MUST use `scripts/postgres-cli` for all database interactions.
- MUST NOT execute `psql` directly, even if `psql` is installed.
- MUST NOT read secret/config files directly:
  - `.agents/postgres-cli/postgres.toml`
  - `.agent/postgres-cli/postgres.toml`
  - `.agents/postgres-cli/.env`
  - `.agent/postgres-cli/.env`
  - `.env` at repository root
- MUST treat target selection as:
  - If the user provides a connection name, pass `--target <name>`.
  - If the user does not provide a connection, omit `--target` and rely on CLI fallback to `default_target`.
  - If the CLI returns `TARGET_MISSING`, ask the user for a connection name and do not inspect config files.
- MUST NOT bypass CLI write-safety controls by using direct DB tools.

## Command Patterns

Run read query:

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-read query --sql "SELECT now();"
```

Run write query intentionally:

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-write query --mode write --sql "UPDATE users SET active = true WHERE id = 1;"
```

Introspect tables:

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-read introspect --kind tables
```

Explain a query:

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-read explain --sql "SELECT * FROM users WHERE id = 1;"
```

Validate config:

```bash
scripts/postgres-cli --project-root /path/to/repo config validate
```

Doctor connectivity:

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-read doctor
```

Update schema cache (JSON only):

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-read schema-cache update
```

Update schema cache with markdown:

```bash
scripts/postgres-cli --project-root /path/to/repo --target app-read schema-cache update --with-markdown
```

## Progressive Schema Loading

When schema context is needed, use this order:

1. Read `.agents/postgres-cli/schema/index.json`.
2. Load only required files from `.agents/postgres-cli/schema/tables/*.json`.
3. Read `.agents/postgres-cli/schema/relations.json` when join/relationship reasoning is needed.
4. If markdown was generated, consult `.md` files only for human-friendly display.
5. If cache is missing or stale, run `schema-cache update`.

## Agent Guidelines

- Pass `--target` whenever the user provides a connection name.
- If the user did not provide a connection name, allow `default_target` fallback.
- Default to `--format json` for machine parsing.
- Prefer `query --mode read` unless the user explicitly requests data mutation.
- Return relevant result rows and summarize key findings.
