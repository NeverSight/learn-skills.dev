---
name: certora
description: Certora formal verification with CVL — write mathematical proofs for smart contract correctness. Rules, invariants, ghost variables, hooks, parametric rules, multi-contract verification, and counter-example debugging.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - certora
  - formal-verification
  - cvl
  - security
  - solidity
---

# Certora Formal Verification

Write mathematical proofs that your smart contracts are correct for ALL possible inputs. Certora translates Solidity + CVL specifications into SMT formulas and exhaustively verifies them — no sampling, no random fuzzing, full coverage of the state space.

## What You Probably Got Wrong

> LLMs confuse CVL with Solidity, hallucinate syntax, and miss the fundamental workflow. Fix these blind spots first.

- **CVL is NOT Solidity** — It is a separate language (Certora Verification Language) with its own syntax, types, and semantics. You cannot use Solidity expressions like `abi.encode` or `keccak256` in CVL. CVL has `methods` blocks, `rule` declarations, `invariant`, `ghost`, and `hook` — none of which exist in Solidity.
- **Certora requires an API key** — The Prover runs on Certora's cloud infrastructure. You need a `CERTORAKEY` environment variable. Academic and open-source projects get free access. Commercial pricing is per-verification-minute.
- **Counter-examples are the key output** — When a rule fails, Certora produces a concrete counter-example showing exact call sequences, storage values, and variable assignments that violate your property. Reading these is the core skill — writing specs is secondary.
- **Verification is exhaustive, not sampling** — Unlike fuzz testing (Foundry, Echidna) which tests random inputs, Certora proves properties hold for ALL possible inputs, ALL possible call sequences, and ALL possible storage states. A passing rule means no counter-example exists.
- **`satisfy` is NOT `assert`** — `satisfy` checks reachability (can this state be reached?). `assert` checks universality (does this always hold?). Confusing them produces vacuously passing specs.
- **`require` in CVL constrains the prover, not the contract** — A CVL `require` narrows the search space. Over-constraining with too many `require` statements makes rules vacuously true (they pass because no valid execution exists). Use `rule_sanity` to catch this.
- **Loops need explicit bounds** — The Prover unrolls loops. Without `--loop_iter N` in your config, loops default to 1 iteration. Most real contracts need 3-7. Too high and verification times explode.
- **`mathint` is unbounded** — CVL's `mathint` type has no overflow. Use it for arithmetic in specs to avoid reasoning about overflow in the spec itself (the contract still has its Solidity overflow behavior).
- **Invariants use induction, not enumeration** — Certora proves invariants by assuming they hold at state N and proving they hold at state N+1. The base case (constructor) is checked separately. A failing invariant often means your `preserved` block is missing assumptions.

## Installation

### Install certoraRun CLI

```bash
pip install certora-cli
```

Requires Python 3.8.16+ and Java 11+. Solidity compiler (`solc`) must be on PATH.

### API Key Setup

```bash
# Get a key at https://www.certora.com/signup
export CERTORAKEY="your-api-key-here"

# Add to shell profile for persistence
echo 'export CERTORAKEY="your-key"' >> ~/.zshrc
```

### Verify Installation

```bash
certoraRun --version
```

### Install solc (if missing)

```bash
# macOS
brew install solidity

# Linux — use solc-select for version management
pip install solc-select
solc-select install 0.8.28
solc-select use 0.8.28
```

## Quick Start

Verify that an ERC-20 transfer cannot create tokens out of thin air.

### Contract (src/Token.sol)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    constructor() ERC20("Token", "TKN") {
        _mint(msg.sender, 1_000_000e18);
    }
}
```

### Spec (specs/Token.spec)

```cvl
methods {
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;
    function transfer(address, uint256) external returns (bool);
}

