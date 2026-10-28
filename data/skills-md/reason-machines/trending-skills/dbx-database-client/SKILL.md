---
name: dbx-database-client
description: Open-source lightweight cross-platform database management tool built with Tauri, Vue 3, and Rust supporting MySQL, PostgreSQL, SQLite, Redis, MongoDB, DuckDB, ClickHouse, and SQL Server.
triggers:
  - set up dbx database client
  - add database connection in dbx
  - how to use dbx with postgres
  - dbx query editor shortcuts
  - configure AI SQL assistant in dbx
  - dbx redis browser setup
  - export data from dbx
  - build dbx from source
---

# DBX Database Client

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

DBX is an open-source, lightweight (~15 MB), cross-platform database management GUI built with Tauri 2 (Rust backend) + Vue 3 frontend. It supports MySQL, PostgreSQL, SQLite, Redis, MongoDB, DuckDB, ClickHouse, SQL Server, MariaDB, TiDB, and more — with no bundled Chromium.

## Installation

### Download Pre-built Binary

Download the latest installer from [Releases](https://github.com/t8y2/dbx/releases).

**macOS (unsigned app workaround):**
```bash
xattr -cr /Applications/dbx.app
```
Or: System Settings → Privacy & Security → Open Anyway.

### Build from Source

**Prerequisites:**
- Node.js >= 18
- pnpm
- Rust >= 1.77

```bash
git clone https://github.com/t8y2/dbx.git
cd dbx
pnpm install
pnpm tauri dev        # Development mode
pnpm tauri build      # Production build → src-tauri/target/release/bundle/
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Tauri 2 |
| Frontend | Vue 3 + TypeScript |
| UI | shadcn-vue + Tailwind CSS |
| Editor | CodeMirror 6 |
| Backend | Rust + sqlx / tiberius / redis-rs / mongodb |

## Project Structure

```
dbx/
├── src/                    # Vue 3 frontend
│   ├── components/         # UI components
│   │   ├── ConnectionForm.vue
│   │   ├── QueryEditor.vue
│   │   ├── DataGrid.vue
│   │   └── SchemaBrowser.vue
│   ├── stores/             # Pinia stores
│   ├── composables/        # Vue composables
│   └── locales/            # i18n (en, zh-CN)
├── src-tauri/              # Rust backend
│   ├── src/
│   │   ├── commands/       # Tauri commands (IPC)
│   │   ├── db/             # Database drivers
│   │   │   ├── mysql.rs
│   │   │   ├── postgres.rs
│   │   │   ├── sqlite.rs
│   │   │   ├── redis.rs
│   │   │   ├── mongodb.rs
│   │   │   ├── duckdb.rs
│   │   │   └── clickhouse.rs
│   │   └── main.rs
│   ├── Cargo.toml
│   └── tauri.conf.json
└── package.json
```

## Adding a Database Connection

DBX stores connections locally. In the UI, click **+ New Connection** and fill in:

| Field | Description |
|-------|-------------|
| Type | MySQL / PostgreSQL / SQLite / Redis / MongoDB / DuckDB / ClickHouse / SQL Server |
| Host | Database host (e.g., `localhost`) |
| Port | Default port auto-fills by type |
| Database | Database/schema name |
| Username | DB user |
| Password | DB password (stored encrypted locally) |
| SSH Tunnel | Optional: host, port, user, key/password |

### Connection String Examples

```
# MySQL / MariaDB / TiDB
mysql://user:password@localhost:3306/mydb

# PostgreSQL / openGauss / GaussDB
postgresql://user:password@localhost:5432/mydb

# SQLite (file path or drag & drop .db file)
/path/to/database.db

# Redis
redis://localhost:6379
redis://:password@localhost:6379/0

# MongoDB
mongodb://user:password@localhost:27017/mydb
mongodb+srv://user:password@cluster.mongodb.net/mydb

# ClickHouse
clickhouse://user:password@localhost:8123/default

# DuckDB
/path/to/database.duckdb
```

## Query Editor

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + Enter` | Execute query |
| `Cmd/Ctrl + scroll` | Zoom editor font size |
| `Cmd/Ctrl + /` | Toggle comment |
| `Cmd/Ctrl + Z` | Undo |

### Features
- CodeMirror 6 with SQL syntax highlighting
- Multi-statement execution
- Safety dialogs for destructive operations (`DROP`, `DELETE`, `TRUNCATE`, `ALTER`)
- Query history with search, restore, one-click copy

## AI SQL Assistant Configuration

DBX supports Claude and OpenAI for natural language → SQL, explain, optimize, and fix errors.

Configure via Settings → AI Assistant:

```typescript
// Environment variables used by the app (set in your shell or .env)
OPENAI_API_KEY=sk-...        // OpenAI key
ANTHROPIC_API_KEY=sk-ant-... // Claude/Anthropic key
```

**Capabilities:**
- **Generate**: "Show me all users who signed up last month"
- **Explain**: Highlights query → "Explain this SQL"
- **Optimize**: "Why is this query slow?"
- **Fix**: Paste error → "Fix this query"

## Data Grid Features

- Virtual scrolling for large datasets
- Inline cell editing
- Column resize by drag
- Row numbers and zebra stripes
- Sort by column header click
- Search/filter rows
- Pagination controls

**Export options:** CSV, JSON, Markdown (toolbar button or right-click)

## Schema Browser

Left sidebar tree structure:
```
Connection
└── Database/Schema
    ├── Tables
    │   └── table_name
    │       ├── Columns (name, type, nullable)
    │       ├── Indexes
    │       ├── Foreign Keys
    │       └── Triggers
    ├── Views
    └── Procedures
```

Double-click a table → opens data grid with `SELECT * FROM table LIMIT 1000`.

## Redis Browser

- Key pattern search (e.g., `user:*`, `session:*`)
- Value viewer for all Redis types:
  - **String**: raw value display
  - **Hash**: field/value table
  - **List**: indexed list
  - **Set**: member list
  - **ZSet**: score/member table
- TTL display and key deletion

## MongoDB Browser

- Database → Collection tree
- Document list with pagination
- CRUD: Create, Read, Update, Delete documents
- JSON document editor

## SSH Tunnel

Configure SSH tunnel in the connection form:

```
SSH Host: bastion.example.com
SSH Port: 22
SSH User: ec2-user
Auth:     Key (paste private key) OR Password
```

The tunnel proxies the DB connection through the SSH host — useful for databases not exposed to the internet.

## Drag & Drop Files

Drag `.db`, `.sqlite`, or `.duckdb` files directly onto the DBX window to open them instantly without configuring a connection.

## Frontend Development Patterns

### Invoking Rust Commands from Vue

```typescript
// src/composables/useDatabase.ts
import { invoke } from '@tauri-apps/api/core'

interface QueryResult {
  columns: string[]
  rows: Record<string, unknown>[]
  rowsAffected: number
  executionTime: number
}

export function useDatabase() {
  const executeQuery = async (connectionId: string, sql: string): Promise<QueryResult> => {
    return await invoke('execute_query', {
      connectionId,
      sql,
    })
  }

  const testConnection = async (config: ConnectionConfig): Promise<boolean> => {
    return await invoke('test_connection', { config })
  }

  return { executeQuery, testConnection }
}
```

### Adding a New Rust Command

```rust
// src-tauri/src/commands/query.rs
use tauri::State;
use crate::db::ConnectionPool;

#[tauri::command]
pub async fn execute_query(
    connection_id: String,
    sql: String,
    pool: State<'_, ConnectionPool>,
) -> Result<QueryResult, String> {
    let conn = pool.get(&connection_id)
        .ok_or("Connection not found")?;
    
    conn.query(&sql).await.map_err(|e| e.to_string())
}
```

```rust
// src-tauri/src/main.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            execute_query,
            test_connection,
            // ... other commands
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Vue Component Example: Custom Query Panel

```vue
<!-- src/components/QueryPanel.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { invoke } from '@tauri-apps/api/core'
import { useConnectionStore } from '@/stores/connection'

const store = useConnectionStore()
const sql = ref('')
const results = ref(null)
const error = ref('')
const loading = ref(false)

async function runQuery() {
  if (!sql.value.trim()) return
  loading.value = true
  error.value = ''
  try {
    results.value = await invoke('execute_query', {
      connectionId: store.activeConnectionId,
      sql: sql.value,
    })
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-2 h-full">
    <textarea
      v-model="sql"
      class="font-mono text-sm border rounded p-2 h-40 resize-none"
      placeholder="SELECT * FROM users LIMIT 10"
      @keydown.meta.enter="runQuery"
      @keydown.ctrl.enter="runQuery"
    />
    <button
      :disabled="loading"
      class="px-4 py-2 bg-primary text-white rounded"
      @click="runQuery"
    >
      {{ loading ? 'Running...' : 'Run (Cmd+Enter)' }}
    </button>
    <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
    <DataGrid v-if="results" :data="results" />
  </div>
</template>
```

### Adding i18n Strings

```typescript
// src/locales/en.json
{
  "connection": {
    "new": "New Connection",
    "test": "Test Connection",
    "save": "Save"
  },
  "query": {
    "run": "Run Query",
    "history": "History"
  }
}

// src/locales/zh-CN.json
{
  "connection": {
    "new": "新建连接",
    "test": "测试连接",
    "save": "保存"
  }
}
```

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<template>
  <button>{{ t('connection.new') }}</button>
</template>
```

## Cargo.toml Key Dependencies

```toml
[dependencies]
tauri = { version = "2", features = ["native-tls-vendored"] }
sqlx = { version = "0.7", features = ["mysql", "postgres", "sqlite", "runtime-tokio-native-tls"] }
tiberius = "0.12"          # SQL Server
redis = "0.25"             # Redis
mongodb = "2.8"            # MongoDB
duckdb = "0.10"            # DuckDB
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

## Troubleshooting

### Build Fails on macOS (Rust linker error)
```bash
xcode-select --install
# Then retry:
pnpm tauri build
```

### "Connection refused" on localhost
- Check the database service is running: `brew services list` or `systemctl status mysql`
- Verify port isn't blocked: `lsof -i :5432`
- For Docker: ensure port is mapped `-p 5432:5432`

### SQLite "database is locked"
Close any other applications (like DB Browser for SQLite) with the file open before connecting in DBX.

### macOS App Won't Open (Gatekeeper)
```bash
xattr -cr /Applications/dbx.app
```

### Redis AUTH Error
Ensure the connection string includes the password:
```
redis://:yourpassword@localhost:6379
```

### MongoDB Atlas Connection
Use the full SRV connection string from Atlas → Connect → Drivers:
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/mydb?retryWrites=true&w=majority
```

### pnpm install Fails
```bash
node --version   # Must be >= 18
pnpm --version   # Install: npm i -g pnpm
rustup update    # Keep Rust current
```

### Query History Not Showing
History is stored in Tauri's app data directory:
- macOS: `~/Library/Application Support/dbx/`
- Linux: `~/.local/share/dbx/`
- Windows: `%APPDATA%\dbx\`

## Contributing

```bash
# Fork & clone
git clone https://github.com/YOUR_USERNAME/dbx.git
cd dbx
pnpm install

# Create feature branch
git checkout -b feat/my-new-database-driver

# Run in dev mode with hot reload
pnpm tauri dev

# Run frontend only (no Rust)
pnpm dev

# Type check
pnpm vue-tsc --noEmit

# Submit PR to t8y2/dbx main branch
```
