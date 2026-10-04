---
name: pollo-generate
version: 0.1.0
description: |
  Drive the pollo-cli to generate images and videos through the Pollo
  platform open API — discover a model, read its input fields, submit a
  generation with local or hosted image inputs, and poll it to a finished
  URL. Use this
  whenever the user asks to generate/create/make an image or video, animate a
  photo, do image-to-video / text-to-video / reference-to-video, check Pollo
  credit balance or estimate the credit cost of a generation, or asks what
  Pollo models are available — trigger even if they don't name "pollo-cli" or
  "pollo" explicitly, e.g. "turn this photo into a video" or "how many
  credits do I have left". NOT for building the platform API itself
  (server-side model exposure — use the expose-platform-model-api skill) or
  wiring a model into the web frontend (use the add-model skill).
allowed-tools: Bash, Read
# ClawHub runtime dependency: this skill drives the pollo CLI, so declare that
# the `pollo` binary must be on PATH.
metadata:
  openclaw:
    requires:
      bins: [pollo]
---

# pollo-generate

`pollo-cli` already owns auth, token refresh, and request shaping. Your job
starts one step later: pick the right model, learn its input fields, build a
valid `input`, submit, and hand back the result. Everything below follows
that order — model, then input, then submit, then result — because that's
also the order the server validates in, so skipping a step just turns into a
server error one step later.

## Setup (once per session)

1. If `pollo` isn't on `$PATH`, install the released binary — don't build from
   source:
   ```bash
   npm i -g @pollo-ai/cli
   ```
   Without Node (macOS / Linux only), fall back to the standalone installer:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/polloaiofficial/cli/main/install.sh | sh
   ```
2. Run `pollo account status`. An `availableCredits` number means you're
   already logged in to prod (`pollo.ai`, profile `default`). A missing/expired
   token error means:
   ```bash
   pollo auth login   # opens the browser, logs into pollo.ai -> profile "default"
   ```
   The CLI owns its own credential storage and refreshes the short-lived token
   before each request, so you won't need to log in again mid-session. Never
   read, print, or copy the stored credentials — every command below
   authenticates on its own.
3. Stay on the `default` profile unless the user names another one. Profiles let
   one machine hold several logins; `pollo profile list` shows them (`*` marks
   current), `pollo profile use <name>` switches, and
   `pollo --profile <name> <command>` overrides for a single command.

## Step 1 — Find the model, then read what it actually accepts

Never guess a `brand`/`alias` or a field name — they change as models ship, so
a guess just surfaces as a server validation error one step later instead of
saving you a lookup now:

```bash
pollo model list                        # every standard model, capabilities aggregated
pollo model list --type text2video      # only models with that capability
pollo model get <brand>/<alias> --fields   # this model's input shape
```

Each model is listed once, with a `capabilities[]` array. A capability is an
**input mode** — `text2video` | `image2video` | `ref2video` | `text2image` |
`image2image` — and each one carries its own `path` (the output endpoint,
`/video` or `/image`) plus its own `fields`/`constraints`. So a model that
takes both text and images has several capabilities sharing one `path`, and a
dual-output model like `kling-v3-omni` has capabilities across both paths.

`--type` on `model list`/`get` filters by **capability** (the values above).
Don't confuse it with `--type` on `generate create`/`cost`, which is the
**output endpoint** (`video`|`image`) — see Step 3.

`model get --fields` (same output as `--json`) returns one entry per endpoint,
each already flattened to:

- `fields[]` — `{name, type, description, values?, min?, max?}`. `values` is
  the enum choices; `min`/`max` bound a numeric field.
- `constraints[]` — `{id, message, expr}`, a boolean rule over the eventual
  `input` (e.g. a field that's only valid in a certain mode). If your planned
  `input` would fail one, `message` tells you what to change before you submit
  instead of finding out from a 400.

The input mode is a capability, but it is **not** a separate endpoint — at
request time it's decided by which fields you put in `input`: `prompt` only →
text-driven, `image` → image-driven, `refs` → reference-driven. So "does this
model support references?" = "does it have a `ref2video` capability whose
`fields` include `refs`?" — check that, don't guess. If a model exposes both a
`/video` and an `/image` path, pick the one matching the user's intent and
build `input` only from that capability's `fields`.

If the user hasn't named a specific model, read
[`references/model-routing.md`](references/model-routing.md) first — it maps
what the user actually said to a concrete `brand/alias` (video branches for
on-screen text / single image / multi-reference / default, quality tiers, and
an image routing table), with the fallback chain to use when a generation
disappoints. Brands are not guessable (HappyHorse and Wan are `alibaba/`, Sora
is `openai/`, Grok is `xai/`, Seedream is `bytedance/`), so route from that
file rather than from memory, and verify with `model list` before you commit.

Once you know which video model you're using, write the `prompt` field's
wording following that vendor's own formula in
[`references/prompt-engineering.md`](references/prompt-engineering.md) —
Kling, Veo, Seedance, Sora, Vidu, Wan, and Pixverse each respond best to a
different prompt structure, and a Seedance-style prompt on Veo (or vice
versa) tends to underperform.

## Step 2 — Prepare inputs

Image/video fields (commonly `image`, `images`, or `refs`) accept **either a
local file path or an HTTPS URL** — you don't upload anything yourself. When you
pass a local path, the CLI uploads it to Pollo storage as part of the generation
and substitutes the resulting URL before submitting; pass a hosted HTTPS URL and
it's used as-is. (base64 isn't accepted.) There is no separate upload command —
uploads only happen as a step inside `generate create`/`cost`.

## Step 3 — Submit and read the result

```bash
# optional: estimate before an expensive run, or whenever the user is cost-sensitive
pollo generate cost <brand>/<alias> [--type video|image] --name value ...
# -> cost / singleCost / discountCost / discountSingleCost (+ their *Usd counterparts)

