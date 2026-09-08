---
name: rust-testing
description: |
  Rust testing — unit tests, integration tests, property tests, benchmarks. Use this skill when:
  - User writes tests with #[test], #[tokio::test], or test modules
  - User asks about test organization, test helpers, or fixtures
  - User implements property-based testing with proptest or quickcheck
  - User writes benchmarks with criterion
  - User mocks traits with mockall or uses test doubles
  - User asks about snapshot testing with insta
  - User tests async code or Tokio tasks
  - User asks about coverage, test isolation, or CI configuration
  Trigger for any Rust testing question.
---



## Quick Navigation

- [references/unit_integration.md](references/unit_integration.md)
- [references/mocks_property.md](references/mocks_property.md)

# Rust Testing

Testing in Rust is first-class: cargo test runs unit + integration tests, doctests are auto-run, and the ecosystem has excellent tools for every testing need.

## Test Organization

```rust
// Unit tests: in the same file as the code they test
// src/user.rs
pub fn validate_age(age: u32) -> bool {
    age >= 0 && age <= 150
}

#[cfg(test)] // Only compiled when running tests
mod tests {
    use super::*; // Access private functions

    #[test]
    fn valid_age_returns_true() {
        assert!(validate_age(25));
    }

    #[test]
    fn age_zero_is_valid() {
        assert!(validate_age(0));
    }

    #[test]
    fn age_over_150_is_invalid() {
        assert!(!validate_age(151));
    }
}
```

```
// Integration tests: in tests/ directory (public API only)
tests/
├── integration_test.rs
└── common/
    └── mod.rs  // Shared test helpers
```

```rust
// tests/integration_test.rs
use my_lib::UserService;

mod common;  // tests/common/mod.rs

#[test]
fn create_and_find_user() {
    let db = common::setup_test_db();
    let svc = UserService::new(db);

    let user = svc.create("Alice", "alice@example.com").unwrap();
    let found = svc.find(user.id).unwrap();

    assert_eq!(found.name, "Alice");
}
```

## Test Naming

Use descriptive names that read like specifications:

```rust
// Bad: no context
#[test] fn test1() {}
#[test] fn test_process() {}

// Good: <what>_<when/given>_<expected result>
#[test] fn validate_email_with_missing_at_sign_returns_error() {}
#[test] fn transfer_funds_when_balance_insufficient_returns_insufficient_funds_error() {}
#[test] fn parse_config_with_missing_required_field_fails() {}
```

## Assertions

```rust
// Basic
assert!(condition);
assert_eq!(left, right);
assert_ne!(left, right);

// With messages
assert!(user.is_active(), "Expected user {id} to be active");
assert_eq!(result, expected, "Processing {input} failed");

// Approximate equality for floats
assert!((result - 3.14159).abs() < 1e-5);

// Pattern matching
assert!(matches!(result, Ok(User { name, .. }) if name == "Alice"));

// Panics assertion
#[test]
#[should_panic(expected = "out of bounds")]
fn access_out_of_bounds_panics() {
    let v = vec![1, 2, 3];
    let _ = v[10];
}
```

## Arrange-Act-Assert Pattern

```rust
#[test]
fn deduct_items_from_inventory_reduces_stock() {
    // Arrange
    let mut inventory = Inventory::new();
    inventory.add_stock("widget", 10);

    // Act
    let result = inventory.deduct("widget", 3);

    // Assert
    assert!(result.is_ok());
    assert_eq!(inventory.stock("widget"), 7);
}
```

## Async Tests

```rust
// Test async functions with tokio
#[tokio::test]
async fn fetch_user_returns_correct_data() {
    let client = TestClient::new();
    let user = client.get_user(42).await.unwrap();
    assert_eq!(user.id, 42);
}

// Single-threaded async test (faster, no thread synchronization)
#[tokio::test(flavor = "current_thread")]
async fn concurrent_tasks_complete() {
    let (r1, r2) = tokio::join!(task_one(), task_two());
    assert!(r1.is_ok());
    assert!(r2.is_ok());
}

// Test with timeout
#[tokio::test]
async fn operation_completes_within_timeout() {
    let result = tokio::time::timeout(
        std::time::Duration::from_secs(1),
        some_async_operation(),
    )
    .await;
    assert!(result.is_ok(), "Operation timed out");
}
```

## Fixtures and Test Helpers

