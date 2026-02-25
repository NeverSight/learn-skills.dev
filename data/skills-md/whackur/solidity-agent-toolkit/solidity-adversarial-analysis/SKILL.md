---
name: solidity-adversarial-analysis
description: Adversarial scenario analysis and threat modeling for Solidity smart contracts. Use when analyzing contracts from an attacker's perspective, identifying multi-step attack vectors, or performing threat modeling. Covers flash loan attacks, oracle manipulation, MEV/front-running, governance exploits, reentrancy scenarios, access control bypasses, economic logic exploits, and cross-contract composability risks. Triggers on tasks involving adversarial analysis, threat modeling, attack scenarios, attack vectors, exploit analysis, or red team review.
license: MIT
metadata:
  author: whackur
  version: "0.5.3"
---

# Solidity Adversarial Scenario Analysis

## When to Apply

- Red-team security reviews and penetration testing
- Pre-deployment threat modeling for DeFi protocols
- Analyzing contracts that handle significant TVL
- Investigating suspicious behavior or incident response
- Extending a standard security audit with attacker-perspective analysis

## Adversarial Thinking Framework

| Step                      | Action                             | Key Question                                                      |
| :------------------------ | :--------------------------------- | :---------------------------------------------------------------- |
| 1. Identify Assets        | Map valuable targets               | What can be stolen, locked, or manipulated?                       |
| 2. Enumerate Entry Points | List all external/public functions | Which functions change state or move value?                       |
| 3. Model Adversary        | Define attacker capabilities       | What resources (flash loans, MEV, tokens) does the attacker have? |
| 4. Construct Sequences    | Build multi-step attack paths      | What sequence of calls achieves the attack goal?                  |
| 5. Verify Invariants      | Check contract assumptions         | Which mathematical or state invariants can be violated?           |

## Attack Scenario Categories

| Category            | Severity | Key Indicators                                      | Example Attack                   |
| :------------------ | :------- | :-------------------------------------------------- | :------------------------------- |
| Reentrancy          | Critical | External calls before state updates, missing guards | Drain via fallback re-entry      |
| Flash Loan          | Critical | Price-dependent logic, spot price reliance          | Borrow → manipulate → profit     |
| Oracle Manipulation | High     | External price feeds, single-source oracles         | Inflate collateral value         |
| MEV / Front-running | High     | DEX interactions, unprotected swaps                 | Sandwich attack on swap          |
| Governance          | High     | Token-weighted voting, timelocks                    | Flash-borrow votes               |
| Access Control      | Critical | Initializers, proxy patterns, ownership             | Unprotected initializer takeover |
| Economic / Logic    | High     | Reward calculations, share math, minting            | Rounding exploit in rewards      |
| Cross-contract      | High     | Token callbacks, composability assumptions          | Malicious ERC777 callback        |

## Scenario Analysis Process

1. **Feature Detection**: Identify what the contract does (oracle usage? governance? DEX interaction?)
2. **Threat Mapping**: Map detected features to applicable attack categories
3. **Scenario Construction**: For each applicable category, build: Pre-conditions → Attack Steps → Impact
4. **Invariant Verification**: Define properties that must always hold (e.g., `totalDeposits <= balance`)
5. **Mitigation Assessment**: Check if existing defenses (ReentrancyGuard, access control, slippage checks) adequately cover the scenario

## Category Deep Dives

### Reentrancy

- Does the contract make external calls before updating state?
- Are there cross-function interactions sharing mutable state?
- Is ReentrancyGuard applied to all functions with external calls?

### Flash Loan

- Does any calculation depend on a spot price that can be manipulated within one transaction?
- Can the attacker's position be established and unwound atomically?

### Oracle Manipulation

- Is a single oracle source used for critical price data?
- Can the oracle price be influenced by large trades in the same block?
- Are there fallback oracles or sanity checks on price deviations?

### MEV / Front-running

- Are there unprotected swaps or liquidity operations?
- Does the contract rely on `block.number` or `block.timestamp` for ordering?
- Can an attacker sandwich a user's transaction for profit?

### Governance

- Can voting power be acquired via flash loans or flash mints?
- Is there a sufficient timelock between proposal and execution?
- Can a malicious actor bypass quorum requirements?

### Access Control

- Are initializers protected against multiple calls?
- Can ownership be hijacked through uninitialized storage or logic flaws?
- Are administrative functions restricted to trusted roles?

### Economic / Logic

- Are there rounding errors in reward or share calculations?
- Can an attacker mint tokens or inflate balances through logic gaps?
- Does the contract handle fee-on-transfer or rebasing tokens correctly?

### Cross-contract

- Does the contract interact with untrusted tokens (e.g., ERC777)?
- Are there assumptions about external contract behavior that can be violated?
- Can a malicious callback disrupt the contract's state?

## Enhanced with MCP

If using the `solidity-agent-toolkit` MCP server:

- `analyze_adversarial_scenarios`: Detect contract features and match applicable attack scenarios automatically
- `adversarial_analysis` prompt: Guided adversarial analysis with scenario knowledge injected
- `adversarial://list`: Browse all attack scenario categories
- `adversarial://category/{category}`: Deep dive into specific attack category
- `match_vulnerability_patterns`: Complement with regex-based vulnerability detection
- `run_slither` / `run_aderyn`: Automated static analysis for supporting evidence

For defensive patterns against identified threats, see the **Security Best Practices** skill.

## References

- For defensive countermeasures: Security Best Practices skill
- For audit methodology: Code Review skill
