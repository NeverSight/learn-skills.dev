---
name: salvo-testing
description: Write unit and integration tests for Salvo applications using TestClient. Use for testing handlers, middleware, and API endpoints.
---

# Salvo Testing

This skill helps write tests for Salvo applications using the built-in testing utilities.

## Setup

Add to `Cargo.toml`:

```toml
[dev-dependencies]
salvo = { version = "0.89.0", features = ["test"] }
tokio-test = "0.4"
```

## Basic Handler Testing

```rust
use salvo::prelude::*;
use salvo::test::{ResponseExt, TestClient};

#[handler]
async fn hello() -> &'static str {
    "Hello World"
}

#[tokio::test]
async fn test_hello() {
    let router = Router::new().get(hello);
    let service = Service::new(router);

    let content = TestClient::get("http://127.0.0.1:8080/")
        .send(&service)
        .await
        .take_string()
        .await
        .unwrap();

    assert_eq!(content, "Hello World");
}
```

## Testing with Path Parameters

```rust
#[handler]
async fn show_user(req: &mut Request) -> String {
    let id = req.param::<i64>("id").unwrap();
    format!("User ID: {}", id)
}

#[tokio::test]
async fn test_show_user() {
    let router = Router::new()
        .push(Router::with_path("users/{id}").get(show_user));
    let service = Service::new(router);

    let content = TestClient::get("http://127.0.0.1:8080/users/123")
        .send(&service)
        .await
        .take_string()
        .await
        .unwrap();

    assert_eq!(content, "User ID: 123");
}
```

## Testing JSON Responses

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, PartialEq, Debug)]
struct User {
    id: i64,
    name: String,
}

#[handler]
async fn get_user() -> Json<User> {
    Json(User {
        id: 1,
        name: "Alice".to_string(),
    })
}

#[tokio::test]
async fn test_get_user() {
    let router = Router::new().get(get_user);
    let service = Service::new(router);

    let user = TestClient::get("http://127.0.0.1:8080/")
        .send(&service)
        .await
        .take_json::<User>()
        .await
        .unwrap();

    assert_eq!(user.id, 1);
    assert_eq!(user.name, "Alice");
}
```

## Testing POST Requests

```rust
#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[handler]
async fn create_user(body: JsonBody<CreateUser>) -> StatusCode {
    let user = body.into_inner();
    // Save user...
    StatusCode::CREATED
}

#[tokio::test]
async fn test_create_user() {
    let router = Router::new().post(create_user);
    let service = Service::new(router);

    let res = TestClient::post("http://127.0.0.1:8080/")
        .json(&serde_json::json!({
            "name": "Bob",
            "email": "bob@example.com"
        }))
        .send(&service)
        .await;

    assert_eq!(res.status_code(), Some(StatusCode::CREATED));
}
```

## Testing with Headers

```rust
#[handler]
async fn protected(req: &mut Request) -> Result<&'static str, StatusError> {
    let token = req.header::<String>("Authorization")
        .ok_or_else(|| StatusError::unauthorized())?;

    if token == "Bearer valid_token" {
        Ok("Protected content")
    } else {
        Err(StatusError::unauthorized())
    }
}

#[tokio::test]
async fn test_protected_with_valid_token() {
    let router = Router::new().get(protected);
    let service = Service::new(router);

    let content = TestClient::get("http://127.0.0.1:8080/")
        .add_header("Authorization", "Bearer valid_token", true)
        .send(&service)
        .await
        .take_string()
        .await
        .unwrap();

    assert_eq!(content, "Protected content");
}

#[tokio::test]
async fn test_protected_without_token() {
    let router = Router::new().get(protected);
    let service = Service::new(router);

    let res = TestClient::get("http://127.0.0.1:8080/")
        .send(&service)
        .await;

    assert_eq!(res.status_code(), Some(StatusCode::UNAUTHORIZED));
}
```

## Testing Middleware

```rust
#[handler]
async fn logger(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    depot.insert("logged", true);
    ctrl.call_next(req, depot, res).await;
}

#[handler]
async fn handler(depot: &mut Depot) -> String {
    let logged = depot.get::<bool>("logged").copied().unwrap_or(false);
    format!("Logged: {}", logged)
}

