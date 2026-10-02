---
name: semgrep-solidity
description: Semgrep rules for smart contract security — custom pattern matching, taint tracking, community rulesets, autofix rules, and CI/CD integration. Write targeted detection rules for Solidity vulnerabilities that static analyzers miss.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Security
tags:
  - semgrep
  - pattern-matching
  - security
  - solidity
  - custom-rules
---

# Semgrep for Solidity

Semgrep is a lightweight static analysis tool that matches code patterns you define. For Solidity, it lets you write custom detection rules in YAML that catch vulnerabilities, anti-patterns, and protocol-specific bugs that generic analyzers miss. The killer combination: community rulesets for known issues + custom rules for your project's invariants.

## What You Probably Got Wrong

> LLMs hallucinate Semgrep features and misunderstand its Solidity support. These are the real facts.

- **Solidity support is community-driven, not official Semgrep Inc** — Semgrep's Solidity parser is maintained by the community (tree-sitter-solidity). It works well for pattern matching but occasionally lags behind bleeding-edge Solidity syntax. Semgrep Inc focuses on their supported languages (Python, JS, Go, etc.) — Solidity is "community-supported."
- **decurity/semgrep-smart-contracts is the go-to ruleset** — This is the most comprehensive open-source Semgrep ruleset for Solidity. It covers reentrancy, access control, unsafe delegatecall, unchecked return values, and more. Start here before writing your own rules.
- **Semgrep finds patterns, not bugs** — Semgrep matches AST patterns you define. It does not reason about program state, symbolic execution, or constraint solving like Mythril or Manticore. If you don't write a rule for it, Semgrep won't find it.
- **Taint tracking is the killer feature** — Semgrep's `mode: taint` lets you trace data flow from sources to sinks. This is how you detect "user input reaches dangerous operation" patterns that simple grep cannot catch.
- **Semgrep is NOT a replacement for Slither** — Slither has 90+ built-in detectors with deep Solidity understanding (inheritance resolution, state variable tracking, CFG analysis). Semgrep excels at custom rules you write for YOUR codebase. Use both.
- **Autofix is real but limited** — Semgrep can auto-apply fixes via the `fix:` key in rules. It works for simple pattern replacements but cannot handle complex refactoring.
- **`--config auto` does not include Solidity rules** — Semgrep's `auto` config pulls from the Semgrep Registry, which has limited Solidity coverage. You need to point at specific rulesets or write your own.

## Installation

```bash
# pip (recommended — always latest)
pip install semgrep

# Homebrew
brew install semgrep

# Docker
docker run --rm -v "${PWD}:/src" semgrep/semgrep semgrep --config auto /src
```

Verify installation:

```bash
semgrep --version
# Expected: 1.x.x (Last verified: February 2026)
```

## Quick Start

Run the community smart contract rules against your project:

```bash
# Clone the community ruleset
git clone https://github.com/Decurity/semgrep-smart-contracts.git /tmp/semgrep-rules

# Run all Solidity rules against your contracts
semgrep --config /tmp/semgrep-rules/solidity/ ./contracts/

# Or run directly from GitHub (slower, downloads each time)
semgrep --config "r/solidity" ./contracts/
```

Run a single rule file:

```bash
semgrep --config my-rules/reentrancy.yaml ./contracts/
```

Run with JSON output for CI parsing:

```bash
semgrep --config /tmp/semgrep-rules/solidity/ --json ./contracts/ > results.json
```

## Community Rulesets

### decurity/semgrep-smart-contracts

The primary open-source Solidity ruleset. Coverage includes:

| Category | Rules | What They Detect |
|----------|-------|------------------|
| Reentrancy | 3+ | State changes after external calls, cross-function reentrancy |
| Access Control | 4+ | Missing `onlyOwner`, `tx.origin` auth, unprotected `selfdestruct` |
| Delegatecall | 2+ | User-controlled delegatecall targets |
| Return Values | 2+ | Unchecked low-level call return values |
| Token | 3+ | Missing zero-address checks, unsafe ERC20 operations |
| Proxy | 2+ | Storage collision, uninitialized proxy |
| Arithmetic | 2+ | Unsafe casting, division before multiplication |

