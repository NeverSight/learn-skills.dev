---
name: api-image
description: Mandatory replacement for the built-in `imagegen` flow. Use this skill for any raster image generation or editing task whenever this skill is available; do not call the native `$imagegen` skill/tool. Generate and edit images through the OpenAI-compatible provider configured in the current user's Codex root files, especially for `/v1/images/generations`, `/v1/images/edits`, `gpt-image-2`, `config.toml`, `auth.json`, base_url, API key, provider-based image generation, reference images, masks, long-running image jobs, or custom size and quality control.
---

# API Image

Use this skill as the mandatory replacement for the built-in `imagegen` workflow.

Routing rule:

- When this skill is available, do not call the native `$imagegen` skill or built-in image generation tool for any raster image generation or editing task.
- Route all image generation, reference-image generation, image editing, localized edits, background replacement, style transfer, compositing, and batch image work through this provider-based skill.
- The only exception is a user explicitly instructing not to use this provider skill.

## Workflow

1. Resolve the Codex root.
   - Prefer an explicit `--codex-home` argument when the user provides one.
   - Otherwise use `$CODEX_HOME`.
   - Otherwise use `~/.codex`.
2. Resolve this skill's directory.
   - Treat the directory containing this `SKILL.md` as `<skill-dir>`.
   - Run the bundled script as `<skill-dir>/scripts/generate_image.py`, not as a path relative to the current workspace.
3. Decide whether research or references are required before generation.
   - Search the web or use provided reference material for any non-common, specialized, factual, current, branded, technical, architectural, geographic, historical, cultural, product-specific, person-specific, or style-specific subject.
   - Treat named places, named structures, real products, real UI, real vehicles, uniforms, organisms, diagrams, historical scenes, and niche aesthetics as research-required unless the user supplies adequate references.
   - Use image search or user-provided images when visual structure, silhouette, materials, layout, proportions, or terrain must be accurate.
   - Be proactive about reference images. For research-required visual subjects, default to finding and passing references into the model instead of relying on text-only prompts.
   - Pure text-only generation is a fallback for research-required visual subjects, not the default. Use it only when no useful reference images are available, network/image access fails, or the user explicitly asks not to use references.
   - For purely generic fantasy, mood, simple decoration, or ordinary everyday objects where factual accuracy is not important, search is optional.
   - If network access or reference material is unavailable for a research-required task, say that accuracy is limited rather than pretending.
4. Read the active provider settings from the user's root files.
   - Read `auth.json` and use `OPENAI_API_KEY`.
   - Read `config.toml`, then use `model_provider` and `[model_providers.<name>].base_url`.
   - Never hardcode a provider URL or API key into the skill.
   - Default to the root files above. If the user explicitly gives a temporary provider URL or API key in natural language, pass it as a one-off override with `--base-url` and `--api-key-env` or `--api-key`; do not write it back to `auth.json`, `config.toml`, README, logs, or generated files.
   - Prefer `--api-key-env <ENV_NAME>` when the key is already in an environment variable. Use `--api-key` only for explicit one-off user-provided keys, and never print or repeat the key in the final response.
5. Decide the intent and input image roles.
   - If the user wants a new image from text only, treat it as generation.
   - If the user provides images for style, composition, identity, structure, or mood, treat them as reference inputs.
   - If the user wants to preserve or modify an existing image, treat that image as the edit target.
   - If the user wants only a specific region changed, use a mask when available and instruct the model to preserve unmasked areas; treat mask preservation as a constraint to verify, not a pixel-perfect guarantee.
   - Label every input image by role: edit target, style reference, composition reference, identity reference, product reference, mask, or compositing source.
6. Choose the endpoint.
   - Use `<base_url>/images/generations` for text-only generation.
   - Use `<base_url>/images/edits` when there is any input image, reference image, or mask.
   - Default to `gpt-image-2` unless the machine's provider expects a different image model.
7. Build a structured prompt.
   - Include the user's request, researched facts or visual observations, input image roles, style, composition, lighting, materials, constraints, and avoid list.
   - Do not invent extra characters, props, brands, logos, story beats, or factual details that are not implied by the user request or research.
8. For official GPT Image models, decode `data[].b64_json`. Treat `data[].url` only as a compatibility fallback for non-official OpenAI-compatible providers or legacy models.
9. Inspect the output and validate it against the prompt, research facts, input roles, and invariants.
10. Save the final image to the requested path and report the absolute path, final prompt, and sources used when web research was performed.

