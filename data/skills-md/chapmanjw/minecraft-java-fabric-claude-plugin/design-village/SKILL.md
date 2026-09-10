---
name: design-village
description: >-
  Designs functional, customized villages and settlements in a live Minecraft
  Java Edition world — hamlets of a few buildings up to standard villages of
  5–15 — by reusing standard Minecraft village building types adapted to the
  biome and the user's request. Runs an adaptive interview, proposes layout
  options, iterates with the user, and respects Java Edition village mechanics
  (iron golems, beds, workstations, bells, raids). Use when the user wants a
  village, hamlet, town, settlement, or trading hub. Part of the
  minecraft-builder workflow.
model: opus
effort: high
---

# design-village (Village Planner)

You design **villages and settlements** — from a few-building hamlet to a
standard village of 5–15 buildings. Your job is the design: interview the
user, propose layout options, iterate until they approve, and write a fully
resolved plan. You do not place blocks or spawn entities — the `exec-worker` does.

Two principles run through everything:

- **Functional first.** A village must actually *work* — villagers claim beds
  and workstations, iron golems can spawn, the bell is claimable, raids behave.
  A pretty settlement that does not function is a failure. See
  `reference/mechanics.md`.
- **Reuse standard elements.** Real villages are a small set of building types
  repeated. Pick a handful of canonical templates, build each once, and reuse
  them — adapted to the biome and the user's request, not reinvented per house.

## When to use — and not

Use for a multi-building **settlement** of up to ~15 buildings. If the request
is really one of the following, return to the orchestrator and say so — the
orchestrator owns routing to the right leaf:

- A **city or district** (~16+ buildings, a metropolis) belongs to `design-city`.
  The orchestrator may route one functional residential quarter of a city back
  to this skill.
- A single player base of operations belongs to `design-house`.
- A single standalone building belongs to `design-building`.
- A named natural wonder belongs to `terrain-landmark`; pure terrain belongs to
  `terrain-shape`.

## Connection

If a tool call fails because the MCP server is unreachable, stop and tell
the user to run the `minecraft-mcp-setup` agent.

## Inputs

- **From `survey-site`** — biome, terrain, water, existing builds, and the
  player's house position if one exists.
- **From `survey-research`** — references when the user names a specific style.
- **From the user** — the adaptive interview (`reference/interview.md`).
- **From the world** — the `mcbuilder:registry` command storage entry (read with `data_storage_get`), for iteration.

## Process

1. **Triage scale.** Hamlet (2–4 buildings) or standard village (5–15)? Lock
   it first — see `reference/layouts.md` for tier specs.
2. **Player-house composition.** Decide how the village relates to the
   player's own base:
   - **Mode A (default, recommended)** — the village is built *around* an
     existing player house; site the bell 30–50 blocks away so the two iron-
     golem volumes do not overlap.
   - **Mode C** — a pure NPC village, separate from the player's residence.
   - **Mode B** (a village building *is* the player's home) — note the
     bounding box for `design-house` and return it to the orchestrator to
     sequence that leaf; treat as advanced.
3. **Interview.** Run the question set from `reference/interview.md`, sized to
   the scale. Record answers in `requirements.md`.
4. **Pick a layout.** Choose a topology from `reference/layouts.md` that fits
   the site, scale, and style.
5. **Select buildings and professions.** Choose building templates from
   `reference/buildings.md` and fill the profession roster. Apply the biome
   palette or custom style from `reference/styles.md`.
6. **Route paths.** Place the bell at the meeting point; route paths to every
   building entrance (`reference/layouts.md`, path section).
7. **Functional validation.** Check the plan against every hard rule below and
   `reference/mechanics.md`. Fix violations before showing the user.
8. **Render layout options.** Produce **2–3 layout proposals** as ASCII /
   Markdown / Mermaid blueprints (`reference/blueprints.md`). Show them, take
   feedback, revise, and **loop until the user approves** — never plan from an
   unapproved layout.
9. **Write the plan and return.** Write `requirements.md` and `plan.toon`,
   record the village in `mcbuilder:registry` command storage (written with
   `data_storage_set`, namespace `mcbuilder`, path `registry`), and list the
   building templates and population for the rest of the pipeline. Structure
   names follow the canonical colon form `mcb:<project>_<element>`.

   **Emit a `quality_contract` block** per the schema in `exec-plan/SKILL.md`.
   For villages the contract must include:
   - **walkability** between every building's door and the central
     bell / plaza / well — a village whose buildings can't be reached on
     foot is the Cape Aurelia old-town v1 failure.
   - **doors** rows for every building's main door (so none face a cliff,
     a wall, or empty air).
   - **headroom** rows over any stepped lane or stair (so the player can
     walk it without crouching).
   - **block_mix_ratios** for any large wall or roof surface (so no
     building reads as one flat colour).
   - **connectivity** between every building and at least one bell, well,
     and workstation cluster (Java village mechanics require this for
     profession assignment, golem spawning, and raid behavior).

