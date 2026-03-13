---
name: pctl
description: "pctl CLI (v0.6.3) — PAIC Control, a unified testing CLI for PingOne Advanced Identity Cloud (AIC). Handles connection profiles, JWT token generation/decoding/validation, authentication journey testing, local ELK stack management (Elasticsearch + Kibana log streaming), historical log search, and configuration change tracking. Contains environment shorthands, ELK workflow recipes, and gotchas."
---

# pctl CLI Skill

For full flag details, run `pctl <command> <action> --help`.

- CLI repo: https://github.com/autumnfallenwang/pctl

## Environments

Use these connection profile names with any pctl command:

| Profile Name | Tenant | Purpose |
|-------------|--------|---------|
| `sandbox` | yourtenantsandbox | Sandbox |
| `dev` | yourtenantdev | Development |
| `staging` | yourtenantstaging | Staging |
| `prod` | yourtenantprod | Production |

```bash
pctl conn list                  # See all saved profiles
pctl conn show sandbox              # Show details of a specific profile
pctl conn validate sandbox          # Validate credentials
```

## Connection Profile Management

**Syntax**: `pctl conn <add|list|show|validate|delete> [options] [conn_name]`

```bash
# Add with flags
pctl conn add myenv --platform https://openam-env.id.forgerock.io \
  --sa-id "account-id" --sa-jwk-file /path/to/jwk.json

# Add from YAML config file
pctl conn add myenv -c /path/to/conn.yaml

# Add without credential validation
pctl conn add myenv --platform https://... --sa-id "..." --sa-jwk-file ... --no-validate

# Show, validate, delete
pctl conn show sandbox
pctl conn validate sandbox
pctl conn delete sandbox              # Prompts for confirmation
pctl conn delete sandbox --force      # Skip confirmation
```

Connection YAML format:
```yaml
platform: "https://openam-env.id.forgerock.io"
sa_id: "service-account-id"
sa_jwk_file: "/path/to/jwk.json"      # File path OR inline JSON via sa_jwk
log_api_key: "optional-key"
log_api_secret: "optional-secret"
admin_username: "optional-admin"
admin_password: "optional-password"
description: "Environment description"
```

Note: JWK credentials can be provided either as `--sa-jwk-file /path/to/file.json` (file path) or `--sa-jwk '{"kty":"RSA",...}'` (inline JSON string). Use one or the other, not both.

## Token Management

**Syntax**: `pctl token <get|decode|validate> [options] <conn_name|token_string>`

```bash
# Generate access token from connection profile
pctl token get sandbox                       # Raw token string
pctl token get sandbox --format bearer       # With "Bearer " prefix
pctl token get sandbox --format json         # Full JSON response

# Inspect a JWT (no verification, just decode)
pctl token decode "eyJhbGciOiJS..."

# Validate JWT structure and format
pctl token validate "eyJhbGciOiJS..."
```

Note: `token get` requires a valid connection profile with sa_id and sa_jwk/sa_jwk_file. `token decode` and `token validate` take a raw JWT string, NOT a connection profile name.

## Journey Testing

**Syntax**: `pctl journey <run|validate> [options] <file>`

```bash
# Validate config before running
pctl journey validate path/to/config.yaml

# Run journey
pctl journey run path/to/config.yaml

# Interactive step-by-step mode (pauses between steps)
pctl journey run path/to/config.yaml --step

# With custom timeout
pctl journey run path/to/config.yaml --timeout 30000
```

Journey YAML config format:
```yaml
platformUrl: https://openam-env.id.forgerock.io
realm: alpha
journeyName: Login

steps:
  step1:
    Username: testuser

  step2:
    Password: testpassword
```

Note: The `--step` / `-s` flag enables interactive step-by-step mode, pausing between each step so you can inspect intermediate state. Useful for debugging failing journeys.

## ELK Stack Management

**Syntax**: `pctl elk <init|health|start|stop|status|clean|purge|hardstop|down> [options]`

### Lifecycle (in order)

```bash
# 1. Initialize — deploy containers, templates, policies (one-time setup)
pctl elk init

# 2. Check health — verify Elasticsearch + Kibana are running
pctl elk health

# 3. Start streaming logs from a connection profile
pctl elk start sandbox                              # Streamer named "sandbox"
pctl elk start sandbox --name my-streamer           # Custom streamer name
pctl elk start sandbox --log-level 3                # DEBUG level
pctl elk start sandbox -c am-core,idm-core          # Specific components

# 4. Check streamer status
pctl elk status                                 # All streamers
pctl elk status --name sandbox                      # Specific streamer

# 5. Stop streamers
pctl elk stop                                   # Stop all
pctl elk stop --name sandbox                        # Stop specific
```

