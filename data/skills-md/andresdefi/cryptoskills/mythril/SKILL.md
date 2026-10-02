---
name: mythril
description: Mythril symbolic execution for Solidity — deep vulnerability detection via multi-transaction analysis, reentrancy, integer overflow, unchecked calls, and delegatecall exploits. Finds bugs that static analysis and fuzzing miss.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - mythril
  - symbolic-execution
  - security
  - solidity
  - consensys
---

# Mythril

Mythril is a symbolic execution tool for EVM bytecode that detects security vulnerabilities in Solidity smart contracts. It uses the LASER symbolic virtual machine to explore all reachable contract states across multiple transactions, then feeds path constraints to the Z3 SMT solver to generate concrete exploit inputs. It is maintained by Consensys Diligence.

Unlike static analyzers (Slither, Semgrep) that match code patterns, Mythril proves whether a vulnerability is actually exploitable by constructing valid transaction sequences that trigger it. This makes it slower but significantly more precise for certain vulnerability classes.

## What You Probably Got Wrong

> LLMs generate bad Mythril commands. These are the blind spots that cause wasted time and missed bugs.

- **Mythril is SLOW. Always set timeouts.** A single-contract analysis with default settings can run for 30+ minutes and consume 8+ GB of RAM. Production usage requires `--execution-timeout` and `--solver-timeout`. Without them, your CI pipeline will hang indefinitely.
- **Default analysis depth is often too shallow.** Without the `-t` (transaction count) flag, Mythril defaults to 2 transactions. Many real exploits (reentrancy across multiple functions, multi-step oracle manipulation) require `-t 3` or higher. But `-t 3` is exponentially slower than `-t 2` — 10x to 100x slower.
- **Docker is easier than pip install for most users.** Mythril depends on Z3 solver, py-solc-x, and specific Python versions. Docker (`myth` via `mythril/myth`) eliminates dependency hell. Pip install frequently fails due to Z3 build issues on macOS and certain Linux distros.
- **Mythril analyzes bytecode, not source.** It compiles your Solidity to bytecode first, then symbolically executes the bytecode. This means it does not understand variable names, function names, or Solidity-level constructs. The output references bytecode offsets, not source lines — unless you provide source maps.
- **`myth analyze` is the correct command.** The old `myth -x` syntax is deprecated. Use `myth analyze` for file analysis and `myth analyze --address` for on-chain contracts. `myth -x` may still work but produces deprecation warnings.
- **Mythril does NOT replace static analysis.** It finds different bugs. Slither catches style issues, missing access control patterns, and centralization risks in seconds. Mythril catches reachable state-dependent exploits in minutes to hours. Use both.
- **False positives happen, especially with `assert` violations.** Mythril reports any reachable `assert(false)` as a vulnerability. Custom `assert` statements used for invariant checking will trigger SWC-110 findings. Triage the output — not every finding is a real bug.
- **Solc version must match the contract pragma.** Mythril calls solc internally. If the installed solc version does not satisfy the pragma, compilation fails silently or with cryptic errors. Use `--solv` to specify the version.

## Installation

### Docker (Recommended)

```bash
docker pull mythril/myth

# Verify
docker run mythril/myth version
```

Run Mythril on a local file (mount the current directory):

```bash
docker run -v $(pwd):/src mythril/myth analyze /src/Contract.sol
```

### pip

Requires Python 3.8-3.12 and a working C++ compiler (for Z3).

```bash
pip3 install mythril
```

Verify:

```bash
myth version
```

If Z3 fails to build, install the system package first:

```bash
# Ubuntu/Debian
sudo apt-get install libz3-dev

# macOS
brew install z3

# Then retry
pip3 install mythril
```

### From Source

```bash
git clone https://github.com/Consensys/mythril.git
cd mythril
pip3 install -e .
```

### Specifying Solc Version

Mythril uses py-solc-x to manage compiler versions. Install the version your contracts need:

```bash
# Mythril installs solc automatically, but you can force a version
python3 -c "from solcx import install_solc; install_solc('0.8.28')"
```

Or specify at analysis time:

```bash
myth analyze Contract.sol --solv 0.8.28
```

## Quick Start

### Analyze a Single File

```bash
myth analyze contracts/Vault.sol
```

