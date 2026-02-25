---
name: rusqlite-guide
description: rusqlite + SQLite database guide. Connection, CRUD, transactions, FTS5 full-text search, migrations.
---

# rusqlite + SQLite Development Guide

## Setup

```toml
[dependencies]
rusqlite = { version = "0.32", features = ["bundled"] }
dirs = "5.0"  # OS data directory
```

## Connection

```rust
use rusqlite::{Connection, Result};

let conn = Connection::open("app.db")?;           // File-based
let conn = Connection::open_in_memory()?;         // In-memory (tests)

// OS-specific data dir
fn get_db_path() -> PathBuf {
    dirs::data_local_dir().unwrap_or_else(|| PathBuf::from("."))
        .join("myapp").join("app.db")
}
// Linux: ~/.local/share/myapp/app.db
// Windows: C:\Users\<user>\AppData\Local\myapp\app.db

// Initialize
let conn = Connection::open(&db_path)?;
conn.execute_batch("PRAGMA foreign_keys = ON;")?;
run_migrations(&conn)?;
```

## CRUD

```rust
use rusqlite::params;

// INSERT
conn.execute("INSERT INTO entries (title) VALUES (?1)", params![title])?;
let id = conn.last_insert_rowid();

// SELECT (single)
conn.query_row("SELECT * FROM entries WHERE id = ?1", params![id], |row| {
    Ok(Entry { id: row.get(0)?, title: row.get(1)? })
})?

// SELECT (multiple)
let mut stmt = conn.prepare("SELECT * FROM entries LIMIT ?1")?;
let entries = stmt.query_map(params![limit], |row| {
    Ok(Entry { id: row.get(0)?, title: row.get(1)? })
})?.collect::<Result<Vec<_>>>()?;

// UPDATE
conn.execute("UPDATE entries SET title = ?1 WHERE id = ?2", params![title, id])?;

// DELETE
conn.execute("DELETE FROM entries WHERE id = ?1", params![id])?;
```

## Transactions

```rust
let tx = conn.transaction()?;

tx.execute("INSERT INTO entries (title) VALUES (?1)", params![title])?;
let entry_id = tx.last_insert_rowid();

tx.execute("INSERT INTO tags (name) VALUES (?1)", params![tag])?;

tx.commit()?;
// Error before commit → auto rollback on drop
```

## Named Parameters

```rust
use rusqlite::named_params;

conn.execute(
    "INSERT INTO entries (title, versioned) VALUES (:title, :versioned)",
    named_params! { ":title": title, ":versioned": versioned as i32 },
)?;
```

## Migrations (PRAGMA user_version)

```rust
fn run_migrations(conn: &Connection) -> Result<()> {
    let version: i32 = conn.query_row("PRAGMA user_version", [], |r| r.get(0))?;

    if version < 1 {
        conn.execute_batch(include_str!("../../migrations/001_initial.sql"))?;
        conn.execute("PRAGMA user_version = 1", [])?;
    }
    if version < 2 {
        conn.execute_batch(include_str!("../../migrations/002_add_field.sql"))?;
        conn.execute("PRAGMA user_version = 2", [])?;
    }
    Ok(())
}
```

## FTS5 Full-Text Search

```sql
-- Virtual table
CREATE VIRTUAL TABLE entries_fts USING fts5(title, code, memo, content='entry_versions', content_rowid='id');

-- Sync triggers
CREATE TRIGGER entry_versions_ai AFTER INSERT ON entry_versions BEGIN
    INSERT INTO entries_fts(rowid, title, code, memo) SELECT ev.id, e.title, ev.code, ev.memo
    FROM entry_versions ev JOIN entries e ON e.id = ev.entry_id WHERE ev.id = NEW.id;
END;
```

```rust
fn search(conn: &Connection, query: &str, limit: i64) -> Result<Vec<SearchResult>> {
    let fts_query = query.split_whitespace()
        .map(|w| format!("{}*", w)).collect::<Vec<_>>().join(" ");

    let mut stmt = conn.prepare(
        "SELECT ev.entry_id, e.title,
                snippet(entries_fts, 1, '<mark>', '</mark>', '...', 32) as code_snippet
         FROM entries_fts
         JOIN entry_versions ev ON entries_fts.rowid = ev.id
         JOIN entries e ON ev.entry_id = e.id
         WHERE entries_fts MATCH ?1 ORDER BY rank LIMIT ?2"
    )?;

    stmt.query_map(params![fts_query, limit], |row| {
        Ok(SearchResult { entry_id: row.get(0)?, title: row.get(1)?, snippet: row.get(2)? })
    })?.collect()
}
```

### FTS5 Query Syntax

| Syntax | Example | Meaning |
|--------|---------|---------|
| Word | `axum` | Contains "axum" |
| Multiple | `axum handler` | Contains both (AND) |
| Prefix | `hand*` | Starts with "hand" |
| Phrase | `"error handling"` | Exact phrase |
| OR | `axum OR leptos` | Either one |
| NOT | `axum NOT leptos` | Has axum, not leptos |

## Error Handling

```rust
use rusqlite::Error as SqliteError;

pub enum DbError {
    Sqlite(SqliteError),
    NotFound(i64),
}

impl From<SqliteError> for DbError {
    fn from(e: SqliteError) -> Self { DbError::Sqlite(e) }
}

// Convert QueryReturnedNoRows to NotFound
conn.query_row(...).map_err(|e| match e {
    SqliteError::QueryReturnedNoRows => DbError::NotFound(id),
    _ => DbError::Sqlite(e),
})
```

## SQLx (PostgreSQL) vs rusqlite

| Item | rusqlite | SQLx |
|------|----------|------|
| Compile-time check | No | `query!` macro |
| Connection | Sync (file) | Async (network) |
| Migrations | Manual (PRAGMA) | sqlx-cli |
| ENUM | No (use INTEGER) | Native |
| Full-text search | FTS5 | tsvector |
| Use case | Single-user app | Multi-user SaaS |
