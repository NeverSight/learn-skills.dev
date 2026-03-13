---
name: salvo-concurrency-limiter
description: Limit concurrent requests to protect resources. Use for file uploads, expensive operations, and preventing resource exhaustion.
---

# Salvo Concurrency Limiter

This skill helps limit concurrent requests in Salvo applications to protect resources and prevent overload.

## What is Concurrency Limiting?

Concurrency limiting restricts how many requests can be processed simultaneously for specific endpoints. Unlike rate limiting (requests per time), this limits parallel execution.

Use cases:
- File upload endpoints (limited disk I/O)
- CPU-intensive operations
- External API calls with connection limits
- Database connections management

## Setup

Concurrency limiter is built into Salvo core:

```toml
[dependencies]
salvo = "0.89.0"
```

## Basic Concurrency Limit

```rust
use salvo::prelude::*;

#[handler]
async fn upload(req: &mut Request, res: &mut Response) {
    // Simulate long-running upload
    tokio::time::sleep(tokio::time::Duration::from_secs(10)).await;

    res.render("Upload complete");
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(
            Router::with_path("upload")
                .hoop(max_concurrency(1))  // Only 1 concurrent upload
                .post(upload)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Different Limits for Different Routes

```rust
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    let router = Router::new()
        // File uploads - limited concurrency
        .push(
            Router::with_path("upload")
                .hoop(max_concurrency(2))  // Max 2 concurrent uploads
                .post(upload_handler)
        )
        // Report generation - very limited
        .push(
            Router::with_path("reports/generate")
                .hoop(max_concurrency(1))  // Only 1 at a time
                .post(generate_report)
        )
        // API endpoints - higher concurrency
        .push(
            Router::with_path("api/{**rest}")
                .hoop(max_concurrency(100))  // Up to 100 concurrent
                .goal(api_handler)
        )
        // No limit for health checks
        .push(Router::with_path("health").get(health_check));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Comparing Limited and Unlimited Endpoints

