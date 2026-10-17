---
name: sgdk-isometric
description: Build SGDK isometric views with coordinate projection, height-aware draw order, elevated surfaces and occlusion. Use for diamond maps, bridges, stairs, actors passing behind scenery and camera/picking problems.
---

# SGDK isometric

Keep the map, movement surfaces and drawing separate. Isometric projection makes
a 2-D world with height look three-dimensional; it does not supply physics,
resource streaming or automatic depth sorting in SGDK.

## Establish the coordinate contract

Choose tile width/height, map units, vertical scale, foot anchors and rounding.
Use world coordinates for collision and surfaces, then project and subtract the
camera for display. Keep the camera out of draw-order comparisons.
Read [coordinates and elevation](references/coordinates.md) for formulas,
known-height inverse projection, stairs, underpasses and controller mapping.

A character's elevation is not its drawing depth. Sorting by screen Y or
`x + y - z` alone fails when one character walks above a bridge and another walks
beneath it. Use a simple foot-depth key only when the content's assumptions make
it sufficient. Read [depth and occlusion](references/occlusion.md) before choosing
a sorter or splitting scenery.

## Design art that can be sorted

- Give each asset a consistent foot anchor and a collision footprint independent
  of its visible pixels. Trim transparency only if the anchor is preserved.
- Keep flat ground in a background when practical. Keep overhangs, foreground
  pillars, bridge decks and other independently occluding pieces separable.
- ResComp cutting a large sprite into hardware pieces does not let a character
  sort between those pieces; split into logical objects where needed.
- For complex overlap, use bounded ordering constraints with stable IDs and
  explicit support rules. Surface ownership can resolve a stair proxy overlapping
  the actor standing on it. Do not use an arbitrary tie rule to hide intersecting
  objects or cyclic content.
- Treat a cutaway or silhouette as a presentation choice. Hiding a roof must not
  silently remove its collision or change the character's surface.

## Integrate and budget

Pull `ewrogers/sgdk:latest` and verify the selected SDK's rendering APIs. Read
[SGDK rendering and budgets](references/sgdk-rendering.md) for actual depth
semantics, plane priority, palette ownership, hardware pieces and retained DMA.
Cache immutable scenery relationships if pairwise work is significant; rebuild
when that scenery changes. Keep dynamic work, capacity failures and graph cycles
visible and bounded. Measure a release build rather than assuming fewer objects
means a cheap frame.

Test projection signs and negative rounding, height round trips, above/below
ordering, disjoint projected shapes, stable ties, cycle/failure results and
walkway boundaries. Compare a cached sorter against the complete one. Verify
compiled assets and target arithmetic, then test actual movement and visuals.
PAL/NTSC build and logical tests do not certify VDP timing or console performance.

[Isometric Lab: Lantern Aqueduct](assets/isometric-lab/README.md) demonstrates a
small original garden, stepped approaches, a bridge and an underpass. Its art,
palette, music and movement tuning are illustrative, not requirements for a game.