### Analyze with Specific Solc Version

```bash
myth analyze contracts/Vault.sol --solv 0.8.20
```

### Analyze a Specific Contract in a Multi-Contract File

```bash
myth analyze contracts/Token.sol --solc-args "--base-path . --include-path node_modules"
```

### Analyze Deployed Contract

```bash
myth analyze --address 0x1234...abcd --rpc infura-mainnet
```

Or with a custom RPC URL:

```bash
myth analyze --address 0x1234...abcd --rpc-url https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
```

## Analysis Depth

The `-t` flag controls how many transactions Mythril simulates in sequence. This is the single most important performance/coverage tradeoff.

| Flag | Transactions | Use Case | Time (typical) |
|------|-------------|----------|----------------|
| `-t 1` | 1 | Quick scan, single-function bugs | 30s - 2min |
| `-t 2` | 2 | Standard analysis (default) | 2 - 15min |
| `-t 3` | 3 | Deep analysis, multi-step exploits | 15min - 2hr+ |
| `-t 4+` | 4+ | Exhaustive, rarely practical | Hours to days |

```bash
# Quick scan for obvious issues
myth analyze Contract.sol -t 1 --execution-timeout 120

# Standard depth (default)
myth analyze Contract.sol -t 2 --execution-timeout 600

# Deep analysis — finds reentrancy across function pairs
myth analyze Contract.sol -t 3 --execution-timeout 3600
```

Each additional transaction multiplies the state space exponentially. A contract with 10 external functions has 10 possible first transactions, 100 possible two-transaction sequences, and 1,000 possible three-transaction sequences. Mythril prunes aggressively using symbolic constraints, but the growth is still significant.

### When to Use `-t 3`

- Reentrancy across different functions (attacker calls `withdraw` during `deposit` callback)
- Flash loan attack paths (borrow -> manipulate -> profit across 3+ calls)
- Multi-step privilege escalation (register -> claim role -> execute)
- State-dependent vulnerabilities where the setup requires 2+ prior transactions

## Detection Modules

Mythril maps findings to SWC (Smart Contract Weakness Classification) identifiers.

| Module | SWC | What It Finds |
|--------|-----|---------------|
| `ether_thief` | SWC-105 | Arbitrary ETH withdrawal via unprotected selfdestruct or call |
| `suicide` | SWC-106 | Unprotected `selfdestruct` callable by non-owner |
| `delegatecall` | SWC-112 | Delegatecall to user-controlled address |
| `reentrancy` | SWC-107 | State changes after external calls |
| `integer` | SWC-101 | Integer overflow/underflow (relevant for Solidity <0.8.0 or `unchecked` blocks) |
| `unchecked_retval` | SWC-104 | Unchecked return value on low-level calls |
| `tx_origin` | SWC-115 | `tx.origin` used for authentication |
| `exceptions` | SWC-110 | Reachable `assert` violations |
| `external_calls` | SWC-107 | Dangerous external call patterns |
| `arbitrary_write` | SWC-124 | Write to arbitrary storage location |
| `arbitrary_read` | N/A | Read from arbitrary storage location |
| `multiple_sends` | SWC-113 | Multiple ETH sends in single transaction (DoS risk) |
| `state_change_external_calls` | SWC-107 | State modification after external call |
| `dependence_on_predictable_vars` | SWC-116, SWC-120 | Weak randomness from block variables |

### Running Specific Modules

```bash
# Only check for reentrancy and unchecked return values
myth analyze Contract.sol -m reentrancy,unchecked_retval

# Exclude integer overflow checks (useful for 0.8.x contracts)
myth analyze Contract.sol --exclude-modules integer
```

## Output Formats

### Text (Default)

```bash
myth analyze Contract.sol
```

```
==== Unprotected Ether Withdrawal ====
SWC ID: 105
Severity: High
Contract: Vault
Function name: withdraw(uint256)
PC address: 1234
Estimated Gas Usage: 3456 - 7890

In the function `withdraw(uint256)` a non-zero amount of Ether is sent to
msg.sender.

There is a check on storage index 0. This storage slot can be written to by
calling the function `deposit()`.
----
Transaction Sequence:
  Caller: 0xdeadbeefdeadbeef...
  calldata: 0xd0e30db0...  (deposit)
  value: 1000000000000000000

  Caller: 0xdeadbeefdeadbeef...
  calldata: 0x2e1a7d4d...  (withdraw)
  value: 0
```

