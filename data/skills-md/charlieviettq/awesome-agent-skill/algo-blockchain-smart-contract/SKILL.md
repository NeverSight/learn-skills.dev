---
name: "\"algo-blockchain-smart-contract\""
description: "\"Design and implement smart contracts as self-executing programmatic agreements on blockchain. Use this skill when the user needs to build automated on-chain logic, evaluate smart contract security, or design tokenized business rules — even if they say 'smart contract development', 'automated agreement', or 'on-chain logic'.\"."
allowed-tools: Read, Glob, Grep
---

# Smart Contracts

## Overview

Smart contracts are self-executing programs stored on a blockchain that automatically enforce agreement terms when conditions are met. Primarily written in Solidity (Ethereum/EVM) or Rust (Solana). Once deployed, code is immutable — bugs cannot be patched without migration. Security is critical as exploits are irreversible.

## When to Use

**Trigger conditions:**
- Automating multi-party agreements that execute without intermediaries
- Building token-based systems (NFTs, DeFi, governance)
- Creating transparent, auditable business logic on-chain

**When NOT to use:**
- For simple CRUD operations (use a database)
- When business logic changes frequently (immutability makes updates costly)
- When off-chain data is the primary input (oracle dependency is risky)

## Algorithm

```
IRON LAW: Deployed Smart Contracts Are IMMUTABLE — Bugs Are Permanent
Once deployed, contract code cannot be changed. A bug that loses funds
is IRREVERSIBLE. There is no "hotfix" or "rollback" (unless the
contract includes an upgrade proxy pattern). Security audit BEFORE
deployment is not optional — it is the only protection.
```

### Phase 1: Input Validation
Define: contract purpose, participants, conditions, state variables, access controls. Determine: which logic MUST be on-chain vs which can be off-chain.
**Gate:** Business logic specified, on-chain necessity justified.

### Phase 2: Core Algorithm
**Design:**
1. Define state variables (stored on-chain, costs gas)
2. Define functions: external (callable by users), internal (helper logic)
3. Implement access control (onlyOwner, role-based, multisig)
4. Handle edge cases: reentrancy guards, integer overflow checks, gas limits

**Security patterns:**
- Checks-Effects-Interactions (prevent reentrancy)
- Pull over push (for payments)
- Minimal on-chain data (store hashes, not full data)
- Upgradeable proxy pattern (if mutability needed)

### Phase 3: Verification
Test: unit tests covering all paths, edge cases, access control violations. Security audit: automated (Slither, Mythril) + manual review. Deploy to testnet first.
**Gate:** All tests pass, automated security scan clean, testnet deployment successful.

### Phase 4: Output
Return contract design with security analysis.

## Output Format

```json
{
  "contract": {"name": "Escrow", "functions": 5, "state_variables": 4, "access_roles": ["buyer", "seller", "arbiter"]},
  "security": {"audit_status": "passed", "patterns_used": ["checks_effects_interactions", "pull_payment"], "known_risks": ["oracle_dependency"]},
  "metadata": {"platform": "ethereum", "language": "solidity", "estimated_gas": 250000}
}
```

## Examples

### Sample I/O
**Input:** Escrow contract: buyer deposits, seller delivers, arbiter resolves disputes
**Expected:** Contract with: deposit(), confirmDelivery(), dispute(), withdraw() functions. Funds held until conditions met.

### Edge Cases
| Input | Expected | Why |
|-------|----------|-----|
| Gas price spike | Transaction may fail or cost more | Always set gas limits and handle failures |
| Reentrant call | Must be blocked | Reentrancy is the #1 smart contract vulnerability |
| Contract upgrade needed | Use proxy pattern or migrate | Immutability by default |

## Gotchas

- **Reentrancy attacks**: The DAO hack ($60M) exploited reentrancy. Always use the Checks-Effects-Interactions pattern and/or ReentrancyGuard.
- **Integer overflow/underflow**: Solidity 0.8+ has built-in overflow checks. Earlier versions require SafeMath library. Never assume arithmetic is safe.
- **Front-running**: Miners/validators can see pending transactions and insert their own first (MEV). Sensitive operations need commit-reveal schemes.
- **Gas optimization**: Every operation costs gas. Minimize storage writes (most expensive), use events for data that doesn't need on-chain querying, pack variables.
- **Upgradeability vs immutability**: Proxy patterns allow upgrades but add complexity and trust assumptions (who can upgrade?). Choose based on trust model.
- **Oracle dependency**: Smart contracts can't access off-chain data directly. Oracles (Chainlink, etc.) introduce trust assumptions. A compromised oracle compromises the contract.

## References

- For common vulnerability patterns, see `references/vulnerability-patterns.md`
- For gas optimization techniques, see `references/gas-optimization.md`
