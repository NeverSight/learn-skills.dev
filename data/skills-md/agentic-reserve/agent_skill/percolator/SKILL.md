---
name: percolator
description: Percolator perpetual futures protocol development (Feb 2026). Educational research project for predictable risk management using profit-as-junior-claims model. Covers core risk engine (Rust), Solana programs, CLI tools, matcher development, testing, and formal verification. Alternative to traditional ADL with global coverage ratio and self-healing mechanics.
user-invocable: true
---

# Percolator Development Skill

## What this Skill is for
Use this Skill when the user asks for:
- Percolator protocol development or integration
- Perpetual futures risk engine implementation
- Profit warmup and withdrawal mechanics
- Global coverage ratio (`h`) calculations
- Matcher program development (passive or vAMM)
- Oracle integration (Pyth, Chainlink, or custom)
- Liquidation and keeper operations
- Funding rate mechanics
- Formal verification with Kani
- Testing and stress testing the protocol
- CLI tool usage and scripting

## Core Concepts

### The Percolator Model
Percolator treats profit differently from traditional exchanges:
- **Capital (Senior Claims)**: User deposits, always withdrawable
- **Profit (Junior Claims)**: Trading gains, must mature before withdrawal
- **Global Coverage Ratio `h`**: Determines how much profit is actually backed
- **Self-Healing**: System automatically recovers as conditions improve

### Key Formula
```
Residual = max(0, V - C_tot - I)
h = min(Residual, PNL_pos_tot) / PNL_pos_tot

Where:
  V = vault balance
  C_tot = total capital across all accounts
  I = insurance fund
  PNL_pos_tot = sum of all positive PnL
```

### Why Not ADL?
Traditional ADL forcibly closes profitable positions when insurance depletes.
Percolator instead applies a pro-rata haircut on profit extraction, preserving positions.

## Default Stack Decisions

1. **Core Library**: Rust with formal verification (Kani)
   - 145 proofs covering conservation, principal protection, isolation
   - Zero unsafe code in critical paths

2. **Solana Program**: percolator-prog
   - Market initialization and configuration
   - User and LP account management
   - Keeper operations (liquidations, funding)

3. **CLI**: TypeScript with @solana/web3.js
   - User operations (deposit, withdraw, trade)
   - LP management
   - Keeper bots
   - Testing and monitoring scripts

4. **Matchers**: Separate Solana programs
   - Passive: Fixed spread pricing
   - vAMM: Dynamic pricing with impact
   - Custom: Implement your own pricing logic

5. **Oracles**: Multi-source support
   - Pyth Network (preferred for production)
   - Chainlink OCR2
   - Oracle Authority (testing only)

## Operating Procedure

### 1. Classify the Task Layer
- **Core risk engine**: Rust library modifications
- **On-chain program**: Solana smart contract changes
- **Matcher logic**: Pricing algorithm implementation
- **CLI/tooling**: User-facing commands and scripts
- **Testing**: Unit tests, integration tests, stress tests
- **Verification**: Kani proofs and invariants

### 2. Understand the Invariants
Always preserve:
- **Conservation**: `Withdrawable ≤ Backed capital`
- **Principal Protection**: Capital never haircut
- **Isolation**: Account operations don't affect others (except via `h`)
- **No Teleport**: Value can't appear/disappear

### 3. Implement with Percolator-Specific Correctness
Be explicit about:
- **Slab state**: Market configuration and nonce
- **Account types**: User vs LP, capital vs profit
- **Coverage ratio**: How `h` affects the operation
- **Keeper requirements**: Fresh crank for risk-increasing trades
- **Oracle freshness**: Timestamp and staleness checks
- **Matcher security**: LP PDA signature verification

### 4. Add Tests
- **Unit tests**: Core logic in Rust
- **Kani proofs**: Formal verification of invariants
- **Integration tests**: Full transaction flows on devnet
- **Stress tests**: Worst-case scenarios (gap risk, insurance depletion)
- **Pen tests**: Security and oracle manipulation

### 5. Deliverables Expectations
When implementing changes, provide:
- Exact files changed with diffs
- Commands to build/test/deploy
- Risk notes for anything touching:
  - Withdrawal mechanics
  - Liquidation logic
  - Oracle price handling
  - Matcher CPI calls
  - Insurance fund operations

## Progressive Disclosure (Read When Needed)
- Core risk engine: [risk-engine.md](risk-engine.md)
- Solana program architecture: [program-architecture.md](program-architecture.md)
- Matcher development: [matchers.md](matchers.md)
- CLI usage and scripting: [cli-guide.md](cli-guide.md)
- Testing strategy: [testing.md](testing.md)
- Oracle integration: [oracles.md](oracles.md)
- Formal verification: [verification.md](verification.md)
- Security considerations: [security.md](security.md)
- Deployment guide: [deployment.md](deployment.md)

## Quick Reference

### Common CLI Commands
```bash
# Initialize user account
percolator-cli init-user --slab <slab-pubkey>

# Deposit collateral
percolator-cli deposit --slab <slab> --user-idx <n> --amount <lamports>

# Check best prices
percolator-cli best-price --slab <slab> --oracle <oracle>

# Run keeper crank (required before trading)
percolator-cli keeper-crank --slab <slab> --oracle <oracle>

# Trade via matcher
percolator-cli trade-cpi --slab <slab> --user-idx <n> --lp-idx <n> \
  --size <i128> --matcher-program <prog> --matcher-ctx <ctx> --oracle <oracle>

# Withdraw capital
percolator-cli withdraw --slab <slab> --user-idx <n> --amount <lamports>
```

### Devnet Test Market
```
Slab:    A7wQtRT9DhFqYho8wTVqQCDc7kYPTUXGPATiyVbZKVFs
Oracle:  99B2bTijsU6f1GCT73HmdR7HCFFjGMBcPZY6jZ96ynrR (Chainlink SOL/USD)
Program: 2SSnp35m7FQ7cRLNKGdW5UzjYFF6RBUNq7d3m5mqNByp
Type:    INVERTED (price = 1/SOL in USD)
```

### Risk Parameters
```
Maintenance Margin: 5%
Initial Margin:     10%
Trading Fee:        10 bps (0.1%)
```

## Important Warnings

⚠️ **EDUCATIONAL RESEARCH PROJECT**
- NOT audited
- NOT production ready
- Do NOT use with real funds
- For learning and testing only

⚠️ **Keeper Crank Requirement**
- Risk-increasing trades require recent crank (within 200 slots / ~80s)
- Run keeper before trading or use a keeper bot

⚠️ **Matcher Security**
- MUST verify LP PDA signature in matcher programs
- MUST create matcher context + LP atomically
- Failure = potential fund theft

⚠️ **Inverted Markets**
- Long = long USD (profit if SOL drops)
- Short = short USD (profit if SOL rises)
- Understand direction before trading
