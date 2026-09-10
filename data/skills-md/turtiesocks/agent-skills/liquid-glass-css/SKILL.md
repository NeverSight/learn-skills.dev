---
name: liquid-glass-css
description: Use when building translucent "liquid glass" or glassmorphism UI on the web with CSS — frosted/blurred panels, cards, navbars, buttons, or modals that blur and tint what's behind them. Triggers on `backdrop-filter`, `blur()`, frosted glass, translucent/acrylic surfaces, Apple-style or iOS-26-style glass on the web, dark dashboards with glowing ambient backgrounds, or porting an iOS Liquid Glass look to HTML/CSS/Tailwind. Covers vanilla CSS, Tailwind v4, and React. Trigger even if the user doesn't say "glassmorphism" — "frosted card", "blurry transparent panel", "glass navbar", "see-through blurred header" all qualify. Not for native iOS/SwiftUI (use `liquid-glass-design`).
---

# Liquid Glass on the web (CSS)

The web/CSS counterpart to the iOS **`liquid-glass-design`** skill. It teaches Apple's iOS 26 "Liquid Glass" look — translucent frosted panels that blur, tint, and refract what's behind them — built with **vanilla CSS, Tailwind v4, and React**. The reference aesthetic is a dark, warm, ambient-gradient dashboard where every surface is a pane of frosted glass floating over glowing background blobs.

The single most important idea, drilled throughout this skill:

> **Glass is a stack of optical layers, not one `backdrop-filter`.** The most common failure is doing only layer 1 (blur) and wondering why it looks flat and cheap. Real glass needs blur **and** tint **and** a light-catching rim **and** a specular highlight **and** inner depth **and** elevation.

Three more rules you will see repeated because they are the difference between shipping and breaking:

- **Always pair `-webkit-backdrop-filter` with `backdrop-filter`.** Safari (and old Edge) need the prefix. One without the other = no glass on a large slice of users.
- **Fallback-first.** Author a legible solid/translucent base, then *enhance* with `backdrop-filter` inside `@supports`. Browsers without the property must still show readable text, never white-on-transparent soup.
- **Don't glass everything.** `backdrop-filter` recomposites the layers beneath it. A page of 30 glass cards janks on mobile. Glass is a *highlight* material — heroes, nav, modals — not the default surface.

---

## When to use this skill

Use it whenever the work touches translucent/frosted surfaces on the web:

- "Build a frosted glass card / panel / navbar / modal / button"
- "Dark dashboard with glowing background and see-through panels"
- "Apple-style / iOS-26 / Liquid Glass look on my website"
- "Make this header blurry and see-through" / "acrylic / frosted surface"
- "Port my iOS Liquid Glass design to HTML/CSS" (the web half of the pair)
- "My `backdrop-filter` does nothing / looks wrong — why?"
- Anything mentioning `backdrop-filter`, `blur()`, glassmorphism, translucent/acrylic UI

If you're unsure, lean toward using it — the references are cheap and prevent the flat single-blur output that training-data drift produces.

## When NOT to use it

