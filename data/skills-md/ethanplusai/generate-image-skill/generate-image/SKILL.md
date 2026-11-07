---
name: generate-image
description: "Generate original images for websites and apps (hero images, backgrounds, textures, spot illustrations, og:images, product shots, transparent cut-outs, edits of an existing image) and show them in the chat. Uses Codex's built-in image generation on the user's ChatGPT plan when the Codex CLI is signed in (no API key, no model download). Falls back to local FLUX.1-schnell on Apple Silicon, or to a hosted API key. Use whenever a project needs real imagery instead of stock photos, gray boxes, or placeholder URLs, or when the user asks Claude to 'make an image' or 'use Codex to generate an image'."
---

# generate-image: images for coding agents, handed back into the chat

Generate production-ready imagery while you build, then show it to the user.
Images are saved straight into the project as exact-size `.webp`/`.png`/`.jpg`.

## Backends: who actually makes the pixels

| Backend | What it is | Cost | Needs |
|---|---|---|---|
| `codex` (**default when available**) | Codex CLI's built-in `image_gen` tool (OpenAI's GPT Image) | the user's ChatGPT plan | `codex` installed and `codex login` with ChatGPT |
| `local` | FLUX.1-schnell via mflux | free, offline | Apple Silicon Mac, ~7 GB one-time model download |
| `openai` / `gemini` / `replicate` | hosted APIs | per image, on the user's API account | a key stored with `--set-key` |

`--backend auto` (the default) picks `codex` if Codex is signed in with ChatGPT,
otherwise `local`. You (Claude) cannot call Codex's image tool directly; this
skill runs `codex exec` headless for you, then collects the finished file from
`~/.codex/generated_images/` and crops it to the exact size you asked for.

## When to use and when NOT to

**Generate:** hero images, section backgrounds, textures, spot illustrations,
og:images (1200x630), product/editorial photography, empty-state art,
transparent cut-outs, and edits or variations of an existing image.

**Don't generate:** logos, icons, and UI screenshots. Use SVG for logos and
icons, and real screenshots for UI. On `codex` a short headline in the image
renders well. On `local` (FLUX), keep legible text to 1–2 words at most. In
both cases, put real page copy in HTML/CSS over the image.

## Setup: do this first (once per session)

```bash
python3 <SKILL_DIR>/scripts/doctor.py
```

It needs only the system `python3`. Act on what it reports; don't make the
user troubleshoot:

- **`! Codex CLI not installed` / `not signed in with ChatGPT`**: if the user
  has a ChatGPT plan, this is the best backend. Offer `npm install -g
  @openai/codex`. The sign-in (`codex login`) opens a browser, so the **user**
  runs it themselves.
- **`✗ uv is not installed`**: offer `brew install uv` (or `curl -LsSf
  https://astral.sh/uv/install.sh | sh`), then re-run the doctor.
- **Local-only items** (`platform`, `disk`, `model not downloaded`) only
  matter for `--backend local`. When Codex is ready they are advisory.

When it says "Ready to generate", go ahead. The doctor also prints the backend
`auto` will use.

## How to run: in the background

The script lives in THIS skill's directory, not the user's project:

```bash
uv run <SKILL_DIR>/scripts/generate.py "PROMPT" --out public/hero.webp --size 1440x800 --json
```

**Run it as a background task.** If you have a background option (Claude
Code: Bash with `run_in_background: true`), use it. You'll be notified when it
exits, so keep working meanwhile and don't poll. Timing: `codex` takes ~30–60 s
per image; `local` takes ~40–90 s, plus several minutes for the ~7 GB model on
first use. If you must run it in the foreground, set the timeout to at least
10 minutes.

`--json` prints one line per saved image, e.g.
`{"path": "/abs/public/hero.webp", "width": 1440, "height": 800, "seed": 1, "backend": "codex"}`.
Use those absolute paths in the next steps.

## Hand the image back: always do both

1. **Look at it yourself.** Read the image file before wiring it into the page.
   If it's wrong, regenerate with a more concrete prompt; don't ship unseen
   images.
2. **Show it to the user in the chat.** Don't leave a path buried in tool
   output. Use the best option the environment has:
   - **A tool that sends or renders files to the user** (in the Claude desktop
     app: `SendUserFile` with `display: "render"`). This shows the image
     inline, the way Codex does. Prefer this whenever it exists.
   - Otherwise put a markdown image in your reply,
     `![hero](/abs/path/hero.webp)`, **and** the plain absolute path. Orcha and
     most IDE chats turn the path into a clickable link.
   - Terminal-only: `--open` opens results in Preview, and `imgcat <path>`
     (iTerm2) or `kitten icat <path>` (Kitty/Ghostty/WezTerm) render inline.

