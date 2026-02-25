---
name: axum-guide
description: Axum v0.8.x backend development guide. Handlers, routing, middleware, auth, error handling.
---

# Axum v0.8.x Development Guide

## Handlers

```rust
use axum::{extract::{Path, Query, State, Json}, response::IntoResponse, http::StatusCode};

async fn get_user(
    State(pool): State<PgPool>,
    Path(id): Path<i32>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(&pool).await?;
    Ok(Json(user))
}

async fn create_user(
    State(pool): State<PgPool>,
    claims: Claims,  // Custom extractor
    Json(payload): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<User>), AppError> {
    // ...
    Ok((StatusCode::CREATED, Json(user)))
}
```

## Routing

```rust
fn app() -> Router<AppState> {
    Router::new()
        .route("/", get(root))
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).put(update_user).delete(delete_user))
        .nest("/api", api_routes())
        .layer(middleware_stack())
        .with_state(state)
}
```

## Error Handling

```rust
pub struct AppError {
    pub code: StatusCode,
    pub message: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        (self.code, Json(json!({"error": self.message}))).into_response()
    }
}

impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        match err {
            sqlx::Error::RowNotFound => AppError {
                code: StatusCode::NOT_FOUND,
                message: "Resource not found".into(),
            },
            _ => AppError {
                code: StatusCode::INTERNAL_SERVER_ERROR,
                message: "Database error".into(),
            },
        }
    }
}
```

## Middleware

```rust
async fn logging_middleware(req: Request, next: Next) -> Response {
    let method = req.method().clone();
    let uri = req.uri().clone();
    let response = next.run(req).await;
    tracing::info!("{} {} -> {}", method, uri, response.status());
    response
}

let app = Router::new()
    .route("/", get(handler))
    .layer(middleware::from_fn(logging_middleware));
```

## Custom Extractor

```rust
pub struct Claims { pub user_id: i32, pub role: String }

#[async_trait]
impl<S: Send + Sync> FromRequestParts<S> for Claims {
    type Rejection = AppError;

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let token = parts.headers.get("cookie")
            .and_then(|v| v.to_str().ok())
            .and_then(extract_token)
            .ok_or(AppError::unauthorized("No token"))?;
        validate_jwt(&token)
    }
}
```

## Auth Middleware

```rust
async fn auth_middleware(claims: Claims, req: Request, next: Next) -> Response {
    next.run(req).await
}

let protected = Router::new()
    .route("/profile", get(profile))
    .layer(middleware::from_fn(auth_middleware));
```

## CORS

```rust
use tower_http::cors::{CorsLayer, Any};

let cors = CorsLayer::new()
    .allow_origin(Any)
    .allow_methods(Any)
    .allow_headers(Any)
    .allow_credentials(true);
```

## Response Headers & Cookies

```rust
async fn login() -> impl IntoResponse {
    let cookie = format!(
        "token={}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age={}",
        token, max_age
    );
    ([(header::SET_COOKIE, cookie)], Json(response))
}
```

## File Upload

```rust
async fn upload(mut multipart: Multipart) -> Result<(), AppError> {
    while let Some(field) = multipart.next_field().await? {
        let name = field.name().unwrap_or_default().to_string();
        let data = field.bytes().await?;
        // Process file
    }
    Ok(())
}
```

## Notes

1. **Extractor order**: Put `State` last (others may consume body)
2. **Consistent error type**: Use single AppError across app
3. **Middleware order**: Executes outer→inner (reverse of layer order)
4. **State type**: Must implement `Clone` (usually wrap in `Arc`)
