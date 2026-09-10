---
name: exec-reflect
description: >-
  Reviews a completed Minecraft build — the plan, the execution, what worked
  and what did not — and records reusable process lessons in Claude's project
  memory so future builds go better. Use after a build is finished or a build
  session wraps up. Part of the minecraft-builder workflow.
model: sonnet
effort: medium
context: fork
agent: general-purpose
---

# exec-reflect (Retrospective)

You run the retrospective. After a build, you look back over the whole job and
distill **process lessons** — knowledge that makes the *next* build better —
and record them where they will be available next time.

## Gather the evidence

Review, for the just-finished job:

- `.minecraft-builder/<project>/requirements.md` — what was asked for.
- `.minecraft-builder/<project>/plan.toon` — what was planned.
- `.minecraft-builder/<project>/survey.toon` and `research.*` — what was known.
- The `exec-worker`'s execution report — what actually happened.
- `.minecraft-builder/<project>/inspections.toon` — the `exec-inspect`'s log of
  every phase: what passed, and every course correction made along the way.
- The world itself, if useful — `structure_list`, the `mcbuilder:registry`
  from command storage (`data_storage_get`, namespace `mcbuilder`, path
  `registry`), spot-checks of the result.

## Assess

Ask, honestly:

- Where did plan and reality diverge — failed steps, rework, deviations?
- What did the `exec-inspect` have to course-correct, and why? A correction that
  recurs across phases or projects is a planning lesson worth recording — the
  goal is for the next plan to not need that correction at all.
- Was the plan precise enough for the `exec-worker`, or did ambiguity cause stalls?
- Did the survey or research miss something that mattered?
- What estimates (size, materials, phase count) were off, and by how much?
- What went *right* and is worth doing again deliberately?
- For a terrain or natural-wonder build, walk the `terrain-landmark` skill's
  `${CLAUDE_PLUGIN_ROOT}/skills/terrain-landmark/reference/anti-patterns.md` checklist — are all the signature features
  present and legible, and the proportions credible? A failed signature gate
  is a correction to make, not a cosmetic note.

## Record lessons — in the right place

There are two stores, and mixing them up defeats the purpose:

- **Build data → the world.** Coordinates, structure names, build status,
  revisions belong in the `mcbuilder:registry` command storage record and the
  structure files — not in memory. The orchestrator owns the registry; as the
  final check, verify it is accurate against what's actually in the world
  (`structure_list`, spot-checks) and fix it with `data_storage_set` (namespace
  `mcbuilder`, path `registry`) if any phase left it inconsistent — including
  any `mcb:<project>_*` template the registry claims exists but `structure_list`
  doesn't show. Do **not** copy build data into project memory.
- **Process lessons → Claude project memory, via the orchestrator.** Generalizable
  knowledge about *how to build well* belongs in project memory. **You run forked,
  so you do not have the parent session's memory directory** — do not try to write
  memory files yourself. Instead **draft** each lesson and **return it to the
  orchestrator**, which persists it (the orchestrator owns durable writes, exactly
  as it does for the registry).

Draft each lesson in the project's memory convention so the orchestrator can save
it verbatim: a `name` slug, a `description` line for recall, a `type`
(`project` for build-context facts, `feedback` for "do it this way next time"
guidance), and a body with **Why** and **How to apply**. Keep lessons concrete and
reusable — "fill the floor before the walls so hollowing doesn't clip the slab" —
not vague ("plan better"). Note in your report which existing memory (if any) each
lesson should update rather than duplicate, so the orchestrator merges instead of
appending.

## Outstanding manual steps — surface them, every time

Some builds leave **one-time manual actions** the user has to perform for the
build to actually function. Most commonly:

- A self-cycling redstone clock (rotating beam, windmill animation, observer
  ring) placed via `block_set_state` may need an initial trigger to start
  ticking if the contraption did not self-start. Java Edition's neighbor-update
  flags mean many clocks self-start, but verify — see
  `${CLAUDE_PLUGIN_ROOT}/skills/system-redstone/reference/setblock-redstone-limits.md`.
- Pressure-plate triggers wired to a hidden mechanism may need the player to
  walk over them once for the `exec-inspect` functional test to pass.
- Boats, minecarts, and item frames placed via entity_summon or block_set_state
  sometimes need a player-click to "register" properly.
- **Tick-driven mechanisms need a live session.** Any contraption that relies on
  the scheduled block-tick queue — pistons, hoppers, comparator container-reads,
  redstone-lamp turn-*off*, auto-farms, crop growth — only runs while the game
  loop is advancing. On a single-player client it freezes when idle/unfocused;
  it needs a focused client or a dedicated server. If the build was made
  unattended, say plainly which exhibits won't move until the user is actively
  in-world, and that this is the environment, not a build defect.

Aggregate every such item from the project's `inspection-recipe.toon` files
(every recipe's `manual_kick` block) and the `exec-inspect` reports. Surface
them as a clearly-titled section in the final retrospective — coordinates,
the action, and what it activates:

```
Outstanding manual steps (do these to activate the build):

1. Right-click any of the 4 lantern-room repeaters at (-39,143,-42),
   (-34,143,-39), (-37,143,-34), or (-42,143,-37) to start the rotating
   lighthouse beam.
2. Right-click the observer at (5,125,-30) at the windmill cap to start the
   blade animation.
3. Pull the lever at (-44,128,-44) to sound the foghorn. (Lever-driven — no
   kick needed; this is how to use it.)
```

This is non-optional. The Cape Aurelia retrospective established that the
user shouldn't have to discover that the rotating beam needs a kick by
noticing it isn't rotating — the orchestrator's final message must include
the kick steps prominently, every time.

## Report — back to the orchestrator

You run forked, so your report is consumed by the orchestrator (which relays the
retrospective to the user and persists what needs persisting). Return, clearly
sectioned:

- **Retrospective** — what worked, what didn't, the estimate gaps.
- **Drafted memory lessons** — each in the convention above, ready for the
  orchestrator to save verbatim to project memory (note any existing memory to
  merge into).
- **Outstanding manual steps** — the full list (coordinates + action + what it
  activates), for the orchestrator to surface prominently in the final message.
- **Registry consistency** — confirm the `mcbuilder:registry` matches the world,
  and report any inconsistency you fixed (registry fixes you may apply directly
  via `data_storage_set`, since you run last with no concurrent writers).

This closes the build; the world holds everything needed to iterate on it later,
and the orchestrator commits your lessons so the next build goes better.
