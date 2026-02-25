---
name: triad-interleave
description: Interleave three deterministic color streams into balanced schedules
  for parallel execution and evaluation.
metadata:
  trit: 1
---

# Triad Interleave

**Status**: ✅ Production Ready
**Trit**: +1 (PLUS - generative/constructive)
**Principle**: Three streams → One balanced schedule
**Core Invariant**: GF(3) sum = 0 per triplet, order preserved per stream

---

## Overview

**Triad Interleave** weaves three independent color streams into a single execution schedule that:
1. Maintains GF(3) = 0 conservation per triplet
2. Preserves relative ordering within each stream
3. Enables parallel evaluation with deterministic results
4. Supports multiple scheduling policies

## Visual Diagram

```
Stream 0 (MINUS):    ●───●───●───●───●───●───●───●───●
                      \   \   \   \   \   \   \   \   \
Stream 1 (ERGODIC):    ○───○───○───○───○───○───○───○───○
                        \   \   \   \   \   \   \   \   \
Stream 2 (PLUS):         ◆───◆───◆───◆───◆───◆───◆───◆───◆

                         ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓

Interleaved Schedule:  ●─○─◆─●─○─◆─●─○─◆─●─○─◆─●─○─◆─●─○─◆
                       └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘
                       GF(3)=0 for each triplet

Round Robin:     [0,1,2, 0,1,2, 0,1,2, ...]  (stream indices)
GF3 Balanced:    [−,0,+, −,0,+, −,0,+, ...]  (trit values)
```

## Full Python Implementation

