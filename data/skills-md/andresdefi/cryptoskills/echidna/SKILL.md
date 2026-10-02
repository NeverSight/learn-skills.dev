---
name: echidna
description: Echidna property-based fuzzer for Solidity — property mode, assertion mode, optimization mode, invariant writing, corpus management, config tuning, and Foundry integration. Catch bugs that static analysis misses with stateful fuzzing.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - echidna
  - fuzzing
  - property-testing
  - security
  - trail-of-bits
---

# Echidna

Echidna is a property-based fuzzer for Ethereum smart contracts built by Trail of Bits. It generates random sequences of transactions to find violations of user-defined properties. Unlike static analysis (Slither) or symbolic execution (Mythril), Echidna executes real EVM bytecode with coverage-guided mutation — it learns which inputs reach new code paths and explores deeper.

## What You Probably Got Wrong

> LLMs treat Echidna like "just run the fuzzer." The hard part is designing properties, not invoking the tool.

- **Property design is the entire game** — Running `echidna .` on a contract with weak properties proves nothing. A property that always returns `true` passes 100% of the time and catches 0% of bugs. Invest time in thinking about what invariants your protocol must maintain.
- **Echidna is stateful, not stateless** — Unlike Foundry fuzz tests that run one function with random inputs, Echidna generates sequences of multiple transactions. It calls function A, then B, then C, checking properties after each. This is how it catches bugs that require specific state setup.
- **Assertion mode catches panics, not properties** — In assertion mode, Echidna looks for `assert()` failures and Solidity panics (division by zero, overflow in unchecked blocks, array out of bounds). It does NOT check `echidna_*` functions. These are two different testing strategies.
- **`echidna_` prefix is mandatory in property mode** — Properties must be public/external functions starting with `echidna_` that take no arguments and return `bool`. Naming a function `check_invariant()` does nothing — Echidna ignores it.
- **Corpus is your most valuable artifact** — The corpus directory contains minimized transaction sequences that achieve new coverage. Save it between runs. Share it with your team. It makes subsequent runs converge faster.
- **Echidna does NOT support Foundry cheatcodes** — `vm.prank`, `vm.deal`, `vm.warp` do not work in Echidna. For time-dependent properties, use `hevm`-compatible cheatcodes or restructure your test harness with helper functions.
- **Shrinking is not optional** — When Echidna finds a failing sequence of 50 transactions, shrinking reduces it to the minimal reproducing sequence (often 2-3 calls). Without shrinking, debugging is painful.
- **More runs does not mean better coverage** — 1 million random transactions with bad properties are worth less than 10,000 with good properties. Coverage-guided mutation helps, but only if your test harness exposes meaningful state transitions.

## Installation

### Prebuilt Binaries (Recommended)

Download the latest release from GitHub:

```bash
# macOS (Apple Silicon)
curl -L https://github.com/crytic/echidna/releases/latest/download/echidna-arm64-macos.tar.gz | tar xz
sudo mv echidna /usr/local/bin/

# macOS (Intel)
curl -L https://github.com/crytic/echidna/releases/latest/download/echidna-x86_64-macos.tar.gz | tar xz
sudo mv echidna /usr/local/bin/

# Linux (x86_64)
curl -L https://github.com/crytic/echidna/releases/latest/download/echidna-x86_64-linux.tar.gz | tar xz
sudo mv echidna /usr/local/bin/
```

Verify installation:

```bash
echidna --version
```

### Docker

```bash
docker pull ghcr.io/crytic/echidna/echidna:latest

# Run on current directory
docker run --rm -v $(pwd):/src ghcr.io/crytic/echidna/echidna echidna /src/test/EchidnaTest.sol --contract EchidnaTest
```

### Building from Source

Requires GHC 9.x and Stack:

```bash
git clone https://github.com/crytic/echidna.git
cd echidna
stack install
```

### Solc Requirement

Echidna needs `solc` on PATH. Install the version matching your contracts:

```bash
pip3 install solc-select
solc-select install 0.8.28
solc-select use 0.8.28
```

## Quick Start

### Minimal Property Test

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Counter {
    uint256 public count;

    error Overflow();

    function increment() external {
        if (count >= 100) revert Overflow();
        count += 1;
    }

    function decrement() external {
        if (count == 0) return;
        count -= 1;
    }
}
```

Test harness:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./Counter.sol";

contract CounterTest is Counter {
    // Property: count never exceeds 100
    function echidna_count_bounded() public view returns (bool) {
        return count <= 100;
    }

    // Property: count is always valid (non-negative is guaranteed by uint256)
    function echidna_count_valid() public view returns (bool) {
        return count <= 100;
    }
}
```

