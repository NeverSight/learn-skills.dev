---
name: gate-graph
description: Find overlap and dead weight in a Python gate layer by extracting AST fingerprints, generating an overlap matrix, and failing CI when redundant gates or too many gates are detected.
when_to_use: Your agent has dozens of gate/validator/middleware modules and you need a deterministic offline signal for consolidation candidates, duplicated checks, and dead gates before CI token/latency spending grows. NOT a replacement for semantic tests.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [agent-governance, gate-maintenance, overlap, redundancy, ci, python-ast]
---

# Gate Graph

Turn a sprawling gate/validator/middleware layer into a deterministic map: how
many modules, which ones overlap, and which are wired to nothing.

## Overview

Long-lived agents grow gates the way houses grow junk drawers. Each new check
looks cheap, but every module in the pipeline is code the agent pays for on
every request — in tokens, latency, and maintenance surface. Nobody removes one
because nobody can prove it's redundant or dead. `gate_graph.py` is that proof:
it parses every module with the `ast` stdlib (no imports run, nothing executes),
builds a structural fingerprint per module (functions, classes, attributes,
regex/substring literals, raised exceptions), and reports three things —
**how many gates**, **which pairs overlap** (Jaccard on fingerprints), and
**which gates are orphans** (imported nowhere in the tree). It exits non-zero
when the gate count blows a budget or two gates overlap past a threshold, so it
drops straight into CI.

Real run against a production agent's gate layer: **56 modules, 26 orphans
imported nowhere, and `self_mod_canary` ↔ `self_mod_canary_io` at 0.43 overlap**
— exactly the "declared but never wired" and "split then forgotten" patterns
that hand-maintained inventory whitelists miss.

## When to use

- A pipeline has grown to dozens of gate/validator/middleware modules and you
  suspect duplication or dead code.
- You want CI to fail when the gate count grows past a budget, or when two gates
  structurally converge (a sign one should absorb the other).
- You're deciding what to consolidate and want a matrix, not vibes.

Not for: semantic correctness (two gates can look similar and do different
things — read the overlap as a *candidate*, then confirm), or replacing tests.

## The method

1. **Point it at the gate directory.**
   ```bash
   python scripts/gate_graph.py path/to/gates --max-gates 40 --max-overlap 0.5
   ```
   It recurses, skips `__init__.py` and vendor/cache dirs, and fingerprints
   each remaining module offline.
2. **Read the three signals.**
   - *Gate count* vs `--max-gates`: your growth budget.
   - *High-overlap pairs* (> `--max-overlap`): consolidation candidates. Only
     these carry the shared/left-only/right-only fingerprint diff so you can see
     *what* they duplicate.
   - *Orphan gates*: modules imported nowhere in the tree — dead until proven
     otherwise. Confirm none are dynamically loaded before deleting.
3. **Wire it into CI.** The tool exits non-zero over either budget:
   ```yaml
   # .github/workflows/gate-graph.yml
   - run: python scripts/gate_graph.py src/agent/gates --max-gates 40 --max-overlap 0.5
   ```
   Now "the gate layer got fatter" fails the build instead of silently taxing
   every request.
4. **Consolidate the top, re-measure.** Merge an overlapping pair, delete a
   confirmed orphan, then re-run. The count and matrix are the scoreboard.

## Output modes

- **Default (text):** human-readable report — fingerprint counts, the full
  matrix, high-overlap pairs, orphans, and a `FAIL:` line per breach.
- **`--json`:** machine-readable and **deliberately lean** — gate names,
  orphans, the top ranked pairs (name + score only), and the heavy
  fingerprint diff *only* for pairs that breach the threshold. On a 56-gate
  layer this is ~12 KB.
- **`--json --full-matrix`:** adds the full NxN matrix and every module's
  fingerprint set (~210 KB on the same layer). Opt in only when you need it.

## Anti-patterns

- **Dumping every pair's fingerprint diff.** With N gates there are N² pairs;
  attaching the full shared/diff sets to all of them is the exact token bloat
  this tool exists to catch. The JSON stays lean by default and enriches only
  breaching pairs — a gate-maintenance tool must not itself be the bloat.
- **Deleting an orphan on sight.** "Imported nowhere" is a strong signal, not a
  proof — check for dynamic/string-based loading (`importlib`, registries, hook
  tables) first.
- **Treating overlap as duplication.** High Jaccard means *structurally
  similar*, which is a review prompt, not a verdict. Confirm behavior before merging.
- **Hardcoding the inventory.** The point is that the map is recomputed from the
  AST every run — a static "these are the real gates" whitelist rots the moment
  someone adds a module.

## Example

```
$ python scripts/gate_graph.py src/agent/gates --max-gates 40 --max-overlap 0.5
Gate-graph overlap report
==============================
gates: 56
max-gates: 40
max-overlap: 0.5
...
High-overlap candidate pairs:
  self_mod_canary <-> self_mod_canary_io: 0.43   (below 0.5 threshold, watch)

Orphan gates:
  - actionable_resource_model
  - temporal_live_claims
  ... (26 total)
FAIL: gate_count 56 > max_gates 40
$ echo $?
1
```
