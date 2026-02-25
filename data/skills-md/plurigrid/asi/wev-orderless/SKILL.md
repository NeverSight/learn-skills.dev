---
name: wev-orderless
description: 'WEV Orderless — World Extractable Value'
version: 1.0.0
---

# WEV Orderless — World Extractable Value

**Trit**: 0 (ERGODIC) — Value flow coordinator
**Status**: Production Ready

---

## Overview

World Extractable Value (WEV) exploits **knowledge differentials** in orderless execution environments. Unlike MEV (Maximal Extractable Value) which requires transaction ordering control, WEV operates in parallel execution systems where order doesn't matter.

## When to Use

- Extracting value from knowledge asymmetry between Aptos world wallets
- Coordinating parallel transactions with GF(3) conservation
- Implementing epistemic arbitrage across skill domains
- Building order-invariant DeFi strategies

## Core Concepts

### WEV vs MEV

| MEV | WEV |
|-----|-----|
| Order-dependent | Order-invariant |
| Front-running | Epistemic transfer |
| Zero-sum | Positive-sum |
| Sequential | Parallel (Block-STM) |

### GF(3) Conservation

All WEV transactions must satisfy:
```
Σ trit(world_i) ≡ 0 (mod 3)
```

This ensures triadic balance: PLUS, ERGODIC, MINUS worlds cooperate.

### Epistemic Arbitrage

Value extraction via knowledge transfer:
```
WEV = knowledge_value(source) × transfer_efficiency - gas_cost
```

## 26 World Wallet Society

```
PLUS  (+1): A, B, C, D, E, W, X, Y, Z  (9 worlds)
ERGODIC(0): F, G, H, I, J, K, L, M     (8 worlds)
MINUS (-1): N, O, P, Q, R, S, T, U, V  (9 worlds)

Total: 9 - 9 = 0 ✓ GF(3) conserved
```

## Commands

```bash
# Scan for WEV opportunities
just wev-scan

# Execute knowledge transfer between worlds
just wev-transfer a p

# Verify GF(3) conservation
just aptos-gf3-verify

# Show world wallet balances
just aptos-world-balances
```

## Triadic Transaction Pattern

```clojure
(defn wev-triplet [from-world to-world]
  {:plus    {:role :generator :trit +1}
   :ergodic {:role :coordinator :trit 0}
   :minus   {:role :validator :trit -1}
   :sum 0
   :orderless true})
```

## Integration

| Skill | Integration |
|-------|-------------|
| `aptos-agent` | Execute blockchain transactions |
| `epistemic-arbitrage` | Propagator network for knowledge flow |
| `spi-parallel-verify` | Verify order-invariance |
| `gay-mcp` | Deterministic coloring for world visualization |
| `local-compositionality-gadget` | GF(3) triplet generation |

## Block-STM Compatibility

WEV is designed for Aptos Block-STM:
- Speculative parallel execution
- Automatic conflict detection
- Deterministic final state regardless of execution order

## See Also

- [dev/WEV_SYNTHESIS.md](file:///Users/alice/agent-o-rama/agent-o-rama/dev/WEV_SYNTHESIS.md)
- [dev/secure_wallets.json](file:///Users/alice/agent-o-rama/agent-o-rama/dev/secure_wallets.json)
- [SKILL_ADJUNCTIONS.md](file:///Users/alice/agent-o-rama/agent-o-rama/dev/SKILL_ADJUNCTIONS.md)