Run:

```bash
echidna test/CounterTest.sol --contract CounterTest
```

Output when all properties hold:

```
echidna_count_bounded: passing
echidna_count_valid: passing

Unique instructions: 42
Corpus size: 3
```

## Testing Modes

### Property Mode (Default)

Properties are functions prefixed with `echidna_` that return `bool`. Echidna calls random contract functions between property checks. A property failure means the function returned `false`.

```solidity
contract TokenPropertyTest is MyToken {
    // MUST: public/external, no args, returns bool, starts with echidna_
    function echidna_total_supply_bounded() public view returns (bool) {
        return totalSupply() <= MAX_SUPPLY;
    }

    function echidna_zero_address_has_no_balance() public view returns (bool) {
        return balanceOf(address(0)) == 0;
    }
}
```

```bash
echidna test/TokenPropertyTest.sol --contract TokenPropertyTest
```

### Assertion Mode

Instead of `echidna_*` functions, assertion mode looks for `assert()` failures and Solidity panic codes. Useful for inline checks within functions.

```solidity
contract VaultAssertionTest is Vault {
    function deposit_and_check(uint256 amount) public {
        if (amount == 0 || amount > 1e30) return;

        uint256 totalBefore = totalAssets();
        deposit(amount);
        uint256 totalAfter = totalAssets();

        // Assertion mode catches this failure
        assert(totalAfter >= totalBefore);
    }
}
```

```bash
echidna test/VaultAssertionTest.sol --contract VaultAssertionTest --test-mode assertion
```

Config equivalent:

```yaml
testMode: "assertion"
```

### Optimization Mode

Finds inputs that maximize or minimize a numeric value. Functions must start with `echidna_optimize_` and return `int256`.

```solidity
contract GasOptimizeTest is MyContract {
    // Echidna tries to MAXIMIZE the return value
    function echidna_optimize_gas_usage() public returns (int256) {
        uint256 gasBefore = gasleft();
        complexOperation();
        uint256 gasUsed = gasBefore - gasleft();
        return int256(gasUsed);
    }

    // Find the maximum extractable value
    function echidna_optimize_max_withdrawal() public returns (int256) {
        uint256 balance = address(this).balance;
        exploit();
        uint256 stolen = balance - address(this).balance;
        return int256(stolen);
    }
}
```

```bash
echidna test/GasOptimizeTest.sol --contract GasOptimizeTest --test-mode optimization
```

### Dapptest Mode

Compatible with `ds-test`/`forge-std` style test functions. Functions starting with `test` that revert are treated as failures.

```bash
echidna test/FoundryStyleTest.sol --contract FoundryStyleTest --test-mode dapptest
```

## Writing Properties

### Invariant Categories

#### 1. Conservation Properties (Most Important)

Assets in = assets out. Nothing created from nothing.

```solidity
contract ERC20InvariantTest is MyToken {
    // Total supply equals sum of all known balances
    function echidna_supply_conservation() public view returns (bool) {
        return totalSupply() <= MAX_SUPPLY;
    }

    // Transfers do not create or destroy tokens
    function echidna_no_token_creation() public view returns (bool) {
        return totalSupply() == _initialSupply;
    }
}
```

#### 2. Access Control Properties

Only authorized actors can perform privileged operations.

```solidity
contract AccessControlTest is Ownable, MyProtocol {
    address constant ECHIDNA_CALLER = address(0x10000);

    // Non-owner should never be able to change critical params
    function echidna_only_owner_sets_fee() public view returns (bool) {
        if (msg.sender != owner()) {
            return fee() == _initialFee;
        }
        return true;
    }
}
```

#### 3. State Machine Properties

Valid state transitions only.

```solidity
contract AuctionTest is Auction {
    // Once ended, auction cannot restart
    function echidna_no_restart_after_end() public view returns (bool) {
        if (hasEnded) {
            return !isActive;
        }
        return true;
    }

    // Bid must be higher than current highest
    function echidna_bids_monotonic() public view returns (bool) {
        return highestBid >= _previousHighestBid;
    }
}
```

#### 4. Solvency Properties

