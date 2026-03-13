---
name: salvo-static-files
description: Serve static files, directories, and embedded assets. Use for CSS, JavaScript, images, and downloadable content.
---

# Salvo Static File Serving

This skill helps serve static files in Salvo applications, including directories, single files, and embedded assets.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["serve-static"] }

# For embedded files
rust-embed = "8"
```

## Serving a Directory

```rust
use salvo::prelude::*;
use salvo::serve_static::StaticDir;

#[tokio::main]
async fn main() {
    let router = Router::with_path("{*path}").get(
        StaticDir::new(["static", "public"])  // Multiple fallback directories
            .defaults("index.html")            // Default file for directories
            .auto_list(true)                   // Enable directory listing
    );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## StaticDir Options

```rust
use salvo::serve_static::StaticDir;

let static_handler = StaticDir::new(["static"])
    // Default file when accessing directories
    .defaults("index.html")
    // Enable directory listing
    .auto_list(true)
    // Include hidden files (starting with .)
    .include_dot_files(false)
    // Set cache control headers
    .cache_control("max-age=3600");
```

## Serving a Single File

```rust
use salvo::prelude::*;
use salvo::serve_static::StaticFile;

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("favicon.ico").get(StaticFile::new("static/favicon.ico")))
        .push(Router::with_path("robots.txt").get(StaticFile::new("static/robots.txt")));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Embedded Static Files

Embed files at compile time for single-binary deployment:

```rust
use rust_embed::RustEmbed;
use salvo::prelude::*;
use salvo::serve_static::static_embed;

#[derive(RustEmbed)]
#[folder = "static"]  // Folder to embed
struct Assets;

#[tokio::main]
async fn main() {
    let router = Router::with_path("{*path}").get(
        static_embed::<Assets>()
            .fallback("index.html")  // SPA fallback
    );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Combined API and Static Files

```rust
use salvo::prelude::*;
use salvo::serve_static::StaticDir;

#[handler]
async fn api_users() -> Json<Vec<String>> {
    Json(vec!["Alice".to_string(), "Bob".to_string()])
}

#[handler]
async fn api_posts() -> Json<Vec<String>> {
    Json(vec!["Post 1".to_string(), "Post 2".to_string()])
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        // API routes
        .push(
            Router::with_path("api")
                .push(Router::with_path("users").get(api_users))
                .push(Router::with_path("posts").get(api_posts))
        )
        // Static files for everything else
        .push(
            Router::with_path("{*path}").get(
                StaticDir::new(["static"])
                    .defaults("index.html")
            )
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## SPA (Single Page Application) Support

```rust
use rust_embed::RustEmbed;
use salvo::prelude::*;
use salvo::serve_static::static_embed;

#[derive(RustEmbed)]
#[folder = "dist"]  // Vue/React build output
struct Assets;

#[tokio::main]
async fn main() {
    let router = Router::new()
        // API routes first
        .push(Router::with_path("api/{**rest}").get(api_handler))
        // SPA - serve index.html for all other routes
        .push(
            Router::with_path("{*path}").get(
                static_embed::<Assets>()
                    .fallback("index.html")  // All routes fall back to index.html
            )
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Serving Different Asset Types

```rust
use salvo::prelude::*;
use salvo::serve_static::StaticDir;

#[tokio::main]
async fn main() {
    let router = Router::new()
        // CSS files
        .push(
            Router::with_path("css/{*path}").get(
                StaticDir::new(["static/css"])
                    .cache_control("max-age=31536000")  // 1 year for hashed assets
            )
        )
        // JavaScript files
        .push(
            Router::with_path("js/{*path}").get(
                StaticDir::new(["static/js"])
                    .cache_control("max-age=31536000")
            )
        )
        // Images
        .push(
            Router::with_path("images/{*path}").get(
                StaticDir::new(["static/images"])
                    .cache_control("max-age=86400")  // 1 day
            )
        )
        // Uploads (user content, no long cache)
        .push(
            Router::with_path("uploads/{*path}").get(
                StaticDir::new(["uploads"])
                    .cache_control("max-age=3600")  // 1 hour
            )
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## File Downloads

```rust
use salvo::prelude::*;
use salvo::fs::NamedFile;

#[handler]
async fn download_file(req: &mut Request, res: &mut Response) {
    let filename: String = req.param("filename").unwrap();
    let file_path = format!("downloads/{}", filename);

    // Serve file with download headers
    match NamedFile::builder(&file_path)
        .attached_name(&filename)  // Forces download with filename
        .send(req.headers(), res)
        .await
    {
        Ok(_) => {}
        Err(_) => {
            res.status_code(StatusCode::NOT_FOUND);
            res.render("File not found");
        }
    }
}

#[handler]
async fn view_pdf(req: &mut Request, res: &mut Response) {
    // Serve PDF for viewing in browser (not download)
    match NamedFile::builder("documents/report.pdf")
        .content_type("application/pdf")
        .send(req.headers(), res)
        .await
    {
        Ok(_) => {}
        Err(_) => {
            res.status_code(StatusCode::NOT_FOUND);
        }
    }
}
```

## Directory Listing

```rust
use salvo::prelude::*;
use salvo::serve_static::StaticDir;

#[tokio::main]
async fn main() {
    let router = Router::with_path("{*path}").get(
        StaticDir::new(["files"])
            .auto_list(true)           // Enable directory listing
            .include_dot_files(false)  // Hide hidden files
            .defaults("index.html")    // Show index.html if exists
    );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Conditional Static Serving

```rust
use salvo::prelude::*;
use salvo::serve_static::StaticDir;

#[handler]
async fn check_auth(
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl,
) {
    // Check if user is authenticated for protected files
    let is_authenticated = depot
        .session_mut()
        .and_then(|s| s.get::<bool>("logged_in"))
        .unwrap_or(false);

    if !is_authenticated {
        res.status_code(StatusCode::UNAUTHORIZED);
        res.render("Please login to access files");
        ctrl.skip_rest();
    }
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        // Public static files
        .push(
            Router::with_path("public/{*path}").get(
                StaticDir::new(["static/public"])
            )
        )
        // Protected static files
        .push(
            Router::with_path("private/{*path}")
                .hoop(check_auth)
                .get(StaticDir::new(["static/private"]))
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Multiple Fallback Directories

```rust
use salvo::serve_static::StaticDir;

// Try directories in order
let static_handler = StaticDir::new([
    "static/overrides",  // Custom overrides first
    "static/default",    // Default files second
    "node_modules",      // npm packages last
])
.defaults("index.html");
```

## Embedded Assets with Custom Handling

```rust
use rust_embed::RustEmbed;
use salvo::prelude::*;

#[derive(RustEmbed)]
#[folder = "static"]
struct Assets;

#[handler]
async fn custom_static(req: &mut Request, res: &mut Response) {
    let path = req.param::<String>("path").unwrap_or_default();

    match Assets::get(&path) {
        Some(content) => {
            // Determine content type
            let content_type = mime_guess::from_path(&path)
                .first_or_octet_stream()
                .to_string();

            res.headers_mut()
                .insert("Content-Type", content_type.parse().unwrap());

            // Add caching for production
            if path.contains(".") {  // Has extension = asset
                res.headers_mut()
                    .insert("Cache-Control", "max-age=31536000".parse().unwrap());
            }

            res.write_body(content.data.to_vec()).ok();
        }
        None => {
            // SPA fallback
            if let Some(index) = Assets::get("index.html") {
                res.headers_mut()
                    .insert("Content-Type", "text/html".parse().unwrap());
                res.write_body(index.data.to_vec()).ok();
            } else {
                res.status_code(StatusCode::NOT_FOUND);
            }
        }
    }
}
```

## Complete Production Example

```rust
use rust_embed::RustEmbed;
use salvo::prelude::*;
use salvo::serve_static::{StaticDir, static_embed};
use salvo::compression::Compression;

#[derive(RustEmbed)]
#[folder = "dist"]
struct Assets;

#[handler]
async fn api_handler() -> &'static str {
    "API Response"
}

#[tokio::main]
async fn main() {
    // Compression for all responses
    let compression = Compression::new()
        .enable_gzip(flate2::Compression::default())
        .enable_brotli(11);

    let router = Router::new()
        .hoop(compression)
        // API routes
        .push(
            Router::with_path("api")
                .push(Router::with_path("data").get(api_handler))
        )
        // Uploads (not embedded)
        .push(
            Router::with_path("uploads/{*path}").get(
                StaticDir::new(["uploads"])
                    .cache_control("max-age=3600")
            )
        )
        // Embedded static files with SPA support
        .push(
            Router::with_path("{*path}").get(
                static_embed::<Assets>()
                    .fallback("index.html")
            )
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. **Use embedded files for deployment**: Single binary is easier to deploy
2. **Set cache headers**: Long cache for hashed assets, short for dynamic content
3. **Enable compression**: Serve gzip/brotli compressed files
4. **SPA fallback**: Return index.html for client-side routing
5. **Separate API from static**: Use distinct paths for API and static content
6. **Security**: Don't expose sensitive files, check paths
7. **Directory listing**: Disable in production unless intentional
8. **Multiple directories**: Use fallback order for themes/overrides
