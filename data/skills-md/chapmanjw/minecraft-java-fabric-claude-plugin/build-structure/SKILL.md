---
name: build-structure
description: >-
  Orchestrates a single named or standalone structure and the ground it sits on
  in a live Minecraft Java world — a building, a real-world or fictional replica,
  a statue or monument, a player house, or a bridge as an object. Sequences
  design, plan, blueprint, build, grading, and one integration pass so the
  structure reads as belonging to its site rather than dropped onto it. Tier-2
  orchestrator (handles the "one sited thing" case the no-trivial rule makes a
  first-class path).
model: opus
effort: high
color: green
---

# build-structure (Tier-2 orchestrator)

A **specialty orchestrator** for one sited structure or art piece. Runs
**inline**, invokes Tier-3 leaves, threads the **shared coherence context** so
the thing sits in the world. Read
`${CLAUDE_PLUGIN_ROOT}/reference/orchestration/coherence.md` and
`workflow-spine.md` first. Every request runs this — there is no "trivial" inline
path; a tiny build is just a shallow pass through the same gated spine.

## What you own (the coherence context)

- **one architectural/material vocabulary** across the structure's parts;
- the **site datum + pad grade**;
- the **integration plan** that grounds the footprint (foundation talus/apron) so
  the structure belongs to its spot.

## The playbook

1. **survey-site** — the real site + datum.
2. **survey-research** — for a replica/real reference (a named building, a
   landmark), pull facts first.
3. **design** — invoke the right design leaf: a building/replica →
   **design-building**; a statue/monument/sculpture/pixel-art →
   **design-monument**; a player's base/house → **design-house**.
4. **exec-plan** → **exec-blueprint** (reusable `mcb:*` modules).
5. **terrain-shape** — pad/grade the site to the datum if needed (one recipe,
   verify gate GATE A). For a cave base, **terrain-cave** carves the chamber.
6. **exec-worker** — build per phase, verified.
7. **terrain-integrate (GATE B)** — ground the footprint: foundation talus, apron
   erosion, biome blend, so there is no hard structure↔world edge. Required.
8. **exec-inspect (GATE C)** — fidelity + quality_contract + seam check at
   eye-level/iso; for a monument, silhouette/proportion; for a contraption-bearing
   structure, hand systems to build-systems. Reconcile: pad matches grade,
   foundation grounded not floating.
9. **register** (you) → **exec-reflect**.

## Coherence reconciliation

Structure↔site (pad to datum), structure↔world (foundation grounded by integrate),
parts↔vocabulary (one palette/style). A structure that floats, trenches, or clashes
with its surroundings is a coherence failure — fix and re-run.
