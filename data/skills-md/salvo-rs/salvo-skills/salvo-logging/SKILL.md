---
name: salvo-logging
description: Implement request logging, tracing, and observability. Use for debugging, monitoring, and production observability.
---

# Salvo Logging and Tracing

This skill helps implement logging and tracing in Salvo applications for debugging and observability.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["logging"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

## Basic Request Logging

```rust
use salvo::logging::Logger;
use salvo::prelude::*;

#[handler]
async fn hello() -> &'static str {
    "Hello, World!"
}

#[handler]
async fn error() -> StatusError {
    StatusError::bad_request()
        .brief("Bad request error")
        .detail("The request was malformed.")
}

#[tokio::main]
async fn main() {
    // Initialize tracing subscriber
    tracing_subscriber::fmt().init();

    let router = Router::new()
        .get(hello)
        .push(Router::with_path("error").get(error));

    // Apply Logger to the service
    let service = Service::new(router).hoop(Logger::new());

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(service).await;
}
```

## Custom Log Format

```rust
use salvo::prelude::*;
use tracing::info;
use std::time::Instant;

#[handler]
async fn request_logger(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let start = Instant::now();
    let method = req.method().clone();
    let path = req.uri().path().to_string();
    let remote_addr = req.remote_addr().map(|a| a.to_string());

    // Call next handlers
    ctrl.call_next(req, depot, res).await;

    let duration = start.elapsed();
    let status = res.status_code().unwrap_or(StatusCode::OK);

    info!(
        method = %method,
        path = %path,
        status = %status.as_u16(),
        duration_ms = %duration.as_millis(),
        remote_addr = ?remote_addr,
        "Request completed"
    );
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_target(false)
        .with_level(true)
        .init();

    let router = Router::new()
        .hoop(request_logger)
        .get(hello);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Structured Logging with Tracing

```rust
use salvo::prelude::*;
use tracing::{info, warn, error, debug, instrument, Level};

#[handler]
#[instrument(skip(req, res), fields(user_id))]
async fn get_user(req: &mut Request, res: &mut Response) {
    let user_id: u32 = req.param("id").unwrap_or(0);

    // Record field value
    tracing::Span::current().record("user_id", user_id);

    debug!("Fetching user from database");

    match fetch_user(user_id).await {
        Ok(user) => {
            info!(user_id = %user_id, "User found");
            res.render(Json(user));
        }
        Err(e) => {
            warn!(user_id = %user_id, error = %e, "User not found");
            res.status_code(StatusCode::NOT_FOUND);
        }
    }
}

async fn fetch_user(id: u32) -> Result<User, String> {
    // Database lookup...
    Ok(User { id, name: "Alice".to_string() })
}
```

## Log Levels and Filtering

```rust
use tracing_subscriber::{EnvFilter, layer::SubscriberExt, util::SubscriberInitExt};

fn init_logging() {
    // Configure log levels via environment
    // RUST_LOG=debug,salvo=info,hyper=warn
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| {
            EnvFilter::new("info")
                .add_directive("salvo=debug".parse().unwrap())
                .add_directive("hyper=warn".parse().unwrap())
        });

    tracing_subscriber::registry()
        .with(filter)
        .with(tracing_subscriber::fmt::layer())
        .init();
}

#[tokio::main]
async fn main() {
    init_logging();

    // Application code...
}
```

## JSON Logging for Production

```rust
use tracing_subscriber::{fmt, EnvFilter, layer::SubscriberExt, util::SubscriberInitExt};

fn init_json_logging() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::registry()
        .with(filter)
        .with(
            fmt::layer()
                .json()
                .with_current_span(true)
                .with_span_list(true)
        )
        .init();
}
```

Output example:
```json
{"timestamp":"2024-01-15T10:30:00Z","level":"INFO","target":"myapp","message":"Request completed","method":"GET","path":"/api/users","status":200,"duration_ms":15}
```

## File-Based Logging

```rust
use tracing_subscriber::{fmt, EnvFilter, layer::SubscriberExt, util::SubscriberInitExt};
use tracing_appender::{rolling, non_blocking};

fn init_file_logging() {
    // Create file appender with daily rotation
    let file_appender = rolling::daily("logs", "app.log");
    let (non_blocking_appender, _guard) = non_blocking(file_appender);

    let filter = EnvFilter::new("info");

    tracing_subscriber::registry()
        .with(filter)
        .with(
            fmt::layer()
                .with_writer(non_blocking_appender)
                .with_ansi(false)  // No colors in file
        )
        .with(
            fmt::layer()  // Also log to console
                .with_ansi(true)
        )
        .init();

    // Note: Keep _guard alive for the lifetime of the application
}
```

## Request ID Tracking

```rust
use salvo::prelude::*;
use uuid::Uuid;
use tracing::{info, Span};

