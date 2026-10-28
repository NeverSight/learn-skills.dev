---
name: minecraft-mod-porting
description: Port Forge-based Minecraft mods across major version jumps, especially legacy-to-modern ports such as 1.7.10 to 1.16.5. Use when updating old mods to newer Minecraft or Forge versions, migrating registries and events, fixing rendering or asset breakage, rebuilding entities or custom mobs, modernizing Gradle or mappings, or preserving gameplay behavior while porting code, textures, models, data, and networking.
---

# Minecraft Mod Porting

## Overview

Port old Forge mods to newer Minecraft versions without stopping at "it compiles." Inspect the mod first, classify the breakage by subsystem, port the code and assets deliberately, and verify that gameplay, visuals, entity behavior, and save data still match the original intent.

## Workflow

1. Inspect the source mod before choosing an approach.
   - Identify the source Minecraft version, target version, source Forge setup, target loader assumptions, Java level, mappings, and major dependencies.
   - Find the high-risk subsystems early: blocks and items, registries, GUIs, networking, worldgen, capabilities or save data, rendering, assets, entities, and custom AI.
   - Check whether the mod is small enough for a direct jump or whether it should be staged through one or more intermediate versions.
2. Decide whether this is a mechanical port, a partial rewrite, or a redesign.
   - Keep the old architecture only when the original concepts still map cleanly to modern Forge patterns.
   - Prefer rewrites for subsystems built around removed APIs, heavy reflection, base-class overrides that no longer exist, obsolete rendering hooks, or brittle global state.
   - Split the work into two passes when useful:
     - Mechanical port: restore compilation, loading, registration, and basic runtime behavior.
     - Feature parity cleanup: restore visuals, AI, balancing, persistence, networking, and edge-case behavior.
3. Port subsystem-by-subsystem instead of renaming symbols blindly.
   - Start with build files, mappings, and dependencies so the project can compile against the target environment.
   - Move next to registries and lifecycle, then data and networking, then rendering and assets, then entities and gameplay logic.
   - Treat each subsystem as a behavior migration, not a search-and-replace exercise.
4. Verify version-sensitive details from primary sources.
   - Do not trust memory for exact API names, event class names, registry helpers, mappings, or Gradle syntax on modern Forge.
   - Use current official or primary project docs for the target version and any major dependency involved.
5. Validate against three definitions of done.
   - Builds: the project compiles and packages for the target environment.
   - Runs: the mod loads, registers content, and basic features work in-game without startup or runtime crashes.
   - Faithfully behaves like the original: textures line up, models render correctly, entities move and attack correctly, data persists, networking syncs, and the player-facing behavior still matches the source mod.

## Decision Rules

- Prefer a direct port only when the old mod is structurally close to modern Forge concepts.
- Prefer a staged jump or selective rewrite when the port crosses multiple ecosystem shifts at once, especially from pre-registry, pre-data-driven, or pre-modern-rendering eras.
- Preserve player-visible behavior first. Internal architecture may change as long as features, balance, visuals, and persistence remain correct.
- Avoid dragging obsolete APIs forward through compatibility hacks if modern Forge offers a cleaner supported pattern.
- Treat textures, models, lang keys, sounds, particles, hitboxes, AI goals, and data sync as first-class porting work, not post-port polish.

## Reference Map

- Read [references/version-jump-strategy.md](references/version-jump-strategy.md) to choose between direct, staged, or rewrite-heavy port strategies.
- Read [references/forge-porting-surfaces.md](references/forge-porting-surfaces.md) for registries, lifecycle, configs, networking, data, recipes, tags, and persistence concerns.
- Read [references/rendering-and-assets.md](references/rendering-and-assets.md) for models, textures, resource locations, language files, sounds, particles, and rendering migration.
- Read [references/entities-and-ai.md](references/entities-and-ai.md) for custom mobs, entity registration, attributes, goals, spawning, synced data, and renderer pitfalls.
- Read [references/build-and-mappings.md](references/build-and-mappings.md) for ForgeGradle, Java level, mappings, dependency modernization, and build hygiene.

## Output Expectations

- Report the source version, target version, loader assumptions, and the main break surfaces before editing code.
- Explain whether the chosen approach is a direct port, staged port, or subsystem rewrite and why.
- Preserve feature parity where practical, and call out any intentional behavior change explicitly.
- When exact target-version APIs are uncertain, verify them from primary docs instead of guessing.
- When finishing a port, summarize what now builds, what now runs, and what still needs gameplay-parity validation.

## Typical Prompts

- `Use $minecraft-mod-porting to port this 1.7.10 Forge mod to 1.16.5 and keep its custom mobs, textures, and drops working.`
- `Use $minecraft-mod-porting to update this old Forge tech mod to a modern version and tell me what should be rewritten instead of mechanically ported.`
- `Use $minecraft-mod-porting to fix rendering, models, and language asset breakage after moving this mod to newer Forge.`
