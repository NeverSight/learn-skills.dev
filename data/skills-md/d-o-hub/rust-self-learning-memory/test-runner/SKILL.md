---
name: test-runner
description: Execute and manage Rust tests including unit tests, integration tests, and doc tests. Use when running tests to ensure code quality and correctness.
---

# Test Runner

Execute and manage Rust tests for the self-learning memory project.

## Test Categories

| Category | Command (preferred) | Fallback | Scope |
|----------|-------------------|----------|-------|
| Unit | `cargo nextest run --lib` | `cargo test --lib` | Individual functions |
| Integration | `cargo nextest run --test '*'` | `cargo test --test '*'` | End-to-end workflows |
| Doc | `cargo test --doc` | (nextest unsupported) | Documentation examples |
| All | `cargo nextest run --all` | `cargo test --all` | Complete validation |
| Mutation | `cargo mutants -p memory-core` | — | Test effectiveness |
| Snapshot | `cargo insta test` | — | Output regression |

## Execution Strategy

### Step 1: Quick Check (Unit Tests)
```bash
cargo nextest run --lib
```
- Fast feedback (< 30s), per-test process isolation
- Catch basic logic errors

### Step 2: Integration Tests
```bash
cargo nextest run --test '*'
```
- Tests database interactions
- Requires Turso/redb setup

### Step 3: Full Suite
```bash
cargo nextest run --all
cargo test --doc  # doctests separately (nextest limitation)
```
- Complete validation before commit

### Step 4: Mutation Testing (Periodic)
```bash
cargo mutants -p memory-core --timeout 120 --jobs 4 -- --lib
```
- Verifies test suite catches real bugs
- Run nightly or before releases (ADR-033)

## Troubleshooting

### Async/Await Issues
**Symptom**: Test hangs
```rust
#[tokio::test]
async fn test_async() {
    let result = async_fn().await;  // Don't forget .await
}
```

### Database Connection
**Symptom**: Connection refused
- Check TURSO_URL, TURSO_TOKEN
- Use test database

### Race Conditions
**Symptom**: Intermittent failures
```bash
cargo test -- --test-threads=1
```

### redb Lock Errors
**Symptom**: "Database is locked"
- Use separate DB per test
- Close transactions promptly

## Coverage

```bash
cargo install cargo-llvm-cov
cargo llvm-cov --html --output-dir coverage
```

## Best Practices

- Isolation: Each test independent
- Cleanup: Remove test data
- Speed: < 1s per unit test
- Naming: `test_<function>_<scenario>_<expected>`
- AAA pattern: Arrange-Act-Assert in every test
- Single responsibility: Each test verifies ONE behavior

## Advanced: Async Testing Patterns

```rust
// Time-based testing (paused clock)
#[tokio::test(start_paused = true)]
async fn test_timeout_behavior() {
    let start = tokio::time::Instant::now();
    tokio::time::sleep(Duration::from_secs(5)).await;
    assert!(start.elapsed().as_millis() < 100);
}

// Concurrent operations
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_concurrent_episodes() {
    let memory = Arc::new(setup_memory().await);
    let handles: Vec<_> = (0..10).map(|i| {
        let mem = memory.clone();
        tokio::spawn(async move {
            mem.start_episode(format!("Task {}", i), ctx, type_).await
        })
    }).collect();
    let results = futures::future::join_all(handles).await;
    assert_eq!(results.len(), 10);
}
```

### Common Async Pitfalls

| Bad | Good |
|-----|------|
| `std::thread::sleep()` | `tokio::time::sleep().await` |
| `memory.start_episode()` | `memory.start_episode().await` |
| Single-threaded for concurrency | `multi_thread` runtime |

## nextest Profiles (.config/nextest.toml)

```toml
[profile.default]
retries = 0
slow-timeout = { period = "60s", terminate-after = 2 }
fail-fast = false

[profile.ci]
retries = 2
slow-timeout = { period = "30s", terminate-after = 3 }
failure-output = "immediate-final"
junit.path = "target/nextest/ci/junit.xml"

[profile.nightly]
retries = 3
slow-timeout = { period = "120s", terminate-after = 2 }
```

```bash
cargo nextest run                  # default profile
cargo nextest run --profile ci     # CI with retries + JUnit
cargo nextest run --profile nightly  # nightly with extended timeouts
```

## Snapshot Testing (insta)

```rust
#[test]
fn test_mcp_tool_response() {
    let response = build_tool_response("search_patterns", &params);
    insta::assert_json_snapshot!(response);
}
```

```bash
cargo insta test     # run snapshot tests
cargo insta review   # accept/reject changes
```

## Property-Based Testing

```rust
proptest! {
    #[test]
    fn test_episode_id_uniqueness(
        tasks in prop::collection::vec(any::<String>(), 1..100)
    ) {
        let rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(async {
            let memory = setup_memory().await;
            let mut ids = HashSet::new();
            for desc in tasks {
                let id = memory.start_episode(desc, ctx, type_).await;
                prop_assert!(ids.insert(id));
            }
        });
    }
}
```

## Advanced: Episodic Memory Testing

```rust
#[tokio::test]
async fn test_complete_episode_lifecycle() {
    let memory = setup_memory().await;
    let id = memory.start_episode("Test task", ctx, TaskType::CodeGen).await;
    memory.log_execution_step(id.clone(), step1).await;
    memory.complete_episode(id.clone(), TaskOutcome::Success, None).await?;
    let episode = memory.get_episode(&id).await?;
    assert_eq!(episode.outcome, TaskOutcome::Success);
}
```

## Performance Targets

| Operation | Target | Actual |
|-----------|--------|--------|
| Episode Creation | < 50ms | ~2.5 µs |
| Step Logging | < 20ms | ~1.1 µs |
| Pattern Extraction | < 1000ms | ~10.4 µs |
| Memory Retrieval | < 100ms | ~721 µs |

## References

- [ADR-033: Modern Testing Strategy](../../../plans/adr/ADR-033-Modern-Testing-Strategy.md)
- [TESTING.md](../../../TESTING.md) — Full testing guide

Consolidated from these former skills (preserved in `_consolidated/`):
- `test-optimization` — cargo-nextest, property testing, benchmarking
- `quality-unit-testing` — AAA pattern, naming conventions, test quality
- `rust-async-testing` — tokio test patterns, time-based testing
- `episodic-memory-testing` — episode lifecycle, pattern extraction, reward scoring tests