/// Transfer does not change total supply
rule transferPreservesTotalSupply(address to, uint256 amount) {
    env e;

    uint256 supplyBefore = totalSupply();

    transfer(e, to, amount);

    uint256 supplyAfter = totalSupply();

    assert supplyAfter == supplyBefore,
        "transfer must not change total supply";
}
```

### Config (certora/Token.conf)

```json
{
    "files": ["src/Token.sol"],
    "verify": "Token:specs/Token.spec",
    "solc": "solc",
    "optimistic_loop": true,
    "loop_iter": "3",
    "rule_sanity": "basic",
    "msg": "Token verification"
}
```

### Run

```bash
certoraRun certora/Token.conf
```

The CLI uploads sources to Certora's cloud, runs the Prover, and prints a link to the verification report.

## CVL Basics

### Methods Block

Declares which contract functions the spec can call. Functions marked `envfree` do not need an `env` argument.

```cvl
methods {
    // View functions — mark envfree (no msg.sender, msg.value needed)
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;
    function allowance(address, address) external returns (uint256) envfree;

    // State-changing functions — need env for msg.sender, msg.value
    function transfer(address, uint256) external returns (bool);
    function approve(address, uint256) external returns (bool);
    function transferFrom(address, address, uint256) external returns (bool);
}
```

### The `env` Type

Represents the EVM transaction context: `msg.sender`, `msg.value`, `block.timestamp`, etc.

```cvl
rule onlyOwnerCanMint(address to, uint256 amount) {
    env e;

    // Constrain the caller
    require e.msg.sender != owner();

    mint@withrevert(e, to, amount);

    assert lastReverted, "non-owner must not be able to mint";
}
```

### `calldataarg`

Represents arbitrary calldata — used in parametric rules to quantify over all function inputs.

```cvl
rule noFunctionChangesOwner(method f) {
    env e;
    calldataarg args;

    address ownerBefore = owner();

    f(e, args);

    assert owner() == ownerBefore, "owner must not change";
}
```

### `mathint`

Unbounded integer type. Use for spec-side arithmetic to avoid reasoning about overflow.

```cvl
rule transferConservesBalance(address from, address to, uint256 amount) {
    env e;
    require e.msg.sender == from;

    mathint balFromBefore = balanceOf(from);
    mathint balToBefore = balanceOf(to);

    require from != to;

    transfer(e, to, amount);

    mathint balFromAfter = balanceOf(from);
    mathint balToAfter = balanceOf(to);

    assert balFromAfter == balFromBefore - amount;
    assert balToAfter == balToBefore + amount;
}
```

### `assert` vs `satisfy`

```cvl
// assert: property must hold for ALL executions (universal)
rule balanceNeverNegative() {
    env e;
    assert balanceOf(e.msg.sender) >= 0;
}

// satisfy: at least ONE execution must reach this state (existential / reachability)
rule canTransferNonZero(address to) {
    env e;
    uint256 amount;
    require amount > 0;

    transfer(e, to, amount);

    satisfy balanceOf(to) > 0;
}
```

## Writing Rules

### Single-State Rules

Check a property about the state at one point in time.

```cvl
/// Zero address has no balance
rule zeroAddressHasNoBalance() {
    assert balanceOf(0) == 0,
        "zero address must have zero balance";
}
```

### Two-State Rules (Before/After)

The most common pattern — capture state before a function call, execute, check state after.

```cvl
/// Approve sets exact allowance
rule approveSetExact(address spender, uint256 amount) {
    env e;

    approve(e, spender, amount);

    assert allowance(e.msg.sender, spender) == amount,
        "allowance must equal approved amount";
}
```

### Revert Conditions with `@withrevert`

```cvl
/// Transfer reverts on insufficient balance
rule transferRevertsOnInsufficientBalance(address to, uint256 amount) {
    env e;

    require balanceOf(e.msg.sender) < amount;

    transfer@withrevert(e, to, amount);

    assert lastReverted,
        "must revert when balance < amount";
}
```

### Satisfy for Reachability

```cvl
/// It is possible to reach a state where someone has tokens
rule reachableNonZeroBalance() {
    env e;
    address user;

    satisfy balanceOf(user) > 0;
}
```

## Invariants

Invariants are properties that must hold in every reachable state. Certora proves them inductively: assume the invariant holds, execute any function, prove it still holds.

```cvl
/// Total supply equals sum of all balances
/// Uses a ghost variable to track the sum (see Ghost Variables section)
invariant totalSupplyIsSumOfBalances()
    to_mathint(totalSupply()) == sumOfBalances
    {
        preserved with (env e) {
            requireInvariant totalSupplyIsSumOfBalances();
        }
    }