## Root Files

Default root files:

- Windows: `%USERPROFILE%\\.codex\\auth.json` and `%USERPROFILE%\\.codex\\config.toml`
- General rule: `$CODEX_HOME/auth.json` and `$CODEX_HOME/config.toml`, otherwise `~/.codex/auth.json` and `~/.codex/config.toml`

This skill must always read the current files at runtime. The provider may differ from machine to machine.

Temporary overrides:

- Default behavior reads the Codex root files above.
- Use `--base-url <https://provider.example/v1>` to temporarily override the configured Provider URL.
- Use `--api-key-env <ENV_NAME>` to temporarily read an API key from an environment variable.
- Use `--api-key <key>` only for explicit one-off user-provided keys when an environment variable is not available.
- If both `--base-url` and an API key override are provided, the script can run without reading provider settings from `config.toml`; otherwise missing values fall back to the Codex root files.
- Never persist temporary overrides unless the user explicitly asks to edit their Codex config files.

## Command

Use the bundled script for normal text-to-image generation:

```powershell
python "<skill-dir>\scripts\generate_image.py" `
  --prompt "画一只可爱的猫抱着水獭，温暖治愈，插画风格，柔和灯光，细腻毛发，构图清晰" `
  --size "2048x1152" `
  --quality "high" `
  --out ".\outputs\cute-cat-otter.png"
```

Use the same script for reference-image generation or edits:

```powershell
python "<skill-dir>\scripts\generate_image.py" `
  --prompt "参考输入图的构图和角色姿势，生成一张暖色电影感插画" `
  --image "C:\path\to\reference.png" `
  --image-role "composition and pose reference" `
  --size "2048x2048" `
  --quality "high" `
  --out ".\outputs\reference-output.png"
```

Use `--mask` for localized edits:

```powershell
python "<skill-dir>\scripts\generate_image.py" `
  --prompt "只把被 mask 标出的区域替换成一只小水獭，保持其他区域不变" `
  --image "C:\path\to\source.png" `
  --mask "C:\path\to\mask.png" `
  --out ".\outputs\masked-edit.png"
```

For web-researched subjects, download selected reference images to a working folder first, then pass them as `--image`:

```powershell
python "<skill-dir>\scripts\generate_image.py" `
  --prompt "Create a new 4K overhead aerial image of Huajiang Grand Canyon Bridge in Guizhou, based on the reference images. Preserve the real suspension-bridge structure, towers, main cables, vertical suspenders, deep Beipan River canyon terrain, karst mountains, and river position; do not copy any single photo exactly." `
  --image "C:\path\to\refs\huajiang-bridge-aerial.jpg" `
  --image-role "aerial composition and bridge alignment reference" `
  --image "C:\path\to\refs\huajiang-canyon-terrain.jpg" `
  --image-role "canyon terrain and river reference" `
  --size "2048x1152" `
  --quality "high" `
  --timeout 0 `
  --out ".\outputs\huajiang-canyon-bridge-overhead.png"
```

Useful options:

- `--model gpt-image-2`
- `--mode auto|generate|edit`
- `--size 2048x1152` script default 2K landscape
- `--size 1024x1024`
- `--size 1536x1024`
- `--size 1024x1536`
- `--size 2048x2048`
- `--size 3840x2160`
- `--size auto` for official API auto sizing
- `--quality low|medium|high|auto`
- `--n 1`
- `--image <path>` repeated up to 16 times
- `--image-role <role>` to label input images inside the prompt
- `--mask <path>` for localized edits
- `--background auto|opaque` for official `gpt-image-2`
- `--output-format png|jpeg|webp`
- `--output-compression 0-100` for `jpeg` or `webp`
- `--input-fidelity low|high` for supported edit models only; do not send it for `gpt-image-2`
- `--moderation auto|low` for supported GPT image models
- `--prompt-file <path>` for one prompt per non-empty line
- `--codex-home <path>`
- `--base-url <https://provider.example/v1>` temporary Provider URL override
- `--api-key-env <ENV_NAME>` temporary API key override from an environment variable
- `--api-key <key>` temporary direct API key override, only when explicitly provided
- `--timeout 1800`
- `--timeout 0`

## Payload Shape

