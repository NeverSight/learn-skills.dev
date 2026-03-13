---
name: salvo-session
description: Implement session management for user state persistence. Use for login systems, shopping carts, and user preferences.
---

# Salvo Session Management

This skill helps implement session management in Salvo applications for maintaining user state across requests.

## What are Sessions?

Sessions allow you to store user-specific data (like login status, shopping cart contents, preferences) on the server side, with a session ID stored in a cookie on the client.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["session"] }
```

## Basic Session Setup

```rust
use salvo::prelude::*;
use salvo::session::{CookieStore, Session, SessionDepotExt, SessionHandler};

#[tokio::main]
async fn main() {
    // Create session handler with cookie store
    // Secret key must be 64 bytes for security
    let session_handler = SessionHandler::builder(
        CookieStore::new(),
        b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
    )
    .build()
    .unwrap();

    let router = Router::new()
        .hoop(session_handler)
        .get(home)
        .push(Router::with_path("login").get(login).post(login))
        .push(Router::with_path("logout").get(logout));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Session Operations

### Creating a Session

```rust
use salvo::session::{Session, SessionDepotExt};

#[handler]
async fn login(req: &mut Request, depot: &mut Depot, res: &mut Response) {
    if req.method() == salvo::http::Method::POST {
        let username = req.form::<String>("username").await.unwrap();

        // Create new session
        let mut session = Session::new();
        session.insert("username", username).unwrap();
        session.insert("logged_in", true).unwrap();

        // Set session in depot
        depot.set_session(session);

        res.render(Redirect::other("/"));
    } else {
        res.render(Text::Html(LOGIN_FORM));
    }
}
```

### Reading Session Data

```rust
#[handler]
async fn home(depot: &mut Depot, res: &mut Response) {
    if let Some(session) = depot.session_mut() {
        if let Some(username) = session.get::<String>("username") {
            res.render(Text::Html(format!("Hello, {}!", username)));
            return;
        }
    }
    res.render(Text::Html("Please login"));
}
```

### Updating Session Data

```rust
#[handler]
async fn update_preferences(depot: &mut Depot, res: &mut Response) {
    if let Some(session) = depot.session_mut() {
        // Update existing value
        session.insert("theme", "dark").unwrap();

        // Increment a counter
        let visits: i32 = session.get("visits").unwrap_or(0);
        session.insert("visits", visits + 1).unwrap();
    }
    res.render("Preferences updated");
}
```

### Removing Session Data

```rust
#[handler]
async fn logout(depot: &mut Depot, res: &mut Response) {
    if let Some(session) = depot.session_mut() {
        // Remove specific key
        session.remove("username");

        // Or clear all session data
        // session.clear();
    }
    res.render(Redirect::other("/"));
}
```

## Session Stores

### Cookie Store (Default)

Stores session data encrypted in cookies. Simple, no external dependencies.

```rust
use salvo::session::CookieStore;

let session_handler = SessionHandler::builder(
    CookieStore::new(),
    b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
)
.build()
.unwrap();
```

### Memory Store

Stores sessions in memory. Fast but lost on restart.

```rust
use salvo::session::MemoryStore;

let session_handler = SessionHandler::builder(
    MemoryStore::new(),
    b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
)
.build()
.unwrap();
```

## Session Configuration

```rust
use std::time::Duration;
use salvo::session::{CookieStore, SessionHandler};

let session_handler = SessionHandler::builder(
    CookieStore::new(),
    b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
)
// Session expiration time
.session_ttl(Some(Duration::from_secs(3600))) // 1 hour
// Cookie name
.cookie_name("session_id")
// Cookie path
.cookie_path("/")
// Cookie domain (optional)
// .cookie_domain("example.com")
// Secure cookie (HTTPS only)
.cookie_secure(true)
// HTTP only (no JavaScript access)
.cookie_http_only(true)
// Same site policy
.cookie_same_site(salvo::http::cookie::SameSite::Strict)
.build()
.unwrap();
```

## Complete Login Example

```rust
use salvo::prelude::*;
use salvo::session::{CookieStore, Session, SessionDepotExt, SessionHandler};

#[handler]
async fn home(depot: &mut Depot, res: &mut Response) {
    let content = if let Some(session) = depot.session_mut()
        && let Some(username) = session.get::<String>("username")
    {
        format!(r#"
            <h1>Welcome, {username}!</h1>
            <p><a href="/logout">Logout</a></p>
        "#)
    } else {
        r#"
            <h1>Welcome, Guest!</h1>
            <p><a href="/login">Login</a></p>
        "#.to_string()
    };
    res.render(Text::Html(content));
}

#[handler]
async fn login(req: &mut Request, depot: &mut Depot, res: &mut Response) {
    if req.method() == salvo::http::Method::POST {
        let username = req.form::<String>("username").await.unwrap_or_default();
        let password = req.form::<String>("password").await.unwrap_or_default();

        // Validate credentials (example only)
        if username == "admin" && password == "password" {
            let mut session = Session::new();
            session.insert("username", username).unwrap();
            session.insert("role", "admin").unwrap();
            depot.set_session(session);
            res.render(Redirect::other("/"));
        } else {
            res.render(Text::Html("Invalid credentials. <a href='/login'>Try again</a>"));
        }
    } else {
        res.render(Text::Html(r#"
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Login</h1>
                <form method="post">
                    <p><input type="text" name="username" placeholder="Username" /></p>
                    <p><input type="password" name="password" placeholder="Password" /></p>
                    <button type="submit">Login</button>
                </form>
            </body>
            </html>
        "#));
    }
}

#[handler]
async fn logout(depot: &mut Depot, res: &mut Response) {
    if let Some(session) = depot.session_mut() {
        session.remove("username");
        session.remove("role");
    }
    res.render(Redirect::other("/"));
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().init();

    let session_handler = SessionHandler::builder(
        CookieStore::new(),
        b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
    )
    .build()
    .unwrap();

    let router = Router::new()
        .hoop(session_handler)
        .get(home)
        .push(Router::with_path("login").get(login).post(login))
        .push(Router::with_path("logout").get(logout));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Session with Authentication Middleware

```rust
use salvo::prelude::*;
use salvo::session::SessionDepotExt;

#[handler]
async fn require_login(
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let logged_in = depot
        .session_mut()
        .and_then(|s| s.get::<bool>("logged_in"))
        .unwrap_or(false);

    if !logged_in {
        res.render(Redirect::other("/login"));
        ctrl.skip_rest();
    }
}

#[handler]
async fn require_admin(
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    let is_admin = depot
        .session_mut()
        .and_then(|s| s.get::<String>("role"))
        .map(|r| r == "admin")
        .unwrap_or(false);

    if !is_admin {
        res.status_code(StatusCode::FORBIDDEN);
        res.render("Admin access required");
        ctrl.skip_rest();
    }
}

#[tokio::main]
async fn main() {
    let session_handler = SessionHandler::builder(
        CookieStore::new(),
        b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
    )
    .build()
    .unwrap();

    let router = Router::new()
        .hoop(session_handler)
        .get(home)
        .push(Router::with_path("login").get(login).post(login))
        .push(
            Router::with_path("dashboard")
                .hoop(require_login)
                .get(dashboard)
        )
        .push(
            Router::with_path("admin")
                .hoop(require_login)
                .hoop(require_admin)
                .get(admin_panel)
        );
}
```

## Shopping Cart Example

```rust
use salvo::prelude::*;
use salvo::session::{Session, SessionDepotExt};
use serde::{Deserialize, Serialize};

#[derive(Clone, Serialize, Deserialize)]
struct CartItem {
    product_id: u32,
    name: String,
    quantity: u32,
    price: f64,
}

#[handler]
async fn add_to_cart(req: &mut Request, depot: &mut Depot, res: &mut Response) {
    let product_id: u32 = req.param("id").unwrap();

    let session = depot.session_mut().unwrap();
    let mut cart: Vec<CartItem> = session.get("cart").unwrap_or_default();

    // Add or update item
    if let Some(item) = cart.iter_mut().find(|i| i.product_id == product_id) {
        item.quantity += 1;
    } else {
        cart.push(CartItem {
            product_id,
            name: format!("Product {}", product_id),
            quantity: 1,
            price: 9.99,
        });
    }

    session.insert("cart", cart).unwrap();
    res.render(Redirect::other("/cart"));
}

#[handler]
async fn view_cart(depot: &mut Depot, res: &mut Response) {
    let cart: Vec<CartItem> = depot
        .session_mut()
        .and_then(|s| s.get("cart"))
        .unwrap_or_default();

    let total: f64 = cart.iter().map(|i| i.price * i.quantity as f64).sum();

    res.render(Json(serde_json::json!({
        "items": cart,
        "total": total
    })));
}

#[handler]
async fn clear_cart(depot: &mut Depot, res: &mut Response) {
    if let Some(session) = depot.session_mut() {
        session.remove("cart");
    }
    res.render(Redirect::other("/cart"));
}
```

## Best Practices

1. **Use secure secret keys**: Generate 64 random bytes for session encryption
2. **Set appropriate TTL**: Balance security with user convenience
3. **Use HTTPS**: Always use secure cookies in production
4. **Set HttpOnly**: Prevent JavaScript access to session cookies
5. **Use SameSite**: Protect against CSRF attacks
6. **Validate session data**: Don't trust session data blindly
7. **Regenerate session on login**: Prevent session fixation attacks
8. **Clean up on logout**: Remove all sensitive session data
