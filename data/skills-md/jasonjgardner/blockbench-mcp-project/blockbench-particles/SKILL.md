---
name: blockbench-particles
description: Add particle effects (smoke, fire, sparks, magic, glow, dust, snow, drips, bubbles, bursts) to Blockbench models with MCP tools. Covers Bedrock/Snowstorm particle JSON, presets and design knobs, locators, particle keyframes on animations, Blockbench's Animate-mode preview, and delivery to Bedrock resource packs (client entity particle_effects) and GeckoLib, plus fallbacks for glTF, Java block and Hytale targets that cannot carry particles. Use when a model needs an emitter, VFX, particle effect, locator, Snowstorm file, particle_effects keyframe, or effect polish in a deliverable.
---

# Blockbench Particles

Blockbench has one particle system: **Bedrock particle effects**, the JSON format Snowstorm edits. Blockbench previews them with Wintersky when a **particle keyframe** on an animation's Effects track fires, optionally at a **locator** on a bone. The same files run in Minecraft Bedrock, and GeckoLib animations carry the same keyframes to a mod's particle handler. Nothing else in Blockbench (glTF, OBJ, Java block models, Hytale) exports particles.

Load [blockbench-use](../blockbench-use/SKILL.md) first. Particles ride on animations, so load [blockbench-animation](../blockbench-animation/SKILL.md) when the model has no clip yet.

## 1. Decide What Carries the Effect

Ask for the destination if it is unknown; it decides everything below.

