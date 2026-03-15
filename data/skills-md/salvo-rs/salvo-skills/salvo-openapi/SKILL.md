---
name: salvo-openapi
description: Generate OpenAPI documentation automatically from Salvo handlers. Use for API documentation, Swagger UI, and API client generation.
---

# Salvo OpenAPI Integration

This skill helps generate OpenAPI 3.0 documentation from Salvo applications.

## Key Difference: #[handler] vs #[endpoint]

- `#[handler]` - Basic Salvo handler, no OpenAPI documentation
- `#[endpoint]` - Generates OpenAPI documentation automatically

Use `#[endpoint]` for all handlers that should appear in API documentation.

## Setup

Add dependencies:

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["oapi"] }
serde = { version = "1", features = ["derive"] }
```

## Basic Usage

Use `#[endpoint]` instead of `#[handler]`:

```rust
use salvo::oapi::extract::*;
use salvo::prelude::*;

#[endpoint]
async fn hello(name: QueryParam<String, false>) -> String {
    format!("Hello, {}!", name.as_deref().unwrap_or("World"))
}

#[tokio::main]
async fn main() {
    let router = Router::new().push(Router::with_path("hello").get(hello));

    // Create OpenAPI documentation
    let doc = OpenApi::new("My API", "1.0.0").merge_router(&router);

    // Add routes for API documentation
    let router = router
        .unshift(doc.into_router("/api-doc/openapi.json"))
        .unshift(SwaggerUi::new("/api-doc/openapi.json").into_router("/swagger-ui"));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## OpenAPI Extractors

These extractors work with both `#[handler]` and `#[endpoint]`, but only generate documentation with `#[endpoint]`:

### Path Parameters

```rust
use salvo::oapi::extract::PathParam;

#[endpoint]
async fn get_user(id: PathParam<i64>) -> String {
    format!("User ID: {}", id.into_inner())
}
```

### Query Parameters

```rust
use salvo::oapi::extract::QueryParam;

// Optional parameter (false = not required)
#[endpoint]
async fn search(q: QueryParam<String, false>) -> String {
    format!("Search: {}", q.as_deref().unwrap_or(""))
}

// Required parameter (true = required)
#[endpoint]
async fn search_required(q: QueryParam<String, true>) -> String {
    format!("Search: {}", q.into_inner())
}
```

### JSON Body

```rust
use salvo::oapi::extract::JsonBody;

#[endpoint]
async fn create_user(user: JsonBody<CreateUser>) -> StatusCode {
    // user.into_inner() to get the actual value
    StatusCode::CREATED
}
```

## Request Body Documentation

```rust
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, ToSchema)]
struct CreateUser {
    /// User's full name
    name: String,
    /// User's email address
    #[salvo(schema(example = "user@example.com"))]
    email: String,
}

#[endpoint]
async fn create_user(body: JsonBody<CreateUser>) -> StatusCode {
    StatusCode::CREATED
}
```

## Response Documentation

```rust
use salvo::oapi::ToSchema;
use serde::Serialize;

#[derive(Serialize, ToSchema)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[endpoint]
async fn get_user(id: PathParam<i64>) -> Json<User> {
    Json(User {
        id: id.into_inner(),
        name: "John".to_string(),
        email: "john@example.com".to_string(),
    })
}
```

## Query Parameters with ToParameters

```rust
use salvo::oapi::{ToParameters, ToSchema};
use serde::Deserialize;

#[derive(Deserialize, ToParameters)]
struct Pagination {
    /// Page number
    #[salvo(parameter(default = 1, minimum = 1))]
    page: Option<u32>,
    /// Items per page
    #[salvo(parameter(default = 20, minimum = 1, maximum = 100))]
    per_page: Option<u32>,
}

#[endpoint]
async fn list_users(pagination: Pagination) -> Json<Vec<User>> {
    let page = pagination.page.unwrap_or(1);
    let per_page = pagination.per_page.unwrap_or(20);
    Json(vec![])
}
```

## Status Codes and Error Responses

```rust
use salvo::oapi::ToSchema;
use serde::Serialize;

#[derive(Serialize, ToSchema)]
struct ErrorResponse {
    message: String,
}

#[endpoint(
    status_codes(200, 404),
    responses(
        (status_code = 200, description = "User found", body = User),
        (status_code = 404, description = "User not found", body = ErrorResponse),
    )
)]
async fn get_user(id: PathParam<i64>) -> Result<Json<User>, StatusError> {
    Ok(Json(User {
        id: id.into_inner(),
        name: "John".to_string(),
        email: "john@example.com".to_string(),
    }))
}
```