## Flags

| Flag | Meaning |
|---|---|
| `--out PATH` | Output file; format from extension: `.webp` (best for web), `.png`, `.jpg` |
| `--size WxH` | Exact output pixels, e.g. `1440x800`. The image is cover-cropped to it |
| `--backend` | `auto` (default), `codex`, `local`, `openai`, `gemini`, `replicate` |
| `--transparent` | Real transparent background (`codex` only; `.png` or `.webp` output) |
| `--ref IMAGE` | Reference or edit-source image, repeatable (`codex` only). Say in the prompt how to use it ("edit this photo: replace only the sky") |
| `--count N` | N candidates as `name-1.webp`, `name-2.webp`, … |
| `--batch FILE` | JSON array of `{prompt, out, size, seed?, count?}`. `codex` runs 3 jobs at once; `local` loads the model once |
| `--json` | Machine-readable result line per image |
| `--seed N` | Reproducible output on `local`/`replicate`; `codex` ignores seeds |
| `--steps N`, `--model REPO` | Local FLUX tuning (advanced) |
| `--no-style` | Ignore the project's `imagegen.toml` |
| `--open` | Open each result in the Mac's default viewer |
| `--dry-run` | Print the plan (styled prompts, sizes) without generating |

## Workflow rules

1. **Plan all assets first, then generate them in one `--batch`**, in the
   background.
2. **Generate 1–2 candidates, not 10.** Each `codex` image uses the user's plan
   quota; each `local` image costs about a minute.
3. **Always view, then show** (see "Hand the image back").
4. **Record what you shipped** in the commit message: the prompt, the backend,
   and the seed when the backend supports one.
5. **Set up style once:** if the project has no `imagegen.toml`, consider
   creating one (copy `imagegen.example.toml` from this skill's directory) so
   all assets share an art direction.

## Writing good prompts

Both backends reward specific, concrete descriptions and punish one-word
prompts. Every prompt should cover:

- **Subject**: the concrete thing ("handmade ceramic bowls", not "something nice")
- **Setting**: where it is and what surrounds it
- **Lighting**: direction and quality ("soft morning light from the left")
- **Mood and palette**: the feeling and the colors
- **Composition**: framing and negative space, *especially where text will
  overlay* ("subject on the right third, empty space on the left for a headline")

On `codex`, a short labeled spec works especially well. This is the format
Codex's own image skill uses:

```text
Use case: product-mockup
Asset type: landing page hero
Primary request: a ceramic coffee mug on a linen tablecloth
Style/medium: clean product photography
Composition/framing: wide, mug on the right third, empty space on the left for copy
Lighting/mood: soft window light, calm morning
Constraints: no logos, no watermark
```

For edits with `--ref`, list what must stay the same ("change only the
background; keep the product and its edges unchanged").

**Weak → strong:**

> ❌ `a coffee shop`
> ✅ `warm natural-light photograph of a cozy independent coffee shop interior at golden hour, exposed brick walls, a barista blurred in the background, steam rising from a cup in the foreground, shallow depth of field, inviting mood`

## Choosing dimensions: always set `--size` deliberately

| Asset | Size |
|---|---|
| Full-width hero | `1440x800` (or `2880x1600` for retina) |
| Wide banner strip | `1200x360` |
| Section background | `1440x600` |
| og:image / social card | `1200x630` |
| Square spot illustration | `800x800` |
| Portrait / mobile hero | `800x1200` |

## Hosted API keys (optional)

Only needed for `openai`, `gemini`, or `replicate`. The **user** stores a key
once at a hidden prompt; never ask them to paste a key into the chat:

```bash
uv run <SKILL_DIR>/scripts/generate.py --set-key openai   # or: gemini, replicate
```

The key goes into the macOS Keychain, and the CLI reads it at run time. This
command refuses to run non-interactively, so you can't run it for them.
`--list-keys` shows which providers have a key; `--delete-key <provider>`
removes one.

## Reference

See `reference/prompting.md` in this skill's directory for per-asset-type
prompt recipes (hero, texture, illustration, og:image, photography).
