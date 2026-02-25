---
name: bisimulation-game
description: Bisimulation game for resilient skill dispersal across AI agents with
  GF(3) conservation and observational bridge types.
license: MIT
metadata:
  source: music-topos + DiscoHy + DisCoPy
  xenomodern: true
  ironic_detachment: 0.42
---

# Bisimulation Game Skill

> *"Two systems are bisimilar if they cannot be distinguished by any observation."*

## Overview

The bisimulation game provides a framework for:
1. **Resilient skill dispersal** across multiple AI agents
2. **GF(3) conservation** during state transitions
3. **Observational bridge types** for version-aware synchronization
4. **Self-rewriting capabilities** via MCP Tasks protocol

## Game Rules

### Players

| Player | Role | Trit | Color |
|--------|------|------|-------|
| Attacker | Tries to distinguish systems | -1 | Blue |
| Defender | Maintains equivalence | +1 | Red |
| Arbiter | Verifies conservation | 0 | Green |

### Moves

```
┌─────────────────────────────────────────────────────────────┐
│  Round n:                                                   │
│                                                             │
│  1. Attacker chooses: system S₁ or S₂                       │
│  2. Attacker makes: transition s₁ →ᵃ s₁'                    │
│  3. Defender responds: matching transition s₂ →ᵃ s₂'        │
│  4. Arbiter verifies: GF(3) conservation                    │
│                                                             │
│  If Defender cannot respond → Attacker wins (distinguishable)│
│  If game continues forever → Defender wins (bisimilar)      │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### Hy (DiscoHy) Implementation

```hy
;;; bisimulation_game.hy

(import [splitmix_ternary [SplitMixTernary]])

(defclass BisimulationGame []
  (defn __init__ [self system1 system2 seed]
    (setv self.s1 system1
          self.s2 system2
          self.rng (SplitMixTernary seed)
          self.history []))
  
  (defn attacker-move [self choice transition]
    "Attacker chooses system and transition."
    (setv trit (self.rng.next-ternary))
    (.append self.history {:role "attacker" 
                           :choice choice 
                           :transition transition
                           :trit trit})
    trit)
  
  (defn defender-respond [self matching-transition]
    "Defender provides matching transition."
    (setv trit (self.rng.next-ternary))
    (.append self.history {:role "defender"
                           :response matching-transition
                           :trit trit})
    trit)
  
  (defn arbiter-verify [self]
    "Arbiter checks GF(3) conservation."
    (setv recent-trits (lfor m (cut self.history -3 None) (get m "trit")))
    (setv conserved (= (% (sum recent-trits) 3) 0))
    (.append self.history {:role "arbiter" :conserved conserved :trit 0})
    conserved))
```

### DisCoPy Operad Interface

```python
from discopy import *

# Game as operad
class GameOperad:
    def __init__(self):
        self.operations = {}
    
    def register(self, name, dom, cod, rule):
        """Register game operation with GF(3) color."""
        self.operations[name] = Rule(dom, cod, name)
    
    def compose(self, op1, op2):
        """Compose operations preserving GF(3)."""
        trit1 = self.operations[op1].trit
        trit2 = self.operations[op2].trit
        # Result trit balances to 0
        result_trit = (-(trit1 + trit2)) % 3 - 1
        return Rule(
            self.operations[op1].dom,
            self.operations[op2].cod,
            f"{op1};{op2}",
            trit=result_trit
        )

# Define game operations
game = GameOperad()
game.register("attack", Ty("S1", "S2"), Ty("S1'"), lambda: -1)
game.register("defend", Ty("S1'"), Ty("S2'"), lambda: +1)  
game.register("verify", Ty("S1'", "S2'"), Ty("Result"), lambda: 0)
```

## Skill Dispersal Protocol

### 1. Fork Phase (Attacker)

```yaml
fork:
  targets:
    - agent: codex
      path: ~/.codex/skills/
      trit: -1
    - agent: claude
      path: ~/.claude/skills/
      trit: 0
    - agent: cursor
      path: ~/.cursor/skills/
      trit: +1
  gf3_check: true
```

### 2. Sync Phase (Defender)

```yaml
sync:
  strategy: observational-bridge
  bridge_type:
    source: skills@v1
    target: skills@v2
    dimension: 1
  conflict_resolution: 2d-cubical
```

### 3. Verify Phase (Arbiter)

```yaml
verify:
  conservation: gf3
  equivalence: bisimulation
  timeout: 60s
  fallback: last-known-good
