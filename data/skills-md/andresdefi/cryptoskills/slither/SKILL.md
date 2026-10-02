---
name: slither
description: Slither static analyzer for Solidity — installation, detector categories, triage workflow, custom detectors, printers, CI integration, and configuration. Run fast security scans on Hardhat and Foundry projects with 90+ built-in detectors.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - slither
  - static-analysis
  - security
  - solidity
  - trail-of-bits
---

# Slither

Slither is a Python-based static analysis framework for Solidity smart contracts, built by Trail of Bits. It runs 95+ vulnerability detectors in under a second, outputs machine-readable JSON, and provides a Python API for writing custom detectors. Works with Hardhat, Foundry, Brownie, and standalone Solidity files.

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Slither catches all bugs"** → Slither is a static analyzer — it examines code structure without executing it. It cannot catch runtime logic errors, economic exploits, or oracle manipulation. It complements fuzzing (Echidna/Halmos) and formal verification (Certora), not replaces them.
- **"All findings are vulnerabilities"** → Expect 30-60% false positive rate on real projects. The default detector set includes informational and optimization findings that are not security issues. Triage is mandatory — raw Slither output is not an audit report.
- **"Just run `slither .` and ship"** → Without configuration, Slither reports on every file including dependencies. You must filter paths (`--filter-paths`), exclude noise detectors, and configure `.slither.conf.json` for meaningful results.
- **`pip install slither`** → The package name is `slither-analyzer`, not `slither`. `pip install slither` installs an unrelated package.
- **"Slither requires Truffle"** → Slither works natively with Foundry (`forge build` output), Hardhat, and standalone `.sol` files. No JavaScript framework required.
- **"Install with npm"** → Slither is Python, not Node. Install via `uv`, `pip`, or Docker. It reads compilation artifacts from your framework but runs as a Python tool.
- **Old detector names** → Detector IDs change between versions. `reentrancy` was split into `reentrancy-eth`, `reentrancy-no-eth`, `reentrancy-benign`, `reentrancy-events`, and `reentrancy-unlimited-gas`. Always check `slither --list-detectors` for your version.
- **`--detect` vs `--exclude`** → `--detect` runs ONLY the listed detectors. `--exclude` runs everything EXCEPT the listed ones. Mixing them up gives either too few or too many results.

## Installation

### uv (recommended)

```bash
uv tool install slither-analyzer
```

### pip

```bash
pip install slither-analyzer
```

### Homebrew (macOS)

```bash
brew install slither-analyzer
```

### Docker

```bash
docker pull trailofbits/eth-security-toolbox
docker run -v $(pwd):/code trailofbits/eth-security-toolbox slither /code
```

### From source (development)

```bash
git clone https://github.com/crytic/slither.git
cd slither
uv sync --dev
```

Verify installation:

```bash
slither --version
```

Slither requires a Solidity compiler. Install `solc-select` to manage versions:

```bash
pip install solc-select
solc-select install 0.8.28
solc-select use 0.8.28
```

## Quick Start

### Foundry Project

```bash
cd my-foundry-project
forge build
slither .
```

Slither reads Foundry's compilation output automatically. If it fails, ensure `forge build` succeeds first.

### Hardhat Project

```bash
cd my-hardhat-project
npx hardhat compile
slither .
```

### Single Solidity File

```bash
slither contracts/Vault.sol
```

### Etherscan Verified Contract

```bash
slither 0xdAC17F958D2ee523a2206206994597C13D831ec7 --etherscan-apikey $ETHERSCAN_KEY
```

## Detector Categories

Slither organizes 95+ detectors by impact (severity) and confidence level.

### High Impact

Critical vulnerabilities that typically enable fund theft or contract destruction.