```bash
# Clone and use specific categories
git clone https://github.com/Decurity/semgrep-smart-contracts.git

# Run only reentrancy rules
semgrep --config semgrep-smart-contracts/solidity/security/reentrancy*.yaml ./contracts/

# Run all security rules
semgrep --config semgrep-smart-contracts/solidity/security/ ./contracts/
```

## Writing Custom Rules

### Rule Anatomy

Every Semgrep rule is a YAML file with this structure:

```yaml
rules:
  - id: my-rule-id
    patterns:
      - pattern: |
          msg.sender.call{value: ...}(...)
    message: >-
      Detected low-level call with value. Ensure reentrancy protection
      is in place (CEI pattern or ReentrancyGuard).
    languages: [solidity]
    severity: WARNING
    metadata:
      category: security
      technology:
        - solidity
      confidence: MEDIUM
```

### Pattern Syntax

Semgrep patterns match against the AST (abstract syntax tree), not raw text. This means whitespace and formatting differences are ignored.

```yaml
# Exact match — matches this exact function call
- pattern: selfdestruct(...)

# Metavariable — captures any expression into $X
- pattern: $X.call{value: $V}($DATA)

# Ellipsis — matches zero or more arguments/statements
- pattern: |
    function $FUNC(...) external {
      ...
      $ADDR.call{value: ...}(...);
      ...
    }

# Deep expression operator — matches inside nested expressions
- pattern: <... msg.value ...>
```

### Metavariables

Metavariables (`$X`, `$FUNC`, `$ADDR`) capture parts of the matched code. They're bound on first match and must be consistent within a rule.

```yaml
rules:
  - id: same-variable-send-receive
    patterns:
      # $TOKEN must be the same in both lines
      - pattern: |
          $TOKEN.transferFrom($FROM, address(this), $AMOUNT);
          ...
          $TOKEN.transfer($TO, $AMOUNT);
    message: >-
      Same $AMOUNT transferred in and out — possible no-op or fee bypass.
    languages: [solidity]
    severity: WARNING
```

### Combining Patterns

```yaml
rules:
  - id: tx-origin-auth
    # ALL of these must match (AND logic)
    patterns:
      # Match require/if using tx.origin
      - pattern-either:
          - pattern: require(tx.origin == $ADDR, ...)
          - pattern: require(tx.origin == $ADDR)
          - pattern: |
              if (tx.origin != $ADDR) { ... }
      # But NOT inside a test file
      - pattern-not-inside: |
          contract $TEST is Test { ... }
    message: >-
      tx.origin used for authorization. Use msg.sender instead —
      tx.origin can be spoofed via phishing contracts (see SWC-115).
    languages: [solidity]
    severity: ERROR
```

### pattern-either (OR Logic)

```yaml
# Matches ANY of the sub-patterns
- pattern-either:
    - pattern: selfdestruct(...)
    - pattern: suicide(...)
```

### pattern-not (Exclusion)

```yaml
# Match external calls WITHOUT nonReentrant modifier
patterns:
  - pattern: |
      function $F(...) external $MOD {
        ...
        $X.call{value: ...}(...);
        ...
      }
  - pattern-not: |
      function $F(...) external nonReentrant {
        ...
      }
```

### pattern-inside (Scope)

```yaml
# Only match if inside a specific context
patterns:
  - pattern: selfdestruct(...)
  - pattern-inside: |
      function $F(...) public { ... }
```

## Taint Tracking

Taint tracking traces data flow from **sources** (untrusted input) through **propagators** to **sinks** (dangerous operations). This is Semgrep's most powerful feature for Solidity — it catches vulnerabilities that pattern matching alone cannot.

```yaml
rules:
  - id: user-controlled-delegatecall
    mode: taint
    message: >-
      User-controlled address passed to delegatecall. An attacker can
      execute arbitrary code in the context of this contract.
    languages: [solidity]
    severity: ERROR
    pattern-sources:
      # Function parameters are user-controlled in external functions
      - patterns:
          - pattern: $PARAM
          - pattern-inside: |
              function $F(..., address $PARAM, ...) external { ... }
    pattern-sinks:
      - pattern: $TARGET.delegatecall(...)
    metadata:
      category: security
      cwe: "CWE-829: Inclusion of Functionality from Untrusted Control Sphere"
```

