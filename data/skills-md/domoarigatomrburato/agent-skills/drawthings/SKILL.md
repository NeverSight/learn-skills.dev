---
name: drawthings
description: Render prompts through the Draw Things app's API server (gRPC) from the terminal instead of pasting them into the app. Picks a model recipe (Krea 2 Turbo, Ideogram 4 and Qwen Image 2512 through Draw Things+ cloud compute, or any model the app has locally), runs a seed set one job at a time, survives the flaky cloud (retries, stall detection, resume) while staying easy to stop, saves PNGs with the exact prompt, a run log and a contact sheet, and looks at the results. Use this skill whenever the user wants to generate, render, batch, retry, compare seeds or log image experiments with Draw Things, mentions its API server, gRPC, Bridge Mode or cloud compute, or asks to run a Krea or Ideogram prompt "in Draw Things", even if they only say "render it" or "try a few seeds".
---

# Draw Things API server

The Draw Things app can expose its generation pipeline as a gRPC service, and with **Bridge
Mode** on (Draw Things+ subscribers) every job sent to that service runs on Draw Things'
cloud compute, including cloud-only models that never touch the Mac. This skill drives that
service through the maintained `drawthings-py` SDK (PyPI, GPL-3.0, used as a dependency), adding
the one thing the SDK lacks: the model spec (`override.models`) that cloud-only models need
because the app does not list them. Files, relative to this skill's folder:

- `scripts/dt_render.py` — the renderer: recipe or custom spec, prompt file, seed set, retries and resume, PNGs, `run.json`, `runs.jsonl` line per image, contact sheet.
- `scripts/setup.sh` — one-time virtualenv with the SDK (`~/.cache/drawthings-skill/venv`).
- `scripts/compute_units.py` — the app's compute-unit formula, ported from `ComputeUnits.swift`; the renderer runs it before every job.
- `scripts/png_config.py` — prints the settings and prompt stored in any Draw Things PNG (the app's exports or this renderer's) and the command that reproduces it.
- `recipes.json` — verified model specs and their default settings.
- `references/server.md` — protocol facts, timings, how to derive a spec for a new cloud model, SDK notes.

## 1. Before the first render

The app must be running with, in Settings, Advanced, API Server: protocol gRPC, port 7859,
Transport Layer Security on, Response Compression on, Model Browsing on, and Bridge Mode on
for the cloud recipes. Cloud Compute must also be selected in the app's project. Then, once
per machine:

```bash
bash scripts/setup.sh          # creates the venv, needs Python 3.11+ or uv
python3 scripts/dt_render.py --check
```

`--check` connects over TLS, lists the models the app has locally, and says which recipes
need the cloud. If it cannot connect, the API server is off or another port is set; if a
recipe's file is "not local" and Bridge Mode is off, the job will ask for a download instead
of rendering. The script re-executes itself under the venv, so any `python3` can launch it;
`DRAWTHINGS_PYTHON` overrides the interpreter, `DRAWTHINGS_HOST` and `DRAWTHINGS_PORT` the
server.

## 2. Run a round

Write the prompt with the model's prompting skill first (`krea-prompt` for Krea 2 Turbo,
`ideogram-prompt` for Ideogram 4, which produces a JSON caption; plain descriptive prose for Qwen
Image), lint or validate it, save it to a file, then:

```bash
python3 scripts/dt_render.py --recipe krea-2-turbo --prompt-file prompts/krea-2-turbo.txt \
  --count 4 --out renders/observer/r12 --log projects/observer/runs.jsonl --note "haze as a surface"
```

