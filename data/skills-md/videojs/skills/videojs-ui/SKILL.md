---
name: videojs-ui
license: Apache-2.0
description: >
  Use when building, polishing, or reviewing the interface of a Video.js 10
  player: custom controls and overlays, control bars, menus and popovers,
  sliders, time displays, icons and icon states, motion, color, and control
  labels, in skin source or in custom components that read player state.
  Applies interface-craft skills such as Jakub Krehel's better-* skills, Emil
  Kowalski's design and animation skills, and an accessibility audit, within
  the constraints of UI that sits over moving video.
---

# Craft Video.js player UI

Player UI is ordinary interface work with unusual conditions: it floats over
a picture that keeps changing, hides itself when idle, is driven by keyboard,
mouse, and touch at once, and reports state that changes many times a second.
General interface advice applies, adjusted by the rules below.

For a whole skin project, the `videojs-skin` skill covers setup, the
workbench, and publishing. To install or configure a player, use the `videojs`
skill.

## Find the docs

Read the docs bundled at `node_modules/@videojs/<react|html>/docs/llms.txt`,
or `https://videojs.org/docs/framework/<react|html>/llms.txt` with `.md`
appended to page URLs. By title:

| Need | Read |
| --- | --- |
| How controls expose state, props, and render customization | UI components |
| A control the library does not provide | Build your own UI component |
| One component's parts, `data-*` state, CSS properties, and keys | Its reference page |
| What the components already do for accessibility | Accessibility |
| Shortcuts, gestures, and translated labels | Keyboard shortcuts, Internationalization |

## Workflow

1. Know what you're building before styling it. When there's a reference or a
   design spec, build to it and add nothing it doesn't show or the user
   didn't ask for. When there isn't, describe the intended look in a few
   lines and confirm it before building more than one control.
2. Start from a Video.js component, or render your element through one, so
   it keeps its role, translated label, state attributes, and keyboard
   support. Build from scratch only what the library lacks, following Build
   your own UI component.
3. Apply the rules below while building.
4. Polish with the companion skills in `references/companions.md`, when they
   are installed or the user agrees to add them.
5. Review with `references/review.md` before handing back.

## Rules for UI over video

- **Contrast against the picture, not a page background.** Measure text and
  icons over bright, dark, and busy frames. Separate controls from the video
  with a scrim, gradient, translucent surface, or shadow; a hairline border
  alone disappears.
- **Keep numbers steady.** Time displays always use
  `font-variant-numeric: tabular-nums` (Tailwind `tabular-nums`), and so do
  rates and counts that change while playing, so digits keep their width and
  the layout never shifts. Allow room for hours on long media and for live
  labels.
- **Icons are one set, drawn at the size they render.** From the user's own
  design file, use its icons as exported. When matching someone else's
  player, redraw its icons to look identical; don't copy its SVG. Otherwise
  use an existing set, or a new set with one grid, stroke, radius, and
  style. Never mix sets. Read `references/icons.md` before adding or
  changing icons.
- **Swap icon states in place.** Play and pause, volume levels, and enter or
  exit icons share one position and switch on the component's `data-*`
  attributes, crossfading rather than jumping. Keep one stroke weight and
  optical size across the set.
- **Keep frequent controls fast.** Play, mute, and seeking are pressed
  constantly: give them immediate press feedback and little or no motion.
  Menus and popovers grow from their trigger, and the settings menu opens
  quickly because people open it often.
- **Hide and show controls calmly.** Idle hiding uses a short, subtle exit;
  controls return at once on pointer movement, touch, or keyboard focus.
  Nothing animates on first load.
- **Touch is first-class.** Put hover styles behind a hover-capable pointer
  query, because a tap shows controls and a stuck hover looks selected. Make
  targets at least 24 by 24 CSS pixels, larger on touch, with slider hit
  areas taller than their visible track and no overlapping targets in dense
  control bars.
- **Motion respects preferences.** Route durations through tokens that
  collapse under reduced motion, animate `transform`, `opacity`, and `filter`,
  and name the properties a transition covers.
- **Color by purpose.** Use semantic tokens such as the accent and controls
  surface, keep the accent for the brand, and keep video controls dark in
  both color schemes unless the design proves otherwise.
- **Never hardcode UI copy.** Visible text, tooltips, and accessible names
  come from Video.js i18n: built-in controls ship translated labels, and new
  strings go through Video.js translations (Internationalization). Keep them
  sentence case and say what happens. Leave room for longer languages and
  mirror the layout for right-to-left.
- **Keep tooltips and focus consistent.** When the player has tooltips, every
  one uses the same offset from its control and the same style, including at
  the player's edges. Every
  focusable part, buttons, slider thumbs, and menu items, shows the same
  visible focus ring, styled from the skin's tokens.
- **Default to system fonts.** Set `--media-font-family` to a system font
  stack unless the user has a web font licensed for their site, and tell the
  user when you choose system fonts over a reference's web font.
- **State is never color alone.** Pair it with an icon change, a label, or
  shape, and keep custom state announced in a live region when the status
  announcer does not cover it.
