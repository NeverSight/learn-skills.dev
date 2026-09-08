---
name: rust-testing
description: Rust testing strategies and patterns. Activates for test writing, test organization, mocking, property-based testing, integration tests, benchmark setup, and test coverage questions. Invoke with /rust-testing.
---

# Rust Testing Skill

## Test Organization

### Unit Tests (same file)
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_name_describes_behavior() {
        // Arrange
        let input = create_test_input();
        // Act
        let result = function_under_test(input);
        // Assert
        assert_eq!(result, expected);
    }
}
```

### Integration Tests (`tests/` directory)
```
tests/
├── common/
│   └── mod.rs          # Shared test helpers (NOT a test file)
├── api_tests.rs        # Test the public API
└── cli_tests.rs        # Test CLI behavior
```

### Test Naming Convention
`test_<unit>_<scenario>_<expected>`:
- `test_parser_empty_input_returns_error`
- `test_cache_expired_entry_evicted`

## Testing Patterns

### Test Fixtures with Builder
```rust
struct TestUserBuilder {
    name: String,
    email: String,
}

impl TestUserBuilder {
    fn new() -> Self { Self { name: "Test".into(), email: "test@example.com".into() } }
    fn name(mut self, name: &str) -> Self { self.name = name.into(); self }
    fn build(self) -> User { User { name: self.name, email: self.email } }
}
```

### Async Tests (tokio)
```rust
#[tokio::test]
async fn test_async_operation() {
    let result = async_function().await;
    assert!(result.is_ok());
}
```

### Snapshot Testing
Use `insta` for output-heavy tests:
```rust
#[test]
fn test_serialization() {
    let output = serialize(&my_struct);
    insta::assert_snapshot!(output);
}
```

### Property-Based Testing
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn roundtrip_serialization(value: i64) {
        let serialized = serialize(value);
        let deserialized = deserialize(&serialized);
        prop_assert_eq!(value, deserialized);
    }
}
```

## Mocking Strategy

| Approach | When | Crate |
|---|---|---|
| Trait-based (manual) | Simple interfaces | — |
| `mockall` | Complex trait mocking | `mockall` |
| Test doubles | Repository/service patterns | — |
| `wiremock` | HTTP API mocking | `wiremock` |
| `testcontainers` | Real databases in tests | `testcontainers` |

## Test Utilities

### `assert` Variants
- `assert_eq!(left, right)` — equality with debug output
- `assert_ne!(left, right)` — inequality
- `assert!(condition, "message {}", var)` — boolean with format
- `assert_matches!(value, Pattern)` — pattern matching

### Testing Errors
```rust
#[test]
fn test_returns_specific_error() {
    let result = risky_operation();
    assert!(matches!(result, Err(MyError::NotFound { .. })));
}
```

### Test Coverage
```bash
# With cargo-llvm-cov
cargo llvm-cov --html --open

# With cargo-tarpaulin
cargo tarpaulin --out Html
```

## Benchmarking with Criterion
```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_parse(c: &mut Criterion) {
    let input = include_str!("../testdata/large.json");
    c.bench_function("parse_large_json", |b| {
        b.iter(|| parse(criterion::black_box(input)))
    });
}

criterion_group!(benches, bench_parse);
criterion_main!(benches);
```
