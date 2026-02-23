---
name: test-optimization
description: Advanced test optimization with cargo-nextest, property testing, and performance benchmarking. Use when optimizing test execution speed, implementing property-based tests, or analyzing test performance.
---

# Test Optimization

Advanced test optimization with cargo-nextest, property testing, and benchmarking.

## cargo-nextest (Primary Test Runner)

```bash
cargo nextest run --all              # all tests
cargo nextest run --profile ci       # CI with retries + JUnit XML
cargo nextest run --profile nightly  # extended timeouts
cargo nextest run -E 'package(memory-core)'  # filterset DSL
cargo test --doc --all               # doctests (nextest limitation)
```

### Configuration (.config/nextest.toml)

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

## Mutation Testing (cargo-mutants)

Verifies tests actually catch bugs by injecting mutations:

```bash
cargo mutants -p memory-core --timeout 120 --jobs 4 -- --lib
```

- **Acceptance**: <20% missed mutants in core business logic
- **Frequency**: Nightly CI or pre-release
- **Scope**: Start with memory-core, expand incrementally

## Property-Based Testing (proptest)

```rust
proptest! {
    #[test]
    fn serialization_roundtrip(episode in any_episode_strategy()) {
        let bytes = postcard::to_allocvec(&episode).unwrap();
        let decoded: Episode = postcard::from_bytes(&bytes).unwrap();
        assert_eq!(episode, decoded);
    }
}
```

## Snapshot Testing (insta)

```rust
#[test]
fn test_mcp_response_format() {
    let response = build_tool_response("search_patterns", &params);
    insta::assert_json_snapshot!(response);
}
```

```bash
cargo insta test     # run snapshot tests
cargo insta review   # accept/reject changes
```

## Performance Targets

| Operation | Target | Actual |
|-----------|--------|--------|
| Episode Creation | < 50ms | ~2.5 µs |
| Step Logging | < 20ms | ~1.1 µs |
| Pattern Extraction | < 1000ms | ~10.4 µs |
| Memory Retrieval | < 100ms | ~721 µs |

## Best Practices

- Use nextest profiles for dev/CI/nightly separation
- Implement property tests for serialization roundtrips and state machines
- Use snapshot tests for MCP responses, CLI output
- Run mutation testing before releases
- Monitor test duration and coverage trends

## References

- [ADR-033: Modern Testing Strategy](../../../plans/adr/ADR-033-Modern-Testing-Strategy.md)
- [TESTING.md](../../../TESTING.md)
