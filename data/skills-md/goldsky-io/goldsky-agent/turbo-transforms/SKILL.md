---
name: turbo-transforms
description: "Write SQL, TypeScript, and dynamic table transforms for Goldsky Turbo pipelines. Use this skill for: decoding EVM event logs with _gs_log_decode (requires ABI) or transaction inputs with _gs_tx_decode, filtering and casting blockchain data in SQL, combining multiple decoded event types into one table with UNION ALL, writing TypeScript/WASM transforms using the invoke(data) function signature, setting up dynamic lookup tables to filter transfers by a wallet list you update at runtime (dynamic_table_check), chaining SQL and TypeScript steps together, or debugging null values in decoded fields. For full pipeline YAML structure, use /turbo-pipelines instead. For building an entire pipeline end-to-end, use /turbo-builder instead."
---

# Turbo Transforms

Write, understand, and debug SQL, TypeScript, and dynamic table transforms for Turbo pipeline configurations.

Identify what the user needs (decode, filter, reshape, combine, custom logic, or lookup joins), then use the relevant section below. After writing transforms, always validate the full pipeline YAML before presenting it to the user:

```bash
goldsky turbo validate <pipeline.yaml>
```

If generating a complete pipeline YAML (not just a transform snippet), always validate with `goldsky turbo validate` before presenting it to the user.

**Reference files for specialized topics:**
- `references/typescript-transforms.md` — TypeScript/WASM script transforms and handler transforms
- `references/dynamic-tables.md` — Dynamic table transforms (allowlists, lookup joins)
- `references/solana-patterns.md` — Solana instruction/log decoding and function examples (array, JSON, hex)

---

## Transform Basics

### YAML Structure

```yaml
transforms:
  my_transform:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, address
      FROM my_source
      WHERE address = '0xabc...'
```

### Required Fields

| Field         | Required | Description                                      |
| ------------- | -------- | ------------------------------------------------ |
| `type`        | Yes      | `sql`, `script`, `handler`, or `dynamic_table`   |
| `primary_key` | Yes      | Column used for uniqueness and ordering           |
| `sql`         | Yes      | SQL query (for `sql` type transforms)            |

### Referencing Data

- Reference **sources** by their YAML key name: `FROM my_source`
- Reference **other transforms** by their YAML key name: `FROM my_transform`
- No need for a `from` field in SQL transforms — the `FROM` clause in SQL handles it

### SQL Streaming Limitations

Turbo SQL is powered by Apache DataFusion in streaming mode. The following are **NOT supported**:

- **Joins** — use `dynamic_table` transforms for lookup-style joins instead
- **Aggregations** (GROUP BY, COUNT, SUM, AVG) — use `postgres_aggregate` sink instead
- **Window functions** (OVER, PARTITION BY, ROW_NUMBER)
- **Subqueries** — use transform chaining instead
- **CTEs** (WITH...AS) **are** supported

### The `_gs_op` Column

Every record includes a `_gs_op` column that tracks the operation type: `'i'` (insert), `'u'` (update), `'d'` (delete). Preserve this column through transforms for correct upsert semantics in database sinks.

---

## Goldsky SQL Functions

### `evm_log_decode()` — Decode Raw EVM Logs

Decodes raw Ethereum log data into structured event fields using an ABI specification.

> **Aliases:** `_gs_log_decode` and `evm_decode_log` also work. Existing pipelines using `_gs_log_decode` are valid.

**Syntax:**
```sql
evm_log_decode(abi_json, topics, data) -> STRUCT<name: VARCHAR, event_params: LIST<VARCHAR>>
```

**Parameters:**
- `abi_json` — JSON string containing the ABI event definitions (or full contract ABI)
- `topics` — The `topics` column from `raw_logs`
- `data` — The `data` column from `raw_logs`

**Returns a struct with:**
- `decoded.name` (or `decoded.event_signature` via alias) — Event name (e.g., `'OrderFilled'`, `'Transfer'`)
- `decoded.event_params[N]` — Positional event parameters (1-indexed, returned as strings)

**Example — Decode ERC-20 Transfer events:**
```yaml
transforms:
  decoded_events:
    type: sql
    primary_key: id
    sql: |
      SELECT
        _gs_log_decode(
          '[{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]',
          topics,
          data
        ) AS decoded,
        id,
        block_number,
        transaction_hash,
        address,
        block_timestamp
      FROM my_raw_logs
```

