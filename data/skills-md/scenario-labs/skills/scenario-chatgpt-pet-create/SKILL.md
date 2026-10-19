---
name: scenario-chatgpt-pet-create
description: "Use when creating a ChatGPT pet or Codex pet with Scenario: hatching an animated companion from a text idea, a character, mascot or brand cue, or reference photos and art; making the 1536x2288 v2 pet sprite sheet with nine animation states and sixteen look directions, the 1536x1872 v1 sheet ChatGPT web uploads, a pixel-perfect pixel-art pet, an animated GIF of the pet, or a Codex pet.json package."
license: MIT
---

# Scenario ChatGPT Pet: Create

## Overview

A ChatGPT pet is one transparent sprite sheet: 192x208 cells, 8 columns, nine animation rows (v1,
1536x1872) plus two rows of sixteen look directions (v2, 1536x2288). Rows, frame counts, what each
state must show, the look directions, the verdict file and the package layout:
[references/sheet-contract.md](references/sheet-contract.md). Read it before the first generation.

This skill delivers, next to the run: a v2 sheet (unless the user wants v1 only), a v1 copy for
ChatGPT web upload, `pet.gif` on a soft background and `pet-transparent.gif`, and a Codex `pet.json`
package, installed only when the user says yes. Every image is generated through the Scenario MCP
server; the frame cutting, sheet assembly, validation, GIFs and packaging run locally in the shipped
scripts, because the deliverable is a file for ChatGPT or Codex and no MCP tool assembles a pet
sheet. An image model never draws the whole sheet: it draws one row at a time, and the scripts place
every frame.

Connection, scope and the core loop: the `scenario` skill. Changing a pet that already has a sheet:
`scenario-chatgpt-pet-update`. If a sibling skill named here is missing from your available skills,
ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended,
proceed from tool schemas and flag the gap.

Scripts, run by the agent with Python 3, Pillow and NumPy (`pip install pillow numpy`, in a virtual
environment outside the run folder when the system Python refuses), by their path in this skill's
`scripts/` folder from the user's working folder (the commands below shorten that path); each prints
JSON, or `error: ...` with exit code 1, and `--help` lists every option:

- [pet_prepare.py](scripts/pet_prepare.py): run folder, background key, one prompt and request size
  per job (`init`), extra prompt sentences (`note`), pixel grid and palette (`pixel`).
- [pet_frames.py](scripts/pet_frames.py): cuts a generated strip into frames and reports problems
  (`extract`); reads an existing sheet (`split`, used by the update skill).
- [pet_build.py](scripts/pet_build.py): assembles the sheet with one pet height, ground line and
  planted anchor on every row.
- [pet_check.py](scripts/pet_check.py): validates the exact file to deliver.
- [pet_preview.py](scripts/pet_preview.py): contact sheet, labeled look sheet, GIFs.
- [pet_package.py](scripts/pet_package.py): package and optional Codex install.
- [pet_common.py](scripts/pet_common.py): shared layout facts, imported by the others.

## Quick reference

| Step                 | Do                                                                                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Brief                | Text, reference images, or both; one round of at most four questions                                                                                               |
| Set up               | `pet_prepare.py init`; `upload_asset` each file a job lists in `references`                                                                                        |
| Model, in this order | `model_openai-gpt-image-2-5-sunburst`, then `model_google-gemini-nano-banana-2-1`; `recommend` only when both are blocked                                          |
| Each generation      | `model_schema_get` once per model, `dry_run`, `model_run` with the job's `prompt` and `sizes`, `jobs_wait`, `asset_download` `format: "png"` to the job's `output` |
| Pixel-perfect        | After the base is approved and before any row: Pixel Snapper (`model_pixel-snapper`) on the base once, then `pet_prepare.py pixel`                                 |
| Each strip           | `pet_frames.py extract RUN --job <id>`; read the JSON; look at `frames/<id>/preview.png`                                                                           |
| Rows 0-8 done        | `pet_build.py RUN --version 1 --out RUN/qa/checkpoint`, then `pet_preview.py contact` and `gif`                                                                    |
| Finish               | `pet_build.py RUN`, `pet_preview.py looks`, verdicts, `pet_check.py`, `pet_preview.py gif`, `pet_package.py make`                                                  |