- `--count 4` draws four random seeds (printed and logged); `--seeds 12345,777` reuses known ones. `--seeds` always means literal seeds, so `--seeds 42` is the one seed 42. Seeds run one after another because the server takes one job at a time. A run refuses to start above `--max-images` (default 8); raise it on purpose for bigger rounds.
- `--size WxH` overrides the recipe's default (multiples of 64, at most 2048 on a side; `size.py` in the krea-prompt skill gives the size for a ratio). `--steps`, `--cfg`, `--shift`, `--sampler` override the recipe; leave them alone while iterating on a prompt.
- A `.json` prompt file is validated and minified before sending; a `.txt` file is sent as is. `--negative-file` adds a negative prompt where the model uses one (Turbo ignores it). A recipe can carry a default negative (`qwen-image-2512` carries the model card's); `--negative-file` or `--negative` replaces it and `--negative ""` sends none.
- `--out` gets `<name>-s<seed>.png` (with Draw Things metadata inside the PNG), a copy of the exact prompt, `run.json` with everything, and `<name>-sheet.jpg` when at least two images succeeded. `--name` sets the base name (default: the prompt file's stem).
- Every successful PNG also gets `<name>-s<seed>.config.json`: a reusable recipe containing the exact prompt and negative prompt plus pasteable Copy Configuration JSON with that image's seed.
- `--log` appends one JSON line per image: settings, seed, timing, prompt hash and file, status, your `--note`. Keep one `runs.jsonl` per project so a whole project's history is one file.
- Expect 15 to 60 s before the first sampling step and 90 to 230 s per 2K image on the cloud (Ideogram and Qwen Image near 40,000 units are the slow end). A round of four seeds is six to fifteen minutes. **Never run a render as a blocking foreground command**, not even a one-image test: start it in the background so the conversation stays open, and tell the user it is running and how to stop it. Before starting, the script prints the plan (images, the most requests it may send, rough minutes) and how to stop it.
- **Stopping a run**: Ctrl-C or `kill <pid>` end it at once; `touch <out>/STOP` ends it within seconds (`~/.cache/drawthings-skill/STOP` stops every run). Stop files older than the run are ignored, so a leftover never blocks the next one. Finished seeds are kept.
- **Resume**: run the same command again with the same `--out` and it renders only the seeds that are missing (`--count` runs reuse the seeds drawn the first time). `run.json` is rewritten after every seed, so an interrupted run loses nothing. Another prompt or other settings in an `--out` that already holds renders is refused; use a new folder or `--overwrite`.

Change one thing per round, say what in `--note`, and keep the note in the project's
`notes.md` when the round taught something.

### Load or save the app's Copy Configuration JSON

The app's **Copy Configuration** command copies the settings but not the prompt. Save it as
JSON and combine it with a prompt on the command line:

```bash
pbpaste | python3 scripts/dt_render.py --config - --prompt-file prompts/qwen.txt \
  --negative "" --out renders/qwen-repro
```

`--config FILE` accepts three shapes: the bare object copied by the app; an app preset with
`name`, `negative` and `configuration`; or the skill's self-contained recipe:

```json
{
  "name": "qwen-image-2512",
  "prompt": "the exact prompt",
  "negative": "",
  "configuration": {"model": "qwen_image_2512_q8p.ckpt", "sampler": 15}
}
```

The model file selects the matching recipe and therefore its full cloud spec. A model absent
from `recipes.json` still needs `--spec FILE` after its spec has been derived. Settings come
from the configuration; explicit command-line flags win, including prompt, negative, seed,
size, steps, CFG, shift, sampler and boolean `--no-*` overrides. `batchCount` and `batchSize`
must be 1 because the renderer saves one image per seed.

To turn an app or API PNG into a self-contained recipe, prompt included:

```bash
python3 scripts/png_config.py image.png --config-out image.config.json
python3 scripts/dt_render.py --config image.config.json --out renders/repro
```

The `configuration` object remains valid app Copy/Paste Configuration JSON; fields unknown to
the Python SDK are preserved when the recipe is loaded and written again.

## 2b. Compute units (the cloud's per-image budget)

The cloud measures each request in compute units and refuses anything above the tier limit
(10,000 for community, 40,000 for Draw Things+) rather than charging for it. The app shows the
number next to the rocket icon; `dt_render.py` computes the same number before sending, from
the app's own formula (`scripts/compute_units.py`, ported from `ComputeUnits.swift`), prints it,
and stops with exit code 3 when it is over the limit unless `--force` is given. The units grow
with the pixel count (attention is quadratic in the image tokens), the steps, and double when
CFG is on (guidance above 1). Reference points for the recipes:

| Recipe | Size | Steps | Units |
|---|---|---|---|
| krea-2-turbo | 2048x1344 | 8 | about 7,300 |
| ideogram-4 | 1920x1280 | 32 | about 39,500: the recipe default, just under |
| ideogram-4 | 2048x1344 | 20 | about 28,300 (28 steps: about 39,700) |
| ideogram-4 | 2048x1344 | 32 | about 45,300: over the limit |
| ideogram-4 | 2048x2048 | 20 | about 48,700: over the limit |
| qwen-image-2512 | 1536x1024 | 34 | about 21,600: the recipe default |
| qwen-image-2512 | 1536x1024 | 50 | about 31,800: the model card's step count |
| qwen-image-2512 | 1408x1792 | 34 | about 38,800 |
| qwen-image-2512 | 1920x1280 | 36 | about 39,700: the app showed 39,699, just under |

`--estimate-only` prints the number without connecting; `--tier community` applies the lower
limit; `DRAWTHINGS_TIER` sets the default. The formula is upstream's, with a calibration
constant they tuned on FLUX; treat a result within a few percent of the limit as over it. Checked against the app once: for 1920x1280 at 32 steps with guidance 7 the app showed about 39,000 and the formula gives 39,477.

## 3. Recipes

`--list-recipes` prints them. Verified through Bridge Mode on 2026-09-26:

| Recipe | Model file | Defaults | Prompt |
|---|---|---|---|
| `krea-2-turbo` | `krea_2_turbo_i8x.ckpt` (cloud) | 8 steps, CFG 1.0, shift 3.16, DDIM Trailing, 2048x1344 | plain text from `krea-prompt` |
| `ideogram-4` | `ideogram_4_q8p.ckpt` (cloud) | 32 steps, CFG 7, shift 2.99, DPM++ 2M Trailing, zero negative prompt on, 1920x1280: the app's own settings for "Ideogram 4 remote" | JSON caption from `ideogram-prompt`, up to 2,000 tokens |
| `qwen-image-2512` | `qwen_image_2512_q8p.ckpt` (cloud) | 34 steps, CFG 4, shift 2.22, DPM++ 2M Trailing, the model card's negative prompt, 1536x1024. Shift follows the card's schedule by size (1024x1024 2.00, 1408x1792 2.67, 1920x1280 2.64); the recipe notes list more | plain descriptive prose; 513 tokens rendered fine |

A model the app already has locally needs no recipe: `--spec` with a file holding the entry
from `--check`'s list (name, file, version, text encoder, autoencoder, default scale) works,
or add it to `recipes.json` with a `defaults` block and a `notes` line saying what was
verified. For a new cloud-only model, first check it is in the cloud's served list (`models.txt` in
the `drawthingsai/community-models` GitHub repository), then derive the spec as described in
`references/server.md` (the version string, the text encoder and the autoencoder come from
the app's open-source model zoo) and test it at a small size first. A spec for a cloud-only model (Krea, Ideogram) needs
`default_scale` 32 for sizes above 1024 px on a side; a model the zoo already has keeps the
zoo's value (Qwen Image's 16 renders 1920x1280).

## 4. Look, then iterate

After the run, read the contact sheet (or the single PNG) with the image-reading tool and
judge it against the brief before saying anything to the user: composition, the elements the
prompt placed, rendered text, the light, the style label. Then:

- Prefer the prompting skill's iteration section for what to change; the settings stay fixed.
- Pick keepers by seed and say which; the lab convention is a JPEG copy in `keepers/` and the PNG left in `renders/`.
- When two seeds disagree on a detail the prompt specified, the prompt is ambiguous there; when all seeds agree on a wrong detail, the wording is wrong.
- Re-render a known seed after a prompt change to see the change itself, then draw fresh seeds.

## 5. Errors and limits

- **The Draw Things+ cloud is generous but flaky.** It aborts jobs at random, mostly before the first sampling step (`INTERNAL: unknown error processing request` after 20 to 30 s), sometimes mid-sampling, and it stalls. The script treats every failure as transient: each attempt gets a fresh connection, a job that sends no progress for `--stall-timeout` (300 s) is cancelled, the retries back off from 20 s to 240 s (`--retries` 3, `--retry-wait`, `--retry-wait-max`), and seeds that still fail get a second pass at the end (`--passes` 2). A PNG only lands on disk after it has been checked (right size, not one flat colour).
- **When failures are systematic the script stops by itself**: after `--max-failures-in-a-row` (5) failed attempts, or when the API server stays unreachable for `--server-wait` (60 s; the user may have quit the app on purpose). Exit code 6 means the run stopped; fix the cause and rerun the same command to resume. Never conclude a spec, size or prompt is wrong from one failure, but the same failure on every attempt is not the cloud.
- **A cloud model that renders in the app but always fails through the API mid-sampling with `No images received from server` has an incomplete spec.** The spec sent through `override.models` replaces the app's built-in entry, so it must carry every field the model zoo entry has: for Qwen Image that is `objective` (`{"u": {"condition_scale": 1000}}`), `hires_fix_scale` and the `mmdit` block with its per-layer activation scaling. Copy these from the model's `metadata.json` in `drawthingsai/community-models` (the JSON form of the zoo entry, snake_case keys) rather than writing a bare spec.
- The same error at the first step on every attempt, for sizes above 1024 px, with a spec for a cloud-only model (Krea, Ideogram) means `default_scale` 16 in the spec; use 32.
- With Bridge Mode on, every job goes to the cloud: local community checkpoints fail through it. Turn Bridge Mode off to render local models, on for the cloud recipes.
- One job at a time. Do not run two `dt_render.py` at once against one server.
- A cloud model that is `not local` with Bridge Mode off returns a download request instead of an image; the script reports it as an error.
- **Ideogram 4 needs the `q8p` model file.** With `ideogram_4_i8x.ckpt` in the spec, guidance above 1 breaks down as the caption grows: at CFG 7 captions up to about 500 Qwen tokens render, 800 come out blown out, 1,000 and more are noise, while CFG 1 stays clean. With `ideogram_4_q8p.ckpt`, the file behind the app's "Ideogram 4 remote", a 1,309-token caption renders cleanly at CFG 7 with or without zero negative prompt, and the app's own image is reproduced pixel for pixel from its seed and settings. The recipe carries the q8p file; if a render ever shows that pattern again (short captions fine, long ones noise), check the model file before anything else.
- `--timeout` (1200 s per attempt) covers 50-step 2K jobs; raise it for video or larger batches.
- Local LoRAs (`--lora file.ckpt:0.8`) are passed through the configuration and work for local models; the cloud has no access to local LoRA files, so do not expect them on cloud recipes.

## 6. Reproducing an image

Every `runs.jsonl` line has the recipe, model file, size, steps, CFG, shift, sampler, seed,
and the prompt file with its SHA-256; `run.json` in the run folder holds the prompt text
itself. To reproduce: same recipe, `--prompt-file` at the commit whose hash matches,
`--seeds <seed>`. The cloud is deterministic for a given seed and settings in practice, but
the model files behind a recipe can be updated upstream, so keep the keeper.

The app stores the same information in every PNG it exports: an XMP block with the prompt,
the negative prompt, the model file, size, steps, guidance, shift, sampler, seed and every
configuration flag. `python3 scripts/png_config.py image.png` prints it, `--prompt-out
caption.json` saves the prompt, `--config-out image.config.json` saves a complete reusable
recipe, and the last line is the `dt_render.py` command that reproduces the image. That is how
the app's own settings for a cloud model are read, since
macOS keeps other processes out of the app's container and its database; a render made this
way from the app's seed matched the app's image pixel for pixel.
