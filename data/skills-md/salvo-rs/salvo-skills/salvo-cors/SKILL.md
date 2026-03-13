---
name: salvo-cors
description: Configure Cross-Origin Resource Sharing (CORS) and security headers. Use for APIs accessed from browsers on different domains.
---

# Salvo CORS Configuration

This skill helps configure CORS and security headers in Salvo applications.

## Understanding CORS

CORS (Cross-Origin Resource Sharing) is a browser security feature that restricts web pages from making requests to different domains. Without proper CORS configuration, browsers will block cross-origin requests to your API.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["cors"] }
```

## Basic CORS Configuration

```rust
use salvo::cors::Cors;
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    let cors = Cors::new()
        .allow_origin("https://example.com")
        .allow_methods(vec!["GET", "POST", "PUT", "DELETE"])
        .allow_headers(vec!["Content-Type", "Authorization"])
        .into_handler();

    let router = Router::new()
        .hoop(cors)
        .push(Router::with_path("api").get(api_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}

#[handler]
async fn api_handler() -> &'static str {
    "Hello from API"
}
```

## Allow All Origins (Development)

```rust
use salvo::cors::Cors;

// WARNING: Only use in development
let cors = Cors::new()
    .allow_origin("*")
    .allow_methods(vec!["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    .allow_headers(vec!["*"])
    .into_handler();
```

## Production CORS Configuration

```rust
use salvo::cors::Cors;
use salvo::http::Method;

let cors = Cors::new()
    // Specific allowed origins
    .allow_origin(["https://app.example.com", "https://admin.example.com"])
    // Allowed HTTP methods
    .allow_methods(vec![Method::GET, Method::POST, Method::PUT, Method::DELETE])
    // Allowed request headers
    .allow_headers(vec!["Authorization", "Content-Type", "X-Requested-With"])
    // Allow credentials (cookies, auth headers)
    .allow_credentials(true)
    // Cache preflight requests for 1 hour
    .max_age(3600)
    .into_handler();
```

## Permissive CORS

Use the built-in permissive preset for quick setup:

```rust
use salvo::cors::Cors;

let cors = Cors::permissive();

let router = Router::new()
    .hoop(cors)
    .get(handler);
```

## CORS with Specific Routes

Apply CORS only to API routes:

```rust
let cors = Cors::new()
    .allow_origin("https://app.example.com")
    .allow_methods(vec!["GET", "POST"])
    .into_handler();

let router = Router::new()
    .push(
        Router::with_path("api")
            .hoop(cors)  // CORS only for /api routes
            .push(Router::with_path("users").get(list_users))
            .push(Router::with_path("posts").get(list_posts))
    )
    .push(
        Router::with_path("health")
            .get(health_check)  // No CORS needed
    );
```

## Security Headers Middleware

Add security headers to protect against common attacks:

```rust
use salvo::prelude::*;

#[handler]
async fn security_headers(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    // Content Security Policy - prevent XSS
    res.headers_mut().insert(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'".parse().unwrap()
    );

    // HTTP Strict Transport Security - force HTTPS
    res.headers_mut().insert(
        "Strict-Transport-Security",
        "max-age=31536000; includeSubDomains; preload".parse().unwrap()
    );

    // Prevent clickjacking
    res.headers_mut().insert(
        "X-Frame-Options",
        "DENY".parse().unwrap()
    );

    // Prevent MIME type sniffing
    res.headers_mut().insert(
        "X-Content-Type-Options",
        "nosniff".parse().unwrap()
    );

    // XSS Protection
    res.headers_mut().insert(
        "X-XSS-Protection",
        "1; mode=block".parse().unwrap()
    );

    // Referrer Policy
    res.headers_mut().insert(
        "Referrer-Policy",
        "strict-origin-when-cross-origin".parse().unwrap()
    );

    ctrl.call_next(req, depot, res).await;
}
```

## Complete Example with CORS and Security Headers

```rust
use salvo::cors::Cors;
use salvo::http::Method;
use salvo::prelude::*;

#[handler]
async fn security_headers(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    res.headers_mut().insert("X-Content-Type-Options", "nosniff".parse().unwrap());
    res.headers_mut().insert("X-Frame-Options", "DENY".parse().unwrap());
    res.headers_mut().insert("X-XSS-Protection", "1; mode=block".parse().unwrap());
    ctrl.call_next(req, depot, res).await;
}

#[handler]
async fn api_handler() -> Json<serde_json::Value> {
    Json(serde_json::json!({"status": "ok"}))
}

#[tokio::main]
async fn main() {
    // CORS configuration
    let cors = Cors::new()
        .allow_origin(["https://app.example.com"])
        .allow_methods(vec![Method::GET, Method::POST, Method::PUT, Method::DELETE])
        .allow_headers(vec!["Authorization", "Content-Type"])
        .allow_credentials(true)
        .max_age(86400)
        .into_handler();

    let router = Router::new()
        .hoop(security_headers)  // Apply security headers globally
        .hoop(cors)               // Apply CORS globally
        .push(Router::with_path("api").get(api_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Dynamic CORS Origins

Allow origins based on request:

```rust
use salvo::cors::Cors;
use salvo::prelude::*;

fn create_cors() -> Cors {
    Cors::new()
        .allow_origin(|origin: &str, _req: &Request| {
            // Allow any subdomain of example.com
            origin.ends_with(".example.com") || origin == "https://example.com"
        })
        .allow_methods(vec!["GET", "POST"])
        .allow_credentials(true)
}
```

## CORS Configuration Options

| Option | Description |
|--------|-------------|
| `allow_origin()` | Origins allowed to make requests |
| `allow_methods()` | HTTP methods allowed |
| `allow_headers()` | Request headers allowed |
| `expose_headers()` | Response headers exposed to browser |
| `allow_credentials()` | Allow cookies and auth headers |
| `max_age()` | Cache preflight response (seconds) |

## Troubleshooting CORS Issues

### Common Problems

1. **Missing OPTIONS handler**: CORS preflight uses OPTIONS method
2. **Credentials with wildcard origin**: Cannot use `*` with `allow_credentials(true)`
3. **Missing headers**: Ensure all required headers are in `allow_headers()`

### Debug CORS

```rust
#[handler]
async fn cors_debug(req: &Request) {
    println!("Origin: {:?}", req.header::<String>("Origin"));
    println!("Method: {}", req.method());
    println!("Headers: {:?}", req.headers());
}
```

## Best Practices

1. **Specify exact origins in production**: Avoid `*` for security
2. **Limit allowed methods**: Only enable methods your API uses
3. **Validate headers**: Only allow headers you need
4. **Use HTTPS**: Always use HTTPS in production
5. **Set appropriate max_age**: Balance security and performance
6. **Apply security headers**: Add CSP, HSTS, X-Frame-Options
7. **Test preflight requests**: Verify OPTIONS requests work correctly
