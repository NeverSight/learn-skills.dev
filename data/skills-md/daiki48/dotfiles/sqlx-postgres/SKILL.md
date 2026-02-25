---
name: sqlx-postgres
description: SQLx + PostgreSQL v17 database guide. Queries, migrations, ENUMs, JSONB, transactions.
---

# SQLx + PostgreSQL v17 Development Guide

## Compile-time Checked Queries

```rust
// query_as! (type-safe)
let user = sqlx::query_as!(
    User,
    r#"SELECT id, name, email, role as "role: UserRole" FROM users WHERE id = $1"#,
    id
).fetch_one(&pool).await?;

// Single column
let count = sqlx::query_scalar!("SELECT COUNT(*) FROM users WHERE active = true")
    .fetch_one(&pool).await?;

// INSERT/UPDATE/DELETE
sqlx::query!("INSERT INTO users (name, email) VALUES ($1, $2)", name, email)
    .execute(&pool).await?;
```

## Fetch Methods

```rust
.fetch_one(&pool)       // 1 row (error if 0 or 2+)
.fetch_optional(&pool)  // 0-1 row (Option<T>)
.fetch_all(&pool)       // All rows (Vec<T>)
.fetch(&pool)           // Stream (Stream<T>)
.execute(&pool)         // Execute only (PgQueryResult)
```

## PostgreSQL ENUM

```sql
-- Migration
CREATE TYPE user_role AS ENUM ('Admin', 'AreaManager', 'ServiceStation');
```

```rust
#[derive(Debug, Clone, sqlx::Type, Serialize, Deserialize)]
#[sqlx(type_name = "user_role", rename_all = "PascalCase")]
pub enum UserRole { Admin, AreaManager, ServiceStation }

// Query (cast required)
sqlx::query_as!(User, r#"SELECT role as "role: UserRole" FROM users"#)
```

## JSONB

```rust
#[derive(Debug, Serialize, Deserialize)]
pub struct Metadata { pub tags: Vec<String> }

// INSERT
sqlx::query!("INSERT INTO items (metadata) VALUES ($1)", sqlx::types::Json(metadata) as _)
    .execute(&pool).await?;

// SELECT
sqlx::query_as!(Item, r#"SELECT metadata as "metadata: Json<Metadata>" FROM items"#)
```

## Transactions

```rust
let mut tx = pool.begin().await?;

sqlx::query!("INSERT INTO users (name) VALUES ($1)", name)
    .execute(&mut *tx).await?;

sqlx::query!("INSERT INTO profiles (user_id) VALUES ($1)", user_id)
    .execute(&mut *tx).await?;

tx.commit().await?;
// Error → tx drops → auto rollback
```

## Pagination

```rust
#[derive(Deserialize)]
pub struct Pagination { page: Option<i64>, per_page: Option<i64> }

impl Pagination {
    pub fn offset(&self) -> i64 { (self.page.unwrap_or(1) - 1) * self.per_page() }
    pub fn per_page(&self) -> i64 { self.per_page.unwrap_or(20).min(100) }
}

sqlx::query_as!(User, "SELECT * FROM users LIMIT $1 OFFSET $2",
    pagination.per_page(), pagination.offset())
```

## Bulk INSERT (UNNEST)

```rust
let names: Vec<String> = items.iter().map(|i| i.name.clone()).collect();
let values: Vec<i32> = items.iter().map(|i| i.value).collect();

sqlx::query!(
    "INSERT INTO items (name, value) SELECT * FROM UNNEST($1::text[], $2::int[])",
    &names, &values
).execute(&pool).await?;
```

## UPSERT

```rust
sqlx::query!(
    r#"INSERT INTO prices (station_id, fuel_type, price)
       VALUES ($1, $2, $3)
       ON CONFLICT (station_id, fuel_type)
       DO UPDATE SET price = EXCLUDED.price, recorded_at = NOW()"#,
    station_id, fuel_type as _, price
).execute(&pool).await?;
```

## Dynamic Query (QueryBuilder)

```rust
let mut builder = QueryBuilder::new("SELECT * FROM users WHERE 1=1");

if let Some(name) = &filter.name {
    builder.push(" AND name ILIKE ").push_bind(format!("%{}%", name));
}
builder.push(" ORDER BY id LIMIT ").push_bind(limit);

builder.build_query_as::<User>().fetch_all(&pool).await?
```

## Migrations

```bash
sqlx migrate add create_users_table
sqlx migrate run
sqlx migrate revert
```

## Notes

1. **ENUM cast**: `role as "role: UserRole"` format required
2. **NULL**: Use `Option<T>` for nullable columns
3. **Compile-time check**: Requires `DATABASE_URL` env
4. **Offline mode**: `cargo sqlx prepare` generates .sqlx dir
5. **Connection**: `&pool` for normal, `&mut *tx` for transactions
