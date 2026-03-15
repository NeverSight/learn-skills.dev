---
name: salvo-rate-limiter
description: Implement rate limiting to protect APIs from abuse. Use for preventing DDoS attacks and ensuring fair resource usage.
---

# Salvo Rate Limiting

This skill helps implement rate limiting in Salvo applications to protect against abuse.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["rate-limiter"] }
```

## Basic Rate Limiting

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

#[handler]
async fn api_handler() -> &'static str {
    "API response"
}

#[tokio::main]
async fn main() {
    // 10 requests per second per IP
    let limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_second(10),
    );

    let router = Router::new()
        .hoop(limiter)
        .push(Router::with_path("api").get(api_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Quota Types

```rust
use salvo::rate_limiter::BasicQuota;

// Per second
BasicQuota::per_second(10)   // 10 requests/second

// Per minute
BasicQuota::per_minute(100)  // 100 requests/minute

// Per hour
BasicQuota::per_hour(1000)   // 1000 requests/hour

// Custom duration
use std::time::Duration;
BasicQuota::new(50, Duration::from_secs(30))  // 50 requests per 30 seconds
```

## Rate Limit by IP Address

```rust
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

let limiter = RateLimiter::new(
    FixedGuard::new(),
    MokaStore::new(),
    RemoteIpIssuer,  // Limit by client IP
    BasicQuota::per_minute(60),
);
```

## Rate Limit by User ID

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, QuotaGetter, RateIssuer};

struct UserIdIssuer;

impl RateIssuer for UserIdIssuer {
    type Key = String;

    async fn issue(&self, req: &mut Request, depot: &Depot) -> Option<Self::Key> {
        // Get user ID from depot (set by auth middleware)
        depot.get::<String>("user_id").cloned()
    }
}

let limiter = RateLimiter::new(
    FixedGuard::new(),
    MokaStore::new(),
    UserIdIssuer,
    BasicQuota::per_minute(100),
);
```

## Rate Limit by API Key

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RateIssuer};

struct ApiKeyIssuer;

impl RateIssuer for ApiKeyIssuer {
    type Key = String;

    async fn issue(&self, req: &mut Request, _depot: &Depot) -> Option<Self::Key> {
        req.header::<String>("X-API-Key")
    }
}

let limiter = RateLimiter::new(
    FixedGuard::new(),
    MokaStore::new(),
    ApiKeyIssuer,
    BasicQuota::per_minute(1000),
);
```

## Dynamic Rate Limits

Different limits for different users:

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{FixedGuard, MokaStore, RateLimiter, RateIssuer, QuotaGetter, BasicQuota};

struct UserIdIssuer;

impl RateIssuer for UserIdIssuer {
    type Key = String;

    async fn issue(&self, req: &mut Request, depot: &Depot) -> Option<Self::Key> {
        depot.get::<String>("user_id").cloned()
    }
}

struct TieredQuota;

impl QuotaGetter<String> for TieredQuota {
    type Quota = BasicQuota;
    type Error = salvo::Error;

    async fn get(&self, key: &String, depot: &Depot) -> Result<Self::Quota, Self::Error> {
        let user_tier = depot.get::<String>("user_tier")
            .map(|s| s.as_str())
            .unwrap_or("free");

        let quota = match user_tier {
            "premium" => BasicQuota::per_minute(1000),
            "basic" => BasicQuota::per_minute(100),
            _ => BasicQuota::per_minute(10),  // Free tier
        };

        Ok(quota)
    }
}

let limiter = RateLimiter::new(
    FixedGuard::new(),
    MokaStore::new(),
    UserIdIssuer,
    TieredQuota,
);
```

## Sliding Window Rate Limiting

```rust
use salvo::rate_limiter::{BasicQuota, SlidingGuard, MokaStore, RateLimiter, RemoteIpIssuer};

// Sliding window for smoother rate limiting
let limiter = RateLimiter::new(
    SlidingGuard::new(),  // Use sliding window instead of fixed
    MokaStore::new(),
    RemoteIpIssuer,
    BasicQuota::per_minute(60),
);
```

## Custom Rate Limit Response

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

#[handler]
async fn rate_limit_exceeded(res: &mut Response) {
    res.status_code(StatusCode::TOO_MANY_REQUESTS);
    res.render(Json(serde_json::json!({
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please try again later.",
        "retry_after": 60
    })));
}

// In your router setup, handle 429 status
```

## Rate Limiting Specific Routes

```rust
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    // Strict limit for login
    let login_limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_minute(5),
    );

    // Relaxed limit for general API
    let api_limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_minute(100),
    );

    let router = Router::new()
        .push(
            Router::with_path("login")
                .hoop(login_limiter)
                .post(login_handler)
        )
        .push(
            Router::with_path("api")
                .hoop(api_limiter)
                .get(api_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Combining with Authentication

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RateIssuer};

// Rate limit authenticated users by user ID, anonymous by IP
struct SmartIssuer;

impl RateIssuer for SmartIssuer {
    type Key = String;

    async fn issue(&self, req: &mut Request, depot: &Depot) -> Option<Self::Key> {
        // Try user ID first (from auth middleware)
        if let Some(user_id) = depot.get::<String>("user_id") {
            return Some(format!("user:{}", user_id));
        }

        // Fall back to IP address
        req.remote_addr()
            .map(|addr| format!("ip:{}", addr))
    }
}
```

## Rate Limit Headers

Add headers to inform clients of their rate limit status:

```rust
use salvo::prelude::*;

#[handler]
async fn add_rate_limit_headers(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl
) {
    ctrl.call_next(req, depot, res).await;

    // Add rate limit headers
    res.headers_mut().insert("X-RateLimit-Limit", "100".parse().unwrap());
    res.headers_mut().insert("X-RateLimit-Remaining", "95".parse().unwrap());
    res.headers_mut().insert("X-RateLimit-Reset", "1609459200".parse().unwrap());
}
```

## Complete Example

```rust
use salvo::prelude::*;
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

#[handler]
async fn public_api() -> &'static str {
    "Public API response"
}

#[handler]
async fn login() -> &'static str {
    "Login successful"
}

#[tokio::main]
async fn main() {
    // General API: 100 requests/minute
    let api_limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_minute(100),
    );

    // Login: 5 attempts/minute (prevent brute force)
    let login_limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_minute(5),
    );

    let router = Router::new()
        .push(
            Router::with_path("api")
                .hoop(api_limiter)
                .get(public_api)
        )
        .push(
            Router::with_path("login")
                .hoop(login_limiter)
                .post(login)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. **Choose appropriate limits**: Base on expected usage patterns
2. **Use different limits for different endpoints**: Stricter for auth, relaxed for reads
3. **Identify users correctly**: IP for anonymous, user ID for authenticated
4. **Inform clients**: Return rate limit headers and retry-after
5. **Log rate limit hits**: Monitor for abuse patterns
6. **Consider sliding window**: Smoother rate limiting than fixed window
7. **Handle gracefully**: Return helpful error messages
8. **Test under load**: Verify limits work correctly