## Tags, Summary and Description

```rust
#[endpoint(
    tags("users"),
    summary = "Create a new user",
    description = "Creates a new user account with the provided information"
)]
async fn create_user(body: JsonBody<CreateUser>) -> StatusCode {
    StatusCode::CREATED
}
```

## OpenAPI Document Generation

```rust
use salvo::oapi::{OpenApi, Info, License};

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("users").get(list_users).post(create_user))
        .push(Router::with_path("users/{id}").get(show_user));

    let doc = OpenApi::new("My API", "1.0.0")
        .info(
            Info::new("My API", "1.0.0")
                .description("API description")
                .license(License::new("MIT"))
        )
        .merge_router(&router);

    let router = router
        .push(doc.into_router("/api-doc/openapi.json"))
        .push(SwaggerUi::new("/api-doc/openapi.json").into_router("/swagger-ui"));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Swagger UI

```rust
use salvo::oapi::swagger_ui::SwaggerUi;

let router = router.push(
    SwaggerUi::new("/api-doc/openapi.json")
        .into_router("/swagger-ui")
);
```

## Schema Customization

```rust
use salvo::oapi::ToSchema;
use serde::Serialize;

#[derive(Serialize, ToSchema)]
#[salvo(schema(example = json!({"id": 1, "name": "John", "email": "john@example.com"})))]
struct User {
    id: i64,

    #[salvo(schema(minimum = 1, maximum = 100))]
    age: Option<u8>,

    #[salvo(schema(pattern = "^[a-zA-Z]+$"))]
    name: String,

    #[salvo(schema(format = "email"))]
    email: String,
}
```

## Security Schemes

```rust
use salvo::oapi::security::{Http, HttpAuthScheme, SecurityScheme};
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("users").get(list_users))
        .push(Router::with_path("profile").get(get_profile));

    let doc = OpenApi::new("My API", "1.0.0")
        .description("API with authentication")
        .add_security_scheme(
            "bearer_auth",
            SecurityScheme::Http(Http::new(HttpAuthScheme::Bearer))
        )
        .merge_router(&router);

    let router = router
        .unshift(doc.into_router("/api-doc/openapi.json"))
        .unshift(SwaggerUi::new("/api-doc/openapi.json").into_router("/swagger-ui"));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}

#[endpoint(
    security(("bearer_auth" = []))
)]
async fn get_profile() -> &'static str {
    "Protected profile"
}
```

## File Upload Documentation

```rust
use salvo::oapi::extract::*;

#[endpoint(
    tags("files"),
    request_body(content = "multipart/form-data")
)]
async fn upload_file(req: &mut Request) -> Result<Json<UploadResponse>, StatusError> {
    let file = req.file("file").await
        .ok_or_else(|| StatusError::bad_request())?;

    let filename = file.name().unwrap_or("unnamed").to_string();
    let size = file.size();

    Ok(Json(UploadResponse { filename, size }))
}
```

## Complete OpenAPI Setup Example

```rust
use salvo::oapi::extract::*;
use salvo::oapi::{OpenApi, ToSchema, ToParameters};
use salvo::prelude::*;
use serde::{Deserialize, Serialize};

// Schema definitions
#[derive(Serialize, Deserialize, ToSchema)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize, ToSchema)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Deserialize, ToParameters)]
struct Pagination {
    #[salvo(parameter(default = 1))]
    page: Option<u32>,
    #[salvo(parameter(default = 20))]
    per_page: Option<u32>,
}

// Endpoints
#[endpoint(tags("users"), summary = "List all users")]
async fn list_users(pagination: Pagination) -> Json<Vec<User>> {
    Json(vec![])
}

#[endpoint(tags("users"), summary = "Get user by ID")]
async fn get_user(id: PathParam<i64>) -> Result<Json<User>, StatusError> {
    Ok(Json(User {
        id: id.into_inner(),
        name: "John".to_string(),
        email: "john@example.com".to_string(),
    }))
}

