---
name: salvo-path-syntax
description: Path parameter syntax guide for Salvo routing. Explains the `{}` syntax (v0.76+) vs deprecated `<>` syntax, with migration examples.
---

# Salvo Path Parameter Syntax

This skill explains the path parameter syntax changes in Salvo and provides migration guidance.

## Syntax Version History

### Version 0.76 and Later (Current)

Starting from Salvo **0.76**, path parameters use **curly braces `{}`** syntax:

```rust
// Basic path parameter
Router::with_path("users/{id}").get(get_user)

// Typed parameter
Router::with_path("users/{id:num}").get(get_user)

// Regex constraint
Router::with_path(r"users/{id|\d+}").get(get_user)

// Single segment wildcard
Router::with_path("files/{*}").get(handler)

// Named single segment wildcard
Router::with_path("files/{*filename}").get(handler)

// Multi-segment wildcard (rest of path)
Router::with_path("static/{**path}").get(serve_static)
```

### Before Version 0.76 (Deprecated)

In versions **before 0.76**, path parameters used **angle brackets `<>`** syntax:

```rust
// Basic path parameter (DEPRECATED)
Router::with_path("users/<id>").get(get_user)

// Typed parameter (DEPRECATED)
Router::with_path("users/<id:num>").get(get_user)

// Regex constraint (DEPRECATED)
Router::with_path(r"users/<id|\d+>").get(get_user)

// Single segment wildcard (DEPRECATED)
Router::with_path("files/<*>").get(handler)

// Named single segment wildcard (DEPRECATED)
Router::with_path("files/<*filename>").get(handler)

// Multi-segment wildcard (DEPRECATED)
Router::with_path("static/<**path>").get(serve_static)
```

## Migration Guide

### Quick Reference Table

| Pattern Type | Before 0.76 (Deprecated) | 0.76+ (Current) |
|--------------|--------------------------|-----------------|
| Basic param | `<id>` | `{id}` |
| Typed param | `<id:num>` | `{id:num}` |
| Regex param | `<id\|\d+>` | `{id\|\d+}` |
| Single wildcard | `<*>` | `{*}` |
| Named wildcard | `<*name>` | `{*name}` |
| Rest wildcard | `<**>` | `{**}` |
| Named rest | `<**path>` | `{**path}` |

### Migration Steps

1. **Find all route definitions** using `<>` syntax
2. **Replace angle brackets** with curly braces
3. **Update tests** if they reference path patterns
4. **Verify** all routes work correctly

### Example Migration

Before (deprecated):
```rust
let router = Router::new()
    .push(
        Router::with_path("api/v1")
            .push(
                Router::with_path("users")
                    .get(list_users)
                    .push(
                        Router::with_path("<id>")
                            .get(get_user)
                            .delete(delete_user)
                    )
            )
            .push(
                Router::with_path("files/<**path>")
                    .get(serve_file)
            )
    );
```

After (current):
```rust
let router = Router::new()
    .push(
        Router::with_path("api/v1")
            .push(
                Router::with_path("users")
                    .get(list_users)
                    .push(
                        Router::with_path("{id}")
                            .get(get_user)
                            .delete(delete_user)
                    )
            )
            .push(
                Router::with_path("files/{**path}")
                    .get(serve_file)
            )
    );
```

## Parameter Types

Both syntaxes support the same type constraints (shown in current `{}` syntax):

```rust
// Numeric types
Router::with_path("users/{id:num}")    // Any number
Router::with_path("users/{id:i32}")    // 32-bit integer
Router::with_path("users/{id:i64}")    // 64-bit integer
Router::with_path("users/{id:u32}")    // Unsigned 32-bit
Router::with_path("users/{id:u64}")    // Unsigned 64-bit

// Regex pattern
Router::with_path(r"posts/{slug|[a-z0-9-]+}")

// UUID pattern (using regex)
Router::with_path(r"users/{id|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}}")
```

## Accessing Parameters in Handlers

Parameter access is the same regardless of syntax version:

```rust
#[handler]
async fn get_user(req: &mut Request) -> String {
    // Get parameter as specific type
    let id: i64 = req.param("id").unwrap();

    // Or with explicit type annotation
    let id = req.param::<i64>("id").unwrap();

    format!("User ID: {}", id)
}

#[handler]
async fn serve_file(req: &mut Request) -> String {
    // Get wildcard path
    let path: String = req.param("path").unwrap();
    format!("Serving: {}", path)
}
```

## Common Mistakes

### Using Wrong Syntax for Version

```rust
// ERROR: Using <> in Salvo 0.76+
Router::with_path("users/<id>")  // Won't match!

// CORRECT: Use {} in Salvo 0.76+
Router::with_path("users/{id}")
```

### Mixing Syntaxes

```rust
// ERROR: Mixed syntax
Router::with_path("users/{id}/posts/<post_id>")  // Won't work!

// CORRECT: Consistent syntax
Router::with_path("users/{id}/posts/{post_id}")
```

## Version Detection

Check your Salvo version in `Cargo.toml`:

```toml
[dependencies]
# Version 0.76+ uses {} syntax
salvo = "0.76"  # First version with {} syntax

# Version 0.75 and earlier uses <> syntax (deprecated)
salvo = "0.75"  # Uses <> syntax (deprecated)
```

For the latest version, always use `{}` syntax:

```toml
[dependencies]
salvo = "1.88.1"  # Current stable - uses {} syntax
```

Note: The `{}` syntax was introduced in version 0.76 and is used in all versions since then, including the current 1.x releases.

## Best Practices

1. **Always use `{}` syntax** for new projects
2. **Migrate existing projects** to `{}` syntax when updating Salvo
3. **Use typed parameters** when possible for automatic validation
4. **Use regex constraints** for complex validation requirements
5. **Name your wildcards** for clarity (`{**path}` instead of `{**}`)
