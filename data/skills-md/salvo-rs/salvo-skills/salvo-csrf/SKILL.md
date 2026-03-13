---
name: salvo-csrf
description: Implement CSRF (Cross-Site Request Forgery) protection using cookie or session storage. Use for protecting forms and state-changing endpoints.
---

# Salvo CSRF Protection

This skill helps implement CSRF protection in Salvo applications to prevent cross-site request forgery attacks.

## What is CSRF?

Cross-Site Request Forgery (CSRF) is an attack that tricks users into executing unwanted actions on a web application where they're authenticated. CSRF protection ensures that form submissions come from your own site.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["csrf"] }
```

## CSRF Protection Methods

Salvo provides four cryptographic methods for CSRF token generation:

| Method | Description | Performance |
|--------|-------------|-------------|
| Bcrypt | Slow hashing, no key needed | Slowest |
| HMAC | Fast, requires 32-byte key | Fast |
| AES-GCM | Authenticated encryption, 32-byte key | Fast |
| ChaCha20Poly1305 | Modern encryption, 32-byte key | Fast |

## Basic CSRF with Cookie Store

```rust
use salvo::csrf::*;
use salvo::prelude::*;
use serde::Deserialize;

#[derive(Deserialize)]
struct FormData {
    csrf_token: String,
    message: String,
}

