---
name: remotion-killer
description: Router skill for making maximum-impact videos with Remotion. Use when starting any Remotion video project — it routes to the topic skills (2D craft, 3D, transitions, audio sync, style, rendering, QA) and defines the shared working loop.
---

# Remotion Killer

Master router. Load the topic skill that matches the current task; load several when a task spans topics.

## The working loop (always follow)

1. **Plan the timeline before code**: list scenes, per-scene narration/text, target duration, resolution, fps. Decide audio first when narration drives timing (see remotion-audio-sync).
2. **Scaffold**: `npx create-video@latest` (blank) or add Remotion to an existing app. One `<Composition>` per deliverable; scenes as separate components joined by `<Sequence>` or `<TransitionSeries>`.
3. **Determinism contract** (non-negotiable): every visible value derives from `useCurrentFrame()` / props. No `setTimeout`, no CSS transitions/animations, no `Math.random()` (use `random(seed)` from remotion), no `Date.now()`, no network fetch without `delayRender`/`continueRender`.
4. **Style through a token file**: one `tokens.ts` (palette, spacing, typography scale, easing presets) imported everywhere. See remotion-style-system.
5. **Provider choices belong to the user**: narration/music/voice services are swappable — the skills define the contract (audio files per scene, durations, manifest), never a vendor. Follow the user's habit, account, or budget. See remotion-audio-sync.
6. **Iterate in Studio** (`npx remotion studio`), render short ranges (`--frames=0-90`) while developing, full render at the end.
7. **QA the rendered file, not the preview**: extract frames, check audio levels, inspect visually. See remotion-video-qa.

## Routing table

| Task | Skill |
| --- | --- |
| Scene internals, animation craft, kinetic type, layout | `remotion-2d` |
| Three.js / R3F 3D content | `remotion-3d` |
| Scene-to-scene transitions | `remotion-transitions` |
| TTS narration, music, beat sync, captions | `remotion-audio-sync` |
| Palettes, gradients, glass, texture, style presets | `remotion-style-system` |
| Multi-resolution, render CLI, codecs, scaling | `remotion-rendering` |
| Checking/accepting a rendered video | `remotion-video-qa` |

## Cross-cutting rules

- All sizing from `useVideoConfig()` — nothing hardcoded to 1920x1080.
- Fonts: load via `@remotion/google-fonts` (promise-gated) or bundle with `@fontsource/*`; never rely on system fonts for final renders.
- Prefer per-scene audio files over one long track; derive scene durations from measured audio.
- Every render input (props, assets, fonts, audio) must be local or pre-cached; renders must never hit the network at frame time.
- Keep compositions cheap: heavy blur/shadows/3D multiply by frame count. Test-render a 5s range before committing to full renders.
