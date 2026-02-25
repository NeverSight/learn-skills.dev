---
name: structural-rewilding
description: "Homotopical approach to Artificial Life where 'life' is the topology of changes (diffs). Three orthogonal directions: Behavioral (→), Structural (↓), Bridge (↘) with Narya interaction-time verification."
version: 1.0.0
---


# Structural Rewilding: Homotopical Artificial Life

> *"Life is not just the state of the system, but the topology of the changes (diffs) it can undergo."*
> — zubyul synthesis

## Overview

**Structural Rewilding** applies homotopy type theory to Artificial Life, treating organisms as **morphisms between states** rather than states themselves. The key insight: verification happens at **interaction time** via Narya bridge types, not static self-verification.

## The Three Orthogonal Vectors of Change

```
          STRUCTURAL (↓)
          Type/Form Diff
              │
              │ δS: Diff Type A B
              │
              ▼
    ┌─────────────────────────────┐
    │                             │
    │   BEHAVIORAL (→)            │
    │   State/Function Diff       │──────────────────────▶
    │   δB: path within type      │     time evolution
    │                             │
    └─────────────────────────────┘
              │
              │ BRIDGE (↘)
              │ Coherence Diff
              │ δC: 2-cell verifying δS preserves δB
              ▼
```

| Vector | Symbol | Meaning | Narya Term |
|--------|--------|---------|------------|
| **Horizontal** | δB | Behavioral/State Diff | Path within type |
| **Vertical** | δS | Structural/Type Diff | `Diff Type A B` |
| **Diagonal** | δC | Bridge/Coherence Diff | 2-cell, "diff of diffs" |

## Interaction Time Verification

Unlike static type checking, verification occurs **during interaction**:

```narya
-- The bridge is constructed at interaction time
def verify_rewilding 
  (Old New : World) 
  (structural_change : Diff World Old New)
  (behavior : Old → Action) 
  : Bridge (behavior Old) (behavior New) := 
    construct_at_runtime structural_change behavior
```

**Key Properties:**
- Bridge types are *computational proofs*
- Verification is *lazy* (constructed when needed)
- Failure = type error at interaction boundary

## A-Life Model Analysis

### 1. Continuous Substrate: Neural Cellular Automata & Lenia

**Models**: H-Lenia, Neural Particle Automata, Flow-Lenia

| Vector | Diff | Verification |
|--------|------|--------------|
| δB | `Update(State)` | Conservation laws (mass, energy) |
| δS | Add hierarchical layer: `L1 → L1 + L2` | Functor mapping resolutions |
| δC | Does new layer preserve soliton stability? | Energy coherence between layers |

```python
class HLeniaBridge:
    """Bridge type for H-Lenia structural changes."""
    
    def verify(self, layer1_state, layer2_state):
        # Bridge validates energy coherence
        energy_l1 = self.compute_energy(layer1_state)
        energy_l2 = self.compute_energy(layer2_state)
        
        # Coherence: energy flow must be consistent
        return abs(energy_l1 - energy_l2) < self.epsilon
    
    def rewild(self, state, new_layer):
        """Add layer only if bridge validates."""
        bridge = self.construct_bridge(state, new_layer)
        if not bridge.is_valid():
            raise BridgeError("Structural change breaks soliton stability")
        return state.with_layer(new_layer)
```

**Rewilding Effect**: System grows new spatial dimensions/resolutions on-the-fly without breaking organism persistence.

### 2. Semantic Substrate: LLM Societies & Language Agents

**Models**: Society of Mind on ALTER3, Internalist Cultural Evolution

| Vector | Diff | Verification |
|--------|------|--------------|
| δB | Next token prediction | Conversation coherence |
| δS | Protocol change: `OpenChat → RestrictedMessage` | Module addition/removal |
| δC | New module maintains agent identity? | Semantic consistency bridge |

```python
class SemanticBridge:
    """Bridge for LLM module rewilding."""
    
    def verify_module_addition(self, agent, new_module):
        # Get agent's identity invariant
        identity = agent.extract_identity()
        
        # Simulate with new module
        test_messages = agent.generate_with(new_module)
        
        # Bridge validates identity preservation
        return all(
            self.maintains_identity(msg, identity) 
            for msg in test_messages
        )
```

**Rewilding Effect**: Society of Mind becomes fluid. K-lines form/dissolve dynamically, validated by coherence with agent identity.

### 3. Logical/Discrete Substrate: Digital Circuits & Rule Evolution

**Models**: Self-Organizing Digital Circuits, QD-LEAR

| Vector | Diff | Verification |
|--------|------|--------------|
| δB | Signal propagation: `Input → Output` | I/O correctness |
| δS | Graph transformer rewires LUTs | Topology patch |
| δC | Rewiring preserves function? | `f(I) = f'(I)` for all I |

```python
class CircuitBridge:
    """Bridge for circuit topology rewilding."""
    
    def verify_rewiring(self, old_circuit, new_circuit, test_inputs):
        # Structure can drift wildly...
        # ...as long as function remains pinned
        for inp in test_inputs:
            old_out = old_circuit(inp)
            new_out = new_circuit(inp)
            if old_out != new_out:
                return False
        return True
    
    def rewild(self, circuit, damage_location):
        """Reroute around damage while preserving function."""
        candidate = circuit.propose_rewiring(damage_location)
        bridge = self.verify_rewiring(circuit, candidate, self.test_suite)
        if not bridge:
            raise BridgeError("Rewiring changes circuit function")
        return candidate
```

**Rewilding Effect**: Circuit becomes "liquid" - constantly rewriting topology for optimization without halting execution.

## Scale MG Standard: Transitivity and Coherence

In a **Skills Dynamic Graph (G)**, every capability is a node. Structural rewilding = adding/removing nodes and edges.

