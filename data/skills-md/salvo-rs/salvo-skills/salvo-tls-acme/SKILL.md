---
name: salvo-tls-acme
description: Configure TLS/HTTPS with automatic certificate management via ACME (Let's Encrypt). Use for production deployments with secure connections.
---

# Salvo TLS and ACME Configuration

This skill helps configure TLS/HTTPS and automatic certificate management in Salvo applications.

## TLS with Rustls

### Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["rustls"] }
```

### Basic TLS Configuration

```rust
use salvo::prelude::*;
use salvo::conn::rustls::{Keycert, RustlsConfig};

#[handler]
async fn hello() -> &'static str {
    "Hello over HTTPS!"
}

#[tokio::main]
async fn main() {
    let router = Router::new().get(hello);

    // Load certificate and private key
    let config = RustlsConfig::new(
        Keycert::new()
            .cert_from_path("certs/cert.pem")
            .unwrap()
            .key_from_path("certs/key.pem")
            .unwrap()
    );

    let acceptor = TcpListener::new("0.0.0.0:443")
        .rustls(config)
        .bind()
        .await;

    Server::new(acceptor).serve(router).await;
}
```

### Certificate from Memory

```rust
use salvo::conn::rustls::{Keycert, RustlsConfig};

let cert_pem = include_bytes!("../certs/cert.pem");
let key_pem = include_bytes!("../certs/key.pem");

let config = RustlsConfig::new(
    Keycert::new()
        .cert(cert_pem.to_vec())
        .key(key_pem.to_vec())
);
```

## ACME (Let's Encrypt) Auto-Certificates

### Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["acme"] }
```

### HTTP-01 Challenge

```rust
use salvo::prelude::*;
use salvo::conn::acme::{AcmeConfig, AcmeListener, ChallengeType};

#[handler]
async fn hello() -> &'static str {
    "Hello with auto-certificate!"
}

#[tokio::main]
async fn main() {
    let router = Router::new().get(hello);

    // Configure ACME
    let config = AcmeConfig::builder()
        .domains(["example.com", "www.example.com"])
        .contacts(["mailto:admin@example.com"])
        .challenge_type(ChallengeType::Http01)
        .cache_path("./acme_cache")
        .build()
        .unwrap();

    // ACME listener handles HTTP-01 challenges and serves HTTPS
    let acceptor = AcmeListener::builder()
        .acme_config(config)
        .bind("0.0.0.0:443")
        .await;

    Server::new(acceptor).serve(router).await;
}
```

### TLS-ALPN-01 Challenge

For environments where port 80 is not available:

```rust
use salvo::conn::acme::{AcmeConfig, AcmeListener, ChallengeType};

let config = AcmeConfig::builder()
    .domains(["example.com"])
    .contacts(["mailto:admin@example.com"])
    .challenge_type(ChallengeType::TlsAlpn01)
    .cache_path("./acme_cache")
    .build()
    .unwrap();
```

## Force HTTPS Redirect

```rust
use salvo::prelude::*;

#[handler]
async fn force_https(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    // Check if request is HTTP (not HTTPS)
    if req.uri().scheme_str() == Some("http") {
        let host = req.header::<String>("Host").unwrap_or_default();
        let path = req.uri().path_and_query().map(|p| p.as_str()).unwrap_or("/");
        let https_url = format!("https://{}{}", host, path);

        res.status_code(StatusCode::MOVED_PERMANENTLY);
        res.headers_mut().insert("Location", https_url.parse().unwrap());
        ctrl.skip_rest();
        return;
    }

    ctrl.call_next(req, depot, res).await;
}
```

## HTTP and HTTPS on Different Ports

```rust
use salvo::prelude::*;
use salvo::conn::rustls::{Keycert, RustlsConfig};

#[tokio::main]
async fn main() {
    let router = Router::new().get(hello);

    // HTTPS on 443
    let tls_config = RustlsConfig::new(
        Keycert::new()
            .cert_from_path("certs/cert.pem").unwrap()
            .key_from_path("certs/key.pem").unwrap()
    );

    let https_acceptor = TcpListener::new("0.0.0.0:443")
        .rustls(tls_config)
        .bind()
        .await;

    // HTTP on 80 (for redirects or ACME challenges)
    let http_acceptor = TcpListener::new("0.0.0.0:80")
        .bind()
        .await;

    // Run both servers
    tokio::join!(
        Server::new(https_acceptor).serve(router.clone()),
        Server::new(http_acceptor).serve(Router::new().hoop(redirect_to_https)),
    );
}

#[handler]
async fn redirect_to_https(req: &mut Request, res: &mut Response) {
    let host = req.header::<String>("Host").unwrap_or_default();
    let path = req.uri().path();
    res.render(salvo::writing::Redirect::permanent(format!("https://{}{}", host, path)));
}
```