```rust
// Reusable test data builders
struct UserBuilder {
    name: String,
    email: String,
    age: u32,
}

impl Default for UserBuilder {
    fn default() -> Self {
        Self {
            name: "Test User".into(),
            email: "test@example.com".into(),
            age: 25,
        }
    }
}

impl UserBuilder {
    fn name(mut self, name: &str) -> Self { self.name = name.into(); self }
    fn email(mut self, email: &str) -> Self { self.email = email.into(); self }
    fn build(self) -> User {
        User::new(self.name, self.email, self.age).unwrap()
    }
}

// Usage in tests
#[test]
fn admin_user_can_delete_posts() {
    let admin = UserBuilder::default()
        .name("Admin")
        .email("admin@example.com")
        .build();
    // ...
}
```

```rust
// RAII fixture — cleanup runs automatically
struct TempDatabase {
    path: std::path::PathBuf,
    conn: DbConnection,
}

impl TempDatabase {
    fn new() -> Self {
        let path = std::env::temp_dir()
            .join(format!("test-db-{}.db", uuid::Uuid::new_v4()));
        let conn = DbConnection::create(&path).unwrap();
        conn.run_migrations().unwrap();
        Self { path, conn }
    }
}

impl Drop for TempDatabase {
    fn drop(&mut self) {
        let _ = std::fs::remove_file(&self.path);
    }
}

#[test]
fn user_created_in_database() {
    let db = TempDatabase::new(); // Created
    db.conn.insert_user("Alice").unwrap();
    assert_eq!(db.conn.count_users().unwrap(), 1);
} // db.drop() called: file deleted
```

## Mocking with Mockall

```rust
use mockall::automock;

#[automock]
trait EmailService: Send + Sync {
    fn send(&self, to: &str, subject: &str, body: &str) -> Result<(), EmailError>;
}

#[test]
fn password_reset_sends_email() {
    let mut mock_email = MockEmailService::new();

    // Set expectation: send() called once with specific args
    mock_email
        .expect_send()
        .with(
            mockall::predicate::eq("user@example.com"),
            mockall::predicate::str::contains("Reset"),
            mockall::predicate::always(),
        )
        .times(1)
        .returning(|_, _, _| Ok(()));

    let service = PasswordService::new(Arc::new(mock_email));
    service.send_reset_link("user@example.com").unwrap();
    // Mock verifies expectations on drop
}
```

## Property-Based Testing

```rust
use proptest::prelude::*;

// Property: encode then decode is identity
proptest! {
    #[test]
    fn encode_decode_roundtrip(original in ".*") {
        let encoded = base64_encode(&original);
        let decoded = base64_decode(&encoded).unwrap();
        prop_assert_eq!(original, decoded);
    }

    #[test]
    fn sort_is_idempotent(mut v in prop::collection::vec(any::<i32>(), 0..100)) {
        v.sort();
        let once_sorted = v.clone();
        v.sort();
        prop_assert_eq!(v, once_sorted);
    }

    #[test]
    fn add_is_commutative(a in 0i32..1000, b in 0i32..1000) {
        prop_assert_eq!(a + b, b + a);
    }
}

// Custom strategies
fn valid_email() -> impl Strategy<Value = String> {
    r"[a-z]{3,10}@[a-z]{3,10}\.[a-z]{2,4}".prop_map(|s| s)
}

proptest! {
    #[test]
    fn valid_emails_parse_successfully(email in valid_email()) {
        prop_assert!(Email::new(&email).is_ok());
    }
}
```

## Snapshot Testing with Insta

```rust
use insta::assert_snapshot;

#[test]
fn render_user_profile() {
    let user = User { name: "Alice".into(), role: Role::Admin, age: 30 };
    let rendered = render_profile(&user);

    // First run: creates snapshot file
    // Subsequent runs: compares against saved snapshot
    assert_snapshot!(rendered);
}

// JSON snapshots
use insta::assert_json_snapshot;

#[test]
fn api_response_matches_snapshot() {
    let response = api_client.get_user(1).unwrap();
    assert_json_snapshot!(response, {
        ".created_at" => "[timestamp]", // Redact dynamic fields
        ".id" => "[id]",
    });
}
```

```bash
# Review and accept new/changed snapshots
cargo install cargo-insta
cargo insta review
```

## Benchmarks with Criterion

```toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }

[[bench]]
name = "my_bench"
harness = false
```

