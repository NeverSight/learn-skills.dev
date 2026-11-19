---
name: cursor-reveal-hero
description: Build, repair, tune, and validate interactive cursor-trail mask reveal hero effects in frontend projects. Use when implementing canvas-based base/reveal compositing, soft radial cursor masks, fading cursor trails, reveal debug controls, full-screen hero scenes without site text, or browser smoke checks for cursor reveal, hover reveal, before/after reveal, and mask compositing effects.
---

# Cursor Reveal Hero

Use this skill to create or fix a soft cursor-trail reveal effect where a base image is always visible and a reveal image appears only through a fading mask.

Core formula:

```text
final = baseImage + revealImage * softCursorTrailMask
```

## Modes

- `build`: create the effect from scratch in an existing app or from the vanilla template.
- `repair`: diagnose broken image loading, mask compositing, pointer handling, sliders, fade, resize, or cache behavior.
- `tune`: adjust radius, feather, fade, strength, opacity, and momentum for the intended feel.
- `validate`: run browser/canvas checks and inspect screenshots.

## Workflow

1. If the user is unsure whether the two image layers match, use `$image-layer-alignment-validator` first.
2. Identify the project stack. Prefer the existing framework and asset pipeline.
3. For a vanilla implementation, copy `assets/vanilla-template/` and replace the image paths.
4. Keep the page focused on the actual reveal surface. Do not add marketing copy, hero text, or unrelated content unless requested.
5. Implement the canvas architecture from `references/canvas-compositing.md`.
6. Add direct controls for tuning: radius, feather, fade, strength, opacity, and momentum.
7. Expose `window.revealSettings` and a clear-mask function in development builds when useful.
8. Run `scripts/smoke-check-reveal.mjs` against the local URL when a browser target is available.
9. Report exact changed files, current tuning values, and validation outcome.

## Implementation Rules

- Use one visible canvas and offscreen canvases for mask and reveal layers.
- Render at device-pixel-ratio scale while keeping CSS size stable.
- Use pointer events and handle mouse, touch, and pen input.
- Use a soft radial gradient, not a hard hover circle.
- Fade old mask content with `destination-out`.
- Apply the mask to the reveal layer with `destination-in`.
- Draw the base layer every frame before drawing the masked reveal layer.
- Clear the accumulated mask when control values change so old trails do not confuse tuning.
- Bump cache-buster query strings or hard refresh when static files are cached.

## Common Repair Targets

- Sliders move but settings do not change: bind `input` and `change`, update `textContent`, clear the mask after setting updates.
- Reveal acts like a hard magnifier: increase feather, radius, and fade smoothness; reduce opacity if the reveal dominates.
- Trail never disappears: increase fade or verify `destination-out` is applied to the mask canvas.
- Reveal image always visible: check `globalCompositeOperation`, mask reset, and reveal canvas clear order.
- Canvas is blurry: fix DPR scaling and resize handling.
- Effect breaks after resize: rebuild all canvas backing stores and redraw.

## Safety And Privacy

- Keep image assets local unless the user explicitly asks for external generation, hosting, or analysis.
- Do not overwrite original base/reveal assets while tuning the effect.
- Do not add analytics, remote tracking, or third-party runtime dependencies to the effect unless the project already uses them and the user wants that path.
- For browser validation, prefer local URLs and file URLs. Do not automate authenticated or private production pages unless the user explicitly scopes that target.

## Validation And Eval

- Use `scripts/smoke-check-reveal.mjs` when a URL is available.
- Inspect a screenshot or live page after automated checks; smoke success does not prove visual quality.
- Verify slider behavior manually when controls were changed.
- Re-test after resizing the viewport and after cache-buster changes.

## Resources

- Read `references/canvas-compositing.md` before implementing or repairing the core render loop.
- Read `references/tuning-and-failure-modes.md` when adjusting feel or diagnosing controls.
- Read `references/browser-validation.md` before final visual checks.
- Copy `assets/vanilla-template/` for a standalone HTML/CSS/JS starter.
- Run `scripts/smoke-check-reveal.mjs` for browser evidence when a local URL is available.
