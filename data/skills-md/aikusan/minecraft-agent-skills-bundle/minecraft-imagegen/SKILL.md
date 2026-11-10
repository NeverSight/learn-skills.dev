---
name: minecraft-imagegen
description: "Generate Minecraft-focused raster assets with Codex's built-in image generation tool, including pack icons, promo art, concept textures, thumbnails, server banners, and UI mockups. Use when the deliverable should be a bitmap image rather than JSON models, SVG, or code-native assets."
---

# Minecraft Image Generation Skill

Use this skill when a Minecraft project needs new raster art or a visual concept
that will later be refined into a resource pack, release post, store listing, or
server brand asset.

## Scope

### Routing Boundaries
- `Use when`: the task is generating or editing a bitmap image for a Minecraft project, such as `pack.png`, release art, store thumbnails, concept textures, UI mockups, or server/banner art.
- `Do not use when`: the task is deterministic resource-pack implementation work such as `pack.mcmeta`, block/item model JSON, blockstates, fonts, sounds, or shader files (`minecraft-resource-pack`).
- `Do not use when`: the task is vector/code-native UI, an existing SVG/logo system, or non-image code/assets.
- `Do not use when`: the current host does not expose built-in image generation or an equivalent image-editing tool.

### Support Assets

- Read `references/prompt-patterns.md` when the request is underspecified or you need a stronger generation vs edit prompt shape.
- Read `references/asset-recipes.md` when the user names a concrete deliverable such as `pack.png`, a release banner, a server header, or a texture concept sheet.
- Use `scripts/scaffold-asset-brief.sh` to create a reviewable asset brief in the active workspace before generation when the task needs multiple rounds or stakeholder feedback.
- Relative `--out` values such as `docs/briefs` are resolved from the project workspace, not from the installed skill directory.
- If you invoke the script from the installed skill directory and the workspace cannot be inferred cleanly, pass an absolute `--out <project-dir>` path or set `CODEX_WORKSPACE_ROOT`.

---

## Default Execution

- If the current host does not expose built-in image generation or an equivalent image-editing tool, stop and tell the user this skill is unavailable on that host; offer to continue with prompt/brief preparation only, or switch to Codex or another supported host for actual generation.
- Use the built-in `image_gen` tool by default when the host supports it.
- Treat the first pass as concepting unless the user explicitly needs near-final artwork.
- The built-in image generation workflow supports fresh generations and edits against existing local/reference images; prefer that over describing a manual paint-over process.
- Save any chosen final asset into the current workspace; do not leave project assets only in Codex's default generated-images area.
- Preserve existing assets non-destructively by using versioned filenames unless the user explicitly asked to overwrite.
- If editing a local image, load or attach it first so the image is visible to Codex before requesting an edit.

---

## Good Use Cases

- `pack.png` concepts or replacements for mods, datapacks, or resource packs
- Release-banner art for GitHub, Modrinth, CurseForge, or social posts
- Texture look-dev references that will be cleaned up manually into final pixel art
- Server logos, banners, splash artwork, or rules-screen art
- HUD/menu mockups for plugin or mod UX planning
- Promo sheets that show blocks, mobs, or themed environments in-context

---

## Workflow

1. Confirm the current host actually exposes image generation or an equivalent image-editing tool; if it does not, stop at briefing or prompt-prep work instead of promising a generated asset.
2. Decide whether the asset is a concept, a reviewable mockup, or near-final artwork.
3. Decide whether this is a fresh generation or an edit of an existing image.
4. If the request is still fuzzy, scaffold a brief with `bash ./scripts/scaffold-asset-brief.sh --type <asset-type> --name <slug>` when the script is already being run from your project workspace.
5. If you are invoking the script from the installed skill directory instead, relative `--out` values still resolve from the project workspace; if the workspace cannot be inferred, pass an absolute project destination such as `bash ./scripts/scaffold-asset-brief.sh --type <asset-type> --name <slug> --out /abs/path/to/project/docs/briefs` or set `CODEX_WORKSPACE_ROOT`.
6. If style consistency matters, gather one or more reference images first.
7. Structure the prompt as scene or backdrop -> subject -> important details -> constraints.
8. Iterate with single targeted changes instead of rewriting the whole prompt every round.
9. Save the chosen final into the workspace with a descriptive filename such as `pack-icon-v2.png` or `release-banner-hero.png`.
10. If the asset will ship inside a resource pack, hand off final pack wiring to `minecraft-resource-pack`.

