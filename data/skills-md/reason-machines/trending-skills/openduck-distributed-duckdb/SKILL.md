---
name: openduck-distributed-duckdb
description: OpenDuck — open-source distributed DuckDB with differential storage, hybrid dual execution, and transparent remote database attach
triggers:
  - attach remote duckdb database
  - distributed duckdb setup
  - hybrid query execution duckdb
  - openduck differential storage
  - self-hosted motherduck alternative
  - split query local and remote duckdb
  - openduck extension setup
  - duckdb remote tables grpc
---

# OpenDuck Distributed DuckDB

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

OpenDuck is an open-source implementation of distributed DuckDB featuring differential storage (append-only immutable layers via Postgres + object store), hybrid dual execution (single queries split across local and remote workers), and transparent remote database attach via `ATTACH 'openduck:mydb'`. It is architecturally inspired by MotherDuck but fully open protocol (gRPC + Arrow IPC).

---

## Architecture Overview

```
DuckDB client (openduck extension)
  └─ ATTACH 'openduck:mydb?endpoint=...' AS cloud
       └─ gRPC + Arrow IPC
            └─ Gateway (Rust)
                 ├─ auth / routing / plan splitting
                 ├─ Worker 1 (embedded DuckDB)
                 └─ Worker N (embedded DuckDB)
                      ├─ Postgres (metadata)
                      └─ Object store (sealed layers)
```

**Key concepts:**
- `OpenDuckCatalog` / `OpenDuckTableEntry` — remote tables appear as first-class DuckDB catalog entries
- Hybrid execution — gateway labels operators `LOCAL` or `REMOTE`, inserts `Bridge` operators at boundaries
- Differential storage — immutable sealed layers, snapshot isolation, one write path, many readers
- Protocol — only 2 gRPC RPCs defined in `proto/openduck/v1/execution.proto`

---

## Repository Layout

```
crates/
  exec-gateway/     # auth, routing, hybrid plan splitting
  exec-worker/      # embedded DuckDB, Arrow IPC streaming
  exec-proto/       # protobuf/tonic codegen
  openduck-cli/     # unified CLI (serve|gateway|worker)
  diff-*/           # differential storage (layers, metadata, FUSE)

extensions/
  openduck/         # DuckDB C++ extension (StorageExtension + Catalog)

clients/
  python/           # pip-installable openduck wrapper

proto/
  openduck/v1/      # execution.proto
```

---

## Installation & Build

### Prerequisites

- Rust toolchain (stable)
- C++ build tools, `vcpkg`, `bison` (macOS: `brew install bison`)
- DuckDB development headers (handled by the extension Makefile)

### 1. Build the Rust backend

```bash
git clone https://github.com/CITGuru/openduck
cd openduck
cargo build --workspace
```

### 2. Build the DuckDB C++ extension

```bash
cd extensions/openduck
make
# Output:
# extensions/openduck/build/release/extension/openduck/openduck.duckdb_extension
```

### 3. Install the Python client (optional)

```bash
pip install -e clients/python
```

---

## Running the Server

```bash
# Required env vars
export OPENDUCK_TOKEN=your-secret-token

# Start all-in-one (gateway + worker)
cargo run -p openduck-cli -- serve -d mydb -t $OPENDUCK_TOKEN

# Or run gateway and worker separately
cargo run -p openduck-cli -- gateway --port 7878
cargo run -p openduck-cli -- worker --gateway http://localhost:7878
```

---

## Connecting from Python

### Via openduck wrapper (recommended)

```python
import openduck  # auto-detects extension from build tree or OPENDUCK_EXTENSION_PATH

con = openduck.connect("mydb")  # uses OPENDUCK_TOKEN env var
con.sql("SELECT 1 AS x").show()
con.sql("SELECT * FROM cloud.users LIMIT 10").show()
```

### Via raw DuckDB SDK

