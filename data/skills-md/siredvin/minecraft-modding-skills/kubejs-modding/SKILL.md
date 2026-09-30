---
name: kubejs-modding
description: Write version-aware KubeJS pack scripts.
license: MIT
metadata:
  author: "SirEdvin"
  version: "1.1.0"
---

# KubeJS Modding

Use this skill to implement or review KubeJS scripts for Minecraft modpacks. Prefer the installed KubeJS, Minecraft, loader, and addon versions in the pack over generic examples. KubeJS APIs are version-sensitive; verify syntax against the local generated ProbeJS typings or the matching official wiki page before making broad changes.

## First Checks

- Confirm Minecraft version, loader, KubeJS version, Rhino version, and relevant KubeJS addons from the instance `mods` list, manifest, `config`, or logs.
- Confirm the script root is the instance-level `kubejs/` directory, not a Java mod source tree.
- Inspect existing `kubejs/startup_scripts`, `kubejs/server_scripts`, `kubejs/client_scripts`, `kubejs/assets`, `kubejs/data`, and `kubejs/config` conventions before adding files.
- Prefer project-local helpers and naming patterns over standalone snippets.
- Check whether ProbeJS output exists; use it as the most reliable API reference for the exact pack.
- Do not assume Forge, NeoForge, or Fabric Java mod APIs are directly available. KubeJS scripts run through the KubeJS/Rhino scripting environment and KubeJS event APIs.

## Script Types

- Use `startup_scripts` for startup-time work: custom item/block/fluid/entity registration, registry modification, custom recipe schemas, and other actions that require a game restart.
- Use `server_scripts` for datapack/server logic: recipes, tags, loot, commands, server events, player events, world events, and most gameplay pack logic. These usually reload with `/reload`.
- Use `client_scripts` for client-only behavior: JEI/REI/EMI integration scripts, tooltips, client events, colors, UI tweaks, and resource-pack-side behavior. These reload with client resource reloads such as F3+T when supported.
- Put generated or hand-written resources under `kubejs/assets/<namespace>` and `kubejs/data/<namespace>` when raw JSON/assets are clearer than JS.
- Keep common reusable JS helpers in a clearly named file and load order that matches the pack's existing convention.

## Reload And Validation

- Use `/reload` for server scripts and data/resource changes that participate in datapack reload.
- Restart the game/server after changing startup scripts or registries. Registry changes cannot be safely hot-reloaded.
- In the reviewed KubeJS 2001 source, script reload clears that script type’s event handlers and loads scripts again; listeners can be replaced. However `/kubejs reload server_scripts` does not itself reload recipes/tags/loot: use `/reload`. Registry startup changes still require a full restart. See the pinned lifecycle reference below.
- Use `/kubejs errors server` (or `startup` / `client`) on KubeJS 2001, or the matching version’s error command for script errors when available.
- Check `logs/kubejs/server.log`, `logs/kubejs/client.log`, normal latest logs, and crash reports after changes.
- Use ProbeJS to generate typings and inspect available globals, events, classes, and addon APIs for the current pack.
- Validate recipes and tags in-game with JEI/REI/EMI and logs, not just by checking that scripts parse.

## Events

- Register handlers with `ServerEvents`, `StartupEvents`, `ClientEvents`, `ItemEvents`, `BlockEvents`, `EntityEvents`, `PlayerEvents`, and addon event groups that exist in the installed version.
- Choose event groups by lifecycle:
  - `StartupEvents.registry(...)` for adding registry entries.
  - `ServerEvents.recipes(...)` for adding/removing/replacing recipes.
  - `ServerEvents.tags(...)` for tag edits.
  - `ServerEvents.loaded`, tick, command, player, or entity events for runtime behavior.
  - `ClientEvents.*` for client-only scripts.
- Keep event code small. Move repeated IDs, ingredient sets, and helper functions to shared constants.
- Do not mutate registries in server scripts. Use startup scripts and restart.
- Be explicit about namespaces. Prefer full IDs like `minecraft:iron_ingot` and `modid:item_name`.

## Recipes

- Use `ServerEvents.recipes(event => { ... })` for recipe changes.
- Prefer targeted recipe removal by `id`, `output`, `input`, `type`, or `mod` over broad removals that may break unrelated progression.
- Add shaped, shapeless, smelting, blasting, smoking, campfire, stonecutting, smithing, and custom JSON recipes with the API style supported by the installed KubeJS version.
- For modded machines, prefer addon-provided helpers or custom recipe JSON matching the target mod's schema.
- Assign stable recipe IDs when replacing important recipes so datapack conflicts are easy to diagnose.
- Use tags for interchangeable inputs instead of enumerating every item when the pack has a stable tag convention.
- Test removed and added recipes in JEI/REI/EMI and by crafting/smelting when the recipe affects progression.

KubeJS 6 / Minecraft 1.20.1 Forge recipe example (the `forge` item tag must exist):

```js
ServerEvents.recipes(event => {
  event.remove({ id: 'minecraft:iron_pickaxe' })

  event.shaped('minecraft:iron_pickaxe', [
    'III',
    ' S ',
    ' S '
  ], {
    I: '#forge:ingots/iron',
    S: 'minecraft:stick'
  }).id('kubejs:iron_pickaxe_from_tagged_iron')
})
```

## Registries

