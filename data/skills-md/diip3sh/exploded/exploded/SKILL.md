---
name: exploded
description: Turn a real, rendered UI component (button, input, switch, card, menu, dialog, any React/Vue/HTML component) into a live, interactive exploded spec sheet. The component is pulled apart in isometric into its paint layers (elevation, surface, stroke, inner surfaces, content, focus ring), every state (hover, focus, pressed, disabled, invalid, on/off) can be switched, and every measurement (padding, radius, gap, type, shadow, ring) plus the design token the author actually wrote is read from the browser, never typed. Use this whenever someone wants component documentation, a design-system or Storybook page, a "spec sheet", redlines, an anatomy or breakdown of a component, an exploded or layered view of UI, a visual handoff doc, or an interactive explainer of how a component is built, even if they never say "exploded". Works framework-free (one script and one stylesheet) and in React/Next.js through a wrapper component.
---

# Exploded

This skill makes figures that take a real component apart. It floats over a cutting mat as a stack of glass sheets. Each sheet carries one kind of paint: the shadow it casts, its fill, its stroke, the chips and thumbs inside it, its text and icons, and its focus ring. Hover the figure and the stack opens. Hover a sheet and its measurements are printed on it in redline. Press 1–5 and the component changes state, and the sheets change with it. The real component sits beside the figure, live, and hovering or focusing it drives the figure.

One complete example ships with the skill: `examples/gallery/index.html`, which has four figures (a primary button with an icon and a shortcut chip, an email field, a switch and a review card). Open it before you start. Serve the folder (`python3 -m http.server`) or open the file directly.

## The one idea that matters

**Nothing is redrawn, and no number is typed.** Every sheet is the real component, cloned with the browser's own computed styles, with every paint that belongs to another sheet made transparent. Every number on a sheet or in the readout comes from `getComputedStyle`, layout boxes and text ranges. Every token name comes from the CSS rule the author actually wrote.

A spec sheet fails in two ways:

- **Mockup.** The component is redrawn as SVG shapes or boxes. It drifts from what ships on the first refactor, and nobody notices.
- **Annotated screenshot.** One flat image with arrows. It has no layers and no states, and it can't answer "what does focus add?"

The runtime avoids both by construction. Your job is to give it the real component in its real states, name what it finds, and prove the result.

If a number is wrong in the figure, the figure is not the problem: the component, the state or the harness is. **Never patch the figure, and never edit the component to make the figure look better.** Fix the harness or report what you found.

## Workflow

1. **Size it, before anything else.** Tell the user which size this is.
   - **Figure**: one component with up to about 6 states. 15–40 minutes. Build it without asking.
   - **Sheet**: a component and its variants (sizes, intents), or 3–6 related components on one page. 1–2 hours. Say so, then build it.
   - **System**: a whole library, wired into a docs site or Storybook with one figure per component. Half a day or more. Don't start it. Propose a Sheet for the 3–5 most-used components first, and list what the full version would add.
2. **Find the truth.** Read the component's source before you render it. Write down:
   - its real states, from its API and its CSS: props (`disabled`, `checked`, `variant`), data attributes (`data-state="open"`), ARIA (`aria-invalid`, `aria-checked`) and pseudo-classes (`:hover`, `:focus-visible`, `:active`, `:focus-within`). Don't invent states it doesn't have, and don't skip states it does have.
   - where its tokens live (CSS variables, a Tailwind theme, a tokens file), so you can check what the T mode shows.
   - the width it really renders at in production (`specimenWidth`), when it is fluid.
3. **Render it in a harness.** The runtime needs the component live in a page, with its CSS readable from the same origin:
   - **React/Next.js:** a docs route or MDX page that renders `<Exploded>` around the real component. See `references/react.md`.
   - **Storybook:** a story that renders the wrapper. See `references/harness.md`.
   - **Plain HTML or any other stack:** a static page with the component's markup and its compiled CSS inlined or served from the same origin, like the gallery example.
   - Fonts must be loaded before mounting (`document.fonts.ready`). The wrapper waits for you.