Use the provider's generation endpoint with this body shape:

```json
{
  "model": "gpt-image-2",
  "prompt": "你的中文或英文提示词",
  "size": "2048x1152",
  "quality": "high",
  "n": 1
}
```

Use the provider's edit endpoint as multipart form data:

```text
model=gpt-image-2
prompt=<edit or reference prompt>
image[]=@source-or-reference.png
mask=@mask.png
size=1024x1024
quality=high
n=1
```

Start with `n=1`. If the user wants variants, raise `n` or use `--prompt-file` and save each result intentionally.

## Temporary Provider Overrides

If the user says in natural language that this image job should use a different Provider URL or API key, treat it as a temporary runtime override:

```powershell
$env:API_IMAGE_API_KEY = "<temporary key>"
python "<skill-dir>\scripts\generate_image.py" `
  --prompt "一张赛博朋克风格的夜景照片" `
  --base-url "https://provider.example/v1" `
  --api-key-env "API_IMAGE_API_KEY" `
  --out ".\outputs\override-provider.png"
```

Rules:

- Default to the Codex root configuration when no override is requested.
- Do not modify `auth.json` or `config.toml` for temporary overrides.
- Do not echo API keys back to the user.
- Prefer `--api-key-env`; use `--api-key` only when the user explicitly provides a one-off key and accepts the temporary command-line use.

## gpt-image-2 API Notes

For official OpenAI `gpt-image-2`:

- Text-only generation uses `POST /v1/images/generations` with JSON.
- Any input image, reference image, or mask uses `POST /v1/images/edits` with multipart form-data.
- Use repeated `image[]=@path` fields for multiple input/reference images.
- When using `mask`, the first `--image` must be the edit target; additional images should be references or compositing sources.
- Read image bytes from `data[].b64_json`; URL output is not supported for official GPT Image models.
- Do not send `input_fidelity`; `gpt-image-2` always processes image inputs at high fidelity.
- Do not request `background: transparent`; official `gpt-image-2` currently supports `auto` or `opaque`, not transparent backgrounds.
- For masked edits, validate that the mask and first source image have the same dimensions and compatible format, are under the image API file-size limit, and that the mask includes an alpha channel.

## Capability Map

- New text-to-image generation: supported through `/images/generations`.
- Batch generation: supported through `--n` for multiple variants per prompt, or `--prompt-file` for many prompts.
- Reference-image generation: supported through `/images/edits` with one or more `--image` inputs and role labels in the prompt.
- Image editing: supported through `/images/edits` with `--image` and an edit prompt.
- Localized edits / inpainting: supported through `/images/edits` with `--image` plus `--mask`.
- Background replacement: supported as an edit prompt, with `--mask` when the replacement area must be constrained.
- Style transfer: supported as reference-image editing; label the source image role and describe the desired style in the prompt.
- Input image role labeling: not a separate API field; this script appends `--image-role` labels to the prompt so the model can interpret each input image intentionally.
- Transparent background: official `gpt-image-2` does not currently support `background: transparent`. Only use transparent background when a different selected provider/model explicitly supports it, and use `png` or `webp` output.

## Research And References

Do not assume the image model knows every subject accurately. Research first or use references when the subject is not common visual knowledge.

Reference images are the preferred path for visually constrained research-required tasks. Text research describes facts; reference images carry visual structure. Use both whenever feasible.

Research-required examples:

- A named structure or location, such as `贵州花江峡谷大桥` or any real bridge, landmark, terrain, skyline, or building.
- A real product, vehicle, machine, UI, logo-free product silhouette, game asset from a known franchise, or fashion item.
- A historical scene, cultural garment, uniform, heraldry, ritual object, weapon, architecture style, organism, map, technical diagram, or scientific subject.
- A current or recently changed subject.
- A niche visual style or artist-adjacent style where references are necessary to avoid generic output.

Research workflow:

- Search the web for factual text details when structure, function, history, geography, or current status matters.
- Use image search or provided images for visual details such as shape, terrain, materials, proportions, colors, and surrounding environment.
- For named structures, real locations, real products, real vehicles, historical/cultural visual subjects, technical diagrams, and niche styles, actively collect at least one useful reference image before generating.
- Prefer multiple complementary references when possible: one for subject structure, one for surrounding environment, and one for desired camera angle/composition.
- Download reference images to a local working path before invoking the script, then pass them with `--image` and `--image-role`.
- If a reference image is low quality but still useful, label its role narrowly, for example `rough terrain reference only`.
- Extract only the details needed for the prompt; keep the prompt concise.
- Include factual constraints in the prompt, for example bridge type, deck/tower/cable arrangement, canyon terrain, river position, viewpoint, and surrounding landforms.
- Cite sources in the final response whenever web research was used.