### The Transitivity Property

```
If Skill A → Skill B and we add Skill C bridging them:

    A ──────→ B
     ╲       ↗
      ╲     ╱
       ╲   ╱
        ↘ ↙
         C

We need a 2-cell (surface) filling the triangle.
```

**In Narya Terms:**
```narya
def transitivity_bridge
  (A B C : Skill)
  (ab : A → B)
  (ac : A → C)
  (cb : C → B)
  : Bridge ab (ac >> cb) := 
    -- Constructed at interaction time
    interaction_verify ac cb
```

### Coherence on the Way In

Using Narya, we don't just "add" a skill. We define a **Diff** between world models:

```narya
-- Step 1: Define the Diff
def add_skill : Diff World Old New := ...

-- Step 2: Construct the Bridge
-- Must show how every neighbor adapts
def bridge : Bridge Old.behaviors New.behaviors := 
  -- Example: Tool Use added to Foraging agent
  -- Bridge maps Forage(EmptyHand) → Forage(Tool)
  fun old_behavior => 
    match old_behavior with
    | Forage(EmptyHand) => Forage(Tool)
    | other => other

-- Step 3: Verification
-- If agent cannot instantiate bridge, skill not admitted
```

**Result**: World Model remains a continuous manifold of behavior, not a fractured set of disconnected scripts.

## GF(3) Integration

### The Rewilding Triad

```
alife (-1)              ⊗ structural-rewilding (0) ⊗ unified-continuations (+1) = 0 ✓
(state observation)        (topology of change)      (change execution)
```

### Direction-Trit Mapping

| Direction | Trit | Role |
|-----------|------|------|
| δB (Behavioral) | -1 | Observes current state |
| δS (Structural) | 0 | Coordinates type changes |
| δC (Bridge) | +1 | Generates verification proofs |

**Conservation**: δB + δS + δC = -1 + 0 + 1 = 0 ✓

## DiscoHy Implementation

```hy
#!/usr/bin/env hy
;; structural_rewilding.hy - Homotopical A-Life

(defclass StructuralRewilding []
  "Three orthogonal vectors of change with bridge verification."
  
  (defn __init__ [self substrate]
    (setv self.substrate substrate)  ;; continuous, semantic, or discrete
    (setv self.bridges {})
    (setv self.trit 0))
  
  (defn delta-behavioral [self state]
    "δB: Horizontal arrow, state evolution. Trit -1."
    {"type" "behavioral"
     "trit" -1
     "diff" (self.substrate.update state)})
  
  (defn delta-structural [self old-type new-type]
    "δS: Vertical arrow, type mutation. Trit 0."
    {"type" "structural"
     "trit" 0
     "diff" {"from" old-type "to" new-type}})
  
  (defn delta-bridge [self structural behavioral]
    "δC: Diagonal arrow, coherence verification. Trit +1."
    (setv bridge-proof (self.construct-bridge structural behavioral))
    {"type" "bridge"
     "trit" 1
     "valid" (bridge-proof.verify)
     "proof" bridge-proof})
  
  (defn rewild [self state structural-change]
    "Apply structural change only if bridge validates."
    (setv delta-b (self.delta-behavioral state))
    (setv delta-s (self.delta-structural state.type structural-change))
    (setv delta-c (self.delta-bridge delta-s delta-b))
    
    (when (not (:valid delta-c))
      (raise (ValueError "Bridge verification failed: change breaks coherence")))
    
    ;; GF(3) conservation check
    (setv total (+ (:trit delta-b) (:trit delta-s) (:trit delta-c)))
    (assert (= (% total 3) 0) "GF(3) violation in rewilding")
    
    (self.substrate.apply-change state structural-change)))
```

## Continuation Interrelation

Structural rewilding connects to all continuation paradigms:

| Continuation | Rewilding Analog |
|--------------|------------------|
| **call/cc** | Capture current substrate state (δB snapshot) |
| **shift/reset** | Delimited structural change (δS within boundary) |
| **CPS** | Explicit bridge passing (δC as continuation) |
| **Kleisli** | Compositional rewilding (δS₁ >> δS₂) |
| **2TDX** | Directed structural change (no backtracking) |
| **Goblins** | Capability-safe rewilding (vow-based verification) |

## Commands

```bash
# Rewild substrate with verification
just rewild-continuous state new_layer    # H-Lenia hierarchy
just rewild-semantic agent new_module     # LLM society
just rewild-discrete circuit damage       # Circuit routing

# Verify bridge coherence
just bridge-verify old new structural_change

# Check transitivity in skill graph
just skill-transitivity A B C

# GF(3) conservation audit
just gf3-audit rewilding_log
```

## References

### ALIFE 2025
- H-Lenia: Hierarchical continuous cellular automata
- Flow-Lenia: Mass-conserving via continuity equation (arXiv:2506.08569)
- Neural Particle Automata: Gradient-based self-organization
- Society of Mind on ALTER3: Modular LLM agents
- Self-Organizing Digital Circuits: Liquid circuit topology

### Type Theory
- Narya: Higher-dimensional type theory with bridge types
- Riehl-Shulman: Synthetic ∞-categories
- 2TDX: Directed extension types

### zubyul Synthesis
- Three orthogonal directions: δB, δS, δC
- Interaction Time Verification
- Scale MG transitivity standard
- Coherence on the way in

---

**Skill Name**: structural-rewilding
**Type**: Homotopical Artificial Life / Type-Theoretic Morphogenesis
**Trit**: 0 (ERGODIC - coordinates topology of changes)
**GF(3)**: Conserved via triadic vector decomposition



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
structural-rewilding (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch7: Propagators
- Ch4: Pattern Matching
- Ch6: Layering
- Ch2: Domain-Specific Languages

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.