```rust
// benches/my_bench.rs
use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 | 1 => n,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn bench_fibonacci(c: &mut Criterion) {
    let mut group = c.benchmark_group("fibonacci");

    for size in [10u64, 20, 30] {
        group.bench_with_input(BenchmarkId::from_parameter(size), &size, |b, &size| {
            b.iter(|| fibonacci(black_box(size)));
        });
    }
    group.finish();
}

// Compare implementations
fn bench_string_ops(c: &mut Criterion) {
    let mut group = c.benchmark_group("string_creation");
    let s = "hello world";

    group.bench_function("to_string", |b| b.iter(|| black_box(s).to_string()));
    group.bench_function("to_owned", |b| b.iter(|| black_box(s).to_owned()));
    group.bench_function("String::from", |b| b.iter(|| String::from(black_box(s))));
    group.finish();
}

criterion_group!(benches, bench_fibonacci, bench_string_ops);
criterion_main!(benches);
```

```bash
cargo bench                    # Run all benchmarks
cargo bench -- "fibonacci"     # Run matching benchmarks
cargo bench -- --save-baseline main  # Save baseline
cargo bench -- --baseline main  # Compare to baseline
```

## Doctest Examples

```rust
/// Parses a version string into components.
///
/// # Examples
///
/// ```
/// use mylib::parse_version;
///
/// let (major, minor, patch) = parse_version("1.2.3").unwrap();
/// assert_eq!(major, 1);
/// assert_eq!(minor, 2);
/// assert_eq!(patch, 3);
/// ```
///
/// Returns `None` for invalid version strings:
///
/// ```
/// use mylib::parse_version;
/// assert!(parse_version("not-a-version").is_none());
/// ```
pub fn parse_version(s: &str) -> Option<(u32, u32, u32)> {
    // ...
}
```

```bash
cargo test --doc  # Run only doctests
```

## Best Practices

### 1. Arrange-Act-Assert (AAA) Structure
Always split your test blocks visually into three distinct phases for maximum readability:
- **Arrange**: Set up requirements, parameters, and mock states.
- **Act**: Call the unit or method under test.
- **Assert**: Validate results against expected outcomes.

```rust
#[test]
fn withdraw_reduces_account_balance() {
    // Arrange
    let mut account = Account::new(dec!(100.00));
    let amount = dec!(40.00);

    // Act
    account.withdraw(amount).unwrap();

    // Assert
    assert_eq!(account.balance(), dec!(60.00));
}
```

### 2. RAII Test Fixtures for Setup/Cleanup
Use structs implementing the `Drop` trait to handle setup and cleanup actions, ensuring database connections, file handles, or mock servers are torn down even if the test panics.

```rust
struct TestDbFixture {
    pub conn_str: String,
}

impl TestDbFixture {
    fn new() -> Self {
        let conn_str = format!("test_db_{}", uuid::Uuid::new_v4());
        // Initialize test database...
        Self { conn_str }
    }
}

impl Drop for TestDbFixture {
    fn drop(&mut self) {
        // Tear down test database...
    }
}

#[test]
fn query_returns_inserted_record() {
    let fixture = TestDbFixture::new();
    // database operations using fixture.conn_str ...
    // automatically dropped at scope exit
}
```

## Running Tests

```bash
cargo test                          # All tests
cargo test user                     # Tests with "user" in name
cargo test -- --nocapture           # Show println! output
cargo test -- --test-threads=1      # Single-threaded (for shared state tests)
cargo test --lib                    # Unit tests only
cargo test --test integration_test  # Specific integration test file
cargo test --doc                    # Doctests only
cargo test --release                # Tests in release mode
```

## Test Coverage

```bash
cargo install cargo-tarpaulin       # Linux/macOS
cargo tarpaulin --out Html --output-dir coverage/

# Or with llvm-cov (cross-platform)
cargo install cargo-llvm-cov
cargo llvm-cov --html
```

## Test Suite Checklist

- Unit-test pure logic close to the module under test.
- Put public behavior and cross-module flows in `tests/` integration tests.
- Use property tests for parsers, serializers, state machines, and invariants.
- Keep mocks at process or trait boundaries, not around simple domain logic.
- Add regression tests before fixing bugs.
- Run doctests for public examples that users may copy.

## References

- [Rust Book: Testing](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [mockall](https://docs.rs/mockall)
- [proptest](https://docs.rs/proptest) + [proptest guide](https://proptest-rs.github.io/proptest/proptest/index.html)
- [insta](https://insta.rs/)
- [criterion](https://bheisler.github.io/criterion.rs/book/)

