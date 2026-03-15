---
name: salvo-error-handling
description: Handle errors gracefully with custom error types, status codes, and error pages. Use for building robust APIs with proper error responses.
---

# Salvo Error Handling

This skill helps implement proper error handling in Salvo applications.

## Error Handling Overview

In Salvo, error handling covers three categories:

1. **Business Errors**: Invalid parameters, resource not found, permission denied - return clear HTTP status codes
2. **System Errors**: Database failures, timeouts, serialization errors - log and return 5xx responses
3. **Panics**: Unrecoverable errors - catch and convert to controlled responses

## Using StatusError

The simplest way to return errors:

```rust
use salvo::prelude::*;

#[handler]
async fn get_user(req: &mut Request) -> Result<Json<User>, StatusError> {
    let id = req.param::<i64>("id")
        .ok_or_else(|| StatusError::bad_request().brief("Missing user ID"))?;

    let user = find_user(id).await
        .ok_or_else(|| StatusError::not_found().brief("User not found"))?;

    Ok(Json(user))
}
```

### Common StatusError Methods

```rust
// Client errors (4xx)
StatusError::bad_request()           // 400
StatusError::unauthorized()          // 401
StatusError::forbidden()             // 403
StatusError::not_found()             // 404
StatusError::method_not_allowed()    // 405
StatusError::conflict()              // 409
StatusError::unprocessable_entity()  // 422

// Server errors (5xx)
StatusError::internal_server_error() // 500
StatusError::not_implemented()       // 501
StatusError::bad_gateway()           // 502
StatusError::service_unavailable()   // 503

// Add details
StatusError::bad_request()
    .brief("Invalid input")
    .cause("Field 'email' is required")
```

## Using anyhow/eyre

Enable features for popular error handling crates:

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["anyhow", "eyre"] }
anyhow = "1"
eyre = "0.6"
```

### With anyhow

```rust
use salvo::prelude::*;
use anyhow::Context;

#[handler]
async fn process_data() -> Result<String, anyhow::Error> {
    let data = fetch_data().await
        .context("Failed to fetch data")?;

    let result = process(data)
        .context("Failed to process data")?;

    Ok(result)
}
```

### With eyre

```rust
use salvo::prelude::*;
use eyre::WrapErr;

#[handler]
async fn process_data() -> eyre::Result<String> {
    let data = fetch_data().await
        .wrap_err("Failed to fetch data")?;

    Ok(data)
}
```

## Custom Error Types with Writer

Define custom errors that implement `Writer` for full control:

```rust
use salvo::prelude::*;
use serde::Serialize;

#[derive(Debug)]
enum AppError {
    NotFound(String),
    ValidationError(String),
    DatabaseError(String),
    Unauthorized,
}

#[async_trait]
impl Writer for AppError {
    async fn write(self, _req: &mut Request, _depot: &mut Depot, res: &mut Response) {
        let (status, message) = match &self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::ValidationError(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::DatabaseError(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg.clone()),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".to_string()),
        };

        res.status_code(status);
        res.render(Json(serde_json::json!({
            "error": message,
            "code": status.as_u16()
        })));
    }
}

#[handler]
async fn get_user(req: &mut Request) -> Result<Json<User>, AppError> {
    let id = req.param::<i64>("id")
        .ok_or_else(|| AppError::ValidationError("Missing user ID".to_string()))?;

    let user = find_user(id).await
        .map_err(|e| AppError::DatabaseError(e.to_string()))?
        .ok_or_else(|| AppError::NotFound(format!("User {} not found", id)))?;

    Ok(Json(user))
}
```

## Using thiserror

Use thiserror for ergonomic error definitions:

```rust
use salvo::prelude::*;
use thiserror::Error;

#[derive(Error, Debug)]
enum ApiError {
    #[error("Resource not found: {0}")]
    NotFound(String),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Unauthorized")]
    Unauthorized,
}

