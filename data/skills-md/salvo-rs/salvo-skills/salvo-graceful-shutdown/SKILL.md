---
name: salvo-graceful-shutdown
description: Implement graceful server shutdown to handle in-flight requests before stopping. Use for zero-downtime deployments and proper resource cleanup.
---

# Salvo Graceful Shutdown

This skill helps implement graceful server shutdown in Salvo applications to ensure in-flight requests are completed before the server stops.

## Why Graceful Shutdown?

- **Zero-downtime deployments**: Complete existing requests before stopping
- **Data integrity**: Ensure database transactions complete properly
- **Clean resource release**: Close connections and files cleanly
- **Better user experience**: Clients don't receive abrupt connection closures

## Setup

Graceful shutdown is built into Salvo core:

```toml
[dependencies]
salvo = "0.89.0"
tokio = { version = "1", features = ["full", "signal"] }
```

## Basic Graceful Shutdown

```rust
use salvo::prelude::*;
use salvo::server::ServerHandle;
use tokio::signal;

#[handler]
async fn hello() -> &'static str {
    "Hello, World!"
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().init();

    let router = Router::new().get(hello);
    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;

    // Create server and get handle
    let server = Server::new(acceptor);
    let handle = server.handle();

    // Spawn shutdown signal listener
    tokio::spawn(listen_shutdown_signal(handle));

    // Start serving
    server.serve(router).await;
}

async fn listen_shutdown_signal(handle: ServerHandle) {
    // Wait for Ctrl+C
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(windows)]
    let terminate = async {
        signal::windows::ctrl_c()
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    tokio::select! {
        _ = ctrl_c => println!("Received Ctrl+C, shutting down..."),
        _ = terminate => println!("Received terminate signal, shutting down..."),
    };

    // Graceful shutdown with no timeout (wait indefinitely)
    handle.stop_graceful(None);
}
```

## Shutdown with Timeout

Set a maximum time to wait for in-flight requests:

```rust
use std::time::Duration;
use salvo::server::ServerHandle;

async fn listen_shutdown_signal(handle: ServerHandle) {
    // Wait for signal...
    tokio::signal::ctrl_c().await.unwrap();

    println!("Shutting down, waiting up to 30 seconds for in-flight requests...");

    // Wait max 30 seconds for graceful shutdown
    handle.stop_graceful(Some(Duration::from_secs(30)));
}
```

## Cross-Platform Signal Handling

```rust
use salvo::server::ServerHandle;
use tokio::signal;

async fn listen_shutdown_signal(handle: ServerHandle) {
    // Ctrl+C handler (works on all platforms)
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
        println!("Ctrl+C received");
    };

    // Unix-specific signals
    #[cfg(unix)]
    let terminate = async {
        use tokio::signal::unix::{SignalKind, signal};

        let mut sigterm = signal(SignalKind::terminate())
            .expect("failed to install SIGTERM handler");
        let mut sigint = signal(SignalKind::interrupt())
            .expect("failed to install SIGINT handler");
        let mut sigquit = signal(SignalKind::quit())
            .expect("failed to install SIGQUIT handler");

        tokio::select! {
            _ = sigterm.recv() => println!("SIGTERM received"),
            _ = sigint.recv() => println!("SIGINT received"),
            _ = sigquit.recv() => println!("SIGQUIT received"),
        }
    };

    // Windows-specific signals
    #[cfg(windows)]
    let terminate = async {
        use tokio::signal::windows;

        let mut ctrl_c = windows::ctrl_c()
            .expect("failed to install ctrl_c handler");
        let mut ctrl_break = windows::ctrl_break()
            .expect("failed to install ctrl_break handler");
        let mut ctrl_close = windows::ctrl_close()
            .expect("failed to install ctrl_close handler");

        tokio::select! {
            _ = ctrl_c.recv() => println!("Ctrl+C received"),
            _ = ctrl_break.recv() => println!("Ctrl+Break received"),
            _ = ctrl_close.recv() => println!("Close received"),
        }
    };

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    };

    handle.stop_graceful(Some(std::time::Duration::from_secs(30)));
}
```

## Cleanup Before Shutdown

Run cleanup tasks before shutting down:

```rust
use salvo::prelude::*;
use salvo::server::ServerHandle;
use std::sync::Arc;
use tokio::sync::RwLock;

struct AppState {
    // Your application state
    db_pool: DatabasePool,
    cache: Cache,
}

async fn cleanup(state: Arc<RwLock<AppState>>) {
    println!("Running cleanup tasks...");

    let state = state.write().await;

    // Close database connections
    state.db_pool.close().await;
    println!("Database connections closed");

    // Flush cache
    state.cache.flush().await;
    println!("Cache flushed");

    // Other cleanup tasks...
    println!("Cleanup complete");
}

async fn listen_shutdown_signal(
    handle: ServerHandle,
    state: Arc<RwLock<AppState>>,
) {
    tokio::signal::ctrl_c().await.unwrap();
    println!("Shutdown signal received");

    // Run cleanup first
    cleanup(state).await;

    // Then stop the server
    handle.stop_graceful(Some(std::time::Duration::from_secs(30)));
}

#[tokio::main]
async fn main() {
    let state = Arc::new(RwLock::new(AppState::new()));

    let router = Router::new()
        .hoop(affix_state::inject(state.clone()))
        .get(handler);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    let server = Server::new(acceptor);
    let handle = server.handle();

    tokio::spawn(listen_shutdown_signal(handle, state));

    server.serve(router).await;
}
```

