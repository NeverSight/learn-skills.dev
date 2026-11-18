---
name: review
title: Review a sprite before calling it done
description: Run the mechanical checks and the by-eye checks, then report what you found with evidence instead of declaring success. Use before finishing any pixel-art task, and when the user asks "is this good" or "why does this look off".
---

# Review a sprite before calling it done

"Done" is a claim. This is how you earn it.

## Procedure

### 0. Cold read

Before you look at the brief again: `look op="preview"`, and write one
sentence on what the picture shows to someone who was never told, plus the
three things the eye lands on first. If that sentence does not name the
subject, or misses a part the brief makes central, the sprite fails review
whatever `validate` says. Squint at the same preview for value: the subject's
lit side should be among the lightest values and its core shadow among the
darkest; everything in the bottom third reads as murk.

### 1. Mechanical checks

```
validate
```

Reports off-palette colours, semi-transparent pixels, isolated stray pixels,
untagged animation frames, uniform timing and unsaved state — each with a
location where one exists.

Fix every **error**. For each **warning** you do not fix, have a reason and say
it.

For animation, tell `validate` what the cycle is supposed to be, and it checks
that instead of only the generic rules:

```
validate expect={ layerFrames: { "sword-fx": [[3,4]] }, mustNotOverlap: [["sword","head"]] }
```

`layerFrames` flags a layer that is empty inside its frame range or has pixels
outside it (a slash effect leaking into the idle); `mustNotOverlap` flags any
frame where two layers' pixels collide (the blade crossing the face).

### 2. Look at it

```
look op="preview"
```

Work down `rules://07-review-checklist`:

- **Silhouette** — recognisable as one flat shape?
- **Value contrast** — would it survive desaturation?
- **Light** — one direction, everywhere?
- **Ramps** — do shadows hue-shift, or are they just darker?
- **Lines** — even runs, no doubled pixels?
- **Outline** — one style, applied consistently?
- **Banding** — long parallel stripes of adjacent ramp steps?
- **Detail placement** — spent on the face and weapon, not the boots?

If the sprite was drawn from a reference (`reference op="list"` is not empty),
`look op="compare"` on each key frame too. A mismatch the PixelSpec lists as a
deviation is a decision; any other large one — a limb in a different place, a
silhouette that lost its defining shape — is a finding.

### 3. Look closely at anything that felt off

```
look op="ascii"
```

This is where you find the pixel one row too low and the line run of 3 in a
sequence of 2s. If step 2 left you with "something is wrong but I cannot say
what", this is the step that names it.

### 4. For animation

```
look op="filmstrip"
```

Volume consistent? Height consistent? Does it loop? Do contact poses hold
longer? Is there anticipation before strong actions?

Then check the in-betweens one at a time against their neighbours:

```
look op="onion" frame=3
```

Ghosts of frames 2 and 4 under frame 3 show whether the spacing eases or jumps,
and whether a limb changed length on the way — both invisible in a filmstrip.

### 5. Report

State what you checked, what you found, and what you chose not to change:

> Validated clean. Silhouette reads at 1×; value contrast holds desaturated.
> Two compromises: the plume colour snapped from `#e04a6a` to `#ff77a8`
> (ΔE 14) because PICO-8 has nothing closer, and the far arm is 2px thick
> rather than 3 to keep the silhouette from fusing with the torso.

A user can act on a stated compromise. They cannot act on one you hid.

## When the user asks "why does this look off"

Run the same checks, then name the specific cause rather than listing
possibilities. The usual answers, in order of frequency: too many colours, flat
shading, semi-transparent pixels, mushy silhouette, uniform animation timing.

## Related

`rules://07-review-checklist`, and every other rule it points at;
`rules://92-generated-art-tells`; and the *Review* section of the subject file
for what was drawn (`skill://studio`, *Subject rules*).
