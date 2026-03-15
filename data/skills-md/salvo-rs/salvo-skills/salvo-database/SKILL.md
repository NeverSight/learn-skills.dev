---
name: salvo-database
description: Integrate databases with Salvo using SQLx, Diesel, SeaORM, or other ORMs. Use for persistent data storage and database operations.
---

# Salvo Database Integration

This skill helps integrate databases with Salvo applications.

## SQLx (Async, Compile-time Checked)

### Setup

```toml
[dependencies]
salvo = "0.89.0"
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
serde = { version = "1", features = ["derive"] }
```

### Connection Pool with Depot Injection

```rust
use salvo::prelude::*;
use salvo::affix_state;
use sqlx::PgPool;

#[tokio::main]
async fn main() {
    let pool = PgPool::connect("postgres://user:pass@localhost/db")
        .await
        .expect("Failed to connect to database");

    let router = Router::new()
        .hoop(affix_state::inject(pool))
        .get(list_users);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

### Query Handlers

```rust
use salvo::prelude::*;
use sqlx::{FromRow, PgPool};
use serde::Serialize;

#[derive(FromRow, Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[handler]
async fn list_users(depot: &mut Depot) -> Result<Json<Vec<User>>, StatusError> {
    let pool = depot.obtain::<PgPool>()
        .ok_or_else(|| StatusError::internal_server_error())?;

    let users = sqlx::query_as::<_, User>("SELECT id, name, email FROM users")
        .fetch_all(pool)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(Json(users))
}

#[handler]
async fn create_user(body: JsonBody<CreateUser>, depot: &mut Depot) -> Result<StatusCode, StatusError> {
    let pool = depot.obtain::<PgPool>()
        .ok_or_else(|| StatusError::internal_server_error())?;
    let user = body.into_inner();

    sqlx::query("INSERT INTO users (name, email) VALUES ($1, $2)")
        .bind(&user.name)
        .bind(&user.email)
        .execute(pool)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(StatusCode::CREATED)
}