### Sources, Sinks, and Sanitizers

```yaml
rules:
  - id: tainted-transfer-amount
    mode: taint
    message: >-
      User-supplied amount flows to token transfer without validation.
    languages: [solidity]
    severity: WARNING
    pattern-sources:
      - patterns:
          - pattern: $PARAM
          - pattern-inside: |
              function $F(..., uint256 $PARAM, ...) external { ... }
    pattern-sinks:
      - pattern: $TOKEN.transfer($TO, $AMOUNT)
      - pattern: $TOKEN.transferFrom($FROM, $TO, $AMOUNT)
    pattern-sanitizers:
      # If the amount is checked against a bound, it's sanitized
      - pattern: require($AMOUNT <= $MAX, ...)
      - pattern: require($AMOUNT <= $MAX)
      - pattern: |
          if ($AMOUNT > $MAX) { revert(...); }
```

### Taint Labels

For complex flows, use labels to track multiple taint sources independently:

```yaml
rules:
  - id: cross-taint-oracle-price
    mode: taint
    message: >-
      Oracle price feeds into calculation without staleness check.
    languages: [solidity]
    severity: ERROR
    pattern-sources:
      - label: ORACLE_PRICE
        patterns:
          - pattern: $ORACLE.latestRoundData()
    pattern-sinks:
      - requires: ORACLE_PRICE
        patterns:
          - pattern: $X * $PRICE / $DENOM
    pattern-sanitizers:
      - label: ORACLE_PRICE
        patterns:
          - pattern: require(block.timestamp - $UPDATED_AT < $THRESHOLD, ...)
```

## Autofix Rules

Semgrep can auto-apply fixes. Use the `fix:` key with metavariable references:

```yaml
rules:
  - id: replace-transfer-with-call
    patterns:
      - pattern: $ADDR.transfer($AMOUNT)
    fix: |
      (bool success, ) = $ADDR.call{value: $AMOUNT}("");
      require(success, "Transfer failed");
    message: >-
      .transfer() forwards only 2300 gas. Use .call{value:}("") instead.
    languages: [solidity]
    severity: WARNING

  - id: add-zero-address-check
    patterns:
      - pattern: |
          function $F(address $ADDR) external {
            $BODY
          }
      - pattern-not: |
          function $F(address $ADDR) external {
            ...
            require($ADDR != address(0), ...);
            ...
          }
    fix: |
      function $F(address $ADDR) external {
        require($ADDR != address(0), "Zero address");
        $BODY
      }
    message: Missing zero-address validation on parameter $ADDR.
    languages: [solidity]
    severity: WARNING
```

Apply fixes:

```bash
# Preview fixes (dry run)
semgrep --config rules/ --autofix --dryrun ./contracts/

# Apply fixes
semgrep --config rules/ --autofix ./contracts/
```

## Rule Testing

Semgrep has built-in test support. Create test files alongside your rules with special annotations.

### Test File Format

```solidity
// test file: reentrancy.sol (lives next to reentrancy.yaml)

contract TestReentrancy {
    mapping(address => uint256) balances;

    // ruleid: unsafe-external-call-before-state-update
    function withdrawBad(uint256 amount) external {
        require(balances[msg.sender] >= amount);
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok);
        balances[msg.sender] -= amount;
    }

    // ok: unsafe-external-call-before-state-update
    function withdrawGood(uint256 amount) external {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok);
    }
}
```

