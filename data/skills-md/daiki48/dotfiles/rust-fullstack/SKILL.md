---
name: rust-fullstack
description: Rust full-stack patterns. Leptos + Axum + PostgreSQL web apps, auth, multi-tenant, API design.
---

# Rust Full-Stack Web Development Patterns

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Leptos (Rust→WASM CSR), Tailwind CSS + DaisyUI |
| Backend | Axum, SQLx (compile-time checked queries) |
| Database | PostgreSQL |
| Build | Trunk (WASM), Docker, Makefile |

## JWT Dual-Token Auth

```
Access Token (short-lived)  → API request auth
Refresh Token (long-lived)  → Access token renewal
```

- Store in HTTP-only Cookie (XSS protection)
- Backend: Token validation
- Frontend: Auto-retry on 401

```rust
// Backend: Cookie setup
let cookie = format!(
    "access_token={}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age={}",
    token, 900  // 15 min
);

// Frontend: 401 retry
if response.status() == 401 {
    refresh_token().await?;
    // Retry original request
}
```

## Frontend State Management

```rust
provide_context(AuthContext::new());
provide_context(AppCache::new());  // TTL-based cache
provide_context(ToastContext::new());

// localStorage for preferences
let stored = window().local_storage()?.get_item("preferences")?;
```

## API Client Pattern

```rust
// Rate limiting (429) handling
async fn fetch_with_retry<T>(request: impl Fn() -> Future<T>) -> Result<T> {
    loop {
        match request().await {
            Err(e) if e.status() == 429 => {
                let delay = e.retry_after().unwrap_or(1000);
                sleep(delay).await;
            }
            result => return result,
        }
    }
}

// Token refresh queue (prevent multiple refreshes)
static REFRESH_LOCK: OnceCell<RwLock<()>> = OnceCell::new();
```

## Multi-tenant Routing

```
{tenant}.example.com → Tenant identification
```

```rust
fn extract_subdomain(host: &str) -> Option<String> {
    let parts: Vec<&str> = host.split('.').collect();
    (parts.len() >= 3).then(|| parts[0].to_string())
}

async fn check_tenant_access(claims: &Claims, subdomain: &str) -> Result<(), AppError> {
    // Verify user has access to this tenant
}
```

## Database

```rust
// SQLx compile-time query checking
let user = sqlx::query_as!(
    User,
    r#"SELECT id, name, role as "role: UserRole" FROM users WHERE id = $1"#,
    id
).fetch_one(&pool).await?;

// PostgreSQL ENUMs
#[derive(sqlx::Type)]
#[sqlx(type_name = "user_role", rename_all = "PascalCase")]
pub enum UserRole { Admin, AreaManager, ServiceStation }
```

## Common Commands

```sh
make dev          # Start local environment
make fmt          # Format (cargo fmt + leptosfmt)
make lint         # Clippy checks
make test         # Run tests
make migrate-run  # Apply migrations
```

## Dev Notes

| Item | Value |
|------|-------|
| Backend port | 3000 |
| Local subdomain | `lvh.me` (resolves to 127.0.0.1) |
| Env files | `.env.development`, `.env.staging`, `.env.production` |
| Required env | `DATABASE_URL`, `JWT_SECRET`, `APP_ENV` |

## Related Skills

- `leptos-guide` - Leptos frontend
- `axum-guide` - Axum backend
- `sqlx-postgres` - SQLx + PostgreSQL