### JSON

```bash
myth analyze Contract.sol -o json > report.json
```

JSON output includes structured fields for each issue: `title`, `description`, `severity`, `address`, `contract`, `function`, `swc-id`, `min_gas_used`, `max_gas_used`, and `tx_sequence`.

### Markdown

```bash
myth analyze Contract.sol -o markdown > report.md
```

### JSONV2 (Machine-Readable with Source Mapping)

```bash
myth analyze Contract.sol -o jsonv2 > report.json
```

The `jsonv2` format includes source mappings and more detailed transaction sequence information, suitable for programmatic processing and CI tooling.

## Practical Settings

Production Mythril commands need explicit resource limits. Without them, analysis can consume all available memory and CPU time.

### Recommended Settings by Context

```bash
# CI pipeline — fast, bounded
myth analyze Contract.sol \
  -t 2 \
  --execution-timeout 300 \
  --solver-timeout 30 \
  --max-depth 50 \
  -o jsonv2

# Pre-audit deep scan — thorough, time-boxed
myth analyze Contract.sol \
  -t 3 \
  --execution-timeout 3600 \
  --solver-timeout 60 \
  --max-depth 128 \
  -o json

# Quick sanity check during development
myth analyze Contract.sol \
  -t 1 \
  --execution-timeout 120 \
  --solver-timeout 10
```

### Key Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--execution-timeout` | None (unlimited) | Max seconds for entire analysis |
| `--solver-timeout` | 10000 (ms) | Max time per Z3 query |
| `--max-depth` | 128 | Max depth of symbolic execution tree |
| `--loop-bound` | 3 | Max times to unroll loops |
| `--call-depth-limit` | 3 | Max depth for inter-contract calls |
| `--strategy` | `bfs` | Search strategy: `bfs`, `dfs`, `naive-random`, `weighted-random` |
| `--solver-log` | N/A | Path to log Z3 queries (debugging) |
| `--bin-runtime` | N/A | Analyze raw runtime bytecode |
| `--enable-physics` | N/A | Enable gas-based path prioritization |

### Docker with Resource Limits

```bash
# Limit Docker container to 4GB RAM and 2 CPUs
docker run \
  --memory=4g \
  --cpus=2 \
  -v $(pwd):/src \
  mythril/myth analyze /src/Contract.sol \
  -t 2 \
  --execution-timeout 300 \
  --solver-timeout 30
```

## Analyzing Deployed Contracts

Mythril can pull bytecode from any EVM chain and analyze it directly.

```bash
# Ethereum mainnet via Infura
myth analyze \
  --address 0xdAC17F958D2ee523a2206206994597C13D831ec7 \
  --rpc-url https://mainnet.infura.io/v3/YOUR_PROJECT_ID

# With transaction depth
myth analyze \
  --address 0xdAC17F958D2ee523a2206206994597C13D831ec7 \
  --rpc-url https://mainnet.infura.io/v3/YOUR_PROJECT_ID \
  -t 2 \
  --execution-timeout 600
```

On-chain analysis is slower because Mythril must resolve storage values and external contract dependencies via RPC calls.

### Analyzing Raw Bytecode

```bash
# Analyze compiled bytecode directly
myth analyze --bin-runtime -c "0x6080604052..."

# From a file containing bytecode
myth analyze --bin-runtime -f bytecode.bin
```

## CI Integration

### GitHub Actions

```yaml
name: Mythril Security Scan

on:
  pull_request:
    paths:
      - 'contracts/**'
      - 'src/**'

jobs:
  mythril:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - name: Run Mythril
        uses: docker://mythril/myth:latest
        with:
          args: >-
            analyze /github/workspace/src/Contract.sol
            --solv 0.8.28
            -t 2
            --execution-timeout 300
            --solver-timeout 30
            -o jsonv2

      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: mythril-report
          path: report.json
```

### Multi-Contract CI Scan