| Detector | Description |
|----------|-------------|
| `reentrancy-eth` | Reentrancy with ETH transfer — CEI violation allowing recursive calls |
| `arbitrary-send-eth` | Unprotected ETH transfer to attacker-controlled address |
| `arbitrary-send-erc20` | `transferFrom` where `from` is not `msg.sender` |
| `controlled-delegatecall` | User-controlled `delegatecall` destination — full storage takeover |
| `suicidal` | Unprotected `selfdestruct` callable by anyone |
| `uninitialized-state` | State variable used before assignment — reads as zero |
| `uninitialized-storage` | Local storage pointer overwrites critical state slots |
| `unchecked-transfer` | ERC20 `transfer`/`transferFrom` return value ignored |
| `weak-prng` | Pseudorandom number from `block.timestamp` or `blockhash` |
| `msg-value-loop` | `msg.value` reused in loop iteration — double-spend |
| `delegatecall-loop` | `delegatecall` inside loop with `payable` — msg.value reuse |
| `reentrancy-balance` | Reentrancy exploiting balance checks before external calls |
| `unprotected-upgrade` | Upgradeable proxy `initialize` callable by anyone |
| `incorrect-exp` | `^` (XOR) used instead of `**` (exponentiation) |
| `shadowing-state` | Derived contract shadows parent state variable |

### Medium Impact

Issues that can cause loss of funds under specific conditions or break protocol invariants.

| Detector | Description |
|----------|-------------|
| `reentrancy-no-eth` | Reentrancy without ETH transfer — state manipulation |
| `tx-origin` | `tx.origin` used for authorization — phishable |
| `incorrect-equality` | Strict `==` on balances — manipulable via direct transfer |
| `locked-ether` | Contract receives ETH but has no withdrawal function |
| `unused-return` | External call return value discarded — silent failure |
| `unchecked-lowlevel` | Low-level `.call()` return not checked |
| `unchecked-send` | `.send()` return value ignored |
| `divide-before-multiply` | Division truncates before multiplication — precision loss |
| `uninitialized-local` | Local variable used before assignment |
| `write-after-write` | Variable written twice without read between — dead write |
| `tautological-compare` | Variable compared to itself — always true/false |
| `mapping-deletion` | `delete` on struct containing mapping leaves mapping intact |
| `domain-separator-collision` | Function selector collides with EIP-2612 `DOMAIN_SEPARATOR()` |

### Low Impact

Code quality issues that may indicate bugs or increase attack surface.

| Detector | Description |
|----------|-------------|
| `missing-zero-check` | Address parameter not validated against `address(0)` |
| `calls-loop` | External calls inside loop — DoS if one call reverts |
| `timestamp` | Dangerous reliance on `block.timestamp` for logic |
| `reentrancy-benign` | Reentrancy with no harmful effect — may indicate design issue |
| `reentrancy-events` | Reentrancy that can reorder event emissions |
| `events-access` | Missing event for critical access control change |
| `events-maths` | Missing event for critical arithmetic parameter change |
| `return-bomb` | Callee returns huge data to consume caller's gas |
| `shadowing-local` | Local variable shadows state variable or function |

### Informational

Code style and best practice suggestions.

| Detector | Description |
|----------|-------------|
| `naming-convention` | Non-standard naming (camelCase, UPPER_CASE violations) |
| `solc-version` | Outdated or floating pragma version |
| `dead-code` | Internal function never called |
| `unused-state` | State variable declared but never read |
| `assembly` | Inline assembly usage (error-prone) |
| `low-level-calls` | Direct `.call()` / `.delegatecall()` usage |
| `pragma` | Multiple different pragma statements across files |
| `cyclomatic-complexity` | Function with complexity > 11 |
| `too-many-digits` | Literal with many digits (use `1e18` not `1000000000000000000`) |

### Optimization

Gas efficiency suggestions.

| Detector | Description |
|----------|-------------|
| `cache-array-length` | `array.length` evaluated on every loop iteration |
| `constable-states` | State variable never modified — should be `constant` |
| `immutable-states` | State variable set once in constructor — should be `immutable` |

List all detectors for your version:

