---
name: figma-roundtrip
description: Keeps a video motion-graphics kit and its editable Figma boards in sync - the creator designs and tweaks in Figma, Claude ports the changes into the Remotion components and brand tokens, and mirrors code changes back. Use when the creator says they changed the boards, wants a new graphic designed, or wants the kit visible in Figma.
---

# Figma ↔ motion kit

Creators design better in Figma than in prompts. Keep every kit component mirrored as an **editable board** and let them edit there.

## Set up once
- A page in their brand file (e.g. "Claude - Editable") with a section per kit version ("Motion kit v1", "Vlog kit v1").
- One board per component at the video's frame size, real copy, every layer named.
- Colours and type bound to **variables** (a "Motion" collection: ink, paper, accent/highlighter, greys; font sizes and paddings as numbers) so a colour change is one edit.
- Use the Figma MCP (load its `figma-use` skill before writing to the file). Record the file key and page in CLAUDE.md.

## When they say "I changed the boards"
1. Read each changed board's layers: fonts, weights, sizes, line heights, paddings, positions, which variables they use, corner radius, strokes.
2. Port the differences into the components and `brand.json` (tokens first, component code only for layout).
3. Render preview stills of the same components and compare side by side with the boards.
4. List what changed ("title Light 120 → Regular 108, padding 64 → 80, label now uppercase mono").

## When the kit changes in code
(e.g. a narrow-frame layout, a caption-safe band) update the matching boards so the two never drift, or tell the creator which boards are now out of date.

## Learned taste (ask your creator, these are examples)
Light/regular at big sizes, never heavy bold; monospace light uppercase labels; 80 px padding; lots of space; one smooth move per element; no device mockups (they add little); prefer text overlays and personal notes.