The model ids are named on purpose: both keep one character across a row of eight poses from a
reference image, which is what this job needs, and a team that cannot run either falls back to
`recommend` with the need and the families (GPT Image, Nano Banana). Pixel Snapper is Scenario's
tool for snapping generated pixel art to a clean grid and palette. Read every schema rather than
trusting the sizes below: at authoring time Sunburst took `referenceImages` (an array, up to 10),
`width` and `height` (16 to 3840, steps of 16), `background` (`opaque` here) and `quality` (left at
its default in every run behind these notes), and widened extreme shapes on its own (asked for
3584x512, it returned 3584x1200), which is why `init` asks for a height of at least a third of the
width; Nano Banana took up to 14 `referenceImages` and an `aspectRatio` preset (`4:1`, `8:1`).
Budget from the `dry_run` quote, which is what each job is charged: the `cuCost` that `jobs_wait`
reports can leave out add-ons such as a project's Quality Gate, so tracking it understates spend. At
authoring time the quotes were 13.75 CU for the base, 13.75 to 17.75 CU per strip (wider strips cost
more) and 6.75 CU for a Snapper call, so a pixel-perfect v2 pet (12 generations with `running-left`
mirrored, plus the Snapper) came to about 198 CU before any repair, about 216 CU when `running-left`
has to be generated: agree a budget with room for two or three repaired rows. Unattended, never
launch a job that would take the quotes already spent plus those still needed past the budget: if
only the look rows are left, deliver v1 without them; otherwise stop and report.

## Worked example: Biscuit, a corgi in a yellow raincoat, from a photo

1. **Brief.** The user sends a photo and a sentence. Ask once, only what changes the art: the name
   and one-line description (default: infer), the style (`auto`, `pixel`, `plush`, `clay`,
   `sticker`, `flat-vector`, `3d-toy`, `painterly`, `brand-inspired`), pixel-perfect or not, and v2
   with look directions (default) or v1 only. A brand name with no visual cues: ask for colors,
   shapes and attitude; never copy a logo or readable text. Unattended, infer and record the
   answers, make every approval below yourself against the brief (recording why), and never install.
   Resolve the team and project, then create one collection for the pet (`collection_create`, then
   `collection_add_assets` for every kept output, per the `scenario` skill).
2. **Set up.**
   `python3 scripts/pet_prepare.py init --name Biscuit --notes "corgi in a yellow raincoat, red collar" --reference photo.jpg --out pets/biscuit`
   (add `--pixel` for pixel-perfect: it sets the pixel style in every prompt; `--version 1` skips
   the look rows). It picks a background key that contrasts with the references (or with the notes:
   a pink pet gets green, never magenta) and writes `jobs.json`: per job an `id`, `frames`,
   `prompt`, `retry_prompt`, `references` (run-relative files), `sizes` per model, `depends_on` and
   `output`. Just before a job runs, `upload_asset` each local file it lists under `references/`
   (once per file, noting the id); a `generated/` file is already an asset, so pass the id its job
   returned instead of uploading the download.
3. **Base.** Run the `base` job with `referenceImages` set to the uploaded photo ids (none for a
   text-only pet), its `prompt` verbatim, and its Sunburst `width`/`height`, `background: "opaque"`.
   Download to `generated/base.png`, run `pet_frames.py extract RUN --job base`, which writes the
   clean identity reference `references/base.png`, and show the base with `asset_display`. Nothing
   else starts before the user approves it; a warning that the pet is close to the key color means
   `init --force --chroma-key` with another key and a new base.
4. **Pixel-perfect variant.** Run `model_pixel-snapper` on the approved base asset as generated,
   background and all (`image`, `colors` 24 unless the user wants fewer, any fixed `seed`), download
   it, then `pet_prepare.py pixel RUN --snapped snapped.png --colors <same>`. It picks a grid of 8,
   4, 2 or 1 screen pixels per art pixel, keeps the palette, and rewrites `references/base.png` as
   the enlarged pixel version (upload that new file), so every row is drawn from clean pixels and
   the build snaps every frame to the same grid and palette. Snap only the base: snapping each frame
   puts frames on different grids and costs a call per frame.
5. **Animation rows.** After the base, every standard row is independent except `running-left`,
   which waits for `running-right`. Launch `idle` and `running-right` first as identity and gait
   checks, then the rest in waves under the team's concurrency limit (`wait: false`, one `jobs_wait`
   over the batch; a 429 naming `parallel-custom-jobs` gives the limit, per the `scenario` skill).
   Each row: `referenceImages` = the uploaded `references/base.png` plus the user's photos, the
   job's `prompt` and `sizes`. After each download, `extract`, read its JSON and look at the
   preview: an error (wrong count, a pose touching the image edge) or a wrong pose means
   regenerating that row now, with `retry_prompt` or a sentence added by
   `pet_prepare.py note RUN --jobs <id> --text "..."`. When the pet looks the same mirrored (nothing
   handed, lettered or leaning to one side, so not a corgi with a one-sided patch or a robot with a
   tilted leaf), skip generating `running-left` and pass `--mirror-left` to every `pet_build.py`
   call instead.
