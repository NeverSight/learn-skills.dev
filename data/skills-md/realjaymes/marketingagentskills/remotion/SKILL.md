---
name: remotion
version: 4.0.0
description: Remotion video creation in React - dynamic concept catalog for video briefs, cold audience optimization, and technical best practices
metadata:
  tags: remotion, video, react, animation, composition, programmatic-video
---

## When to Use

Use this skill when:
- Creating a new Remotion video from scratch
- Generating video brief variants for a content asset
- Modifying an existing Remotion composition
- Debugging Remotion animation or rendering issues
- Working with any Remotion-specific APIs or components

## Video Creation Process

When creating a new Remotion video, follow this 8-step process. Step 2 selects 3-5 concepts from the catalog based on the brief and cold audience optimization. Steps 4 and 5 are approval gates. Do not write code until both are approved.

For the full process document with templates and decision matrices, read [references/video-creation-process.md](references/video-creation-process.md).

### Step 0: Brand Identification

Before any creative work, identify the brand. Ask the user: **"What brand is this video for?"**

**If the brand has a preset below**, use it directly. No further brand questions needed.

**If the brand is not listed**, ask the user to provide a brand website URL or brand guidelines. Extract: background color, primary accent, secondary accent, text colors, font family, and theme (light/dark). If no guidelines exist, ask for at minimum: primary color, background color, and font preference.

### Step 1: Creative Brief

Gather and lock before any creative work:

```
Purpose: [Why this video exists]
Audience: [Who is watching]
Core message: [One sentence]
Content type: [blog-post, case-study, webinar, podcast, lead-magnet, product-update, tool-launch, industry-report, event-recap, client-testimonial, playbook, template, ai-demo, custom-gpt]
Channels: [Where it will be distributed]
CTA: [What the viewer should do next]
Source assets: [Files, components, or URLs to reference]
Tone: [Descriptive words for the feel]
Brand: [Brand name from Step 0]
```

### Step 2: Concept Selection (3-5 Recommended Concepts)

After locking the creative brief, analyze it to select the best video concepts for this specific use case. Do not present a fixed set of variants. Draw from the concept catalog in [references/concept-catalog.md](references/concept-catalog.md).

**The catalog contains 18 primary concepts, 8 visual style modifiers, and 5 cold audience hook patterns.** Read it before generating recommendations.

#### Selection Process

1. **Score concepts against the brief.** For each concept in the catalog, evaluate:
   - Does the concept's "Best For" match the content type?
   - Can the core message land in 15-30 seconds with this structure?
   - Does the concept work at the target duration and dimensions?
   - Does the brief provide the data/visuals this concept needs?

2. **Apply the cold audience filter.** For each scored concept, evaluate:
   - Can a viewer with ZERO prior context understand the value in the first 3 seconds?
   - Does the concept create scroll-stopping visual motion in the opening beat?
   - Does the concept avoid requiring prior knowledge of the brand, product, or problem space?
   - If the concept naturally front-loads a result or data point (metric-counter, animated-infographic, before-after), it is inherently stronger for cold audiences than narrative concepts that need setup time.

3. **Select a hook pattern.** For each recommended concept, pair it with a hook pattern from the catalog:
   - Content with data → result-first
   - Product launches and tools → pattern-interrupt
   - Thought leadership and education → curiosity-gap
   - Trust-building content → social-proof-hook
   - Competitive and pricing content → loss-aversion

4. **Present 3-5 recommended concepts** as one-page briefs. For each:
   - Concept name (from the catalog) and one-sentence description
   - Why it fits this brief (1-2 sentences referencing the specific content and audience)
   - Recommended hook pattern and opening beat description
   - Scene-by-scene table (from the catalog template, customized for this content)
   - Optional visual style modifier if one enhances the concept

5. **Rank the recommendations.** Mark the top recommendation and explain why.

6. **User selects one (or a hybrid of two).** Lock the selected concept before proceeding to Step 3.

#### Cold Audience Optimization Rules

These rules apply to all concept recommendations and override content-type defaults when they conflict:

- **Default assumption: cold audience.** Unless the brief explicitly states the audience is warm (retargeting, existing users, newsletter subscribers), assume zero brand awareness.
- **First scene requirements for cold audiences:**
  1. A visual pattern interrupt (motion, color contrast, or scale change)
  2. Text that names a problem or result the viewer recognizes WITHOUT knowing the brand
  3. No brand identification in scene 1 (save brand card for scene 2 or later)
