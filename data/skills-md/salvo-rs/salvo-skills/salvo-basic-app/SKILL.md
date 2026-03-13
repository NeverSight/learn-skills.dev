---
name: salvo-basic-app
description: Create basic Salvo web applications with handlers, routers, and server setup. Use when starting a new Salvo project or adding basic HTTP endpoints.
---

# Salvo Basic Application Setup

This skill helps create basic Salvo web applications with proper structure and best practices.

## Core Concepts

### Handler

Handlers process HTTP requests. Use the `#[handler]` macro on async functions:

```rust
use salvo::prelude::*;

#[handler]
async fn hello() -> &'static str {
    "Hello World"
}

#[handler]
async fn greet(req: &mut Request) -> String {
    let name = req.query::<String>("name").unwrap_or("World".to_string());
    format!("Hello, {}!", name)
}
```

Handler parameters can be in any order and are all optional:
- `req: &mut Request` - HTTP request object
- `res: &mut Response` - HTTP response object
- `depot: &mut Depot` - Request-scoped data storage
- `ctrl: &mut FlowCtrl` - Flow control for middleware

### Router

Routers define URL paths and attach handlers:

```rust
use salvo::prelude::*;

let router = Router::new()
    .get(hello)
    .push(Router::with_path("greet").get(greet));
```

### Server Setup

Basic server configuration:

```rust
use salvo::prelude::*;

#[handler]
async fn hello() -> &'static str {
    "Hello World"
}

#[tokio::main]
async fn main() {
    let router = Router::new().get(hello);
    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Response Types

### Returning Different Types

Handlers can return any type implementing `Writer` or `Scribe`:

```rust
use salvo::prelude::*;

#[handler]
async fn json_response() -> Json<serde_json::Value> {
    Json(serde_json::json!({"status": "ok"}))
}

#[handler]
async fn text_response() -> &'static str {
    "Plain text response"
}

#[handler]
async fn html_response(res: &mut Response) {
    res.render(salvo::writing::Html("<h1>Hello</h1>"));
}

#[handler]
async fn status_response() -> StatusCode {
    StatusCode::NO_CONTENT
}

#[handler]
async fn redirect_response(res: &mut Response) {
    res.render(salvo::writing::Redirect::found("https://example.com"));
}
```

### Rendering JSON

```rust
use salvo::prelude::*;
use serde::Serialize;

#[derive(Serialize)]
struct User {
    name: String,
    age: u8,
}

#[handler]
async fn get_user() -> Json<User> {
    Json(User {
        name: "Alice".to_string(),
        age: 30,
    })
}
```

### Error Handling

Return `Result<T, E>` where both implement `Writer`:

```rust
use salvo::prelude::*;

#[handler]
async fn may_fail() -> Result<Json<Data>, StatusError> {
    let data = fetch_data().await.map_err(|_| StatusError::internal_server_error())?;
    Ok(Json(data))
}
```

## Request Object

### Common Request Methods

```rust
#[handler]
async fn handle_request(req: &mut Request) -> String {
    // Get request method
    let method = req.method();

    // Get request URI
    let uri = req.uri();

    // Get header value
    if let Some(content_type) = req.header::<String>("Content-Type") {
        println!("Content-Type: {}", content_type);
    }

    // Get query parameter
    let name = req.query::<String>("name").unwrap_or_default();

    // Get path parameter (requires route like /users/{id})
    let id = req.param::<i64>("id").unwrap();

    // Parse JSON body
    let body: UserData = req.parse_json().await.unwrap();

    format!("Processed request")
}
```

## Response Object

### Common Response Methods

```rust
use salvo::prelude::*;

#[handler]
async fn handle_response(res: &mut Response) {
    // Set status code
    res.status_code(StatusCode::CREATED);

    // Set response header
    res.headers_mut().insert("X-Custom-Header", "value".parse().unwrap());

    // Render text response
    res.render("Hello, World!");
}
```

## Dependencies

Add to `Cargo.toml`:

```toml
[dependencies]
salvo = "0.89.0"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

## Best Practices

1. Use `#[handler]` macro for all handlers
2. Keep handlers focused on single responsibility
3. Use appropriate return types (Json, Text, StatusCode)
4. Handle errors with Result types
5. Use `TcpListener` for basic HTTP servers
6. Extract common logic into middleware using `hoop()`
