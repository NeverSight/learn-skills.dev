---
name: novelai-cli
description: Run the novelai-image-mcp Typer CLI to generate, upscale, and transform NovelAI images from a shell. Use when scripting image workflows outside an MCP host or batch-generating images.
---

# novelai-cli

Instructions for the agent to follow when driving the NovelAI image CLI from a shell.

## When to use

Use this skill when driving NovelAI image generation from a shell script, CI job, or one-off command instead of through an MCP host like Claude Desktop. The `novelai-image-mcp` package ships a Typer-based sync CLI (entry point: `novelai-image-mcp`) that wraps the same async `NovelAIClient` the MCP server uses. This skill covers the CLI only — for the MCP tool interface (the 11 registered tools exposed over stdio / streamable-http), see the `novelai-mcp-tools` skill instead, and do not duplicate that reference here.

## Instructions

1. Install the CLI — see [Installation](#installation).
2. Configure credentials — see [Credentials](#credentials).
3. Run a command — see [Commands](#commands) for the six subcommands (`serve`, `generate`, `upscale`, `director`, `annotate`, `info`).
4. Read the output — see [Output behavior](#output-behavior).

### Installation

```bash
# From PyPI
pip install novelai-image-mcp

# Or run ad-hoc without installing
uvx novelai-image-mcp <command>

# From source (monorepo)
uv sync
uv run --directory apps/server novelai-image-mcp <command>
```

### Credentials

The CLI needs exactly one auth method configured via environment variables
(see `.env.example`):

- **Preferred** — `NOVELAI_TOKEN`: a persistent API token. Get it from
  <https://novelai.net> > Account (the `pst-...` string).
- **Fallback** — `NOVELAI_USERNAME` + `NOVELAI_PASSWORD`: the access key is
  derived with argon2id. Requires `argon2-cffi` (a core dependency).

If neither is set, every command (except `serve` without credentials loaded)
exits with code 2 and prints a reminder. Set credentials inline for one-shot
use:

```bash
export NOVELAI_TOKEN=pst-xxxxxxxxxxxxxxxx
novelai-image-mcp info
```

#### Useful environment variables

All are optional; defaults shown.

| Variable | Default | Purpose |
|---|---|---|
| `NOVELAI_TOKEN` | — | API token (preferred auth) |
| `NOVELAI_USERNAME` / `NOVELAI_PASSWORD` | — | Alt auth (derived) |
| `NOVELAI_OUTPUT_DIR` | `outputs` | Where PNGs are saved |
| `NOVELAI_DEFAULT_MODEL` | `nai-diffusion-4-5-full` | Default model id |
| `NOVELAI_DEFAULT_WIDTH` / `NOVELAI_DEFAULT_HEIGHT` | `832` / `1216` | Default size |
| `NOVELAI_DEFAULT_STEPS` | `28` | Default step count |
| `NOVELAI_DEFAULT_SCALE` | `5.0` | Default CFG scale |
| `NOVELAI_DEFAULT_SAMPLER` | `k_euler_ancestral` | Default sampler |
| `NOVELAI_TIMEOUT` | `120` | HTTP timeout (seconds) |
| `MCP_TRANSPORT` | `stdio` | `serve` transport (`stdio` or `streamable-http`) |
| `MCP_HOST` / `MCP_PORT` | `127.0.0.1` / `8000` | `serve` HTTP bind |

### Commands

The CLI exposes six subcommands. Run `novelai-image-mcp --help` or
`novelai-image-mcp <command> --help` for the authoritative flag list.

#### `serve` — run the MCP server

```bash
novelai-image-mcp serve                              # stdio (default)
novelai-image-mcp serve --transport streamable-http  # → http://127.0.0.1:8000/mcp
novelai-image-mcp serve -t streamable-http --host 0.0.0.0 --port 9000
```

Flags:

- `--transport, -t` — `stdio` (default) or `streamable-http`. Overrides `MCP_TRANSPORT`.
- `--host` — bind host for HTTP mode. Overrides `MCP_HOST`.
- `--port` — bind port for HTTP mode. Overrides `MCP_PORT`.

Use this when integrating with Claude Desktop, Cline, or a remote MCP client.
For one-off image work, prefer the dedicated subcommands below — they avoid
the MCP SDK import cost and surface credential errors immediately.

#### `generate` — text-to-image

```bash
novelai-image-mcp generate \
  --prompt "a girl reading under cherry blossoms, soft light" \
  --negative "lowres, bad anatomy, watermark" \
  --model nai-diffusion-4-5-full \
  --width 832 --height 1216 \
  --steps 28 --scale 5.0 \
  --sampler k_euler_ancestral \
  --seed 0 \
  --n-samples 4 \
  --output-dir ./batch
```

Flags:

- `--prompt, -p` (required) — text prompt.
- `--negative, -n` — negative prompt. Default empty.
- `--model, -m` — model id. Falls back to `NOVELAI_DEFAULT_MODEL`.
- `--width` / `--height` — pixel size, multiple of 64. Default `832` / `1216`.
- `--steps` — sampling steps (1–50). Default `28`.
- `--scale` — CFG scale (>0, ≤20). Default `5.0`.
- `--sampler` — sampler id. Default `k_euler_ancestral`.
- `--seed` — RNG seed. `0` (default) means random.
- `--n-samples` — number of images (1–8). Default `1`.
- `--output-dir, -o` — override `NOVELAI_OUTPUT_DIR` for this invocation.

Valid model ids include: `nai-diffusion-4-5-full` (default),
`nai-diffusion-4-5-full-inpainting`, `nai-diffusion-4-5-curated`,
`nai-diffusion-4-5-curated-inpainting`, `nai-diffusion-4-full`,
`nai-diffusion-4-full-inpainting`, `nai-diffusion-4-curated-preview`,
`nai-diffusion-4-curated-inpainting`, `nai-diffusion-3`,
`nai-diffusion-3-inpainting`, `nai-diffusion-furry-3`,
`nai-diffusion-furry-3-inpainting`, `nai-diffusion-5-full`,
`nai-diffusion-5-curated`, `nai-diffusion-5-full-inpainting`.

The CLI prints one absolute path per generated image to stdout (one per line).
Use `-o` to redirect output without touching the env var.

#### `upscale` — 2× or 4× upscale

```bash
novelai-image-mcp upscale ./outputs/generate-20260728.png --factor 4
novelai-image-mcp upscale input.jpg -f 2 -o ./upscaled
```

Arguments / flags:

- `image` (positional, required) — path to the PNG/JPEG to upscale.
- `--factor, -f` — `2` or `4`. Default `4`.
- `--output-dir, -o` — override `NOVELAI_OUTPUT_DIR`.

Note: `/ai/upscale` lives on the legacy Primary API (`api.novelai.net`), not
`image.novelai.net`. The client handles this automatically via
`NOVELAI_LEGACY_IMAGE_BASE_URL` — do not point that at `image.novelai.net`.

#### `director` — Director tools

```bash
# Extract line art
novelai-image-mcp director lineart ./photo.png

# Convert to sketch with extra sharpening
novelai-image-mcp director sketch ./photo.png --defry 5

# Remove background
novelai-image-mcp director bg-removal ./subject.png -o ./transparent

# Colorize a black-and-white photo
novelai-image-mcp director colorize ./bw.png --prompt "warm afternoon tones"

# Apply an emotion (requires --emotion)
novelai-image-mcp director emotion ./portrait.png --emotion happy --emotion-level 2
```

Arguments / flags:

- `tool` (positional, required) — one of: `lineart`, `sketch`, `bg-removal`,
  `declutter`, `colorize`, `emotion`.
- `image` (positional, required) — path to the input image.
- `--prompt, -p` — guides `colorize` and `emotion`. Default empty.
- `--defry` — line-art sharpening (0–10). Default `0`. Only meaningful for
  `lineart` / `sketch`.
- `--emotion` — emotion name. **Required when `tool=emotion`.** One of:
  `neutral`, `happy`, `sad`, `angry`, `scared`, `surprised`, `tired`,
  `excited`, `nervous`, `thinking`, `confused`, `shy`, `disgusted`, `smug`,
  `bored`, `laughing`, `irritated`, `aroused`, `embarrassed`, `worried`,
  `love`, `determined`, `hurt`, `playful`.
- `--emotion-level` — emotion intensity (0–5). `0` is normal intensity; `5`
  is weakest. Only meaningful for `emotion`.
- `--output-dir, -o` — override `NOVELAI_OUTPUT_DIR`.

#### `annotate` — ControlNet preprocessor

```bash
novelai-image-mcp annotate ./photo.png --model hed
novelai-image-mcp annotate sketch.png -m mlsd -o ./controlnet
```

Arguments / flags:

- `image` (positional, required) — path to the input image.
- `--model, -m` (required) — ControlNet preprocessor. One of: `hed`
  (palette swap / soft edges), `midas` (form lock / depth), `fake_scribble`
  (scribbler), `mlsd` (building control / straight lines),
  `uniformer` (landscaper / segmentation).
- `--output-dir, -o` — override `NOVELAI_OUTPUT_DIR`.

Note: `/ai/annotate-image` also lives on the legacy Primary API
(`api.novelai.net`). The client routes it correctly via
`NOVELAI_LEGACY_IMAGE_BASE_URL`.

#### `info` — account subscription and Anlas balance

```bash
novelai-image-mcp info
```

No flags. Prints the account subscription payload as pretty-printed JSON to
stdout — useful for verifying credentials and checking remaining Anlas before
a large batch. Example shape:

```json
{
  "active": true,
  "trainingStepsLeft": { "fixedTrainingStepsLeft": 10000, ... },
  "perks": { ... },
  "subscription": { "tier": "All-Access", ... }
}
```

### Output behavior

- Every image-producing command (`generate`, `upscale`, `director`, `annotate`)
  saves a PNG to `NOVELAI_OUTPUT_DIR` (default `outputs`, created if missing)
  and prints the absolute path to stdout.
- `generate --n-samples N` prints one path per line, in generation order.
- Output filenames are timestamped with the operation name, e.g.
  `generate-20260728-153012-001.png`, `upscale-20260728-153045.png`,
  `director-lineart-20260728-160001.png`, `annotate-hed-20260728-160215.png`.
- `-o` / `--output-dir` overrides the directory for a single invocation
  without mutating the environment.
- The CLI constructs a fresh `httpx.AsyncClient` + `NovelAIClient` per
  invocation (no shared session). For long-lived multi-tool workflows, prefer
  `serve` — the MCP server keeps a pooled client alive across tool calls.

### Common patterns

#### Override output dir without env vars

```bash
novelai-image-mcp generate -p "cyberpunk city, neon rain" -o ./runs/exp-01
```

#### Batch generate with a fixed seed for reproducibility

```bash
novelai-image-mcp generate -p "study, 1girl, reading" --seed 42 --n-samples 8 -o ./study-batch
```

#### Pick a different model

```bash
novelai-image-mcp generate -p "furry character ref" -m nai-diffusion-furry-3
novelai-image-mcp generate -p "fast preview" -m nai-diffusion-4-5-curated
```

#### Chain generate → upscale → annotate

```bash
IMG=$(novelai-image-mcp generate -p "portrait, studio light" | tail -n1)
UP=$(novelai-image-mcp upscale "$IMG" -f 4)
novelai-image-mcp annotate "$UP" -m midas -o ./controlnet
```

#### Verify credentials before a long run

```bash
novelai-image-mcp info | jq '.subscription.tier'
```

### Troubleshooting

- **Exit code 2 with "NovelAI credentials are not configured"** — set
  `NOVELAI_TOKEN` (preferred) or `NOVELAI_USERNAME` + `NOVELAI_PASSWORD`.
- **Unknown model / director tool / emotion / controlnet model** — the CLI
  prints the accepted values in the error message. Use exactly those strings.
- **Connection reset / Cloudflare WAF block** — the client uses
  `curl_cffi` with a Chrome TLS fingerprint by design; do not bypass
  `create_http_client()`. If you see TLS errors, ensure `curl_cffi` is
  installed and up to date (`uv sync`).
- **`/ai/upscale` or `/ai/annotate-image` 404** — these endpoints are on
  `api.novelai.net`, not `image.novelai.net`. Do not override
  `NOVELAI_LEGACY_IMAGE_BASE_URL` to point at `image.novelai.net`.

### Source reference

- CLI implementation: `apps/server/src/novelai_image_mcp/cli.py`
- Settings / env vars: `apps/server/src/novelai_image_mcp/settings.py`
- Enum values (models, tools, emotions, controlnet): `apps/server/src/novelai_image_mcp/nai/constants.py`
- Install / quickstart: `apps/server/README.md`
- Env var template: `.env.example`
