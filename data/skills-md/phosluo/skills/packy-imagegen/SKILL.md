---
name: packy-imagegen
description: Generate raster images with PackyAPI's gpt-image-2.5-flare image endpoint and save verified PNG or JPEG files locally. Use when the agent needs to create an image through PackyAPI, or when users mention PackyAPI, gpt-image-2.5-flare, gpt-image-2.5-sunburst, gpt-image-2, an image-group token, or the Packy drawing API.
---

# Packy Imagegen

Generate one image through PackyAPI's OpenAI-compatible Images API with the bundled dependency-free script. Do not modify or invoke the system `imagegen` CLI for this route.

## Requirements

Require a PackyAPI token whose group can access the model. `gpt-image-2.5-flare` is served from the `image` group; the older `gpt-image-2` is served from `sora`. Read the token from `PACKY_API_KEY`; fall back to `OPENAI_API_KEY`. Never place a key in a command argument, prompt, file, output, or chat response.

If neither variable is set, ask the user to set one locally. Do not ask them to paste a key into chat.

```bash
export PACKY_API_KEY="<image group token>"
```

## Workflow

1. Shape the user's request into a concise production prompt. Preserve exact requested text and list essential constraints.
2. Choose a valid size. Prefer `1024x1024`, `1536x1024`, or `1024x1536`; `2048x2048` and `3840x2160` are available for larger output.
3. Pick quality deliberately: `low` for tests, `medium` for drafts, `high` for finals. `auto` costs roughly four times `high` at the same size, so pass an explicit level unless the user asks for `auto`.
4. Choose a workspace output under `output/imagegen/` unless the user names another destination.
5. Run `scripts/generate.py`. Use `--force` only when the user explicitly requested replacement or the target is a disposable test artifact.
6. Inspect the resulting image with the available image-viewing tool. Check subject, composition, text, dimensions, and obvious artifacts.
7. Iterate with one targeted prompt change if necessary.
8. Return the absolute saved path, final prompt summary, model, size, quality, and that PackyAPI CLI mode was used.

## Command

```bash
python3 <this-skill-dir>/scripts/generate.py \
  --prompt "A realistic product photo of a ceramic mug" \
  --size 1024x1024 \
  --quality medium \
  --out output/imagegen/ceramic-mug.png
```

The default model is `gpt-image-2.5-flare`. Switch variants with `--model gpt-image-2.5-sunburst`, or use `--model gpt-image-2` for the legacy route.

Use `--prompt-file` for long prompts. Use `--dry-run` to print the exact request without a network call. The script waits synchronously, accepts either `b64_json` or a URL response, validates the file signature, and writes atomically.

## Guardrails

- Use only `POST /v1/images/generations`; PackyAPI does not support these image models through Responses or Chat Completions.
- Keep `n=1`; make separate calls for variants.
- Do not send `response_format` to `gpt-image-2.5-flare`. It rejects the field with `400 unknown_parameter` and returns `b64_json` by default; the bundled script omits it.
- Do not request transparent output. The tested route reports an opaque background; native transparency is not documented for this model.
- Do not persist credentials in this skill.
- Do not run duplicate requests after an execution tool yields early. Check the returned session/process and wait for it to finish before retrying.
- Treat a valid PNG/JPEG output as success only after visual inspection.

Read [references/packy-api.md](references/packy-api.md) when diagnosing provider errors, changing advanced parameters, or selecting nonstandard sizes.