#[handler]
async fn get_user(req: &mut Request, depot: &mut Depot) -> Result<Json<User>, StatusError> {
    let pool = depot.obtain::<PgPool>()
        .ok_or_else(|| StatusError::internal_server_error())?;
    let id = req.param::<i64>("id")
        .ok_or_else(|| StatusError::bad_request())?;

    let user = sqlx::query_as::<_, User>("SELECT id, name, email FROM users WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await
        .map_err(|_| StatusError::internal_server_error())?
        .ok_or_else(|| StatusError::not_found())?;

    Ok(Json(user))
}
```

## SeaORM (Async ORM)

### Setup

```toml
[dependencies]
salvo = "0.89.0"
sea-orm = { version = "1.0", features = ["sqlx-postgres", "runtime-tokio-native-tls", "macros"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

### Connection with Depot Injection

```rust
use salvo::prelude::*;
use salvo::affix_state;
use sea_orm::{Database, DatabaseConnection};

#[tokio::main]
async fn main() {
    let db = Database::connect("postgres://user:pass@localhost/db")
        .await
        .expect("Failed to connect");

    let router = Router::new()
        .hoop(affix_state::inject(db))
        .get(list_users);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

### Entity Operations

```rust
use salvo::prelude::*;
use sea_orm::*;

// Assuming entities are generated with sea-orm-cli

#[handler]
async fn list_users(depot: &mut Depot) -> Result<Json<Vec<user::Model>>, StatusError> {
    let db = depot.obtain::<DatabaseConnection>()
        .ok_or_else(|| StatusError::internal_server_error())?;

    let users = user::Entity::find()
        .all(db)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(Json(users))
}

#[handler]
async fn show_user(id: PathParam<i64>, depot: &mut Depot) -> Result<Json<user::Model>, StatusError> {
    // Route: Router::with_path("users/{id}").get(show_user)
    let db = depot.obtain::<DatabaseConnection>().unwrap();

    let user = user::Entity::find_by_id(id)
        .one(db)
        .await
        .map_err(|_| StatusError::internal_server_error())?
        .ok_or_else(|| StatusError::not_found())?;

    Ok(Json(user))
}

#[handler]
async fn create_user(body: JsonBody<CreateUser>, depot: &mut Depot) -> Result<StatusCode, StatusError> {
    let db = depot.obtain::<DatabaseConnection>()
        .ok_or_else(|| StatusError::internal_server_error())?;
    let data = body.into_inner();

    let user = user::ActiveModel {
        name: Set(data.name),
        email: Set(data.email),
        ..Default::default()
    };

    user.insert(db).await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(StatusCode::CREATED)
}
```

## Diesel (Sync ORM)

### Setup

```toml
[dependencies]
salvo = "0.89.0"
diesel = { version = "2.2", features = ["postgres", "r2d2"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

### Connection Pool with Depot Injection

```rust
use salvo::prelude::*;
use salvo::affix_state;
use diesel::r2d2::{self, ConnectionManager};
use diesel::PgConnection;

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[tokio::main]
async fn main() {
    let manager = ConnectionManager::<PgConnection>::new("postgres://user:pass@localhost/db");
    let pool = r2d2::Pool::builder()
        .build(manager)
        .expect("Failed to create pool");

    let router = Router::new()
        .hoop(affix_state::inject(pool))
        .get(list_users);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

### Query Handlers (with spawn_blocking)

```rust
use salvo::prelude::*;
use diesel::prelude::*;

#[handler]
async fn list_users(depot: &mut Depot) -> Result<Json<Vec<User>>, StatusError> {
    let pool = depot.obtain::<DbPool>()
        .ok_or_else(|| StatusError::internal_server_error())?
        .clone();

    let users = tokio::task::spawn_blocking(move || {
        let mut conn = pool.get().map_err(|_| ())?;
        use crate::schema::users::dsl::*;
        users.load::<User>(&mut conn).map_err(|_| ())
    })
    .await
    .map_err(|_| StatusError::internal_server_error())?
    .map_err(|_| StatusError::internal_server_error())?;

    Ok(Json(users))
}
```

## Transactions

```rust
#[handler]
async fn transfer_funds(body: JsonBody<Transfer>, depot: &mut Depot) -> Result<StatusCode, StatusError> {
    let pool = depot.obtain::<PgPool>()
        .ok_or_else(|| StatusError::internal_server_error())?;
    let transfer = body.into_inner();

    let mut tx = pool.begin().await
        .map_err(|_| StatusError::internal_server_error())?;

    sqlx::query("UPDATE accounts SET balance = balance - $1 WHERE id = $2")
        .bind(transfer.amount)
        .bind(transfer.from_account)
        .execute(&mut *tx)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    sqlx::query("UPDATE accounts SET balance = balance + $1 WHERE id = $2")
        .bind(transfer.amount)
        .bind(transfer.to_account)
        .execute(&mut *tx)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    tx.commit().await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(StatusCode::OK)
}
```

## Complete Example

```rust
use salvo::prelude::*;
use sqlx::{FromRow, PgPool};
use serde::{Deserialize, Serialize};

#[derive(FromRow, Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[handler]
async fn list_users(depot: &mut Depot) -> Result<Json<Vec<User>>, StatusError> {
    let pool = depot.obtain::<PgPool>()
        .ok_or_else(|| StatusError::internal_server_error())?;

    let users = sqlx::query_as::<_, User>("SELECT id, name, email FROM users")
        .fetch_all(pool)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(Json(users))
}

#[handler]
async fn create_user(body: JsonBody<CreateUser>, depot: &mut Depot) -> Result<StatusCode, StatusError> {
    let pool = depot.obtain::<PgPool>()
        .ok_or_else(|| StatusError::internal_server_error())?;
    let user = body.into_inner();

    sqlx::query("INSERT INTO users (name, email) VALUES ($1, $2)")
        .bind(&user.name)
        .bind(&user.email)
        .execute(pool)
        .await
        .map_err(|_| StatusError::internal_server_error())?;

    Ok(StatusCode::CREATED)
}

#[tokio::main]
async fn main() {
    let pool = PgPool::connect("postgres://user:pass@localhost/db")
        .await
        .expect("Failed to connect");

    let router = Router::new()
        .hoop(affix_state::inject(pool))
        .push(
            Router::with_path("users")
                .get(list_users)
                .post(create_user)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. Use `affix_state::inject()` for dependency injection
2. Use `depot.obtain::<T>()` to retrieve injected state
3. Use `spawn_blocking` for sync database operations (Diesel)
4. Handle database errors gracefully with proper error conversion
5. Use transactions for multi-step operations
6. Validate input before database operations
7. Use prepared statements to prevent SQL injection
8. Consider using migrations for schema management
9. Use connection pooling for performance
10. Keep database operations in dedicated handler functions
