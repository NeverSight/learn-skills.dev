---
name: salvo-caching
description: Implement caching strategies for improved performance. Use for reducing database load and speeding up responses.
---

# Salvo Caching Strategies

This skill helps implement caching in Salvo applications for better performance.

## HTTP Cache Headers

Set cache control headers to enable browser and proxy caching:

```rust
use salvo::prelude::*;

#[handler]
async fn cached_response(res: &mut Response) -> &'static str {
    // Cache for 1 hour
    res.headers_mut().insert(
        "Cache-Control",
        "public, max-age=3600".parse().unwrap()
    );

    "This response will be cached by browsers"
}
```

### Cache-Control Directives

```rust
// Public caching (can be cached by proxies)
res.headers_mut().insert("Cache-Control", "public, max-age=3600".parse().unwrap());

// Private caching (only browser can cache)
res.headers_mut().insert("Cache-Control", "private, max-age=3600".parse().unwrap());

// No caching
res.headers_mut().insert("Cache-Control", "no-store".parse().unwrap());

// Stale while revalidate (serve stale while refreshing)
res.headers_mut().insert(
    "Cache-Control",
    "public, max-age=3600, stale-while-revalidate=86400".parse().unwrap()
);
```

## ETag for Validation

```rust
use salvo::prelude::*;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

#[handler]
async fn with_etag(req: &mut Request, res: &mut Response) -> Result<Json<Data>, StatusError> {
    let data = get_data().await?;

    // Generate ETag from content
    let mut hasher = DefaultHasher::new();
    format!("{:?}", data).hash(&mut hasher);
    let etag = format!("\"{}\"", hasher.finish());

    // Check If-None-Match header
    if let Some(if_none_match) = req.header::<String>("If-None-Match") {
        if if_none_match == etag {
            res.status_code(StatusCode::NOT_MODIFIED);
            return Err(StatusError::not_modified());
        }
    }

    res.headers_mut().insert("ETag", etag.parse().unwrap());
    Ok(Json(data))
}
```

## In-Memory Response Cache

```rust
use salvo::prelude::*;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::time::{Duration, Instant};

#[derive(Clone)]
struct CacheEntry {
    data: String,
    expires_at: Instant,
}

#[derive(Clone)]
struct ResponseCache {
    store: Arc<RwLock<HashMap<String, CacheEntry>>>,
    ttl: Duration,
}

impl ResponseCache {
    fn new(ttl: Duration) -> Self {
        Self {
            store: Arc::new(RwLock::new(HashMap::new())),
            ttl,
        }
    }

    fn get(&self, key: &str) -> Option<String> {
        let store = self.store.read().ok()?;
        let entry = store.get(key)?;

        if Instant::now() < entry.expires_at {
            Some(entry.data.clone())
        } else {
            None
        }
    }

    fn set(&self, key: String, data: String) {
        if let Ok(mut store) = self.store.write() {
            store.insert(key, CacheEntry {
                data,
                expires_at: Instant::now() + self.ttl,
            });
        }
    }
}

#[handler]
async fn cache_middleware(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
    ctrl: &mut FlowCtrl
) {
    let cache = depot.obtain::<ResponseCache>().unwrap();
    let cache_key = format!("{}:{}", req.method(), req.uri().path());

    // Try cache first
    if let Some(cached) = cache.get(&cache_key) {
        res.headers_mut().insert("X-Cache", "HIT".parse().unwrap());
        res.render(cached);
        return;
    }

    // Process request
    ctrl.call_next(req, depot, res).await;
    res.headers_mut().insert("X-Cache", "MISS".parse().unwrap());

    // Cache successful responses
    // Note: In production, extract body from response properly
}
```

## Using Moka for Caching

```toml
[dependencies]
moka = { version = "0.12", features = ["future"] }
```

```rust
use salvo::prelude::*;
use moka::future::Cache;
use std::sync::Arc;
use std::time::Duration;

type AppCache = Cache<String, String>;

async fn create_cache() -> AppCache {
    Cache::builder()
        .max_capacity(10_000)
        .time_to_live(Duration::from_secs(300))
        .build()
}

#[handler]
async fn cached_handler(req: &mut Request, depot: &mut Depot) -> Result<String, StatusError> {
    let cache = depot.obtain::<AppCache>().unwrap();
    let key = req.uri().path().to_string();

    // Try cache
    if let Some(cached) = cache.get(&key).await {
        return Ok(cached);
    }

    // Compute result
    let result = expensive_computation().await?;

    // Store in cache
    cache.insert(key, result.clone()).await;

    Ok(result)
}

#[tokio::main]
async fn main() {
    let cache = create_cache().await;

    let router = Router::new()
        .hoop(affix_state::inject(cache))
        .get(cached_handler);

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Database Query Caching

```rust
use salvo::prelude::*;
use moka::future::Cache;
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Clone, Serialize, Deserialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

