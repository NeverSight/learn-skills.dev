---
name: halmos
description: Halmos symbolic testing for Foundry — write symbolic Solidity tests that mathematically verify properties. Foundry-native (no new language), bounded model checking, counter-example generation, and lightweight alternative to Certora.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - halmos
  - symbolic-testing
  - formal-verification
  - security
  - foundry
---

# Halmos

Halmos is a symbolic testing tool for EVM smart contracts. It executes Foundry tests symbolically — instead of running with concrete random values like a fuzzer, it reasons about ALL possible inputs simultaneously. When an assertion fails, Halmos produces a concrete counter-example. Built by a16z, it requires no new language (unlike Certora's CVL) and no API key.

GitHub: https://github.com/a16z/halmos
Docs: https://github.com/a16z/halmos/wiki

## What You Probably Got Wrong

> LLMs conflate symbolic testing with fuzzing and full formal verification. These distinctions matter.

- **Halmos is BOUNDED, not full formal verification** — It checks properties up to N loop iterations and call depth. If your contract has an unbounded loop, Halmos verifies correctness only for the iterations you specify via `--loop`. This is weaker than Certora's unbounded reasoning but catches most real bugs.
- **Tests look like Foundry tests but execute symbolically** — A `function check_transfer(address to, uint256 amount)` test in Halmos does NOT run with random `to` and `amount`. The parameters are symbolic variables representing ALL possible values. Every `assert` must hold for every combination.
- **Pre-1.0 software — expect breaking changes** — Halmos is under active development. CLI flags, cheatcode support, and output format change between releases. Pin your version in CI.
- **No API key needed** — Unlike Certora Prover (which requires a paid API key and sends code to their cloud), Halmos runs entirely locally using an SMT solver (z3).
- **`vm.assume` is NOT `require`** — `vm.assume(condition)` tells the solver to only consider inputs where `condition` is true. It prunes the search space. If you over-constrain with too many assumes, you may verify a property only for a trivially small input set.
- **Symbolic != random** — Foundry's fuzzer (`forge test`) generates random inputs. Halmos's symbolic execution covers EVERY input within bounds. A fuzzer might miss the one value that breaks your invariant; Halmos will find it (if within bounds).
- **Counter-examples are concrete** — When Halmos finds a violation, it outputs specific values (e.g., `to = 0x0000...0000`, `amount = 115792...`). These are reproducible as standard Foundry tests.
- **Not all cheatcodes are supported** — Halmos supports a subset of Foundry cheatcodes. `vm.assume`, `vm.prank`, `vm.deal`, `vm.store`, `vm.load` work. Complex cheatcodes like `vm.ffi` and `vm.createSelectFork` are not supported.

## Installation

### Prerequisites

- Python 3.12+
- Foundry (`forge`, `anvil`)
- A Foundry project with compiled contracts

### Install via pip

```bash
pip install halmos
```

Verify installation:

```bash
halmos --version
```

### Pin version in CI

```bash
pip install halmos==0.2.1
```

> Last verified: February 2026. Check PyPI for latest: https://pypi.org/project/halmos/

## Quick Start

### 1. Create a Symbolic Test

Symbolic tests use the `check_` prefix (not `test_`). Parameters become symbolic inputs.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import {Test} from "forge-std/Test.sol";
import {SimpleToken} from "../src/SimpleToken.sol";

contract SimpleTokenSymTest is Test {
    SimpleToken token;
    address alice;
    address bob;

    function setUp() public {
        token = new SimpleToken("Test", "TST", 1000e18);
        alice = address(0x1);
        bob = address(0x2);
        deal(address(token), alice, 500e18);
    }

    /// @dev Transfer must not create or destroy tokens
    function check_transfer_preserves_supply(uint256 amount) public {
        vm.assume(amount <= token.balanceOf(alice));

        uint256 supplyBefore = token.totalSupply();

        vm.prank(alice);
        token.transfer(bob, amount);

        uint256 supplyAfter = token.totalSupply();
        assert(supplyBefore == supplyAfter);
    }
}
```

### 2. Run Halmos

```bash
halmos
```

Halmos automatically finds `check_` prefixed functions in your test files and executes them symbolically.

### 3. Read the Output

```
Running 1 tests for test/SimpleToken.t.sol:SimpleTokenSymTest
[PASS] check_transfer_preserves_supply(uint256) (paths: 3, time: 2.41s)
```

If a violation exists, Halmos outputs:

```
[FAIL] check_transfer_preserves_supply(uint256)
Counterexample:
    p_amount_uint256 = 0x0000...0001
```

## How It Works

### Symbolic Execution vs Fuzzing

| Aspect | Foundry Fuzzer | Halmos |
|--------|---------------|--------|
| Input generation | Random concrete values | Symbolic variables (ALL values) |
| Coverage | Statistical (more runs = more coverage) | Complete within bounds |
| Speed | Fast (milliseconds per run) | Slower (seconds to minutes per test) |
| Guarantees | "No bug found in N runs" | "No bug exists (within bounds)" |
| Counter-examples | Random failing input | Minimal concrete witness |
| Loop handling | Executes actual iterations | Bounded (--loop flag) |

### Execution Model

1. Halmos compiles your test contracts with `forge build`
2. It creates symbolic variables for each test function parameter
3. It executes the EVM bytecode symbolically — every branch creates a new execution path
4. At each `assert`, it asks the SMT solver (z3): "Is there ANY assignment to the symbolic variables that makes this assertion false?"
5. If yes, it returns the concrete counter-example. If no, the property is verified (within bounds).

### Path Explosion

Every `if` statement doubles the number of execution paths. A function with 20 conditional branches has up to 2^20 (1M+) paths. Halmos manages this through:

- **Path merging**: Combining paths with identical post-states
- **Solver timeout**: Abandoning paths that take too long (`--solver-timeout`)
- **Loop bounding**: Limiting loop iterations (`--loop`)
- **Early termination**: Stopping on first counter-example (`--early-exit`)

## Writing Symbolic Tests

### Function Naming Convention

```solidity
// Halmos runs functions prefixed with `check_`
function check_propertyName(uint256 x, address y) public { ... }

// Foundry fuzzer runs functions prefixed with `test`
function test_propertyName(uint256 x, address y) public { ... }

// Use `check_` for symbolic, `test` for fuzz — they can coexist
```

### Symbolic Inputs via Parameters

Every parameter to a `check_` function becomes a symbolic variable:

```solidity
function check_addition_commutative(uint256 a, uint256 b) public pure {
    // a and b represent ALL possible uint256 values simultaneously
    vm.assume(a <= type(uint128).max);
    vm.assume(b <= type(uint128).max);

    assert(a + b == b + a);
}
```

### Constraining Inputs with vm.assume

`vm.assume` prunes the symbolic search space. Use it to express preconditions:

```solidity
function check_withdraw(uint256 amount, address user) public {
    // Only consider valid inputs — not a limitation, a precondition
    vm.assume(user != address(0));
    vm.assume(amount > 0);
    vm.assume(amount <= vault.balanceOf(user));

    uint256 balBefore = token.balanceOf(user);

    vm.prank(user);
    vault.withdraw(amount);

    // Withdrawn amount must increase user's token balance
    assert(token.balanceOf(user) >= balBefore);
}
```

**Warning**: Over-constraining with `vm.assume` can make the test vacuously true. If no inputs satisfy all assumptions, the test passes trivially (no paths to check). Watch the path count in output — 0 paths means your assumptions are contradictory.

### Assertions

Halmos supports `assert()` for property checks. Do NOT use `assertEq`, `assertGt`, etc. from forge-std — these revert on failure and Halmos treats reverts as acceptable paths (the transaction just reverts, no invariant broken). Use raw `assert()`:

```solidity
// CORRECT: Halmos checks this symbolically
assert(balanceAfter >= balanceBefore);

// WRONG: assertEq reverts on failure — Halmos sees a revert, not a violation
assertEq(balanceAfter, balanceBefore);
```

> If you want Halmos to treat reverts as failures, use `--revert-as-failure` flag. But the default and recommended approach is `assert()`.

### Testing State Transitions

```solidity
function check_deposit_increases_shares(uint256 amount) public {
    vm.assume(amount > 0);
    vm.assume(amount <= 1e30);

    deal(address(token), address(this), amount);
    token.approve(address(vault), amount);

    uint256 sharesBefore = vault.balanceOf(address(this));
    vault.deposit(amount, address(this));
    uint256 sharesAfter = vault.balanceOf(address(this));

    // Depositing must increase shares
    assert(sharesAfter > sharesBefore);
}
```

## Bounded Model Checking

Halmos is a bounded model checker. It checks properties up to a configurable bound on loops and recursion depth.

### Loop Bounding with --loop

```bash
# Check with up to 3 loop iterations (default: 2)
halmos --loop 3
```

```solidity
function check_sum_array(uint256[] memory values) public pure {
    uint256 sum;
    // Halmos unrolls this loop up to --loop iterations
    for (uint256 i = 0; i < values.length; i++) {
        sum += values[i];
    }
    // With --loop 3, this is verified for arrays of length 0, 1, 2, 3
    assert(sum >= values[0]);
}
```

### What "Bounded" Means for Correctness

| Bound | Meaning |
|-------|---------|
| `--loop 2` | Properties hold for 0, 1, or 2 loop iterations |
| `--loop 10` | Properties hold for up to 10 iterations |
| `--loop 256` | Practically complete for most contracts (slow) |

**If a bug exists only at iteration 11 and you set `--loop 10`, Halmos will NOT find it.** Increase bounds for higher confidence at the cost of performance.

### Call Depth Bounding with --depth

```bash
# Limit symbolic execution depth (default: unbounded)
halmos --depth 100
```

This limits the depth of nested contract calls. Useful for contracts with deep delegation chains.

## Symbolic Storage

For tests that need symbolic state beyond function parameters, use Halmos's `svm` cheatcodes:

```solidity
import {SymTest} from "halmos-cheatcodes/SymTest.sol";

contract VaultSymTest is SymTest, Test {
    function check_invariant_with_symbolic_state() public {
        // Create symbolic values for contract state
        uint256 totalAssets = svm.createUint256("totalAssets");
        uint256 totalShares = svm.createUint256("totalShares");
        address depositor = svm.createAddress("depositor");

        vm.assume(totalShares > 0);
        vm.assume(totalAssets >= totalShares);

        // Store symbolic state into contract storage
        vm.store(
            address(vault),
            bytes32(uint256(0)), // totalAssets storage slot
            bytes32(totalAssets)
        );

        assert(vault.totalAssets() >= vault.totalShares());
    }
}
```

### Installing halmos-cheatcodes

```bash
forge install a16z/halmos-cheatcodes
```

### Available Symbolic Constructors

| Function | Description |
|----------|-------------|
| `svm.createUint256(string)` | Symbolic uint256 with label |
| `svm.createUint(uint256, string)` | Symbolic uint of N bits |
| `svm.createInt256(string)` | Symbolic int256 |
| `svm.createAddress(string)` | Symbolic address |
| `svm.createBytes32(string)` | Symbolic bytes32 |
| `svm.createBytes(uint256, string)` | Symbolic bytes of fixed length |
| `svm.createBool(string)` | Symbolic boolean |

## Counter-Example Interpretation

When Halmos finds a violation, it outputs concrete values:

```
[FAIL] check_no_overflow(uint256,uint256)
Counterexample:
    p_a_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    p_b_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000001
```

### Reading Counter-Examples

1. **Parameter naming**: `p_<name>_<type>` — `p_a_uint256` is the `a` parameter of type `uint256`
2. **Hex encoding**: Values are hex-encoded. Decode to decimal for readability
3. **Minimal witnesses**: Halmos tries to find the simplest failing input, but it depends on the solver

### Reproducing as a Foundry Test

Take the counter-example values and write a concrete test:

```solidity
function test_reproduce_overflow() public {
    // Counter-example from Halmos
    uint256 a = type(uint256).max;
    uint256 b = 1;

    // This should trigger the same assertion failure
    check_no_overflow(a, b);
}
```

Run with `forge test --match-test test_reproduce_overflow -vvvv` to get full traces.

## Configuration

### CLI Flags

```bash
# Run specific test function
halmos --function check_transfer

# Run tests in a specific contract
halmos --contract SimpleTokenSymTest

# Set solver timeout (milliseconds) — abandon paths that take too long
halmos --solver-timeout-assertion 60000

# Set loop iteration bound
halmos --loop 5

# Set call depth
halmos --depth 50

# Set symbolic execution timeout (seconds)
halmos --timeout 3600

# Run with branching to find all counter-examples
halmos --solver-timeout-branching 10000

# Set storage layout for symbolic storage access
halmos --storage-layout generic

# Print detailed solver statistics
halmos --statistics

# Early exit on first counter-example
halmos --early-exit

# Treat reverts as test failures
halmos --error-unknown

# Verbose output with execution traces
halmos -v

# Extra verbose output
halmos -vv
```

### Configuration via foundry.toml

Halmos reads from your `foundry.toml` for project configuration (src, out, remappings). Add a `[profile.halmos]` section for Halmos-specific settings:

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]

# Halmos runs on the default profile's compiled output
# Remappings are shared with forge
remappings = [
    "forge-std/=lib/forge-std/src/",
    "halmos-cheatcodes/=lib/halmos-cheatcodes/src/",
]
```

### halmos.toml (Dedicated Config)

For dedicated Halmos config, create a `halmos.toml` in your project root:

```toml
[global]
loop = 3
solver-timeout-assertion = 60000
storage-layout = "generic"
early-exit = true
```

## Comparison with Echidna

Echidna is a property-based fuzzer. Halmos is a symbolic executor. They complement each other.

| Aspect | Halmos | Echidna |
|--------|--------|---------|
| Approach | Symbolic (ALL inputs within bounds) | Fuzzing (random inputs, guided by coverage) |
| Completeness | Complete within bounds | Statistical (more runs = more confidence) |
| Speed per test | Seconds to minutes | Milliseconds per run, minutes for campaigns |
| Loop handling | Bounded (explicit limit) | Runs actual iterations |
| External calls | Limited symbolic support | Full concrete execution |
| Test language | Solidity (Foundry-native) | Solidity (custom harness) |
| Counter-examples | Exact minimal witness | Random failing input |
| Best for | Mathematical properties, overflow, access control | Complex stateful interactions, edge cases in business logic |
| Setup effort | Minimal (just `check_` functions) | Moderate (config file, assertion mode vs property mode) |

**Use both**: Write `check_` tests for Halmos (mathematical correctness within bounds) and Echidna property tests for complex stateful exploration.

## Comparison with Certora

Certora Prover is a full formal verification tool. Halmos is a lightweight bounded alternative.

| Aspect | Halmos | Certora Prover |
|--------|--------|----------------|
| Verification | Bounded model checking | Full formal verification (unbounded) |
| Specification language | Solidity (Foundry tests) | CVL (Certora Verification Language) |
| Learning curve | Low (write Solidity, prefix with `check_`) | High (learn CVL spec language) |
| Execution | Local (z3 solver) | Cloud (Certora's servers) |
| API key required | No | Yes (paid service) |
| Loop handling | Bounded (must specify limit) | Unbounded (proves for all iterations) |
| Cross-contract | Limited | Full support with linking |
| Quantifiers | Limited | Full first-order logic |
| Summaries | Not supported | Function summaries, harnesses |
| Maintenance | Pin version, expect breaking changes | Stable API, versioned specs |
| Best for | Quick property checks, CI integration | Critical protocol invariants, audit-grade proofs |

**When to use which**:
- **Halmos**: Quick sanity checks, CI/CD integration, teams without formal methods expertise, pre-audit verification
- **Certora**: Critical DeFi protocols, post-audit formal proofs, properties requiring unbounded reasoning

## Limitations

1. **Bounded verification only** — Cannot prove properties that require unbounded loop reasoning. A bug at iteration N+1 is invisible if `--loop N`.
2. **Solver timeouts on complex math** — Contracts with heavy fixed-point math, exponentiation, or complex bitwise operations can cause z3 timeouts. Use `--solver-timeout-assertion` to skip instead of hanging.
3. **Limited cross-contract symbolic execution** — External calls to unknown contracts are treated as returning arbitrary values. For complex multi-contract systems, each contract must be tested in isolation with assumptions about its dependencies.
4. **Not all EVM opcodes supported** — `CREATE2` with symbolic salt, `SELFDESTRUCT`, and some precompiles may not be fully supported.
5. **Memory and path explosion** — Contracts with many branches can cause exponential path growth. Use `--depth` and `--loop` aggressively for large contracts.
6. **Pre-1.0 stability** — The tool, CLI flags, and output format may change between releases. Pin versions in CI.
7. **No fork mode** — Cannot symbolically execute against forked mainnet state. Use Foundry fork tests for mainnet interaction testing.

## Tool Comparison Matrix

| Need | Tool | Why |
|------|------|-----|
| "Does this property hold for ALL inputs?" | **Halmos** | Symbolic execution covers every input within bounds |
| "Find edge cases in stateful interactions" | **Echidna** | Coverage-guided fuzzing explores complex state sequences |
| "Prove this property holds unconditionally" | **Certora** | Unbounded formal verification with CVL |
| "Quick regression test for known scenarios" | **Foundry** (unit tests) | Concrete tests are fast and readable |
| "Find bugs with random inputs" | **Foundry** (fuzz tests) | Built-in fuzzer, zero setup |
| "Gas optimization confidence" | **Foundry** (gas snapshots) | Not a verification tool — measure, don't prove |

## Recommended Workflow

### 1. Start with Foundry Fuzz Tests

Write `test_` functions with fuzz parameters. These run fast and catch obvious bugs:

```solidity
function test_transfer_noMint(address to, uint256 amount) public {
    vm.assume(to != address(0));
    vm.assume(amount <= token.balanceOf(alice));

    uint256 supplyBefore = token.totalSupply();
    vm.prank(alice);
    token.transfer(to, amount);
    assertEq(token.totalSupply(), supplyBefore);
}
```

### 2. Promote Critical Properties to Halmos

For properties that MUST hold (no false negatives acceptable), create `check_` equivalents:

```solidity
function check_transfer_noMint(address to, uint256 amount) public {
    vm.assume(to != address(0));
    vm.assume(amount <= token.balanceOf(alice));

    uint256 supplyBefore = token.totalSupply();
    vm.prank(alice);
    token.transfer(to, amount);
    assert(token.totalSupply() == supplyBefore);
}
```

### 3. Run in CI

```yaml
# .github/workflows/halmos.yml
name: Symbolic Tests
on: [push, pull_request]

jobs:
  halmos:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - uses: foundry-rs/foundry-toolchain@v1

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Halmos
        run: pip install halmos==0.2.1

      - name: Build
        run: forge build

      - name: Run symbolic tests
        run: halmos --solver-timeout-assertion 60000 --loop 5
```

### 4. Escalate to Certora for Critical Invariants

If a property requires unbounded reasoning (e.g., "the sum of all balances always equals totalSupply across ANY number of transfers"), Halmos cannot prove it. Write a CVL spec for Certora.

## References

- GitHub: https://github.com/a16z/halmos
- Wiki/Docs: https://github.com/a16z/halmos/wiki
- halmos-cheatcodes: https://github.com/a16z/halmos-cheatcodes
- a16z blog post: https://a16zcrypto.com/posts/article/symbolic-testing-with-halmos-leveraging-existing-tests-for-formal-verification/
- Trail of Bits — symbolic execution primer: https://blog.trailofbits.com/2023/09/19/introduction-to-symbolic-testing-with-halmos/