pollo generate create <brand>/<alias> [--type video|image] \
  --name value ... --json    # -> { "taskId": "...", "status": "waiting" }

pollo generate wait <taskId> [--timeout 10m] [--interval 3s] --json
# -> { "taskId", "credit", "generations": [{ "status": "succeed|failed",
#      "url", "mediaType", "failMsg" }] }
```

Notes on the flags above:

- You usually don't need `--type`: the CLI resolves the endpoint from
  `/v1/models` on its own. Pass `--type video|image` only when the model
  has both output types (the CLI errors and tells you so), or to skip the
  extra lookup when you already know.
- Every other `--name value` becomes `input.<name>`. Values auto-type:
  `true`/`false` → boolean, numeric strings → number, everything else →
  string. Repeat a flag to build an array (e.g. multiple `--images <url>`);
  `refs` is always sent as an array even from a single `--refs <url>`.
- `--webhookUrl` is lifted to the request envelope's top level, not into
  `input`.
- There is no `--wait` flag on `create` — an unknown flag would be sent as an
  `input` field instead of erroring, so always go through `create` then
  `wait` as two separate calls, and use `--json` on `create` so you can parse
  `taskId` reliably.
- The deliverable lives in the `generations` array: each item carries the
  output `url`, `mediaType`, and per-item `status`/`failMsg`. Parse it from
  the `--json` output — without `--json`, `wait`/`get` print a human summary
  of only the **first** generation, so multi-output results get truncated.
  Hand the user the URL(s); everything before that (taskId, polling) is just
  plumbing you don't need to narrate.

## Credits & recharge

Credits are spent per generation. Gauge affordability up front by comparing
`pollo account status` (`availableCredits`) with `pollo generate cost …`.

When the user is short on credits — **either** you can already see
`availableCredits` is below the cost, **or** a `generate create` fails with
`insufficient credits — recharge at <url>` — treat it as **terminal**: do not
switch models, retry, or loop. Tell the user how many more credits they need and
point them to the recharge page **`<host>/pricing`**, where `<host>` is the
environment you're logged into (`pollo profile current` shows it, e.g.
`https://pollo.ai/pricing`). Always give the actual link, not just "please
recharge".

