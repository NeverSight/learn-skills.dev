---
name: sgdk-collision
description: Build reliable SGDK collision queries with swept boxes, finite ray tests, moving-target detection and bounded wall sliding. Use for tunnelling, contact and collision-response problems rather than a general physics engine.
---

# SGDK collision

Use this skill when endpoint overlap checks miss fast motion, an aiming or sight
query needs its first obstruction, or movement should slide along solid walls.
The provided routines are original C algorithms, not SGDK collision APIs.

## Decide what the query means

- Keep collision geometry in world/local simulation coordinates. Apply cameras
  only when rendering. Sprite art, visible pixels and hardware sprite pieces
  are not automatically the collision shape.
- Specify overlap versus contact, touching while moving away, grazing corners,
  starting inside a wall, nearest-hit ties and what happens when a work limit is
  reached. Do not hide these choices behind a generic Boolean.
- Choose endpoint overlap for slow or intentionally discrete interactions;
  use swept queries when a body can cross an obstacle between ticks. A ray is
  a finite zero-width segment, not a substitute for sweeping a thick body.
- For moving targets, sweep relative motion from both bodies' **old** positions.
  Detecting that contact does not provide pushing, platform carrying or an
  impulse solver. Sliding in the example is against static boxes only.

## Keep the work and arithmetic bounded

Read [query contracts](references/queries.md) for slab tests, exact hit ordering,
fixed-point range and API examples. Do not reinterpret Q4 units as SGDK `fix32`.
Read [sliding and candidate selection](references/sliding.md) for static response,
initial overlap policy, tile candidates and limits. Never silently drop solids
when a candidate buffer fills; stop or use a documented conservative fallback.

Use the project's existing collision model where practical. Keep slopes,
one-way platforms and gameplay-specific interaction rules separate; this skill
does not replace those with a full rigid-body framework. Collision layers or
category masks should filter candidates before narrow tests, according to the
game's actual rules, not SGDK palette or sprite priority flags.

## Integrate and prove it

- Verify types, rendering calls and resource syntax in the selected toolchain;
  pull `ewrogers/sgdk:latest` before validation. Read
  [SGDK integration and sources](references/sgdk-integration.md).
- Test zero/negative motion, thin walls, moving targets, grazing, equal-time
  corners, initial overlap, nearest hit, finite endpoints and range rejection.
  Use an independent oracle or hand-computed cases; optimized versus debug
  agreement alone can preserve the same bug.
- Record candidate/narrow-test counts separately from CPU/frame timing. Keep
  response iteration and collision data lifetimes explicit. Do not grow the
  example's arithmetic limits or candidate arrays without checking the cost.
- Check release builds and target arithmetic, then emulator/hardware movement
  and visuals. PAL/NTSC scheduler tests do not prove VBlank performance.

[Collision Lab](assets/collision-lab/README.md) is a standalone executable example
with endpoint/swept shots, movable aiming rays and wall sliding. Its art and
controls demonstrate the algorithms; they do not prescribe another game's style.

For deciding whether a valid contact causes damage, is blocked or triggers a
reaction, use sgdk-combat when available. Those policies do not change the
geometric meaning of this skill’s query results.
