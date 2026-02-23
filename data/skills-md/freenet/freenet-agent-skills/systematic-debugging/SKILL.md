---
name: systematic-debugging
description: Methodology for debugging non-trivial problems systematically. This skill should be used automatically when investigating bugs, test failures, or unexpected behavior that isn't immediately obvious. Emphasizes hypothesis formation, parallel investigation with subagents, and avoiding common anti-patterns like jumping to conclusions or weakening tests.
license: LGPL-3.0
---

# Systematic Debugging

## When to Use

Invoke this methodology automatically when:
- A test fails and the cause isn't immediately obvious
- Unexpected behavior occurs in production or development
- An error message doesn't directly point to the fix
- Multiple potential causes exist

## Core Principles

1. **Hypothesize before acting** - Form explicit hypotheses about root cause before changing code
2. **Test hypotheses systematically** - Validate or eliminate each hypothesis with evidence
3. **Parallelize investigation** - Use subagents for concurrent readonly exploration
4. **Preserve test integrity** - Never weaken tests to make them pass

## Debugging Scope Ladder

**Always prefer the smallest, most reproducible scope that demonstrates the bug.** Work up the ladder only when the smaller scope can't reproduce or doesn't apply:

| Priority | Scope | When to Use | Command |
|----------|-------|-------------|---------|
| 1 | **Unit test** | Logic errors, algorithm bugs, single-function issues | `cargo test -p freenet -- specific_test` |
| 2 | **Mocked unit test** | Transport/ring logic needing isolation | Unit test with `MockNetworkBridge` / `MockRing` |
| 3 | **Simulation test** | Multi-node behavior, state machines, race conditions | `cargo test -p freenet --test simulation_integration -- --test-threads=1` |
| 4 | **SimNetwork + FaultConfig** | Fault tolerance, message loss, network partitions | SimNetwork with configured fault injection |
| 5 | **fdev single-process** | Quick multi-peer CI validation | `cargo run -p fdev -- test --seed 42 single-process` |
| 6 | **freenet-test-network** | 20+ peer large-scale behavior | Docker-based `freenet-test-network` |
| 7 | **Real network** | Issues that only manifest with real UDP/NAT/latency | Manual multi-peer test across machines |

**Why this order matters:**
- Lower scopes are faster, deterministic, and reproducible by anyone
- Higher scopes require more infrastructure, time, and may not be accessible to all contributors
- Gateway logs, aggregate telemetry, and production metrics are not available to every developer — don't assume access to these when designing reproduction steps

## Debugging Workflow

### Phase 1: Reproduce and Isolate

1. **Reproduce the failure** — Confirm the bug exists and is reproducible
2. **Use the scope ladder** — Start at the smallest scope that can demonstrate the bug:
   - Can you write a unit test? Try that first
   - Needs multiple nodes? Use the simulation framework with a deterministic seed
   - Only happens under fault conditions? Use `SimNetwork` with `FaultConfig`
   - Can't reproduce in simulation? Then escalate to real network testing
3. **Record the seed** — When using simulation tests, always record the seed value for reproducibility
4. **Gather initial evidence** — Read error messages, logs, stack traces

**Simulation-first approach for distributed bugs:**
```bash
# Run simulation tests deterministically
cargo test -p freenet --features simulation_tests --test sim_network -- --test-threads=1

# With logging to observe event sequences
RUST_LOG=info cargo test -p freenet --features simulation_tests --test sim_network -- --nocapture --test-threads=1

# Reproduce with a specific seed
cargo run -p fdev -- test --seed 0xDEADBEEF single-process
```

### Phase 2: Form Hypotheses

Before touching any code, explicitly list potential causes:

```
Hypotheses:
1. [Most likely] The X component isn't handling Y case
2. [Possible] Race condition between A and B
3. [Less likely] Configuration mismatch in Z
```

Rank by likelihood based on evidence. Avoid anchoring on the first idea.