type UserCache = Cache<i64, User>;

async fn create_user_cache() -> UserCache {
    Cache::builder()
        .max_capacity(1000)
        .time_to_live(Duration::from_secs(60))
        .build()
}

#[handler]
async fn get_user(req: &mut Request, depot: &mut Depot) -> Result<Json<User>, StatusError> {
    let id = req.param::<i64>("id").ok_or_else(|| StatusError::bad_request())?;
    let cache = depot.obtain::<UserCache>().unwrap();
    let pool = depot.obtain::<PgPool>().unwrap();

    // Check cache
    if let Some(user) = cache.get(&id).await {
        return Ok(Json(user));
    }

    // Query database
    let user = sqlx::query_as::<_, User>("SELECT id, name, email FROM users WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await
        .map_err(|_| StatusError::internal_server_error())?
        .ok_or_else(|| StatusError::not_found())?;

    // Cache result
    cache.insert(id, user.clone()).await;

    Ok(Json(user))
}
```

## Cache Invalidation

```rust
use moka::future::Cache;

struct CacheService {
    user_cache: Cache<i64, User>,
}

impl CacheService {
    // Invalidate single entry
    async fn invalidate_user(&self, id: i64) {
        self.user_cache.invalidate(&id).await;
    }

    // Invalidate all entries
    async fn invalidate_all_users(&self) {
        self.user_cache.invalidate_all();
    }

    // Invalidate matching entries
    async fn invalidate_users_by_ids(&self, ids: &[i64]) {
        for id in ids {
            self.user_cache.invalidate(id).await;
        }
    }
}

// Invalidate on update
#[handler]
async fn update_user(
    req: &mut Request,
    depot: &mut Depot
) -> Result<StatusCode, StatusError> {
    let id = req.param::<i64>("id").unwrap();

    // Update in database...

    // Invalidate cache
    let cache = depot.obtain::<UserCache>().unwrap();
    cache.invalidate(&id).await;

    Ok(StatusCode::OK)
}
```

## Conditional Requests

```rust
use salvo::prelude::*;
use time::OffsetDateTime;

#[handler]
async fn conditional_get(req: &mut Request, res: &mut Response) -> Result<Json<Data>, StatusError> {
    let data = get_data().await?;
    let last_modified = data.updated_at;

    // Check If-Modified-Since
    if let Some(since) = req.header::<String>("If-Modified-Since") {
        // Parse and compare timestamps
        // Return 304 if not modified
    }

    res.headers_mut().insert(
        "Last-Modified",
        last_modified.format(&time::format_description::well_known::Rfc2822)
            .unwrap()
            .parse()
            .unwrap()
    );

    Ok(Json(data))
}
```

## Complete Caching Example

```rust
use salvo::prelude::*;
use moka::future::Cache;
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Clone, Serialize)]
struct Product {
    id: i64,
    name: String,
    price: f64,
}

type ProductCache = Cache<i64, Product>;

#[handler]
async fn get_product(req: &mut Request, depot: &mut Depot, res: &mut Response) -> Result<Json<Product>, StatusError> {
    let id = req.param::<i64>("id").ok_or_else(|| StatusError::bad_request())?;
    let cache = depot.obtain::<ProductCache>().unwrap();

    // Check cache
    if let Some(product) = cache.get(&id).await {
        res.headers_mut().insert("X-Cache", "HIT".parse().unwrap());
        res.headers_mut().insert("Cache-Control", "public, max-age=60".parse().unwrap());
        return Ok(Json(product));
    }

    // Fetch from database (simulated)
    let product = Product {
        id,
        name: format!("Product {}", id),
        price: 99.99,
    };

    // Cache the result
    cache.insert(id, product.clone()).await;

    res.headers_mut().insert("X-Cache", "MISS".parse().unwrap());
    res.headers_mut().insert("Cache-Control", "public, max-age=60".parse().unwrap());

    Ok(Json(product))
}

#[tokio::main]
async fn main() {
    let cache: ProductCache = Cache::builder()
        .max_capacity(10_000)
        .time_to_live(Duration::from_secs(300))
        .build();

    let router = Router::new()
        .hoop(affix_state::inject(cache))
        .push(Router::with_path("products/{id}").get(get_product));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Best Practices

1. **Use appropriate TTL**: Match cache duration to data freshness requirements
2. **Set cache headers**: Enable browser and CDN caching
3. **Implement cache invalidation**: Clear cache when data changes
4. **Use ETag for validation**: Enable conditional requests
5. **Monitor cache hit rate**: Track effectiveness
6. **Size cache appropriately**: Balance memory usage and hit rate
7. **Cache at multiple layers**: Browser, CDN, application, database
8. **Consider stale-while-revalidate**: Serve stale content while refreshing