```bash
slither --list-detectors
```

## Triage Workflow

Raw Slither output on a real project contains noise. Triage is the process of separating true findings from false positives.

### Step 1: Run with JSON output

```bash
slither . --json slither-report.json
```

### Step 2: Filter dependency paths

```bash
slither . --filter-paths "node_modules|lib/forge-std|lib/openzeppelin"
```

### Step 3: Exclude noise detectors

```bash
slither . \
  --exclude naming-convention,solc-version,pragma,dead-code,assembly \
  --exclude-informational \
  --exclude-optimization
```

### Step 4: Interactive triage

```bash
slither . --triage-mode
```

Slither prompts for each finding: hide or keep. Decisions are saved to `slither.db.json`. Subsequent runs skip hidden findings. Delete `slither.db.json` to reset.

### Step 5: Configuration file

Persist all filters in `.slither.conf.json`:

```json
{
  "filter_paths": "node_modules|lib/forge-std|lib/openzeppelin-contracts",
  "exclude_informational": true,
  "exclude_optimization": true,
  "exclude_low": false,
  "detectors_to_exclude": "naming-convention,solc-version,pragma,dead-code",
  "solc_remaps": "forge-std/=lib/forge-std/src/"
}
```

## Printers

Printers extract structural information from contracts without running detectors.

### Contract Overview

```bash
slither . --print contract-summary
```

Lists all contracts, functions, state variables, and modifiers in a table.

### Human-Readable Summary

```bash
slither . --print human-summary
```

One-line-per-contract overview: name, LOC, ERCs implemented, number of functions, complexity.

### Function Details

```bash
slither . --print function-summary
```

Per-function table: visibility, modifiers, state variables read/written, external calls made.

### Call Graph

```bash
slither . --print call-graph
```

Exports DOT file showing function-to-function call relationships. View with:

```bash
dot -Tpng all_contracts.call-graph.dot -o call-graph.png
```

### Inheritance

```bash
slither . --print inheritance-graph
```

DOT graph of contract inheritance hierarchy.

### Control Flow Graph

```bash
slither . --print cfg
```

Per-function control flow graph in DOT format.

### Storage Layout

```bash
slither . --print variable-order
```

Prints storage slot layout — essential for upgradeable contracts.

### Authorization Analysis

```bash
slither . --print vars-and-auth
```

Per-function: which state variables are written and what `require`/`onlyOwner` checks guard the function.

### Function Selectors

```bash
slither . --print function-id
```

Prints the 4-byte keccak256 selector for each function — useful for debugging raw calldata.

### All Printers

```bash
slither --list-printers
```

## Custom Detectors

Slither's Python API lets you write detectors that plug into the analysis pipeline.

### Detector Structure

```python
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)

class MissingEventEmission(AbstractDetector):
    ARGUMENT = "missing-event-on-state-change"
    HELP = "State change without event emission"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/example/detectors#missing-event"
    WIKI_TITLE = "Missing Event on State Change"
    WIKI_DESCRIPTION = (
        "Detect functions that modify state variables without emitting events."
    )
    WIKI_EXPLOIT_SCENARIO = """
    ```solidity
    function setFee(uint256 _fee) external onlyOwner {
        fee = _fee; // No event — off-chain indexers miss this change
    }
    ```
    """
    WIKI_RECOMMENDATION = "Emit an event after every state variable modification."

    def _detect(self):
        results = []
        for contract in self.compilation_unit.contracts_derived:
            for function in contract.functions:
                if function.is_constructor or function.view or function.pure:
                    continue

                state_vars_written = function.all_state_variables_written()
                if not state_vars_written:
                    continue

                has_event = any(
                    node.contains_require_or_assert() is False
                    and len(node.irs) > 0
                    for node in function.nodes
                    if any(
                        hasattr(ir, "event") for ir in node.irs
                    )
                )

                if not has_event and state_vars_written:
                    info = [
                        function,
                        " modifies state variables ",
                        str([str(v) for v in state_vars_written]),
                        " without emitting an event\n",
                    ]
                    res = self.generate_result(info)
                    results.append(res)
        return results
```