```

### Preserved Blocks

The `preserved` block adds assumptions needed for the inductive step. Without it, the Prover assumes arbitrary starting states.

```cvl
invariant solvencyInvariant()
    to_mathint(totalSupply()) <= to_mathint(underlyingBalance())
    {
        preserved with (env e) {
            // The invariant itself must hold at the start of the step
            requireInvariant solvencyInvariant();
            // Exclude unrealistic states
            require e.msg.value == 0;
        }
        // Per-function preserved blocks for targeted assumptions
        preserved deposit(uint256 amount) with (env e) {
            requireInvariant solvencyInvariant();
            require amount > 0;
        }
    }
```

## Ghost Variables and Hooks

Ghosts are spec-side variables that track derived state the contract does not expose. Hooks update ghosts when contract storage changes.

### Sum-of-Balances Pattern

```cvl
// Ghost: sum of all balances (unbounded integer)
ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

// Hook: fires when the _balances mapping is updated
hook Sstore _balances[KEY address user] uint256 newBal (uint256 oldBal) {
    sumOfBalances = sumOfBalances + newBal - oldBal;
}

// Also handle loads for consistency
hook Sload uint256 val _balances[KEY address user] {
    require to_mathint(val) <= sumOfBalances;
}

invariant totalSupplyIsSumOfBalances()
    to_mathint(totalSupply()) == sumOfBalances
    {
        preserved with (env e) {
            requireInvariant totalSupplyIsSumOfBalances();
        }
    }
```

### Tracking Function Calls

```cvl
ghost uint256 transferCount {
    init_state axiom transferCount == 0;
}

hook Sstore _balances[KEY address user] uint256 newBal (uint256 oldBal) {
    if (newBal != oldBal) {
        transferCount = transferCount + 1;
    }
}
```

## Parametric Rules

Parametric rules quantify over ALL public/external functions. Use `method f` as a parameter and `calldataarg args` for arbitrary inputs.

```cvl
/// No function can decrease total supply (no burning)
rule totalSupplyNeverDecreases(method f) {
    env e;
    calldataarg args;

    uint256 supplyBefore = totalSupply();

    f(e, args);

    assert totalSupply() >= supplyBefore,
        "no function should decrease total supply";
}

/// Only the owner can change the fee
rule onlyOwnerChangeFee(method f) {
    env e;
    calldataarg args;

    uint256 feeBefore = fee();

    f(e, args);

    assert fee() != feeBefore => e.msg.sender == owner(),
        "only owner should change fee";
}
```

### Filtering Functions

```cvl
/// Skip view functions in parametric rules
rule noStateChangeFromView(method f) filtered {
    f -> !f.isView
} {
    env e;
    calldataarg args;

    uint256 supplyBefore = totalSupply();

    f(e, args);

    assert totalSupply() == supplyBefore || !f.isView;
}
```

## Multi-Contract Verification

### Linking Contracts

When your contract calls another contract, declare it in the config and link storage references.

```json
{
    "files": [
        "src/Vault.sol",
        "src/Token.sol"
    ],
    "verify": "Vault:specs/Vault.spec",
    "link": ["Vault:asset=Token"],
    "solc": "solc"
}
```

### Using Declarations

Reference external contracts in CVL.

```cvl
using Token as token;

methods {
    function token.balanceOf(address) external returns (uint256) envfree;
    function token.totalSupply() external returns (uint256) envfree;

    function deposit(uint256) external returns (uint256);
    function withdraw(uint256) external returns (uint256);
    function totalAssets() external returns (uint256) envfree;
}

rule depositIncreasesAssets(uint256 amount) {
    env e;

    mathint assetsBefore = totalAssets();

    deposit(e, amount);

    assert to_mathint(totalAssets()) >= assetsBefore,
        "deposit must not decrease total assets";
}
```

### Dispatchers

When the contract makes external calls to unknown addresses, use dispatchers to handle dynamic dispatch.

```cvl
methods {
    // DISPATCHER tells Certora to consider all known implementations
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
}
```

## Harnesses

Wrap internal functions to make them verifiable. Create a harness contract that exposes internals.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "../src/Vault.sol";

contract VaultHarness is Vault {
    constructor(IERC20 _asset) Vault(_asset) {}

    // Expose internal function for verification
    function convertToSharesPublic(uint256 assets) external view returns (uint256) {
        return _convertToShares(assets);
    }

    function convertToAssetsPublic(uint256 shares) external view returns (uint256) {
        return _convertToAssets(shares);
    }
}
```

Use the harness in your config:

```json
{
    "files": ["certora/harnesses/VaultHarness.sol", "src/Token.sol"],
    "verify": "VaultHarness:specs/Vault.spec",
    "link": ["VaultHarness:asset=Token"]
}
```

## Configuration (.conf file)

Core configuration options for `certoraRun`.

```json
{
    "files": ["src/Token.sol"],
    "verify": "Token:specs/Token.spec",
    "solc": "solc",

    "optimistic_loop": true,
    "loop_iter": "3",

    "rule_sanity": "basic",

    "msg": "Token verification run",

    "packages": [
        "@openzeppelin=node_modules/@openzeppelin"
    ],

    "solc_optimize": "200",

    "prover_args": [
        "-smt_hashingScheme plainInjectivity"
    ]
}
```

| Option | Purpose | Default |
|--------|---------|---------|
| `files` | Solidity source files to verify | Required |
| `verify` | `ContractName:path/to/spec.spec` | Required |
| `solc` | Path to Solidity compiler | `solc` |
| `optimistic_loop` | Assume loops terminate at `loop_iter` bound | `false` |
| `loop_iter` | Maximum loop iterations to unroll | `1` |
| `rule_sanity` | `none`, `basic`, or `advanced` — checks for vacuous rules | `none` |
| `msg` | Description shown in the dashboard | Empty |
| `packages` | Path mappings for imports | Empty |
| `link` | Link contract storage to other deployed contracts | Empty |
| `solc_optimize` | Optimizer runs (pass to solc) | Disabled |
| `rule` | Run only specific rules (comma-separated) | All rules |
| `method` | Run only specific methods in parametric rules | All methods |
| `prover_args` | Advanced Prover tuning flags | Empty |
| `smt_timeout` | Per-rule SMT solver timeout in seconds | `600` |

## Interpreting Counter-Examples

When a rule fails, the verification report contains a counter-example — a concrete execution trace that violates your property.

### Reading a Counter-Example

1. **Variable assignments** — Concrete values for all `env`, `calldataarg`, and rule parameters
2. **Call trace** — Exact sequence of function calls with arguments and return values
3. **Storage state** — Pre-state and post-state of all relevant storage slots
4. **Violated assertion** — Which `assert` failed and the concrete values

### Common Counter-Example Patterns

| Pattern | Meaning | Fix |
|---------|---------|-----|
| `msg.sender == address(0)` | Prover found violation with zero caller | Add `require e.msg.sender != 0` if your contract checks this |
| Sender and recipient are the same | Self-transfer edge case | Add `require from != to` or fix contract logic |
| Huge `msg.value` | Prover uses extreme values | Constrain with `require e.msg.value == 0` for non-payable |
| Intermediate overflow | Arithmetic overflow in spec math | Use `mathint` for spec-side calculations |
| Unreachable initial state | Invariant induction starts from impossible state | Add assumptions in `preserved` block |

### Debugging Workflow

```bash
# Run a single rule to isolate
certoraRun certora/Token.conf --rule transferPreservesTotalSupply

# Enable sanity checks to catch vacuity
certoraRun certora/Token.conf --rule_sanity advanced

# Increase timeout for complex rules
certoraRun certora/Token.conf --smt_timeout 1200

# Run with verbose output
certoraRun certora/Token.conf --prover_args "-depth 15"
```

## CI Integration

### GitHub Actions

```yaml
name: Certora Verification
on:
  pull_request:
    paths:
      - "src/**"
      - "specs/**"
      - "certora/**"

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "11"

      - name: Install solc
        run: |
          pip install solc-select
          solc-select install 0.8.28
          solc-select use 0.8.28

      - name: Install Certora CLI
        run: pip install certora-cli

      - name: Install dependencies
        run: npm ci

      - name: Run Certora verification
        env:
          CERTORAKEY: ${{ secrets.CERTORAKEY }}
        run: certoraRun certora/Token.conf
```

## Common Verification Patterns

### ERC-20: Total Supply = Sum of Balances

The canonical token invariant. Every mint/burn/transfer must preserve this equality.

```cvl
ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sstore _balances[KEY address user] uint256 newBal (uint256 oldBal) {
    sumOfBalances = sumOfBalances + newBal - oldBal;
}

invariant totalSupplyEqualsSumOfBalances()
    to_mathint(totalSupply()) == sumOfBalances
    {
        preserved with (env e) {
            requireInvariant totalSupplyEqualsSumOfBalances();
        }
    }
```