```rust
use std::path::Path;
use salvo::prelude::*;

#[handler]
async fn index(res: &mut Response) {
    res.render(Text::Html(r#"
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Upload Test</h1>
            <h3>Unlimited Uploads (can run in parallel)</h3>
            <form action="/unlimit" method="post" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" value="Upload" />
            </form>
            <h3>Limited Uploads (max 1 concurrent)</h3>
            <form action="/limited" method="post" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" value="Upload" />
            </form>
        </body>
        </html>
    "#));
}

#[handler]
async fn upload(req: &mut Request, res: &mut Response) {
    // Simulate slow processing
    tokio::time::sleep(tokio::time::Duration::from_secs(10)).await;

    if let Some(file) = req.file("file").await {
        let dest = format!("temp/{}", file.name().unwrap_or("file"));
        if let Err(e) = std::fs::copy(file.path(), Path::new(&dest)) {
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            res.render(format!("Error: {e}"));
        } else {
            res.render(format!("File uploaded to {dest}"));
        }
    } else {
        res.status_code(StatusCode::BAD_REQUEST);
        res.render("No file in request");
    }
}

#[tokio::main]
async fn main() {
    std::fs::create_dir_all("temp").unwrap();

    let router = Router::new()
        .get(index)
        // Limited: Only 1 concurrent request
        .push(
            Router::with_path("limited")
                .hoop(max_concurrency(1))
                .post(upload)
        )
        // Unlimited: All requests processed in parallel
        .push(
            Router::with_path("unlimit")
                .post(upload)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Combining with Rate Limiting

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

#[tokio::main]
async fn main() {
    // Rate limiter: 10 requests per second per IP
    let rate_limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_second(10),
    );

    let router = Router::new()
        .push(
            Router::with_path("api/{**rest}")
                .hoop(rate_limiter)        // Rate limit first
                .hoop(max_concurrency(50)) // Then concurrency limit
                .goal(api_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Combining with Timeout

```rust
use std::time::Duration;
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(
            Router::with_path("process")
                .hoop(Timeout::new(Duration::from_secs(30)))  // Timeout
                .hoop(max_concurrency(5))                      // Concurrency
                .post(process_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Use Cases

### CPU-Intensive Operations

```rust
// Limit image processing to prevent CPU exhaustion
let router = Router::new()
    .push(
        Router::with_path("resize")
            .hoop(max_concurrency(num_cpus::get()))  // One per CPU core
            .post(resize_image)
    );
```

### Database Connection Protection

```rust
// Match concurrency to database pool size
let db_pool_size = 10;

let router = Router::new()
    .push(
        Router::with_path("heavy-query")
            .hoop(max_concurrency(db_pool_size))
            .get(heavy_query_handler)
    );
```

### External API Limits

```rust
// External API allows only 5 concurrent connections
let router = Router::new()
    .push(
        Router::with_path("external")
            .hoop(max_concurrency(5))
            .get(call_external_api)
    );
```

### Memory-Intensive Operations

```rust
// Large file processing - limit to prevent OOM
let router = Router::new()
    .push(
        Router::with_path("analyze")
            .hoop(max_concurrency(2))  // Only 2 concurrent analyses
            .post(analyze_large_file)
    );
```

## What Happens When Limit is Reached

When concurrency limit is reached, additional requests receive `503 Service Unavailable`:

```rust
use salvo::prelude::*;
use salvo::catcher::Catcher;

#[handler]
async fn handle_503(res: &mut Response, ctrl: &mut FlowCtrl) {
    if res.status_code() == Some(StatusCode::SERVICE_UNAVAILABLE) {
        res.render(Json(serde_json::json!({
            "error": "Server busy",
            "message": "Too many concurrent requests. Please try again.",
            "retry_after": 5
        })));
        ctrl.skip_rest();
    }
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(
            Router::with_path("process")
                .hoop(max_concurrency(2))
                .post(process_handler)
        );

    let service = Service::new(router).catcher(
        Catcher::default().hoop(handle_503)
    );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(service).await;
}
```

## Complete Example with Monitoring

```rust
use salvo::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

// Track active requests for monitoring
static ACTIVE_UPLOADS: AtomicUsize = AtomicUsize::new(0);
static TOTAL_UPLOADS: AtomicUsize = AtomicUsize::new(0);

#[handler]
async fn upload(req: &mut Request, res: &mut Response) {
    // Track active requests
    ACTIVE_UPLOADS.fetch_add(1, Ordering::Relaxed);
    TOTAL_UPLOADS.fetch_add(1, Ordering::Relaxed);

    // Simulate processing
    tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;

    // Process upload...
    res.render("Upload complete");

    ACTIVE_UPLOADS.fetch_sub(1, Ordering::Relaxed);
}

#[handler]
async fn metrics() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "active_uploads": ACTIVE_UPLOADS.load(Ordering::Relaxed),
        "total_uploads": TOTAL_UPLOADS.load(Ordering::Relaxed),
        "max_concurrent": 3
    }))
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("metrics").get(metrics))
        .push(
            Router::with_path("upload")
                .hoop(max_concurrency(3))
                .post(upload)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Recommended Concurrency Limits

| Operation Type | Recommended Limit |
|----------------|-------------------|
| File uploads | 1-5 |
| Image processing | CPU cores |
| Report generation | 1-2 |
| Database heavy queries | DB pool size |
| External API calls | API limit |
| General API endpoints | 50-200 |
| WebSocket connections | Memory-based |

## Best Practices

1. **Set based on resource constraints**: Match limits to actual resource capacity
2. **Consider downstream limits**: Database pools, external API limits
3. **Combine with timeout**: Prevent stuck requests from blocking slots
4. **Monitor active requests**: Track usage to tune limits
5. **Return meaningful errors**: Tell clients to retry later
6. **Different limits per endpoint**: Not all endpoints need same limits
7. **Test under load**: Verify limits work as expected
8. **Leave headroom**: Don't set limit exactly at resource maximum