## Worked examples

```bash
pollo account status
pollo model list --type text2image
pollo model get google/nano-banana --fields

# Text-to-video
pollo generate create bytedance/seedance-2-0-fast \
  --prompt "a red sports car drifting on a mountain road" \
  --aspectRatio 16:9 --duration 5 --json

# Text-to-image (endpoint auto-resolved to /image for an image-only model)
pollo generate create pollo-ai/pollo-image-v2 \
  --prompt "a cozy cabin in a snowy forest, warm light" --aspectRatio 16:9 --json

# Image-to-image (image field = local path, uploaded automatically; or an HTTPS URL)
pollo generate create google/nano-banana \
  --image ./photo.png --prompt "make it nighttime" --aspectRatio 1:1 --json

# Reference-to-video: refs on the video endpoint (repeat --refs for multiple).
# Only refs-capable models accept it — confirm `refs` shows up in model get --fields.
pollo generate create vidu/viduq3 \
  --refs ./character.png --prompt "the character walks into frame" --json

# Dual-output model (both /video and /image): pick with --type
pollo generate create kling-ai/kling-v3-omni --type image --prompt "..." --json

pollo generate cost pollo-ai/pollo-image-v2 --prompt "..." --aspectRatio 16:9
pollo generate wait <taskId>
pollo generate get <taskId>        # one-shot status check, no polling
```

## When it fails

- **Insufficient credits** (`insufficient credits — recharge at …`, or you can
  see `availableCredits` is below the `generate cost`) — **terminal, not a model
  problem.** Do NOT switch models or retry; give the user the recharge link
  `<host>/pricing` and how many more credits are needed. See "Credits & recharge".
- **`403 "This model is not enabled for API access."`** — that model isn't
  exposed on this account/environment, even though `model get` and `generate
  cost` may still succeed for it. Go back to Step 1, pick a different model,
  retry.
- **Any other validation error from the server** — re-run `pollo model get
  <brand>/<alias> --fields` and check the offending field/value against the
  `fields`/`constraints` you got back; something in `input` doesn't match what
  the model actually declared.
- **Expired/invalid token** — `pollo auth login` again. This is only needed
  once the long-lived refresh token itself has expired; the short-lived one
  refreshes automatically.
- **Generation fails uploading a local image (`/file/sign` 403)** — the upload
  step is gated to some accounts. Pass an existing HTTPS image URL for the image
  field instead of a local path.
- **`generate list`** returns the server's raw history shape (always JSON) —
  treat it as opaque history to skim, not a typed result to parse fields out
  of.

## Everything else

`pollo --help` / `pollo <command> --help` cover the full flag list: global
flags (`--profile`, `--json`, …) and profile management
(`pollo profile list|use|current|remove`). The request body
`create`/`cost` build is `{ "input": { ...your --name value... }, "webhookUrl"?
}`, posted to `/v1/generation/{brand}/{model}/{video|image}` (`/estimate` for
cost) and validated against that endpoint's `fields`/`constraints` — the same
data `model get --fields` shows you up front.

The same capabilities are also exposed over MCP (`pollo mcp`, a local stdio
server) for non-terminal agent clients like Cursor or Claude Desktop — same
login and `/v1` endpoints, tools `pollo_list_models` (pass `format: 'fields'` to
read a model's input fields) / `pollo_estimate_generation_cost` /
`pollo_generate_image` / `pollo_generate_video` / `pollo_get_generation_status`.
Image inputs there also take a local path (uploaded automatically) or an HTTPS
URL — there's no separate upload tool. As this skill drives the CLI directly you
won't call those here; see the README "Use as an MCP server" for client setup.
