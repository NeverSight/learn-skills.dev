---
name: salvo-proxy
description: Implement reverse proxy to forward requests to backend services. Use for load balancing, API gateways, and microservices routing.
---

# Salvo Reverse Proxy

This skill helps implement reverse proxy functionality in Salvo applications.

## What is Reverse Proxy?

A reverse proxy accepts client requests and forwards them to backend servers. Benefits:

- **Load Balancing**: Distribute requests across multiple servers
- **Security**: Hide backend server details
- **Caching**: Cache responses for better performance
- **Path Rewriting**: Flexibly route requests

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["proxy"] }
```

## Basic Proxy

### Using HyperClient (High Performance)

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};

#[tokio::main]
async fn main() {
    // Proxy all requests to backend
    let proxy = Proxy::new(
        vec!["http://localhost:3000"],
        HyperClient::default(),
    );

    let router = Router::new()
        .push(Router::with_path("{**rest}").goal(proxy));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

### Using ReqwestClient (Simple)

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, ReqwestClient};

let proxy = Proxy::new(
    vec!["http://localhost:3000"],
    ReqwestClient::default(),
);
```

## Load Balancing

Distribute requests across multiple backends:

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};

let proxy = Proxy::new(
    vec![
        "http://backend1:3000",
        "http://backend2:3000",
        "http://backend3:3000",
    ],
    HyperClient::default(),
);

let router = Router::new()
    .push(Router::with_path("{**rest}").goal(proxy));
```

## Path-Based Routing

Route different paths to different backends:

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};

#[tokio::main]
async fn main() {
    // API requests to API server
    let api_proxy = Proxy::new(
        vec!["http://api-server:3000"],
        HyperClient::default(),
    );

    // Static files to static server
    let static_proxy = Proxy::new(
        vec!["http://static-server:8080"],
        HyperClient::default(),
    );

    // WebSocket to WS server
    let ws_proxy = Proxy::new(
        vec!["http://ws-server:9000"],
        HyperClient::default(),
    );

    let router = Router::new()
        .push(Router::with_path("api/{**rest}").goal(api_proxy))
        .push(Router::with_path("static/{**rest}").goal(static_proxy))
        .push(Router::with_path("ws/{**rest}").goal(ws_proxy));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## API Gateway Pattern

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};

#[tokio::main]
async fn main() {
    // User service
    let user_proxy = Proxy::new(
        vec!["http://user-service:3001"],
        HyperClient::default(),
    );

    // Order service
    let order_proxy = Proxy::new(
        vec!["http://order-service:3002"],
        HyperClient::default(),
    );

    // Product service
    let product_proxy = Proxy::new(
        vec!["http://product-service:3003"],
        HyperClient::default(),
    );

    let router = Router::new()
        .push(
            Router::with_path("api/v1")
                .hoop(auth_middleware)  // Apply auth to all routes
                .push(Router::with_path("users/{**rest}").goal(user_proxy))
                .push(Router::with_path("orders/{**rest}").goal(order_proxy))
                .push(Router::with_path("products/{**rest}").goal(product_proxy))
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Proxy with Authentication

Add authentication before proxying:

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};

#[handler]
async fn auth_middleware(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    let token = req.header::<String>("Authorization");

    match token {
        Some(t) if validate_token(&t) => {
            ctrl.call_next(req, depot, res).await;
        }
        _ => {
            res.status_code(StatusCode::UNAUTHORIZED);
            res.render("Unauthorized");
            ctrl.skip_rest();
        }
    }
}

#[tokio::main]
async fn main() {
    let proxy = Proxy::new(
        vec!["http://backend:3000"],
        HyperClient::default(),
    );

    let router = Router::new()
        .push(
            Router::with_path("api/{**rest}")
                .hoop(auth_middleware)
                .goal(proxy)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Adding Headers

Add headers before forwarding:

```rust
use salvo::prelude::*;

#[handler]
async fn add_proxy_headers(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    // Add forwarded headers
    if let Some(addr) = req.remote_addr() {
        req.headers_mut().insert("X-Forwarded-For", addr.to_string().parse().unwrap());
    }

    req.headers_mut().insert("X-Forwarded-Proto", "https".parse().unwrap());

    ctrl.call_next(req, depot, res).await;
}
```

## Health Check for Backends

```rust
use salvo::prelude::*;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone)]
struct HealthyBackends {
    backends: Arc<RwLock<Vec<String>>>,
}

impl HealthyBackends {
    async fn get_backends(&self) -> Vec<String> {
        self.backends.read().await.clone()
    }

    async fn update_health(&self, all_backends: &[&str]) {
        let mut healthy = Vec::new();

        for backend in all_backends {
            if check_health(backend).await {
                healthy.push(backend.to_string());
            }
        }

        *self.backends.write().await = healthy;
    }
}

async fn check_health(backend: &str) -> bool {
    // Implement health check logic
    reqwest::get(format!("{}/health", backend))
        .await
        .map(|r| r.status().is_success())
        .unwrap_or(false)
}
```

## WebSocket Proxy

Proxy WebSocket connections:

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};

let ws_proxy = Proxy::new(
    vec!["http://ws-backend:9000"],
    HyperClient::default(),
);

let router = Router::new()
    .push(Router::with_path("ws").goal(ws_proxy));
```

## Rate Limiting at Proxy

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};
use salvo::rate_limiter::{BasicQuota, FixedGuard, MokaStore, RateLimiter, RemoteIpIssuer};

#[tokio::main]
async fn main() {
    let limiter = RateLimiter::new(
        FixedGuard::new(),
        MokaStore::new(),
        RemoteIpIssuer,
        BasicQuota::per_second(100),
    );

    let proxy = Proxy::new(
        vec!["http://backend:3000"],
        HyperClient::default(),
    );

    let router = Router::new()
        .push(
            Router::with_path("{**rest}")
                .hoop(limiter)
                .goal(proxy)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Complete Gateway Example

```rust
use salvo::prelude::*;
use salvo::proxy::{Proxy, HyperClient};
use salvo::cors::Cors;
use salvo::compression::Compression;

#[handler]
async fn logging(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    let start = std::time::Instant::now();
    let method = req.method().clone();
    let path = req.uri().path().to_string();

    ctrl.call_next(req, depot, res).await;

    let duration = start.elapsed();
    let status = res.status_code().unwrap_or(StatusCode::OK);
    println!("{} {} -> {} ({:?})", method, path, status, duration);
}

#[tokio::main]
async fn main() {
    let cors = Cors::permissive();
    let compression = Compression::new();

    // Backend services
    let user_proxy = Proxy::new(vec!["http://users:3001"], HyperClient::default());
    let order_proxy = Proxy::new(vec!["http://orders:3002"], HyperClient::default());

    let router = Router::new()
        .hoop(logging)
        .hoop(cors)
        .hoop(compression)
        .push(Router::with_path("users/{**rest}").goal(user_proxy))
        .push(Router::with_path("orders/{**rest}").goal(order_proxy));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. **Use HyperClient for production**: Better performance than ReqwestClient
2. **Implement health checks**: Remove unhealthy backends from rotation
3. **Add timeout handling**: Prevent slow backends from blocking
4. **Log proxy requests**: Monitor traffic patterns
5. **Set proper headers**: X-Forwarded-For, X-Forwarded-Proto
6. **Apply rate limiting**: Protect backends from overload
7. **Use HTTPS between proxy and backends**: Secure internal traffic
8. **Handle WebSocket upgrades**: Ensure protocol support
