---
name: woostack-design
description: "Organize user flows, screen sequences, and multi-step UI designs into a standardized horizontal layout with aligned branch rows and vertical flow separation."
---

# woostack-design

Organize multi-step user flows, screen sequences, and UI journeys into a clear, standardized
spatial layout. Spatial arrangement and consistent relative rhythm communicate progression and
branching without altering frame content or visual styling. Caller-supplied tool context owns
execution; this skill contributes only the layout standard.

## Command

- `/woostack-design [target]`
  - Standardizes spatial flow layout for multi-step UI sequences, screen flows, or user journeys.

## Layout standard

Apply this spatial standard to all arranged flows:

### 1. Flow grouping and title hierarchy

- **One group per flow.** Enclose each distinct flow—including its title, description, main step
  sequence, and all associated forks—in a single dedicated parent group.
- **Title and description.** Place the flow title above the step sequence. Place the flow
  description directly below the title.

### 2. Primary sequence

- **Left-to-right progression.** Arrange primary sequence step frames horizontally from left to
  right in sequential order.
- **Consistent horizontal rhythm.** Maintain a uniform relative horizontal gap between adjacent
  step frames across the sequence.
- **Preserve frame design.** Preserve supplied frame dimensions, aspect ratios, and visual styling.
  Do not resize, restyle, or alter the internal content of any frame.
- **Screen-frame backgrounds only.** Give each actual screen frame a background that makes its outer
  edge unambiguous. Do not add backgrounds to flow groups, sequence or fork rows, titles,
  descriptions, labels, or surrounding canvas regions.
- **Preserve clear frame backgrounds.** Keep an existing screen-frame background unchanged when it
  already defines the screen edge; otherwise add only the frame-level background needed to make
  that edge clear.

### 3. Branches and forks

- **Dedicated rows beneath source.** Place alternative paths, error branches, and forks in their own
  horizontal rows positioned beneath the exact source sequence from which they branch.
- **Fork row order.** Order fork rows from top to bottom by their source steps' order in the flow:
  earlier forks sit above later forks. Keep forks from the same source step together in their
  existing relative order, and keep nested forks beneath their own source sequence.
- **Equivalent-step alignment.** Place steps representing the same stage or outcome in the same
  column across the primary sequence and fork rows, so equivalent steps align vertically.
  Match by meaning, not ordinal position within each row.
- **Fork start.** When a fork's first frame has an equivalent step, use that step's column;
  otherwise align it directly beneath the source step from which it branches.
- **Matching rhythm.** Subsequent frames proceed left-to-right using the primary sequence's
  horizontal spacing rhythm. Leave empty column space for skipped steps and reserve columns for
  branch-only steps across affected rows; equivalent-step alignment takes precedence over uniform
  gaps between occupied frames. Preserve each path's step order.
- **Clear vertical separation.** Maintain a distinct relative vertical gap between the source
  sequence and each fork row.
- **Branch explanation.** Precede every fork's first screen with a concise explanation of the branch
  condition or trigger, placed immediately to the left of that screen. Keep the explanation outside
  screen frames and reserve space for it without shifting screens out of their aligned columns.
- **Contained in flow group.** All fork rows and explanations remain inside the parent flow group.

### 4. Multi-flow arrangement

- **Vertical stacking.** When organizing multiple distinct flows on the same canvas, stack flow
  groups vertically with clear separation that accounts for every fork row so that flows never overlap.

## Hard constraints

- **Relative layout only.** Define spatial placement through relative positioning, uniform spacing,
  and column alignment. Do not rely on fixed numeric dimensions or pixel coordinates.
- **Preserve visual design.** Except for a screen-frame background required above when the screen
  edge is unclear, do not alter colors, typography, frame sizing, or existing visual appearance.
- **No connectors.** Do not create arrows, connecting lines, or link vectors between frames.
  Spatial alignment and horizontal reading order establish sequence and relationships.
- **Tool agnostic.** Do not include tool-specific APIs, MCP bindings, platform plugins, scripts,
  templates, or external assets.