```python
import duckdb
import os

ext_path = os.environ["OPENDUCK_EXTENSION_PATH"]
# e.g. extensions/openduck/build/release/extension/openduck/openduck.duckdb_extension

con = duckdb.connect(config={"allow_unsigned_extensions": "true"})
con.execute(f"LOAD '{ext_path}';")
con.execute(
    "ATTACH 'openduck:mydb"
    "?endpoint=http://localhost:7878"
    f"&token={os.environ[\"OPENDUCK_TOKEN\"]}' AS cloud;"
)

# Query remote table
con.sql("SELECT * FROM cloud.users LIMIT 10").show()

# Hybrid query — local table joined with remote table
con.sql("""
    SELECT l.product_id, l.name, r.total_sales
    FROM local.products l
    JOIN cloud.sales r ON l.product_id = r.product_id
    WHERE r.total_sales > 1000
""").show()
```

### Environment variables

```bash
export OPENDUCK_TOKEN=your-secret-token
export OPENDUCK_EXTENSION_PATH=extensions/openduck/build/release/extension/openduck/openduck.duckdb_extension
export OPENDUCK_ENDPOINT=http://localhost:7878   # default
```

---

## Connecting from the CLI

```bash
duckdb -unsigned -c "
  LOAD 'extensions/openduck/build/release/extension/openduck/openduck.duckdb_extension';
  ATTACH 'openduck:mydb?endpoint=http://localhost:7878&token=${OPENDUCK_TOKEN}' AS cloud;
  SHOW ALL TABLES;
  SELECT * FROM cloud.users LIMIT 5;
"
```

---

## Connecting from Rust

```rust
use duckdb::{Connection, Result};

fn main() -> Result<()> {
    let conn = Connection::open_in_memory()?;
    let ext_path = std::env::var("OPENDUCK_EXTENSION_PATH").unwrap();
    let token = std::env::var("OPENDUCK_TOKEN").unwrap();

    conn.execute_batch(&format!(r#"
        SET allow_unsigned_extensions = true;
        LOAD '{ext_path}';
        ATTACH 'openduck:mydb?endpoint=http://localhost:7878&token={token}' AS cloud;
    "#))?;

    let mut stmt = conn.prepare("SELECT * FROM cloud.users LIMIT 10")?;
    let rows = stmt.query_map([], |row| {
        Ok(row.get::<_, String>(0)?)
    })?;

    for row in rows {
        println!("{}", row?);
    }
    Ok(())
}
```

---

## Hybrid Execution Pattern

Hybrid execution happens automatically — the gateway splits the logical plan:

```
[LOCAL]  HashJoin(l.id = r.id)
  [LOCAL]  Scan(products)       ← runs on your machine
  [LOCAL]  Bridge(REMOTE→LOCAL)
    [REMOTE] Scan(sales)        ← runs on remote worker
```

Write queries naturally — the extension handles routing:

```python
# This single query runs across two engines transparently
con.sql("""
    SELECT
        p.category,
        SUM(s.amount) AS revenue
    FROM local.products p          -- local table
    JOIN cloud.sales s             -- remote table
      ON p.id = s.product_id
    GROUP BY p.category
    ORDER BY revenue DESC
""").show()
```

---

## Differential Storage

Differential storage is managed server-side. Key properties:
- **Append-only sealed layers** stored in object storage (S3-compatible)
- **Postgres** stores layer metadata and snapshot pointers
- **Snapshot isolation** — readers always see a consistent view
- **One serialized write path** — many concurrent readers

From a client perspective it is fully transparent. DuckDB sees normal table semantics.

---

## ATTACH URL Reference

```
openduck:<database_name>?endpoint=<url>&token=<token>
```

| Parameter  | Default                    | Description                        |
|------------|----------------------------|------------------------------------|
| `endpoint` | `http://localhost:7878`    | Gateway URL                        |
| `token`    | `$OPENDUCK_TOKEN` env var  | Auth token matching server config  |

Examples:
```sql
-- Local dev
ATTACH 'openduck:mydb?token=dev-token' AS cloud;

-- Remote server, explicit endpoint
ATTACH 'openduck:mydb?endpoint=https://my-server.example.com&token=prod-token' AS cloud;

-- Alias: od: also works
ATTACH 'od:mydb?endpoint=http://localhost:7878&token=dev-token' AS cloud;
```

---

## DuckLake Integration

OpenDuck and DuckLake operate at different layers and complement each other:

```python
import duckdb, os

ext_path = os.environ["OPENDUCK_EXTENSION_PATH"]
token = os.environ["OPENDUCK_TOKEN"]

con = duckdb.connect(config={"allow_unsigned_extensions": "true"})
con.execute(f"LOAD '{ext_path}';")

# Attach DuckLake catalog (managed by remote worker backed by DuckLake)
con.execute(f"ATTACH 'openduck:lakehouse?endpoint=http://localhost:7878&token={token}' AS lh;")

# Query DuckLake tables transparently via OpenDuck transport
con.sql("SELECT * FROM lh.events WHERE event_date = today()").show()

# Hybrid: local scratch data joined with remote DuckLake table
con.sql("""
    SELECT l.session_id, r.user_email
    FROM memory.sessions l
    JOIN lh.users r ON l.user_id = r.id
""").show()
```

---

## Protocol Reference

The wire protocol is intentionally minimal. See `proto/openduck/v1/execution.proto`:

- **`ExecuteQuery`** — send SQL, receive a query handle
- **`StreamResults`** — stream Arrow IPC record batches back to client

Any gRPC service implementing these two RPCs is a valid OpenDuck backend. You can replace the Rust gateway with a custom implementation in any language.

---

## Common Patterns

### Check which tables are available remotely

```sql
-- After ATTACH ... AS cloud
SHOW ALL TABLES;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'cloud';
```

### Write to a remote table

```sql
INSERT INTO cloud.events SELECT * FROM read_parquet('local_dump.parquet');
```

### Create a remote table from local data

```sql
CREATE TABLE cloud.new_table AS SELECT * FROM local_csv LIMIT 0;
INSERT INTO cloud.new_table SELECT * FROM local_csv;
```

### Export remote query result to local Parquet

```python
con.sql("SELECT * FROM cloud.large_table WHERE region = 'us-east'") \
   .write_parquet("output/us_east.parquet")
```

---

## Troubleshooting

### `Extension is not trusted` / signature error

```python
# Always set allow_unsigned_extensions before loading
con = duckdb.connect(config={"allow_unsigned_extensions": "true"})
```

Or in CLI:
```bash
duckdb -unsigned
```

### `LOAD` fails — extension not found

```bash
# Set the env var to the exact built path
export OPENDUCK_EXTENSION_PATH=$(pwd)/extensions/openduck/build/release/extension/openduck/openduck.duckdb_extension
ls -la $OPENDUCK_EXTENSION_PATH   # confirm it exists
```

### Connection refused to gateway

```bash
# Verify server is running
cargo run -p openduck-cli -- serve -d mydb -t $OPENDUCK_TOKEN
# Default port is 7878 — check firewall / port binding
curl http://localhost:7878/health
```

### Token mismatch / auth failure

```bash
# Server token and client token must match exactly
export OPENDUCK_TOKEN=same-value-on-both-sides
# Server: cargo run -p openduck-cli -- serve -d mydb -t $OPENDUCK_TOKEN
# Client: ATTACH '...&token=same-value-on-both-sides' AS cloud;
```

### Build fails on macOS — bison version

```bash
brew install bison
export PATH="$(brew --prefix bison)/bin:$PATH"
cd extensions/openduck && make
```

### Extension version mismatch with DuckDB

The extension must be built against the same DuckDB version as the Python package:

```bash
python -c "import duckdb; print(duckdb.__version__)"
# Ensure the extension Makefile targets the same version
# Check extensions/openduck/Makefile for DUCKDB_VERSION
```

---

## OpenDuck vs Alternatives

| Feature | OpenDuck | Arrow Flight SQL | DuckLake |
|---|---|---|---|
| Remote attach UX | `ATTACH 'openduck:db'` | Separate driver | `ATTACH 'ducklake:...'` |
| Hybrid execution | ✅ split plan | ❌ full remote | ❌ |
| DuckDB catalog integration | ✅ native | ❌ | ✅ |
| Protocol RPCs | 2 | ~15 | N/A |
| Differential storage | ✅ | ❌ | via Parquet layers |
| Self-hosted | ✅ | ✅ | ✅ |