**Then filter by event in a downstream transform:**
```yaml
  transfers:
    type: sql
    primary_key: id
    sql: |
      SELECT
        id,
        block_number,
        block_timestamp,
        transaction_hash,
        address AS token_address,
        decoded.event_params[1] AS from_address,
        decoded.event_params[2] AS to_address,
        (CAST(decoded.event_params[3] AS DOUBLE) / 1e18) AS amount
      FROM decoded_events
      WHERE decoded.event_signature = 'Transfer'
```

**Tips for `_gs_log_decode()`:**
- The ABI JSON must be a **single-line string** or use YAML `>-` / `|` block syntax
- Include **all event ABIs** you want to decode in a single array — events not matching are ignored
- Multiple events with the same name but different signatures (e.g., from different contracts) can coexist
- Use the source's `filter:` field to pre-filter by contract address before decoding (more efficient)
- **Backtick-escape reserved words:** Several column names conflict with SQL reserved words and must be escaped with backticks: `` `data` ``, `` `decoded` ``, `` `balance` ``, `` `owner_address` ``, `` `id` `` (in some contexts). When in doubt, backtick-escape column names that could be keywords.

**Correct escaping example:**
```sql
SELECT
  _gs_log_decode('[...]', topics, `data`) AS `decoded`,
  id, block_number, transaction_hash, address, block_timestamp
FROM my_raw_logs
```

### `fetch_abi()` — Fetch ABI/IDL from URL

Fetch an ABI or IDL from a remote URL. Cached internally for performance.

```sql
fetch_abi(url, format) -> VARCHAR
-- format: 'raw' for plain JSON, 'etherscan' for Etherscan API responses
```

**Aliases:** `_gs_fetch_abi`

**Example:**
```sql
evm_log_decode(
  fetch_abi('https://example.com/erc20.json', 'raw'),
  topics, data
) AS decoded
```

### `_gs_keccak256()` — Keccak256 Hash