#[endpoint(tags("users"), summary = "Create a new user", status_codes(201))]
async fn create_user(body: JsonBody<CreateUser>) -> StatusCode {
    StatusCode::CREATED
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

    // Create OpenAPI documentation with metadata
    let doc = OpenApi::new("User API", "1.0.0")
        .description("A comprehensive user management API")
        .contact_name("API Support")
        .contact_email("support@example.com")
        .license_name("MIT")
        .merge_router(&router);

    // Add documentation routes
    let router = router
        .unshift(doc.into_router("/api-doc/openapi.json"))
        .unshift(SwaggerUi::new("/api-doc/openapi.json").into_router("/swagger-ui"));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Generated Client Libraries

With OpenAPI documentation, you can generate client libraries:

- **OpenAPI Generator**: `openapi-generator-cli generate -i openapi.json -g rust`
- **Swagger Codegen**: For various languages
- **Postman**: Import directly for testing

## Best Practices for Automatic Documentation

### Use Function Parameters Instead of Manual Extraction

**IMPORTANT**: For OpenAPI documentation to be generated automatically, use function parameter extractors instead of manually extracting from `Request`.

```rust
// ❌ BAD: Manual extraction - NO OpenAPI documentation generated
#[endpoint]
async fn get_user(req: &mut Request) -> Json<User> {
    let id = req.param::<i64>("id").unwrap();  // Not documented!
    let page = req.query::<i32>("page");        // Not documented!
    // ...
}

// ✅ GOOD: Parameter extractors - OpenAPI documentation auto-generated
#[endpoint]
async fn get_user(
    id: PathParam<i64>,           // Documented as path parameter
    page: QueryParam<i32, false>, // Documented as optional query parameter
) -> Json<User> {
    // ...
}
```

When you use extractors like `PathParam`, `QueryParam`, `JsonBody`, the OpenAPI generator can:
- Automatically detect parameter names and types
- Mark parameters as required or optional
- Generate proper schema definitions

### Return Result with impl Writer Types

**IMPORTANT**: Return `Result<T, E>` where both `T` and `E` implement `Writer` and `EndpointOutRegister`. This enables automatic documentation of both success and error responses.

```rust
// ❌ LIMITED: Only success response documented
#[endpoint]
async fn get_user(id: PathParam<i64>) -> Json<User> {
    Json(User { /* ... */ })
}

// ✅ BETTER: Both success and error responses documented
#[endpoint]
async fn get_user(id: PathParam<i64>) -> Result<Json<User>, StatusError> {
    let id = id.into_inner();
    if id <= 0 {
        return Err(StatusError::bad_request().brief("Invalid ID"));
    }
    Ok(Json(User { id, name: "John".into(), email: "john@example.com".into() }))
}
```

### Custom Error Types for Rich Documentation

Define custom error types that implement `Writer` and `EndpointOutRegister` for detailed error documentation:

```rust
use salvo::oapi::{ToSchema, EndpointOutRegister, Components, Operation};
use salvo::prelude::*;
use serde::Serialize;

#[derive(Debug, Serialize, ToSchema)]
struct ApiError {
    /// Error code
    code: i32,
    /// Error message
    message: String,
}

impl Writer for ApiError {
    async fn write(self, _req: &mut Request, _depot: &mut Depot, res: &mut Response) {
        res.status_code(StatusCode::BAD_REQUEST);
        res.render(Json(self));
    }
}

impl EndpointOutRegister for ApiError {
    fn register(components: &mut Components, operation: &mut Operation) {
        operation.responses.insert(
            "400".into(),
            salvo::oapi::Response::new("Bad Request")
                .add_content("application/json", Self::to_schema(components)),
        );
    }
}

// Now both success and custom error are documented
#[endpoint]
async fn create_user(body: JsonBody<CreateUser>) -> Result<Json<User>, ApiError> {
    let user = body.into_inner();
    if user.name.is_empty() {
        return Err(ApiError {
            code: 1001,
            message: "Name cannot be empty".into(),
        });
    }
    Ok(Json(User { id: 1, name: user.name, email: user.email }))
}
```

### Summary of Documentation Requirements

| Pattern | Parameters Documented | Response Documented |
|---------|----------------------|---------------------|
| `req.param()` / `req.query()` | ❌ No | - |
| `PathParam<T>` / `QueryParam<T>` | ✅ Yes | - |
| `-> Json<T>` | - | ✅ Success only |
| `-> Result<Json<T>, StatusError>` | - | ✅ Success + Error |
| `-> Result<Json<T>, CustomError>` | - | ✅ Full control |

## General Best Practices

1. Use `#[endpoint]` for all API handlers that need documentation
2. **Use function parameter extractors** (not manual `Request` extraction) for auto-documentation
3. **Return `Result<T, E>`** where both types implement `Writer` for complete response documentation
4. Add `ToSchema` to all request/response types
5. Document fields with Rust doc comments (`///`)
6. Use `ToParameters` for query parameter structs
7. Specify response status codes explicitly
8. Group endpoints with meaningful tags
9. Provide examples for complex schemas
10. Use security schemes for protected endpoints
11. Serve Swagger UI for interactive documentation
12. Keep documentation in sync by generating from code
