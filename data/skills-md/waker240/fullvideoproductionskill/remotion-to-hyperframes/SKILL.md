---
name: remotion-to-hyperframes
description: Port an existing Remotion composition to HyperFrames HTML while preserving visible behavior. Use only when the user requests a Remotion migration.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

# Remotion to HyperFrames

> **Confirm the route before you build.** Use this **only** to port an existing **Remotion** (React) composition's source into HyperFrames. Authoring a **new** composition (even one inspired by a Remotion video) → the creation workflows / `/general-video`. **Out of scope** (one-way, Remotion-only): no reverse export (HyperFrames → Remotion or any framework), and a **non-Remotion** source (After Effects, Framer Motion, plain React / CSS) has no Remotion source to translate → re-create via `/general-video`. Unsure, or only a passing Remotion mention? **Read `/hyperframes` first.**

## Overview

Translate Remotion (React-based) video compositions into HyperFrames (HTML + GSAP) compositions. Most Remotion idioms have direct HyperFrames equivalents — the translation is mechanical for ~80% of typical compositions. This skill encodes the mapping and guards against the lossy 20% by refusing to translate patterns that don't fit HF's seek-driven model and recommending the runtime interop pattern from [PR #214](https://github.com/heygen-com/hyperframes/pull/214) instead.

The skill ships comparison scripts; the large upstream test corpus is excluded. Validate the actual translated project using matched renders, numerical comparison and visual/audio inspection. SSIM alone does not establish semantic fidelity.

## When to use

**Use this skill ONLY when the user explicitly asks to migrate from Remotion.** Example trigger phrases:

- "port my Remotion project to HyperFrames"
- "convert this Remotion code to HyperFrames"
- "migrate from Remotion"
- "translate this Remotion comp"
- "rewrite this as HyperFrames HTML"

**Do NOT use this skill when:**

- (a) The user is authoring a **new** HyperFrames composition, even if they have or are A/B-testing a similar Remotion video.
- (b) The user mentions Remotion in passing without asking for migration.
- (c) The user shares Remotion code as reference material rather than asking for a translation.
- (d) The user asks for "the same video as my Remotion one" without explicitly asking to migrate the source — treat that as a fresh HyperFrames build.

**NOT SUPPORTED (decline — this is not what this skill does):**

- **The reverse direction.** Exporting a HyperFrames composition back out _to_ Remotion (or to any other framework) is not a workflow — the translation is Remotion → HyperFrames only. Say so plainly.
- **Non-Remotion sources.** An After Effects project (`.aep`), a Framer Motion / plain-React / CSS animation, or any other tool's source is not a Remotion composition — there is no Remotion source to translate. Re-create it natively via `/general-video`, or decline if HyperFrames can't represent it.

When in doubt, default to authoring a native HyperFrames composition with `/general-video` (the general HyperFrames authoring flow) instead.

## Workflow

### Step 1: Lint the source

Run [`scripts/lint_source.py`](scripts/lint_source.py) over the Remotion source directory. The lint detects patterns that can't translate cleanly:

- **Blockers** (refuse + recommend interop): `useState`, `useReducer`, `useEffect`/`useLayoutEffect` with non-empty deps, async `calculateMetadata`, third-party React UI libraries (MUI, Chakra, Mantine, antd, shadcn, Radix, NextUI).
- **Warnings** (translate after dropping the construct): `@remotion/lambda` config, `delayRender`, `useCallback`, `useMemo`, custom hooks.
- **Info** (translate with note): `staticFile`, `interpolateColors`.

If any blocker fires, **stop**. Read [`references/escape-hatch.md`](references/escape-hatch.md) and surface the recommendation message. Warnings don't stop translation — drop the offending construct in step 3 and note the gap in `TRANSLATION_NOTES.md`. `@remotion/lambda` config is the canonical warning case: the skill drops the import + `renderMediaOnLambda(...)` calls but translates the rest of the composition.

### Step 2: Plan the translation

Read [`references/api-map.md`](references/api-map.md) — the index of every Remotion API and its HF equivalent or per-topic reference. Identify which topic references you'll need based on what the source uses:

| Source contains                                                           | Load reference                                |
| ------------------------------------------------------------------------- | --------------------------------------------- |
| `Composition`, `defaultProps`, `schema`, `calculateMetadata`              | [`parameters.md`](references/parameters.md)   |
| `Sequence`, `Series`, `Loop`, `AbsoluteFill`, `Freeze`                    | [`sequencing.md`](references/sequencing.md)   |
| `useCurrentFrame`, `interpolate`, `spring`, `Easing`, `interpolateColors` | [`timing.md`](references/timing.md)           |
| `Audio`, `Video`, `Img`, `IFrame`, `staticFile`, `delayRender`            | [`media.md`](references/media.md)             |
| `TransitionSeries`, `@remotion/transitions`                               | [`transitions.md`](references/transitions.md) |
| `@remotion/lottie`                                                        | [`lottie.md`](references/lottie.md)           |
| `@remotion/google-fonts/<Family>`, `Font.loadFont`, `@font-face`          | [`fonts.md`](references/fonts.md)             |

Don't load all of them — load only what the specific source needs.

### Step 3: Generate the HF composition

Emit `index.html` with:

- Root `<div id="stage">` carrying the composition's `data-composition-id`, `data-start="0"`, `data-duration` (in seconds), `data-fps`, `data-width`, `data-height`, plus one `data-*` per scalar prop.
- A flat list of scene divs with `data-start` / `data-duration` / `data-track-index`.
- Inline `<style>` for layout; CSS sets the `from` state of every animated property.
- A single `<script>` tag at the bottom containing one paused `gsap.timeline({paused: true})`. Every Remotion `useCurrentFrame()` derivation becomes a tween on this timeline at the right offset.
- `window.__timelines["<composition-id>"] = tl;` registers the timeline with HF's runtime.

Custom React subcomponents inline as repeated HTML using the prop interface as the template (see [`parameters.md`](references/parameters.md) for the per-instance `data-*` pattern).

### Step 4: Validate

Run the eval harness — [`references/eval.md`](references/eval.md) for the full guide. Quick path:

```bash
# Set these to the installed skill and actual source/translation directories.
R2HF_DIR="/absolute/path/to/skills/remotion-to-hyperframes"
SOURCE_DIR="/absolute/path/to/remotion-project"
TARGET_DIR="/absolute/path/to/hyperframes-project"
(cd "$SOURCE_DIR" && npx remotion render <CompositionId> out/baseline.mp4)
(cd "$TARGET_DIR" && npx --yes hyperframes@0.7.17 render --output translated.mp4)
bash "$R2HF_DIR/scripts/render_diff.sh" "$SOURCE_DIR/out/baseline.mp4" "$TARGET_DIR/translated.mp4" "$TARGET_DIR/diff"
```

Threshold: ~0.02 below `p05` of the source's complexity tier (see [eval.md](references/eval.md) for historical calibration context). If the diff fails, run [`scripts/frame_strip.sh`](scripts/frame_strip.sh) to see _which_ frames diverged, then re-read the relevant timing/sequencing/media reference.

**Critical**: both renders must use matching pixel format. Set `Config.setVideoImageFormat("png")` + `Config.setColorSpace("bt709")` in the Remotion source's `remotion.config.ts` — otherwise the diff measures encoder differences (~0.05 SSIM hit), not translation fidelity.

### Step 5: Document gaps

Anything that didn't translate cleanly (volume ramps dropped, custom presentations approximated, fonts substituted) gets a `TRANSLATION_NOTES.md` written next to the HF output. See [`references/limitations.md`](references/limitations.md) for the format.

## What this skill explicitly does NOT do

- **Translate React state machines.** Compositions that drive animation via `useState` + `useEffect` are not deterministic frame-capture targets in HyperFrames' seek-driven model. Recommend the runtime interop pattern.
- **Run Remotion's render pipeline alongside HyperFrames.** That's the runtime interop pattern from [PR #214](https://github.com/heygen-com/hyperframes/pull/214) — a separate solution for compositions that fail this skill's lint.

(`@remotion/lambda` is _not_ a blocker — Lambda config is deployment, not animation. The skill drops it as a warning and translates the rest. See [`references/escape-hatch.md`](references/escape-hatch.md).)

## Validate your translation

The large upstream test corpus is not included. Use the supplied `scripts/lint_source.py`, `scripts/render_diff.sh` and `scripts/frame_strip.sh` on your own source and translated composition. Match size, frame rate, duration, fonts and encoding, then inspect semantic differences and sound as well as SSIM. See [eval.md](references/eval.md). Historical benchmark numbers do not prove this release or your project was rendered successfully.