### Classification Levels

| Level | Use When |
|-------|----------|
| `DetectorClassification.HIGH` | Direct fund loss or contract destruction |
| `DetectorClassification.MEDIUM` | Conditional fund loss or broken invariant |
| `DetectorClassification.LOW` | Best practice violation, minor risk |
| `DetectorClassification.INFORMATIONAL` | Code style, gas optimization |
| `DetectorClassification.OPTIMIZATION` | Gas savings opportunity |

### Running Custom Detectors

```bash
slither . --detect missing-event-on-state-change \
  --plugin-detect path/to/my_detector.py
```

Or install as a pip package with an entry point:

```toml
# pyproject.toml
[project.entry-points."slither_analyzer.plugin"]
my_detectors = "my_package.detectors"
```

### Python API Basics

```python
from slither.slither import Slither

slither = Slither(".")

for contract in slither.contracts_derived:
    print(f"Contract: {contract.name}")
    for func in contract.functions:
        print(f"  {func.visibility} {func.name}")
        print(f"    State vars read: {[v.name for v in func.state_variables_read]}")
        print(f"    State vars written: {[v.name for v in func.state_variables_written]}")
        print(f"    External calls: {[str(c) for c in func.external_calls_as_expressions]}")
```

## CI/CD Integration

### GitHub Actions with slither-action

```yaml
name: Slither Analysis
on:
  pull_request:
    paths:
      - "contracts/**"
      - "src/**"
      - "foundry.toml"
      - "hardhat.config.*"

jobs:
  slither:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Run Slither
        uses: crytic/slither-action@v0.4.1
        id: slither
        with:
          fail-on: high
          sarif: results.sarif
          slither-args: >-
            --filter-paths "lib/|node_modules/"
            --exclude naming-convention,solc-version,pragma

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: results.sarif
```

### Key `slither-action` Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `fail-on` | Minimum severity to fail the job: `none`, `low`, `medium`, `high` | `all` |
| `sarif` | Path to write SARIF output for GitHub Code Scanning | — |
| `node-version` | Node.js version for Hardhat/Truffle compilation | `18` |
| `slither-args` | Extra CLI args passed to slither | — |
| `slither-version` | Pin slither version | latest |
| `ignore-compile` | Skip `npx hardhat compile` / `forge build` | `false` |
| `slither-plugins` | pip requirements file for custom detector packages | — |

### SARIF Integration

SARIF output integrates with GitHub's Code Scanning tab. Findings appear inline on PRs with severity badges. Security managers can dismiss or triage findings directly from the GitHub UI.

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: slither
        name: slither
        entry: slither . --exclude naming-convention,solc-version --fail-on high
        language: system
        pass_filenames: false
        files: '\.sol$'