6. **Checkpoint.** `pet_build.py RUN --version 1 --out RUN/qa/checkpoint`, then
   `pet_preview.py contact RUN/qa/checkpoint.png --out RUN/qa/contact.png` and
   `pet_preview.py gif RUN/qa/checkpoint.png --out-dir RUN/qa/checkpoint-previews`;
   `pet_check.py RUN/qa/checkpoint.png --run RUN --json-out RUN/qa/checkpoint-check.json` catches
   height and jump errors before the look rows are paid for. Show the GIF (open the local file, or
   upload it and share the `app_url` from `asset_display`); feedback goes into the affected rows,
   never into the sheet.
7. **Look rows (v2).** Decide how this pet looks around (what stays planted, what leads, how the
   eyes and ears move), add it with `note --jobs look-cardinals,look-9,look-10`, then run
   `look-cardinals` (four poses: up, right, down, left). Extract it and approve all four by eye
   before anything else: a cardinal that does not read at pet size is regenerated now. Then
   `look-9`, extract, `pet_build.py RUN --out RUN/qa/checkpoint` (it warns that `look-10` is still
   empty) and `pet_preview.py looks RUN/qa/checkpoint.png --out RUN/qa/looks.png` to look at it;
   then `look-10`, whose references include `generated/look-9.png` so the sweep continues.
8. **Finish.** `pet_build.py RUN` writes `final/spritesheet.png` and `final/spritesheet.webp` with
   one edge cleanup pass. `pet_preview.py looks RUN/final/spritesheet.webp --out RUN/qa/looks.png`,
   look at it, and write `qa/direction-semantics.json` (format in the contract).
   `pet_check.py RUN/final/spritesheet.webp --run RUN --require-v2` (no `--require-v2` for a v1-only
   pet) must print `ok: true`; fix what it names and rebuild.
   `pet_preview.py gif RUN/final/spritesheet.webp --out-dir RUN/previews`, then `upload_asset` the
   sheet and both GIFs (`kind: "image"` takes WebP and GIF, and a GIF keeps its animation), file
   them with `collection_add_assets`, then show the local `pet.gif` (an inline `asset_display` can
   show a single frame; the `app_url` it returns plays the animation).
9. **Package.** `pet_package.py make RUN` writes `package/biscuit/` (`pet.json`,
   `spritesheet.webp`), `package/spritesheet-v1.png` and the GIFs. Tell the user: ChatGPT web takes
   the v1 file under Settings > Personalization > Pet > Select pet > Upload pet, where the name is
   set and the look directions are absent (they exist only in the v2 file); Codex desktop takes the
   package folder. Ask before `pet_package.py install RUN`: it copies into
   `${CODEX_HOME:-~/.codex}/pets/biscuit/`, refuses to replace an existing pet without `--force`,
   and backs it up into the run first.

## Common mistakes

- Generating the whole sheet in one image, or cutting a strip into equal slots: models do not draw
  grids to the pixel, so `extract` finds each pose by its shapes and `pet_build.py` places it.
- Drawing frames with code when a generation fails: stop and report instead. The scripts only move,
  scale, mirror and clean generated pixels.
- Accepting a row with a warning unread: a pose cut by the image edge, an extra pose, or key-colored
  pixels inside the pet all come back as broken frames after the build.
- Fixing a sheet by regenerating everything: keep every row that passed, regenerate the smallest
  failing row, and when the same failure repeats twice, change the approach (simpler pose, a `note`
  sentence, fewer props) instead of rerunning the same prompt.
- Splicing one regenerated look direction into an approved row: a wrong direction regenerates its
  whole row, so the sixteen poses stay one family.
- Approving a cardinal that only reads when labeled: `000` is up, not neutral, and right means the
  viewer's right.
- Re-encoding or editing the sheet after `pet_check.py`: the package step compares SHA-256 and
  refuses other bytes; rebuild and check again.
- Sending only the v2 file to someone uploading on ChatGPT web: OpenAI documents 1536x1872 for that
  upload, which is `spritesheet-v1.png`.
- Installing over an existing Codex pet without asking: `install` needs `--force` for that, and the
  user's yes.