- **Hook pattern restrictions for cold audiences:** Use pattern-interrupt, result-first, or loss-aversion. Avoid curiosity-gap unless the stat/claim is universally relatable without brand context.
- **Concept flexibility:** If no concept in the catalog fits the brief well for a cold audience, create a hybrid or adapt an existing concept. The catalog is a starting library, not a constraint.

### Step 3: Format and Specs

Resolve from the brief and selected variant using the format decision matrix:

| Channel | Dimensions | Duration |
|---------|-----------|----------|
| LinkedIn/Instagram feed | 1080x1080 | 15-30s |
| Website/presentation | 1920x1080 | 15-60s |
| Reels/TikTok/Stories | 1080x1920 | 15-60s |
| Email (GIF) | 600x600 or 800x450 | 5-10s |

Default FPS: 30. Only use 60 if smooth motion is critical.

```
Dimensions: [width]x[height]
Duration: [X] seconds ([X * fps] frames)
FPS: 30
Composition ID: [PascalCase]
Loop: [yes/no]
Output formats: [mp4, gif, webm]
Selected concept: [concept-id from catalog, or hybrid]
```

### Step 4: Scene Breakdown (APPROVAL GATE)

Define every scene before writing code. Use the selected variant's scene template as the starting structure, then customize for the specific content.

Present the scene table for approval.

**Scene table format:**

| # | Name | Time | Copy | Animation | Purpose |
|---|------|------|------|-----------|---------|
| 1 | Hook | 0-3s | Exact text | Motion description | Why it exists |

**Timing guidelines:**

| Duration | Scene Count | Avg Per Scene |
|----------|-------------|---------------|
| 10s | 3-4 | 2.5-3.3s |
| 15s | 4-6 | 2.5-3.75s |
| 30s | 8-12 | 2.5-3.75s |
| 60s | 12-20 | 3-5s |

Lock copy, timing, and narrative structure before proceeding.

### Step 5: Visual Design (APPROVAL GATE)

Lock before implementation:

**Color palette** (minimum required roles):
- Background, Primary accent, Secondary accent
- Text primary, Text secondary, Text tertiary
- Border/divider

**Brand theme presets** (use for known brands, skip color questions):

| Brand | Background | Primary Accent | Secondary Accent | Text Primary | Text Muted | Font | Theme |
|-------|-----------|---------------|-----------------|-------------|-----------|------|-------|
| FunnelEnvy | `#FFFFFF` / `#1a1a2e` (terminal) | `#3B82F6` (Blue) | `#8B5CF6` (Purple) | `#000000` | `#6B7280` | Inter, system | Light |
| Reform | `#FFFFFF` / `#1a1a2e` (terminal) | `#48EC80` (Green) | `#EDE630` (Yellow) | `#000000` | `#6B7280` | Inter, system | Light |
| GrowthNode | `#0f0a1a` (all scenes) | `#8B5CF6` (Purple) | `#3B82F6` (Blue) | `#FFFFFF` | `#a1a1aa` | Inter, system | Dark |
| MIA | `#F7F4FA` / `#1c1422` (dark) | `#F1DE71` (Yellow) | `#7184F1` (Purple) | `#1c1422` / `#f7f4fa` (dark) | `rgba(28,20,34,0.62)` | system-ui, -apple-system, Segoe UI | Light |

**MIA accent palette**: Blue `#71C4F1`, Purple `#7184F1`, Pink `#F171C4`, Green `#71F19E`

**Custom brands**: If the brand is not listed above, define colors from the brand website or guidelines provided in Step 0. Fill the same roles: background, primary accent, secondary accent, text primary, text muted, font, theme.

**Typography**: Font family, weight hierarchy, sizes at target resolution.

**Animation style**: Spring (bouncy/smooth/snappy), linear, or ease-based. Pick a dominant style.

**Source of truth**: If matching an existing design, reference the source file.

### Step 6: Architecture Decision

Agent resolves this based on scene complexity:

| Condition | Approach |
|-----------|----------|
| Under 15 scenes | Single file |
| 15+ scenes or reusable parts | Multi-file with `scenes/` directory |
| Shared elements across scenes | Persistent layer with opacity envelope |

Always use a centralized timing constant (`const T = { ... }`).

### Step 7: Implementation

Write code against locked decisions. All animation must follow Remotion rules (see Technical Reference below).

### Step 8: Output Documentation