**Freenet-specific hypothesis patterns:**
- **State machine bugs** — Invalid transitions in operations (CONNECT, GET, PUT, UPDATE, SUBSCRIBE)
- **Ring/routing errors** — Incorrect peer selection, distance calculations, topology issues
- **Transport issues** — UDP packet loss handling, encryption/decryption, connection lifecycle
- **Contract execution** — WASM sandbox issues, state verification failures
- **Determinism violations** — Code using `std::time::Instant::now()` instead of `TimeSource`, or `rand::random()` instead of `GlobalRng`
- **Silent failure / fire-and-forget** — Spawned task dies with no error propagation (check: is the `JoinHandle` stored and polled? what happens if the task exits?), broadcast sent to zero targets with no warning, channel overflow silently dropping messages. Look for: `tokio::spawn` without `.await`/`.abort()`, `let _ = sender.send()`, missing logging on empty target sets
- **Resource exhaustion** — HashMap/Vec/channel entries inserted but never removed, causing unbounded memory growth or channel backpressure. Check: is there a cleanup path for every insert? Is cleanup triggered on both success AND failure/timeout? Run sustained operations and assert collection sizes stay bounded
- **Incomplete wiring** — Feature only works for some operation types (e.g., router feedback wired for GET but not subscribe/put/update). When debugging "X doesn't work for operation Y," check all enum variants in the dispatch path — commented-out arms, `_ => Irrelevant` catch-alls, and missing match arms are common
- **TTL/timing race conditions** — Two time-dependent operations where the first can expire before the second completes (e.g., transient TTL expires before CONNECT handshake, interest TTL expires before subscription renewal, broadcast fires before subscriptions complete). Check: what happens if operation A takes longer than timeout B?
- **Regressions from "safe" changes** — A seemingly harmless change (code simplification, removing a feature flag, changing defaults) breaks an invariant that nothing tests. When a recent commit looks innocent, check what implicit behaviors it removed
- **Mock/test divergence** — Bug can't be reproduced in tests because the mock runtime behaves differently from production. Check: does the mock skip side effects (e.g., BSC emission)? Does the test use a different code path than production (e.g., explicit subscribe vs background subscribe)? Does the mock socket behave differently from real UDP?

See [Module-Specific Debugging Guide](references/module-debugging.md) for detailed bug patterns, data collection strategies, and test approaches per module.

### Phase 3: Investigate Systematically

**For each hypothesis:**
1. Identify what evidence would confirm or refute it
2. Gather that evidence (logs, code reading, adding debug output)
3. Update hypothesis ranking based on findings
4. Move to next hypothesis if current one is eliminated

**Freenet-specific data gathering:**

| What You Need | How to Get It | Access |
|---------------|---------------|--------|
| Event sequences | `RUST_LOG=info` + `--nocapture` on simulation tests | Everyone |
| Network message patterns | `sim.get_network_stats()` in simulation tests | Everyone |
| Convergence behavior | `sim.await_convergence(timeout, poll, min_contracts)` | Everyone |
| Virtual time state | `sim.virtual_time().now_nanos()` | Everyone |
| Git history of affected code | `git log --oneline -20 -- path/to/file.rs` | Everyone |
| Fault injection results | SimNetwork + FaultConfig, then inspect stats | Everyone |
| Gateway logs | Access to running gateway node | **Limited — not all contributors** |
| Aggregate telemetry | Production monitoring dashboards | **Limited — core team only** |
| Real network packet captures | Physical access to test machines | **Limited — specific environments** |

For module-specific data gathering techniques, see [Module-Specific Debugging Guide](references/module-debugging.md) — it covers observation APIs, `#[freenet_test]` event capture, `RUST_LOG` targets, and fault injection per module.

**Parallel investigation with subagents:**

Use `general-purpose` agents with `codebase-investigator` instructions for independent, readonly investigations. Spawn multiple in parallel, each with a specific focus.

```
Spawn investigators in parallel using Task tool (subagent_type="general-purpose"):

1. "You are a codebase-investigator. [Include agents/codebase-investigator.md instructions]
    Search for similar error handling patterns in the codebase related to [bug description]"

2. "You are a codebase-investigator. [Include agents/codebase-investigator.md instructions]
    Check git history for recent changes to [affected module/files]"

3. "You are a codebase-investigator. [Include agents/codebase-investigator.md instructions]
    Read and analyze [test file] and related fixtures for [component]"
```

