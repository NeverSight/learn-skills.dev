---
name: glslviewer-shader-debug
description: Adapt fragment shaders or runtime-shader snippets into standard GLSL, render them with glslViewer in headless mode, and inspect PNG output for shader debugging. Use when Codex needs to validate SDFs, gradients, masks, edge contours, or intermediate shader math by producing reproducible preview images from `.frag` files or translated shader snippets.
---

# glslViewer Shader Debug

Use this skill to turn shader math into repeatable headless previews.

## Workflow

1. Confirm `glslViewer` is available with `command -v glslViewer || command -v glslviewer`.
2. Create a scratch `.frag` file, usually by copying [`assets/sdf-contour-template.frag`](./assets/sdf-contour-template.frag).
3. Translate the source shader into standard GLSL.
4. Render the shader with [`scripts/render_headless.sh`](./scripts/render_headless.sh).
5. Inspect the generated PNGs and compare the contour or mask shape against expectations.

## Translation Rules

- For runtime-shader or SkSL-like snippets, read [`references/runtime-effect-to-glsl.md`](./references/runtime-effect-to-glsl.md).
- Keep the math identical first. Change syntax before changing behavior.
- Replace non-standard types such as `half4` or `float2` with GLSL equivalents.
- Rewrite `main(vec2 fragCoord)` into standard fragment entrypoint form:
```glsl
void main()
{
    vec2 fragCoord = gl_FragCoord.xy;
    fragColor = ...;
}
```
- Prefer adding a contour or mask visualization instead of staring at raw SDF alpha. The template already includes a reusable `previewColor()` helper.

## Rendering

Render one or more fragment shaders like this:

```bash
/root/.codex/skills/glslviewer-shader-debug/scripts/render_headless.sh path/to/a.frag path/to/b.frag
```

Useful options:

- `--output DIR`: choose output directory
- `--size WIDTHxHEIGHT`: choose render size, default `256x256`
- `GLSLVIEWER_BIN=/full/path/to/glslViewer`: force a specific binary

The script writes one PNG per input shader plus a frame directory that contains the original exported frame.

## Validation Heuristics

- For rounded-rect SDFs, top and bottom scanlines should narrow near the corners.
- For gradients or normals, prefer false-color output so directional changes are obvious.
- If the headless preview looks correct but device output does not, suspect uniform binding, backend shader translation, or downstream thresholding rather than the pure math.

## Resources

- Renderer: [`scripts/render_headless.sh`](./scripts/render_headless.sh)
- Translation notes: [`references/runtime-effect-to-glsl.md`](./references/runtime-effect-to-glsl.md)
- Starter template: [`assets/sdf-contour-template.frag`](./assets/sdf-contour-template.frag)