```

## MCP Tasks Integration

### Self-Rewriting Task

```json
{
  "task": "skill-dispersal",
  "objective": "Propagate skill updates to all agents",
  "constraints": {
    "gf3_conservation": true,
    "bisimulation_equivalence": true,
    "max_divergence": 0.1
  },
  "steps": [
    {"action": "fork", "trit": -1},
    {"action": "propagate", "trit": 0},
    {"action": "verify", "trit": +1}
  ]
}
```

### Firecrawl Integration

```json
{
  "task": "skill-discovery",
  "objective": "Discover new skills from web resources",
  "tools": ["firecrawl", "exa"],
  "sources": [
    "https://github.com/topics/ai-agent-skills",
    "https://modelcontextprotocol.io/",
    "https://agentclientprotocol.com/"
  ],
  "output": {
    "format": "skill-yaml",
    "destination": ".ruler/skills/"
  }
}
```

## Resilience Patterns

### Redundant Storage

```
~/.codex/skills/     ← Primary (Codex)
~/.claude/skills/    ← Mirror 1 (Claude)
~/.cursor/skills/    ← Mirror 2 (Cursor)
.ruler/skills/       ← Source of truth
```

### Conflict Resolution

```
Dimension 0: Value conflict  → Use source of truth
Dimension 1: Diff conflict   → Merge via LCA
Dimension 2: Meta conflict   → Arbiter decides
```

## Xenomodern Stance

The bisimulation game embodies xenomodernity by:

1. **Ironic distance**: We know perfect equivalence is unattainable, yet we play the game
2. **Sincere engagement**: The game produces real, useful synchronization
3. **Playful synergy**: Attacker/Defender/Arbiter dance together
4. **Conservation laws**: GF(3) as the invariant that holds everything together

```
    xenomodernity
         │
    ┌────┴────┐
    │         │
 ironic    sincere
    │         │
    └────┬────┘
         │
   bisimulation
   (both/neither)
```

## Integration with LocalSend-MCP for Skill Dispersal

Use LocalSend peer discovery for resilient skill propagation:

```python
# localsend_bisim.py
import asyncio
from localsend_mcp import LocalSendClient

class BisimulationDispersalProtocol:
    """Disperse skills via LocalSend with bisimulation verification."""
    
    def __init__(self, skill_path, seed=1069):
        self.skill_path = skill_path
        self.client = LocalSendClient()
        self.rng = SplitMixTernary(seed)
        self.game_log = []
        
    async def discover_peers(self):
        """Find all agents on local network."""
        peers = await self.client.list_peers(source="all")
        return [p for p in peers if p.get("capabilities", []).count("skill-sync")]
    
    async def disperse_with_bisim(self, skill_file):
        """Disperse skill to all peers with bisimulation verification."""
        peers = await self.discover_peers()
        
        for i, peer in enumerate(peers):
            trit = (i % 3) - 1  # Assign trits: -1, 0, +1, -1, ...
            
            # Negotiate transfer session
            session = await self.client.negotiate(
                peer_id=peer["id"],
                preferred_transport="tailscale"  # Or localsend, nats
            )
            
            # Send skill (Attacker move)
            self.game_log.append({
                "round": len(self.game_log),
                "role": "attacker",
                "action": f"send:{skill_file}",
                "peer": peer["id"],
                "trit": trit
            })
            
            result = await self.client.send(
                session_id=session["sessionId"],
                file_path=skill_file
            )
            
            # Verify receipt (Defender move)
            defender_trit = await self.verify_peer_receipt(peer, skill_file)
            self.game_log.append({
                "round": len(self.game_log),
                "role": "defender",
                "action": f"ack:{result['status']}",
                "peer": peer["id"],
                "trit": defender_trit
            })
            
        # Arbiter verifies GF(3) conservation
        return self.verify_gf3_conservation()
    
    def verify_gf3_conservation(self):
        """Check that sum of trits ≡ 0 (mod 3)."""
        total = sum(entry["trit"] for entry in self.game_log)
        conserved = (total % 3) == 0
        self.game_log.append({
            "round": len(self.game_log),
            "role": "arbiter",
            "conserved": conserved,
            "total_trit": total,
            "trit": 0
        })
        return conserved
```

## Temporal vs Derivational Learning Comparison (NEW)

### NEW: Compare Agent-o-rama vs Unworld Patterns

```python
game = BisimulationGame(
    player1_type="temporal_learning",      # agent-o-rama
    player2_type="derivational_learning",  # unworld
    domain="pattern_extraction"
)

# Adversary tries to distinguish them
distinguishable = game.play()

if not distinguishable:
    print("✓ Patterns are behaviorally equivalent")
    print("✓ Can safely switch from temporal to derivational")

    # Migration report
    migration_report = {
        "original_cost": benchmark(agent_o_rama),
        "migrated_cost": benchmark(unworld),
        "speedup": original_cost / migrated_cost,
        "equivalence_verified": game.play()
    }
```

## Concrete Attacker/Defender Example

```
╔══════════════════════════════════════════════════════════════════════╗
║                    BISIMULATION GAME TRANSCRIPT                       ║
╠══════════════════════════════════════════════════════════════════════╣
║ Systems: S₁ = Codex skill state, S₂ = Claude skill state             ║
║ Goal: Prove skills are bisimilar (observationally equivalent)         ║
╠══════════════════════════════════════════════════════════════════════╣