### Data Management

```bash
# Clean index data but keep streamer running (name required)
pctl elk clean --name sandbox
pctl elk clean --name sandbox --force               # Skip confirmation

# Purge streamer completely — stop + delete indices (name required)
pctl elk purge --name sandbox
pctl elk purge --name sandbox --force               # Skip confirmation
```

### Teardown

```bash
# Stop all streamers + containers, PRESERVE data
pctl elk hardstop
pctl elk hardstop --force                       # Skip confirmation

# Stop all + REMOVE containers + DELETE all data
pctl elk down
pctl elk down --force                           # Skip confirmation
```

ELK log levels: `1` = ERROR, `2` = INFO, `3` = DEBUG, `4` = ALL (default: depends on command).

Note: `elk clean` and `elk purge` require `--name` / `-n` — they do NOT operate on "all" streamers. `elk stop`, `elk hardstop`, and `elk down` operate on all if no name given.

### Querying Local Elasticsearch

After `pctl elk start` streams logs into local ES, you can query them directly. This is different from `pctl log search` which queries the remote AIC API.

**Connection**: `http://localhost:9200`, no authentication.

**Index pattern**: `paic-logs-{profile_name}-{YYYY.MM}` (e.g., `paic-logs-sandbox-2026.03`). Indices rotate monthly. Use `paic-logs-*` to search across all profiles/months, or `paic-logs-sandbox*` for a specific profile.

**Document schema**:

| Field | ES Type | Description |
|-------|---------|-------------|
| `timestamp` | `date` | ISO 8601 timestamp |
| `source` | `keyword` | Log source (e.g., `idm-core`, `am-access`) |
| `type` | `keyword` | `application/json` or `text/plain` |
| `payload` | `object` | Log content (flexible structure) |

**Payload structure** depends on the `type` field:

- `text/plain`: `payload` only has `message` — a raw log string with level/logger info embedded in the text.
- `application/json` (structured logs): `payload` has structured fields:

| Payload Field | Description |
|---------------|-------------|
| `payload.message` | Log message (present in both types) |
| `payload.level` | Log level string (`SEVERE`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `FINE`, `FINER`, `FINEST`) |
| `payload.logger` | Java class name (e.g., `org.forgerock.am.health.LivenessCheckEndpoint`) |
| `payload.transactionId` | Transaction ID for request tracing |
| `payload.mdc.transactionId` | Same transaction ID (nested in MDC context) |
| `payload.thread` | Java thread name |
| `payload.context` | AM context (e.g., `default`) |
| `payload.timestamp` | Log-level timestamp (may differ slightly from top-level `timestamp`) |

**Retention**: Data auto-deletes after 7 days (ILM policy). Don't search beyond that window.

```bash
# Check available indices
curl -s 'localhost:9200/_cat/indices/paic-logs-*?v&s=index'

# Search by source
curl -s 'localhost:9200/paic-logs-sandbox*/_search?pretty' -H 'Content-Type: application/json' -d '
{"query":{"match":{"source":"idm-core"}},"size":10,"sort":[{"timestamp":"desc"}]}'

# Search by keyword in message
curl -s 'localhost:9200/paic-logs-sandbox*/_search?pretty' -H 'Content-Type: application/json' -d '
{"query":{"match":{"payload.message":"authentication failed"}},"size":10,"sort":[{"timestamp":"desc"}]}'

# Filter by transaction ID
curl -s 'localhost:9200/paic-logs-sandbox*/_search?pretty' -H 'Content-Type: application/json' -d '
{"query":{"match":{"payload.transactionId":"abc-123-def"}}}'

# Errors — structured logs (application/json) use payload.level
curl -s 'localhost:9200/paic-logs-sandbox*/_search?pretty' -H 'Content-Type: application/json' -d '
{"query":{"bool":{"must":[{"match":{"payload.level":"SEVERE"}},{"range":{"timestamp":{"gte":"now-1h"}}}]}}}'

# Errors — text/plain logs have level in the message string
curl -s 'localhost:9200/paic-logs-sandbox*/_search?pretty' -H 'Content-Type: application/json' -d '
{"query":{"bool":{"must":[{"match":{"payload.message":"SEVERE"}},{"match":{"type":"text/plain"}}]}}}'

# Count docs per source
curl -s 'localhost:9200/paic-logs-sandbox*/_search?pretty' -H 'Content-Type: application/json' -d '
{"size":0,"aggs":{"by_source":{"terms":{"field":"source"}}}}'
```

