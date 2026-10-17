---
name: sgdk-ui
description: Build SGDK fonts, text, menus and HUDs with bounded formatting, controller navigation and clear tile/palette ownership. Use for title screens, options, pause menus, score displays and text glitches, rather than general sprite or scrolling-map work.
---

# SGDK UI

Make the screen easy to read and the controls predictable. SGDK supplies text
and VDP functions, not a ready-made menu or widget system. Keep menu state,
controller navigation and drawing separate enough to test without a console.
Use the game's existing structure rather than imposing a UI framework.

For NPC conversations, branching choices and portrait exchanges, use
`sgdk-dialogue` when available. This skill covers the shared UI foundations.

## Choose the right reference

- [Fonts and text](references/fonts-and-text.md): glyph layout, bounded
  strings, numbers, field widths and clearing old text.
- [Menus and controls](references/menus-and-controls.md): focus, repeat,
  pause, transitions and options.
- [HUDs and budgets](references/huds-and-budgets.md): Window, planes,
  palettes, font tiles and transfer costs.
- [Menu Lab](assets/menu-lab/README.md): an original title/options/pause/results
  example with a switchable font and fixed score HUD over a scrolling grid.

Build with `ewrogers/sgdk:latest` and pull before validation. Check unfamiliar
calls in the selected image's `inc/vdp_bg.h`, `src/vdp_bg.c`, `inc/vdp_tile.h`,
`inc/vdp.h`, `inc/joy.h` and `bin/rescomp.txt`. The references cite SGDK 2.11;
verify differences when the image moves forward. Never invent menu, Unicode,
wrapping or font APIs that the installed SDK does not provide.

## Plan the screen before drawing

Agree on visible rows/columns, safe margins, glyphs, palette lines and which
plane owns the HUD. Text coordinates are 8x8 cells. A 320x224 display has
40x28 visible cells, even if its backing plane is larger. Keep player-facing
text inside the visible area; plane clipping alone is not screen clipping.

Reserve font and UI graphics tiles alongside the game's other art. A font
normally replaces SGDK's font slots; it must not silently overwrite sprite or
map storage. Decide who may change its palette during fades or transitions.
Window replaces part of plane A; it is not an extra scrolling background.

## Keep updates small and predictable

Sample cached input once per frame. Confirm/back are press edges; held cursor
movement gets an explicit delay and repeat interval. Base menu repeat and
countdowns on the project's region/timing policy, not assumed 60 Hz frames.
Consume the action that opens a screen so it cannot also select its first item.

Use bounded buffers and field widths. Pad or clear a field when its new value
is shorter; avoid formatting and rewriting unchanged HUD text every frame.
The SDK's string conversion calls do not receive destination capacity. Check
the selected implementation before choosing a convenience helper.

Test navigation, held buttons across transitions, changing options, pause,
maximum numbers, shorter replacements and unsupported text bytes. Compile real
font resources and verify glyph order, not just C syntax. Finish with an
emulator checklist and say which checks still need console testing.