- Register new content in `startup_scripts`, usually through `StartupEvents.registry('<registry>', event => { ... })`.
- Register items, blocks, fluids, creative tabs, and other supported registry entries only if the installed KubeJS version supports that registry.
- Keep registry IDs lowercase snake_case and namespaced under `kubejs` or the pack's chosen namespace.
- Restart after registry changes and check startup logs for duplicate IDs or invalid builder properties.
- Add models, textures, blockstates, lang, loot, tags, and recipes for custom entries under `kubejs/assets` and `kubejs/data` or through scripts/datagen-style helpers.

KubeJS 6 / Minecraft 1.20.1 startup item example:

```js
StartupEvents.registry('item', event => {
  event.create('compressed_copper_ingot')
    .displayName('Compressed Copper Ingot')
})
```

## Tags, Loot, And Data

- Use `ServerEvents.tags(...)` for tag edits when script-driven tags are clearer than raw JSON.
- Prefer conventional cross-mod tag namespaces used by the pack, such as `c`, `forge`, or loader-specific conventions, based on the installed ecosystem.
- Use raw JSON in `kubejs/data/<namespace>` for complex loot tables, advancements, predicates, worldgen, or mod-specific data when JS wrappers would obscure the schema.
- Keep generated JSON deterministic and organized by namespace/path.
- Check data pack load errors after edits; a single invalid JSON file can invalidate a larger reload.
- Tags are registry-specific: a block tag does not automatically make the corresponding block item a valid item-tag recipe ingredient. Tags also cannot distinguish NBT/data-component variants.

## Client Integration

- Put client-only scripts in `client_scripts`.
- Use client scripts for tooltips, JEI/REI/EMI category hiding, item hiding, color handlers, keybind/client events, or UI tweaks supported by the installed addons.
- Never place client-only classes or APIs in server scripts.
- Confirm the target integration addon is installed before using its event group.
- Test client changes with a resource reload and by opening the affected UI.

## Java Interop

- Prefer KubeJS wrappers and event APIs before using Java interop. On the reviewed 2001 line use `Java.loadClass`; `Java.type` is not present in its Java wrapper.
- When Java interop is needed, load classes lazily inside the script or handler that uses them.
- Avoid client-only Java classes in server scripts and common startup code.
- Treat Java objects as version-specific. Check ProbeJS typings, generated docs, or decompiled sources before calling methods.
- Avoid reflection and internal Minecraft classes unless the pack requires it and the failure mode is understood.

## Organization

- Split scripts by domain: `recipes/`, `tags/`, `loot/`, `registries/`, `integrations/`, or the pack's established folders.
- Keep high-risk progression edits close together and comment intent briefly when a recipe removal or replacement is non-obvious.
- Use constants for repeated mod ids, tag ids, ingredient arrays, and machine recipe helpers.
- Keep script IDs and recipe IDs stable across updates to avoid datapack churn.
- Avoid giant catch-all files that make reload errors hard to isolate.

## Addons And Integrations

- Check installed addons before writing integration scripts: common examples include ProbeJS, JEI/REI/EMI integrations, Create, Thermal, Mekanism, FTB Quests, and Almost Unified.
- Prefer addon-specific KubeJS APIs over raw JSON when they provide validation and readable helpers.
- For unsupported modded recipes, inspect the mod's generated recipe JSON or existing datapack examples and use `event.custom(...)`.
- For addon/plugin development in Java, use the KubeJS source README and plugin APIs; do not confuse addon development with pack-level scripts.

## Porting Notes

- KubeJS is pack scripting, not a compiled Fabric/Forge/NeoForge mod. There is no `@Mod`, `ModInitializer`, or Gradle build for normal scripts.
- Loader differences matter for tag namespaces, available mods, and event/addon APIs. Confirm whether the pack runs Forge, NeoForge, or Fabric.
- KubeJS major versions changed APIs substantially. Do not copy scripts between 1.16, 1.18, 1.19, 1.20, and 1.21 packs without checking syntax.
- JavaScript runtime behavior is Rhino-based, not Node.js. Do not use Node-only APIs, npm packages, filesystem APIs, or browser globals unless the pack provides them.
- Recipes and tags are often safer to port conceptually than line-by-line.

## Validation Checklist

- Run or reload the instance with the relevant lifecycle: restart for startup scripts, `/reload` for server scripts, resource reload for client scripts.
- Check KubeJS logs and the normal Minecraft log for parse errors, missing methods, invalid IDs, datapack errors, and recipe conflicts.
- Verify recipe changes in JEI/REI/EMI and by performing the action in-game when progression matters.
- Verify custom registry entries have display names, models/textures, recipes, loot, and tags as needed.
- Run a dedicated server or server launch path for scripts that should work server-side.
- Regenerate ProbeJS typings after changing installed mods, KubeJS versions, or major script APIs.

## Official References

- KubeJS wiki: `https://kubejs.com/`
- KubeJS source: `https://github.com/KubeJS-Mods/KubeJS`
- ProbeJS: `https://github.com/Prunoideae/ProbeJS`
- Rhino: `https://github.com/KubeJS-Mods/Rhino`
- KubeJS Maven/releases: `https://maven.latvian.dev/#/releases/dev/latvian/mods`

## Versioned source checks

Read [lifecycle and schema boundaries](references/versioned-lifecycle.md) before porting scripts or developing a compiled plugin.
