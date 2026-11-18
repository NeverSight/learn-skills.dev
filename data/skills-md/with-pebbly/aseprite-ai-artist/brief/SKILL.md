---
name: brief
title: Plan a sprite before drawing it
description: Turn a vague pixel-art request into a written brief — size, palette, view, light, outline style — and confirm it with the user before any pixel is drawn. Use when the request is open-ended ("make me a knight") rather than a specific edit.
---

# Plan a sprite before drawing it

A request like "draw me a knight sprite" contains none of the decisions that
determine whether the result is usable. Guessing them and drawing anyway wastes
the user's time and yours. Five questions, one answer, then draw.

## What you need to know

| Decision | Why it cannot be deferred | Reasonable default |
|----------|--------------------------|--------------------|
| **Canvas size** | Determines how much can be shown at all | 32×32 for a character |
| **Palette** | Choosing it later means repainting | PICO-8 (16 colours) |
| **View** | Side-on, top-down and 3⁄4 are different drawings | 3⁄4 |
| **Light direction** | Must be fixed before any shading | Upper-left |
| **Outline** | Changes every edge in the sprite | Selective, dark-coloured |
| **Destination** | A game engine wants tags and a sheet | Ask |

## Procedure

1. **`preflight`.** If not ready, stop and tell the user — nothing below works
   without a live Aseprite.

2. **Read what already exists.** If a sprite is open, `sprite_info` it. The
   user's existing canvas size and palette usually answer half the questions,
   and matching an existing project's style is almost always what they want.

3. **Draft the brief.** Fill the table above from what the user said plus the
   defaults. Do not ask about things you can reasonably infer — "a Game Boy
   style knight" has already told you the palette and the size range.

4. **Put it to the user in one message**, as decisions rather than questions:

   > 32×32, PICO-8 palette, 3⁄4 view, light from upper-left, selective dark
   > outline. Knight in plate with a sword, facing camera. Say if any of that
   > is wrong — otherwise I'll start.

   One round trip, not five. If they said nothing about a detail, they probably
   do not care about it.

   When the request is something new — a character, a prop, an animation —
   `aseprite:concept` follows, and its offer goes **in this same message**:
   the decisions above, then the image-model prompt in one code block, then the
   choice between sending references and continuing without. The user answers
   once. If they correct a decision, fix the prompt to match before they copy it.

5. **Ask only what genuinely blocks you.** If the sprite is for a specific game
   and you do not know its tile size, that one is worth asking. Light direction
   is not.

6. **Record the brief** in your working notes and hold to it. Every later
   decision either follows from the brief or is a mistake.

## Then

`aseprite:concept` for anything drawn from scratch — its offer is already in
the message above. Then `aseprite:new` to create the document, or
`aseprite:draw` if a suitable sprite is already open.

## Related

`rules://00-core-principles` for what the sizes buy you.
`rules://03-silhouette-and-form` for view and proportion.
`rules://30-proportions-by-size` and `rules://14-readability-and-scale` for what
each canvas size can hold; `rules://90-platform-styles` when the user names a
console or era.