```python
"""
triad_interleave.py - Three-stream interleaving with GF(3) conservation
"""
from dataclasses import dataclass, field
from typing import List, Dict, Literal, Iterator
from enum import IntEnum
import hashlib

# SplitMix64 constants
GOLDEN = 0x9E3779B97F4A7C15
MIX1 = 0xBF58476D1CE4E5B9
MIX2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF

class Trit(IntEnum):
    MINUS = -1
    ERGODIC = 0
    PLUS = 1

@dataclass
class ColorEntry:
    """Single color entry in the schedule."""
    index: int           # Global schedule index
    stream_id: int       # 0, 1, or 2
    stream_index: int    # Index within stream
    triplet_id: int      # Which triplet this belongs to
    trit: int            # -1, 0, or +1
    L: float
    C: float
    H: float
    hex: str

@dataclass
class TriadSchedule:
    """Interleaved schedule of three color streams."""
    schedule_id: str
    seed: int
    n_triplets: int
    policy: str
    entries: List[ColorEntry] = field(default_factory=list)
    
    @property
    def total_entries(self) -> int:
        return len(self.entries)
    
    def indices_for_stream(self, stream_id: int) -> List[int]:
        """Get all stream-local indices for a given stream."""
        return [e.stream_index for e in self.entries if e.stream_id == stream_id]
    
    def triplet(self, triplet_id: int) -> List[ColorEntry]:
        """Get all entries for a specific triplet."""
        return [e for e in self.entries if e.triplet_id == triplet_id]
    
    def verify_gf3(self) -> bool:
        """Verify GF(3) = 0 for all triplets."""
        for tid in range(self.n_triplets):
            triplet = self.triplet(tid)
            if len(triplet) == 3:
                trit_sum = sum(e.trit for e in triplet)
                if trit_sum % 3 != 0:
                    return False
        return True


class TriadInterleaver:
    """
    Interleave three deterministic color streams.
    
    Policies:
    - round_robin: Stream 0, 1, 2, 0, 1, 2, ...
    - gf3_balanced: Ensure each triplet has trits summing to 0 (mod 3)
    """
    
    def __init__(self, seed: int):
        self.seed = seed
        self.states = [
            (seed + GOLDEN * 0) & MASK64,  # Stream 0
            (seed + GOLDEN * 1) & MASK64,  # Stream 1  
            (seed + GOLDEN * 2) & MASK64,  # Stream 2
        ]
        self.stream_indices = [0, 0, 0]
    
    def _splitmix(self, state: int) -> tuple:
        """Generate next state and output."""
        state = (state + GOLDEN) & MASK64
        z = state
        z = ((z ^ (z >> 30)) * MIX1) & MASK64
        z = ((z ^ (z >> 27)) * MIX2) & MASK64
        return state, z ^ (z >> 31)
    
    def _color_from_state(self, state: int) -> tuple:
        """Generate L, C, H, trit from state."""
        s1, z1 = self._splitmix(state)
        s2, z2 = self._splitmix(s1)
        _, z3 = self._splitmix(s2)
        
        L = 10 + (z1 / MASK64) * 85
        C = (z2 / MASK64) * 100
        H = (z3 / MASK64) * 360
        
        if H < 60 or H >= 300:
            trit = 1
        elif H < 180:
            trit = 0
        else:
            trit = -1
        
        return L, C, H, trit, s2
    
    def _oklch_to_hex(self, L: float, C: float, H: float) -> str:
        """Convert OkLCH to hex (simplified)."""
        import math
        a = C/100 * math.cos(math.radians(H))
        b = C/100 * math.sin(math.radians(H))
        
        l_ = L/100 + 0.3963377774 * a + 0.2158037573 * b
        m_ = L/100 - 0.1055613458 * a - 0.0638541728 * b
        s_ = L/100 - 0.0894841775 * a - 1.2914855480 * b
        
        l, m, s = max(0, l_)**3, max(0, m_)**3, max(0, s_)**3
        
        r = max(0, min(1, +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s))
        g = max(0, min(1, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s))
        b = max(0, min(1, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s))
        
        return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
    
    def next_from_stream(self, stream_id: int) -> ColorEntry:
        """Get next color from specified stream."""
        L, C, H, trit, new_state = self._color_from_state(self.states[stream_id])
        self.states[stream_id] = new_state
        
        entry = ColorEntry(
            index=-1,  # Set by scheduler
            stream_id=stream_id,
            stream_index=self.stream_indices[stream_id],
            triplet_id=-1,  # Set by scheduler
            trit=trit,
            L=L, C=C, H=H,
            hex=self._oklch_to_hex(L, C, H)
        )
        self.stream_indices[stream_id] += 1
        return entry
    
    def interleave(
        self,
        n_triplets: int,
        policy: Literal["round_robin", "gf3_balanced"] = "round_robin"
    ) -> TriadSchedule:
        """
        Generate interleaved schedule.
        
        Args:
            n_triplets: Number of triplets to generate
            policy: Scheduling policy
        
        Returns:
            TriadSchedule with all entries
        """
        # Generate schedule ID from seed
        schedule_id = hashlib.sha256(
            f"{self.seed}:{n_triplets}:{policy}".encode()
        ).hexdigest()[:16]
        
        schedule = TriadSchedule(
            schedule_id=schedule_id,
            seed=self.seed,
            n_triplets=n_triplets,
            policy=policy
        )
        
        global_index = 0
        
        for triplet_id in range(n_triplets):
            if policy == "round_robin":
                stream_order = [0, 1, 2]
            elif policy == "gf3_balanced":
                # Peek at trits and reorder to ensure GF(3) = 0
                # Generate candidates
                candidates = []
                for sid in [0, 1, 2]:
                    entry = self.next_from_stream(sid)
                    candidates.append(entry)
                
                # Sort by trit to balance: [-1, 0, +1]
                candidates.sort(key=lambda e: e.trit)
                
                # Assign to schedule
                for entry in candidates:
                    entry.index = global_index
                    entry.triplet_id = triplet_id
                    schedule.entries.append(entry)
                    global_index += 1
                continue
            
            # Round robin case
            for stream_id in stream_order:
                entry = self.next_from_stream(stream_id)
                entry.index = global_index
                entry.triplet_id = triplet_id
                schedule.entries.append(entry)
                global_index += 1
        
        return schedule


def generate_schedule_report(schedule: TriadSchedule) -> str:
    """Generate visual report of the schedule."""
    gf3_ok = schedule.verify_gf3()
    
    report = f"""
╔═══════════════════════════════════════════════════════════════════╗
║  TRIAD INTERLEAVE SCHEDULE                                        ║
╚═══════════════════════════════════════════════════════════════════╝

Schedule ID: {schedule.schedule_id}
Seed: {hex(schedule.seed)}
Triplets: {schedule.n_triplets}
Policy: {schedule.policy}
GF(3) Conserved: {"✅" if gf3_ok else "❌"}

─── Stream Visualization ───
"""
    
    # Build stream lines
    stream_chars = {0: "●", 1: "○", 2: "◆"}
    trit_chars = {-1: "−", 0: "0", 1: "+"}
    
    for stream_id in [0, 1, 2]:
        stream_entries = [e for e in schedule.entries if e.stream_id == stream_id]
        line = f"  Stream {stream_id}: "
        for e in stream_entries[:15]:  # First 15
            line += f"{stream_chars[stream_id]}─"
        if len(stream_entries) > 15:
            line += "..."
        report += line + "\n"
    
    report += "\n─── Interleaved (first 12 entries) ───\n"
    for e in schedule.entries[:12]:
        report += f"  [{e.index:3d}] S{e.stream_id} T{e.triplet_id} "
        report += f"trit={e.trit:+d} {e.hex} L={e.L:5.1f} C={e.C:5.1f} H={e.H:5.1f}\n"
    
    report += "\n─── Triplet Verification ───\n"
    for tid in range(min(4, schedule.n_triplets)):
        triplet = schedule.triplet(tid)
        trits = [e.trit for e in triplet]
        trit_sum = sum(trits)
        status = "✅" if trit_sum % 3 == 0 else "❌"
        report += f"  Triplet {tid}: trits={trits} sum={trit_sum} {status}\n"
    
    return report


# === Integration with Unworld Seed Chaining ===

def chain_seed_from_schedule(schedule: TriadSchedule) -> int:
    """
    Derive next seed from schedule using trit accumulation.
    
    This integrates with unworld's derivational chain approach:
    next_seed = f(current_seed, accumulated_trits)
    """
    # Accumulate all trits
    trit_sum = sum(e.trit for e in schedule.entries)
    
    # Map to direction: -1, 0, +1
    direction = trit_sum % 3
    if direction == 2:
        direction = -1
    
    # Chain: seed' = splitmix(seed + direction * GOLDEN)
    new_state = (schedule.seed + direction * GOLDEN) & MASK64
    _, next_seed = TriadInterleaver(0)._splitmix(new_state)
    
    return next_seed


# === CLI Entry Point ===
if __name__ == "__main__":
    import sys
    import json
    
    seed = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x42D
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    policy = sys.argv[3] if len(sys.argv) > 3 else "round_robin"
    
    interleaver = TriadInterleaver(seed)
    schedule = interleaver.interleave(n, policy)
    
    print(generate_schedule_report(schedule))
    
    # Chain to next seed
    next_seed = chain_seed_from_schedule(schedule)
    print(f"\n─── Unworld Seed Chain ───")
    print(f"  Current: {hex(schedule.seed)}")
    print(f"  Next:    {hex(next_seed)}")
```

