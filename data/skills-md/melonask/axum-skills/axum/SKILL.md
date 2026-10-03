---
name: axum
description: "Comprehensive guide for building web applications and APIs with the axum Rust framework (by tokio-rs). Use this skill whenever the user wants to: build web servers, REST APIs, or HTTP services in Rust using axum; set up routing with path parameters, nested routers, fallbacks, or method routing; use request extractors (Path, Query, Json, Form, Bytes, String, HeaderMap, State, Extension, WebSocket, Multipart, Cookie); create response types with IntoResponse; implement middleware with middleware::from_fn or tower layers; manage application state with State and FromRef; handle errors with custom IntoResponse implementations; work with WebSocket connections for real-time features; serve Server-Sent Events (SSE); handle multipart form uploads; manage cookies (signed, private, or plain); serve static files; configure CORS, tracing, compression, timeouts, and other tower-http layers; set up graceful shutdown; migrate from axum 0.7 to 0.8; or integrate axum with tower middleware. Make sure to use this skill when the user mentions axum, Rust web framework, Rust HTTP server, Rust REST API, tokio-rs axum, Rust web development, Rust API server, or any web service built with axum."
---

# Axum — Rust Web Framework

Axum is an ergonomic and modular web framework built on top of Tokio, Tower, and Hyper. It is maintained by the tokio-rs team and provides a first-class async experience for building HTTP services in Rust. Axum's design revolves around converting handler functions into services via traits like `FromRequest` and `IntoResponse`, making it both intuitive to use and deeply composable with the Tower middleware ecosystem. It supports HTTP/1 and HTTP/2 out of the box, WebSocket upgrades, Server-Sent Events, and integrates seamlessly with the broader tokio ecosystem.

## Crate Architecture