4. **Mount once with defaults, then read the plan.** Call `figure.model()` (or read the margin) and look at the stack the runtime found: layer names, and a summary of each layer in each state. Then name things:
   - Name inner surfaces by what they are, not by their DOM: `parts: { ".btn-kbd": "Shortcut chip", ".thumb": "Thumb" }`, or `data-xp-name="Thumb"` on the element.
   - Choose `splitStroke`: `"root"` (default: the outer stroke gets its own sheet), `"all"` (every stroke gets its own sheet, for inputs and outlined components) or `"none"`.
   - Mark anything that isn't part of the component with `data-xp-ignore`.
5. **States.** Use a preset or write the real ones. `"pressable"` and `"field"` force CSS pseudo-classes. `"pointer"` also fires real pointer and mouse events, for components whose hover and press come from their own handlers (React state, motion, springs) rather than CSS `:hover`. Each state is any mix of `pseudo` (forced without a pointer), `attrs` (set on the state target, or on `on: "selector"`) and `apply(root, target)` (any setup, returning an undo function). Every state is captured once it has settled: nothing that paints has changed for two frames (budget `settle`, 3000 ms). Never type a state's values by hand: drive the component and let it paint. Check in `model()` that every state really differs from rest: a state that reads the same as rest means the selector didn't apply (see Limits).
6. **Frame it.** `fig` number, a short `title` ("Button · primary"), and a `theme` that matches the host page. The hint, readout and margin keys are written for you.
7. **Verify like a critic.** Run `node scripts/audit.mjs <page> --out shots`. It finds Chrome, Chromium, Edge, Brave or Aside (set `CHROME_PATH` for anything else). It must end with `passed`: every figure's audit passed, every state's pixels match the live component, and no page errors. Read every `⚠` line: they mark what the sheets can't show exactly (see Limits). Then read every PNG it writes, apart and together, and check the list in `references/verify.md`. Fix and repeat until there's nothing left to fix.

## Mount options

```js
const figure = await Exploded.mount(hostElement, {   // resolves once every state is captured
  target,                 // the live component's root element (required)
  title: "Button · primary",
  fig: 1,
  states: "pressable",    // "pressable" | "pointer" | "field" | [{ id, label, pseudo?, attrs?, on?, apply? }]
  stateTarget: "input",   // selector inside target that takes the states (default: target)
  parts: { ".thumb": "Thumb" },
  splitStroke: "root",    // "root" | "all" | "none"
  theme: "light",         // "light" | "dark"
  specimenWidth: 320,     // width of the live slot, for fluid components
  azimuth: -38, tilt: 56, // camera: turn and look-down angle in degrees
  stack: 0.42,            // share of the card's height the open stack may use
  maxGap: 84, maxScale: 5,
  tokens: true,           // set false to skip token tracing on very large pages
  settle: 3000,           // ms each state may take to settle before it's captured
});
figure.setState(2); figure.apart(true); figure.setActive(1); figure.tokens(true); figure.turn(-50, 60);
figure.model();   // [{ state, w, h, settled, layers: [{ key, name, summary }] }]
figure.audit();   // { ok, checked, problems }
figure.pose(i);   // puts the live component in state i; resolves to an async undo (used by the audit)
figure.composite(i); // state i's sheets stacked flat at zoom 1 (used by the audit's pixel check)
figure.destroy(); // puts the component back where it was
```

Keyboard on a focused figure: `1`–`9` states, `E` apart or together, `↑ ↓` select a layer (↑ starts at the bottom and climbs), `← →` turn, `T` tokens or pixels, `Esc` reset. Drag turns it. Hover opens it.

## How the stack is decided

The runtime finds the stack itself. Know the rules so you can explain what you see:

- **Elevation** holds every outer shadow with a blur or an offset.
- **Surface n** holds fills (background colour, gradient, inset shadow, backdrop filter) at paint depth n. Depth counts how many filled ancestors an element has inside the component, so a chip inside a button is Surface 2. A part named in `parts` at the top level gets its own sheet (a button's base and its cap); deeper named parts share their depth's sheet.
- **Stroke** holds borders, at the root (or at every depth with `splitStroke: "all"`), and edges: spread-only shadows that are already there at rest (an outline drawn with `box-shadow: 0 0 0 1px`).
- **Content** holds text, icons, images, and a control's value and placeholder. Each `::before` and `::after` becomes a real element, so it lands on the right sheet too.
- **Focus ring** holds outlines, and ring shadows (no blur, no offset, only spread) that appear only in a state.
- The stack is the union over all states, so it never changes shape. A sheet with nothing on it in the current state is drawn dashed: the focus ring waits, empty, at rest.
- Closed, the figure shows the component whole, so it matches the real thing exactly (a disabled state's group opacity included). It hands over to the sheets as they open.
- Summaries name every part's fill, and its offset when it moves (`shifted -1, 11`, or `z 8` in 3D), so a press that only moves something still reads.
- The specimen inherits the font and colour of the place it was mounted from, not the figure's, so a component that inherits its typography is measured as it ships.
- When light paint would vanish on a light sheet (white text, a translucent chip), the sheet gets a backing: the surface that paint really sits on in the component, in its own shape and colour. The paint stays true.

## Craft rules

- **The component's own colours are never touched.** The only colour the figure adds is the redline accent (`--xp-lit`), and only on the active sheet.
- **Layer names describe paint, not markup.** Write "Shortcut chip", "Thumb", "Avatar", never "span.btn-kbd" or "div".
- **Labels are a fixed size on screen** (8.5 px), never sit on the glyphs they measure, and are dropped rather than stacked when there's no room. If a dense component loses labels you need, split it into two figures (the header and the body of a card) rather than shrinking text.
- **The readout is live.** It reads `state · layer · values` from the model, and in T mode it reads the tokens the author wrote.
- **The specimen stays live.** Never screenshot it or replace it: hovering, pressing and focusing the real component drives the figure.
- **One figure, one component.** Variants (sizes, intents) are separate figures on the same page with the same camera, so they compare.
- **Match the host page.** Use the light theme on light docs and the dark theme on dark docs, and keep `--xp-sans` on the host's font.

## Limits (v0.1)

Say these to the user when they apply. Don't work around them silently.

- **Cross-origin stylesheets** (a CDN or another port) can't be read. Their `:hover`/`:focus` rules can't be forced, and their tokens can't be traced. Serve the CSS from the same origin, or use `attrs` and `apply` states.
- **Shadow DOM** (web components) isn't captured. Mount on a light-DOM wrapper, or render the component's light-DOM equivalent.
- **Canvas** pixels are copied once per state (2D and WebGL; WebGL right after the page draws its frame). **Video** clones without its pixels.
- **Transitions and animations** are captured at their settled end. The figure shows states, not motion. A component that never settles (a render loop, a drifting cursor) is captured at one moment, and the audit marks it `⚠ never settled`.
- **3D components** (`preserve-3d`) keep their 3D inside each sheet, but sheets are stacked by kind of paint, not depth, so a deep edge can paint over a face that sits above it. The closed figure is exact; the audit marks the sheets `⚠ 3D`.
- **Group opacity or filters on inner elements** apply per sheet, not to the group, so a faded inner part can look washed out when apart. On the root it's exact.
- **Token tracing** finds the winning declaration for a property family, and for shorthands with several values (`padding: 0 calc(var(--spacing) * 2.5) 0 …`) it reports the first token. Pixel values are always exact.
- **`!important` author rules** can beat the frozen clone's inline styles. If the audit passes but a sheet looks wrong, look for them.

## Files

| File | Use it for |
|---|---|
| `runtime/exploded.js` | The whole runtime as one classic script: capture, layer planning, painting, the 3D stage, motion, input and the audit. Exposes `window.Exploded`. |
| `runtime/exploded.css` | The figure's styles and both themes. Tokens are `--xp-*`. |
| `runtime/react/Exploded.tsx` | The React/Next.js wrapper. It waits for fonts, mounts on the child, and puts the child back on unmount. |
| `scripts/audit.mjs` | Headless Chrome with no dependencies: the stack per state, the audit, and PNGs apart and together. |
| `examples/gallery/` | Four figures: button, field, switch and card. |
| `references/harness.md` | Getting a component onto a page the runtime can read: Next.js, Storybook, Vite, plain HTML. |
| `references/react.md` | The wrapper, server/client boundaries and re-mounting. |
| `references/verify.md` | The review checklist and the faults to look for. |
