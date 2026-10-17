---
name: sgdk-multiplayer
description: Build local SGDK multiplayer with join/leave during play, direct pads and multitaps, shared cameras, independent respawns and fair shared interactions. Use for co-op player ownership and session rules beyond low-level controller polling.
---

# SGDK multiplayer

Keep a controller's logical slot separate from the player it controls. A pad on
`JOY_7` can join as Player 1. Joining, leaving, pausing and respawning are game
rules; SGDK supplies controller snapshots and rendering services.

## Establish the session rules

Agree on participant count, join/leave controls, pause ownership, shared versus
individual progress, body blocking and what happens when everyone is down.
Choose a shared camera, separate screens or another framing policy deliberately.
Do not silently impose the Lab's four-player cap, theme or tuning on another game.

Pull `ewrogers/sgdk:latest` and verify its controller headers and implementation.
Read [controller routes and SGDK contracts](references/contracts.md) before
configuring adapters. sgdk-input covers low-level input; this skill owns the
participant/session layer. It does not implement network multiplayer.

## Keep device and participant ownership stable

- Build a route table from the actual port topology. Enable detected Team
  Players explicitly; EA 4-Way Play occupies both ports. Do not assume four
  consecutive `JOY_*` IDs belong to one adapter.
- Snapshot each logical pad once after normal SDK service. Seed held-button
  history after setup/rescan so a held Start cannot create a phantom join.
- Process a fresh Start on an unused pad as Join before considering Pause.
  Consume Leave edges too. Simultaneous pause requests must toggle only once.
- Preserve each participant's device assignment until an explicit departure.
  Quiet input or cached pad type is not reliable disconnect detection.
- Rescan during setup or a controlled session change. SGDK's reset includes
  VBlank processing; do not insert it into an ordinary gameplay tick.

## Make shared play predictable

Calculate every player's proposed movement before applying the group constraint.
A shared camera should not favor Player 1 just because that player updates first.
Keep collision correction and the final camera span compatible. Let players
move inward to regroup; exclude downed participants from the live framing set.

Use a bounded respawn search with walkability, group visibility and a temporary
protection policy. If no candidate fits, retry later rather than spawning inside
a wall. Define an all-down checkpoint separately. Pause must freeze gameplay
timers, while still allowing the chosen join/resume controls.

Resolve shared pickups once. Use nearest-player ownership or another explicit
rule; break equal-distance ties fairly. Keep deterministic update order and
consume input edges only once even if PAL scheduling runs two simulation ticks.

See [camera, respawn and testing patterns](references/session.md) and the
standalone [Co-op Lab: Bellkeepers](assets/coop-lab/README.md). Its C model has no
SDK dependencies; the renderer uses normal SGDK APIs. It is an executable
example, not a required framework.

## Budget and prove the combined case

Budget all joined players, enemies, effects and HUD together. Share palettes by
art role where useful; do not spend one palette per player by default. Account
for hardware pieces and same-line pixels as well as logical sprite counts.

Test join/leave races, capacity, simultaneous Start, pause joins, last-player
departure, all-down recovery and equal-distance pickups. Compare PAL/NTSC logic
schedules and compile both release/debug builds for the base 68000. Check actual
presentation and sound in an emulator, then validate intended physical pads and
adapter models on a console. The CPU tour proves four-character gameplay and
presentation; it does not test multitap electronics or the polling protocol.

Use sgdk-performance for measured frame costs, sgdk-raster for split-screen
rendering and sgdk-hardware for physical compatibility checks when available.

For damage filtering, friendly fire and hit reactions between participants,
use sgdk-combat when available. Preserve the session’s player assignments and
respawn rules rather than creating a second participant registry.