---

## Prompt Schema

Use a short, labeled spec when the request is not already precise:

```text
Use case: <pack-icon | texture-concept | promo-art | server-banner | ui-mockup>
Asset type: <where the image will be used>
Minecraft context: <vanilla-faithful | modded sci-fi | medieval RPG server | etc>
Primary request: <main prompt>
Input images: <reference or edit target, if any>
Style/medium: <pixel art | painterly splash art | clean UI mockup | product-style render>
Composition/framing: <close-up | square icon | wide banner | negative space left>
Palette: <color direction>
Pixel treatment: <flat tileable | hand-painted | chunky retro | crisp UI>
Text (verbatim): "<exact text>"
Constraints: <must keep / must avoid>
Avoid: <negative constraints>
```

For edits, explicitly say what must stay unchanged, for example: `change only the background; keep the logo, silhouette, and text layout unchanged`.

---

## Asset-Specific Guidance

### Pack Icons

- Design for square cropping and tiny-size readability.
- Keep the silhouette bold and text minimal.
- Generate high-resolution source art, then downscale to the final `64x64` icon manually if needed.

### Texture Concepts

- Ask for flat, front-on presentation with even lighting and minimal perspective.
- State whether the texture should feel vanilla-faithful, noisy/gritty, hand-painted, or stylized.
- Assume manual cleanup before shipping. Generated textures are best used as concept or paint-over references, not automatic drop-ins.

### UI Mockups

- Reserve negative space for labels, slots, and status text.
- Keep text large and high-contrast.
- Call out whether the mockup should feel vanilla, modded-tech, fantasy, or admin-panel inspired.

### Promo Art and Thumbnails

- Leave copy-safe negative space for release titles or taglines.
- Avoid tiny text and clutter that will collapse on mobile or store cards.
- Specify whether the output should show gameplay-like framing, hero artwork, or a clean showcase layout.

---

## Review Checklist

- The image reads clearly at the actual target size.
- Any text is spelled correctly and positioned as requested.
- No extra logos, watermarks, or unrelated objects were introduced.
- The style matches the requested Minecraft context.
- For texture concepts, the result looks easy to paint over, simplify, or tile manually.

---

## End-to-End Patterns

### Existing `pack.png` Refresh

1. Load the current `pack.png`.
2. Ask for an edit that preserves the core silhouette or theme while improving readability at icon size.
3. Keep at least one conservative variant and one bolder variant.
4. Save the selected result into the workspace with a versioned filename such as `pack-v2.png`.

### Texture Concept to Pack Handoff

1. Generate a flat texture concept with neutral lighting and no perspective.
2. Treat the result as look-dev, not an automatic ship-ready texture.
3. Hand the approved concept to `minecraft-resource-pack` for final pack structure, sizing, tiling, and JSON wiring.

### UI or Server Brand Mockup

1. Reserve explicit negative-space regions for text, buttons, or status overlays.
2. Keep generated text minimal; if exact typography matters, leave clean space and add final copy later in-code or in a design tool.
3. Save both the art-only background and the composed mockup when possible so downstream edits stay flexible.

---

## Example Prompt Shapes

Pack icon:

```text
Use case: pack-icon
Asset type: resource-pack icon
Minecraft context: vanilla-faithful fantasy mining pack
Primary request: a glowing emerald pickaxe crossed over a cave entrance
Style/medium: crisp pixel-art-inspired emblem
Composition/framing: centered square icon with bold silhouette
Palette: emerald green, deepslate gray, warm torch gold
Constraints: no text, no watermark, readable at very small size
```

Texture concept:

```text
Use case: texture-concept
Asset type: reference sheet for a block texture
Minecraft context: modded industrial factory pack
Primary request: concept art for a rusted steel machine casing block
Style/medium: flat texture concept
Composition/framing: straight-on tile, no perspective
Pixel treatment: tileable, lighting-neutral, easy to simplify into 16x16 or 32x32
Constraints: no background scene, no labels, no watermark
```

Promo banner:

```text
Use case: promo-art
Asset type: GitHub release banner
Minecraft context: cooperative sky-islands server
Primary request: sweeping hero art of floating islands linked by rope bridges and glowing lanterns
Style/medium: polished cinematic illustration
Composition/framing: wide banner with negative space on the left for release text
Palette: sunrise oranges, cool blue shadows, warm lantern gold
Constraints: no logos, no watermark, no tiny unreadable text
```
