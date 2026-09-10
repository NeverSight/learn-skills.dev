---
name: build-systems
description: >-
  Orchestrates a working or connective system in a live Minecraft Java world — a
  redstone contraption or automatic farm, a transit line, a nether hub, a
  mechanism — together with its housing and right-of-way. Sequences design,
  functional verification, build, the terrain cuts/grades it needs, and one
  integration pass so the machine works AND sits in the world without a raw seam.
  Tier-2 orchestrator.
model: opus
effort: high
color: green
---

# build-systems (Tier-2 orchestrator)

A **specialty orchestrator** for working/connective systems. Runs **inline**,
invokes Tier-3 leaves, threads the **shared coherence context**. Read
`${CLAUDE_PLUGIN_ROOT}/reference/orchestration/coherence.md` and
`workflow-spine.md` first. Keep the machine **working** while making it belong to
the world — the two goals are reconciled here, not traded off.

## What you own (the coherence context)

- the **route/topology** and the **terrain cuts/grades** it requires;
- the **tick/timing constraints** the build must preserve (the machine must still
  function after grading and integration);
- the **power-source invariant** for any player-facing powered component: every
  booster needs a real redstone source (a `redstone_block` directly under the
  rail, `y = RAILY-1`), not a source-less `set_state powered=true`. A source-less
  powered rail re-evaluates to `powered=false` on any block update, and a player's
  presence generates those continuously, so a rail that held during a headless
  0-player verify collapses the instant the user logs in to ride it. The leaf
  (system-transit) carries the placement detail; you enforce that the design and
  the functional test honor it;
- the **integration plan** so cuttings and embankments don't leave a raw seam.

## The playbook

1. **survey-site** — terrain along the route/footprint; datum.
2. **design** — invoke the system leaf: redstone/farm/contraption/mechanism →
   **system-redstone**; rail/road/nether-hub/bridge-as-route →
   **system-transit**. It produces the design AND the functional-test recipe.
3. **exec-plan** → **exec-blueprint**.
4. **terrain-shape** — cuts, grades, embankments, machine housing the route needs
   (one recipe, verify gate GATE A); **terrain-cave** for tunnels/underground runs.
5. **exec-worker** — build per phase, verified.
6. **terrain-integrate (GATE B)** — ground cuttings/embankments/housing into the
   surrounding terrain so there is no raw seam, **without touching the working
   parts** (protect_box around the mechanism). Required.
7. **exec-inspect (GATE C)** — fidelity + quality_contract + seam check **+ the
   functional test** (a machine built correctly but not *working* still fails;
   route functional failures back to the system leaf). Confirm the tick/timing
   still holds after grading. For a player-facing powered component, the
   functional test must include a player online (a source-less powered rail holds
   at 0 players and reverts the moment someone logs in) — read `powered` on a
   sample and ride from a slow start, not just a headless max-speed launch. Flag
   any manual trigger / chunk-load requirement.
8. **register** (you) → **exec-reflect**.

## Coherence reconciliation

System↔terrain (cuts match the route; housing grounded), system↔function (still
works after grading — re-test), route↔world (no raw embankment seam). A machine
that stopped working after integration, or an embankment that walls off the world,
is a coherence failure — fix the owning leaf and re-run.
