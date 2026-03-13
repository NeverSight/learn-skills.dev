---
name: rust-tdd
description: Test-driven development enforcement for Rust. Requires failing tests before implementation. Use when implementing features, fixing bugs, or when code quality discipline is needed.
---

# Rust TDD Enforcement

Strict test-driven development practices for Rust projects.

## The Golden Rule

**No Code Without a Failing Test First**

This is not optional. This is not negotiable. Every feature, every bug fix, every change starts with a test.

## The TDD Cycle

1. **Red**: Write a test that describes the behavior you want. Run it. It must fail.
2. **Green**: Write the minimum code to make the test pass. Nothing more.
3. **Refactor**: Clean up while keeping tests green.
4. **Repeat**

```rust
// Step 1: Write the failing test
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn create_user_with_valid_email() {
        let user = User::new("test@example.com", "Test User").unwrap();
        assert_eq!(user.email(), "test@example.com");
        assert_eq!(user.name(), "Test User");
    }
}

// Step 2: Run it — it MUST fail
// $ cargo test create_user_with_valid_email
// error[E0599]: no function `new` found for struct `User`

// Step 3: Write minimum code to pass
impl User {
    pub fn new(email: &str, name: &str) -> Result<Self, ValidationError> {
        Ok(Self {
            email: email.to_string(),
            name: name.to_string(),
        })
    }
}

// Step 4: Run test again — it passes
// Step 5: Refactor if needed, keeping tests green
```

## Test Organization

Tests live in the same file as the code they test, in a `#[cfg(test)]` module:

```rust
// src/user.rs
pub struct User { /* ... */ }

impl User {
    pub fn new(email: &str, name: &str) -> Result<Self, Error> {
        // ...
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    mod new {
        use super::*;

        #[test]
        fn with_valid_email() { /* ... */ }

        #[test]
        fn with_invalid_email_returns_error() { /* ... */ }

        #[test]
        fn with_empty_name_returns_error() { /* ... */ }
    }
}
```

Integration tests go in `tests/` directory:

```
src/
├── lib.rs
├── user.rs
└── db.rs
tests/
├── user_integration.rs
└── api_integration.rs
```

## Mandatory Test Cases

For every function, test:

### 1. Happy Path

Valid input produces expected output.

```rust
#[test]
fn parse_config_with_valid_toml() {
    let input = r#"
        [server]
        port = 8080
        host = "localhost"
    "#;
    let config = Config::parse(input).unwrap();
    assert_eq!(config.server.port, 8080);
    assert_eq!(config.server.host, "localhost");
}
```

### 2. Error Cases

Invalid input returns appropriate errors.

```rust
#[test]
fn parse_config_with_invalid_toml_returns_error() {
    let input = "not valid toml {{{";
    let err = Config::parse(input).unwrap_err();
    assert!(matches!(err, ConfigError::ParseError(_)));
}

#[test]
fn parse_config_with_missing_required_field_returns_error() {
    let input = r#"
        [server]
        host = "localhost"
    "#;  // missing port
    let err = Config::parse(input).unwrap_err();
    assert!(matches!(err, ConfigError::MissingField(field) if field == "port"));
}
```

### 3. Edge Cases

Boundary conditions and unusual inputs.

```rust
#[test]
fn parse_port_zero() {
    let err = ServerConfig::new(0, "localhost").unwrap_err();
    assert!(matches!(err, ConfigError::InvalidPort));
}

#[test]
fn parse_port_max() {
    let config = ServerConfig::new(65535, "localhost").unwrap();
    assert_eq!(config.port, 65535);
}

#[test]
fn empty_string_input() {
    let err = Config::parse("").unwrap_err();
    assert!(matches!(err, ConfigError::Empty));
}
```

### 4. Type Safety

Ensure newtypes and wrappers enforce invariants.

```rust
#[test]
fn email_rejects_missing_at_sign() {
    let err = Email::new("invalid").unwrap_err();
    assert!(matches!(err, ValidationError::InvalidEmail));
}

#[test]
fn email_normalizes_to_lowercase() {
    let email = Email::new("User@Example.COM").unwrap();
    assert_eq!(email.as_str(), "user@example.com");
}

#[test]
fn user_id_equality() {
    assert_eq!(UserId(1), UserId(1));
    assert_ne!(UserId(1), UserId(2));
}
```