Guidelines:
- Each investigator focuses on one hypothesis or evidence type
- Only parallelize readonly tasks — code changes must be sequential
- Investigators report findings; you synthesize and decide next steps

### Phase 4: Fix and Verify

1. **Fix the root cause** — Not symptoms
2. **Verify with deterministic reproduction** — Re-run the failing test with the same seed
3. **Check for regressions** — `cargo test -p freenet`
4. **Consider edge cases** — Does the fix handle similar scenarios?
5. **Verify determinism** — If you added new code, ensure it uses `TimeSource` and `GlobalRng` (not `std::time` / `rand` directly)

### Phase 5: Test Coverage Analysis

**Always ask: "Why didn't CI catch this?"**

Freenet has multiple test layers:

| Layer | Scope | What It Catches |
|-------|-------|-----------------|
| Unit tests (~1000) | Individual functions | Logic errors, algorithm bugs |
| Integration tests (~80) | Component interactions | Interface mismatches, data flow bugs |
| Simulation tests | Multi-node deterministic | State machine bugs, race conditions, protocol errors |
| `fdev single-process` | Quick multi-peer | Basic distributed behavior |
| `freenet-test-network` | 20+ peers in Docker | Scale-dependent bugs, realistic network behavior |
| Real network tests | Physical machines | NAT traversal, real latency, UDP behavior |

If a bug reached production or manual testing, there's a gap. Investigate:

1. **Which test layer should have caught this?**
   - Logic error → unit test
   - Component interaction bug → integration test
   - Distributed/state machine behavior → simulation test with `#[freenet_test]`
   - Fault tolerance → SimNetwork with FaultConfig
   - Scale-dependent → freenet-test-network

2. **Why didn't the existing tests catch it?**
   - Tests use different topology/configuration than production
   - Tests mock components that exhibit the bug in real usage
   - Simulation doesn't inject the right fault conditions
   - Test assertions too weak to detect the failure
   - Determinism violation — code path bypasses `TimeSource`/`GlobalRng`

3. **Document the gap** — Include in the issue/PR:
   - What test would have caught this
   - Why existing tests didn't
   - Whether a new test should be added to prevent regression

## Anti-Patterns to Avoid

### Jumping to conclusions
- **Wrong:** See error, immediately change code that seems related
- **Right:** Form hypothesis, gather evidence, then act

### Tunnel vision
- **Wrong:** Spend hours on one theory despite contradicting evidence
- **Right:** Set time bounds, pivot when evidence points elsewhere

### Weakening tests
- **Wrong:** Test fails, reduce assertions or add exceptions to make it pass
- **Right:** Understand why the test expects what it does, fix the code to meet that expectation
- **Exception:** The test itself has a bug or tests incorrect behavior (rare, requires clear justification)

### Sequential investigation when parallel is possible
- **Wrong:** Read file A, wait, read file B, wait, read file C
- **Right:** Spawn `codebase-investigator` agents to read A, B, C concurrently, synthesize findings

### Fixing without understanding
- **Wrong:** Copy a fix from Stack Overflow that makes the error go away
- **Right:** Understand why the fix works and whether it addresses root cause

### Skipping the scope ladder
- **Wrong:** Jump straight to real network debugging when the bug could be reproduced in a unit test
- **Right:** Start small — unit test, then simulation, then real network

### Breaking determinism
- **Wrong:** Use `std::time::Instant::now()` or `rand::random()` in core logic
- **Right:** Use `TimeSource` trait and `GlobalRng` so simulation tests remain reproducible

### Assuming data access
- **Wrong:** "Check the gateway logs to see what happened" (not everyone has gateway access)
- **Right:** Design reproduction steps using simulation tests and `RUST_LOG` that any contributor can run

## Checklist Before Declaring "Fixed"

- [ ] Root cause identified and understood
- [ ] Fix addresses root cause, not symptoms
- [ ] Original failure no longer reproduces
- [ ] No new test failures introduced
- [ ] Test added if one didn't exist (when practical)
- [ ] No test assertions weakened or disabled
- [ ] Answered "why didn't CI catch this?" and documented the test gap