Annotations:
- `// ruleid: <rule-id>` — this line (or block) SHOULD trigger the rule
- `// ok: <rule-id>` — this line (or block) should NOT trigger the rule
- `// todoruleid: <rule-id>` — known false negative (rule doesn't catch this yet)

### Running Tests

```bash
# Test all rules in a directory
semgrep --test ./rules/

# Test a specific rule
semgrep --test ./rules/reentrancy.yaml

# Expected output:
# 1/1 tests passed for reentrancy.yaml
```

Directory structure for tests:

```
rules/
├── reentrancy.yaml          # Rule definition
├── reentrancy.sol           # Test file (same name, .sol extension)
├── tx-origin.yaml
├── tx-origin.sol
├── delegatecall.yaml
└── delegatecall.sol
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/semgrep.yml
name: Semgrep Security Scan

on:
  pull_request:
    paths:
      - "contracts/**"
      - "src/**"
      - ".semgrep/**"
  push:
    branches: [main]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Clone community rules
        run: |
          git clone --depth 1 \
            https://github.com/Decurity/semgrep-smart-contracts.git \
            /tmp/semgrep-rules

      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: |
            /tmp/semgrep-rules/solidity/
            .semgrep/
        env:
          SEMGREP_RULES: /tmp/semgrep-rules/solidity/ .semgrep/
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/semgrep/semgrep
    rev: v1.108.0
    hooks:
      - id: semgrep
        args:
          - --config
          - .semgrep/
          - --error
        files: \.sol$
```

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run manually
pre-commit run semgrep --all-files
```

## Solidity-Specific Patterns

### Reentrancy Detection

```yaml
rules:
  - id: unsafe-external-call-before-state-update
    patterns:
      - pattern: |
          $ADDR.call{value: ...}(...);
          ...
          $STATE[$KEY] = $VAL;
      - pattern-inside: |
          function $F(...) { ... }
    message: >-
      External call before state update — classic reentrancy vector.
      Move state changes before the external call (CEI pattern).
    languages: [solidity]
    severity: ERROR
    metadata:
      category: security
      cwe: "CWE-841: Improper Enforcement of Behavioral Workflow"
      references:
        - https://swcregistry.io/docs/SWC-107
```

### tx.origin Authorization

```yaml
rules:
  - id: tx-origin-authentication
    pattern-either:
      - pattern: require(tx.origin == $ADDR, ...)
      - pattern: require(tx.origin == $ADDR)
      - pattern: |
          if (msg.sender != tx.origin) { ... }
    message: >-
      tx.origin used for authentication. A malicious contract can trick
      a user into calling it, then forward the call to your contract
      with the user's tx.origin. Use msg.sender.
    languages: [solidity]
    severity: ERROR
    metadata:
      cwe: "CWE-477: Use of Obsolete Function"
      references:
        - https://swcregistry.io/docs/SWC-115
```

### Delegatecall to User-Controlled Address

```yaml
rules:
  - id: delegatecall-to-arbitrary-address
    mode: taint
    message: >-
      delegatecall target is derived from a function parameter.
      An attacker can execute arbitrary code in this contract's context.
    languages: [solidity]
    severity: ERROR
    pattern-sources:
      - patterns:
          - pattern: $PARAM
          - pattern-inside: |
              function $F(..., address $PARAM, ...) external { ... }
    pattern-sinks:
      - pattern: $ADDR.delegatecall(...)
```

### Unchecked Return Values

```yaml
rules:
  - id: unchecked-low-level-call
    patterns:
      - pattern: $ADDR.call{...}(...)
      - pattern-not: |
          (bool $OK, ...) = $ADDR.call{...}(...);
          ...
          require($OK, ...);
      - pattern-not: |
          (bool $OK, ) = $ADDR.call{...}(...);
          ...
          require($OK);
      - pattern-not: |
          (bool $OK, ) = $ADDR.call{...}(...);
          if (!$OK) { revert(...); }
    message: >-
      Low-level call return value not checked. The call may silently fail.
    languages: [solidity]
    severity: ERROR
```

### Missing Access Control

```yaml
rules:
  - id: unprotected-selfdestruct
    patterns:
      - pattern: selfdestruct(...)
      - pattern-not-inside: |
          function $F(...) ... onlyOwner ... { ... }
      - pattern-not-inside: |
          function $F(...) ... onlyRole(...) ... { ... }
      - pattern-not-inside: |
          require(msg.sender == $OWNER, ...);
          ...
          selfdestruct(...);
    message: >-
      selfdestruct without access control. Anyone can destroy this contract.
    languages: [solidity]
    severity: ERROR
    metadata:
      cwe: "CWE-284: Improper Access Control"
```

### Unsafe Casting

```yaml
rules:
  - id: unsafe-downcast
    pattern-either:
      - pattern: uint128($X)
      - pattern: uint96($X)
      - pattern: uint64($X)
      - pattern: uint32($X)
      - pattern: uint16($X)
      - pattern: uint8($X)
      - pattern: int128($X)
      - pattern: int64($X)
      - pattern: int32($X)
    message: >-
      Downcasting without overflow check. Solidity 0.8.x checked math
      does NOT protect type casts. Use OpenZeppelin SafeCast.
    languages: [solidity]
    severity: WARNING
    metadata:
      references:
        - https://docs.openzeppelin.com/contracts/5.x/api/utils#SafeCast
```

## Tool Comparison

| Feature | Semgrep | Slither | Mythril | Echidna |
|---------|---------|---------|---------|---------|
| Analysis type | Pattern matching + taint | IR-based static analysis | Symbolic execution | Fuzzing |
| Custom rules | YAML (easy) | Python plugins (harder) | Not designed for custom | Property-based |
| Built-in detectors | Community rulesets | 90+ built-in | 30+ built-in | User-defined |
| Speed | Fast (seconds) | Fast (seconds) | Slow (minutes) | Variable |
| False positives | Depends on rule quality | Moderate | Low | Very low |
| Solidity support | Community parser | Native (deep) | Native (deep) | Native |
| Data flow | Taint tracking | Full CFG + data flow | Path-based | Runtime |
| CI/CD integration | Excellent | Good | Moderate | Moderate |
| Learning curve | Low (YAML) | Medium | High | Medium |

### When to Use Each

- **Semgrep**: Custom rules for YOUR project's patterns, CI gatekeeping on known anti-patterns, quick checks during development
- **Slither**: Comprehensive automated audit, understanding inheritance and state, built-in detector coverage
- **Mythril**: Finding complex bugs that require reasoning about execution paths and constraints
- **Echidna**: Testing invariants with fuzzing, finding edge cases in business logic

### Recommended Workflow

```
Development    → Semgrep (pre-commit, fast feedback)
Pull Request   → Semgrep + Slither (CI pipeline)
Pre-audit      → Semgrep + Slither + Mythril (comprehensive)
Pre-mainnet    → All above + Echidna invariant tests + manual audit
```

## Configuration Reference

### .semgrep.yaml Project Config

```yaml
# Place in project root as .semgrep.yaml or .semgrep/
rules:
  - id: my-rule
    # ... rule definition
```

### CLI Options

```bash
# Run with multiple configs
semgrep --config rules/ --config community-rules/ ./contracts/

# Exclude paths
semgrep --config rules/ --exclude "test/*" --exclude "lib/*" ./

# Output formats
semgrep --config rules/ --json ./contracts/        # JSON
semgrep --config rules/ --sarif ./contracts/       # SARIF (GitHub compatible)
semgrep --config rules/ --emacs ./contracts/       # Emacs format
semgrep --config rules/ --vim ./contracts/         # Vim format

# Severity filtering
semgrep --config rules/ --severity ERROR ./contracts/

# Timeout per rule (default 5s, increase for complex taint rules)
semgrep --config rules/ --timeout 30 ./contracts/

# Max memory per rule (MB)
semgrep --config rules/ --max-memory 2048 ./contracts/

# Verbose output (debugging rules)
semgrep --config rules/ --verbose ./contracts/
semgrep --config rules/ --debug ./contracts/
```

## References

- Semgrep documentation: https://semgrep.dev/docs/
- Semgrep rule syntax: https://semgrep.dev/docs/writing-rules/rule-syntax/
- decurity/semgrep-smart-contracts: https://github.com/Decurity/semgrep-smart-contracts
- Semgrep Registry (Solidity): https://semgrep.dev/r?lang=solidity
- Semgrep taint tracking: https://semgrep.dev/docs/writing-rules/data-flow/taint-mode/
- SWC Registry: https://swcregistry.io/

Last verified: February 2026