### Vault: Share Accounting Correctness

```cvl
/// Deposit and immediate withdraw returns at least amount minus rounding
rule depositWithdrawRoundTrip(uint256 assets) {
    env e;

    require assets > 0;
    require assets <= totalAssets();

    uint256 shares = deposit(e, assets);
    uint256 returned = withdraw(e, shares);

    // Rounding can lose at most 1 wei
    assert returned >= assets - 1,
        "deposit then withdraw must return assets minus rounding";
}

/// Share price is monotonically non-decreasing (no inflation attack)
rule sharePriceNeverDecreases(method f) filtered {
    f -> !f.isView
} {
    env e;
    calldataarg args;

    // Share price = totalAssets / totalSupply
    mathint priceBefore = totalSupply() > 0
        ? to_mathint(totalAssets()) * 1e18 / to_mathint(totalSupply())
        : 1e18;

    f(e, args);

    mathint priceAfter = totalSupply() > 0
        ? to_mathint(totalAssets()) * 1e18 / to_mathint(totalSupply())
        : 1e18;

    assert priceAfter >= priceBefore,
        "share price must never decrease";
}
```

### Access Control: Monotonic Permissions

```cvl
/// Admin role can only be revoked by explicit call, never silently lost
rule adminNeverSilentlyRevoked(method f) filtered {
    f -> f.selector != sig:revokeRole(bytes32,address).selector
      && f.selector != sig:renounceRole(bytes32,address).selector
} {
    env e;
    calldataarg args;
    address user;

    bool isAdminBefore = hasRole(DEFAULT_ADMIN_ROLE(), user);

    f(e, args);

    assert isAdminBefore => hasRole(DEFAULT_ADMIN_ROLE(), user),
        "admin role must not be silently removed";
}
```

### Lending: Solvency Invariant

```cvl
/// Protocol always has enough collateral to cover all borrows
invariant solvencyInvariant()
    totalCollateralValue() >= totalBorrowValue()
    {
        preserved with (env e) {
            requireInvariant solvencyInvariant();
            require e.msg.value == 0;
        }
        preserved liquidate(address borrower, uint256 amount) with (env e) {
            requireInvariant solvencyInvariant();
        }
    }
```

## Tool Comparison

| Tool | Type | Coverage | Speed | Learning Curve | Best For |
|------|------|----------|-------|---------------|----------|
| **Slither** | Static analysis | Pattern-based | Seconds | Low | Quick vulnerability scan, CI gate |
| **Mythril** | Symbolic execution | Path-based | Minutes | Medium | Finding concrete exploits |
| **Echidna** | Fuzz testing | Random sampling | Minutes | Medium | Stateful property testing |
| **Halmos** | Symbolic testing | Bounded | Minutes-hours | Medium | Foundry-native symbolic testing |
| **Certora** | Formal verification | Exhaustive (SMT) | Minutes-hours | High | Mathematical correctness proofs |
| **Semgrep** | Pattern matching | Rule-based | Seconds | Low | Custom lint rules, code patterns |

**When to use Certora over alternatives:**
- You need mathematical certainty, not probabilistic confidence
- The property involves numeric invariants (token accounting, share pricing)
- The protocol handles significant value and the cost of a bug exceeds the cost of verification
- You want CI-integrated continuous verification as code changes

## Recommended Workflow

1. **Start with Slither** — catch low-hanging fruit in seconds
2. **Write Foundry fuzz tests** — cover happy paths and edge cases
3. **Write Certora specs** for critical invariants:
   - Token accounting (supply = sum of balances)
   - Access control (permissions monotonicity)
   - Economic properties (solvency, share pricing)
4. **Run with `rule_sanity basic`** — catch vacuous rules early
5. **Debug counter-examples** — the most valuable output of the entire process
6. **Add to CI** — verify on every PR that touches contracts or specs

## References

- Certora Documentation: https://docs.certora.com
- CVL Language Reference: https://docs.certora.com/en/latest/docs/cvl/index.html
- Certora Examples Repository: https://github.com/Certora/Examples
- Certora Tutorials: https://docs.certora.com/en/latest/docs/user-guide/tutorials.html
- ERC-20 Spec Example: https://github.com/Certora/Examples/tree/master/CVLByExample
- Certora Prover CLI: https://docs.certora.com/en/latest/docs/prover/cli/options.html

Last verified: February 2026
