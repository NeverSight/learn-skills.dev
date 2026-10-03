---
name: novelai-workflows
description: "Chain NovelAI tools into creative pipelines: txt2img to upscale, annotate to img2img, Director edits, full production. Use when asked to build multi-step image workflow recipes or pipelines."
---

# novelai-workflows

Instructions for the agent to follow when chaining NovelAI tools into multi-step creative pipelines.

## When to use

Use this skill when the user asks for a multi-step image pipeline or workflow recipe — e.g. generate then upscale for higher resolution, build a ControlNet-style pipeline (txt2img → annotate → img2img), apply Director edits to an existing image (img2img → director), or run a full end-to-end production flow (txt2img → director → upscale). It covers how to wire the 11 NovelAI MCP tools and the matching CLI commands into chains. For individual tool parameters, see the `novelai-mcp-tools` skill; for CLI flags, see the `novelai-cli` skill — do not duplicate those references here.

## Instructions

### Prerequisites

- **Credentials** configured: `NOVELAI_TOKEN` (preferred) or
  `NOVELAI_USERNAME` + `NOVELAI_PASSWORD`.
- **Output directory** writable: `NOVELAI_OUTPUT_DIR` (default `outputs`), or
  pass `-o <dir>` per CLI invocation.
- **MCP**: a connected MCP host (Claude Desktop, Cline, or `mcp dev
  apps/server/dev_server.py`). **CLI**: `novelai-image-mcp` on `PATH` (or
  `uvx novelai-image-mcp`, or
  `uv run --directory apps/server novelai-image-mcp`).
- **Check Anlas balance before expensive chains** — call `get_subscription`
  (MCP) or `novelai-image-mcp info` (CLI) first. Upscale and Director tools
  cost Anlas proportional to source resolution.

1. **txt2img → upscale** — generate then upscale for higher resolution.

   **Goal**: generate an image, then upscale it for higher resolution than the
   generator produces natively.

   **When to use**: you need a final image larger than the model's native
   output, or you want to refine detail on a low-step draft before committing
   Anlas to a full-resolution render.

   **MCP sequence**:

   1. `generate_image(prompt="...", width=832, height=1216, seed=42)` → returns
      `ImageContent` + path like `outputs/generate-<ts>.png`.
   2. Read that PNG, base64-encode it, and call
      `upscale_image(image="<base64>", factor=4)` → returns the 4× PNG
      (`outputs/upscale-<ts>.png`).

   The model is irrelevant to upscale — the upscaler is model-independent.

   **CLI sequence**:

   ```bash
   IMG=$(novelai-image-mcp generate -p "a serene mountain lake at dawn" --seed 42 | tail -n1)
   novelai-image-mcp upscale "$IMG" -f 4
   ```

   **Notes**:

   - `factor` must be `2` or `4`. 4× on a large source yields a very large PNG —
     verify the Anlas budget first.
   - Upscale hits the legacy `api.novelai.net` host (`/ai/upscale`); the client
     routes this automatically. Do not override
     `NOVELAI_LEGACY_IMAGE_BASE_URL` to `image.novelai.net` or it 404s.
   - Generate at the model's native aspect ratio first; upscaling does not
     change aspect ratio.

