---
name: rendiv-video
description: >
  Guidance for building programmatic videos with rendiv — a React/TypeScript
  framework for composing video scenes, animating with springs and interpolation,
  and rendering to MP4/WebM. Use when writing or modifying rendiv compositions,
  working with rendiv animation APIs, or setting up a rendiv project.
license: Apache-2.0
compatibility: Requires Node.js 18+, pnpm, and a React 19 project
metadata:
  author: rendiv
  version: "1.0"
---

# Rendiv Video Skills

Use these skills whenever you are working with rendiv code — writing compositions,
animating elements, embedding media, or rendering output.

## Core Mental Model

Rendiv treats video as a **pure function of a frame number**. Every visual property
(position, opacity, color, scale) is derived from the current frame via `useFrame()`.
There is no timeline state machine, no imperative keyframe API. You write a React
component that accepts a frame and returns JSX — rendiv handles the rest.

```tsx
import { useFrame, interpolate } from '@rendiv/core';

export const FadeIn: React.FC = () => {
  const frame = useFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  return <div style={{ opacity }}>Hello rendiv</div>;
};
```

### Key principles

- Every animation MUST be driven by `useFrame()`. CSS animations and transitions are
  forbidden — they run on wall-clock time and will desync during frame-by-frame rendering.
- Use `interpolate()` for linear mappings and `spring()` for physics-based motion.
- Use `<Img>`, `<Video>`, `<Audio>`, and `<AnimatedImage>` from `@rendiv/core` instead
  of native HTML elements — they integrate with the render lifecycle via `holdRender`.
- Compositions are registered declaratively via `<Composition>` and `<Still>` — they
  render `null` and only provide metadata to the framework.

## Quick Start

A minimal rendiv project entry point:

```tsx
import { setRootComponent, Composition } from '@rendiv/core';
import { FadeIn } from './FadeIn';

const Root: React.FC = () => (
  <>
    <Composition
      id="FadeIn"
      component={FadeIn}
      durationInFrames={90}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);

setRootComponent(Root);
```

Render to MP4: `rendiv render src/index.tsx FadeIn out/fade-in.mp4`

## Topic Guide

Load the relevant rule file based on the task at hand:

| Task | Rule file |
|---|---|
| Animate with `interpolate`, `spring`, `Easing`, `blendColors` | [animation.md](rules/animation.md) |
| Set up compositions, stills, folders, entry point | [composition-setup.md](rules/composition-setup.md) |
| Time-shift with `Sequence`, `Series`, `Loop`, `Freeze` | [sequencing-and-timing.md](rules/sequencing-and-timing.md) |
| Control z-ordering and timeline overrides | [timeline-overrides.md](rules/timeline-overrides.md) |
| Embed images, video, audio, GIFs, iframes | [media-components.md](rules/media-components.md) |
| Render animated GIFs with playback control | [gif.md](rules/gif.md) |
| Add subtitles, SRT parsing, word highlighting | [captions.md](rules/captions.md) |
| Understand `holdRender`, environment modes, rendering pipeline | [render-lifecycle.md](rules/render-lifecycle.md) |
| Animate between scenes with `TransitionSeries` | [transitions.md](rules/transitions.md) |
| Generate SVG shapes or manipulate paths | [shapes-and-paths.md](rules/shapes-and-paths.md) |
| Add noise-driven motion or motion blur | [procedural-effects.md](rules/procedural-effects.md) |
| Load Google Fonts or local font files | [typography.md](rules/typography.md) |
| Embed Lottie animations | [lottie.md](rules/lottie.md) |
| Add 3D scenes with Three.js / R3F | [three.md](rules/three.md) |
| Use the CLI, Studio, or Player | [cli-and-studio.md](rules/cli-and-studio.md) |

## Critical Constraints

1. **No CSS animations or transitions.** Everything MUST be frame-driven via `useFrame()`.
2. **Use rendiv media components** (`<Img>`, `<Video>`, `<Audio>`, `<AnimatedImage>`)
   instead of native HTML elements. They manage `holdRender` automatically.
3. **`<Composition>` renders null.** It only registers metadata. The actual component
   is rendered by the Player, Studio, or Renderer — not by `<Composition>` itself.
4. **`setRootComponent` can only be called once.** It registers the root that defines
   all compositions.
5. **`inputRange` must be monotonically non-decreasing** in `interpolate()` and
   `blendColors()`. Both ranges must have equal length with at least 2 elements.
6. **`<Series.Sequence>` must be a direct child of `<Series>`.** It throws if rendered
   outside a `<Series>` parent.
7. **`morphPath` requires matching segments.** Both paths must have the same number of
   segments with matching command types.

## Packages

| Package | Purpose |
|---|---|
| `@rendiv/core` | Hooks, components, animation, contexts |
| `@rendiv/player` | Browser `<Player>` component |
| `@rendiv/renderer` | Playwright + FFmpeg rendering |
| `@rendiv/bundler` | Vite-based project bundler |
| `@rendiv/cli` | CLI: render, still, compositions, studio |
| `@rendiv/studio` | Studio dev server with render queue |
| `@rendiv/transitions` | TransitionSeries with fade, slide, wipe, flip, clockWipe |
| `@rendiv/shapes` | SVG shape generators (circle, rect, star, polygon, etc.) |
| `@rendiv/paths` | SVG path parsing, measurement, morphing, stroke reveal |
| `@rendiv/noise` | Simplex noise (2D, 3D, 4D) |
| `@rendiv/fonts` | Local font loading with holdRender |
| `@rendiv/google-fonts` | Google Fonts loading with holdRender |
| `@rendiv/motion-blur` | MotionTrail and ShutterBlur components |
| `@rendiv/gif` | Animated GIF playback with speed control and fit modes |
| `@rendiv/captions` | SRT/Whisper parsing, word-by-word highlighting, caption overlay |
| `@rendiv/lottie` | Frame-accurate Lottie animations via lottie-web |
| `@rendiv/three` | 3D scenes via React Three Fiber with context bridging |

## Example Assets

- [Animated bar chart](assets/animated-bar-chart.tsx) — Spring-animated bars with staggered entrances
- [Text reveal](assets/text-reveal.tsx) — Character-by-character text animation