Protocol always has enough to cover its obligations.

```solidity
contract VaultInvariantTest is Vault {
    // Vault holds at least as much as it owes
    function echidna_solvent() public view returns (bool) {
        return token.balanceOf(address(this)) >= totalDebt();
    }

    // No share holder can extract more than total assets
    function echidna_no_excess_withdrawal() public view returns (bool) {
        if (totalSupply() == 0) return true;
        uint256 maxWithdraw = previewRedeem(totalSupply());
        return maxWithdraw <= token.balanceOf(address(this));
    }
}
```

### Property Design Patterns

#### Bounded State Helper

Constrain fuzz inputs to meaningful ranges within the test harness:

```solidity
contract BoundedTest is MyProtocol {
    // Helper: Echidna calls this with random amounts
    function deposit_bounded(uint256 amount) public {
        // Skip meaningless inputs instead of reverting
        if (amount == 0 || amount > 1e24) return;
        token.mint(msg.sender, amount);
        token.approve(address(this), amount);
        deposit(amount);
    }

    function echidna_total_deposits_tracked() public view returns (bool) {
        return totalDeposits == token.balanceOf(address(this));
    }
}
```

#### Ghost Variables for Tracking

Track cumulative state that the contract itself doesn't store:

```solidity
contract GhostTracker is MyToken {
    uint256 internal _ghostTotalMinted;
    uint256 internal _ghostTotalBurned;

    function mint(address to, uint256 amount) public override {
        super.mint(to, amount);
        _ghostTotalMinted += amount;
    }

    function burn(uint256 amount) public override {
        super.burn(amount);
        _ghostTotalBurned += amount;
    }

    function echidna_mint_burn_conservation() public view returns (bool) {
        return totalSupply() == _ghostTotalMinted - _ghostTotalBurned;
    }
}
```

## Corpus Management

### How Corpus Works

Echidna maintains a corpus of transaction sequences that achieve new code coverage. Each entry is a minimized sequence of calls that reached a previously unseen execution path.

```yaml
# Save corpus to disk
corpusDir: "corpus"
```

```bash
# First run — builds corpus from scratch
echidna test/MyTest.sol --contract MyTest --corpus-dir corpus

# Subsequent runs — starts from existing corpus, finds new coverage faster
echidna test/MyTest.sol --contract MyTest --corpus-dir corpus
```

### Corpus Directory Structure

```
corpus/
├── coverage/           # Transaction sequences that hit new code paths
│   ├── 0001.txt       # Minimized call sequence
│   ├── 0002.txt
│   └── ...
└── reproducers/        # Transaction sequences that violate properties
    ├── 0001.txt
    └── ...
```

### Seeding the Corpus

Provide initial transaction sequences to guide the fuzzer:

```yaml
# Use a dictionary of interesting values
dictionary: "dict.txt"
```

Dictionary file format:

```
# dict.txt — one value per line, hex encoded
0x0000000000000000000000000000000000000000000000000000000000000000
0x0000000000000000000000000000000000000000000000000000000000000001
0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
0x00000000000000000000000000000000000000000000000000000000deadbeef
```

### Replaying Corpus

```bash
# Replay all saved reproducers to verify they still fail
echidna test/MyTest.sol --contract MyTest --corpus-dir corpus
```

## Configuration

### echidna.yaml Basics

```yaml
# Number of transactions to generate per test
testLimit: 50000

# Maximum transaction sequence length before checking properties
seqLen: 100

# Shrink failing sequences to minimal reproduction
shrinkLimit: 5000

# Testing mode: "property" | "assertion" | "optimization" | "dapptest"
testMode: "property"

# Addresses
deployer: "0x30000"
sender: ["0x10000", "0x20000", "0x30000"]
contractAddr: "0x00a329c0648769A73afAc7F9381E08FB43dBEA72"

# Corpus persistence
corpusDir: "corpus"

# Compilation
cryticArgs: ["--solc-remaps", "@openzeppelin/=lib/openzeppelin-contracts/"]

# Coverage
coverage: true

# Workers (parallel fuzzing)
workers: 4

# Timeout per test in seconds (0 = no timeout)
testTimeout: 300

# Balance of test contract in wei
balanceContract: 0xffffffffffffffffffffffff

# Balance of sender addresses
balanceAddr: 0xffffffffffffffffffffffff
```

### Key Configuration Decisions

