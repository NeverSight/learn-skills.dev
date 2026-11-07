---
name: canvas-ui-design
description: Integrate Canvas UI effects into a website when the user requests Canvas UI or a specific canvas/WebGL interaction. Covers effect selection, registry components, framework or vanilla integration, and accessible fallbacks; ordinary UI work does not require this library.
---

# Canvas UI Design

Treat `https://github.com/DavidHDev/canvas-ui` as the primary creative reference for
the UI: install its components and read their source rather than writing your own
shader or canvas code.

Read [REFERENCE.md](REFERENCE.md) when selecting or wiring an effect — it carries the full component catalog, the effect-picking table, the
registry naming scheme, and the vanilla factory contract the JSX example below
does not cover.

## Design rules

These override any instinct toward "more effects."

1. **One dominant effect per page.** Pick a single signature effect and let it own the
   hero. Everything else is typography, spacing, and color. A page with four canvas
   effects reads as a demo reel, not a product.
2. **Ship a cohesive site, not a collection of effects.** The effect must serve real
   content — an actual product, an actual argument. If the page has nothing to say,
   the effect makes that louder, not better.
3. **Motion is a response, not decoration.** Canvas UI effects are pointer- and
   scroll-driven. Wire them to something the user did. Ambient loops with no input
   are noise.
4. **Never trade functionality for aesthetics.** Text stays selectable, links stay
   clickable, forms stay submittable, focus rings stay visible. If the effect breaks
   any of these, the effect loses.
5. **Avoid generic AI-generated look.** No purple-to-blue gradient hero, no floating
   glassmorphic cards on a mesh background, no emoji feature bullets. Commit to a
   specific typographic and color point of view.

## Workflow

1. **Read the content first.** Decide what the page is arguing before choosing an
   effect. Effect follows message.
2. **Pick one effect** from the table in [REFERENCE.md](REFERENCE.md), matched to
   tone — fluid/optical for calm and premium, glitch/retro for loud and technical,
   particle/3D for product showcases.
3. **Install it** from the registry (see Install).
4. **Build the page around it.** Layout, type scale, palette, and copy carry the
   design. The effect is the accent that makes it memorable.
5. **Verify the fallback path.** Load the page in a browser without the html-in-canvas
   flag and confirm it still looks intentional (see Browser support).
6. **Clear every guardrail** in the last section before calling it done.

## Install

Canvas UI is copy-in source via a shadcn registry, not an npm dependency:

```bash
npx shadcn@latest init                       # only if the project has no components.json
npx shadcn@latest add @canvas-ui/liquid-react
```

Swap `liquid` for any component in [REFERENCE.md](REFERENCE.md), and `react` for
`solid`, `preact`, `vue`, `svelte`, or `vanilla`. Files land in `components/canvasui/`
(Svelte: `src/lib/components/canvasui/`) and are yours to edit.

Most components wrap content rather than sit beside it:

```jsx
import { Liquid } from "@/components/canvasui/Liquid";

<Liquid intensity={2} distortion={0.4}>
  <Hero />
</Liquid>
```

## Browser support

The html-in-canvas components read the live DOM as a texture. That API needs Chrome
with a compatible html-in-canvas capability (check the installed version and current upstream requirements). On unsupported browsers they are intended to degrade to a **WebGL overlay** — the effect renders, but
it no longer distorts the page content. Check the selected component's WebGL/browser support rather than promising every browser works.

Design for the fallback as the default state. The flagged version is the upgrade.

## Guardrails

- Honor `prefers-reduced-motion` — the components already do; any motion you add
  checks it too.
- Keep the effect off the critical render path so first paint is text, not a blank canvas.
- On the vanilla path call `destroy()` on teardown or route change; the framework
  wrappers already destroy on unmount. Leaked WebGL contexts kill the tab.
- One WebGL context per page. Each additional canvas costs a context and a frame budget.
- Contrast is measured against the *rendered* result, not the CSS color underneath.
- License is MIT + Commons Clause: free to use in your own projects, commercial or not;
  you may not resell the library itself.
