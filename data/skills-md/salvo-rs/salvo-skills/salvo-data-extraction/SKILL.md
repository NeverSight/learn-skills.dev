---
name: salvo-data-extraction
description: Extract and validate data from requests including JSON, forms, query parameters, and path parameters. Use for handling user input and API payloads.
---

# Salvo Data Extraction

This skill helps extract and validate data from HTTP requests in Salvo applications.

## Manual Extraction (Simplest)

For simple cases, extract directly from Request:

```rust
use salvo::prelude::*;

#[handler]
async fn handler(req: &mut Request) -> String {
    // Query parameter
    let name = req.query::<String>("name").unwrap_or_default();

    // Path parameter (requires route like /users/{id})
    let id = req.param::<i64>("id").unwrap();

    // Header
    let token = req.header::<String>("Authorization");

    // Parse JSON body
    let body: UserData = req.parse_json().await.unwrap();

    // Parse form data
    let form: LoginForm = req.parse_form().await.unwrap();

    // Parse query parameters as struct
    let pagination: Pagination = req.parse_queries().unwrap();

    format!("Processed request")
}
```

## Using JsonBody Extractor

```rust
use salvo::prelude::*;
use serde::Deserialize;

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[handler]
async fn create_user(body: JsonBody<CreateUser>) -> StatusCode {
    let user = body.into_inner();
    println!("Name: {}, Email: {}", user.name, user.email);
    StatusCode::CREATED
}
```

## Extractible Trait

The `Extractible` derive macro enables automatic data extraction from requests.

### Basic Usage

```rust
use salvo::prelude::*;
use serde::Deserialize;

#[derive(Extractible, Deserialize, Debug)]
#[salvo(extract(default_source(from = "body")))]
struct CreateUser {
    name: String,
    email: String,
}

#[handler]
async fn create_user(user: CreateUser) -> String {
    format!("Created user: {:?}", user)
}
```

## Data Sources

### JSON Body

```rust
#[derive(Extractible, Deserialize)]
#[salvo(extract(default_source(from = "body")))]
struct UserData {
    name: String,
    email: String,
}
```

### Query Parameters

```rust
#[derive(Extractible, Deserialize)]
#[salvo(extract(default_source(from = "query")))]
struct Pagination {
    page: Option<u32>,
    per_page: Option<u32>,
}

#[handler]
async fn list_items(query: Pagination) -> String {
    let page = query.page.unwrap_or(1);
    let per_page = query.per_page.unwrap_or(20);
    format!("Page {} with {} items", page, per_page)
}
```

### Path Parameters

```rust
#[derive(Extractible, Deserialize)]
#[salvo(extract(default_source(from = "param")))]
struct UserId {
    id: i64,
}

#[handler]
async fn show_user(params: UserId) -> String {
    format!("User ID: {}", params.id)
}
```

### Form Data

```rust
#[derive(Extractible, Deserialize)]
#[salvo(extract(default_source(from = "body"), default_format = "form"))]
struct LoginForm {
    username: String,
    password: String,
}

#[handler]
async fn login(form: LoginForm) -> Result<String, StatusError> {
    Ok(format!("Login: {}", form.username))
}
```

## Mixed Sources

Extract from multiple sources simultaneously:

```rust
#[derive(Extractible, Deserialize)]
struct UpdateUser {
    #[salvo(extract(source(from = "param")))]
    id: i64,

    #[salvo(extract(source(from = "body")))]
    name: String,

    #[salvo(extract(source(from = "body")))]
    email: String,
}

#[handler]
async fn update_user(data: UpdateUser) -> StatusCode {
    // data.id from path, name and email from body
    println!("Update user {}: {} {}", data.id, data.name, data.email);
    StatusCode::OK
}
```

## Depot Extraction

Extract data from `Depot` that was injected by middleware. This is useful for accessing authenticated user information or other request-scoped data.

### Basic Depot Extraction

```rust
use salvo::prelude::*;
use serde::{Deserialize, Serialize};

/// Middleware that injects user data into depot
#[handler]
async fn inject_user(depot: &mut Depot) {
    depot.insert("user_id", 123i64);
    depot.insert("username", "alice".to_string());
    depot.insert("is_admin", true);
}

/// Extract user context from depot
#[derive(Serialize, Deserialize, Extractible, Debug)]
#[salvo(extract(default_source(from = "depot")))]
struct UserContext {
    user_id: i64,
    username: String,
    is_admin: bool,
}

#[handler]
async fn protected_handler(user: UserContext) -> String {
    format!("Hello {}, your ID is {}", user.username, user.user_id)
}

// Router setup with middleware
let router = Router::new()
    .hoop(inject_user)
    .push(Router::with_path("protected").get(protected_handler));
```

### Supported Depot Types

Depot extraction supports the following types:
- `String` and `&'static str`
- Signed integers: `i8`, `i16`, `i32`, `i64`, `i128`, `isize`
- Unsigned integers: `u8`, `u16`, `u32`, `u64`, `u128`, `usize`
- Floating point: `f32`, `f64`
- `bool`