## Certificate Hot Reload

```rust
use salvo::prelude::*;
use salvo::conn::rustls::{Keycert, RustlsConfig};
use std::sync::Arc;
use tokio::sync::RwLock;

// Reload certificates without restarting
async fn reload_certificates(config: Arc<RwLock<RustlsConfig>>) {
    let new_config = RustlsConfig::new(
        Keycert::new()
            .cert_from_path("certs/cert.pem").unwrap()
            .key_from_path("certs/key.pem").unwrap()
    );

    let mut guard = config.write().await;
    *guard = new_config;
}
```

## HTTP/2 Support

HTTP/2 is automatically enabled when using Rustls:

```rust
use salvo::prelude::*;
use salvo::conn::rustls::{Keycert, RustlsConfig};

// HTTP/2 is enabled by default with TLS
let config = RustlsConfig::new(
    Keycert::new()
        .cert_from_path("certs/cert.pem").unwrap()
        .key_from_path("certs/key.pem").unwrap()
);
```

## HTTP/3 (QUIC) Support

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["quinn"] }
```

```rust
use salvo::prelude::*;
use salvo::conn::quinn::QuinnListener;

#[tokio::main]
async fn main() {
    let router = Router::new().get(hello);

    let acceptor = QuinnListener::builder()
        .cert_path("certs/cert.pem")
        .key_path("certs/key.pem")
        .bind("0.0.0.0:443")
        .await;

    Server::new(acceptor).serve(router).await;
}
```

## Security Headers for HTTPS

```rust
use salvo::prelude::*;

#[handler]
async fn security_headers(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    // HTTP Strict Transport Security
    res.headers_mut().insert(
        "Strict-Transport-Security",
        "max-age=31536000; includeSubDomains; preload".parse().unwrap()
    );

    // Prevent mixed content
    res.headers_mut().insert(
        "Content-Security-Policy",
        "upgrade-insecure-requests".parse().unwrap()
    );

    ctrl.call_next(req, depot, res).await;
}
```

## Complete ACME Example

```rust
use salvo::prelude::*;
use salvo::conn::acme::{AcmeConfig, AcmeListener, ChallengeType};

#[handler]
async fn hello() -> &'static str {
    "Hello with Let's Encrypt!"
}

#[handler]
async fn security_headers(req: &mut Request, depot: &mut Depot, res: &mut Response, ctrl: &mut FlowCtrl) {
    res.headers_mut().insert(
        "Strict-Transport-Security",
        "max-age=31536000; includeSubDomains".parse().unwrap()
    );
    ctrl.call_next(req, depot, res).await;
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .hoop(security_headers)
        .get(hello);

    let acme_config = AcmeConfig::builder()
        .domains(["example.com", "www.example.com"])
        .contacts(["mailto:admin@example.com"])
        .challenge_type(ChallengeType::Http01)
        .cache_path("./acme_cache")
        .directory_url("https://acme-v02.api.letsencrypt.org/directory")
        .build()
        .unwrap();

    let acceptor = AcmeListener::builder()
        .acme_config(acme_config)
        .bind("0.0.0.0:443")
        .await;

    println!("Server running on https://example.com");
    Server::new(acceptor).serve(router).await;
}
```

## Staging Environment

Use Let's Encrypt staging for testing:

```rust
let acme_config = AcmeConfig::builder()
    .domains(["example.com"])
    .contacts(["mailto:admin@example.com"])
    .directory_url("https://acme-staging-v02.api.letsencrypt.org/directory")  // Staging
    .build()
    .unwrap();
```

## Best Practices

1. **Use ACME in production**: Automatic certificate renewal
2. **Set HSTS header**: Force browsers to use HTTPS
3. **Enable HTTP/2**: Better performance with TLS
4. **Test with staging**: Use Let's Encrypt staging before production
5. **Cache certificates**: Persist to disk for restart recovery
6. **Monitor expiration**: Alert before certificates expire
7. **Redirect HTTP to HTTPS**: Don't serve content over HTTP
8. **Use strong ciphers**: Let Rustls handle cipher selection