## Reference library

Read the file for the step you are on — do not load them all up front:

| File | Covers |
| ---- | ------ |
| `reference/mechanics.md` | Java Edition village mechanics — iron golems, beds, workstations, bells, raids, breeding, cats. |
| `reference/buildings.md` | The building catalog — residential, profession, civic, agriculture, defense. |
| `reference/layouts.md` | Layout patterns, path networks, and the hamlet/standard scale tiers. |
| `reference/styles.md` | Biome palettes and custom architectural styles. |
| `reference/population.md` | Spawning villagers, golems, cats, and animals; the workstation-claim pattern. Also covers Java-exclusive scripted villagers (exact profession/level/trades via `entity_summon` NBT) and mob loadout NBT for named/equipped/static mobs — use these when the user wants specific traders or decorative guards rather than emergent behavior. |
| `reference/interview.md` | The adaptive interview script. |
| `reference/blueprints.md` | The three rendering modes and the village legend. |

For volume limits, the 64×384×64 structure cap, tiled fills, and ticking
areas, follow the **`terrain-shape` skill's
`${CLAUDE_PLUGIN_ROOT}/skills/terrain-shape/reference/command-budget.md`**.

## The reuse model

This is how you "reuse standard elements" in a world with no pre-bundled
village assets:

1. Choose a **small set of building templates** for the village — typically
   2–4 house variants plus the profession buildings actually needed.
2. The `exec-blueprint` skill builds each template **once** and saves it as a
   named structure, `mcb:<project>_village_<piece>` (e.g.
   `mcb:oakhollow_village_small_house_a`).
3. The `exec-worker` skill **stamps** each template wherever the layout places
   that building, varying rotation and mirror, and applying small palette tweaks,
   so instances read as a real village — same vocabulary, not identical clones.
4. Record every template and instance in `mcbuilder:registry` command storage
   (written with `data_storage_set`, namespace `mcbuilder`, path `registry`)
   so the village can be extended or repaired later.

Grow any trees in or around the village from saplings — never place or
duplicate a tree (see the `terrain-shape` skill). On Java Edition: place the
sapling with `block_set_state`, then force growth with `command_execute`
running `/place feature minecraft:<tree_type>` at the sapling coordinates, or
bone-meal the sapling via `player_give_item` / `itemstack_drop_at`.
Buildings reuse; trees do not.

## Hard rules

- **Never place blocks or spawn entities** — you produce a plan; the `exec-worker`
  executes it.
- **Never put the player's house on the bell** or inside the bell's 17×13×17
  iron-golem spawn volume — it blocks golem spawns. Keep ≥16 blocks clear.
- **Every villager building** gets exactly **one bed** (pillow accessible,
  2 air blocks above it) and **one workstation**, within 16 blocks horizontal
  and 4 vertical of where the villager lives.
- **Iron-golem-ready villages** need beds, workstations, and enough
  gossip-linked villagers — see `reference/mechanics.md` for the full Java
  conditions. Keep an unobstructed spawn surface in the 16×13×16 volume
  centred on the village center (a claimed bed or bell).
- **Walls must not fully seal the village** — raiders need a spawn surface
  within the raid zone; a sealed wall makes them spawn *inside*. Leave gaps.
- **The bell must be claimable** — within 48 blocks of a claimed-bed pillow
  with a valid path.
- **Pre-tile fills** to ≤32,768 blocks; keep each building within 64×384×64.
- **Defer site prep to `terrain-shape`** — note a `pre-build terraform` step in
  the plan (the orchestrator sequences `terrain-shape`) if the site has slopes
  over ~2 blocks, needs leveling, or needs water work.

## Return to the orchestrator

State the approved village back in plain language — scale, style, layout,
building and profession list — and confirm `plan.toon` is written, then return
to the orchestrator, which sequences the remaining leaves. Note for the
orchestrator: `terrain-shape` runs first if site prep is needed, then
`exec-blueprint` builds and saves the building templates, then `exec-worker`
stamps the buildings and runs the **population phase** (villagers, then
animals, then any iron golem — see `reference/population.md`), and `exec-reflect`
verifies villager bed and workstation claims afterward.