Generate a reference doc covering: specs, selected variant, preview/render commands, scene breakdown, color palette, timing config, architecture notes, iteration guide.

---

## Technical Reference

Read individual rule files for API details and code examples.

### Core Animation and Timing

- [rules/animations.md](rules/animations.md) - Animation fundamentals. All motion via `useCurrentFrame()`. No CSS transitions
- [rules/timing.md](rules/timing.md) - `interpolate()`, `spring()`, easing functions, spring configs
- [rules/sequencing.md](rules/sequencing.md) - `<Sequence>` and `<Series>` for timing, delay, and duration control
- [rules/trimming.md](rules/trimming.md) - Trim beginnings (negative `from`) and ends (`durationInFrames`)
- [rules/transitions.md](rules/transitions.md) - `<TransitionSeries>` with fade, slide, wipe, flip, clockWipe

### Media

- [rules/assets.md](rules/assets.md) - `staticFile()` for public folder assets
- [rules/videos.md](rules/videos.md) - `<Video>` with trimming, volume, speed, looping, pitch
- [rules/audio.md](rules/audio.md) - `<Audio>` with trimming, volume, speed, pitch
- [rules/images.md](rules/images.md) - `<Img>` component (ensures load before render)
- [rules/gifs.md](rules/gifs.md) - `<AnimatedImage>` for GIF/APNG/AVIF/WebP
- [rules/fonts.md](rules/fonts.md) - Google Fonts via `@remotion/google-fonts`, local fonts via `@remotion/fonts`

### Text and Captions

- [rules/text-animations.md](rules/text-animations.md) - Typewriter, word highlighting patterns
- [rules/measuring-text.md](rules/measuring-text.md) - `measureText()`, `fitText()`, `fillTextBox()`
- [rules/display-captions.md](rules/display-captions.md) - TikTok-style captions, word-by-word highlighting
- [rules/import-srt-captions.md](rules/import-srt-captions.md) - Parse `.srt` files with `parseSrt()`
- [rules/transcribe-captions.md](rules/transcribe-captions.md) - Whisper.cpp, Whisper Web, OpenAI API

### Composition and Metadata

- [rules/compositions.md](rules/compositions.md) - `<Composition>`, `<Still>`, `<Folder>`, `defaultProps`
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - Dynamic duration, dimensions, and props

### Advanced

- [rules/3d.md](rules/3d.md) - `<ThreeCanvas>` with React Three Fiber
- [rules/charts.md](rules/charts.md) - SVG/D3.js charts animated via `useCurrentFrame()`
- [rules/lottie.md](rules/lottie.md) - `<Lottie>` component with `@remotion/lottie`
- [rules/tailwind.md](rules/tailwind.md) - TailwindCSS (no `transition-*` or `animate-*` classes)

### Media Utilities (Mediabunny)

- [rules/extract-frames.md](rules/extract-frames.md) - Extract video frames at timestamps
- [rules/can-decode.md](rules/can-decode.md) - Check video/audio decodability
- [rules/get-video-duration.md](rules/get-video-duration.md) - Video duration in seconds
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) - Video width and height
- [rules/get-audio-duration.md](rules/get-audio-duration.md) - Audio duration in seconds

### Layout

- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - `useCurrentScale()` for accurate measurements

---

## References

- [references/concept-catalog.md](references/concept-catalog.md) - Concept catalog with 18 primary concepts, 8 visual style modifiers, 5 cold audience hook patterns, selection criteria, and content-type affinity matrix
- [references/video-creation-process.md](references/video-creation-process.md) - Full process document with templates, decision matrices, and detailed guidance

---

## Hard Rules

These apply to all Remotion code. Violations will produce incorrect output.

1. **All animation driven by `useCurrentFrame()`**. No CSS transitions, no Tailwind `animate-*` or `transition-*` classes, no React Three Fiber `useFrame()`
2. **Use Remotion components** (`<Img>`, `<Video>`, `<Audio>`) not native HTML elements
3. **Use `staticFile()`** for all assets in the `public/` folder
4. **Time in seconds**: multiply by `fps` from `useVideoConfig()` to get frames
5. **No third-party animation libraries** driving motion (disable their animations, use `useCurrentFrame()` instead)
6. **Every concept must be self-explanatory.** A viewer scrolling with zero context should understand the value from the video alone. No scene should depend on external knowledge. Copy must carry the full message independently. Always assume a cold audience unless the brief says otherwise.