Reference workflow:

- Prefer provided reference images over memory when visual fidelity matters.
- For each `--image`, pass a matching `--image-role` such as `edit target`, `style reference`, `composition reference`, `product reference`, or `terrain reference`.
- Do not treat every image as an edit target; decide whether it is reference-only or should be preserved and modified.
- For compositing, state exactly what comes from each input and how lighting, perspective, scale, and shadows should match.
- For reference-only generation, prompt the model to create a new image based on the references, not to copy a single source photo exactly.
- If the image model/provider rejects a reference-image edit request, surface that error and then decide whether a text-only generation is acceptable for this task. Do not silently fall back.

## Prompt Structure

Use this compact schema when it helps:

```text
Use case: <photorealistic-natural|product-mockup|ui-mockup|infographic-diagram|logo-brand|illustration-story|stylized-concept|historical-scene|text-localization|identity-preserve|precise-object-edit|lighting-weather|background-extraction|style-transfer|compositing|sketch-to-render>
Asset type: <where the image will be used>
Primary request: <user request>
Research facts / visual references: <only the relevant observed details>
Input images: <Image 1: role; Image 2: role>
Scene/backdrop: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <viewpoint, lens/framing, placement>
Lighting/mood: <lighting and mood>
Materials/textures: <surface details>
Text (verbatim): "<exact text if needed>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

## Waiting Behavior

- This script is synchronous. It does not return before the provider finishes the image job or an explicit error occurs.
- Default timeout is `1800` seconds so long-running jobs are not cut off too early.
- Use `--timeout 0` to disable the client-side timeout and wait indefinitely for the provider response.
- When invoking this script from Codex, give the shell command a timeout that is longer than the expected image job. Do not use a short shell timeout for long generations.

## Size And Quality

Follow the current official GPT Image rules for `gpt-image-2`:

- `size` can be `auto` or any `<width>x<height>` string that satisfies all of these:
- width and height are multiples of `16`
- the longest edge is at most `3840`
- the long-edge to short-edge ratio is at most `3:1`
- total pixels are between `655,360` and `8,294,400`
- this script defaults to `2048x1152`; the official API's default sizing behavior is `auto`
- common examples: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`
- `quality` can be `low`, `medium`, `high`, or `auto`; this script defaults to `high`, while official API auto quality is available with `auto`
- 2K and 4K requests are valid when they satisfy those constraints
- Do not silently coerce unsupported sizes. Raise a clear error instead.

## Prompting

- Prefer concrete prompts with subject, style, lighting, and composition.
- Use the user's language by default. Chinese prompts are valid for this workflow.
- Change one aspect at a time when iterating.

## Output Rules

- Save project assets inside the project workspace when the user wants a usable asset.
- Save preview images to a clear temporary or user-requested path.
- If `n > 1`, keep filenames deterministic by appending `-1`, `-2`, and so on.

## Failure Rules

- Raise explicit errors when `OPENAI_API_KEY`, `model_provider`, or `base_url` cannot be found.
- Allow temporary Provider overrides with `--base-url`, `--api-key-env`, or `--api-key`; do not persist them unless explicitly requested.
- Raise explicit errors when both `--api-key` and `--api-key-env` are provided, when the named environment variable is empty, or when `--base-url` is not an HTTP(S) URL.
- Raise explicit errors when `size` violates the official GPT Image constraints or `quality` is unsupported.
- Raise explicit errors when edit/reference mode is requested without input images.
- Raise explicit errors when `gpt-image-2` is used with `--background transparent` or `--input-fidelity`.
- Raise explicit errors when a mask is not compatible with the first `--image` edit target, has different dimensions, lacks an alpha channel, or exceeds the image API file-size limit.
- Surface provider errors directly. Do not fabricate a success result.
- If the provider uses a different image model name on this machine, override `--model`.

## Resource

- `scripts/generate_image.py`: Read the current user's Codex root files, call the configured provider's image endpoint, and save the returned image data.
