---
name: salvo-auth
description: Implement authentication and authorization using JWT, Basic Auth, or custom schemes. Use for securing API endpoints and user management.
---

# Salvo Authentication

This skill helps implement authentication and authorization in Salvo applications.

## JWT Authentication

### Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["jwt-auth"] }
jsonwebtoken = "9"
serde = { version = "1", features = ["derive"] }
chrono = "0.4"
```

### JWT Middleware Setup

```rust
use salvo::jwt_auth::{JwtAuth, JwtClaims};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct JwtClaims {
    sub: String,
    exp: i64,
    role: String,
}

const SECRET_KEY: &str = "your-secret-key-at-least-32-bytes";

#[tokio::main]
async fn main() {
    let auth_handler = JwtAuth::new("secret_key")
        .finders(vec![
            Box::new(HeaderFinder::new()),
            Box::new(QueryFinder::new("token")),
        ]);

    let router = Router::new()
        .push(Router::with_path("login").post(login))
        .push(
            Router::with_path("protected")
                .hoop(auth_handler)
                .get(protected_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

### Login Handler

```rust
use jsonwebtoken::{encode, EncodingKey, Header};
use salvo::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct LoginRequest {
    username: String,
    password: String,
}

#[derive(Serialize)]
struct LoginResponse {
    token: String,
}

#[handler]
async fn login(body: JsonBody<LoginRequest>) -> Result<Json<LoginResponse>, StatusError> {
    let req = body.into_inner();

    // Validate credentials (replace with actual validation)
    if req.username != "admin" || req.password != "password" {
        return Err(StatusError::unauthorized());
    }

    // Create JWT claims
    let claims = JwtClaims {
        sub: req.username,
        exp: (chrono::Utc::now() + chrono::Duration::hours(24)).timestamp(),
        role: "user".to_string(),
    };

    // Encode JWT
    let token = encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(SECRET_KEY.as_bytes()),
    )
    .map_err(|_| StatusError::internal_server_error())?;

    Ok(Json(LoginResponse { token }))
}
```

### Protected Handler

```rust
use salvo::jwt_auth::JwtAuthDepotExt;

#[handler]
async fn protected_handler(depot: &mut Depot) -> Result<String, StatusError> {
    let token_data = depot.jwt_auth_data::<JwtClaims>()
        .ok_or_else(|| StatusError::unauthorized())?;

    Ok(format!("Hello, {}! Role: {}", token_data.claims.sub, token_data.claims.role))
}
```

## Basic Authentication

### Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["basic-auth"] }
```

### Basic Auth Middleware

```rust
use salvo::prelude::*;
use salvo::basic_auth::{BasicAuth, BasicAuthValidator};

struct MyValidator;

impl BasicAuthValidator for MyValidator {
    async fn validate(&self, username: &str, password: &str, depot: &mut Depot) -> bool {
        if username == "admin" && password == "password" {
            depot.insert("user_role", "admin");
            true
        } else if username == "user" && password == "userpass" {
            depot.insert("user_role", "user");
            true
        } else {
            false
        }
    }
}

#[tokio::main]
async fn main() {
    let auth_handler = BasicAuth::new(MyValidator);

    let router = Router::new()
        .push(
            Router::with_path("admin")
                .hoop(auth_handler)
                .get(admin_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Custom Authentication Middleware

```rust
use salvo::prelude::*;

#[handler]
async fn auth_middleware(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    let token = req.header::<String>("Authorization")
        .and_then(|h| h.strip_prefix("Bearer ").map(String::from));

    match token {
        Some(token) => {
            match validate_token(&token) {
                Ok(user_id) => {
                    depot.insert("user_id", user_id);
                    ctrl.call_next(req, depot, res).await;
                }
                Err(_) => {
                    res.status_code(StatusCode::UNAUTHORIZED);
                    res.render(Json(serde_json::json!({"error": "Invalid token"})));
                    ctrl.skip_rest();
                }
            }
        }
        None => {
            res.status_code(StatusCode::UNAUTHORIZED);
            res.render(Json(serde_json::json!({"error": "Missing token"})));
            ctrl.skip_rest();
        }
    }
}

fn validate_token(token: &str) -> Result<i64, ()> {
    // Implement token validation logic
    if token == "valid_token" {
        Ok(123)
    } else {
        Err(())
    }
}
```

## API Key Authentication

```rust
#[handler]
async fn api_key_auth(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    let api_key = req.header::<String>("X-API-Key");

    match api_key {
        Some(key) if is_valid_api_key(&key) => {
            depot.insert("api_key", key);
            ctrl.call_next(req, depot, res).await;
        }
        _ => {
            res.status_code(StatusCode::UNAUTHORIZED);
            res.render("Invalid API key");
            ctrl.skip_rest();
        }
    }
}

fn is_valid_api_key(key: &str) -> bool {
    // Validate against database or config
    key == "valid-api-key-12345"
}
```

## Session-Based Authentication

```rust
use salvo::prelude::*;
use salvo::session::{SessionHandler, CookieStore, SessionDepotExt};

#[tokio::main]
async fn main() {
    let session_handler = SessionHandler::builder(
        CookieStore::new(),
        b"secret_key_must_be_at_least_64_bytes_long_for_security_reasons!!",
    )
    .build()
    .unwrap();

    let router = Router::new()
        .hoop(session_handler)
        .push(Router::with_path("login").post(login))
        .push(Router::with_path("profile").get(profile));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}

#[handler]
async fn login(depot: &mut Depot) -> StatusCode {
    let session = depot.session_mut().unwrap();
    session.insert("user_id", 123).unwrap();
    StatusCode::OK
}

#[handler]
async fn profile(depot: &mut Depot) -> Result<String, StatusError> {
    let session = depot.session().unwrap();
    let user_id: Option<i64> = session.get("user_id");

    match user_id {
        Some(id) => Ok(format!("User ID: {}", id)),
        None => Err(StatusError::unauthorized()),
    }
}
```

## Role-Based Access Control (RBAC)

```rust
#[derive(Clone)]
enum Role {
    Admin,
    User,
    Guest,
}

#[handler]
fn require_role(required: Role) -> impl Handler {
    move |depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl| async move {
        let user_role = depot.get::<Role>("user_role");

        match user_role {
            Some(role) if matches!((role, &required), (Role::Admin, _) | (Role::User, Role::User)) => {
                ctrl.call_next(req, depot, res).await;
            }
            _ => {
                res.status_code(StatusCode::FORBIDDEN);
                res.render("Insufficient permissions");
                ctrl.skip_rest();
                return;
            }
        }
    }
    check_role
}

let router = Router::new()
    .push(
        Router::with_path("admin")
            .hoop(auth_middleware)
            .hoop(RequireRole::new(Role::Admin))
            .get(admin_handler)
    )
    .push(
        Router::with_path("user")
            .hoop(auth_middleware)
            .hoop(require_role(Role::User))
            .get(user_handler)
    );
```

## JWT with Refresh Tokens

```rust
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct RefreshRequest {
    refresh_token: String,
}

#[derive(Serialize)]
struct TokenResponse {
    access_token: String,
    refresh_token: String,
    expires_in: i64,
}

#[handler]
async fn refresh_token(body: JsonBody<RefreshRequest>) -> Result<Json<TokenResponse>, StatusError> {
    let req = body.into_inner();

    // Validate refresh token (check database/cache)
    let user_id = validate_refresh_token(&req.refresh_token)
        .map_err(|_| StatusError::unauthorized())?;

    // Generate new tokens
    let access_claims = JwtClaims {
        sub: user_id.to_string(),
        exp: (chrono::Utc::now() + chrono::Duration::minutes(15)).timestamp(),
        role: "user".to_string(),
    };

    let access_token = encode(
        &Header::default(),
        &access_claims,
        &EncodingKey::from_secret(SECRET_KEY.as_bytes()),
    )
    .map_err(|_| StatusError::internal_server_error())?;

    // Generate new refresh token and store it
    let refresh_token = generate_refresh_token();

    Ok(Json(TokenResponse {
        access_token,
        refresh_token,
        expires_in: 900, // 15 minutes
    }))
}
```

## Complete Authentication Example

```rust
use salvo::prelude::*;
use salvo::jwt_auth::{ConstDecoder, JwtAuth, HeaderFinder, JwtAuthDepotExt};
use jsonwebtoken::{encode, EncodingKey, Header};
use serde::{Deserialize, Serialize};

const SECRET_KEY: &str = "your-secret-key-at-least-32-bytes";

#[derive(Debug, Serialize, Deserialize)]
struct JwtClaims {
    sub: String,
    exp: i64,
}

#[derive(Deserialize)]
struct LoginRequest {
    username: String,
    password: String,
}

#[derive(Serialize)]
struct LoginResponse {
    token: String,
}

#[handler]
async fn login(body: JsonBody<LoginRequest>) -> Result<Json<LoginResponse>, StatusError> {
    let req = body.into_inner();

    if req.username != "admin" || req.password != "password" {
        return Err(StatusError::unauthorized());
    }

    let claims = JwtClaims {
        sub: req.username,
        exp: (chrono::Utc::now() + chrono::Duration::hours(24)).timestamp(),
    };

    let token = encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(SECRET_KEY.as_bytes()),
    )
    .map_err(|_| StatusError::internal_server_error())?;

    Ok(Json(LoginResponse { token }))
}

#[handler]
async fn protected(depot: &mut Depot) -> Result<String, StatusError> {
    let data = depot.jwt_auth_data::<JwtClaims>()
        .ok_or_else(|| StatusError::unauthorized())?;
    Ok(format!("Welcome, {}!", data.claims.sub))
}

#[tokio::main]
async fn main() {
    let auth: JwtAuth<JwtClaims, _> = JwtAuth::new(ConstDecoder::from_secret(SECRET_KEY.as_bytes()))
        .finders(vec![Box::new(HeaderFinder::new())]);

    let router = Router::new()
        .push(Router::with_path("login").post(login))
        .push(
            Router::with_path("protected")
                .hoop(auth)
                .get(protected)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. Never store passwords in plain text - use bcrypt or argon2
2. Use strong secret keys (at least 32 bytes for HMAC, 64 bytes for sessions)
3. Set appropriate token expiration times (15 min for access, days for refresh)
4. Use HTTPS in production
5. Implement rate limiting for login endpoints
6. Store sensitive data in environment variables
7. Validate tokens on every protected request
8. Use refresh tokens for long-lived sessions
9. Implement proper logout functionality (token revocation)
10. Log authentication failures for security monitoring