**testLimit** — Default is 50,000. For CI, use 10,000-50,000. For deep campaigns, use 500,000-5,000,000. Higher is not always better if properties are weak.

**seqLen** — Maximum number of transactions in a single test sequence. Default is 100. Increase for protocols where bugs require long setup sequences (lending protocols, governance). Decrease for simple contracts to speed up exploration.

**shrinkLimit** — How many attempts Echidna makes to minimize a failing sequence. Default is 5,000. Higher values give cleaner reproducers but take longer.

**workers** — Parallel fuzzing workers. Set to your CPU core count. Each worker explores independently and shares coverage.

**sender** — Addresses that Echidna uses as `msg.sender`. By default, three addresses. Add more for multi-user interaction testing. The deployer is NOT automatically a sender.

## Multi-Contract Testing

### Testing a System of Contracts

Create a test harness that deploys and wires up all contracts:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "../src/Token.sol";
import "../src/Vault.sol";
import "../src/PriceOracle.sol";

contract SystemTest {
    Token public token;
    Vault public vault;
    PriceOracle public oracle;

    constructor() {
        token = new Token("Test", "TST", 18);
        oracle = new PriceOracle();
        vault = new Vault(address(token), address(oracle));

        // Seed initial state
        token.mint(address(this), 1_000_000e18);
        token.approve(address(vault), type(uint256).max);

        // Fund sender addresses so they can interact
        token.mint(address(0x10000), 100_000e18);
        token.mint(address(0x20000), 100_000e18);
    }

    // Expose vault functions for Echidna to call
    function deposit(uint256 amount) public {
        if (amount == 0 || amount > token.balanceOf(msg.sender)) return;
        vault.deposit(amount);
    }

    function withdraw(uint256 shares) public {
        if (shares == 0 || shares > vault.balanceOf(msg.sender)) return;
        vault.withdraw(shares);
    }

    function updatePrice(uint256 price) public {
        if (price == 0 || price > 1e36) return;
        oracle.setPrice(price);
    }

    // System-wide invariant
    function echidna_vault_solvent() public view returns (bool) {
        return token.balanceOf(address(vault)) >= vault.totalDebt();
    }

    function echidna_total_supply_matches() public view returns (bool) {
        return vault.totalSupply() <= vault.totalAssets();
    }
}
```

Config for multi-contract:

```yaml
testLimit: 100000
seqLen: 200
sender: ["0x10000", "0x20000"]
deployer: "0x30000"
# allContracts: true makes Echidna call functions on ALL deployed contracts
allContracts: true
corpusDir: "corpus"
workers: 4
```

```bash
echidna test/SystemTest.sol --contract SystemTest --config echidna.yaml
```

## Foundry Integration

### Using Echidna with Forge Projects

Echidna works with Foundry project layouts. Set compilation args to use `forge`'s remappings:

```yaml
# echidna.yaml for a Foundry project
cryticArgs: ["--compile-force-framework", "foundry"]
corpusDir: "corpus"
testLimit: 50000
```

Alternatively, pass remappings explicitly:

```yaml
cryticArgs: [
  "--solc-remaps",
  "@openzeppelin/=lib/openzeppelin-contracts/src/;forge-std/=lib/forge-std/src/"
]
```

### Project Structure with Both Tools

```
project/
├── foundry.toml
├── echidna.yaml
├── src/
│   └── Token.sol
├── test/
│   ├── Token.t.sol              # Foundry unit/fuzz tests
│   └── echidna/
│       └── TokenEchidna.sol     # Echidna property tests
├── corpus/                       # Echidna corpus (gitignore in CI, commit for shared campaigns)
└── lib/
    └── forge-std/
```

### Running Both in CI

```yaml
# .github/workflows/security.yml
name: Security
on: [push, pull_request]

jobs:
  foundry-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      - uses: foundry-rs/foundry-toolchain@v1
      - run: forge test --fuzz-runs 10000

  echidna:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      - name: Install Echidna
        run: |
          curl -L https://github.com/crytic/echidna/releases/latest/download/echidna-x86_64-linux.tar.gz | tar xz
          sudo mv echidna /usr/local/bin/
      - name: Install solc
        run: |
          pip3 install solc-select
          solc-select install 0.8.28
          solc-select use 0.8.28
      - name: Run Echidna
        run: echidna test/echidna/TokenEchidna.sol --contract TokenEchidna --config echidna.yaml
