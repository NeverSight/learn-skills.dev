---
name: sgdk-raster
description: Implement SGDK per-line scrolling and H-interrupt display effects, including waterline palette switches and split-screen cameras. Use for water ripples, heat haze, road-style scroll tables, mid-frame palette changes and two-view displays, rather than ordinary sprites or whole-plane scrolling.
---

# SGDK Raster

Choose the least timing-sensitive technique that gives the desired effect.
Water ripples usually need a line-scroll table, not an interrupt on every line.
A Sonic-style underwater tint does need a mid-frame palette change: the same
color indexes acquire different colors below the waterline.

Use `ewrogers/sgdk:latest`, pulling before validation. Check the selected SDK's
headers, implementations and H-interrupt samples before using an unfamiliar
call. These references were verified with SGDK 2.11; do not silently transfer
their timing assumptions to another video mode or driver.

## Choose the effect

- [Scroll tables](references/scroll-tables.md): per-line waves, camera offsets,
  persistent DMA sources, MAP ownership and separate RAM/transfer costs.
- [Waterline palettes](references/waterline-palettes.md): the interrupt ABI,
  HBlank synchronization, palette ownership and a deliberately masked split.
- [Split-screen cameras](references/split-screen.md): two independent views,
  resident map ownership, sprite clipping and the difference from Sonic 2 interlace.
- [Timing and validation](references/timing-and-validation.md): interrupt/main
  coordination, PAL/NTSC, audio interaction and what each test proves.
- [Raster Lab](assets/raster-lab/README.md): a standalone water scene with original
  foam, bubbles, splashes and soft FM music over Level Lab's map/robot.
- [Split Lab](assets/split-lab/README.md): a separate two-camera ROM with a CPU
  second player, a masked midpoint and per-view sprite projections.

## Make the ownership explicit

Keep ordinary VDP work and queued DMA in VBlank. Prepare scroll tables and
palette variants outside the handler. Protect main-loop VDP port operations
against an H interrupt; an interrupted command/data sequence can corrupt the
display. Do not add allocation, decompression, logging, formatting or audio
calls to a scanline handler.

`SYS_setHIntCallback()` jumps directly to its callback. Use
`HINTERRUPT_CALLBACK`, which must return with `RTE`, not a normal C return.
`VDP_setHIntCounter(N)` means every `N + 1` lines. Re-enabling may deliver a
pending event during VBlank; do not let that consume the intended active split.

Restore the normal palette at the start of VBlank, before queued DMA can consume
its budget. SGDK's `SYS_setVBlankCallback()` runs after those tasks; Raster Lab
uses `SYS_setVIntCallback()` for this deadline and keeps HUD work in the later
callback. Finish Z80 driver loading before installing raster callbacks. Publish
the split line and enable flag together with the completed sprite/scroll frame;
do not let an interrupt read a partly updated game model. See the timing reference
for the callback ownership and main-loop port protection this requires.

Do not claim a whole palette fits inside one HBlank. Display blank alone does
not hide CRAM dots, nor does an opaque sprite. The lab writes only two colors per
fresh HBlank, skips unchanged pairs and masks the mixed-palette rows with animated
surface sprites on an unchanged palette. That is a conservative teaching design, not
a cycle-exact reproduction of Sonic's renderer or a universal raster API.

## Prove the result

Exercise table bounds, phase wrap, camera limits, pause and region cadence.
Record palette restoration, one-shot arming, pending/late events and bounded
timeouts. Inspect the target handler's disassembly: correct interrupt return,
preloaded port writes and bounded polling matter here.

Then inspect the ROM in actual detected PAL/NTSC modes. Move the waterline,
pan the camera, cross the split with a sprite and listen with graphics DMA
active. Check the HUD stays unchanged and late/timeout diagnostics stay stable.
Sweep the waterline repeatedly through its full range in both directions. A
stationary split can hide missed palette restores and frame-snapshot mismatches.
Host tests and a clean emulator image do not certify CRAM timing on a console;
record hardware and emulator evidence separately.

For split-screen, also check camera independence, viewport-origin offsets,
sprite disappearance at each view's edges and the shared scanline budget.
The supplied Split Lab uses normal noninterlaced output and one resident world;
do not present it as Sonic 2's double-resolution renderer or a streaming solution.
