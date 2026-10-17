---
name: sgdk-graphics
description: Build SGDK sprite rendering, frame animations, scrolling backgrounds and palette effects. Use when implementing or improving game graphics, rather than preparing source art or diagnosing an unrelated build failure.
---

# SGDK Graphics

Help a game put its art on screen and update it efficiently. Work with the
project's existing loop and resource layout; this skill does not require a
scene system or a new engine.

## Start with the screen

Identify what moves, what stays fixed, and which colors change together. Read
the project's resource declarations and frame loop before assigning palettes,
tile ranges or a second graphics update.

For a new project, use the tested Linux ARM64/AMD64 toolchain:

```text
ewrogers/sgdk:latest
```

Check unfamiliar calls in that image's `/opt/sgdk/inc` and `/opt/sgdk/src`, and
resource syntax in `/opt/sgdk/bin/rescomp.txt`. The references below describe
SGDK 2.11; do not assume another version behaves identically.

## Choose the relevant guide

- [Sprites and animations](references/sprites.md): sprite allocation, animation
  controls, completion, frame timing and scanline limits.
- [Backgrounds and scrolling](references/backgrounds.md): plane layout, parallax,
  a fixed HUD, larger maps and scroll tables.
- [Palettes and frame updates](references/palettes.md): color ownership, fades,
  cycling and safe queued transfers.
- [Graphics Lab](assets/graphics-lab/README.md): a standalone example with two
  scrolling planes, an animated sprite, a one-shot animation, a fade and a
  palette cycle. Copy it into a new folder when a small reproduction is useful.
  Its optional [art generator](scripts/make_lab_art.py) recreates the supplied
  PNGs in a new directory without external image libraries.

## Keep the budgets separate

Track main RAM, VRAM, palettes, sprite count **and scanline peaks**, plus DMA
bytes and queue space. A large sprite can use several hardware sprites.
Sharing a sprite definition does not automatically share each instance's VRAM.
Loading another palette changes every object that uses that palette slot.

Choose the plane layout before assigning tile ranges. Initialize the sprite
engine before checking the remaining user tile range. Keep a clear owner for
each range and each palette effect; do not let two systems update the same
colors or call `SPR_update()` twice per displayed frame by accident.

Prefer built-in plane scrolling, prepared tiles and small palette updates over
redrawing whole images each frame. Keep queued sources alive and unchanged
until transfer, or use `DMA_QUEUE_COPY` for temporary data. See the frame guide
before changing DMA or VBlank scheduling.

## Prove the result

Build the affected resources and release ROM through Docker. Exercise observable
behavior: play/stop/replay, one-shot completion, scroll wrap or map boundaries,
fade/cycle interaction, allocation failure and teardown. Check PAL timing if the
game targets PAL; animation updates and VBlanks are not universal milliseconds.

Then check the actual screen in an emulator or on hardware. Look for missing
sprites on crowded rows, incorrect colors, seams, palette dots and stalls during
frame changes or transitions. State exactly what was built, what was run, and
what remains visually unverified. A successful build is not a frame-rate test.
