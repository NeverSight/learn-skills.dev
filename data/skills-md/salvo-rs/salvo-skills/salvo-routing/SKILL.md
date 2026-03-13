---
name: salvo-routing
description: Configure Salvo routers with path parameters, nested routes, and filters. Use for complex routing structures and RESTful APIs.
---

# Salvo Routing

This skill helps configure advanced routing patterns in Salvo applications.

## Salvo Routing Innovation

Salvo's routing system has unique features:

1. **Path as Filter**: Path matching is essentially a filter, allowing unified combination with method and custom conditions
2. **Reusable Routes**: Routers can be added to multiple locations for flexible composition
3. **Unified Middleware Model**: Middleware and handlers share the same concept via `hoop()` method
4. **Flexible Nesting**: Use `push()` for arbitrary depth hierarchical structures

## Path Patterns

### Static Paths

```rust
Router::with_path("users").get(list_users)
```

### Path Parameters

Salvo uses `{id}` syntax for path parameters (since version 0.76). Earlier versions used `<id>` syntax, which is now deprecated.

```rust
// Basic parameter
Router::with_path("users/{id}").get(show_user)

// Typed parameter (num, i32, i64, etc.)
Router::with_path("users/{id:num}").get(show_user)

// Regex pattern
Router::with_path(r"users/{id|\d+}").get(show_user)

// Wildcard (captures rest of path)
Router::with_path("files/{**path}").get(serve_file)
```

### Accessing Parameters

```rust
#[handler]
async fn show_user(req: &mut Request) -> String {
    let id = req.param::<i64>("id").unwrap();
    format!("User ID: {}", id)
}
```

## Wildcard Types

Salvo supports multiple wildcard patterns (using `{}` syntax since version 0.76; earlier versions used `<>` syntax):

1. **`{*}`**: Matches any single path segment
   ```rust
   Router::new().path("{*}").get(catch_all)
   ```

2. **`{**}`**: Matches all remaining path segments (including slashes)
   ```rust
   Router::new().path("static/{**path}").get(serve_static)
   // Matches: static/css/style.css, static/js/main.js, etc.
   ```

3. **Named wildcards**: Can retrieve matched content in handler
   ```rust
   Router::new().path("files/{*rest}").get(handler)
   // In handler: req.param::<String>("rest")
   ```

## Nested Routers

### Tree Structure

```rust
let router = Router::new()
    .push(
        Router::with_path("api/v1")
            .push(
                Router::with_path("users")
                    .get(list_users)
                    .post(create_user)
                    .push(
                        Router::with_path("{id}")
                            .get(show_user)
                            .patch(update_user)
                            .delete(delete_user)
                    )
            )
            .push(
                Router::with_path("posts")
                    .get(list_posts)
                    .post(create_post)
            )
    );
```

### Route Composition

```rust
fn user_routes() -> Router {
    Router::with_path("users")
        .get(list_users)
        .post(create_user)
        .push(
            Router::with_path("{id}")
                .get(get_user)
                .patch(update_user)
                .delete(delete_user)
        )
}

fn post_routes() -> Router {
    Router::with_path("posts")
        .get(list_posts)
        .post(create_post)
}

let api_v1 = Router::with_path("v1")
    .push(user_routes())
    .push(post_routes());

let api_v2 = Router::with_path("v2")
    .push(user_routes())
    .push(post_routes());

let router = Router::new()
    .push(Router::with_path("api/v1/users").get(list_users).post(create_user))
    .push(Router::with_path("api/v1/users/{id}").get(show_user).patch(update_user).delete(delete_user));
```

## HTTP Methods

```rust
Router::new()
    .get(handler)      // GET
    .post(handler)     // POST
    .put(handler)      // PUT
    .patch(handler)    // PATCH
    .delete(handler)   // DELETE
    .head(handler)     // HEAD
    .options(handler); // OPTIONS
```

## Path Matching Behavior

When a request arrives, routing works as follows:

1. **Filter Matching**: First attempts to match route filters (path, method, etc.)
2. **Match Failed**: If no filter matches, that route's middleware and handler are skipped
3. **Match Success**: If matched, executes middleware and handler in order

```rust
use salvo::routing::filters;

// Path filter
Router::with_filter(filters::path("users"))

// Method filter
Router::with_filter(filters::get())

// Combined filters
Router::with_filter(filters::path("users").and(filters::get()))
```

## Middleware with Routes

Use `hoop()` to add middleware to routes:

```rust
let router = Router::new()
    .hoop(logging)  // Applies to all routes
    .path("api")
    .push(
        Router::new()
            .hoop(auth_check)  // Only applies to routes under this
            .path("users")
            .get(list_users)
            .post(create_user)
    );
```

## HTTP Redirects

```rust
use salvo::prelude::*;
use salvo::writing::Redirect;

// Permanent redirect (301)
#[handler]
async fn permanent_redirect(res: &mut Response) {
    res.render(Redirect::permanent("/new-location"));
}

// Temporary redirect (302)
#[handler]
async fn temporary_redirect(res: &mut Response) {
    res.render(Redirect::found("/temporary-location"));
}

// See Other (303)
#[handler]
async fn see_other(res: &mut Response) {
    res.render(Redirect::see_other("/another-page"));
}
```

## Custom Route Filters

Create custom filters for complex matching logic:

```rust
use salvo::prelude::*;
use salvo::routing::filter::Filter;
use uuid::Uuid;

pub struct GuidFilter;

impl Filter for GuidFilter {
    fn filter(&self, req: &mut Request, _state: &mut PathState) -> bool {
        if let Some(param) = req.param::<String>("id") {
            Uuid::parse_str(&param).is_ok()
        } else {
            false
        }
    }
}

#[handler]
async fn get_user_by_guid(req: &mut Request) -> String {
    let id = req.param::<Uuid>("id").unwrap();
    format!("User GUID: {}", id)
}

let router = Router::new()
    .path("users/{id}")
    .filter(GuidFilter)
    .get(get_user_by_guid);
```

## Best Practices

1. Use tree structure for complex APIs
2. Use route composition functions for reusability
3. Use regex constraints for path parameters when needed (`{id:/\d+/}`)
4. Group related routes under common paths
5. Use descriptive parameter names
6. Apply middleware at the appropriate route level
7. Prefer `{id}` syntax for consistency