ROUND 1:
  ┌─ ATTACKER (Blue, trit=-1) ─────────────────────────────────────────┐
  │ "I choose S₁ and execute: load_skill('gay-mcp')"                   │
  │ Transition: s₁ →^load s₁' where s₁'.has_skill('gay-mcp') = true    │
  └────────────────────────────────────────────────────────────────────┘
  
  ┌─ DEFENDER (Red, trit=+1) ──────────────────────────────────────────┐
  │ "I match in S₂: load_skill('gay-mcp')"                             │
  │ Transition: s₂ →^load s₂' where s₂'.has_skill('gay-mcp') = true    │
  │ Response: MATCHED ✓                                                 │
  └────────────────────────────────────────────────────────────────────┘
  
  ┌─ ARBITER (Green, trit=0) ──────────────────────────────────────────┐
  │ GF(3) check: (-1) + (+1) + (0) = 0 ≡ 0 (mod 3) ✓                   │
  │ ROUND 1: VALID                                                      │
  └────────────────────────────────────────────────────────────────────┘

ROUND 2:
  ┌─ ATTACKER ─────────────────────────────────────────────────────────┐
  │ "I choose S₂ and execute: generate_color(seed=0x42)"               │
  │ Transition: s₂' →^gen s₂'' where s₂''.color = #FF6B6B              │
  └────────────────────────────────────────────────────────────────────┘
  
  ┌─ DEFENDER ─────────────────────────────────────────────────────────┐
  │ "I match in S₁: generate_color(seed=0x42)"                         │
  │ Transition: s₁' →^gen s₁'' where s₁''.color = #FF6B6B              │
  │ Response: MATCHED ✓ (deterministic - same seed = same color)       │
  └────────────────────────────────────────────────────────────────────┘
  
  ┌─ ARBITER ──────────────────────────────────────────────────────────┐
  │ GF(3) check: (-1) + (+1) + (0) = 0 ≡ 0 (mod 3) ✓                   │
  │ ROUND 2: VALID                                                      │
  └────────────────────────────────────────────────────────────────────┘

ROUND 3:
  ┌─ ATTACKER ─────────────────────────────────────────────────────────┐
  │ "I choose S₁ and execute: self_modify(patch='add_feature')"        │
  │ Transition: s₁'' →^mod s₁''' (skill version incremented)          │
  └────────────────────────────────────────────────────────────────────┘
  
  ┌─ DEFENDER ─────────────────────────────────────────────────────────┐
  │ "I match in S₂ via observational bridge type:"                     │
  │ Bridge: (s₁''.version, s₂''.version) →₁ (s₁'''.version, s₂'''.v)   │
  │ Transition: s₂'' →^mod s₂''' using same patch                      │
  │ Response: MATCHED ✓ (bridge type ensures coherence)                │
  └────────────────────────────────────────────────────────────────────┘
  
  ┌─ ARBITER ──────────────────────────────────────────────────────────┐
  │ GF(3) check: (-1) + (+1) + (0) = 0 ≡ 0 (mod 3) ✓                   │
  │ ROUND 3: VALID                                                      │
  │                                                                     │
  │ After 3 rounds: Defender has matched all Attacker moves            │
  │ Verdict: S₁ ∼ S₂ (bisimilar to depth 3)                            │
  └────────────────────────────────────────────────────────────────────┘

╠══════════════════════════════════════════════════════════════════════╣
║ RESULT: BISIMULATION ESTABLISHED                                      ║
║ - All transitions matched                                             ║
║ - GF(3) conserved across all rounds                                   ║
║ - Skills are observationally equivalent                               ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Verification Output Format

```json
{
  "verification": {
    "timestamp": "2024-12-22T10:30:00Z",
    "systems": ["codex", "claude"],
    "rounds_played": 3,
    "result": "BISIMILAR",
    "gf3_conservation": {
      "total_trit_sum": 0,
      "mod_3": 0,
      "conserved": true
    },
    "game_log": [
      {"round": 1, "attacker": "load_skill", "defender": "matched", "arbiter": "valid"},
      {"round": 2, "attacker": "generate_color", "defender": "matched", "arbiter": "valid"},
      {"round": 3, "attacker": "self_modify", "defender": "bridge_matched", "arbiter": "valid"}
    ],
    "bridge_types_used": [
      {"dim": 1, "source": "v1.2.0", "target": "v1.2.1"}
    ],
    "confidence": 0.99,
    "max_distinguishing_depth": "∞ (no distinguisher found)"
  }
}
```

## Commands

```bash
just bisim-init           # Initialize bisimulation game
just bisim-round          # Play one round
just bisim-disperse       # Disperse skills to all agents
just bisim-verify         # Verify GF(3) conservation
just bisim-reconcile      # Reconcile divergent states
just bisim-localsend      # Disperse via LocalSend peers
just bisim-transcript     # Show attacker/defender transcript
just bisim-json           # Output verification as JSON
```