#[handler]
async fn add_request_id(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    // Generate or extract request ID
    let request_id = req
        .header::<String>("X-Request-ID")
        .unwrap_or_else(|| Uuid::new_v4().to_string());

    // Store in depot for handlers
    depot.insert("request_id", request_id.clone());

    // Add to response header
    res.headers_mut().insert(
        "X-Request-ID",
        request_id.parse().unwrap(),
    );

    // Create span with request ID
    let span = tracing::info_span!(
        "request",
        request_id = %request_id,
        method = %req.method(),
        path = %req.uri().path()
    );

    let _enter = span.enter();
    ctrl.call_next(req, depot, res).await;
}

#[handler]
async fn my_handler(depot: &mut Depot) -> &'static str {
    let request_id: &String = depot.get("request_id").unwrap();
    info!(request_id = %request_id, "Processing request");
    "Hello"
}
```

## Error Logging

```rust
use salvo::prelude::*;
use tracing::{error, warn};

#[handler]
async fn error_handler(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    ctrl.call_next(req, depot, res).await;

    // Log errors after handler completes
    if let Some(status) = res.status_code() {
        if status.is_server_error() {
            error!(
                status = %status.as_u16(),
                path = %req.uri().path(),
                "Server error occurred"
            );
        } else if status.is_client_error() {
            warn!(
                status = %status.as_u16(),
                path = %req.uri().path(),
                "Client error"
            );
        }
    }
}
```

## Performance Metrics Logging

```rust
use salvo::prelude::*;
use std::time::Instant;
use tracing::info;

#[handler]
async fn metrics_logger(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let start = Instant::now();
    let path = req.uri().path().to_string();
    let method = req.method().to_string();

    ctrl.call_next(req, depot, res).await;

    let duration = start.elapsed();
    let status = res.status_code().unwrap_or(StatusCode::OK);

    // Log metrics
    info!(
        target: "metrics",
        path = %path,
        method = %method,
        status = %status.as_u16(),
        duration_ms = %duration.as_millis(),
        duration_us = %duration.as_micros(),
    );

    // Alert on slow requests
    if duration.as_millis() > 1000 {
        tracing::warn!(
            path = %path,
            duration_ms = %duration.as_millis(),
            "Slow request detected"
        );
    }
}
```

## OpenTelemetry Integration

```toml
[dependencies]
opentelemetry = "0.22"
opentelemetry-otlp = "0.15"
tracing-opentelemetry = "0.23"
```

```rust
use opentelemetry::global;
use opentelemetry_otlp::WithExportConfig;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

fn init_otel() {
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint("http://localhost:4317")
        )
        .install_batch(opentelemetry_sdk::runtime::Tokio)
        .unwrap();

    let otel_layer = tracing_opentelemetry::layer().with_tracer(tracer);

    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(otel_layer)
        .init();
}

#[tokio::main]
async fn main() {
    init_otel();

    // Application code...

    // Shutdown tracer on exit
    global::shutdown_tracer_provider();
}
```

## Complete Production Logging Setup

```rust
use salvo::logging::Logger;
use salvo::prelude::*;
use tracing::{info, Level};
use tracing_subscriber::{
    fmt, EnvFilter,
    layer::SubscriberExt,
    util::SubscriberInitExt,
};
use tracing_appender::rolling;
use std::time::Instant;

#[handler]
async fn request_timing(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let start = Instant::now();
    ctrl.call_next(req, depot, res).await;

    let duration = start.elapsed();
    if duration.as_millis() > 500 {
        tracing::warn!(
            path = %req.uri().path(),
            duration_ms = %duration.as_millis(),
            "Slow request"
        );
    }
}

fn init_logging() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| {
            EnvFilter::new("info")
                .add_directive("salvo=info".parse().unwrap())
        });

    // File logging
    let file_appender = rolling::daily("logs", "app.log");
    let (file_writer, _guard) = tracing_appender::non_blocking(file_appender);

    tracing_subscriber::registry()
        .with(filter)
        // Console logging (human-readable)
        .with(
            fmt::layer()
                .with_target(true)
                .with_level(true)
        )
        // File logging (JSON for parsing)
        .with(
            fmt::layer()
                .json()
                .with_writer(file_writer)
        )
        .init();
}

#[tokio::main]
async fn main() {
    init_logging();

    info!("Starting server...");

    let router = Router::new()
        .hoop(request_timing)
        .get(handler);

    let service = Service::new(router).hoop(Logger::new());

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    info!("Server listening on 0.0.0.0:8080");
    Server::new(acceptor).serve(service).await;
}
```

## Best Practices

1. **Use structured logging**: Key-value pairs are easier to parse and search
2. **Include request context**: Request ID, user ID, path for correlation
3. **Log at appropriate levels**: DEBUG for development, INFO for production
4. **Use JSON in production**: Machine-parseable for log aggregation
5. **Rotate log files**: Prevent disk space exhaustion
6. **Include timing information**: Track request duration for performance monitoring
7. **Don't log sensitive data**: Passwords, tokens, PII should never be logged
8. **Use async/non-blocking**: Don't let logging slow down request handling