2. **txt2img → annotate → img2img (ControlNet)** — extract a structural annotation and use it as the input image for a styled img2img pass.

   **Goal**: generate a base image, extract a structural annotation (line art,
   depth, scribble), then use that annotation as the input image for an img2img
   pass to create a styled variation that preserves the original composition.

   **When to use**: you want to keep the composition / pose / structure of a
   generated image but re-render it in a different style, palette, or medium
   (e.g. turn a photo render into line-art-guided watercolor).

   **MCP sequence**:

   1. `generate_image(prompt="<base composition>")` →
      `outputs/generate-<ts>.png`.
   2. Read the PNG, base64-encode, and call
      `annotate_image(image="<base64>", model="hed")` →
      `outputs/annotate-hed-<ts>.png`. Choose the preprocessor by what you want
      to preserve:
      - `hed` — soft edges (palette swap / general structure)
      - `midas` — depth (form lock / 3D structure)
      - `fake_scribble` — scribbles
      - `mlsd` — straight lines (architecture)
      - `uniformer` — segmentation (landscapes)
   3. Read the annotation PNG, base64-encode, and call
      `image_to_image(prompt="<new style>", image="<base64-of-annotation>",
      strength=0.6)` → `outputs/img2img-<ts>.png`. Higher `strength` (0.01–0.99)
      diverges further from the annotation; lower `strength` stays closer to it.

   **CLI sequence**:

   The CLI does **not** expose `image_to_image` — only `generate`, `upscale`,
   `director`, `annotate`, `info`. So this workflow is **MCP-only for the final
   img2img step**. You can still do the first two steps from the shell:

   ```bash
   BASE=$(novelai-image-mcp generate -p "a girl reading under cherry blossoms" | tail -n1)
   ANNOT=$(novelai-image-mcp annotate "$BASE" -m hed)
   # Then switch to an MCP host (or `mcp dev apps/server/dev_server.py`) for the img2img pass:
   #   image_to_image(prompt="watercolor painting, soft pastels", image=<base64 of $ANNOT>, strength=0.6)
   ```

   **Notes**:

   - `annotate_image` lives on the legacy `api.novelai.net` host
     (`/ai/annotate-image`); routed automatically.
   - The annotation is used as a normal `image` input to `image_to_image`.
     There is no separate "controlnet condition" field on the MCP tool — the
     annotation **is** the input image.
   - Match the img2img `model` to the annotation domain. A `hed` line-art
     annotation pairs well with anime models; `midas` depth pairs well with
     photorealistic re-styling.

3. **img2img → director** — apply a Director tool to an existing image, optionally pre-edited with img2img.

   **Goal**: take an existing image (optionally pre-edited with img2img), then
   apply a NovelAI Director tool — line art extraction, background removal,
   sketch, colorize, emotion, or declutter.

   **When to use**: extracting line art from photos, removing backgrounds to
   isolate a subject, colorizing black-and-white source material, or applying an
   emotion to a portrait. The optional img2img pre-step lets you restyle before
   the Director pass.

   **MCP sequence**:

   1. (Optional) `image_to_image(prompt="<pre-edit style>",
      image="<base64-source>", strength=0.4)` → `outputs/img2img-<ts>.png`.
   2. Read the resulting PNG (or use the source directly), base64-encode, and
      call `director_tool(tool="lineart", image="<base64>", defry=3)` →
      `outputs/director-lineart-<ts>.png`.

   `tool` is one of: `lineart`, `sketch`, `bg-removal`, `declutter`,
   `colorize`, `emotion`. Per-tool extras:

   - `lineart` / `sketch` — `defry` (0–10) sharpens lines.
   - `colorize` — `prompt` guides the color palette.
   - `emotion` — **requires** `emotion` (e.g. `"happy"`) and accepts
     `emotion_level` (0–5; 0 = normal intensity, 5 = weakest).
   - `bg-removal` / `declutter` — no extra params.

   **CLI sequence**:

   ```bash
   # Line art from a photo, with sharpening
   novelai-image-mcp director lineart ./photo.png --defry 5

   # Background removal → transparent PNG
   novelai-image-mcp director bg-removal ./subject.png -o ./transparent

   # Colorize a black-and-white photo with a warm palette
   novelai-image-mcp director colorize ./bw.png -p "warm afternoon tones"

   # Apply an emotion to a portrait
   novelai-image-mcp director emotion ./portrait.png --emotion happy --emotion-level 2

   # Optional pre-edit via img2img is MCP-only (no CLI command for img2img).
   ```

   Chain two Director tools by capturing the path:

   ```bash
   LINEART=$(novelai-image-mcp director lineart ./photo.png)
   novelai-image-mcp director colorize "$LINEART" -p "soft pastel palette"
   ```

   **Notes**:

   - Director tools hit `image.novelai.net` (the migrated host). No legacy
     routing needed here.
   - `bg-removal` returns a PNG with transparency — suitable for compositing.
   - `emotion` requires the `emotion` name; both CLI and MCP enumerate the
     accepted values in the error if you pass an unknown one.