| Crate         | Version | Purpose                                                                                                                                                                                                                                                                                     |
| ------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `axum`        | 0.8.9   | Main crate — routing, handlers, extractors (Path, Query, Json, Form, Bytes, WebSocket, Multipart), middleware, SSE, body types                                                                                                                                                              |
| `axum-core`   | 0.5.6   | Core traits (`FromRequest`, `FromRequestParts`, `IntoResponse`, `IntoResponseParts`), body types, error types, middleware primitives                                                                                                                                                        |
| `axum-extra`  | 0.12.6  | Extended extractors: `CookieJar`, `SignedCookieJar`, `PrivateCookieJar`, `TypedHeader`, `Host`, `Either`/`Either3..8`, `OptionalQuery`, `Cached`, `JsonDeserializer`, `ErasedJson`, `JsonLines`, `WithRejection`, `TypedPath`, `AsyncReadBody`, `FileStream`, `Attachment`, `ErrorResponse` |
| `axum-macros` | 0.5.1   | Procedural macros: `#[debug_handler]`, `#[debug_middleware]`, `TypedPath` derive                                                                                                                                                                                                            |
| `tower-http`  | 0.6.x   | Production-ready middleware layers: CORS, tracing, compression, timeouts, auth, rate limiting, static file serving, request IDs                                                                                                                                                             |
| `tower`       | 0.5.x   | Service trait, `ServiceBuilder`, `ServiceExt` — the middleware foundation axum builds upon                                                                                                                                                                                                  |
| `tokio`       | 1.x     | Async runtime, TCP listener, signal handling, file I/O                                                                                                                                                                                                                                      |
| `hyper`       | 1.4+    | Low-level HTTP server/client (axum's HTTP implementation)                                                                                                                                                                                                                                   |
| `matchit`     | 0.9.x   | Path matching engine used by axum's router                                                                                                                                                                                                                                                  |

## Quick Start: Minimal Dependency Setup

The minimal setup only requires `axum` and `tokio`. Default features include HTTP/1, JSON, form, query, matched-path, original-uri, tokio integration, and tracing:

```toml
# Cargo.toml
[dependencies]
axum = "0.8.9"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

For a production-ready setup with all common features enabled:

```toml
# Cargo.toml
[dependencies]
axum = { version = "0.8.9", features = [
    "http1",         # HTTP/1.1 support (default)
    "http2",         # HTTP/2 support
    "json",          # Json extractor/response (default)
    "form",          # URL-encoded form extractor (default)
    "query",         # Query string extractor (default)
    "multipart",     # Multipart form data
    "ws",            # WebSocket support
    "macros",        # #[debug_handler], #[debug_middleware]
] }
axum-extra = { version = "0.12.6", features = [
    "typed-header",      # TypedHeader extractor
    "cookie",            # CookieJar (unsigned)
    "cookie-signed",     # SignedCookieJar
    "cookie-private",    # PrivateCookieJar
    "typed-routing",     # TypedPath derive macro
    "with-rejection",    # WithRejection wrapper
] }
tokio = { version = "1", features = ["full"] }
tower-http = { version = "0.6", features = [
    "cors", "trace", "compression-gzip", "timeout", "limit", "fs",
] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

### Feature Flags Reference

| Feature        | Default | Description                                         |
| -------------- | ------- | --------------------------------------------------- |
| `form`         | Yes     | URL-encoded form body extractor                     |
| `http1`        | Yes     | HTTP/1.1 support via hyper                          |
| `json`         | Yes     | JSON body extractor and `Json<T>` response          |
| `matched-path` | Yes     | `MatchedPath` extractor                             |
| `original-uri` | Yes     | `OriginalUri` extractor                             |
| `query`        | Yes     | Query string extractor                              |
| `tokio`        | Yes     | tokio runtime integration, `axum::serve`            |
| `tracing`      | Yes     | tracing instrumentation on requests                 |
| `tower-log`    | Yes     | Enable `tower/log` feature                          |
| `http2`        | No      | HTTP/2 support                                      |
| `multipart`    | No      | Multipart form data parsing                         |
| `ws`           | No      | WebSocket support                                   |
| `macros`       | No      | `#[debug_handler]` and `#[debug_middleware]` macros |

## Quick Reference: Which Guide Do I Need?

The user's task determines which reference file to read:

- **Routing, path parameters, nested routers, fallbacks, method routing** -> Read `references/routing.md`
- **Request extractors (Path, Query, Json, Form, Bytes, State, Extension, WebSocket, Multipart, cookies)** -> Read `references/extractors.md`
- **Response types, IntoResponse, IntoResponseParts, custom response builders** -> Read `references/responses.md`
- **Middleware (tower layers, from_fn, from_fn_with_state, map_request/response)** -> Read `references/middleware.md`
- **State management, FromRef, shared application state patterns** -> Read `references/state-management.md`
- **Error handling, custom error types, WithRejection** -> Read `references/error-handling.md`
- **WebSocket, SSE, real-time communication** -> Read `references/realtime.md`
- **Multipart uploads, file handling, static file serving** -> Read `references/files-uploads.md`
- **Cookie management (plain, signed, private)** -> Read `references/cookies.md`
- **tower-http layers (CORS, tracing, compression, auth, rate limiting)** -> Read `references/tower-http-layers.md`
- **Testing, tower::ServiceExt, into_service, oneshot** -> Read `references/testing.md`
- **Migration from axum 0.7 to 0.8, breaking changes** -> Read `references/migration-0.8.md`

## Core Patterns at a Glance

### 1. Build and Serve a Complete Application

This is the foundational pattern every axum application follows. The `Router` composes routes, `with_state` provides shared state, `layer` applies middleware, and `axum::serve` starts the server with built-in graceful shutdown support.

```rust
use axum::{
    Router, serve,
    routing::{get, post},
    extract::{State, Path, Json},
    response::IntoResponse,
    http::StatusCode,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone, Debug, Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
}

#[derive(Clone)]
struct AppState {
    users: Arc<RwLock<Vec<User>>>,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let state = AppState {
        users: Arc::new(RwLock::new(Vec::new())),
    };

    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .route("/users", get(list_users).post(create_user))
        .route("/users/{id}", get(get_user).delete(delete_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    serve(listener, app).await.unwrap();
}

async fn list_users(State(state): State<AppState>) -> Json<Vec<User>> {
    let users = state.users.read().await;
    Json(users.clone())
}

async fn create_user(
    State(state): State<AppState>,
    Json(mut user): Json<User>,
) -> (StatusCode, Json<User>) {
    let mut users = state.users.write().await;
    user.id = users.len() as u64 + 1;
    users.push(user.clone());
    (StatusCode::CREATED, Json(user))
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<u64>,
) -> Result<Json<User>, (StatusCode, String)> {
    let users = state.users.read().await;
    users.iter()
        .find(|u| u.id == id)
        .cloned()
        .map(Json)
        .ok_or_else(|| (StatusCode::NOT_FOUND, "User not found".to_string()))
}

async fn delete_user(
    State(state): State<AppState>,
    Path(id): Path<u64>,
) -> StatusCode {
    let mut users = state.users.write().await;
    if let Some(pos) = users.iter().position(|u| u.id == id) {
        users.remove(pos);
        StatusCode::NO_CONTENT
    } else {
        StatusCode::NOT_FOUND
    }
}
```

### 2. Authentication Middleware

Middleware in axum uses `middleware::from_fn` or `middleware::from_fn_with_state`. The middleware receives the full request, can inspect or modify it, call `next.run(req).await` to continue to the handler, and return a custom response to short-circuit.

```rust
use axum::{
    Router, routing::get,
    extract::{State, Request},
    middleware::{self, Next},
    response::IntoResponse,
    http::StatusCode,
};

async fn auth_middleware(
    State(state): State<AppState>,
    mut req: Request,
    next: Next,
) -> impl IntoResponse {
    let auth_header = req
        .headers()
        .get(http::header::AUTHORIZATION)
        .and_then(|v| v.to_str().ok());

    match auth_header {
        Some(token) if state.validate_token(token) => next.run(req).await,
        _ => (StatusCode::UNAUTHORIZED, "Unauthorized").into_response(),
    }
}

let app = Router::new()
    .route("/protected", get(protected_handler))
    .route_layer(middleware::from_fn(auth_middleware))
    .route("/public", get(public_handler)); // No auth required
```

### 3. Custom Error Handling

Axum's error model relies on `IntoResponse`. Implement it for any custom error type, then return `Result<T, YourError>` from handlers. The `?` operator propagates errors automatically since `Result<T, E>` implements `IntoResponse` when both `T` and `E` do.

```rust
use axum::response::{IntoResponse, Response};
use axum::http::StatusCode;

#[derive(Debug)]
enum AppError {
    NotFound(String),
    Unauthorized(String),
    InternalError(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Unauthorized(msg) => (StatusCode::UNAUTHORIZED, msg),
            AppError::InternalError(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
        };
        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "Not found: {}", msg),
            AppError::Unauthorized(msg) => write!(f, "Unauthorized: {}", msg),
            AppError::InternalError(msg) => write!(f, "Internal error: {}", msg),
        }
    }
}

impl std::error::Error for AppError {}

// Now use it in handlers:
async fn get_user(Path(id): Path<u64>) -> Result<Json<User>, AppError> {
    let user = db::find_user(id).await
        .ok_or_else(|| AppError::NotFound(format!("User {} not found", id)))?;
    Ok(Json(user))
}
```

### 4. WebSocket Real-Time Communication

WebSocket support requires the `ws` feature. Use `WebSocketUpgrade` as an extractor to upgrade HTTP connections. The handler returns the upgraded socket after calling `ws.on_upgrade()`. For HTTP/2 WebSocket support, register the route with `.any()` instead of `.get()`.

```rust
use axum::{
    extract::ws::{WebSocket, WebSocketUpgrade, Message},
    response::IntoResponse,
};

async fn ws_handler(ws: WebSocketUpgrade) -> impl IntoResponse {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(mut socket: WebSocket) {
    while let Some(Ok(msg)) = socket.recv().await {
        if socket.send(msg).await.is_err() {
            break;
        }
    }
}

// Register with .any() to support WebSocket over HTTP/2
let app = Router::new().route("/ws", any(ws_handler));
```

### 5. Server-Sent Events (SSE)

SSE provides a unidirectional stream from server to client. The `Sse` type wraps any `Stream<Item = Result<Event, Error>>`. Use `KeepAlive` to prevent connection drops.

```rust
use axum::response::sse::{Event, Sse, KeepAlive};
use std::convert::Infallible;

async fn sse_handler() -> Sse<impl futures_util::stream::Stream<Item = Result<Event, Infallible>> {
    let stream = async_stream::stream! {
        for i in 0..10 {
            yield Ok(Event::default()
                .data(format!("ping {}", i))
                .event("message"));
            tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        }
    };
    Sse::new(stream).keep_alive(KeepAlive::default())
}
```

### 6. CORS, Tracing, and tower-http Layers

Tower-http provides production-grade middleware as composable layers. Layers are applied via `ServiceBuilder` or directly with `.layer()`. Order matters — layers wrap the service, so the first `.layer()` call is the outermost layer.

```rust
use tower_http::{
    cors::{CorsLayer, Any},
    trace::TraceLayer,
    compression::CompressionLayer,
};
use tower::ServiceBuilder;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(CorsLayer::permissive())
            .layer(CompressionLayer::new()),
    );
```

## Key Concepts

### Extractor Categories

Axum extractors fall into two categories, and understanding the distinction is critical for writing correct handlers:

**FromRequestParts** — extract from request metadata (headers, path, query, state). These do NOT consume the request body and can appear in any order among themselves:

| Extractor        | Source                     | Example                                   |
| ---------------- | -------------------------- | ----------------------------------------- |
| `Path<T>`        | URL path segments          | `Path(id): Path<u64>`                     |
| `Query<T>`       | Query string               | `Query(params): Query<SearchParams>`      |
| `State<T>`       | Application state          | `State(db): State<DbPool>`                |
| `Extension<T>`   | Request extensions         | `Extension(user): Extension<User>`        |
| `HeaderMap`      | All headers                | `HeaderMap(headers): HeaderMap`           |
| `CookieJar`      | Cookies (axum-extra)       | `jar: CookieJar`                          |
| `TypedHeader<T>` | Single header (axum-extra) | `TypedHeader(ua): TypedHeader<UserAgent>` |
| `MatchedPath`    | Matched route pattern      | `MatchedPath(path)`                       |
| `OriginalUri`    | Original request URI       | `OriginalUri(uri)`                        |

**FromRequest** — extract from the request body. These CONSUME the body and must be the last extractor parameter:

| Extractor          | Body Type              | Example                        |
| ------------------ | ---------------------- | ------------------------------ |
| `Json<T>`          | JSON                   | `Json(data): Json<CreateUser>` |
| `Form<T>`          | URL-encoded form       | `Form(data): Form<LoginForm>`  |
| `String`           | Raw text body          | `body: String`                 |
| `Bytes`            | Raw bytes body         | `body: bytes::Bytes`           |
| `Multipart`        | Multipart form         | `multipart: Multipart`         |
| `Request`          | Full request with body | `req: extract::Request`        |
| `Body`             | Raw axum body          | `body: axum::body::Body`       |
| `WebSocketUpgrade` | WebSocket upgrade      | `ws: WebSocketUpgrade`         |

### Middleware Layer Stack

Understanding the layering order is essential. Tower layers wrap the service from outside-in. The first layer applied is the outermost — it sees the request first and the response last:

```
Incoming Request
    |
    v
TraceLayer          (logs request, starts span)
    |
    v
CorsLayer           (adds CORS headers)
    |
    v
CompressionLayer    (decompresses request)
    |
    v
AuthMiddleware       (from_fn: validates token)
    |
    v
Handler              (your route handler)
    |
    v
CompressionLayer    (compresses response)
    |
    v
CorsLayer           (adds CORS headers to response)
    |
    v
TraceLayer          (logs response, ends span)
    |
    v
Outgoing Response
```

### State Management Patterns

The `State<T>` extractor provides type-safe access to shared application state. The state type must implement `Clone` because axum clones it for each request. For complex state, use `Arc` internally to avoid expensive cloning.

```rust
#[derive(Clone)]
struct AppState {
    db: Arc<DbPool>,            // Arc for shared ownership
    config: AppConfig,           // Small types can be Clone directly
}

// FromRef lets you extract sub-parts of state
#[derive(Clone)]
struct AppState {
    db: DbPool,
    cache: RedisClient,
}

impl FromRef<AppState> for DbPool {
    fn from_ref(state: &AppState) -> Self {
        state.db.clone()
    }
}

impl FromRef<AppState> for RedisClient {
    fn from_ref(state: &AppState) -> Self {
        state.cache.clone()
    }
}

// Now extract individual fields directly:
async fn handler(State(db): State<DbPool>, State(cache): State<RedisClient>) { }
```

The `#[derive(FromRef)]` macro (from axum's `macros` feature) can auto-generate these implementations for struct fields.

## Common Pitfalls

1. **Body-consuming extractors must be last** — `Json`, `String`, `Bytes`, `Form`, `Multipart`, and `Request` consume the body. Place them as the final parameter in your handler function signature. If you put a `FromRequestParts` extractor after a body extractor, it will fail at compile time or runtime.

2. **State must be `Clone + Send + Sync`** — axum clones the state type for each request via `.with_state(state)`. Wrap expensive-to-clone fields in `Arc` or `Arc<RwLock<>>` so the clone is cheap. The type itself must be `Send + Sync` because handlers run on Tokio's thread pool.

3. **All handlers must be `Send + Sync` (0.8+)** — axum 0.8 requires that handler functions and any captured state are `Send + Sync`. If you use `Rc`, `RefCell`, or other non-thread-safe types, the code will not compile. Use `Arc` and `RwLock`/`Mutex` instead.

4. **Path syntax changed in 0.8** — Use `{id}` instead of `:id`, and `{*path}` instead of `*path`. The old colon syntax no longer compiles. This was driven by an upgrade to matchit 0.8/0.9.

5. **Don't double-nest at the same path** — `.nest("/api", a).nest("/api", b)` will panic at runtime. Instead, merge the routers first: `let combined = a.merge(b); app.nest("/api", combined)`.

6. **Default body limit is 2MB** — `Json`, `Form`, and `Multipart` extractors reject bodies larger than 2MB by default. For file uploads or large payloads, increase the limit with `DefaultBodyLimit::max()` or disable it with `DefaultBodyLimit::disable()`.

7. **WebSocket over HTTP/2 needs `.any()`** — When using HTTP/2 (the `http2` feature), WebSocket upgrade requests are not sent as GET requests. Register WebSocket handlers with `.any(ws_handler)` instead of `.get(ws_handler)` to ensure compatibility with both HTTP/1 and HTTP/2.

8. **`Option<T>` behavior changed in 0.8** — `Option<Path<T>>` now rejects the request if path segments exist but fail to parse (instead of silently returning `None`). Use `OptionalFromRequestParts`/`OptionalFromRequest` implementations for fine-grained control.

9. **`#[async_trait]` is no longer needed** — Custom extractors and middleware in 0.8 use native `impl Future` in traits instead of the `#[async_trait]` macro. Remove `async_trait` from your implementations when upgrading from 0.7.

10. **Layer ordering is outside-in** — The first `.layer()` call wraps the outermost layer. For `ServiceBuilder`, layers are applied in order (first listed = outermost). Think carefully about whether your auth middleware should see requests before or after decompression.

## Reference Files

For detailed information on any topic, read the appropriate reference file:

- `references/routing.md` — Route definition, path parameters (new `{id}` syntax), wildcard `{*path}`, nested routers, `nest` vs `merge`, `fallback`, `method_not_allowed_fallback`, `route_service`, `nest_service`, `MethodRouter` chaining, method-specific routing, `CONNECT` method
- `references/extractors.md` — All built-in extractors (Path, Query, Json, Form, Bytes, String, State, Extension, HeaderMap, MatchedPath, OriginalUri, ConnectInfo, WebSocketUpgrade, Multipart, Request, Body), axum-extra extractors (CookieJar, SignedCookieJar, PrivateCookieJar, TypedHeader, Host, Either/Either3..8, OptionalQuery, Cached, JsonDeserializer, WithRejection), custom extractor implementation, FromRequestParts vs FromRequest, `Option<T>` and `Result<T, E>` extractor patterns
- `references/responses.md` — IntoResponse trait and all implementations (String, Json, Html, StatusCode, tuples, Sse, WebSocketUpgrade, Redirect, NoContent), IntoResponseParts for headers/cookies, AppendHeaders, custom IntoResponse implementations, response builder patterns
- `references/middleware.md` — `middleware::from_fn`, `middleware::from_fn_with_state`, `middleware::map_request`, `middleware::map_response`, applying middleware to specific routes with `route_layer`, layer on Router vs MethodRouter, request/response transformation, composing multiple middleware, custom middleware patterns
- `references/state-management.md` — `Router::with_state`, `State<T>` extractor, `FromRef` trait, `#[derive(FromRef)]` macro, `Extension<T>` for runtime injection, sharing state across middleware and handlers, state lifetime patterns with `Arc`, `Arc<RwLock<>>`, `Arc<Mutex<>>`
- `references/error-handling.md` — Custom error types with IntoResponse, Result<T, E> in handlers, BoxError, `#[derive(Debug)]` patterns, rejection types, `WithRejection` wrapper, error propagation with `?`, combining multiple error types, axum-extra `ErrorResponse`
- `references/realtime.md` — WebSocket setup and configuration (max_frame_size, max_send_queue, write_buffer_size), WebSocket message types (Text with Utf8Bytes, Binary with Bytes), WebSocket over HTTP/2, Server-Sent Events (SSE) with Event streams, KeepAlive, JSON data in SSE, binary SSE data, broadcast patterns with tokio::sync::broadcast
- `references/files-uploads.md` — Multipart form handling, field iteration (name, file_name, content_type, bytes, text, chunk), saving uploaded files, `DefaultBodyLimit` for upload size, static file serving with `ServeDir` and `ServeFile`, SPA fallback patterns, `tower_http::services::ServeDir`
- `references/cookies.md` — CookieJar (unsigned), SignedCookieJar (HMAC-signed), PrivateCookieJar (AES-encrypted), cookie Key generation and management, `FromRef` for Key, reading/writing/removing cookies, cookie options (path, domain, secure, httponly, max-age, same-site)
- `references/tower-http-layers.md` — Complete reference for all tower-http layers: CorsLayer (permissive and restrictive), TraceLayer, CompressionLayer/DecompressionLayer, RequestBodyLimitLayer, TimeoutLayer, SetRequestIdLayer, PropagateHeaderLayer, SensitiveHeaderLayer, CatchPanicLayer, AuthLayer/RequireAuthorizationLayer, MetricsLayer, NormalizePathLayer, SetHeaderLayer, SetStatusLayer, RedirectLayer, ServeDir/ServeFile
- `references/testing.md` — `tower::ServiceExt::oneshot` for unit testing, `Router::into_service`, building test requests, asserting response status and body, integration testing patterns, test state setup
- `references/migration-0.8.md` — Complete migration guide from axum 0.7 to 0.8: path syntax changes, Host extractor move, WebSocket Message type changes, Option<T> behavior, Sync requirement, removed APIs, new APIs (method_not_allowed_fallback, NoContent, WebSocket over HTTP/2, CONNECT method)
