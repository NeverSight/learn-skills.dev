---
name: superimg
description: >
  This skill should be used when the user asks to "create a video template",
  "animate with SuperImg", "render HTML to MP4", "use defineScene", "work with
  ctx.std", or mentions SuperImg, video generation, or programmatic video.
  Provides the SuperImg framework for HTML/CSS templates rendered to video.
---

# SuperImg Skill

## Mental Model

Video is a pure function of time. Your template's `render(ctx)` is called once per frame. It receives a `RenderContext` and returns an HTML string. All animation is derived from `sceneProgress` (0→1 over the scene) or `sceneTimeSeconds` (elapsed seconds). Use `std.tween` as the canonical animation primitive. Data comes from `defaults`, merged with per-scene overrides. No timeline editor, no keyframes — just math and HTML.

## Quick Start

```typescript
import { defineScene } from "superimg";

export default defineScene({
  defaults: { message: "Hello!", accentColor: "#667eea" },
  config: {
    durationSeconds: 3,
    inlineCss: ["* { margin: 0; box-sizing: border-box; } body { background: #0f0f23; font-family: system-ui; }"],
  },
  render(ctx) {
    const { std, sceneTimeSeconds: time, width, height, data } = ctx;
    const progress = std.math.clamp(time / 1.0, 0, 1);
    const opacity = std.tween(0, 1, progress, "easeOutCubic");
    const y = std.tween(30, 0, progress, "easeOutCubic");
    return `
      <div style="${std.css({ width, height })};${std.css.center()}">
        <div style="${std.css({ opacity, transform: "translateY(" + y + "px)", color: data.accentColor, fontSize: 64 })}">${data.message}</div>
      </div>
    `;
  },
});
```

## Key Context Fields

Use these from `ctx`: `sceneProgress`, `sceneTimeSeconds`, `sceneDurationSeconds`, `width`, `height`, `isPortrait`, `data`, `std`. Ignore `globalProgress` for scene animation — use `sceneProgress` or `sceneTimeSeconds` instead.

## Core Patterns

**Phase timing (enter/hold/exit):**
```typescript
const enterProgress = std.math.clamp(time / 1.0, 0, 1);
const exitProgress = std.math.clamp((time - 3.0) / 1.0, 0, 1);
const opacity = std.tween(0, 1, enterProgress, "easeOutCubic") * (1 - exitProgress);
```

**Phase sequence (no manual clamp):**
```typescript
const phases = std.timing.sequence({
  enter: { duration: 0.8, render: (p) => card(std.tween(0, 1, p, "easeOutCubic")) },
  hold: { duration: 2, render: () => card(1) },
  exit: { duration: 0.8, render: (p) => card(std.tween(1, 0, p, "easeInCubic")) },
});
return phases.render(time);
```

**Animated counter:** `Math.floor(std.tween(0, value, progress, "easeOutCubic"))`

**Layout:** `std.css({ width, height })`, `std.css.center()`, `std.css.fill()`, `std.css.stack()`

**Color:** `std.color.alpha(color, 0.5)`, `std.color.mix(c1, c2, t)`

## Stdlib Cheat Sheet

- `std.tween(from, to, progress, "easeOutCubic")` — canonical animation
- `std.math.clamp`, `std.math.map`
- `std.color.alpha`, `std.color.mix`, `std.color.lighten`, `std.color.darken`
- `std.css(obj)` — object → inline style string
- `std.timing.sequence({ enter, hold, exit })` — phase manager

## Do / Don't

**DO:** Use `sceneProgress` or `sceneTimeSeconds` for animation. Put shared CSS in `config.inlineCss`. Use `config.fonts` for Google Fonts. Set root element to `width: ${width}px; height: ${height}px`. Use `std.css()` for inline styles. Import from `"superimg"` in templates.

**DON'T:** Return JSX — return template literal strings. Mutate state in render — keep it pure. Use `globalProgress` for scene animation. Import from `"superimg/server"` in templates. Use `@import url()` for fonts — use `config.fonts`.

## Config

`defineScene` config: `width`, `height`, `fps`, `durationSeconds`, `fonts`, `inlineCss`, `stylesheets`, `outputs`. Precedence: CLI flags > template config > `_config.ts` (cascading) > built-in defaults. Use `defineConfig` in `_config.ts` for project-wide settings.

## CLI

```bash
superimg init my-project
superimg init .                    # Add to existing project
superimg dev intro
superimg render videos/intro.ts -o output.mp4
superimg list
superimg info videos/intro.ts
superimg setup
superimg add skill
```

## Server API

```typescript
import { renderVideo, loadTemplate } from "superimg/server";
const t = await loadTemplate("videos/intro.ts");
await renderVideo("videos/intro.ts", { outputPath: "out.mp4", width: 1920, height: 1080 });
```

## Additional Resources

For detailed API documentation and working examples, consult:

### Reference Files
- **[references/api.md](references/api.md)** — Complete RenderContext interface, all std.tween easings, full std.math/color/css/timing APIs, config options

### Example Files
- **[examples/hello-world.ts](examples/hello-world.ts)** — Minimal template demonstrating core concepts
- **[examples/stats-card.ts](examples/stats-card.ts)** — Advanced template with phase timing, animated counters, responsive sizing

### Project Examples
See `examples/templates/` in the SuperImg repo for full templates: `lower-thirds`, `stats-card`, `phase-demo`, `countdown`.