```

## Shrinking

When Echidna finds a property violation, the raw failing sequence might be 50+ transactions. Shrinking iteratively removes and simplifies transactions to find the minimum reproducing case.

### How It Works

1. Echidna finds a sequence of N transactions that breaks a property
2. It tries removing each transaction and re-running
3. It tries simplifying inputs (smaller numbers, shorter data)
4. It repeats until no further reduction is possible (up to `shrinkLimit`)

### Reading Shrunk Output

```
echidna_no_free_tokens: failed!
  Call sequence:
    mint(115792089237316195423570985008687907853269984665640564039457584007913129639935)
    transfer(0x10000, 1)

  Shrunk 47/50 times
```

This tells you: the original failing sequence was ~50 calls, but the minimal reproduction is just `mint` followed by `transfer` with specific arguments.

### Tuning Shrinking

```yaml
# More shrink attempts = cleaner reproducers, slower
shrinkLimit: 10000

# Fewer attempts = faster results, noisier reproducers
shrinkLimit: 1000
```

## Tool Comparison

| Tool | Type | Strengths | Limitations |
|------|------|-----------|-------------|
| **Slither** | Static analysis | Fast (<30s), CI-friendly, low false positives | Cannot find state-dependent bugs |
| **Mythril** | Symbolic execution | Finds deep logic bugs, path exploration | Slow on large contracts, state explosion |
| **Echidna** | Property-based fuzzing | Stateful, coverage-guided, corpus reuse | Only as good as your properties |
| **Foundry Fuzz** | Fuzz testing | Fast, Solidity-native, cheatcodes | Single-function (not stateful sequences) |
| **Halmos** | Symbolic testing | Formal verification in Solidity | Early stage, limited EVM support |
| **Certora** | Formal verification | Mathematical proofs of correctness | Expensive, custom specification language |
| **Semgrep** | Pattern matching | Custom rules, fast CI scans | Surface-level, no execution semantics |

## Recommended Workflow

### Development Phase

1. Write unit tests in Foundry first (fast feedback)
2. Add fuzz tests for individual functions (`testFuzz_*`)
3. Write Echidna properties for system-level invariants
4. Run Slither in CI on every PR

### Pre-Audit Phase

1. Run Echidna with high `testLimit` (500,000+) and long `seqLen` (200+)
2. Review corpus coverage — are there untested code paths?
3. Add properties for every critical invariant documented in the spec
4. Run optimization mode to find maximum extractable value

### Post-Deployment

1. Keep the Echidna test suite updated as the protocol evolves
2. Run campaigns against fork state for upgrade testing
3. Share corpus with auditors

## Common Pitfalls

### Properties That Always Pass

```solidity
// BAD: this always returns true because Echidna calls it from a non-owner address
function echidna_only_owner_mints() public view returns (bool) {
    return totalSupply() <= MAX_SUPPLY;
}
```

This property checks the effect (supply bounded) rather than the cause (unauthorized minting). If an attacker finds a way to mint without being owner but stays under MAX_SUPPLY, this property misses it.

```solidity
// BETTER: track actual minting behavior
function echidna_unauthorized_cannot_mint() public view returns (bool) {
    if (msg.sender != owner()) {
        return totalSupply() == _supplyAtLastOwnerAction;
    }
    return true;
}
```

### Constructor State Issues

Echidna deploys the contract once and then sends many transaction sequences. If your constructor sets up state that makes properties trivially true, you are testing nothing:

```solidity
// BAD: empty vault always passes solvency check
constructor() {
    // no initial deposits
}

function echidna_solvent() public view returns (bool) {
    return totalAssets() >= totalDebt(); // always 0 >= 0
}
```

Seed meaningful state in the constructor or use helper functions that Echidna can call to build up state.

## References

- [Echidna GitHub](https://github.com/crytic/echidna) — Source, releases, and issue tracker
- [Building Secure Contracts](https://secure-contracts.com/program-analysis/echidna/) — Trail of Bits tutorial series
- [Echidna Streaming Workshop](https://github.com/crytic/echidna-streaming-series) — Hands-on exercises
- [Not All Bugs Are Created Equal](https://blog.trailofbits.com/2023/02/14/not-all-bugs-are-created-equal/) — Trail of Bits on property design
- [crytic/properties](https://github.com/crytic/properties) — Reusable ERC-20/ERC-4626 property suites

Last verified: February 2026