#[async_trait]
impl Writer for ApiError {
    async fn write(self, _req: &mut Request, _depot: &mut Depot, res: &mut Response) {
        let status = match &self {
            ApiError::NotFound(_) => StatusCode::NOT_FOUND,
            ApiError::Validation(_) => StatusCode::BAD_REQUEST,
            ApiError::Database(_) => StatusCode::INTERNAL_SERVER_ERROR,
            ApiError::Unauthorized => StatusCode::UNAUTHORIZED,
        };

        res.status_code(status);
        res.render(Json(serde_json::json!({
            "error": self.to_string()
        })));
    }
}
```

## Catching Panics

Use `CatchPanic` middleware to handle panics gracefully:

```rust
use salvo::prelude::*;
use salvo::catcher::CatchPanic;

#[handler]
async fn may_panic() -> &'static str {
    panic!("Something went wrong!");
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .hoop(CatchPanic::new())  // Catch panics globally
        .get(may_panic);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Custom Error Pages with Catcher

Create custom error pages for specific status codes:

```rust
use salvo::prelude::*;
use salvo::catcher::Catcher;

#[handler]
async fn handle_404(res: &mut Response, ctrl: &mut FlowCtrl) {
    if res.status_code() == Some(StatusCode::NOT_FOUND) {
        res.render("Custom 404 - Page Not Found");
        ctrl.skip_rest();
    }
}

#[handler]
async fn handle_500(res: &mut Response, ctrl: &mut FlowCtrl) {
    if res.status_code().map_or(false, |c| c.is_server_error()) {
        res.render("Custom 500 - Internal Server Error");
        ctrl.skip_rest();
    }
}

fn create_service(router: Router) -> Service {
    Service::new(router).catcher(
        Catcher::default()
            .hoop(handle_404)
            .hoop(handle_500)
    )
}

#[tokio::main]
async fn main() {
    let router = Router::new().get(hello);
    let service = create_service(router);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(service).await;
}
```

## JSON Error Responses for APIs

```rust
use salvo::prelude::*;
use serde::Serialize;

#[derive(Serialize)]
struct ErrorResponse {
    code: u16,
    error: String,
    message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    details: Option<Vec<String>>,
}

impl ErrorResponse {
    fn new(status: StatusCode, error: &str, message: &str) -> Self {
        Self {
            code: status.as_u16(),
            error: error.to_string(),
            message: message.to_string(),
            details: None,
        }
    }

    fn with_details(mut self, details: Vec<String>) -> Self {
        self.details = Some(details);
        self
    }
}

#[handler]
async fn api_handler() -> Result<Json<Data>, (StatusCode, Json<ErrorResponse>)> {
    let data = fetch_data().await.map_err(|e| {
        let error = ErrorResponse::new(
            StatusCode::INTERNAL_SERVER_ERROR,
            "DATABASE_ERROR",
            &e.to_string(),
        );
        (StatusCode::INTERNAL_SERVER_ERROR, Json(error))
    })?;

    Ok(Json(data))
}
```

## Error Logging

Log errors with context for debugging:

```rust
use salvo::prelude::*;
use tracing::{error, warn};

#[handler]
async fn handler(req: &mut Request) -> Result<String, StatusError> {
    let result = process_request(req).await;

    match result {
        Ok(data) => Ok(data),
        Err(e) => {
            // Log the error with context
            error!(
                error = %e,
                path = %req.uri().path(),
                method = %req.method(),
                "Request processing failed"
            );

            Err(StatusError::internal_server_error()
                .brief("An error occurred processing your request"))
        }
    }
}
```

## Best Practices

1. **Distinguish 4xx from 5xx**: 4xx = client error, 5xx = server error
2. **Don't expose internal errors**: Return generic messages to users, log details
3. **Use structured error responses**: Consistent JSON format for APIs
4. **Log with context**: Include request ID, path, and relevant parameters
5. **Treat panics as bugs**: Use `CatchPanic` as safety net, not normal flow
6. **Define domain errors**: Map business logic errors to appropriate HTTP codes
7. **Validate at boundaries**: Catch bad input early with clear error messages
8. **Use error chains**: anyhow/eyre for context, thiserror for type safety