4. **txt2img → director → upscale** — complete pipeline from text prompt to polished high-resolution output.

   **Goal**: complete creative pipeline from a text prompt to a polished
   high-resolution output, with a Director transformation in the middle.

   **When to use**: end-to-end production — e.g. generate a scene, extract line
   art, then upscale the line art to 4× for print; or generate a subject,
   remove its background, and upscale the cutout for a poster.

   **MCP sequence**:

   1. `generate_image(prompt="<scene>")` → `outputs/generate-<ts>.png`.
   2. Read PNG, base64-encode, call
      `director_tool(tool="lineart", image="<base64>", defry=4)` →
      `outputs/director-lineart-<ts>.png`.
   3. Read that PNG, base64-encode, call
      `upscale_image(image="<base64>", factor=4)` →
      `outputs/upscale-<ts>.png`.

   **CLI sequence**:

   ```bash
   GEN=$(novelai-image-mcp generate -p "a cathedral interior, dramatic light" | tail -n1)
   DIR=$(novelai-image-mcp director lineart "$GEN" --defry 4)
   novelai-image-mcp upscale "$DIR" -f 4
   ```

   Or as a one-liner relying on glob prefixes:

   ```bash
   novelai-image-mcp generate -p "a cathedral interior, dramatic light" && \
   novelai-image-mcp director lineart "$(ls -t outputs/generate-*.png | head -n1)" --defry 4 && \
   novelai-image-mcp upscale "$(ls -t outputs/director-lineart-*.png | head -n1)" -f 4
   ```

   **Notes**:

   - Each step's output filename is prefixed with the operation name
     (`generate-`, `director-lineart-`, `upscale-`), so globbing by prefix is
     reliable. Use `ls -t | head -n1` to grab the most recent.
   - This chain crosses both hosts: `generate` → `image.novelai.net`,
     `director` → `image.novelai.net`, `upscale` → `api.novelai.net` (legacy).
     The client handles routing; do not override the legacy base URL.
   - **Budget check first**: this chain spends Anlas three times (generate +
     director + upscale). Call `get_subscription` / `info` ahead of time if the
     balance is uncertain.

### How tools link together

Two linking mechanisms, depending on which surface you drive.

#### MCP (interactive agent session)

Every image-producing tool returns a list with two content blocks:
`[ImageContent, "Saved image: <absolute-path>"]` (or
`"Saved N image(s): [...]"` for `generate_image` / `image_to_image` /
`inpaint`). The next tool in the chain needs the image as a **base64-encoded
string** in its `image` parameter. Two ways to obtain it:

1. Read the saved PNG from the returned path and base64-encode it, then pass
   it to the next tool's `image` argument.
2. Use the base64 payload already inside the `ImageContent` block returned by
   the previous call.

Both are valid; the agent typically uses the path because it is plain text in
the response. The MCP server keeps a **pooled `NovelAIClient`** alive across
tool calls (via the server lifespan), so chained MCP calls reuse one TLS
session — faster than re-handshaking per call.

#### CLI (shell)

Every image-producing subcommand prints the absolute path of each saved PNG
to stdout (one per line; `generate --n-samples N` prints N lines). Chain by
capturing stdout:

```bash
IMG=$(novelai-image-mcp generate -p "..." | tail -n1)   # last of N samples
UP=$(novelai-image-mcp upscale "$IMG" -f 4)
```

Or glob by operation-name prefix (filenames are timestamped, e.g.
`generate-20260728-153012-001.png`, `director-lineart-20260728-160001.png`,
`annotate-hed-20260728-160215.png`, `upscale-20260728-160045.png`):

```bash
novelai-image-mcp upscale "$(ls -t outputs/generate-*.png | head -n1)" -f 4
```