#[tokio::test]
async fn test_middleware() {
    let router = Router::new()
        .hoop(logger)
        .get(handler);
    let service = Service::new(router);

    let content = TestClient::get("http://127.0.0.1:8080/")
        .send(&service)
        .await
        .take_string()
        .await
        .unwrap();

    assert_eq!(content, "Logged: true");
}
```

## Testing with Query Parameters

```rust
#[handler]
async fn search(req: &mut Request) -> String {
    let query = req.query::<String>("q").unwrap_or_default();
    format!("Search: {}", query)
}

#[tokio::test]
async fn test_search() {
    let router = Router::new().get(search);
    let service = Service::new(router);

    let content = TestClient::get("http://127.0.0.1:8080/?q=rust")
        .send(&service)
        .await
        .take_string()
        .await
        .unwrap();

    assert_eq!(content, "Search: rust");
}
```

## Testing Error Handling

```rust
#[handler]
async fn may_fail(req: &mut Request) -> Result<String, StatusError> {
    let id = req.param::<i64>("id").unwrap();

    if id == 0 {
        return Err(StatusError::bad_request());
    }

    Ok(format!("ID: {}", id))
}

#[tokio::test]
async fn test_error_handling() {
    let router = Router::new()
        .push(Router::with_path("{id}").get(may_fail));
    let service = Service::new(router);

    let res = TestClient::get("http://127.0.0.1:8080/0")
        .send(&service)
        .await;

    assert_eq!(res.status_code(), Some(StatusCode::BAD_REQUEST));
}
```

## Testing with Depot

```rust
#[handler]
fn setup_depot(depot: &mut Depot) {
    depot.insert("config", "test_value");
}

#[handler]
async fn use_depot(depot: &mut Depot) -> String {
    let config = depot.get::<&str>("config").copied().unwrap();
    format!("Config: {}", config)
}

#[tokio::test]
async fn test_depot() {
    let router = Router::new()
        .hoop(setup_depot)
        .get(use_depot);
    let service = Service::new(router);

    let content = TestClient::get("http://127.0.0.1:8080/")
        .send(&service)
        .await
        .take_string()
        .await
        .unwrap();

    assert_eq!(content, "Config: test_value");
}
```

## Testing Form Data

```rust
#[tokio::test]
async fn test_form_submission() {
    let router = Router::new().post(handle_form);
    let service = Service::new(router);

    let res = TestClient::post("http://127.0.0.1:8080/")
        .form(&[("name", "Alice"), ("email", "alice@example.com")])
        .send(&service)
        .await;

    assert_eq!(res.status_code(), Some(StatusCode::OK));
}
```

## Integration Testing

```rust
#[tokio::test]
async fn test_full_crud() {
    let router = create_router();
    let service = Service::new(router);

    // Create
    let res = TestClient::post("http://127.0.0.1:8080/users")
        .json(&serde_json::json!({"name": "Alice"}))
        .send(&service)
        .await;
    assert_eq!(res.status_code(), Some(StatusCode::CREATED));

    // Read
    let user = TestClient::get("http://127.0.0.1:8080/users/1")
        .send(&service)
        .await
        .take_json::<User>()
        .await
        .unwrap();
    assert_eq!(user.name, "Alice");

    // Update
    let res = TestClient::patch("http://127.0.0.1:8080/users/1")
        .json(&serde_json::json!({"name": "Alice Updated"}))
        .send(&service)
        .await;
    assert_eq!(res.status_code(), Some(StatusCode::OK));

    // Delete
    let res = TestClient::delete("http://127.0.0.1:8080/users/1")
        .send(&service)
        .await;
    assert_eq!(res.status_code(), Some(StatusCode::NO_CONTENT));
}
```

## Best Practices

1. Test each handler in isolation
2. Test middleware separately from handlers
3. Test error cases and edge cases
4. Use descriptive test names
5. Test with different HTTP methods
6. Verify status codes and response bodies
7. Test authentication and authorization
8. Mock external dependencies
9. Use test fixtures for complex data
10. Run tests in parallel when possible