**When to use local ES vs `pctl log search`**:
- `pctl log search` — searches historical logs from the AIC API. Looking into the past.
- Local ES queries — queries live-streamed data captured by `pctl elk start`. Requires ELK running. Better for real-time monitoring, complex queries, and aggregations.

## Historical Log Search

**Syntax**: `pctl log search [options] <conn_name>`

```bash
# Last 24h from idm-config (all defaults)
pctl log search sandbox

# Last 7 days, specific component, with filter
pctl log search sandbox -c idm-config --days 7 -q '/payload/objectId co "endpoint/"'

# Specific date range
pctl log search sandbox -c am-access --from 2025-10-01 --to 2025-10-06

# Filter by transaction ID
pctl log search sandbox --txid "abc-123-def"

# Errors only
pctl log search sandbox -l 1

# Save to file
pctl log search sandbox -c idm-config --days 7 -o logs.jsonl
pctl log search sandbox -c idm-config --format json -o report.json
```

Log levels: `1` = ERROR, `2` = INFO (default), `3` = DEBUG, `4` = ALL.

Default component is `idm-config`. Default time range is last 24 hours (`--days 1`).

Note: `--days` overrides `--from`/`--to` if both are provided. Use `--no-default-noise-filter` to disable built-in noise filtering.

## Configuration Change Tracking

**Syntax**: `pctl log changes [options] <conn_name>`

### IDM-Config Types

```bash
# Endpoint changes
pctl log changes sandbox --type endpoint --name my_endpoint

# Connector changes (last 30 days)
pctl log changes sandbox --type connector --name MyConnector --days 30

# Email template changes
pctl log changes sandbox --type emailtemplate --name welcome-email

# Mapping changes
pctl log changes sandbox --type mapping --name managedAlpha_user

# Access control changes (no --name needed, global config)
pctl log changes sandbox --type access --days 30

# Repo changes (no --name needed)
pctl log changes sandbox --type repo --days 7
```

### AM-Config Types

```bash
# Script changes (name auto-resolved to UUID)
pctl log changes sandbox --type script --name "My Test Script"

# Journey changes
pctl log changes sandbox --type journey --name MyLoginJourney --days 30

# SAML entity changes
pctl log changes sandbox --type saml --name "https://example.com/saml/logout/"
```

### Output Formats

```bash
# JSON (default, human-readable)
pctl log changes sandbox --type endpoint --name my_endpoint --format json

# JSONL (one object per line, for piping)
pctl log changes sandbox --type endpoint --name my_endpoint --format jsonl

# JS (JavaScript, for embedding)
pctl log changes sandbox --type endpoint --name my_endpoint --format js

# Save to file
pctl log changes sandbox --type endpoint --name my_endpoint -o report.json
```

Supported types: `endpoint`, `connector`, `emailtemplate`, `mapping`, `access`, `repo` (IDM-Config) and `script`, `journey`, `saml` (AM-Config).

Note: `access` and `repo` types do NOT require `--name` — they track global config changes. All other types require `--name`. For AM-Config `script` type, the human-readable name is auto-resolved to UUID for the API query.

## Gotchas

- `token decode` and `token validate` take a raw JWT string, NOT a connection profile name. Only `token get` uses a profile name.
- `elk clean` and `elk purge` REQUIRE `--name` — they refuse to run without it to prevent accidental data loss.
- `elk down` deletes ALL data (containers + indices). Use `elk hardstop` if you want to preserve data.
- `--days` overrides `--from`/`--to` in both `log search` and `log changes`. If you pass all three, the date range is ignored.
- ELK log levels start at 1 (ERROR), not 0. The scale is 1=ERROR, 2=INFO, 3=DEBUG, 4=ALL.
- `log changes` for `access` and `repo` types do NOT take `--name` — they track global config, not individual resources.
- `log changes` for `script` type auto-resolves human-readable names to UUIDs. You pass the friendly name, not the UUID.
- Connection profiles support JWK as either a file path (`--sa-jwk-file`) or inline JSON (`--sa-jwk`). Never pass both.
- `conn add` validates credentials by default. Use `--no-validate` to skip if the environment isn't reachable yet.
- Journey `--step` mode is interactive — it pauses between steps and waits for user input. Don't use it in scripts.
