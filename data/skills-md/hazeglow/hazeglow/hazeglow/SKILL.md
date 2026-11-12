---
name: hazeglow
description: Add animated, grainy gradient backgrounds and mesh gradients to React and Next.js apps with the hazeglow package (WebGL2, zero dependencies). Use when a hero, section, card or page needs a gradient background, a mesh gradient, a Stripe-like animated gradient, a grainy, dithered or ASCII backdrop, or a replacement for a CSS linear-gradient, and whenever the user mentions hazeglow.
license: MIT
---

# Hazeglow

Hazeglow draws an animated gradient on a canvas with WebGL2: a blurred shape or a colour mesh, with film grain, slow motion, an optional hover pull and dither, ASCII, halftone, pixel or glass effects. A small JSON config goes in, a canvas comes out.

## When to use it

- A hero, section, card or full-page background that should move and glow instead of a flat CSS gradient.
- Mesh gradients, grainy gradients, dithered, pixel or ASCII backdrops.
- Not for text gradients, borders or icons, and not for dozens of gradients on one page (see Rules).

## Steps

1. Install: `npm i hazeglow`. Needs React 18 or 19. There is no CSS to import.
2. Pick a config, don't write one field by field:
   - best: ask the user to design one at https://hazeglow.dev/generator and paste the copied JSON,
   - or start from a preset: `presets.dusk`, `presets.pearl`, `presets.ember`, `presets.horizon`, `presets.ultraviolet` or `presets.candy`, then change `palette` and `background` to the site's colours.
3. Put it behind the content. The canvas fills its parent, so the parent needs a size:

   ```tsx
   import { Hazeglow, presets } from "hazeglow";

   export function Hero() {
     return (
       <section style={{ position: "relative", isolation: "isolate", minHeight: 480 }}>
         <Hazeglow config={presets.dusk} style={{ position: "absolute", inset: 0, zIndex: -1 }} />
         <h1>Your headline</h1>
       </section>
     );
   }
   ```

4. Remove the CSS gradient it replaces. Change the config to change the look; don't stack a CSS gradient on top of the canvas.
5. Keep a plain CSS background colour on the parent. Without WebGL2 on a GPU the canvas stays empty and `onUnsupported` is called once, so that colour, or an image you swap in, is the fallback.
6. To follow the site's theme, use CSS variables in the config: `palette: ["var(--brand, #4fc4f0)", "oklch(0.77 0.15 68)"]`. Colours can be hex, `oklch()` or `var(--token, fallback)`. Always give a `var()` a fallback. It redraws when the theme changes.

## Rules

- Run any config that comes from a URL, a CMS, storage or user input through `parseConfig` before rendering it. It never throws, clamps numbers and drops fields it doesn't know.
- Keep `version: 1` and don't add fields to a config.
- Next.js App Router: the component ships with `"use client"`, so render it straight from a server component. Configs are plain JSON and safe to import anywhere.
- Keep live gradients to a few per page. Browsers allow about 16 WebGL canvases and the oldest get dropped past that. For grids and lists, use a still image exported from the generator.
- Reduced motion is handled (one still frame, no hover), and it pauses off screen and in hidden tabs. Don't add your own motion toggle or unmount it for performance.
- Without React (Vue, Svelte, Astro, plain JavaScript): `import { createRenderer } from "hazeglow/core"` and follow "Without React" in the README.

## Reference

- Props, the full config reference, colours, hover and limits: `node_modules/hazeglow/README.md` when the package is installed, otherwise https://github.com/hazeglow/hazeglow#readme.
- Short version for agents: https://hazeglow.dev/llms.txt