### Mixed Sources with Depot

Combine depot with other data sources:

```rust
#[derive(Serialize, Deserialize, Extractible, Debug)]
struct RequestData {
    #[salvo(extract(source(from = "depot")))]
    user_id: i64,
    #[salvo(extract(source(from = "query")))]
    page: i64,
    #[salvo(extract(source(from = "body")))]
    content: String,
}
```

## Validation with validator Crate

```rust
use salvo::prelude::*;
use serde::Deserialize;
use validator::Validate;

#[derive(Extractible, Deserialize, Validate)]
#[salvo(extract(default_source(from = "body")))]
struct CreateUser {
    #[validate(length(min = 1, max = 100))]
    name: String,

    #[validate(email)]
    email: String,

    #[validate(range(min = 18, max = 120))]
    age: u8,
}

#[handler]
async fn create_user(user: CreateUser) -> Result<StatusCode, StatusError> {
    // Validate input
    if let Err(errors) = user.validate() {
        return Err(StatusError::bad_request().brief(errors.to_string()));
    }
    Ok(StatusCode::CREATED)
}
```

### Custom Validation Rules

```rust
use validator::{Validate, ValidationError};

fn validate_username(username: &str) -> Result<(), ValidationError> {
    if username.contains("admin") {
        return Err(ValidationError::new("forbidden_username"));
    }
    Ok(())
}

#[derive(Deserialize, Validate)]
struct User {
    #[validate(custom(function = "validate_username"))]
    username: String,
}
```

## Nested Structures

```rust
use salvo::prelude::*;
use serde::Deserialize;

#[derive(Deserialize)]
struct Address {
    street: String,
    city: String,
    country: String,
}

#[derive(Extractible, Deserialize)]
#[salvo(extract(default_source(from = "body")))]
struct CreateUserWithAddress {
    name: String,
    email: String,
    address: Address,
}

#[handler]
async fn create_user(data: CreateUserWithAddress) -> Result<String, StatusError> {
    Ok(format!("User {} from {}", data.name, data.address.city))
}
```

## Error Handling

```rust
use salvo::prelude::*;
use serde::Deserialize;

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[handler]
async fn create_user(req: &mut Request, res: &mut Response) {
    match req.parse_json::<CreateUser>().await {
        Ok(user) => {
            res.render(Json(serde_json::json!({
                "success": true,
                "user": {"name": user.name, "email": user.email}
            })));
        }
        Err(e) => {
            res.status_code(StatusCode::BAD_REQUEST);
            res.render(Json(serde_json::json!({
                "error": format!("Invalid JSON: {}", e)
            })));
        }
    }
}
```

## Headers Extraction

```rust
#[handler]
async fn handler(req: &mut Request) -> Result<String, StatusError> {
    // Get specific header
    let auth = req.header::<String>("Authorization")
        .ok_or_else(|| StatusError::unauthorized())?;

    // Get content type
    let content_type = req.header::<String>("Content-Type");

    Ok(format!("Auth: {}", auth))
}
```

## Complete Example

```rust
use salvo::prelude::*;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Deserialize, Validate)]
struct CreateUser {
    #[validate(length(min = 1, max = 100))]
    name: String,
    #[validate(email)]
    email: String,
}

#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    per_page: Option<u32>,
}

#[derive(Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[handler]
async fn list_users(req: &mut Request) -> Json<Vec<User>> {
    let pagination: Pagination = req.parse_queries().unwrap_or(Pagination {
        page: Some(1),
        per_page: Some(20),
    });

    Json(vec![User {
        id: 1,
        name: "Alice".to_string(),
        email: "alice@example.com".to_string(),
    }])
}

#[handler]
async fn create_user(body: JsonBody<CreateUser>) -> Result<StatusCode, StatusError> {
    let user = body.into_inner();

    if let Err(e) = user.validate() {
        return Err(StatusError::bad_request().brief(e.to_string()));
    }

    Ok(StatusCode::CREATED)
}

#[handler]
async fn get_user(req: &mut Request) -> Result<Json<User>, StatusError> {
    let id = req.param::<i64>("id")
        .ok_or_else(|| StatusError::bad_request())?;

    Ok(Json(User {
        id,
        name: "Alice".to_string(),
        email: "alice@example.com".to_string(),
    }))
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(
            Router::with_path("users")
                .get(list_users)
                .post(create_user)
                .push(Router::with_path("{id}").get(get_user))
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. Use `JsonBody<T>` for simple JSON extraction
2. Use `Extractible` for complex multi-source extraction
3. Specify data sources explicitly for clarity
4. Validate input data at API boundaries
5. Use typed path parameters (`req.param::<i64>`)
6. Handle extraction errors with proper error responses
7. Use `into_inner()` to unwrap extracted data
8. Add `#[serde(default)]` for optional fields
