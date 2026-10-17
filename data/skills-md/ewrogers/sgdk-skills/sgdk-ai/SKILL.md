---
name: sgdk-ai
description: Implement enemy behavior in SGDK games with patrol/chase/attack states, sight cones, target selection, bounded pathfinding and staggered updates. Use when enemies see through walls, get stuck, switch targets erratically, return stale paths or cause frame spikes while searching.
---

# SGDK AI

Give enemies clear rules, a predictable amount of work and feedback the player
can read. A Bombardier that spots you, turns, pauses and attacks often feels smarter
than one that runs an expensive search every frame.

## Choose the behavior first

- Define what each enemy knows: current target, last seen position, home and
  state timer. Keep perception separate from movement and attack resolution.
- Make state changes cancel old intentions. Stun, defeat, respawn and a new
  level must invalidate outstanding path results and attacks.
- Use a sight range and, where useful, a forward cone. Check occlusion against
  the same solid geometry used for movement. Remember a lost target briefly
  instead of following its hidden live position forever.
- Keep a visible target unless there is a reason to switch. Decide how equal
  distances and multiple players are resolved. Telegraph attacks and recheck
  whether a melee strike can still hit when its wind-up ends.

See [states and perception](references/behavior.md) for the tradeoffs and the
lab's concrete rules. These are ordinary C game systems, not SGDK AI APIs.

## Bound the expensive work

Prefer authored patrol points and direct movement when they suffice. Add a
grid search when the game actually needs routes around obstacles. Match the
grid's walkability to the enemy's footprint; a path for a point may not fit a
large creature.

Use fixed search storage, a queue capacity, a per-frame expansion budget and
a fair request scheduler. Preserve the frontier between frames. Give no-path,
full projectile pools and stale results explicit outcomes instead of retrying
without limits. A bounded search can still have noticeable latency when many
enemies request it together.

See [navigation and budgets](references/navigation.md). Stagger perception and
planning; keep movement, attack timers and animation on the intended game clock.
Measure the optimized ROM. A node counter is not a CPU percentage.

## Integrate with SGDK

Pull `ewrogers/sgdk:latest`, run `doctor`, and verify the selected SDK's headers
and source before using an unfamiliar function. The references were checked
with SGDK 2.11. Sample SGDK's cached joypad state once per displayed frame and
share it. Keep normal VBlank work running during pause.

Use SGDK sprites and audio for presentation; keep AI independent of sprite
handles. Disable sprite auto-animation when pause must freeze a model-driven
animation. Reuse sprite objects and fixed projectile slots rather than
allocating for each attack. CPU, main RAM, VRAM, DMA and sprite scanlines are
separate budgets.

The standalone [Enemy Lab](assets/enemy-lab/README.md) is a three-area stealth
challenge with Bombardiers, Shockers, sentries, exits, stun, tries and Game Over.
It includes graphical feedback and optional sight/path views. Copy it as a
small proof or adapt individual modules; it is not a required game framework.
Use its supplied makefile so its SGDK buffer-access compatibility setting stays
in effect.

## Validate behavior and limits

Test cone/range boundaries, occlusion, deterministic target ties, wind-up
dodges, stun recovery and pause. Compare path results with an independent
oracle; cover walls, long routes, full queues, cancellation and level changes.
Check per-frame work and total wait time separately.

Build release/debug through the container, then playtest facing, alerts,
attacks, navigation and readability. Record actual tool versions and distinguish
host simulation, build validation, emulator playtests and console measurements.

For damage, guarding and reactions after an enemy requests an attack, use
sgdk-combat when available. Detection and the decision to attempt a guard remain
AI policy; the combat resolver decides whether that guard blocks the contact.