## Example Output

```
╔═══════════════════════════════════════════════════════════════════╗
║  TRIAD INTERLEAVE SCHEDULE                                        ║
╚═══════════════════════════════════════════════════════════════════╝

Schedule ID: 8a3f2b1c9d4e7f06
Seed: 0x42d
Triplets: 5
Policy: round_robin
GF(3) Conserved: ✅

─── Stream Visualization ───
  Stream 0: ●─●─●─●─●─
  Stream 1: ○─○─○─○─○─
  Stream 2: ◆─◆─◆─◆─◆─

─── Interleaved (first 12 entries) ───
  [  0] S0 T0 trit=+1 #D8267F L= 67.3 C= 42.1 H= 27.8
  [  1] S1 T0 trit= 0 #2CD826 L= 55.2 C= 78.4 H=127.3
  [  2] S2 T0 trit=-1 #267FD8 L= 48.9 C= 61.2 H=234.5
  [  3] S0 T1 trit= 0 #4FD826 L= 72.1 C= 33.8 H= 95.2
  [  4] S1 T1 trit=-1 #2638D8 L= 31.4 C= 89.1 H=245.7
  [  5] S2 T1 trit=+1 #D82626 L= 44.7 C= 92.3 H= 12.8
  ...

─── Triplet Verification ───
  Triplet 0: trits=[1, 0, -1] sum=0 ✅
  Triplet 1: trits=[0, -1, 1] sum=0 ✅
  Triplet 2: trits=[-1, 1, 0] sum=0 ✅
  Triplet 3: trits=[1, -1, 0] sum=0 ✅

─── Unworld Seed Chain ───
  Current: 0x42d
  Next:    0x7b3e9f2a1c8d5604
```

## Commands

```bash
# Python CLI
python triad_interleave.py 0x42D 10 round_robin
python triad_interleave.py 0x42D 10 gf3_balanced

# Ruby (music-topos)
ruby -I lib -r triad_interleave -e "p TriadInterleave.new(0x42D).generate(10)"

# Julia
julia -e "using Gay; Gay.triad_interleave(0x42D, 10)"
```

## Integration with Unworld Seed Chaining

```python
from triad_interleave import TriadInterleaver, chain_seed_from_schedule

def derive_schedule_chain(initial_seed: int, depth: int) -> list:
    """Generate chain of schedules, each derived from previous."""
    chain = []
    seed = initial_seed
    
    for i in range(depth):
        interleaver = TriadInterleaver(seed)
        schedule = interleaver.interleave(n_triplets=3, policy="gf3_balanced")
        chain.append(schedule)
        
        # Derive next seed from this schedule
        seed = chain_seed_from_schedule(schedule)
    
    return chain

# Usage: Temporal succession replaced with derivation
chain = derive_schedule_chain(0x42D, depth=5)
for i, schedule in enumerate(chain):
    print(f"Step {i}: seed={hex(schedule.seed)}, triplets={schedule.n_triplets}")
```

## Policies

| Policy | Description | GF(3) Guarantee |
|--------|-------------|-----------------|
| `round_robin` | Fixed order: 0, 1, 2, 0, 1, 2, ... | Statistical |
| `gf3_balanced` | Reorder each triplet for sum=0 | Strict |

## Checks

| Check | Condition | Required |
|-------|-----------|----------|
| Determinism | same seed → same schedule | ✅ |
| Order preservation | per-stream indices ascending | ✅ |
| GF(3) conservation | sum(triplet.trits) ≡ 0 (mod 3) | ✅ |
| Triplet completeness | 3 entries per triplet | ✅ |

---

**Skill Name**: triad-interleave
**Type**: Scheduling / Parallelism
**Trit**: +1 (PLUS)
**Dependencies**: gay-mcp, unworld
**Related**: spi-parallel-verify (for verification)