```bash
#!/usr/bin/env bash
set -euo pipefail

# Scan all Solidity files in src/, fail if any High severity issues found
FAILED=0

for sol_file in src/*.sol; do
  echo "Analyzing: $sol_file"
  if ! docker run --memory=4g -v "$(pwd)":/src mythril/myth analyze \
    "/src/$sol_file" \
    --solv 0.8.28 \
    -t 2 \
    --execution-timeout 300 \
    --solver-timeout 30 \
    -o json > "reports/$(basename "$sol_file" .sol).json" 2>&1; then
    echo "ISSUES FOUND in $sol_file"
    FAILED=1
  fi
done

exit $FAILED
```

## Comparison with Slither

Mythril and Slither are complementary, not competing tools.

| Aspect | Slither | Mythril |
|--------|---------|---------|
| **Approach** | Static analysis (AST pattern matching) | Symbolic execution (SMT solving) |
| **Speed** | Seconds | Minutes to hours |
| **Detectors** | 90+ detectors, many style/best-practice | ~15 modules, focused on exploitability |
| **False positives** | Higher (pattern-based) | Lower (proves exploitability) |
| **False negatives** | Misses state-dependent bugs | Misses pattern-based issues |
| **Multi-transaction** | No | Yes (core strength) |
| **Upgradeable contracts** | Good support | Limited |
| **CI suitability** | Excellent (fast) | Requires timeout tuning |
| **Output** | JSON, SARIF, markdown, text | JSON, JSONV2, markdown, text |
| **Install** | `pip install slither-analyzer` | `pip install mythril` or Docker |

### Recommended Workflow

1. **Slither first** — catches low-hanging fruit in seconds
2. **Fix all Slither High/Medium findings** — these are usually real
3. **Mythril second** — deep scan for state-dependent exploits
4. **Review Mythril findings manually** — verify the transaction sequences make sense
5. **Targeted Mythril runs** — use `-m` to focus on specific vulnerability classes

## Tool Comparison

| Tool | Type | Speed | Depth | Ease of Use | Best For |
|------|------|-------|-------|-------------|----------|
| **Slither** | Static analysis | Seconds | Pattern-based | Easy | Fast feedback, style, known patterns |
| **Mythril** | Symbolic execution | Minutes-hours | State-dependent | Medium | Proving exploitability, multi-tx bugs |
| **Echidna** | Fuzzing | Minutes-hours | Property-based | Medium | Custom invariant testing |
| **Halmos** | Symbolic testing | Minutes | Foundry-integrated | Medium | Formal verification in test framework |
| **Certora** | Formal verification | Minutes-hours | Full specification | Hard | Complete correctness proofs |
| **Semgrep** | Pattern matching | Seconds | Syntactic | Easy | Custom rules, large codebases |

### When to Use What

- **Every PR**: Slither (fast, catches regressions)
- **Pre-audit**: Mythril + Echidna (find state-dependent bugs before auditors do)
- **Critical DeFi**: Certora or Halmos (prove correctness properties mathematically)
- **Custom rules**: Semgrep (org-specific patterns across many repos)

## Common Pitfalls

### Solc Version Mismatch

```
mythril.exceptions.CompilerError: Solc experienced a fatal error
```

Fix: specify the correct solc version:

```bash
myth analyze Contract.sol --solv 0.8.28
```

### Import Resolution

Mythril cannot resolve imports by default. Provide paths:

```bash
myth analyze Contract.sol \
  --solc-args "--base-path . --include-path node_modules --include-path lib"
```

For Foundry projects with remappings:

```bash
myth analyze src/Contract.sol \
  --solc-args "--base-path . --include-path lib --allow-paths ."
```

### Timeout Without Results

If Mythril times out with no findings, it does not mean the contract is safe — it means analysis was incomplete. Increase the timeout or reduce scope:

```bash
# Focus on specific modules to reduce analysis scope
myth analyze Contract.sol -m reentrancy -t 2 --execution-timeout 600
```

### Memory Exhaustion

Large contracts with many state variables cause memory exhaustion. Limit with Docker:

```bash
docker run --memory=8g -v $(pwd):/src mythril/myth analyze /src/Contract.sol -t 2
```

## Reference

- Official repository: https://github.com/Consensys/mythril
- SWC Registry: https://swcregistry.io/
- Mythril documentation: https://mythril-classic.readthedocs.io/
- Consensys Diligence: https://consensys.io/diligence/

Last verified: February 2026
