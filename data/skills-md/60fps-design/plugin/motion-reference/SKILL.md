---
name: motion-reference
description: >
  Build an iOS interaction by copying one that already shipped. Use when asked to design or
  implement any animation, transition, gesture or micro-interaction in SwiftUI: a bottom sheet,
  a pull-to-refresh, a card morph, an onboarding sequence, a loading state, a success moment.
  Also use when asked "how does app X do Y" about mobile motion, or for a reference clip to
  copy. iOS and SwiftUI only.
license: MIT
compatibility: Needs the 60fps MCP server (https://mcp.60fps.design/mcp), signed in with OAuth.
metadata:
  author: 60fps-Design
  version: "1.0"
---

# Motion reference

The `60fps` MCP server holds 2,000+ clips of real iOS interactions. Each one has a written motion
breakdown, and many have a compile-checked SwiftUI recreation. Use it instead of inventing timings.
The numbers in this library came off apps that shipped.

## Use the tools in this order

1. **`60fps_search_shots`**. Write natural language, not keywords. "Springy bottom sheet for
   checkout" works. "Sheet" does not. Only set `app` or `filters` if the user named one.
2. **`60fps_get_motion_breakdown`**. This gives you the start state, the transition, the end state,
   and the timing and easing. Design from this.
3. **`60fps_get_motion_code`**. This returns a self-contained SwiftUI file. **Show it to the user in
   full, in a swift code block.** It is the deliverable, not a citation.
4. **`60fps_get_related_shots`** if the first pick is close but not right.

## Read the results honestly

Search ranks the whole library by closeness, so it always returns something, however far off the
question was. A high `total` is how many shots were searched, not how many matched. Judge each
result on its own merits, and say so when nothing fits.

## When not to use it

The library is iOS only, and it is about motion.

Do not use it for Android, Material, Flutter, React Native or web. Do not use it for icon design,
colour palettes, logos or brand work. Do not use it for performance or frame-rate profiling, which
shares the name and nothing else. On any of those it will still return iOS clips, and they will be
wrong. Answer directly instead.

## Using the code

Each file is standalone. Paste it into Xcode and run it.

It carries none of the original app's words, colours, branding or assets, by design. Restyle it to
the user's design system. The motion is the part worth keeping.
