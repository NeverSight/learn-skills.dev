---
name: astria-api
description: Use when making API calls to Astria for tunes, prompts, packs, image/video generation (Gemini/Seedream), inspecting or variating videos, handing an external agent session into Astria, or estimating generation and pack pricing. The reference for the `astria` CLI.
allowed-tools: Bash(astria:*)
---

# Astria CLI Reference

All Astria operations go through the bundled **`astria`** command-line tool. It
handles authentication, the API base URL, and workspace scoping for you — never
build raw `curl` calls and never read API tokens from environment variables.

Output is JSON on stdout, so you can parse ids and image URLs directly.

## Authentication

`astria` resolves credentials automatically:
1. Environment variables, if present (the Astria web app injects these).
2. `~/.astria/config.json`, written by `astria login`.

If a command fails with *"not authenticated"*, tell the user to run:

```bash
astria login          # prompts for an API key (astria.ai/users/edit/api)
```

Check the active account any time with `astria whoami`.

## Profiles

Profiles work like the AWS CLI — keep separate credentials, base URL and
workspace per profile (e.g. production vs a local dev server):

```bash
astria --profile localhost login --base-url http://localhost:3000
astria --profile localhost generate --text "..."
ASTRIA_PROFILE=localhost astria tunes list       # env-var form
```

`--profile <name>` (before the subcommand) or the `ASTRIA_PROFILE` env var
selects it. Each profile is its own file — `~/.astria/config.<name>.json`; the
default profile stays at `~/.astria/config.json`.

## Tune reference syntax

The core concept. A **tune** is a fine-tuned model trained on user images —
"tune" and "reference" mean the same thing. Reference a tune inside prompt text
with `<model_type:id:1> name`:

- `model_type` and `id` come from the tune JSON (`astria tunes get <id>`)
- `name` is the tune's class name and MUST appear right after the `<...>` token
- the trailing `:1` is a fixed part of the token syntax — it is NOT a weight or strength. Always write `:1`; never vary it and never suggest changing it.
- Combine freely: `<faceid:123:1> woman wearing <faceid:456:1> dress, white studio background`

`<faceid:123:1> woman` is correct; `John` (a bare name the model never trained on) is wrong.

## Workspace scoping

Add `-w/--workspace` to any command:
- `-w <id>` — target a specific workspace
- `-w all` — query across every workspace
- omit it — uses `WORKSPACE_ID`/config default, or personal scope

## Models

`--model` accepts a model name or a raw tune id. **Don't hardcode model
names — discover the current catalog at runtime:**

```bash
astria models              # image + video models — name, title, tune id, resolutions
astria models --refresh    # force-refresh (otherwise cached for a day)
```

The catalog is fetched from the Astria server, so it stays current as models
are added or retired and the tune ids never go stale. The output marks the
`default` model (used when `--model` is omitted) and lists each model's
supported `--resolution` values — a model with no resolutions listed doesn't
accept `--resolution`. It also lists the `video_models` catalog and the
`default_video_model` used by `astria video`.

`astria generate` / `astria video` `--help` print the current model,
resolution and video-model names inline — they read the same cached catalog.

---

## Tunes / references

```bash
astria tunes list                              # all tunes
astria tunes list --title "brown dress"        # by title / product name / SKU
astria tunes list --name shoes --name sandals  # by class name (repeatable)
astria tunes list --gallery --model-type faceid --limit 200   # public gallery
astria tunes get 123
astria tunes create --title "Brown dress" --name dress \
  --description "satin brown dress" \
  --image-url https://example.com/a.jpg --image-url https://example.com/b.jpg
astria tunes create --title "Studio shot" --name woman --image ./face1.jpg --image ./face2.jpg
astria tunes update 123 --name ring --title "Gold ring"
```

`tunes create` takes `--image-url` (remote) and/or `--image` (local file),
both repeatable. `--name` is the subject class (man, woman, dress, shoes,
sandals, pose, …). `--model-type` defaults to `faceid`.