The CLI builds a **fresh `httpx.AsyncClient` per invocation** (no shared
session), so each step re-handshakes with NovelAI. For 3+ step chains, MCP's
pooled session is noticeably faster.

### CLI vs MCP

| Reach for **CLI** when… | Reach for **MCP** when… |
|---|---|
| Shell script, CI/CD, cron, batch processing | Interactive agent session (Claude Desktop, Cline) |
| Automation with no LLM in the loop | The agent needs to **see** intermediate images (`ImageContent`) |
| Quick one-off generation | Multi-step conversation with real-time parameter exploration |
| Reproducible pipelines checked into git | The agent decides the next step based on the previous image |
| You only need disk paths back | You want the agent to inspect and iterate on each result |

**Key difference**: MCP returns `ImageContent` (the agent sees the image)
**and** the disk path; CLI returns only the disk path. If the next decision
depends on what the image looks like, use MCP.

**Performance difference**: the MCP server keeps a pooled `NovelAIClient`
alive across tool calls (one TLS session); the CLI builds a fresh
`httpx.AsyncClient` per invocation (re-handshake every step). For 3+ step
chains, MCP is faster. The CLI is fine for 1–2 step scripts.

**Coverage difference**: the CLI exposes `generate`, `upscale`, `director`,
`annotate`, and `info` (subscription) — but **not** `image_to_image`,
`inpaint`, `suggest_tags`, `encode_vibe`, `get_user_data`, or
`estimate_anlas_cost`. Any chain involving img2img or inpaint is MCP-only.

### Chaining gotchas

- **Base64 between MCP calls**: `image_to_image`, `inpaint`, `upscale_image`,
  `director_tool`, and `annotate_image` all take a base64-encoded `image`
  string. The `ImageContent` block from the previous call contains base64
  already; alternatively re-encode the saved PNG. Either works.
- **CLI path capture**: `generate --n-samples N` prints N lines. Use
  `| tail -n1` to pick the last sample, or drop the flag (default 1) for a
  single path.
- **Output filenames are timestamped** with the operation prefix
  (`generate-`, `img2img-`, `inpaint-`, `upscale-`, `director-<tool>-`,
  `annotate-<model>-`). Globbing by prefix + `ls -t | head -n1` is the robust
  way to grab "the most recent output of step X".
- **Reproducibility**: pass `--seed` (CLI) or `seed` (MCP) on `generate` /
  `image_to_image` to make the upstream end of a chain reproducible. Director
  and upscale tools are deterministic given their input.
- **Output directory**: `-o <dir>` (CLI) overrides `NOVELAI_OUTPUT_DIR` for
  one invocation without mutating the env. Use it to keep each pipeline run
  in its own folder: `-o ./runs/exp-01`.
- **Two hosts**: `upscale` and `annotate` hit legacy `api.novelai.net`; all
  other image tools hit `image.novelai.net`. The client routes correctly —
  do not override `NOVELAI_LEGACY_IMAGE_BASE_URL` to `image.novelai.net` or
  the legacy endpoints 404.
- **Cost awareness**: every generate / img2img / inpaint / upscale / director
  call spends Anlas. Before a 3-step chain, check the balance with
  `get_subscription` (MCP) or `novelai-image-mcp info` (CLI). For a
  no-API-call estimate of a single generation's cost, use
  `estimate_anlas_cost` (MCP only).

### Source reference

- Tool implementations: `apps/server/src/novelai_image_mcp/tools/generate.py`,
  `apps/server/src/novelai_image_mcp/tools/enhance.py`
- CLI: `apps/server/src/novelai_image_mcp/cli.py`
- Save/return helper (image return contract): `_save_and_return` in
  `tools/generate.py` and `tools/enhance.py`
- Output naming: `apps/server/src/novelai_image_mcp/output.py`
- Endpoint routing (legacy vs migrated host):
  `apps/server/src/novelai_image_mcp/nai/constants.py`
- Companion skills: `skills/novelai-mcp-tools/SKILL.md` (tool reference),
  `skills/novelai-cli/SKILL.md` (CLI reference)
