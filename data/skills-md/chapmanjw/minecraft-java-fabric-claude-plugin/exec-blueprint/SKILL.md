---
name: exec-blueprint
description: >-
  Turns a Minecraft build plan into named, reusable structure definitions saved
  inside the world, so build elements can be placed, copied, and iterated later
  without any external state. Use after planning, to create or update the
  structure library for a build. Part of the minecraft-builder workflow.
model: sonnet
effort: medium
context: fork
agent: general-purpose
---

# exec-blueprint (Blueprinter)

You create the **reusable structure library** for a build. A blueprint is a
named Minecraft structure file living in the world — once defined, it can be
stamped anywhere, copied, and re-saved. This is what lets a build be iterated
later with no memory outside the world.

## Connection

If a tool call fails because the MCP server is unreachable, stop and tell
the user to run the `minecraft-mcp-setup` agent.

## Inputs

- `.minecraft-builder/<project>/plan.toon` — its `blueprints` list names every
  reusable element you must define.
- `research.toon` — dimensions and materials, if a real reference is involved.
- The `mcbuilder:registry` from command storage (`data_storage_get`, namespace
  `mcbuilder`, path `registry`) — to see what structures already exist and
  whether you are creating or revising one.

## Naming

Name every structure **`mcb:<project>_<element>`** — lowercase, consistent,
project-scoped, with the **colon namespace**. This is the canonical form
across the whole plugin: in `plan.toon`, in `mcbuilder:registry`, and in
every `structure_*` call.

Always use the `mcb:` namespace. A bare, colon-less name is not rejected —
it is silently filed under `minecraft:` (e.g. `mcb_demo` becomes
`minecraft:mcb_demo`), where it clutters the hundreds of vanilla templates,
risks colliding with them, and is hard to find in `structure_list`. The `mcb:`
namespace keeps the build's templates isolated and listable. Treat the colon
as required, and keep the form identical in `plan.toon` and the registry so a
later session can find every structure by name.

## Create each blueprint

For every element in the plan's `blueprints` list:

1. **Decide the method:**
   - **Scratch-and-capture** (default) — build the element in-world in a clear
     staging area using `block_fill_region` and `block_set_state`, then capture
     it with `structure_save_from_world` over its exact bounds. Clear the
     staging area afterward. This is the simplest path for any element easier
     to construct directly than to generate.
   - **Capture from final spot** — if the element is being built at its final
     position anyway, capture with `structure_save_from_world` immediately after
     the `exec-worker` leaf finishes placing it.
   - **Direct NBT write** — for computed grids (pixel-art murals, voxelized
     models, anything image-mapped or parametric), generate a structure `.nbt`
     and write it with `structure_file_write` (content is base64). Heavier —
     only use when a script already produces NBT. See
     `${CLAUDE_PLUGIN_ROOT}/skills/exec-blueprint/reference/generated-structures.md`.
2. Build it from the plan's exact materials and dimensions.
3. Save it under the `mcb:<project>_<element>` name. Java structure templates
   are saved as `.nbt` files under `<world>/generated/<namespace>/structures/`.
4. Verify with `structure_get_info` / `structure_list` that it saved with the
   expected size.

If you build prototypes in a staging area, clean them up afterward so the only
trace is the saved structure file.

## Iteration

To revise an existing blueprint: `structure_load_to_world` it into a staging
area, edit the blocks, capture it again under the **same name** with
`structure_save_from_world` (bumping its revision in the registry). Because the
structure lives in the world, anyone in a later session can do this — no
project files needed.

### Java-exclusive: structure placement options

When stamping with `structure_load_to_world` (for iteration or for the
`exec-worker` leaf's `place-structure` op), use the exact enum strings:

- **`rotation`** ∈ {`none`, `clockwise_90`, `180`, `counterclockwise_90`} — never bare numbers or "90 degrees".
- **`mirror`** ∈ {`none`, `front_back`, `left_right`}.
- **`integrity`** — float 0..1; `1.0` places every block intact; values below 1 randomly omit blocks, giving weathered or scattered/ruined placement. Useful for pre-aged ruins and naturalistic scattering.
- **`include_entities`** — boolean; `true` captures/places any entities (armor stands, item frames, paintings, villagers) stored in the structure. Set `false` when stamping structural geometry only.

## Register — report it, do not write it

The **orchestrator owns the `mcbuilder:registry`** and is its sole writer. Do
**not** call `data_storage_set` on the registry yourself — parallel sub-agents
writing the shared document clobber each other's entries. Instead, **report to
the orchestrator** the row it should record for each blueprint, in the registry
form (TOON — see <https://toonformat.dev/>):

```toon
builds[1]{project,element,structure,x,y,z,status,revision}:
  lakeside-village,table-set,mcb:lakeside-village_table-set,0,0,0,blueprint,1
```

Use `status: blueprint` for a defined-but-not-yet-placed structure; the
orchestrator updates it to `built` with real coordinates once the `exec-worker`
leaf stamps it. Reading the registry with `data_storage_get` for context is fine;
writing it is not your job.

**Confirm persistence before handing off.** A blueprint phase that "ran" but
left no `.nbt` on disk is a silent failure — a later consumer can't find the
template and substitutes ad-hoc geometry, breaking cohesion (this happened on a
large build). After saving, re-list with `structure_list` and verify each
`mcb:<project>_<element>` you created actually appears with the expected size.
Report the **verified** list of persisted templates so the orchestrator and
every consumer can rely on it; flag any that did not persist rather than
assuming they did.

## Return to the orchestrator

Return the structure names you created or revised and their sizes to the
orchestrator. The plan is now ready for the build phase — every `place-structure`
step in `plan.toon` (which maps to `structure_load_to_world`) references a
structure you have now defined. The orchestrator sequences the next leaf
(`exec-worker`) to stamp them; you do not invoke it yourself.