### 5. State Transitions (if applicable)

```rust
#[test]
fn order_can_transition_from_pending_to_confirmed() {
    let order = Order::new();
    assert_eq!(order.status(), Status::Pending);

    let order = order.confirm().unwrap();
    assert_eq!(order.status(), Status::Confirmed);
}

#[test]
fn order_cannot_transition_from_pending_to_shipped() {
    let order = Order::new();
    let err = order.ship().unwrap_err();
    assert!(matches!(err, OrderError::InvalidTransition { .. }));
}
```

## Async Tests

Use `#[tokio::test]` for async tests:

```rust
#[tokio::test]
async fn fetch_user_returns_user() {
    let pool = setup_test_db().await;
    let repo = UserRepo::new(pool);

    let user = repo.create("test@example.com", "Test").await.unwrap();
    let found = repo.find_by_id(user.id).await.unwrap();

    assert_eq!(found.email, "test@example.com");
}

#[tokio::test]
async fn fetch_nonexistent_user_returns_not_found() {
    let pool = setup_test_db().await;
    let repo = UserRepo::new(pool);

    let err = repo.find_by_id(UserId(999)).await.unwrap_err();
    assert!(matches!(err, RepoError::NotFound));
}
```

## Test Utilities

```rust
// Use rstest for parameterized tests
use rstest::rstest;

#[rstest]
#[case("test@example.com", true)]
#[case("invalid", false)]
#[case("", false)]
#[case("a@b.c", true)]
fn email_validation(#[case] input: &str, #[case] expected_valid: bool) {
    assert_eq!(Email::new(input).is_ok(), expected_valid);
}

// Use proptest for property-based testing
use proptest::prelude::*;

proptest! {
    #[test]
    fn parse_then_display_roundtrips(port in 1u16..=65535, host in "[a-z]{1,10}") {
        let config = ServerConfig::new(port, &host).unwrap();
        let serialized = config.to_string();
        let parsed = ServerConfig::from_str(&serialized).unwrap();
        assert_eq!(config, parsed);
    }
}
```

## What NOT to Do

### ❌ Don't write tests after the code

```rust
// WRONG: Code first, then tests
fn create_user(email: &str) -> User { ... }  // Written first
#[test]
fn test_create_user() { ... }  // Added later to "cover" it
```

### ❌ Don't skip tests for "simple" functions

```rust
// WRONG: "It's too simple to test"
fn full_name(first: &str, last: &str) -> String {
    format!("{first} {last}")
}
// Still needs tests! What about empty strings? Whitespace?
```

### ❌ Don't test private implementation details

```rust
// WRONG: Testing private helper
#[test]
fn test_internal_parse() {
    assert_eq!(internal_parse("abc"), 42);
}

// RIGHT: Test through the public API
#[test]
fn process_accepts_valid_input() {
    let result = process("abc").unwrap();
    assert_eq!(result.value, 42);
}
```

### ❌ Don't write tests that always pass

```rust
// WRONG: Test always passes
#[test]
fn does_something() {
    let result = do_thing();
    assert!(result.is_ok()); // What if Ok(()) is wrong?
}

// RIGHT: Assert specific expectations
#[test]
fn returns_created_user() {
    let result = create_user("test@example.com").unwrap();
    assert_eq!(result.email, "test@example.com");
}
```

## Pre-Implementation Checklist

Before writing ANY code, ask yourself:

1. ☐ Have I written a failing test?
2. ☐ Does the test describe the behavior I want?
3. ☐ Have I run the test and confirmed it fails?
4. ☐ Does it fail for the RIGHT reason?

Only after checking all boxes: write the implementation.

## Running Tests

```bash
# Run all tests
cargo test

# Run specific test
cargo test create_user_with_valid_email

# Run tests in a module
cargo test user::tests

# Run with output shown
cargo test -- --nocapture

# Run ignored tests
cargo test -- --ignored

# Run with coverage (requires cargo-tarpaulin)
cargo tarpaulin

# Run specific integration test
cargo test --test user_integration
```
