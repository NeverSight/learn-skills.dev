---
name: v
description: 'World V Skill'
version: 1.0.0
---

# World V Skill

**Trit**: -1 (MINUS (validator/constrainer))
**Color Range**: Cold hues (180-300°)
**Index**: 21
**Wallet**: world_v_aptos
**MCP Server**: `mcp__world_v_aptos__*`

## GF(3) Role

This world operates as **MINUS (validator/constrainer)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_v_aptos__aptos_balance      # Check APT balance
mcp__world_v_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_v_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_v_aptos__aptos_stake        # Stake with validator
mcp__world_v_aptos__aptos_view         # Call view function (read-only)
mcp__world_v_aptos__aptos_intent       # Natural language intent
mcp__world_v_aptos__aptos_pending      # List pending decisions
mcp__world_v_aptos__aptos_approve      # Approve/reject decision
```

## World Description

Viro topology visualization

## Triadic Coordination

When operating in parallel with other worlds:

| Your Role | Partner Roles | Combined |
|-----------|--------------|----------|
| -1 | Need +1, 0 | Σ = 0 ✓ |

## Related Skills

- `aptos-agent` - Core Aptos interaction patterns
- `aptos-society` - World Extractable Value (WEV) contracts
- `gay-mcp` - Deterministic color generation from seed
- `plurigrid-asi-integrated` - Unified skill orchestration

## Customization

Add world-specific configurations below this line:

---

<!-- World V custom content -->