Compute Keccak256 hash (same as Solidity's `keccak256`). Returns hex with `0x` prefix.

```sql
_gs_keccak256('Transfer(address,address,uint256)')
-- 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
```

### `xxhash()` — Fast Non-Cryptographic Hash

```sql
xxhash(concat(transaction_hash, '_', log_index::VARCHAR)) AS unique_id
```

### U256/I256 — 256-bit Integer Math

For precise token amount arithmetic without JavaScript precision loss.

```sql
-- Convert to/from U256
to_u256(value)              -> U256
u256_to_string(u256_value)  -> VARCHAR

-- Arithmetic (also available: u256_sub, u256_mul, u256_div, u256_mod)
u256_add(a, b) -> U256

-- Automatic operator rewriting: once values are cast to U256/I256,
-- standard operators (+, -, *, /, %) are auto-rewritten to function calls
to_u256(value) / to_u256('1000000000000000000')  -- same as u256_div(...)
```

**I256 (signed):** `to_i256`, `i256_to_string`, `i256_add`, `i256_sub`, `i256_mul`, `i256_div`, `i256_mod`, `i256_neg`, `i256_abs`

**Example — Convert wei to ETH:**
```sql
u256_to_string(
  to_u256(evt.event_params[3]) / to_u256('1000000000000000000')
) AS amount_eth
```

### Solana Decode Functions

```sql
-- Decode instruction data using IDL (returns STRUCT<name, value>)
_gs_decode_instruction_data(idl_json, data)

-- Decode program log messages using IDL
_gs_decode_log_message(idl_json, log_messages)

-- Program-specific decoders:
gs_solana_decode_token_program_instruction(data)
gs_solana_decode_system_program_instruction(data)
gs_solana_get_accounts(transaction_data)
gs_solana_get_balance_changes(transaction_data)
gs_solana_decode_associated_token_program_instruction(data)
gs_solana_decode_stake_program_instruction(data)
gs_solana_decode_vote_program_instruction(data)

-- Base58 decoding
_gs_from_base58(base58_string) -> BINARY
```

### Array Functions

```sql
-- Filter array elements by struct field matching a list of values
-- (prevents overflow panics by filtering BEFORE unnest)
array_filter_in(array, field_name, values_list) -> LIST

-- Convert list to large-list (i64 offsets) for very large arrays
to_large_list(array) -> LARGE_LIST

-- Filter array by field value
array_filter(array, field_name, value) -> LIST

-- Get first matching element
array_filter_first(array, field_name, value) -> STRUCT

-- Add index to each element
array_enumerate(array) -> LIST<STRUCT<index, value>>

-- Combine multiple arrays element-wise
zip_arrays(array1, array2, ...) -> LIST<STRUCT>
```

### JSON Functions

```sql
json_query(json_string, path) -> VARCHAR       -- Query JSON by path
json_value(json_string, path) -> VARCHAR       -- Extract scalar value
json_exists(json_string, path) -> BOOLEAN      -- Check path exists
is_json(string) -> BOOLEAN                     -- Validate JSON
parse_json(json_string) -> JSON                -- Parse (errors on invalid)
try_parse_json(json_string) -> JSON            -- Parse (NULL on invalid)
json_object(key1, val1, ...) -> JSON           -- Construct JSON object
json_array(val1, val2, ...) -> JSON            -- Construct JSON array
```

### Time Functions

```sql
to_timestamp(seconds) -> TIMESTAMP
to_timestamp_micros(microseconds) -> TIMESTAMP
now() -> TIMESTAMP                              -- volatile, current time
date_part('hour', timestamp) -> INT             -- extract timestamp parts
```

### `dynamic_table_check()` — Lookup Table Check

Check if a value exists in a dynamic table (async). Used with `dynamic_table` transforms.

```sql
WHERE dynamic_table_check('tracked_wallets', from_address)
```

### String & Encoding Functions

```sql
_gs_hex_to_byte(hex_string) -> BINARY
_gs_byte_to_hex(bytes) -> VARCHAR
string_to_array(string, delimiter) -> LIST<VARCHAR>
regexp_extract(string, pattern, group_index) -> VARCHAR
regexp_replace(string, pattern, replacement) -> VARCHAR
```

### Standard SQL Functions

All Apache DataFusion SQL functions are also available: `lower`, `upper`, `trim`, `substring`, `concat`, `replace`, `reverse`, `COALESCE`, `CASE WHEN`, `CAST`, etc.

```sql
-- Common patterns
lower('0xABC...')                              -- case-insensitive address
CONCAT('base', '-', COALESCE(addr, ''))        -- composite keys
COALESCE(balance.contract_address, '')         -- null-safe values
to_timestamp(block_timestamp) AS block_time    -- timestamp conversion
```

---

## Common Transform Patterns

### 1. Table Aliasing

Use table aliases to reference columns clearly, especially when column names are ambiguous:

```sql
SELECT
  balance.token_type,
  balance.owner_address,
  contract_address AS token_address,
  CAST(`balance` AS STRING) AS balance_amount
FROM my_balances_source balance
WHERE balance.token_type = 'ERC_20'
  AND balance.balance IS NOT NULL
```

**Null checks:** Use `IS NULL` and `IS NOT NULL` to filter on nullable columns:
```sql
WHERE balance.token_type IS NULL    -- native token (no token type)
WHERE balance.balance IS NOT NULL   -- only rows with a balance value
```

### 2. Simple Filtering (WHERE)

Filter rows from a source by column values:

```yaml
transforms:
  usdc_transfers:
    type: sql
    primary_key: id
    sql: |
      SELECT *
      FROM base_transfers
      WHERE address = lower('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')
```

### 3. Column Projection and Aliasing

Select and rename specific columns:

```yaml
transforms:
  clean_transfers:
    type: sql
    primary_key: id
    sql: |
      SELECT
        id,
        block_number,
        to_timestamp(block_timestamp) AS block_time,
        address AS token_address,
        sender,
        recipient,
        amount
      FROM my_source
```

### 4. Type Casting and Numeric Scaling

Cast values between types. Supported CAST targets include `DOUBLE`, `STRING`, `VARCHAR`, `DECIMAL(p,s)`, `INT`, `BIGINT`.

```sql
-- Convert from raw uint256 to human-readable amounts
(CAST(decoded.event_params[3] AS DOUBLE) / 1e6) AS amount_usdc    -- 6 decimals (USDC)
(CAST(decoded.event_params[3] AS DOUBLE) / 1e18) AS amount_eth    -- 18 decimals (ETH, most ERC-20s)
(CAST(decoded.event_params[3] AS DOUBLE) / 1e8) AS amount_btc     -- 8 decimals (WBTC)

-- Cast to STRING to preserve precision for very large numbers (e.g., raw balances)
CAST(`balance` AS STRING) AS balance_amount
```

Common decimal places by token:

| Token          | Decimals | Divisor |
| -------------- | -------- | ------- |
| USDC, USDT     | 6        | `1e6`   |
| WBTC           | 8        | `1e8`   |
| ETH, most ERC-20 | 18    | `1e18`  |

### 5. Conditional Logic with CASE WHEN

Derive new columns based on conditions:

```sql
-- Determine trade side based on asset type
CASE WHEN decoded.event_params[4] = '0' THEN 'BUY' ELSE 'SELL' END AS side

-- Conditional amount extraction
(CASE
  WHEN decoded.event_params[4] = '0'
  THEN CAST(decoded.event_params[6] AS DOUBLE)
  ELSE CAST(decoded.event_params[7] AS DOUBLE)
END / 1e6) AS amount_usdc

-- Classify transaction types
CASE
  WHEN decoded.event_params[3] = '0x4bfb...' THEN 'taker'
  WHEN decoded.event_params[3] = '0xc5d5...' THEN 'taker'
  ELSE 'maker'
END AS order_type
```

### 6. String Manipulation

```sql
-- Prepend '0x' to hex values from decoded params
'0x' || decoded.event_params[4] AS condition_id

-- Static string values
'TRADE' AS tx_type
'' AS placeholder_field
```

### 7. Exclusion Filters

Exclude known contract/system addresses from user-facing data:

```sql
WHERE decoded.event_params[1] NOT IN (
  '0x4bfb41d5b3570defd03c39a9a4d8de6bd8b8982e',
  '0xc5d563a36ae78145c45a50134d48a1215220f80a',
  '0x4d97dcd97ec945f40cf65f87097ace5ea0476045'
)
```

### 8. Price Calculations

Derive price from filled amounts:

```sql
-- price = cost / quantity
(CASE
  WHEN decoded.event_params[4] = '0'
  THEN CAST(decoded.event_params[6] AS DOUBLE)
  ELSE CAST(decoded.event_params[7] AS DOUBLE)
END / CASE
  WHEN decoded.event_params[4] = '0'
  THEN CAST(decoded.event_params[7] AS DOUBLE)
  ELSE CAST(decoded.event_params[6] AS DOUBLE)
END) AS price
```

---

## Advanced Patterns

### Decode Once, Filter Many

When working with raw logs from multiple contract events, decode **all events in a single transform** and then create separate downstream transforms that filter by `decoded.event_signature`. This is more efficient than creating multiple decode transforms.

```yaml
transforms:
  # Single decode step — include ALL event ABIs
  all_decoded:
    type: sql
    primary_key: id
    sql: |
      SELECT
        _gs_log_decode('[...full ABI with all events...]', topics, `data`) AS `decoded`,
        id, block_number, transaction_hash, address, block_timestamp
      FROM raw_logs_source

  # Downstream: each transform filters for one event type
  transfers:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, decoded.event_params[1] AS from_addr, ...
      FROM all_decoded
      WHERE decoded.event_signature = 'Transfer'

  approvals:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, decoded.event_params[1] AS owner, ...
      FROM all_decoded
      WHERE decoded.event_signature = 'Approval'
```

Even if you only need one event type downstream, it's fine to include the full ABI — unmatched events are simply ignored by the downstream WHERE filter.

### Transform Chaining

Build multi-step pipelines where each transform reads from the previous one:

```yaml
transforms:
  # Step 1: Decode raw logs
  decoded:
    type: sql
    primary_key: id
    sql: |
      SELECT
        _gs_log_decode('[...]', topics, data) AS decoded,
        id, block_number, transaction_hash, address, block_timestamp
      FROM raw_logs_source

  # Step 2: Extract specific event fields
  transfers:
    type: sql
    primary_key: id
    sql: |
      SELECT
        id, block_number, block_timestamp, transaction_hash,
        decoded.event_params[1] AS from_address,
        decoded.event_params[2] AS to_address,
        (CAST(decoded.event_params[3] AS DOUBLE) / 1e18) AS amount
      FROM decoded
      WHERE decoded.event_signature = 'Transfer'

  # Step 3: Add computed columns
  enriched_transfers:
    type: sql
    primary_key: id
    sql: SELECT *, 'ethereum' AS chain FROM transfers
```

### UNION ALL — Combining Multiple Event Types

Combine multiple transforms with identical schemas into a single output. Every SELECT in the UNION must have the **exact same columns in the same order**.

```yaml
transforms:
  # Individual event transforms (each with identical output columns)
  transfers:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, block_timestamp, transaction_hash,
        decoded.event_params[1] AS user_id,
        (CAST(decoded.event_params[3] AS DOUBLE) / 1e18) AS amount,
        'TRANSFER' AS event_type
      FROM decoded_events
      WHERE decoded.event_signature = 'Transfer'

  approvals:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, block_timestamp, transaction_hash,
        decoded.event_params[1] AS user_id,
        (CAST(decoded.event_params[3] AS DOUBLE) / 1e18) AS amount,
        'APPROVAL' AS event_type
      FROM decoded_events
      WHERE decoded.event_signature = 'Approval'

  # Combined output
  all_events:
    type: sql
    primary_key: id
    sql: |
      SELECT * FROM transfers
      UNION ALL
      SELECT * FROM approvals
```

**UNION ALL rules:**
- All SELECTs must produce the **same number of columns** with **compatible types**
- Use empty strings (`''`) or zero (`0`) as placeholders for columns that don't apply to a particular event type
- `UNION ALL` keeps duplicates (use `UNION` to deduplicate, but `UNION ALL` is preferred for performance)
- You can UNION as many transforms as needed

### Normalizing Disparate Events to a Common Schema

When different events have different fields, map them all to a unified schema using placeholder values:

```yaml
transforms:
  trades:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, block_timestamp, transaction_hash, address,
        decoded.event_params[2] AS user_id,
        decoded.event_params[4] AS asset,
        '' AS condition_id,                    -- not applicable for trades
        (CAST(decoded.event_params[6] AS DOUBLE) / 1e6) AS amount_usdc,
        'TRADE' AS tx_type,
        CASE WHEN decoded.event_params[4] = '0' THEN 'BUY' ELSE 'SELL' END AS side,
        (CAST(decoded.event_params[8] AS DOUBLE) / 1e6) AS fee
      FROM decoded_events
      WHERE decoded.event_signature = 'OrderFilled'

  redemptions:
    type: sql
    primary_key: id
    sql: |
      SELECT id, block_number, block_timestamp, transaction_hash, address,
        decoded.event_params[1] AS user_id,
        '' AS asset,                           -- not applicable for redemptions
        '0x' || decoded.event_params[4] AS condition_id,
        (CAST(decoded.event_params[6] AS DOUBLE) / 1e6) AS amount_usdc,
        'REDEEM' AS tx_type,
        '' AS side,                            -- not applicable for redemptions
        0 AS fee                               -- no fee for redemptions
      FROM decoded_events
      WHERE decoded.event_signature = 'PayoutRedemption'

  all_activities:
    type: sql
    primary_key: id
    sql: |
      SELECT * FROM trades
      UNION ALL
      SELECT * FROM redemptions
```

### Adding Columns to an Existing Transform

Extend a transform's output without rewriting it:

```yaml
  activities_v2:
    type: sql
    primary_key: id
    sql: SELECT *, '' AS builder FROM all_activities
```

---

## Source-Level Filtering

For efficiency, filter data **at the source** before it reaches transforms. Use the `filter:` field on dataset sources to reduce the volume of data processed:

```yaml
sources:
  my_logs:
    type: dataset
    dataset_name: matic.raw_logs
    version: 1.0.0
    start_at: earliest
    filter: >-
      address IN ('0xabc...', '0xdef...')
      AND block_number > 50000000
```

This is significantly more efficient than filtering in a transform because it reduces data at the ingestion layer.

### Bounded Historical Backfill

To process historical data starting from a specific block (not genesis), combine `start_at: earliest` with a `block_number` floor in the filter:

```yaml
sources:
  poly_logs:
    type: dataset
    dataset_name: matic.raw_logs
    version: 1.0.0
    start_at: earliest
    filter: >-
      address IN ('0xabc...', '0xdef...')
      AND block_number >= 82422949
```

This processes all data from block 82422949 onward, rather than from genesis or only latest. Useful when:
- A contract was deployed at a known block
- You only need data from a certain date forward
- You want to avoid processing irrelevant ancient blocks

**Combine source filtering with transform filtering:**
- Source `filter:` → coarse pre-filtering (contract addresses, block ranges)
- Transform `WHERE` → fine-grained filtering (event types, parameter values, exclusions)

---

## Debugging Transforms

### Common Errors

**"Unknown source reference"**
The `FROM` clause references a name that doesn't match any source or transform key in the YAML. Check for typos.

**"Missing primary_key"**
Every transform needs `primary_key`. Almost always use `id` (carried from the source data).

**"Column not found"**
Column name doesn't exist on the source. Use `goldsky turbo inspect <pipeline> -n <source_node>` to see actual column names.

**Empty results from decoded events**
- Verify the ABI JSON matches the actual contract events
- Check `decoded.event_signature` matches the event name exactly (case-sensitive)
- Ensure `address` filter matches the correct contract
- Check `decoded.event_params[N]` indexing — parameters are **1-indexed**

**Type mismatch in UNION ALL**
All branches of a UNION ALL must have identical column counts and compatible types. Add placeholder columns (`''`, `0`) where needed.

### Inspecting Transform Output

Use the TUI inspector to see data at any node in the pipeline:

```bash
# Inspect a specific transform's output
goldsky turbo inspect <pipeline-name> -n <transform_name>
```

This helps verify that decoded fields, casts, and filters are producing expected results.

---

## Complete Example: Multi-Event Activity Feed

This end-to-end example shows how to build a unified activity feed from raw logs. See the template file `templates/multi-event-activity-feed.yaml` for the full working YAML.

**Pattern:**
1. Source raw logs filtered by contract addresses
2. Decode all events with `_gs_log_decode()`
3. Create individual transforms per event type, each mapping to a common schema
4. Combine with `UNION ALL`
5. Sink to a database

---

## Sink Batching Configuration

Database and streaming sinks support batching to tune latency vs throughput:

```yaml
sinks:
  my_sink:
    type: clickhouse
    from: my_transform
    table: my_table
    secret_name: MY_SECRET
    primary_key: id
    batch_size: 1000           # rows per batch
    batch_flush_interval: 300ms # max time before flushing
```

| Setting                | Description                              | Trade-off                        |
| ---------------------- | ---------------------------------------- | -------------------------------- |
| `batch_size`           | Max rows accumulated before flushing     | Higher = more throughput         |
| `batch_flush_interval` | Max wait time before flushing a batch    | Lower = lower latency            |

**Guidelines:**
- Latency-sensitive (real-time dashboards): `batch_flush_interval: 300ms`, `batch_size: 1000`
- Moderate throughput (trade data, events): `batch_flush_interval: 1000ms`, `batch_size: 1000`
- High-volume streaming (balance snapshots): `batch_flush_interval: 10s`, `batch_size: 100000`

---

## TypeScript / WASM Script Transforms

For logic SQL can't express: custom parsing, BigInt arithmetic, stateful processing, or complex conditionals. Schema types: `string`, `uint64`, `int64`, `float64`, `boolean`, `bytes`.

Key rules: define `function invoke(data)`, return `null` to filter a record, return an object matching the schema, no async/await or external imports.

See `references/typescript-transforms.md` for full docs, schema field reference, examples, and the when-to-use-script-vs-SQL table. Also includes Handler transforms for HTTP enrichment via external APIs.

---

## Dynamic Table Transforms

Updatable lookup tables for allowlists, blocklists, and join-style enrichment — without redeploying. Backed by either PostgreSQL (durable, externally updatable) or in-memory (fast, ephemeral). Use `dynamic_table_check('table_name', column)` in SQL transforms to filter records.

See `references/dynamic-tables.md` for full config, backend options, `dynamic_table_check()` usage, REST API updates, and a complete wallet-tracking example.

---

## Solana Transform Patterns

For decoding Solana instructions with IDL, program-specific decoders (Token, System, Stake, Vote programs), and SPL token tracking.

See `references/solana-patterns.md` for IDL-based decoding, all built-in program decoders, a full example pipeline, and detailed array/JSON/hex function usage examples.

---

## Related

- **`/turbo-builder`** — Build and deploy pipelines interactively using these transforms
- **`/turbo-doctor`** — Diagnose and fix pipeline issues (including transform errors)
- **`/turbo-pipelines`** — Pipeline YAML configuration reference
- **`/turbo-architecture`** — Architecture decisions (source types, data flow patterns, resource sizing)
- **`/datasets`** — Blockchain dataset and chain prefix reference
- **`/turbo-monitor-debug`** — Monitoring and debugging reference
