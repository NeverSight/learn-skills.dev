---
name: remotion
description: 'Best practices for Remotion - Video creation in React. Use when creating programmatic videos with Remotion, adding animations or transitions, working with audio/captions, rendering compositions, embedding 3D content, building charts, or using Mapbox maps in video.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://www.remotion.dev/docs'
user-invocable: false
---

# Remotion

## Overview

Remotion enables programmatic video creation using React components. Compositions define renderable videos with explicit width, height, fps, and duration. All animations must be driven by `useCurrentFrame()` -- CSS animations and Tailwind animation classes are forbidden as they cause rendering artifacts. Use this skill for Remotion compositions, animations, audio, captions, transitions, media handling, or rendering. Not intended for general React UI development.

## Quick Reference

| Pattern           | API / Approach                                                      | Key Points                                                                            |
| ----------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Basic animation   | `useCurrentFrame()` + `interpolate()`                               | Always clamp with `extrapolateRight: 'clamp'`                                         |
| Spring animation  | `spring({ frame, fps })`                                            | `{ damping: 200 }` for smooth, no-bounce motion                                       |
| Composition       | `<Composition id, component, durationInFrames, fps, width, height>` | Always set explicit dimensions                                                        |
| Dynamic metadata  | `calculateMetadata` on `<Composition>`                              | Set duration, dimensions, props before render                                         |
| Sequencing        | `<Sequence from, durationInFrames>`                                 | `useCurrentFrame()` returns local frame (starts at 0)                                 |
| Series            | `<Series>` with `<Series.Sequence>`                                 | Sequential playback; negative offset for overlaps                                     |
| Transitions       | `<TransitionSeries>` with `fade()`, `slide()`, `wipe()`             | Total duration = sum of scenes minus transition durations                             |
| Audio/Video       | `<Audio>` / `<Video>` from `@remotion/media`                        | Use `staticFile()` for local assets                                                   |
| Captions          | `createTikTokStyleCaptions()`                                       | Token-level word highlighting via `page.tokens`                                       |
| Images            | `<Img>` from `remotion`                                             | Never use native `<img>` or Next.js `<Image>`                                         |
| GIFs              | `<AnimatedImage>` from `remotion`                                   | Synced with timeline; `playbackRate` for speed control                                |
| Fonts             | `@remotion/google-fonts` or `@remotion/fonts`                       | Call `loadFont()` at top level; blocks rendering until ready                          |
| 3D content        | `<ThreeCanvas>` from `@remotion/three`                              | Must set `width`/`height`; `useFrame()` from R3F is forbidden                         |
| Text measurement  | `measureText()`, `fitText()` from `@remotion/layout-utils`          | Load fonts first; match properties for measurement and render                         |
| Parameters        | Zod schema on `<Composition schema>`                                | Top-level must be `z.object()`; exact Zod version required (check Remotion docs)      |
| Transparent video | `--pixel-format=yuva420p --codec=vp9`                               | WebM for browser; ProRes 4444 for editing software                                    |
| Maps              | Mapbox with `useCurrentFrame()`                                     | Set `interactive: false`, `fadeDuration: 0`; render with `--gl=angle --concurrency=1` |

## Common Mistakes

| Mistake                                                         | Correct Pattern                                                            |
| --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Using CSS animations or `setTimeout`                            | Use `interpolate()` and `useCurrentFrame()` for timeline-synced animations |
| Using native `<img>`, `<video>`, `<audio>` tags                 | Use `<Img>`, `<Video>`, `<Audio>` from Remotion for proper preloading      |
| Hardcoding video duration                                       | Use `calculateMetadata` to dynamically set duration from content           |
| Not specifying width/height on compositions                     | Always define explicit dimensions to avoid rendering issues                |
| Using `useFrame()` from React Three Fiber                       | Use `useCurrentFrame()` from Remotion inside `<ThreeCanvas>`               |
| Forgetting `premountFor` on sequences                           | Always premount sequences to preload components before playback            |
| Not clamping `interpolate()` output                             | Set `extrapolateRight: 'clamp'` to prevent values exceeding target range   |
| Placing `<Sequence>` in `<ThreeCanvas>` without `layout="none"` | Set `layout="none"` on any `<Sequence>` inside `<ThreeCanvas>`             |

## Delegation

- **Discover available Remotion components and their props**: Use `Explore` agent to search the codebase for composition definitions and asset usage
- **Build a multi-scene video with transitions and audio**: Use `Task` agent to compose sequences, transitions, and audio tracks step by step
- **Plan a video generation pipeline with dynamic data**: Use `Plan` agent to design the architecture for parametrized compositions and rendering workflow

## References

- [Animations and Timing](references/animations-and-timing.md) -- Interpolation, springs, easing, and frame-driven animation patterns
- [Compositions and Sequencing](references/compositions-and-sequencing.md) -- Defining compositions, stills, folders, sequences, series, and trimming
- [Media and Assets](references/media-and-assets.md) -- Audio, video, images, GIFs, fonts, and static file handling
- [Captions and Text](references/captions-and-text.md) -- Transcription, SRT import, TikTok-style captions, and text animations
- [Transitions](references/transitions.md) -- Scene transitions with fade, slide, wipe, flip, and duration calculation
- [Advanced Features](references/advanced-features.md) -- 3D content, charts, maps, parameters, transparent video, and DOM measurement
