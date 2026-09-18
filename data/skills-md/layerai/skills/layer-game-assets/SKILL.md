---
name: layer-game-assets
description: "Use when producing in-game art with Layer: characters, heroes, NPCs, enemies and mascots, environment and background concept art, parallax layers, or game UI such as icons, buttons, frames, panels, HUD elements and currency symbols. Also when a cast must stay on-model across many images, when an icon must read at 64px, or when a character must be split into parts for a skeletal rig. Keywords: character art, NPC, enemy, concept art, background, parallax, game UI, HUD, icon set, Spine, rigging."
license: MIT
---

# Layer Game Assets

## Overview

Game art differs from illustration in one way that governs everything: it has to sit in a system.
An icon shares a set, a character shares a cast, a background shares a parallax stack. A beautiful
asset that does not match its neighbours is a defect.

Generation mechanics are in the `layer` skill and prompt craft is in `layer-image`. This skill covers
what those leave out: the constraints specific to art that ships inside a game. Pixel art has its own
rules (`layer-pixel-art`), as do tiling surfaces (`layer-textures`).

If a sibling skill named here is missing from your available skills, ask the user to install it
(`npx skills add layerai/skills --skill <name>`); unattended, proceed from tool schemas and flag the
gap.

## Characters and casts

A character prompt must name the **role** before the look. An enemy grunt, a shopkeeper, and a raid
boss are read differently by players, and silhouette carries that read before any detail does. State
silhouette explicitly: bulk, stance, and the one shape that identifies them at a glance.

Then pin the production terms a prompt cannot leave to chance: full body or portrait, view (front,
three-quarter, side), background treatment (isolated on flat colour if it will be composited), and
whether the pose is neutral for reference or dynamic for key art.

A cast is the hard part. Writing the same adjectives twice does not produce the same character, and
seeds do not carry across prompts. Two things work:

1. **Anchor image.** Approve one hero image, then drive every sibling with it attached as
   `reference_image`, filtering for `image_editing`, which is the capability for art that must
   reproduce a provided subject. `style_reference` transfers a look only and will not keep the
   character, which is the usual reason an anchored cast still drifts.
2. **Trained style.** For a cast that will grow over weeks, train a reference set on approved art and
   apply it to every run. See `layer-reference-sets`.

The first is right for a handful of assets this week. The second is right for a live game.

## Rig-ready characters

A character destined for Spine or a skeletal rig needs its parts separable. Generate the character
in a neutral, limbs-apart pose so no part occludes another, on a transparent or flat background, then
separate the parts with `layer-image-editing` using `split_into_layers`.

Occlusion is the thing to get right up front: a crossed arm or a cloak covering the torso means the
hidden geometry does not exist in any layer, and no amount of splitting recovers it. Say
"arms clear of the body, legs apart, cape swept behind and clear of the torso" in the prompt.

## Environments and parallax

An environment prompt needs camera height and depth layers stated, because these are what make a
background sit behind gameplay rather than compete with it. Name the tier the art belongs to:
foreground silhouette, midground playable, far background.

For a parallax stack, generate each layer as a separate run against one shared style anchor, and say
in each prompt what that layer contains and that the rest is empty: "far background only, distant
mountains and sky, nothing in the midground or foreground, isolated on transparent". Generating the
whole scene and splitting it afterwards gives layers that were never designed to move independently.

Keep contrast and saturation deliberately low on gameplay backgrounds. The most common note on
generated game backgrounds is that they are too busy to read characters against.

## UI and icons

State the pixel size in the prompt, and design for the smallest one. An icon set delivered at 512px
that turns to mush at 64px has failed, and the fix is fewer elements and heavier strokes, not a
better upscale.

Hold a set together by naming the shared grammar in every prompt: stroke weight, corner radius,
perspective (flat, isometric, or slight three-quarter), palette, and whether icons sit on a plate or
float free. Generate on transparent backgrounds so the engine can place them.

Extending an existing set is an editing job, not a generation job: attach two or three approved icons
as style references so the new one inherits the grammar rather than reinventing it.

## Worked example

"Six ability icons for our fantasy RPG, matching the two we already approved."

1. The two approved icons already have `file_id` values from their original runs.
2. `list_base_models` with `filter.use_case: "text_to_image"` and
   `filter.capabilities: {image_editing: true, square: true}` (an object of booleans, not a list of
   names). Take the first result.
3. One run per icon, six runs. Each attaches both approved icons as `reference_image`, and each
   prompt names the shared grammar plus the one new subject: "Ability icon, 64px target, flat
   three-quarter view, heavy uniform outline, two-tone fill, muted gold and slate palette, isolated
   on transparent. Subject: a frost sigil."
4. Estimate the first, confirm the look, then run the remaining five.
5. Review them together at 64px, not individually at full size.

## Common mistakes

- Judging an icon at full resolution instead of at its target size.
- Rewriting the same description and expecting the same character.
- Generating a whole scene, then splitting it into parallax layers afterwards.
- Generating a rig-ready character in a pose where limbs occlude the torso.
- Leaving background treatment unstated on an asset that will be composited.
- High-contrast, busy gameplay backgrounds that characters cannot read against.
- Adding to an approved icon set without attaching the approved icons as references.