#[handler]
async fn show_form(depot: &mut Depot, res: &mut Response) {
    let token = depot.csrf_token().unwrap_or_default();
    res.render(Text::Html(format!(r#"
        <form method="post">
            <input type="hidden" name="csrf_token" value="{token}" />
            <input type="text" name="message" />
            <button type="submit">Submit</button>
        </form>
    "#)));
}

#[handler]
async fn handle_form(req: &mut Request, res: &mut Response) {
    let data = req.parse_form::<FormData>().await.unwrap();
    res.render(format!("Message received: {}", data.message));
}

#[tokio::main]
async fn main() {
    // Configure where to find CSRF token in requests
    let form_finder = FormFinder::new("csrf_token");

    // Create CSRF handler with bcrypt (no key required)
    let csrf_handler = bcrypt_cookie_csrf(form_finder);

    let router = Router::new()
        .hoop(csrf_handler)
        .get(show_form)
        .post(handle_form);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## CSRF Methods with Cookie Store

### Bcrypt (No Key Required)

```rust
use salvo::csrf::{bcrypt_cookie_csrf, FormFinder};

let form_finder = FormFinder::new("csrf_token");
let csrf_handler = bcrypt_cookie_csrf(form_finder);
```

### HMAC (32-byte Key)

```rust
use salvo::csrf::{hmac_cookie_csrf, FormFinder};

let key = *b"01234567012345670123456701234567"; // 32 bytes
let form_finder = FormFinder::new("csrf_token");
let csrf_handler = hmac_cookie_csrf(key, form_finder);
```

### AES-GCM (32-byte Key)

```rust
use salvo::csrf::{aes_gcm_cookie_csrf, FormFinder};

let key = *b"01234567012345670123456701234567"; // 32 bytes
let form_finder = FormFinder::new("csrf_token");
let csrf_handler = aes_gcm_cookie_csrf(key, form_finder);
```

### ChaCha20Poly1305 (32-byte Key)

```rust
use salvo::csrf::{ccp_cookie_csrf, FormFinder};

let key = *b"01234567012345670123456701234567"; // 32 bytes
let form_finder = FormFinder::new("csrf_token");
let csrf_handler = ccp_cookie_csrf(key, form_finder);
```

## CSRF with Session Store

For session-based CSRF storage, combine with SessionHandler:

```rust
use salvo::csrf::*;
use salvo::session::{CookieStore, SessionHandler};
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    // Session handler (required for session-based CSRF)
    let session_handler = SessionHandler::builder(
        CookieStore::new(),
        b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
    )
    .build()
    .unwrap();

    let form_finder = FormFinder::new("csrf_token");

    // Use session-based CSRF storage
    let csrf_handler = bcrypt_session_csrf(form_finder);

    let router = Router::new()
        .hoop(session_handler)  // Session must come first
        .hoop(csrf_handler)
        .get(show_form)
        .post(handle_form);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

### Session Store Methods

```rust
// Bcrypt
let csrf = bcrypt_session_csrf(form_finder);

// HMAC
let csrf = hmac_session_csrf(key, form_finder);

// AES-GCM
let csrf = aes_gcm_session_csrf(key, form_finder);

// ChaCha20Poly1305
let csrf = ccp_session_csrf(key, form_finder);
```

## Token Finders

### Form Finder (POST Body)

```rust
use salvo::csrf::FormFinder;

// Look for "csrf_token" in form data
let finder = FormFinder::new("csrf_token");
```

### Header Finder

```rust
use salvo::csrf::HeaderFinder;

// Look for "X-CSRF-Token" header
let finder = HeaderFinder::new("X-CSRF-Token");
```

### Query Finder

```rust
use salvo::csrf::QueryFinder;

// Look for "csrf_token" in query string
let finder = QueryFinder::new("csrf_token");
```

## Getting CSRF Token

Use `CsrfDepotExt` to get the CSRF token in handlers:

```rust
use salvo::csrf::CsrfDepotExt;

#[handler]
async fn show_form(depot: &mut Depot, res: &mut Response) {
    // Get CSRF token for the form
    let token = depot.csrf_token().unwrap_or_default();

    res.render(Text::Html(format!(r#"
        <form method="post">
            <input type="hidden" name="csrf_token" value="{token}" />
            <!-- form fields -->
        </form>
    "#)));
}
```

## Multiple CSRF Methods

Apply different CSRF methods to different routes:

```rust
let form_finder = FormFinder::new("csrf_token");

let bcrypt_csrf = bcrypt_cookie_csrf(form_finder.clone());
let hmac_csrf = hmac_cookie_csrf(*b"01234567012345670123456701234567", form_finder.clone());

let router = Router::new()
    .push(
        Router::with_hoop(bcrypt_csrf)
            .path("forms")
            .get(show_form)
            .post(handle_form)
    )
    .push(
        Router::with_hoop(hmac_csrf)
            .path("api")
            .get(get_token)
            .post(api_handler)
    );
```

## CSRF for AJAX Requests

For AJAX/fetch requests, use header-based CSRF:

```rust
use salvo::csrf::{HeaderFinder, hmac_cookie_csrf};

let header_finder = HeaderFinder::new("X-CSRF-Token");
let csrf_handler = hmac_cookie_csrf(*b"01234567012345670123456701234567", header_finder);

// Client JavaScript:
// fetch('/api', {
//     method: 'POST',
//     headers: { 'X-CSRF-Token': token },
//     body: JSON.stringify(data)
// });
```

## Complete Example

```rust
use salvo::csrf::*;
use salvo::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct FormData {
    csrf_token: String,
    message: String,
}

#[handler]
async fn index(res: &mut Response) {
    res.render(Text::Html(r#"
        <h1>CSRF Protection Demo</h1>
        <ul>
            <li><a href="/form">Protected Form</a></li>
        </ul>
    "#));
}

#[handler]
async fn show_form(depot: &mut Depot, res: &mut Response) {
    let token = depot.csrf_token().unwrap_or_default();
    res.render(Text::Html(format!(r#"
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Submit Message</h2>
            <form method="post">
                <input type="hidden" name="csrf_token" value="{token}" />
                <label>Message: <input type="text" name="message" /></label>
                <button type="submit">Send</button>
            </form>
        </body>
        </html>
    "#)));
}

#[handler]
async fn handle_form(req: &mut Request, depot: &mut Depot, res: &mut Response) {
    match req.parse_form::<FormData>().await {
        Ok(data) => {
            // Generate new token for next request
            let new_token = depot.csrf_token().unwrap_or_default();
            res.render(Text::Html(format!(
                "Received: {} <br><a href='/form'>Back</a>",
                data.message
            )));
        }
        Err(e) => {
            res.status_code(StatusCode::BAD_REQUEST);
            res.render(format!("Error: {}", e));
        }
    }
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().init();

    let form_finder = FormFinder::new("csrf_token");
    let csrf_handler = hmac_cookie_csrf(
        *b"01234567012345670123456701234567",
        form_finder,
    );

    let router = Router::new()
        .get(index)
        .push(
            Router::with_hoop(csrf_handler)
                .path("form")
                .get(show_form)
                .post(handle_form)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. **Use HMAC or AES-GCM in production**: Bcrypt is slow; use faster methods with a secure key
2. **Generate secure keys**: Use cryptographically secure random bytes for keys
3. **Session store for sensitive apps**: Session-based storage is more secure than cookie-based
4. **Include token in all forms**: Every state-changing form needs a CSRF token
5. **Validate on all state-changing requests**: POST, PUT, DELETE, PATCH all need protection
6. **Use SameSite cookies**: Combine CSRF with SameSite=Strict cookies for extra protection
7. **Rotate tokens**: Generate new tokens after successful form submission
