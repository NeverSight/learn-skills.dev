---
name: style-library
description: Select, customize, or extend the project's reusable motion-graphics card library and style templates. Use for choosing a visual style, adding a card, building a new style pack, or reusing a template in a HyperFrames video.
---

# Reuse the style library

Read `style-library/GUIDE.md`, then `style-library/registry.json`. Filter by
style, tier, and purpose before opening individual cards. Read the selected
style's `DESIGN.md`, `tokens.css`, and manifest slot limits.

For an overlay, preserve transparency outside the card and the speaker's face.
For a takeover, use an opaque background. Copy the chosen card into the video's
`compositions/`, localize its CSS, fonts, and GSAP dependency, fill its named
`data-slot` values, and wire its timing using the HyperFrames skill. Copying a
card without its relative dependencies does not produce a complete asset.

Use `style-templates/` for a whole-scene starting point. A media template may
require the student's own `assets/source.mp4`; check its README before rendering.

The catalog contains draft resources, not a promise that every card has passed
rendered QA. Lint and render the selected card at actual project resolution,
inspect its hero frame and transition, and check slot text at its maximum length.

When adding a style, use `node scripts/style-library/new-style.mjs 03 my-style "My Style"`, then
complete its design tokens, manifest, and cards. Run
`node scripts/style-library/build-registry.mjs` after manifest changes. Keep
project-specific copy in the project, leaving reusable library cards generic.
