---
name: liquid-glass
description: >
  Apple Liquid Glass (iOS/iPadOS/macOS 26–27, WWDC25/26): how the material is really built
  (Apple Figma kit effect stacks, Core Animation glassBackground parameters), design rules
  (regular / clear / tinted / identity, the iOS 27 transparency slider, where to put colour,
  glass-on-glass, vibrancy, accessibility), native SwiftUI/UIKit/AppKit APIs (glassEffect,
  GlassEffectContainer, glassEffectID/Union, UIGlassEffect, NSGlassEffectView), GPU shader
  recreation (WGSL/WebGPU, GLSL, Metal, three.js: squircle bevel refraction, dispersion, frost
  pyramid, SDF liquid merging, rim light), Apple-style spring motion, and the Liquid Rust
  engine (Rust + wgpu, native and WebGPU/wasm). Use for any request about Liquid Glass, glass
  UI, "the iOS 26 glass look", glassEffect, Figma glass effect parameters, glass shaders,
  liquid/metaball merging of UI shapes, or picking glass vs fill vs tint colours.
---

# Liquid Glass

Liquid Glass is a **lensing** material for the functional layer: bars, buttons, menus and
sheets floating above content. It bends light through a curved edge, compresses the
backdrop's contrast, lights its rim, and merges with neighbouring glass like liquid. It is
**not** glassmorphism (big blur plus a white fill).

## Pick the path

| You are building | Do | Read |
|---|---|---|
| A native Apple app | Use the system API. Never hand-roll shaders there | `references/native-apple.md` |
| A web page | Liquid Rust compiled to wasm (WebGPU); raw WebGPU with `assets/*.wgsl`; CSS fallback | `references/webgpu.md` |
| Rust (any GPU / UI stack) | the Liquid Rust crate | `references/liquid-rust.md` |
| Any other engine (Unity, Godot, Metal, GL) | port `assets/glass.wgsl` | `references/shader-math.md` |
| A design / Figma file | the kit layer recipe | `references/anatomy.md` §2 |
| Motion, physics, interaction | analytic springs, choreography | `references/motion.md` |
| "Is this right?" reviews | rules + checklist | `references/design-rules.md`, `anatomy.md` §5 |

Always read `design-rules.md` before deciding colours or stacking.

## Presets

| Preset | Apple API | Use | Kit numbers (Figma GLASS) |
|---|---|---|---|
| **Regular** | `.regular` | Default: bars, buttons, menus, anything with text. Adaptive | frost 10–16, refraction 70, depth 30, dispersion 20, splay 20, light 25–30 % |
| **Clear** | `.clear` | Only over media; needs 35 % dimming when the media is bright | frost 6, refraction 70, depth 30, dispersion 20, splay 20, light 40 %; fill `#101010` dodge + white 4 % luminosity |
| **Tinted** | `.regular.tint(c)` / `.glassProminent` | The **one** primary action on screen | stained glass: hue from the tint, lightness from the backdrop |
| Identity | `.identity` | Transition endpoint | nothing |

There is also a user-level setting. iOS 26.1 had a **Clear | Tinted** switch; iOS 27 replaced
it with a **slider from ultra clear to fully tinted**. Native apps get it for free. Custom
renderers should expose a 0…1 knob for it.

## Colour: shape or icon?

- **Primary action:** tint the glass **background**, white label. One per screen.
- **Toggle state inside a glass panel:** a solid system-colour circle (e.g. `#0088FF`) behind
  a white glyph. Not glass.
- **Meaning of a value** (brightness, volume): colour the **glyph**, keep the glass neutral.
- **Bars over colourful content:** monochrome glyphs that flip black/white with the glass.
- Brand colour goes in the content layer. Never tint every button, and never put a solid
  opaque fill on glass.

## Layering: glass on glass?

**No.** Elements on glass are fills with vibrancy blend modes. The kit's sub-buttons are
`#111 luminosity 60 %` + `#777 color-dodge` + `#222 linear-dodge`. Glass siblings share one
container, which merges them and renders them in one pass.

Unavoidable stacking (a sheet over a toolbar):
- the upper glass must be Regular;
- it must sample the *rendered* lower glass, which Liquid Rust does by rebuilding the backdrop only
  where the layers overlap.

## Non-negotiables for an Apple-grade look

1. **Refraction band:** a squircle bevel about 30 pt wide, Snell η 1.5. The centre stays flat
   and colour-clean.
2. **Small frost:** σ = Frost / 2. Calibrate the blur, or the result reads as plastic.
3. **Luminance compression, not a white overlay:** Figma fills applied in sRGB space.
4. **Crisp lit rim line:** about 0.25 pt, brightest facing the light, about 40 % on the opposite
   edge, splay on the flanks, plus soft inner rims. **iOS 27:** a dark 0.5 pt outer hairline.
5. **Liquid merge** through an SDF smooth union with k = container spacing. Never collision physics.
6. **Motion:** analytic springs (`duration`/`bounce`) that are retargetable and keep velocity.
   Press grows the glass and lights it from the finger. Release bounces. Glass materializes
   through lensing, never an alpha fade.
7. **Adaptivity:** small glass flips light/dark; big glass is thicker; shadows follow the
   content behind.
8. **Accessibility:** Reduce Transparency, Increase Contrast and Reduce Motion, and the slider.
9. **Render on demand:** idle at 0 fps when nothing moves; cache the blurred backdrop.
10. **Squircle corners:** continuous curvature (Figma smoothing 60 %) on every rounded glass
    panel and on the fills sitting on it. Circles and capsules stay round. See `anatomy.md` §2.7
    for where Apple uses them; the superellipse SDF is in `shader-math.md` §1.

## Quick starts

```swift
// SwiftUI
GlassEffectContainer(spacing: 16) {
    HStack(spacing: 12) {
        Button("Edit") {}.buttonStyle(.glass)
        Button("Done") {}.buttonStyle(.glassProminent)
    }
}
```

```rust
// Liquid Rust (native or wasm)
let bar = scene.add_container(14.0, 0);
scene.add(Glass::new(Rect::new(24.0, 24.0, 52.0, 52.0)).interactive().container(bar));
if scene.update(dt) { /* keep requesting frames */ }
renderer.render(&device, &queue, &mut encoder, &Frame { content, target, size, scale, content_changed }, &scene);
```

```js
// Web via wasm (LiquidRust/web)
const glass = await LiquidGlass.create(canvas, imageBitmap, devicePixelRatio);
glass.add(24, 24, 52, 52, -1, "regular", 0, true, false, -1, 0);
```

## Files

- `references/anatomy.md`: the layer stack and exact kit/compositor numbers; the look checklist
- `references/design-rules.md`: variants, colour, layering, legibility, accessibility, anti-patterns
- `references/native-apple.md`: SwiftUI, UIKit and AppKit APIs including SDK 27; migration
- `references/shader-math.md`: the full algorithm with calibration constants and a bug table
- `references/webgpu.md`: browser paths, backdrop capture (HTML-in-Canvas), buffer layouts, CSS fallback
- `references/motion.md`: the spring maths (copy-ready), choreography values, frame pacing
- `references/liquid-rust.md`: engine API, recipes, what it fixes vs naive copies
- `references/sources.md`: what each claim rests on
- `assets/glass.wgsl`, `assets/pyramid.wgsl`: tested shaders (WebGPU / wgpu)
