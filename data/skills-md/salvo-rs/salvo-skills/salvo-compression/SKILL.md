---
name: salvo-compression
description: Compress HTTP responses using gzip, brotli, zstd, or deflate. Use for reducing bandwidth and improving load times.
---

# Salvo Response Compression

This skill helps configure response compression in Salvo applications.

## HTTP Compression Basics

HTTP compression reduces response size by compressing content before sending. The process:

1. Client sends `Accept-Encoding: gzip, deflate, br` header
2. Server compresses response and sets `Content-Encoding: gzip` header
3. Client automatically decompresses the response

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["compression"] }
```

## Basic Usage

```rust
use salvo::prelude::*;
use salvo::compression::Compression;

#[handler]
async fn large_response() -> String {
    "This response will be compressed if the client supports it. ".repeat(100)
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .hoop(Compression::new())  // Enable compression
        .get(large_response);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Supported Algorithms

Salvo supports four compression algorithms:

| Algorithm | Feature | Description |
|-----------|---------|-------------|
| **Gzip** | Default | Most widely supported, good balance |
| **Brotli (br)** | Default | Best compression ratio, higher CPU |
| **Zstd** | Default | Fast with good compression |
| **Deflate** | Default | Legacy, rarely used alone |

## Configuring Specific Algorithms

```rust
use salvo::compression::{Compression, CompressionLevel};

// Only gzip
let gzip_only = Compression::new()
    .enable_gzip(CompressionLevel::Default);

// Only brotli
let brotli_only = Compression::new()
    .enable_brotli(CompressionLevel::Best);

// Multiple algorithms
let multi = Compression::new()
    .enable_gzip(CompressionLevel::Default)
    .enable_brotli(CompressionLevel::Default)
    .enable_zstd(CompressionLevel::Default);
```

## Compression Levels

```rust
use salvo::compression::CompressionLevel;

// Available levels
CompressionLevel::Fastest  // Fastest speed, lower compression
CompressionLevel::Default  // Balanced speed and compression
CompressionLevel::Best     // Best compression, slower
CompressionLevel::Precise(6)  // Exact level (algorithm-specific)
```

### Level Selection Guide

| Use Case | Recommended Level |
|----------|-------------------|
| Dynamic API responses | `Fastest` |
| Static assets | `Best` |
| General purpose | `Default` |

## Minimum Response Size

Small responses may become larger after compression. Set a minimum threshold:

```rust
let compression = Compression::new()
    .min_length(1024);  // Only compress responses > 1KB
```

## Content Type Filtering

Only compress text-based content (default behavior):

```rust
let compression = Compression::new()
    .content_types(vec![
        "text/html",
        "text/css",
        "text/javascript",
        "application/json",
        "application/xml",
        "image/svg+xml",
    ]);
```

## Algorithm Priority

When client supports multiple algorithms, set server preference:

```rust
let compression = Compression::new()
    .force_priority(true);  // Use server's priority order

// Default priority: Brotli > Zstd > Gzip > Deflate
```

## Different Routes, Different Compression

```rust
use salvo::compression::{Compression, CompressionLevel};
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    // High compression for static assets
    let static_compression = Compression::new()
        .enable_brotli(CompressionLevel::Best)
        .enable_gzip(CompressionLevel::Best);

    // Fast compression for API
    let api_compression = Compression::new()
        .enable_gzip(CompressionLevel::Fastest)
        .min_length(256);

    let router = Router::new()
        .push(
            Router::with_path("static")
                .hoop(static_compression)
                .get(StaticDir::new("./public"))
        )
        .push(
            Router::with_path("api")
                .hoop(api_compression)
                .get(api_handler)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Pre-compressed Static Files

For best performance, pre-compress static files at build time:

```bash
# Pre-compress with gzip
gzip -k -9 ./public/bundle.js

# Pre-compress with brotli
brotli -k ./public/bundle.js
```

Then serve with static file handler that detects pre-compressed files.

## Complete Example

```rust
use salvo::compression::{Compression, CompressionLevel};
use salvo::prelude::*;
use serde::Serialize;

#[derive(Serialize)]
struct LargeResponse {
    items: Vec<String>,
}

#[handler]
async fn large_json() -> Json<LargeResponse> {
    Json(LargeResponse {
        items: (0..1000).map(|i| format!("Item {}", i)).collect(),
    })
}

#[handler]
async fn html_page() -> Text<&'static str> {
    Text::Html(r#"
        <!DOCTYPE html>
        <html>
        <head><title>Compressed Page</title></head>
        <body>
            <h1>This page is compressed!</h1>
            <p>The server compresses this HTML before sending it.</p>
        </body>
        </html>
    "#)
}

#[tokio::main]
async fn main() {
    let compression = Compression::new()
        .enable_gzip(CompressionLevel::Default)
        .enable_brotli(CompressionLevel::Default)
        .min_length(512)
        .content_types(vec![
            "text/html",
            "text/css",
            "application/json",
            "application/javascript",
        ]);

    let router = Router::new()
        .hoop(compression)
        .push(Router::with_path("api/data").get(large_json))
        .push(Router::with_path("page").get(html_page));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Testing Compression

```bash
# Request with gzip support
curl -H "Accept-Encoding: gzip" -v http://localhost:8080/api/data

# Request with brotli support
curl -H "Accept-Encoding: br" -v http://localhost:8080/api/data

# Check response headers for Content-Encoding
```

## Best Practices

1. **Use compression for text content**: HTML, CSS, JS, JSON, XML
2. **Skip already compressed content**: JPEG, PNG, MP4, ZIP
3. **Set minimum size threshold**: Avoid compressing tiny responses
4. **Choose level based on content type**: Static = Best, Dynamic = Fastest
5. **Pre-compress static assets**: Build-time compression for best performance
6. **Monitor CPU usage**: High compression levels increase CPU load
7. **Test with real clients**: Verify compression works end-to-end
8. **Consider CDN compression**: CDNs often handle compression for you