## Health Check During Shutdown

Indicate server is shutting down via health endpoint:

```rust
use salvo::prelude::*;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

static SHUTTING_DOWN: AtomicBool = AtomicBool::new(false);

#[handler]
async fn health_check(res: &mut Response) {
    if SHUTTING_DOWN.load(Ordering::Relaxed) {
        res.status_code(StatusCode::SERVICE_UNAVAILABLE);
        res.render(Json(serde_json::json!({
            "status": "shutting_down",
            "message": "Server is shutting down"
        })));
    } else {
        res.render(Json(serde_json::json!({
            "status": "healthy"
        })));
    }
}

async fn listen_shutdown_signal(handle: salvo::server::ServerHandle) {
    tokio::signal::ctrl_c().await.unwrap();

    // Mark as shutting down (load balancer will stop sending traffic)
    SHUTTING_DOWN.store(true, Ordering::Relaxed);
    println!("Marked as shutting down, waiting for traffic to drain...");

    // Wait for load balancer to detect and stop sending traffic
    tokio::time::sleep(std::time::Duration::from_secs(5)).await;

    // Now gracefully shutdown
    println!("Stopping server...");
    handle.stop_graceful(Some(std::time::Duration::from_secs(30)));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("health").get(health_check))
        .push(Router::with_path("api/{**rest}").get(api_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    let server = Server::new(acceptor);
    let handle = server.handle();

    tokio::spawn(listen_shutdown_signal(handle));

    server.serve(router).await;
}
```

## Kubernetes/Docker Shutdown

Handle SIGTERM from container orchestrators:

```rust
use salvo::prelude::*;
use salvo::server::ServerHandle;
use std::time::Duration;

async fn kubernetes_shutdown(handle: ServerHandle) {
    // Kubernetes sends SIGTERM, then SIGKILL after grace period

    #[cfg(unix)]
    {
        use tokio::signal::unix::{SignalKind, signal};

        let mut sigterm = signal(SignalKind::terminate())
            .expect("failed to install SIGTERM handler");

        sigterm.recv().await;
        println!("SIGTERM received from Kubernetes");
    }

    #[cfg(windows)]
    {
        tokio::signal::ctrl_c().await.unwrap();
        println!("Shutdown signal received");
    }

    // Kubernetes typically has 30s grace period
    // Use 25s to have buffer before SIGKILL
    handle.stop_graceful(Some(Duration::from_secs(25)));
}

#[tokio::main]
async fn main() {
    let router = Router::new().get(handler);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    let server = Server::new(acceptor);
    let handle = server.handle();

    tokio::spawn(kubernetes_shutdown(handle));

    server.serve(router).await;
}
```

## Complete Production Example

```rust
use salvo::prelude::*;
use salvo::server::ServerHandle;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::Duration;
use tokio::signal;

static SHUTTING_DOWN: AtomicBool = AtomicBool::new(false);

#[handler]
async fn hello() -> &'static str {
    "Hello, World!"
}

#[handler]
async fn health(res: &mut Response) {
    if SHUTTING_DOWN.load(Ordering::Relaxed) {
        res.status_code(StatusCode::SERVICE_UNAVAILABLE);
        res.render(Json(serde_json::json!({"status": "shutting_down"})));
    } else {
        res.render(Json(serde_json::json!({"status": "healthy"})));
    }
}

#[handler]
async fn ready(res: &mut Response) {
    if SHUTTING_DOWN.load(Ordering::Relaxed) {
        res.status_code(StatusCode::SERVICE_UNAVAILABLE);
        res.render("not ready");
    } else {
        res.render("ready");
    }
}

async fn shutdown_signal(handle: ServerHandle) {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(windows)]
    let terminate = async {
        signal::windows::ctrl_c()
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    tokio::select! {
        _ = ctrl_c => println!("Ctrl+C received"),
        _ = terminate => println!("Terminate signal received"),
    };

    println!("Starting graceful shutdown...");

    // Mark as shutting down
    SHUTTING_DOWN.store(true, Ordering::Relaxed);

    // Wait for load balancer health checks to fail
    println!("Waiting for traffic to drain...");
    tokio::time::sleep(Duration::from_secs(5)).await;

    // Graceful shutdown with 25s timeout
    println!("Stopping server...");
    handle.stop_graceful(Some(Duration::from_secs(25)));

    println!("Server stopped");
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().init();

    let router = Router::new()
        .push(Router::with_path("health").get(health))
        .push(Router::with_path("ready").get(ready))
        .push(Router::with_path("api").get(hello));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    let server = Server::new(acceptor);
    let handle = server.handle();

    tokio::spawn(shutdown_signal(handle));

    println!("Server starting on http://0.0.0.0:8080");
    server.serve(router).await;
    println!("Server has shut down");
}
```

## Best Practices

1. **Always use graceful shutdown in production**: Never abruptly terminate servers
2. **Set appropriate timeouts**: Balance between completing requests and fast shutdown
3. **Handle multiple signals**: Support both Ctrl+C and SIGTERM
4. **Health check integration**: Tell load balancers you're shutting down
5. **Run cleanup tasks**: Close database connections, flush caches
6. **Log shutdown progress**: Helps debugging deployment issues
7. **Match orchestrator grace period**: Shutdown before SIGKILL arrives
8. **Test shutdown behavior**: Ensure in-flight requests complete properly