```

## Configuration Reference

`.slither.conf.json` lives at the project root. CLI arguments override config values.

```json
{
  "detectors_to_run": "reentrancy-eth,arbitrary-send-eth,controlled-delegatecall",
  "detectors_to_exclude": "naming-convention,solc-version,pragma",
  "exclude_informational": false,
  "exclude_optimization": false,
  "exclude_low": false,
  "filter_paths": "node_modules|lib/forge-std|lib/openzeppelin-contracts",
  "json": "slither-report.json",
  "sarif": "slither-report.sarif",
  "solc": "0.8.28",
  "solc_remaps": "forge-std/=lib/forge-std/src/",
  "solc_args": "--optimize --optimize-runs 200",
  "compile_force_framework": "foundry",
  "triage_mode": false
}
```

| Key | Type | Description |
|-----|------|-------------|
| `detectors_to_run` | string | Comma-separated detector IDs to run (overrides defaults) |
| `detectors_to_exclude` | string | Comma-separated detector IDs to skip |
| `exclude_informational` | bool | Skip all informational findings |
| `exclude_optimization` | bool | Skip all optimization findings |
| `exclude_low` | bool | Skip all low-severity findings |
| `filter_paths` | string | Regex of paths to exclude from results |
| `json` | string | Path for JSON output |
| `sarif` | string | Path for SARIF output |
| `solc` | string | Solidity compiler path or version |
| `solc_remaps` | string | Import remappings (Foundry/Hardhat style) |
| `solc_args` | string | Extra solc arguments |
| `compile_force_framework` | string | Force compilation framework: `foundry`, `hardhat`, `truffle` |
| `triage_mode` | bool | Enable interactive triage |

## Tool Comparison

| Feature | Slither | Mythril | Echidna | Halmos | Certora | Semgrep |
|---------|---------|---------|---------|--------|---------|---------|
| **Type** | Static analysis | Symbolic execution | Fuzzer | Symbolic testing | Formal verification | Pattern matching |
| **Speed** | < 1 second | Minutes to hours | Minutes to hours | Minutes | Minutes to hours | Seconds |
| **False positive rate** | Medium-high | Low | Very low | Very low | Very low | Depends on rules |
| **Custom rules** | Python detectors | — | Solidity invariants | Solidity assertions | CVL specs | YAML rules |
| **Finds** | Code patterns, known vulns | Reachable exploits | Invariant violations | Assertion violations | Spec violations | Code patterns |
| **Misses** | Logic bugs, economic attacks | State space limits | Coverage gaps | Loops, complex math | Spec incompleteness | Anything not patterned |
| **CI integration** | Native GH Action + SARIF | Docker | Docker | forge test | Cloud service | Native GH Action |
| **Language** | Python | Python | Haskell | Python | Proprietary (CVL) | OCaml/Python |
| **Cost** | Free (OSS) | Free (OSS) | Free (OSS) | Free (OSS) | Commercial | Free for basic |
| **Learning curve** | Low | Medium | Medium | Medium | High | Low |

## Recommended Security Workflow

Use multiple tools in layers. Each catches what others miss.

```
1. Slither (seconds)     → Fast scan for known vulnerability patterns
2. Semgrep (seconds)     → Custom pattern rules for project-specific anti-patterns
3. Echidna/Halmos (mins) → Property-based testing / symbolic execution for invariants
4. Certora (hours)       → Formal verification for critical protocol invariants
5. Manual review         → Logic bugs, economic attacks, access control design
```

### When to Run Each

| Stage | Tool | Purpose |
|-------|------|---------|
| Every commit | Slither | Catch regressions, known patterns |
| Every PR | Slither + Semgrep | Patterns + project-specific rules |
| Before audit | Echidna / Halmos | Property testing, edge cases |
| Pre-mainnet | Certora | Formal proof of critical invariants |
| Pre-mainnet | Manual review | Full threat model, economic analysis |

## Common CLI Patterns

### Run only high/medium detectors

```bash
slither . --exclude-informational --exclude-optimization --exclude-low
```

### Run a single detector

```bash
slither . --detect reentrancy-eth
```

### JSON output to stdout

```bash
slither . --json -
```

### Analyze specific contract

```bash
slither . --contract-name Vault
```

### Show compiler warnings

```bash
slither . --solc-disable-warnings
```

### List all detectors with severity

```bash
slither --list-detectors
```

### List all printers

```bash
slither --list-printers
```

## References

- GitHub: https://github.com/crytic/slither
- Detector documentation: https://github.com/crytic/slither/wiki/Detector-Documentation
- Printer documentation: https://github.com/crytic/slither/wiki/Printer-documentation
- Python API: https://github.com/crytic/slither/wiki/Python-API
- GitHub Action: https://github.com/crytic/slither-action
- Trail of Bits blog: https://blog.trailofbits.com/

Last verified: February 2026 against Slither v0.10.x
