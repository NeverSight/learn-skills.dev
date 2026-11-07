---
name: lucida-remove-background
description: Remove image backgrounds locally with Lucida's bgr CLI and save transparent RGBA PNGs while preserving soft alpha in glass, smoke, glow and VFX, camouflage, text and logos, line art, illustrations, and print designs. Use when a user asks to remove, erase, isolate, cut out, or make the background of an image transparent; prefer Lucida for translucent or effect-heavy artwork and BiRefNet-HR for high-resolution solid physical objects or product photos.
---

# Lucida Background Removal

Use the `bgr` executable from `egeorcun/lucida`. Preserve the source image and create a separate transparent PNG.

## Workflow

1. Resolve the input image and confirm it exists.
2. Use the user's output path when provided. Otherwise, write `<input-stem>-transparent.png` beside the input. Do not overwrite the source unless the user explicitly requests it.
3. Check whether `bgr` is available:

   ```text
   bgr --help
   ```

   **Note:** If the current environment is sandboxed (for example: Codex sandbox), run all `bgr` commands in the user's normal terminal. Otherwise the `bgr --help` command process might be freezed or timeout.

4. If `bgr` is missing, verify that `uv` is available and install the CLI:

   ```text
   uv tool install --from git+https://github.com/egeorcun/lucida.git my-bg-remover
   ```

   The package requires Python 3.12 or newer. The installation exposes one executable: `bgr`.

5. Select the model:

   - Use `lucida` by default, especially for glass, partial transparency, smoke, glow, VFX, camouflage, text or logos with soft shadows, line art, illustrations, and print or sticker designs.
   - Use `birefnet-hr` for high-resolution general segmentation, especially solid physical subjects, product photos, or when Lucida keeps unwanted low-alpha background haze. Expect higher compute and memory use because it processes at 2048×2048.
   - Read [references/models.md](references/models.md) only when an alternate model, a versioned local checkpoint, or model-loading troubleshooting is needed.

6. Run the removal command with quoted paths:

   ```text
   bgr remove "<input-path>" -o "<output-path>.png" --model lucida
   ```

   Replace `lucida` with `birefnet-hr` when that model better matches the subject.

7. Confirm that the command succeeds and the output PNG exists. Inspect the result when image viewing is available, paying particular attention to partial transparency, holes, fine edges, retained background haze, and color fringing.
8. Return the output file to the user and state which model and optional flags were used.

## Optional passes

- Add `--refine` when the first result has visibly rough or broken edges. Treat it as a retry, not a default, because refinement adds processing and can change soft boundaries.
- Keep color decontamination enabled by default. Add `--no-decontaminate` only when decontamination shifts intentional glow, translucent color, or edge color.
- Change one variable per retry so the effect of the model or flag remains clear.

Examples:

```text
bgr remove "input.jpg" -o "output.png" --model lucida --refine
bgr remove "product.jpg" -o "product-transparent.png" --model birefnet-hr
bgr remove "glow.png" -o "glow-transparent.png" --model lucida --no-decontaminate
```

## Weight behavior

- The current `lucida` registry entry uses the Hugging Face model ID `egeorcun/lucida`. On first use, Transformers downloads the published weights to its cache; allow time and network access for this download.
- The `birefnet-hr` registry entry uses the Hugging Face model ID `ZhengPeng7/BiRefNet_HR` and downloads its published weights to the same cache on first use.
- The separate `lucida-v7` registry entry expects a training checkpoint at `data/checkpoints/epoch_7.pth`, resolved from the command's working directory. Use that entry only when the matching training checkpoint is already available at that exact path.
- Do not rename the published `model.safetensors` to `epoch_7.pth`: the local entry expects a training-checkpoint payload containing a `model` state dictionary.

## Guardrails

- Always use PNG for transparent output. JPEG cannot preserve an alpha channel.
- Keep the original dimensions unless the user explicitly requests resizing.
- Do not claim success from the command exit alone when visual inspection is possible.
- Do not switch to experimental or versioned checkpoints without explaining the choice.