## Prompts

```bash
astria prompts list                            # recent prompts
astria prompts list --pack-id 88               # a pack's template prompts
astria prompts list --tune-id 123              # prompts for one tune
astria prompts list --liked --is-video         # liked video prompts
astria prompts list --today --limit 100        # prompts created today
astria prompts list --text "white background" --limit 100 --offset 0
astria prompts get 555 --model nano-banana-pro       # one prompt (needs its tune/model)
astria prompts update 555 --model nano-banana-pro --pack-id 88   # assign a prompt to a pack
astria prompts update 555 --model nano-banana-pro --base-pack-id 88   # bind as a pack one-off (board frame)
```

- `prompts list` filters: `--pack-id`, `--base-pack-id`, `--tune-id`,
  `--user-id`, `--orig-prompt-id`, `--text`, and the flags `--liked`,
  `--today`, `--is-video`, `--is-api`.

## Generate images

```bash
astria generate --text "<faceid:123:1> woman, clean white studio background"
astria generate --model nano-banana-pro --text "..." --num-images 4 --aspect-ratio 3:4 --resolution 2K
astria generate --model seedream --text "product photo of headphones on marble" --num-images 2
astria generate --text "cinematic portrait" --film-grain
astria generate --text "recreate this in 4K" --input-image https://example.com/photo.jpg
astria generate --text "<faceid:123:1> woman, white bg" --pack-id 88 --wait   # author a pack template prompt
astria generate --text "..." --base-pack-id 88       # one-off bound to pack 88 — lands in its board frame
```

- `--input-image` accepts a URL or a local file path (used for image editing/upscaling).
- `--film-grain` sends film grain as a separate prompt attribute and leaves
  `--text` unchanged. `--film_grain` is an alias; `--no-film-grain` explicitly
  disables it.
- `--pack-id` authors the prompt as a pack **template** prompt; `--base-pack-id`
  records pack provenance only (a one-off). On the board, `--base-pack-id`
  generations appear as free rows inside that pack's frame.