| Destination | Particles | Where the effect lives |
|---|---|---|
| Bedrock entity or attachable (`bedrock`) | Native | Particle JSON + locators in geometry + keyframes in animation JSON or controller states + `particle_effects` map in the client entity. See [delivery](references/delivery.md). |
| GeckoLib (`geckolib_model`) | Keyframes only | Keyframes (effect, locator, script) export in the animation JSON; the mod's particle keyframe handler spawns real particles. Bedrock JSON here is only the Blockbench preview. |
| Generic Model / glTF, Java block/item, Hytale, OBJ | None | Fake the effect with geometry, emissive flipbook textures and bone keyframes, or leave it to the runtime. See [non-particle targets](references/delivery.md#targets-without-particles). |

Also settle the **trigger** before building, because Bedrock treats the two differently:

- **Animation keyframe** (`manage_particle_keyframes`): fire-and-forget. Good for one-shots (impact sparks, a poof on landing, hearts). A *looping* emitter fired this way never stops in game, and a looping clip starts another one every cycle. For a continuous effect keyed on a looping clip, use `looping: false` with `duration` equal to the clip length, keyed at 0.
- **Animation controller state**: the game starts the emitters on state entry and ends them on exit. This is the right home for sustained loops (a burning state, a casting state). The MCP tools do not edit controllers; add the entry in Blockbench's Animation Controllers panel or in the controller JSON ([delivery](references/delivery.md#controller-states)).

The tools warn when a looping effect lands on a keyframe.

## 2. Tools

Desktop plugin (Blockbench open):

| Tool | Use |
|---|---|
| `list_particle_presets` | Presets, built-in sprites and textures, materials, facing modes. Read before designing. |
| `create_particle_effect` | Preset + design knobs (or raw JSON) → `<pack_root>/particles/<name>.json`, validated and loaded into the preview. Optional custom texture from a Blockbench texture or PNG. |
| `update_particle_effect` | Change knobs on an existing file (only the components each knob owns are rewritten), replace it with raw JSON, or load a file from disk. |
| `add_locator` | Named point on a bone that effects spawn at and follow. Formats with locators: Bedrock Entity, GeckoLib, Generic Model. |
| `manage_particle_keyframes` | Add, remove or list particle keyframes on an animation. Validates locators and times. |
| `list_particle_effects` | Loaded effects, usages, preview problems, looping-on-keyframe warnings and the client-entity map. |
| `export_particle_pack` | Copy used effects and custom textures into a resource pack; returns the `particle_effects` map. |
| `animation_timeline` `set_time`, `capture_screenshot` | Preview. |

Headless server (files only, parallel agents): `bbmodel_particle_effect` (create/update a file next to the model), `bbmodel_edit` operations `add_locator`, `set_particle_keyframe`, `remove_particle_keyframe`, and `bbmodel_particle_pack`. Keyframe `file` paths are relative to the `.bbmodel` (`particles/smoke.json`); `bbmodel_particle_effect` returns the right value as `keyframe_file` when given `model`. Headless cannot render particles; open the model in Blockbench to preview.

## 3. Workflow

1. **Plan the effect.** Write down what it communicates, where it spawns, how long it lasts, how many particles are alive at peak, and whether it is continuous or one-shot. Read [effect design](references/effect-design.md) for scale, timing, color and budget rules.
2. **Place locators** at the spawn points: a chimney top, a mouth, a sword tip, a wheel's contact point. Parent them to the bone that should carry the effect. Positions are absolute model units (16 per block).
   ```
   add_locator: name="mouth", parent="head", position=[0, 26, -7]
   ```
3. **Create the effect** from the closest preset and adjust knobs. Units are blocks and seconds.
   ```
   create_particle_effect: identifier="mymod:dragon_smoke", preset="smoke",
     design={rate: 10, size: [0.3, 0.9], color: ["#6b5b53cc", "#3a3a3a"], looping: false, duration: 2}
   ```
   Use your own namespace, never `minecraft:`. For a custom sprite, paint or generate a small PNG first (8-32 px, transparent background) and pass `texture_image`; sprite sheets use `design.flipbook` (vertical strips by default, like [flipbook textures](../blockbench-flipbook-textures/SKILL.md)).
4. **Key it.** Continuous effect on a looping clip: one keyframe at 0 with the `looping: false`, `duration` = clip length variant. One-shot: a keyframe on the contact frame.
   ```
   manage_particle_keyframes: animation_id=<clip uuid>, action="add",
     keyframes=[{time: 0, effect: "mymod:dragon_smoke", locator: "mouth"}]
   ```
   Read every returned warning; fix them rather than reporting them.
5. **Preview** in Animate mode: `animation_timeline set_time` to 0, then to two or three moments (early, peak, late), capturing each. After editing an effect, go back to 0 first so emitters restart with the new settings. Check readability at the intended camera distance, not only close up.
6. **Validate** with `list_particle_effects`: no problems, no checkerboard textures, sensible counts.
7. **Deliver** per [delivery](references/delivery.md): `export_particle_pack` to the resource pack, paste the returned `client_entity.particle_effects` into the client entity, export the animation JSON, and save the `.bbmodel`. Report the files written and any step left to the user (client entity edits, controller states, in-game check).

## 4. Rules That Prevent Broken Effects

- **Blocks, not pixels.** Particle sizes, speeds, offsets and shape radii are in blocks; locators and model coordinates are in pixels (16 per block). Billboard `size` is a half-width: 0.1 is a vanilla smoke puff (0.2 blocks across) and 0.5 spans a whole block.
- **Material decides fades.** `particles_alpha` cuts off partial transparency, so alpha gradients pop. Use `particles_blend` for smoke and soft shapes and `particles_add` for light (fire, magic, sparks, glow).
- **White keeps sprite colors.** Tints multiply. Colored sprites (flame, heart, bubble, soul, fire) want white or no tint.
- **Budget live particles:** rate × lifetime. Keep ambient loops under about 50, busy effects under 100, and never let `max_particles` cap a steady emitter mid-effect (the validator reports it).
- **Local space vs world space:** `local_space: true` makes particles move with the bone (auras, rings, orbiting motes). Leave it off for smoke, trails and exhaust so they stay behind as the model moves. `bind_to_actor: false` on a keyframe leaves the whole emitter where it spawned.
- **The preview is not the game.** Blockbench has no blocks to collide with and approximates lighting, and it restarts looping emitters every `duration` seconds (presets use 10 s for that reason). Verify collisions, lighting and `entity_aabb` shapes in game when possible and say so when not.
- **Names must resolve.** Keyframes use effect *names*; the client entity maps names to identifiers. `export_particle_pack` reports name conflicts, missing textures and keyframes without files.

## References

- [Effect design](references/effect-design.md): planning, presets, recipes, color, timing, budgets, Molang patterns, custom sprites.
- [Bedrock particle format](references/bedrock-particle-format.md): component cheat sheet, raw JSON skeleton, events and curves, for effects the knobs cannot express.
- [Delivery](references/delivery.md): Bedrock resource pack wiring, controller states, attachables, GeckoLib handlers, and substitutes for targets without particles.
- Primary sources: [Particle entity integration (Microsoft)](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particleentityintegration?view=minecraft-bedrock-stable), [Bedrock particle documentation](https://bedrock.dev/docs/stable/Particles), [Snowstorm](https://snowstorm.app) for hand editing, and Mojang's [vanilla particle files](https://github.com/Mojang/bedrock-samples/tree/main/resource_pack/particles) as worked examples.