- **Native iOS / SwiftUI / UIKit / WidgetKit glass → use `liquid-glass-design`.** That skill owns `.glassEffect()`, `GlassEffectContainer`, `glassEffectID`, and the real Metal-backed material. This skill is the *web* port; it can only approximate the OS compositor in CSS. (Cross-link #1: the two are a deliberate pair — iOS ↔ web — discoverable from either side.)
- **Fully opaque UI.** If nothing shows through, you don't need glass; you need a normal card. Don't pay the compositing cost for a solid panel.
- **Where translucency would fail accessibility and no fallback is acceptable.** If text *must* sit on a busy backdrop at guaranteed WCAG contrast and you can't add a tint/scrim, use a solid surface. See `references/fallbacks-a11y.md`.

> The iOS skill and this one mirror each other section-for-section (material → levels → components → morphing → anti-patterns). If you've used `liquid-glass-design`, the map here will feel familiar — same model, CSS mechanisms instead of SwiftUI modifiers. (Cross-link #2.)

---

## The 6-layer optical model

Glass is built by stacking these layers. L1 lights up layers 1–3 + 6; L2 adds 4–5; L3 adds real refraction to layer 1. Memorize the table — it is the mental model the whole skill hangs on.

| # | Optical layer | What it does | CSS mechanism |
|---|---|---|---|
| 1 | **Backdrop** | blurs + saturates what's behind | `backdrop-filter: blur() saturate()` — `+ url(#glass-refract)` at L3 |
| 2 | **Body tint** | translucent color wash over the blur | translucent fill — flat at L1, top-lit gradient at L2/L3 |
| 3 | **Rim / edge** | the glass has a visible edge | hairline `border` (L1) → gradient light-catching border (L2/L3) |
| 4 | **Specular highlight** | top light glint, the "wet" look | `inset 0 1px 0` + a `::before` sheen gradient |
| 5 | **Inner depth** | the pane has thickness | `inset 0 -Npx` inner bottom shadow |
| 6 | **Elevation** | it floats off the page | outer `box-shadow` |

Layer 1 alone is what beginners ship. Layers 4–5 are what make it read as *glass* and not *a blurry box*. Layer 3 done wrong (invisible border) is the #1 reason glass disappears on light backgrounds.

---

## The three tiers — CSS → JS → WebGL

Fidelity (`L1/L2/L3`) is one axis; **dependency** is the other. Everything in this skill is **Tier 1 (pure CSS/SVG)** unless noted — drop it into a static page, no JS, no build. **Tier 2** adds JavaScript for what CSS can't do (react to pointer/gyro, sample the backdrop). **Tier 3** is a WebGL shader (cross-browser, real-time, native-grade — but a renderer). Pick the *lowest* tier that gets the look: fidelity is **not** monotonic with tier — the Tier-1 `.glass--apple` beats a bare Tier-2 glint. Full matrix + feature→tier map in `references/tiers.md`.

| Tier | Dependency | Highlights |
|---|---|---|
| **1** | pure CSS/SVG | L1–L3, `.glass--clear`, `.glass--fresnel`, `.glass--apple` (chromatic + specular ceiling), components, gooey merge |
| **2** | + JavaScript | `.glass--interactive` pointer specular, `useGlassTilt` (gyro/pointer glint), `useGlassVibrancy` (adapt to backdrop), `useGlassLens` map, matched-geometry morph |
| **3** | + WebGL | `createWebGLGlass` — per-frame shader refraction (reference) |

---

## Token schema

Every layer is a CSS custom property on `:root`. **Presets** change the *values*; **levels** change *how many layers are on*; **components** reuse the *same tokens* with different geometry. The channel trick — store the tint as raw `R G B`, then apply `/ alpha` per use — lets one tint value drive every translucent surface.

```css
:root {
  /* 1 backdrop  */  --glass-blur: 16px;            --glass-saturate: 140%;
  /* 2 body tint */  --glass-tint: 255 255 255;     --glass-tint-opacity: .08;
                     --glass-fill: rgb(var(--glass-tint) / var(--glass-tint-opacity));
  /* 3 rim       */  --glass-border: rgb(255 255 255 / .18);   --glass-radius: 18px;
  /* 4 highlight */  --glass-highlight: rgb(255 255 255 / .5);
  /* 5 inner     */  --glass-inner-shadow: rgb(0 0 0 / .18);
  /* 6 elevation */  --glass-shadow: 0 12px 40px rgb(0 0 0 / .45);

  /* pointer-tracking specular (set by JS on .glass--interactive) */
  --mx: 50%;  --my: 50%;
}
```

`assets/glass.css` is the **single source of truth** for these. Tailwind mirrors them (`--blur-glass`, `--color-glass-tint`, `--radius-glass`), React wraps the classes — nobody re-invents the look. Edit the values in one place and the whole system retunes.

---

## L1 recipe — baseline (production-safe, universal)

Layers 1, 2, 3, 6. Authored **fallback-first**: a legible base, then the glass enhancement guarded by `@supports`. This is the floor every glass surface starts from.

```css
.glass {
  position: relative;          /* anchor ::before/::after sheen */
  isolation: isolate;          /* contain the stacking context  */

  /* fallback: legible even with NO backdrop-filter support */
  background: rgb(var(--glass-tint) / .6);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow);
}

@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass {
    background: var(--glass-fill);               /* drop to translucent  */
    -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
    backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  }
}
```

`position: relative; isolation: isolate;` are **mandatory** on `.glass` — the sheen pseudo-elements anchor to it and the isolated stacking context keeps the backdrop blur from bleeding. Note `-webkit-backdrop-filter` is written **before** `backdrop-filter`, and the base `background` is the readable `.6` opacity, not the `.08` glass fill.

## L2 recipe — specular / "liquid" (pure CSS, cross-browser)

Stacks on `.glass`. Adds layers 4–5: a top-lit gradient fill, an inner highlight + inner depth shadow, and a `::before` sheen. No JS, no SVG — works everywhere `.glass` does.

```css
.glass--l2 {
  background:
    linear-gradient(135deg,
      rgb(var(--glass-tint) / .15),
      rgb(var(--glass-tint) / .04));
  box-shadow:
    var(--glass-shadow),                               /* 6 elevation     */
    inset 0 1px 0 var(--glass-highlight),              /* 4 top glint     */
    inset 0 -8px 22px var(--glass-inner-shadow);       /* 5 inner depth   */
}

.glass--l2::before {       /* sheen — pseudo, never blocks clicks */
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;              /* behind content — sheen never paints over it */
  border-radius: inherit;
  pointer-events: none;
  background: linear-gradient(158deg, var(--glass-highlight), transparent 36%);
  opacity: .55;
}
```

`pointer-events: none` on the sheen is not optional — without it the `::before` eats clicks on whatever it covers. The gradient-rim ("light-catching border") technique and L3 refraction live in `references/levels.md`.

```html
<!-- usage: levels stack on the base -->
<div class="glass glass--l2 glass-card">…</div>
<div class="glass glass--l2 glass--l3">…</div>   <!-- L3 = L2 + refraction -->
```

---

## Which level? (decision flowchart)

The level/fallback choice is the one genuinely non-obvious call — everything else is "pick a component and a preset." Use this:

```
Is this a hero / signature surface (one or two on the page)?
│
├─ NO  → L1 or L2. Use L2 for any visible card; L1 for tiny chips/pills
│        where the specular cost isn't worth it. Never L3 on repeated cards.
│
└─ YES → Do you want real backdrop *refraction* (lensing), not just blur?
         │
         ├─ NO  → L2. Specular + depth is the "liquid" look 95% of the time.
         │
         └─ YES → L3.  Then ask: which browsers must look right?
                  │
                  ├─ Chromium-only / progressive-enhancement OK
                  │      → ship L3. Safari/Firefox ignore url(#glass-refract)
                  │        and degrade to L2 blur automatically — no breakage.
                  │
                  └─ Must look identical cross-browser
                         → use L2. L3's feDisplacementMap refraction is
                           Chromium-leaning; don't promise it on Safari/FF.

ALWAYS, regardless of level:
  • fallback-first base (legible with no backdrop-filter)   → @supports
  • -webkit-backdrop-filter paired with backdrop-filter
  • glass-on-LIGHT background? → darken --glass-border (light rims vanish)
```

**Glass-on-light is the classic gotcha.** White-ish rims and highlights disappear over a light backdrop. Switch to `[data-glass-theme="light"]`, which darkens `--glass-border` and softens the shadow. Details in `references/levels.md` and the light preset in `references/components.md`.

---

## Quick reference — levels

| Level | Class stack | Layers on | Tech | Use for |
|---|---|---|---|---|
| **L1** | `.glass` | 1,2,3,6 | `backdrop-filter` + `@supports` | universal baseline, tiny chips |
| **L2** | `.glass .glass--l2` | + 4,5 | pure CSS gradients + insets + `::before` | default for any visible card/panel |
| **L3** | `.glass .glass--l2 .glass--l3` | + refracted 1 | SVG `feTurbulence` displacement (`#glass-refract`) | hero panels only; degrades to L2 off-Chromium |
| **L3 · apple** | `.glass .glass--clear .glass--apple .glass--fresnel` | + chromatic + specular | gradient map + chromatic aberration + `feSpecularLighting` | **Tier-1 refraction ceiling** — most Apple-accurate *without JS*; one hero element, heavy, Chromium-only |

**Apple-accurate recipe** (vs 2020-era glassmorphism, which over-blurs): **less** blur, more refraction, a bright bezel, over **rich** content (Apple glass reflects the wallpaper — a flat backdrop hides it). The **Tier-1 ceiling** is `.glass--clear .glass--apple .glass--fresnel`: `--clear` thins the frost so light bends instead of scattering (Apple's "clear" variant — it needs a dimming layer under it for legibility); `--apple` adds no-JS gradient-map barrel refraction + real chromatic aberration + a `feSpecularLighting` glint; `--fresnel` adds the bright rim. Two SVG filters, Chromium-only, heavy — one hero element. Full breakdown in `references/levels.md` (*Pure CSS/SVG ceiling*); live in `assets/demo.html`.

> **Tier-2 footnote — `.glass--lens`.** A JS-generated (canvas) corner-accurate SDF displacement map, via `useGlassLens` / `makeDisplacementMap`. Only reach for it when `.glass--apple`'s rectangular barrel isn't accurate enough at the corners — otherwise prefer the Tier-1 `--apple`. See `references/levels.md` and `references/tiers.md`.

**Adaptive vibrancy** (glass lightens over dark content / darkens over light) is the one trait pure CSS can't do — it needs JS to sample the backdrop (Tier 2). For the native iOS/SwiftUI material itself, see the `liquid-glass-design` skill.

## Quick reference — components

Same tokens, different geometry + state. Each maps to an iOS-skill twin. Full CSS in `references/components.md`.

| Class | Shape / role | iOS twin | Notes |
|---|---|---|---|
| `.glass-card` | radius-xl padded panel | card / container | stat & chart panels |
| `.glass-button` | capsule, interactive | `.buttonStyle(.glass)` | `:hover` brighten, `:active` scale(.98) |
| `.glass-button--prominent` | filled accent button | `.glassProminent` | tinted, higher contrast |
| `.glass-nav` | sticky topbar / toolbar | toolbar | stronger blur, thin bottom rim |
| `.glass-pill` | small capsule | — | nav items, tags |
| `.glass-badge` | tiny status capsule | — | `$12.4K`, "Total Pending" chip |
| `.glass-modal` + `.glass-scrim` | centered panel + blurred backdrop | sheet | scrim carries its own blur; fixed-position |
| `.glass--interactive` | opt-in pointer specular | `.interactive()` | reads `--mx/--my`; costs a little JS |
| `.glass-goo` | gooey-merge container | gooey morph | uses `#glass-goo`; advanced, see `morphing.md` |

## Quick reference — presets

Override the token block on a `data-` attribute; nothing else changes. **`dark` is the `:root` default** (no attribute needed).

| Attribute | Vibe | Key retune |
|---|---|---|
| *(none)* / `[data-glass-theme="dark"]` | hero — low-opacity white tint, bright highlights | the defaults; pair with a warm ambient bg |
| `[data-glass-theme="light"]` | glass on light pages (the hard case) | denser white tint + **darker rim** (the #1 light-glass fix) + softer shadow + less saturate |
| `[data-glass-theme="tinted"]` | colored glass (maps iOS `.tint()`) | e.g. `--glass-tint: 255 122 26` for orange |

---

## Deep dive →

Load only what the task needs — these are heavy.

| If you need… | Read |
|---|---|
| The CSS → JS → WebGL **tier model**, the Level × Tier axes, the feature→tier map, which tier to pick | `references/tiers.md` |
| L1/L2/L3 in full, the `#glass-refract` filter, the `.glass--apple` pure-CSS/SVG ceiling, gradient-rim, browser-support matrix, fallback chain | `references/levels.md` |
| Full CSS for all 5 components + every interaction state, modal + scrim + fixed-position note, prominent button | `references/components.md` |
| Tailwind v4: `@theme` tokens, `@utility glass`, vanilla→utility class-mapping table, L3 arbitrary-value note | `references/tailwind-v4.md` |
| React: `<GlassCard>/<GlassButton>/<GlassPanel>/<GlassModal>`, all hooks (`useGlassPointer`, `useGlassTilt`, `useGlassVibrancy`, `useGlassLens`, `useGlassMorphTransition`), `<GlassFilter>`, SSR/Next.js notes | `references/react.md` |
| Morphing: matched-geometry (framer-motion `layoutId` / vanilla FLIP), gooey merge (`#glass-goo`), shader morph | `references/morphing.md` |
| `@supports` patterns, `prefers-reduced-transparency`/`-motion`/`-contrast`, contrast-on-glass (WCAG), perf, "don't glass everything" | `references/fallbacks-a11y.md` |

Copy-paste artifacts in `assets/`:

| Want a… | Copy from |
|---|---|
| Drop-in stylesheet (tokens + 3 presets + L1–L3 + components + fallbacks) | `assets/glass.css` |
| Self-contained live demo (all tiers — refraction, vibrancy, WebGL, morph) | `assets/demo.html` |
| Typed React components + every hook + `<GlassFilter>` | `assets/Glass.tsx` |
| **Tier 2** — backdrop-luminance vibrancy sampler (`.js` + `.d.ts`) | `assets/glass-vibrancy.js` |
| **Tier 2** — canvas SDF displacement-map generator for `.glass--lens` | `assets/displacement-map.js` |
| **Tier 3** — WebGL reference: per-frame shader refraction | `assets/glass-webgl.js` |

---

## Working autonomously

1. **Pick the level first** (flowchart above), then the component, then the preset. Most tasks are L2 + a component class + the dark default.
2. **Start from `assets/glass.css`** — it's the source of truth. Don't hand-roll the material from memory; you'll forget `-webkit-`, the fallback, or the specular.
3. **Verify in `assets/demo.html`.** Open it standalone, confirm the glass actually renders (blur + tint + specular) and the console is clean before wiring into a real app.
4. **Set a backdrop.** Glass over a flat color looks like nothing — it needs something behind it (an ambient gradient, an image, content). The dark preset assumes a warm glowing background.
5. **Audit count and contrast before shipping.** Count your glass surfaces (don't glass everything) and check text contrast over busy backdrops (`references/fallbacks-a11y.md`).
6. **Suggest a commit at natural break points** — material in, components in, theme switched — per the user's commit preferences.
