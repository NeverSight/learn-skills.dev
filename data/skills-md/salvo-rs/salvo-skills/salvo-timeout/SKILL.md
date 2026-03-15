---
name: salvo-timeout
description: Configure request timeouts to prevent slow requests from blocking resources. Use for protecting APIs from long-running operations.
---

# Salvo Request Timeout

This skill helps configure request timeouts in Salvo applications to prevent slow requests from consuming server resources indefinitely.

## Why Use Timeouts?

- **Prevent resource exhaustion**: Long-running requests can consume connections and memory
- **Improve reliability**: Fail fast rather than hang indefinitely
- **Better user experience**: Users get quick feedback instead of waiting forever
- **Protection against attacks**: Slowloris and similar attacks are mitigated

## Setup

Timeout is built into Salvo core:

```toml
[dependencies]
salvo = "0.89.0"
```

## Basic Timeout

```rust
use std::time::Duration;
use salvo::prelude::*;

#[handler]
async fn fast_handler() -> &'static str {
    "Hello, World!"
}

#[handler]
async fn slow_handler() -> &'static str {
    // Simulates a slow operation
    tokio::time::sleep(Duration::from_secs(10)).await;
    "This takes a while..."
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().init();

    let router = Router::new()
        // Apply 5-second timeout to all routes
        .hoop(Timeout::new(Duration::from_secs(5)))
        .push(Router::with_path("fast").get(fast_handler))
        .push(Router::with_path("slow").get(slow_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

When accessing `/slow`, the request will timeout after 5 seconds and return a 408 Request Timeout response.

## Route-Specific Timeouts

Apply different timeouts to different routes:

```rust
use std::time::Duration;
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(
            Router::with_path("quick")
                .hoop(Timeout::new(Duration::from_secs(2)))
                .get(quick_handler)
        )
        .push(
            Router::with_path("standard")
                .hoop(Timeout::new(Duration::from_secs(30)))
                .get(standard_handler)
        )
        .push(
            Router::with_path("long-running")
                .hoop(Timeout::new(Duration::from_secs(300)))
                .get(long_running_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Timeout with API Routes

```rust
use std::time::Duration;
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    // Short timeout for API endpoints
    let api_timeout = Timeout::new(Duration::from_secs(10));

    // Longer timeout for file uploads
    let upload_timeout = Timeout::new(Duration::from_secs(120));

    let router = Router::new()
        .push(
            Router::with_path("api")
                .hoop(api_timeout)
                .push(Router::with_path("users").get(list_users))
                .push(Router::with_path("products").get(list_products))
        )
        .push(
            Router::with_path("upload")
                .hoop(upload_timeout)
                .post(handle_upload)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Global Timeout with Exceptions

```rust
use std::time::Duration;
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    // Default 30-second timeout
    let default_timeout = Timeout::new(Duration::from_secs(30));

    let router = Router::new()
        .hoop(default_timeout)  // Apply to all routes
        .push(Router::with_path("health").get(health_check))
        .push(Router::with_path("api/{**rest}").get(api_handler))
        .push(
            // Override with longer timeout for specific route
            Router::with_path("reports/generate")
                .hoop(Timeout::new(Duration::from_secs(300)))
                .post(generate_report)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Timeout with Custom Error Response

Handle timeout errors with a custom catcher:

```rust
use std::time::Duration;
use salvo::prelude::*;
use salvo::catcher::Catcher;

#[handler]
async fn handle_timeout(res: &mut Response, ctrl: &mut FlowCtrl) {
    if res.status_code() == Some(StatusCode::REQUEST_TIMEOUT) {
        res.render(Json(serde_json::json!({
            "error": "Request Timeout",
            "message": "The request took too long to process",
            "code": 408
        })));
        ctrl.skip_rest();
    }
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .hoop(Timeout::new(Duration::from_secs(5)))
        .get(slow_handler);

    let service = Service::new(router).catcher(
        Catcher::default().hoop(handle_timeout)
    );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(service).await;
}
```

## Combining Timeout with Other Middleware

```rust
use std::time::Duration;
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

#[tokio::main]
async fn main() {
    // Rate limiter
    let limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_second(10),
    );

    // Timeout
    let timeout = Timeout::new(Duration::from_secs(30));

    let router = Router::new()
        .hoop(limiter)   // Rate limit first
        .hoop(timeout)   // Then apply timeout
        .push(Router::with_path("api/{**rest}").get(api_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Practical Timeout Values

| Endpoint Type | Recommended Timeout |
|---------------|---------------------|
| Health checks | 1-2 seconds |
| Simple API calls | 5-10 seconds |
| Database queries | 10-30 seconds |
| File uploads | 60-300 seconds |
| Report generation | 120-600 seconds |
| Real-time endpoints | Consider no timeout |

## Example: Microservices Gateway

```rust
use std::time::Duration;
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    let router = Router::new()
        // Auth service - should be fast
        .push(
            Router::with_path("auth/{**rest}")
                .hoop(Timeout::new(Duration::from_secs(5)))
                .goal(auth_proxy)
        )
        // User service - moderate
        .push(
            Router::with_path("users/{**rest}")
                .hoop(Timeout::new(Duration::from_secs(15)))
                .goal(users_proxy)
        )
        // Analytics service - can be slow
        .push(
            Router::with_path("analytics/{**rest}")
                .hoop(Timeout::new(Duration::from_secs(60)))
                .goal(analytics_proxy)
        )
        // Report service - long running
        .push(
            Router::with_path("reports/{**rest}")
                .hoop(Timeout::new(Duration::from_secs(300)))
                .goal(reports_proxy)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. **Set appropriate timeouts**: Match timeout to expected operation duration
2. **Use shorter timeouts for public APIs**: Prevent abuse and resource exhaustion
3. **Longer timeouts for internal services**: Trusted services may need more time
4. **Log timeouts**: Track which requests are timing out for debugging
5. **Consider client expectations**: Some clients may have their own timeouts
6. **Combine with rate limiting**: Protect against slowloris attacks
7. **Graceful degradation**: Return meaningful error messages on timeout
8. **No timeout for WebSocket**: Long-lived connections shouldn't have request timeouts
