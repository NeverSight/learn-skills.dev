---
name: remotion-video
description: "Remotion video production best practices — spring animations, interpolation patterns, SVG draw-on effects, scene transitions, chart animations, audio integration, and rendering. Use when building programmatic videos with Remotion, creating animated content, or producing marketing videos with code."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: creative
  domain: video
  updated: 2026-03-13
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Remotion Video Production

Best practices for building programmatic videos with Remotion — animations, transitions, charts, and rendering.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/remotion-video ~/.claude/skills/
```

## Core Capabilities

- Spring animation presets (bouncy, smooth, crisp, staggered)
- Interpolation patterns (camera zoom, parallax, scroll simulation)
- SVG draw-on animations (path tracing, stroke reveal)
- Scene transitions via TransitionSeries
- AbsoluteFill layering for compositing
- Chart animations (bar grow, line draw-on, pie reveal, count-up numbers)
- Audio integration and sync
- Rendering configuration

## Spring Presets

Use `spring()` from Remotion for physics-based animations:

| Preset | Config | Use Case |
|--------|--------|----------|
| Bouncy | `mass: 0.5, damping: 8, stiffness: 120` | Playful reveals, logo bounces |
| Smooth | `mass: 1, damping: 15, stiffness: 80` | UI transitions, slide-ins |
| Crisp | `mass: 0.8, damping: 20, stiffness: 200` | Snappy interactions, toggles |
| Staggered | Any preset with frame offset per item | List reveals, grid animations |

```tsx
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
  config: { mass: 0.5, damping: 8, stiffness: 120 },
});
```

## Interpolation Patterns

### Camera Zoom

```tsx
import { interpolate } from "remotion";

const zoom = interpolate(frame, [0, 30], [1, 1.5], {
  extrapolateRight: "clamp",
});
```

### Parallax Layers

```tsx
const bgX = interpolate(frame, [0, 100], [0, -50]);
const fgX = interpolate(frame, [0, 100], [0, -150]);
```

### Scroll Simulation

```tsx
const scrollY = interpolate(frame, [0, 90], [0, -800], {
  extrapolateRight: "clamp",
});
```

## SVG Draw-On

Animate `strokeDashoffset` to reveal SVG paths:

```tsx
const pathLength = 500;
const draw = interpolate(frame, [0, 60], [pathLength, 0], {
  extrapolateRight: "clamp",
});

<path
  d="..."
  strokeDasharray={pathLength}
  strokeDashoffset={draw}
/>
```

## Chart Animation Patterns

| Pattern | Technique |
|---------|-----------|
| Bar grow | Animate height from 0 to target, stagger each bar by 3-5 frames |
| Line draw-on | SVG path with strokeDashoffset animation |
| Pie/donut reveal | Animate conic-gradient stop or SVG arc path |
| Count-up numbers | Interpolate from 0 to target, `Math.round()` for display |

## Scene Transitions

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneOne />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    timing={linearTiming({ durationInFrames: 15 })}
    presentation={fade()}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneTwo />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

## Performance Rules

1. **No `useEffect` for animations.** Use `useCurrentFrame()` + `interpolate()`.
2. **Memoize static components.** `React.memo` for anything that does not depend on frame.
3. **Preload assets.** `staticFile()` for local, `prefetch()` for remote URLs.
4. **Keep compositions under 30s** for fast render iteration during development.
5. **Test at target resolution** (1920x1080 or 1080x1080) before final render.

## Anti-Patterns

- No CSS `transition` or `animation` — use Remotion `interpolate()` and `spring()`
- No `setTimeout` or `setInterval` — frame-based timing only
- No absolute pixel positioning for responsive layouts — use `AbsoluteFill` + flex
- No inline `style` objects recreated every frame — extract to constants or `useMemo`
- No uncontrolled audio — always set explicit `volume` and `startFrom`

For complete code examples and composition templates, see [REFERENCE.md](REFERENCE.md).