- A `--pack-id` template prompt must **reference a fine-tuned tune** — embed a
  `<faceid:ID:1>` (or `<lora:ID:1>` …) token in `--text`. A plain foundation-model
  prompt with no reference is rejected (HTTP 422, "Prompt is not using a fine-tuned
  model"). `--base-pack-id` one-offs have no such requirement.
- `--wait` polls until the images are ready and prints the finished prompt JSON.
  Without it, the command returns immediately — images render asynchronously.
- `aspect_ratio` values: `1:1 16:9 9:16 21:9 9:21 3:2 2:3 5:4 4:5 4:3`.
- `--seed` sets the generation seed. Astria dedups prompts by `(text, seed)`
  within a tune, so the same prompt text reused on different input images
  collapses onto one prompt — pass a distinct `--seed` per call to keep them
  separate without altering the prompt text.

## Generate video

Video runs through the same prompt: the image stage renders the first frame
from `--text`, then the video model animates it from `--video-prompt`.

```bash
# Existing reference: use the same token + tune-name syntax as image generation.
# Put Seedance 2 references in --video-prompt so their images condition the video.
astria video --video-model seedance2_fast_720p \
  --video-prompt "<faceid:1234:1> woman walks down a runway as the camera tracks her" \
  --duration 5 --aspect-ratio 16:9 --wait

# New references: create them from local files or URLs and use them immediately.
astria video --video-model seedance2_fast_720p \
  --video-prompt "woman wearing a dress walks down a runway" \
  --reference woman=./model.jpg --reference dress=https://example.com/dress.jpg \
  --duration 5 --aspect-ratio 16:9 --wait

# Ordered raw references: attach the images directly without creating tunes.
astria video --video-model seedance2_fast_720p \
  --video-prompt "transition through these looks in order" \
  --image-reference ./look-1.jpg --image-reference ./look-2.jpg \
  --duration 15 --aspect-ratio 16:9 --wait

astria video --text "zwx man <faceid:123:1> in a dance arena" \
  --video-model kling30_motion_control_pro --video-prompt "match the dance moves" \
  --duration 10 --input-video ./reference.mp4
```

- Seedance 2 references use `<faceid:TUNE_ID:1> TUNE_NAME`, exactly like image
  prompts. The tune's class name must immediately follow the token. A bare
  `<faceid:1234:1>` token is incomplete.
- Put existing reference mentions in `--video-prompt`; Seedance 2 resolves the
  referenced tunes' images and sends them as video reference images.
- `--reference NAME=PATH_OR_URL` creates an instant `faceid` reference and
  prepends `<faceid:NEW_ID:1> NAME` to both `--text` (when present) and
  `--video-prompt`. Repeat it for multiple references. `--images` is an alias.
- `--image-reference PATH_OR_URL` attaches a raw image directly to the video
  prompt without creating a tune. Repeat it in storyboard order. Use either
  all local files or all URLs in one request so that ordering remains exact.
- `--first-frame` / `--last-frame` / `--input-video` accept a URL or local file.
- Motion-control models (`*_motion_control*`, `wan_animate_*`, `dreamactor_m2`,
  `happyhorse_motion_control`) require `--input-video`.

### `video_model` values and cost

Costs are per 5-second base (per 10s for motion-control / fixed-duration
models) and scale linearly with duration. `_audio` models include a soundtrack.

| video_model                     | cost (¢)    | duration options |
|----------------------------------|------------:|------------------|
| seedance_480p                    |          10 | 2–12             |
| seedance_v15_720p                |          14 | 4–12             |
| seedance_v15_audio_720p          |          29 | 4–12             |
| cinematic_video                  |          84 | 5, 10, 15        |
| wan25_720p                       |          53 | 5, 10            |
| wan26_720p / wan26_1080p         |       53/79 | 5, 10, 15        |
| wan27_720p / wan27_1080p         |       55/83 | 5, 10, 15        |
| wan_animate_720p                 |          44 | 10               |
| ltx23_720p / ltx23_1080p         |       17/22 | 5, 10, 15, 20    |
| happyhorse_720p / _1080p         |      77/132 | 3–10             |
| happyhorse_motion_control        |         154 | 10               |
| dreamactor_m2                    |          29 | 10               |
| seedance2_fast_480p / _720p      |      60/140 | 4–15             |
| seedance2_480p / _720p / _1080p  | 120/280/450 | 4–15             |
| veo31_fast_720p / _1080p         |          85 | 4, 6, 8          |
| veo31_fast_4k                    |         264 | 8                |
| veo31_lite_720p / _1080p         |       44/71 | 4, 6, 8          |
| kling30_standard / _pro          |      92/123 | 3–15             |
| kling30_4k                       |         263 | 3–15             |
| kling30_motion_control / _pro    |     277/370 | 10               |

Video output is delivered in the prompt's `images[]` with `content_type=video/mp4`.

## Inspect video

Turn a local video or public HTTPS video URL into timestamped text-to-video
prompt text. Local files are direct-uploaded to Astria automatically; do not
upload them separately or build raw API requests.

```bash
astria inspect-video ./clip.mp4
astria inspect-video https://example.com/clip.mp4
astria inspect-video ./clip.mp4 --tune-id 123 --tune-id 456
```

The output uses one `SS-SS - description` line per cut for videos up to 30
seconds. `--tune-id` is repeatable: use it when the resulting generation will
carry those references, so inspection removes their appearance details and
inserts the exact Astria reference tokens. There is intentionally no custom
prompt option; use the returned `description` as the video prompt.

## Variate video

Use `astria variate` when the user wants to preserve a source video's timing,
performance, camera, transitions, and audio while changing its content. The
command runs the Variate mini-app workflow end to end: source inspection,
replacement-reference creation, structured prompt writing, and fixed-model
Seedance 2.5 generation.

```bash
# Edit from a written brief
astria variate ./source.mp4 \
  --brief 'Change the text on the final card to say "Astria"' --wait

# Mix existing references with new local or remote images
astria variate ./source.mp4 \
  --tune-id 123 \
  --reference ./dress.jpg \
  --reference woman=https://example.com/model.jpg \
  --brief 'Replace the presenter and wardrobe' --wait

# Reuse an existing source description and avoid another inspection charge
astria variate https://example.com/source.mp4 \
  --description-file ./source-description.txt \
  --brief 'Use a warmer end-card treatment'
```

- `SOURCE` is a local MP4/MOV or public HTTPS URL.
- Repeat `--tune-id ID` for existing replacement references.
- Repeat `--reference [NAME=]PATH_OR_URL` to create replacement references.
  Without `NAME=`, the CLI detects the image class. With it, detection is
  skipped. References preserve command order within the existing/new groups.
- At least one reference or a non-empty `--brief` is required.
- `--description` / `--description-file` bypass source inspection.
- The command intentionally fixes `video_model=seedance25_720p`, enables
  generated audio, and omits duration/aspect ratio so the source drives them.
- Local source and reference files are direct-uploaded in one parallel batch.
- The JSON result contains `description`, `references`, `video_prompt`, and
  `prompt`; add `--wait` to receive the settled generation in `prompt`.

## Download

`astria download` saves a prompt's rendered assets (images, or `video/mp4`) to a
local directory. It works from a **prompt id alone** — no tune id needed — and
fetches each prompt fresh from the API, so newly rendered assets are included.

```bash
astria download 555 556 557                       # ids as arguments
astria download 555 --out ./shoot                  # custom target directory
astria download --prompts-file ids.txt             # one id per line (or whitespace)
astria prompts list --pack-id 88 | \
  python3 -c 'import sys,json; [print(p["id"]) for p in json.load(sys.stdin)]' | \
  astria download                                  # ids piped on stdin
```

- Prompt ids come from positional args, `--prompts-file`, and/or stdin; they are
  deduped with original order preserved.
- `--out` defaults to `./astria-downloads` and is created if missing.
- Each asset is saved as `prompt-<id>-<NN><ext>` — `<NN>` is a zero-padded
  index, `<ext>` is derived from the URL (`.jpg`/`.png`/`.webp`/`.mp4`/…).
- Downloads run in parallel (~6 at a time).
- A prompt that 404s, errors, or has no images yet is reported in the JSON
  output (`error` field) and does not abort the run.
- The JSON summary lists per prompt `{id, images, saved[], error?}` plus
  `totals {prompts, downloaded, failed}`.

## Packs

Packs are surfaced in the Astria GUI as **Templates** — "pack" and "template" are interchangeable terms for the same object.

```bash
astria packs list
astria packs get spring-lookbook
astria packs create --title "Spring Lookbook"
astria prompts update 555 --model nano-banana-pro --pack-id 88   # add a prompt to the pack
```

## Pricing

`cost_mc` is an integer number of **millicents** (one thousandth of a US cent):

- 1,000 `cost_mc` = $0.01
- 100,000 `cost_mc` = $1.00
- Convert to dollars with `cost_mc / 100_000`.

A prompt's `cost_mc` already includes its `num_images`; never multiply by
`num_images` again. Sum `cost_mc` across prompt records to price a prompt batch.
For example, prompts priced at 12,500 and 25,000 `cost_mc` total 37,500
millicents, or **$0.375**.

Use `astria packs get <slug|id>` before running a pack:

- `template_prompts[].cost_mc` is each stored template prompt's baseline. Sum
  all entries for the full stored baseline, or selected entries for a
  `--prompt-ids` subset.
- `costs.<class>.cost_mc` estimates a fresh reference tune of that class plus
  that class's prompt group. For multi-class packs it is not necessarily the
  cost of the entire pack.

These are estimates, not personalized quotes. Generated prompts recalculate
cost after prompt overrides; creator discounts, the payer's ecommerce pricing,
workspace rules, and Cartesian tune variants can change the result.

After `astria packs run`, use `order.total_cost_mc` as the authoritative amount
charged when an order is returned. If no order is returned, the generated
prompts' `cost_mc` values describe their individual base costs.

### Run a pack

`astria packs run <slug|id>` fires a pack's template prompts —
`POST /p/:slug/tunes`. This is the canonical "run a template": the pack
generates its whole prompt set, either against **tunes you already have** or
against a **fresh tune trained from photos**. The positional accepts either the
pack **slug** or its numeric **id** — `astria packs run zara-pants …` and
`astria packs run 3893 …` are equivalent.

```bash
# multi packs — run against existing tunes (tune_ids), with overrides
astria packs run spring-lookbook --tune-id 123 --tune-id 456 \
  --brief "golden hour, Lisbon" --aspect-ratio 3:4 --inpaint-faces

# only a subset of the pack's template prompts
astria packs run spring-lookbook --tune-id 123 --prompt-ids 501,502

# regular packs — train a fresh tune from photos, then generate
astria packs run my-pack --title Jane --name woman \
  --image ./a.jpg --image ./b.jpg          # or --image-url https://…
```

- **Who the pack runs on** — pass either `--tune-id ID` (repeatable, or a
  comma-separated list) to reuse existing tunes, **or** a training set
  (`--title` + `--name` + `--image`/`--image-url`) to train a new tune first.
  **Multi packs require at least one `--tune-id`** (the server routes tune_ids
  to its multi handler; omitting them on a multi pack is a 422).
- `--prompt-ids 501,502` runs only that subset of the pack's template prompts;
  omit it to run them all.
- `--brief` is an art-direction brief applied to the generated prompts.
- **Overrides** ride along as `prompt_attributes`: `--num-images`,
  `--aspect-ratio`, `--resolution`, `--inpaint-faces/--no-inpaint-faces`, and
  `--attr KEY=VALUE` (repeatable) for any other prompt attribute, e.g.
  `--attr super_resolution=true`.
- The positional is the pack **slug or numeric id** — both resolve to the same
  `/p/:slug/tunes` endpoint. On a multi pack the JSON response includes the new
  `order` and its `prompt_ids` — feed those to `astria prompts wait` and
  `astria download` to fetch the images.

#### Worked example — a multi pack, step by step

`zara-boot-test` (id `4001`) is a **multi pack** that composes two references —
a `dress` and a `shoes` (Footwear) — into one shoot. Create a reference per
garment, then run the pack against both by id. Scope every step to a workspace
with `-w` (find yours with `astria workspaces list`).

```bash
# 1. Create a reference for the dress (Gemini branch — instant, no training wait)
astria tunes create -w 679 --name dress --title "Zara dress" --image ./dress.jpg
# → { "id": 5234832, "branch": "gemini-2", "trained_at": "..." }

# 2. Create a SEPARATE reference for the boots.
#    Use a class the pack's slot recognizes: 'boots' (like 'shoes'/'sandals')
#    resolves to the Footwear cube, so it fills the pack's shoes slot.
astria tunes create -w 679 --name boots --title "Zara boots" --image ./boot.jpg
# → { "id": 5234834, "branch": "gemini-2", "trained_at": "..." }

# 3. Run the pack against both references — one --tune-id each.
#    'zara-boot-test' or its id '4001' are interchangeable here.
astria packs run zara-boot-test -w 679 \
  --tune-id 5234832 --tune-id 5234834 --num-images 1 --aspect-ratio 3:4
# → { "status": 201, "order": { "id": 37345, "tune_ids": [5234834, 5234832] },
#     "prompt_ids": [45042524, 45042523] }

# 4. Fetch the results (the order hands back the prompt ids)
astria prompts wait -w 679 45042524 45042523              # block until rendered (or user_error)
astria download 45042524 45042523 --out ./zara-boot-shoot
```

The pack swaps each reference into the matching template slot by lookbook cube,
so the generated prompts come back with both tokens recorded, e.g.
`a model wearing <faceid:5234832:1> dress and <faceid:5234834:1> boots, …`
(and the shoes-only template gets just the boots token). The overrides land as
prompt attributes (`aspect_ratio: 3:4`, `num_images: 1`).

Gemini-branch references (step 1–2) are ready instantly; a pack built on trained
tunes queues its prompts and renders them once the tunes finish training. Pass
one `--tune-id` per reference slot the pack defines — a multi pack needs at
least one, and rejects the run (422) if you send none.

## Board (infinite canvas)

The board (`/boards/:id` in the GUI) organizes work as **frames** (a pack-bound working context), **order rows** (one Order = a line of prompts sharing one reference set) and **reference cards** (tunes with lookbook roles: Pose, Face, Accessories, Jacket, Top, Bags & Belts, Footwear, Bottom, Background). There is no board API and no `board` verb — you act on the regular domain objects with the verbs above, and the canvas updates live (new rows land via the `order.created` broadcast, cells re-render as prompts finish).

```bash
astria packs run 88 --tune-id 123 --tune-id 456 \
    --prompt-ids 501,502 --brief "golden hour, Lisbon"  # new row: clone the pack's templates with swapped refs
astria prompts wait 7001 7002 && astria download 7001 7002   # wait for the row's cells, fetch images
astria generate --text "..." --base-pack-id 88       # one-off into pack 88's frame (free row, not a template)
# variant with edited text (stacks as a version on its cell; order_id from `astria prompts get`):
astria api POST /prompts/7001/duplicate --query view=board --data '{"prompt":{"text":"...","order_id":901}}'
# promote a prompt into the pack template / demote a template back out (confirm with the user first):
astria api PATCH /prompts/7001 --query view=board --data '{"prompt":{"pack_id":88,"base_pack_id":null,"orig_prompt_id":null}}'
astria api PATCH /prompts/7001 --query view=board --data '{"prompt":{"pack_id":null,"base_pack_id":88}}'
```

For an ordered raw-image video, pass the selected images directly with repeated
`astria video --image-reference PATH_OR_URL` options. Do not create temporary
tunes for those images.

## Workspaces & landing pages

```bash
astria workspaces list
astria workspaces create --title "Acme Store"   # new workspace → returns its id/slug
astria landing get -w 42                        # workspace JSON incl. landing_page_html
astria landing set -w 42 --html-file ./edited.html
```

## Hand work into Astria’s embedded agent

When the user asks to continue the current ChatGPT, Codex, Claude, or Cursor
session in Astria, write a concise UTF-8 `HANDOFF.md` containing the objective,
completed work, important decisions, artifact paths, unresolved issues, and the
recommended next action. Do not include credentials or hidden reasoning.

Attach only files needed to continue. Include a custom skill only when it was
actually used or is needed for the remaining work; never export credential
files or an entire agent configuration directory.

```bash
astria agent handoff -w 42 \
  --handoff ./HANDOFF.md \
  --attach ./deliverables \
  --skill ~/.claude/skills/relevant-skill \
  --source claude-code \
  --open
```

`--attach` and `--skill` are repeatable. A skill path must be a directory with
`SKILL.md`. The command uploads the versioned bundle, creates a dedicated chat
session, prints its HTTPS deep link, and opens it with `--open`. Imported skills
are reviewable session-scoped references; Astria does not silently install them
into the shared workspace skill directory.

## Raw API escape hatch

For anything without a dedicated verb:

```bash
astria api GET /prompts --query limit=5 --query offset=0
astria api POST /tunes --form 'tune[title]=Hat' --form 'tune[images][]=@./hat.jpg'
```

## Pagination

List commands accept `--limit N` and `--offset Y`. Default sort is id
descending, so `--offset` walks backwards through history.

## Errors

A non-zero exit prints `astria: <METHOD> <PATH> → HTTP <code>: <message>` on
stderr. Surface the message to the user and suggest a fix. HTTP 422 means a
validation error (missing/invalid fields).
