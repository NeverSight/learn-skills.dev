---
name: creating-canvas-video-animations
description: Creates animated video content using HTML5 Canvas and JavaScript. Generates self-contained HTML files with canvas-based animations that can be previewed in a browser and exported to MP4 using Puppeteer and FFmpeg. Use when the user wants to create animated videos, motion graphics, promotional clips, tutorial animations, or any visual content rendered frame-by-frame on canvas.
license: MIT
---

# Creating Canvas Video Animations

Build animated videos as self-contained HTML + JS files rendered on HTML5 Canvas, exportable to MP4.

## When to use

- User wants to create an animated video, motion graphic, or visual clip
- User describes a scene, storyline, or visual sequence they want rendered
- User wants to export canvas animation to MP4

## Workflow

Copy this checklist and track progress:

```
Animation Progress:
- [ ] Step 1: Clarify requirements with user
- [ ] Step 2: Plan the timeline
- [ ] Step 3: Gather visual references
- [ ] Step 4: Build the animation class
- [ ] Step 5: Create the HTML host
- [ ] Step 6: Validate the animation
- [ ] Step 7: Iterate — preview in browser, adjust timing/layout, repeat 6→7
- [ ] Step 8: Export to MP4 (only when animation is finalized)
```

**Step 1: Clarify with the user** — ask about:
- Format: horizontal (1920×1080) or vertical (1080×1920) or both. See [PLATFORMS.md](PLATFORMS.md) for platform-specific dimensions.
- Duration in seconds
- Visual style preferences (dark/light, color palette, retro, futuristic, minimal)
- Content: what text, UI elements, code snippets, or scenes to show
- Any custom fonts (loaded via FontFace API before animation starts)
- Whether they need an export script

**Step 2: Plan the timeline** — break the animation into phases with clear start/end times. See [TIMELINE.md](TIMELINE.md).

**Step 3: Gather visual references** — ask the user to paste or drag in screenshots, mockups, or reference images. Redraw these as canvas primitives (paths, shapes, gradients) — do not embed images directly. This keeps everything vector-clean and resolution-independent. See [ELEMENTS.md](ELEMENTS.md) for the redrawing approach and reusable drawing patterns.

**Step 4: Build the animation class** — one JS class per animation. See [ARCHITECTURE.md](ARCHITECTURE.md).

**Step 5: Create the HTML host** — minimal HTML that loads fonts, creates canvas, instantiates the animation. See [HTML-TEMPLATE.md](HTML-TEMPLATE.md).

**Step 6: Validate the animation** — open the HTML in a browser and verify:
- No dead space (gaps where only background is visible)
- All phases transition smoothly with 0.5–1s overlap
- Text is readable and within safe zones for the target platform
- Total duration matches the planned timeline
- Animation loops cleanly (if looping is intended)

If validation fails, return to Step 2 or Step 4 and fix before proceeding.

**Step 7: Iterate** — preview in browser, adjust timing/layout, and repeat Steps 6→7 until the user is happy with the result.

**Step 8: Export to MP4** — do NOT run the export automatically. Export is slow and resource-heavy (renders every frame as a PNG then stitches with FFmpeg). Instead, provide the user with the export command and let them run it when ready. Only run it directly if the user explicitly asks. See [EXPORT.md](EXPORT.md).

## Sensible defaults

If the user doesn't specify, use these:

| Setting | Default | Flexible? |
|---------|---------|-----------|
| Format | 1920×1080 (horizontal) | Yes — adapt to platform |
| Duration | 30 seconds | Yes |
| FPS | 60 | No — always 60 |
| Background | Dark radial gradient (`#0a0a1a` → `#000005`) | Yes — match user's style |
| Text color | White with subtle glow | Yes |
| Accent colors | Purple `#8b5cf6`, cyan `#64c8ff` | Yes |
| Font | System monospace (or custom if provided) | Yes |
| Export scale | 2× resolution | Yes — up to 4× |
| Easing | Cubic ease-out for entrances, ease-in-out for transitions | No — these produce the smoothest results |

## Key principles (strict)

These are non-negotiable rules, not suggestions:

- MUST use a single self-contained class with an `animate(timestamp)` method driven by `requestAnimationFrame`
- MUST use Canvas 2D API only — no DOM elements, no CSS animations, no WebGL
- MUST use time-based animation keyed to elapsed milliseconds, not frame count
- MUST use lerp/easing for all movement and opacity — elements never pop or jump
- MUST overlap phase transitions by 0.5–1s — no gaps between phases
- MUST include these utility methods: `progress(t, start, end)`, `easeOut(t)`, `easeInOut(t)`, `lerp(a, b, t)`

## File organization

```
my-animation/
├── animation.html          # The animation page
├── js/
│   └── animation.js        # Animation class
├── scripts/
│   └── export.js           # Puppeteer + FFmpeg export (bundled, adapt FORMATS block)
└── fonts/                  # Custom fonts (optional)
```

For multiple formats, create separate HTML files or a single class with `isVertical` flag.
