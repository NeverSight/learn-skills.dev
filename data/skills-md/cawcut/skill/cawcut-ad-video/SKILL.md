---
version: 0.7.0
name: cawcut-ad-video
description: |
  Create a complete product ad video through CawCut's 5-stage AD Video wizard
  (Product → Config → Idea → Storyboard → Video) via the `cawcut ad-video` CLI.
  Use when: "/cawcut-ad-video", "ad video", "video ad", "product ad",
  "广告视频", "商品广告", "带货视频", "产品宣传视频", "make an ad for <product URL>",
  "turn this product page into a video", or the user wants a multi-shot
  marketing video built from a product link with script/storyboard review.
  Requires `cawcut` installed and `cawcut auth login` completed.
  NOT for: single-prompt image/video generation (use cawcut-generate),
  talking-head avatar videos (use cawcut-avatar-video), running published
  Apps (use cawcut-app-run), or listing/deleting/sharing existing Video Ad
  projects (not exposed to the CLI).
argument-hint: "[product URL or product description]"
allowed-tools: Bash AskUserQuestion AskQuestion PushNotification
---

# CawCut Ad Video

Create a complete product ad video through the 5-stage AD Video wizard: **Product → Config → Idea → Storyboard → Video**. Each stage maps to `cawcut ad-video` commands against the developer API. Full command flag tables live in `references/api.md`; stage semantics and the invalidation matrix live in `references/stages.md`; authoring a script edit lives in `references/script-editing.md`; error recovery lives in `references/troubleshooting.md`. `Read` them at `<base_dir>/references/<file>.md` using the base directory printed at the top of this skill body — do not `find`/`grep` for them.

**Reply language.** All live replies — prose, status updates, `AskUserQuestion` / `AskQuestion` questions and option labels — follow the user's language for that turn. This is judged from the user's actual chat message content for that turn — not from whether the `Skill` tool call itself carried an `args` parameter, which is an unrelated, optional pass-through field. This includes implicit triggers: if the skill was invoked because the user's message matched a trigger phrase (e.g. "广告视频", "商品广告", "make an ad for …") rather than the literal `/cawcut-ad-video` command, that trigger phrase **is** the user's chat message content for the turn — reply in its language from the very first response, including when asking for the missing product URL. Only default to English when the invocation carries no language signal at all (e.g. literally just `/cawcut-ad-video` alone with no other text); once the user adds a real request in another language, follow that language for the rest of the session. Keep CLI commands/flags, JSON keys, URLs, and raw error codes in their original form regardless of reply language, and never paste raw English CLI output as the user-facing answer — summarize it in `reply_language`.

## Step 0 — Bootstrap

Run bootstrap as a silent guardrail, not as a user-facing phase.

1. **At most once per AI session.** If any `cawcut` command has already succeeded in this AI session, skip all bootstrap checks and continue.
2. **Use only one explicit check command:** `cawcut upgrade check --json`.
   - If `"update_available": true`, **run `cawcut upgrade` yourself in the host shell** (do not ask the user to type it). After it succeeds, continue this skill from Step 1.
   - If `"ahead_of_registry": true`, continue without upgrading.
   - If `cawcut` is missing, ask the user to install it: `npm install -g @ubnt/cawcut`. Then continue bootstrap.
   - For other check failures, continue and mention the warning only if a later CLI command fails.
3. Do **not** print "bootstrap checks passed" — move directly to Step 1.
4. Let the first real command validate auth. If it fails with token/auth errors (including `Token expired`), **run `cawcut auth login` yourself in the host shell**; tell the user a browser tab will open for OAuth consent; wait for login, then **retry the failed command** once.
5. **Structured user-ask tool (check every session).** In **Claude Code**, use **`AskUserQuestion`** for every enumerable choice; in **Cursor**, use **`AskQuestion`**. If either is available, you **must** use it for all enumerable decisions in this skill — platform, resolution, duration, video type, storyboard style, language, idea candidate, credit confirmation — **including when the candidate list is longer than the popup holds**: a long list still opens the tool, with its leading entries as the options and the full numbered list beside them so any later entry can be typed back (see Interactive selection).

## Wizard overview

```
① Product    create → analyze run → poll → review/confirm analysis
② Config     options → pick settings → config set
③ Idea       idea run → poll → pick candidate (or custom) → idea select
④ Storyboard storyboard run → poll → (optional edit / regenerate) → image quote → confirm → image run (×2 if hand-drawn)
⑤ Video      video quote → confirm → video run → poll → download
```

One project = one `video_ad_id`. Every long stage is triggered without `--wait`, then polled with the bundled script (see Polling). **`cawcut ad-video detail <id> --json` is the single polling point** — only it returns the `outputs` map.

### Bundled-script runner

Use `cawcut` CLI commands directly for project operations and detail inspection. Choose bundled helpers for the host platform. Windows helpers require PowerShell and the installed `cawcut` CLI, not Python, jq, bash, or external curl; do not ask Windows users to install those tools for this skill. macOS/Linux `.sh` helpers require jq; neither platform uses Python.

- macOS/Linux: `bash <base_dir>/scripts/<name>.sh …`
- Windows PowerShell: `powershell -ExecutionPolicy Bypass -File "<base_dir>\scripts\<name>.ps1" …`

The three helpers (`poll`, `script_plan`, `download_media`) have equivalent `.sh` and `.ps1` implementations. Use the matching extension and platform-specific flags throughout one run; for example, `--kind video` on bash is `-Kind video` on PowerShell.

## Stage ① — Product

1. Collect the product URL (Amazon/Shopify/official page all work). If the user didn't give one, ask in plain text (open-ended). Do NOT ask for a project name — the backend auto-names the project from the product info after analysis/export.
2. `cawcut ad-video create --url "<url>" --json` → capture `id`. `--url` is optional at create (an empty draft is allowed), but pass it whenever the user gave one — `analyze run` requires it later regardless. `--category` is optional; omit it and the backend auto-detects after analysis. Only pass `--name` if the user explicitly asked for a specific title.
3. `cawcut ad-video analyze run <id> --url "<the product URL from step 1>" --json` (no `--wait`; the API requires `url` in the body), then poll with the platform runner: `poll.sh <id> '.status' stage_completed 600 15` on macOS/Linux, or `poll.ps1 <id> '.status' stage_completed 600 15` on Windows.
4. Read `detail <id> --json` and present the analysis result:
   - **Product info verbatim** — every populated `product_info` field: `name`, `description`, `selling_points[]` (each in full, numbered), `target_audience`, `brand_style`, `promotional_info`, `source_platform`, `category`. Do not summarize, truncate, or translate the product content itself — it is the user's marketing copy and must be shown as returned; only your surrounding labels and prose follow reply_language.
   - **Product images** — first download them with the platform-specific `download_media` helper: `<id> --kind product`. Then present by category (labels in reply_language):
     - **Logo** (`logo_images`) and **Primary images** (`primary_images`): preview each inline via the host's send-file tool (e.g. Claude's `SendUserFile`) with the local path just downloaded (e.g. `~/Downloads/ad-video-<name>/product/logo-1.jpg`, `primary-1.jpg`) — a markdown link only renders as a clickable line, not a visible image.
     - **Additional product images** (`images[]`): if inline previews are supported, list them **one by one**, each labeled `Product Image #n` with the image sent inline; **cap at the first 9** — if there are more, say so (e.g. `…and N–9 more`) and tell the user the rest are in the `<dest>/product/` folder. If inline previews are not supported, list them as a table of local paths (`#` + path) and point to the same folder.
     - No `asset_id` column in either form — the local path is a **preview** reference only. These files exist so the user can see the images; never hand them back to the CLI.
   Then ask the user to confirm or correct via AskUserQuestion:
   - `✅ Looks good` → continue to Stage ②
   - `✏️ Edit product info` → collect the changes and pass **only those fields** to `cawcut ad-video product set <id> …`: the command reads the project first and carries every field you did not pass forward. (The API replaces `product_info` wholesale, so a bare `--product-name` would otherwise erase the description, the images and the selling points.) Re-run `analyze run` afterwards if the URL or the product changed materially.
     - **An image list is replaced by passing it**, so `--logo` / `--primary-image` / `--asset` take the complete kept list — that is also how an image is removed. A replaced list drops its own selection, and the backend falls back to its defaults (every candidate for `--asset`, the first candidate for logo/primary). Never re-send the files you downloaded: the persisted refs already come back as `asset_id`s.
     - Pass a local path only for an image the user supplies from outside the project; the CLI uploads it as a brand-new asset (7-day TTL).
     - `--description ""` clears the description and `--clear-selling-points` empties the selling points — an empty list is a real state, not "unset".
5. If the user wants to abort a running analysis: `cawcut ad-video analyze cancel <id>`.

**Material rights (state this once, when the user supplies their own image).** Images uploaded through the CLI are **not** run through the material compliance check and are accepted as-is — there is no rights attestation step to walk through, unlike the web portal. That check exists to catch third-party logos and celebrity likeness; on this path the responsibility for holding the rights to the material sits with the user. Say so plainly in one sentence before uploading, so nobody assumes the tool vetted it. This applies only to *new* files the user supplies: images already in the project (crawler-extracted product images) were never subject to it.

## Stage ② — Config (all options are runtime-fetched, never hardcoded)

1. `cawcut ad-video options --video-ad-id <id> --json` → read `video_settings` (publish_to, languages, aspect_ratios, resolutions, duration_ranges, video_types, storyboard_styles, video_models, defaults).
2. Ask the axes in this order — **video type first**, because it decides both whether captions are a question at all and which model/resolution combinations are legal.
   - **video type** — one option per entry in `video_types`.
   - **video model** — **only when `video_models` is non-empty.** Candidates are `video_models[].value`, default `defaults.video_model`. The table that carries the list has three columns beyond `#`: **the model, its `supported_resolutions`, and a default mark on `defaults.video_model`** — the resolutions belong in view because picking a model is what decides which ones stay legal on the next axis. With exactly one candidate, state it in prose and carry on (one option is not a choice); with none, skip the axis entirely.
   - **resolution** — default `defaults.resolution`, then **clamp to the chosen model's `supported_resolutions`** (the same list the server validates against). Never offer a resolution the model does not support: `config set` rejects it. When no model was chosen, offer the full `resolutions` list.
   - **auto captions** — **only for `product_with_voiceover` and `talking_video`.** Captions are burned in from the voiceover/dialogue track, so `product_showcase` has nothing to caption; do not ask, and pass `--auto-captions false` explicitly (mirrors the web portal, which forces the value off for that type).
   - **platform** — show each option's `default_aspect_ratio` in its description (e.g. `TikTok — 9:16`), **language**, **duration**, **storyboard style** (explain: hand-drawn adds a sketch pass before photo-realistic panels).
   - **Aspect ratio is NOT a question.** It is bound to the platform (mirrors the web portal, which has no ratio selector): take the picked `publish_to` option's `default_aspect_ratio` automatically. Never ask for a ratio separately; only if the user explicitly overrides should you deviate from the platform default.

   Batch the axes into **one** AskUserQuestion call — one question per axis, at most four questions per call. A long axis (**platform**, **language**, **video model**) follows Interactive selection's overflow shape: the full list is a numbered table in the message body — `#` plus what that axis actually carries: a platform's label with its `default_aspect_ratio`, a language's label, a model's label with its `supported_resolutions` and default mark. The question itself is one short sentence, the popup holds the leading entries as options labelled with their number, and the entries past them are answered by number or name in the free-text field. Each axis keeps its own table and its own numbering — the answer goes into that axis's own field, so never ask for two numbers at once (`1 + 10`).
3. `cawcut ad-video config set <id> --publish-to … --language … --aspect-ratio <the platform's default_aspect_ratio> --resolution … --duration-seconds … --video-type … --video-model … --storyboard-style … --auto-captions … --json`

`video_model` is a real cost lever — say so when offering it (a cheaper model may be available), but never present a model the endpoint did not return.

## Stage ③ — Idea

1. `cawcut ad-video idea run <id> --json`, poll until `outputs.generated_marketing_messages.status === "succeeded"`.
2. **Reveal up to eight, then stop.** One run generates up to 16 candidates but `detail` hands back one page (4) at a time, so a fresh read shows only the first four. Read `outputs.generated_marketing_messages`, and call `cawcut ad-video idea load-more <id> --json` (re-reading `detail` each time) until **eight are visible** or `has_more === false` — whichever comes first:
   - `load-more` only reveals already-generated candidates — no LLM call, no credit cost.
   - **Eight is the ceiling, not a target.** A project holding fewer shows fewer; once eight are visible you stop revealing even if `has_more` is still true. This flow has no "one more batch" step.
   - State the number you are showing, and never imply the set is everything the project holds when it is not.
3. Present them **as a table, in full, verbatim** — one row per candidate: `#`, title, content. No summarizing, no paraphrasing, no truncating, no translating: this is the user's marketing copy and they are choosing between the whole set. Lead with the count (e.g. "Showing 8 candidates:"). The `#` column is the popup's index — this table is what any number the popup could not hold is typed against.
4. **One decision, one question.** The choice is a **single** AskUserQuestion — never a candidate question followed by a second one asking what to do with that answer. Four options, in this order:
   - `1. <title>`, `2. <title>`, `3. <title>` — the first three candidates, each labelled with its number
   - `✏️ Write my own` → submit the idea text the user or agent produced with `idea select <id> --custom "<text>"` (60–10000 chars, mirroring the web custom-idea limits). This follows the portal custom path: the CLI sends that text as `custom_content` with `is_custom: true`; do not turn it into a generated-candidate selection or add a title wrapper.
   - a candidate from the fourth to the eighth is selected by typing **its number or its title** into the free-text field; name that in the question's own text, in `reply_language`, so the user answers from a set the question stated rather than guessing
5. On a pick: `cawcut ad-video idea select <id> --message-id <mm-N> --title "<title>" --content "<content>" --json`. Offer light edits to title/content before submitting.
6. **A fresh batch is user-initiated only.** `idea regenerate` is not a menu entry: when the user asks for one in their own words ("换一批" / "regenerate"), run `cawcut ad-video idea regenerate <id> --json` + poll — it clears the current selection, so warn first — then re-reveal (step 2) and re-ask (step 4).

## Stage ④ — Storyboard

1. `cawcut ad-video storyboard run <id> --json` (optional `--style-id` from the options storyboard section), poll until `outputs.storyboard_plan.status === "succeeded"` — the 3600 deadline from the polling table, which is a give-up line and never a figure to quote.
2. Read `detail <id> --json` → `outputs.storyboard_plan.value`. Show the plan as a concise shot table. The table contains the user-reviewable fields only; prompts remain in the stored plan but are not displayed:
   - plan level, above the table: `title`, `synopsis`
   - per shot, in this order: `shot_no` (**Shot #**), `duration` (**Duration**), `shot_type` (**Shot Type**), `shot_description` (**Shot Description**), `dialogue` (**Voiceover** — that is its business meaning), `camera` (**Camera**), `light` (**Light**), `sfx` (**SFX**)
   - Omit the Voiceover column for `product_showcase` (the web portal hides it too — that type has no spoken track).
   - Never show `shot_prompt`, `video_prompt`, or their statuses in the table or elsewhere in the reply. They are implementation fields, not review content.

   Then ask via AskUserQuestion:
   - `✅ Looks good` → continue
   - `✏️ Work on the script` → **the script is a file in the project folder; the table is rendered from it.** Run the platform-specific `script_plan` helper with `take <id>` once — it writes the plan to `<dest>/storyboard/script.json` and prints the paths. Edit **that file**, never a plan retyped from context. After every change, write the fields you touched into a small edits JSON and run the same helper with `show <plan.json> <edits.json>`: it applies them, lists what it applied, and prints the whole current review table. Say what changed, then paste that table into your reply text — the script's stdout is a tool result the user does not see; only what you write in your own message counts as shown. A diff alone makes them hold the rest of the script in their head. **Nothing reaches the server until they confirm**, so a half-formed idea costs no revision, no invalidation and no credit. **When you customize any user-visible shot field, you must also update the hidden `shot_prompt` and/or `video_prompt` in the same working copy according to the association table in `references/script-editing.md`; submit them but do not display them.** The platform's own Prompt Generator is the alternative when you would rather not write them. The edits-file format, the prompt shapes, the trigger mapping and the server's limits are in `references/script-editing.md` — read it before the first edit.
     - **Editable per-shot fields:** `duration`, `shot_type`, `shot_description`, `dialogue` (the Voiceover column), `camera`, `light`, `sfx`, `shot_prompt`, `video_prompt`. **Never add or remove shots** — the count comes from the generated script, and the portal's editor has no such action either. Rewriting a shot's content is the way to change it. `shot_type`/`camera` option values come from `cawcut ad-video options --json` → storyboard section, never hardcoded. Everything else in the file (`assets`, `character_refs`, `scene_ref`, the prompt statuses) is carried through untouched — the script refuses to edit it.
     - **Save once:** `cawcut ad-video storyboard set <id> --base-revision <value.revision> --plan-file <dest>/storyboard/script.json --json`; on `409` re-read detail, take a fresh copy and re-apply the same edits, save again — the edits file is your record, so nothing is lost. The CLI checks the whole plan against the server's own `constraints` before sending it: a refusal names the shot and field, nothing was sent, and the shot at fault is often one you did not edit — fix that field and save again, never resend the same plan. If `--update-prompts` was used, the save only starts asynchronous prompt generation: poll `.outputs.storyboard_plan.prompt_status` to `succeeded` before treating either prompt as ready; `storyboard_plan.status: succeeded` alone is not sufficient.
     - `duration` or the shot set changing invalidates the sketch, the panels and the final video: say so before the save, then run the invalidation protocol.
   - `🔁 Regenerate the script` → `cawcut ad-video storyboard run <id> --force` + poll. **Warn before running it: this discards every edit** — the script LLM writes a new script from the same idea and config. It is the only way back to a platform-written script; a plain re-run will not do it (unchanged inputs make it a no-op). Re-show the table and ask again.
3. **Quote before every image run:** `cawcut ad-video image quote <id> --generation-type <type> --json` → AskUserQuestion to confirm the credit cost → **immediately** `cawcut ad-video image run <id> --generation-type <type> --confirmation-token <token> --json` (token TTL is 5 minutes — do not pause between confirm and run). See Quote timing.
4. Branch by storyboard style (from Stage ② config):
   - `hand_drawn_then_photo`: pass 1 `--generation-type hand_drawn` → poll `storyboard_sketch` → preview the sketch (Media preview & downloads), AskUserQuestion `✅ Continue to photo-realistic` / `✏️ Edit script` → pass 2 `--generation-type photo_realistic` → poll `storyboard_image`
   - `photo_realistic_only`: single `--generation-type photo_realistic` run → poll `storyboard_image`
5. Generation-stage polls use the longest deadline in the polling table (3600). On success, preview the sketch/grid image per Media preview & downloads (platform-specific `download_media <id> --kind storyboard`), then continue.

## Stage ⑤ — Video

1. `cawcut ad-video video quote <id> --json` → AskUserQuestion confirm credits → immediately `cawcut ad-video video run <id> --confirmation-token <token> --json` (add `--force` only when the user explicitly re-renders an unchanged result).
2. Poll until one of `final_video` / `voiceover_final_video` / `talking_video` is `succeeded` — the 3600 deadline from the polling table.
3. On success: download the video into the project folder with platform-specific `download_media <id> --kind video` and take the printed path (`cawcut ad-video video run <id> --wait --download` is only for when you haven't triggered the run yet). See Media preview & downloads.
4. Report `local_path` and the result URL, then **hand off unconditionally to `cawcut-vn`** with `<local_path>` — no VN menu, no `cawcut vn` commands of your own (decide-once: the receiving skill owns the VN decision and you never re-check).

## Media preview & downloads

All media URLs the API returns (product images, storyboard sketch/grid, final video) are **pre-signed** — plain `curl` downloads them directly, no extra signing step. If one ever 403s, re-read `detail` and retry with the fresh URL (product image URLs are re-signed on every `detail` call).

**Preview priority** (product logo/primary images, storyboard sketch/grid):
1. If the host has a send-file-to-user tool (e.g. Claude's `SendUserFile`), download the file first, then send it so the user previews inline in the chat.
2. Otherwise `open` the downloaded file (macOS) or just report the local path.

Always use the bundled downloader instead of hand-rolling curl/jq pipelines:

```bash
# macOS/Linux
bash <base_dir>/scripts/download_media.sh <id> [--kind product|storyboard|video|all] [dest_dir]

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File "<base_dir>\scripts\download_media.ps1" <id> [-Kind product|storyboard|video|all] [-Destination <dir>]
```

Default dest: `~/Downloads/ad-video-<product-name>` (falls back to `ad-video-<id>` before the project is named). Layout: `product/` (logo + primary + additional images), `storyboard/` (sketch + panel grid), final video at the folder root. It prints every saved path — relay those paths to the user in `reply_language`.

## Invalidation semantics (mandatory — mirrors the web portal)

After **every** mutation (`product set`, `config set`, `idea select`, `storyboard set`):

1. Immediately run `cawcut ad-video detail <id> --json`. First distinguish **cleared** artifacts from **retained-but-stale** artifacts; never infer either from the project history.
   - A mutation to any creative config field — `--duration-seconds`, `--language`, `--video-type`, `--storyboard-style`, or `--publish-to` — clears downstream content. If `outputs.generated_marketing_messages` no longer has a usable succeeded `value` / `selection`, the previous Idea does not exist in the current project state. **Do not ask whether to reuse, keep, or continue using that Idea; do not offer it as an option.** Continue at Stage ③ with `cawcut ad-video idea run <id>`, poll it to success, select a fresh Idea, then generate a new storyboard.
   - Only an output that remains present with `status: "succeeded"` and `need_regenerate === true` is retained-but-stale and eligible for the regeneration/later decision. A cleared output is neither stale nor reusable.
2. Collect every retained-but-stale `outputs.<key>` with `need_regenerate === true`. If any exist: list the affected artifacts to the user in one message, then a **single** AskUserQuestion:
   - `🔄 Regenerate affected` → re-run the affected stages in pipeline order (`storyboard run` → `image quote/run` → `video quote/run`), quoting + confirming credits again per generation stage
   - `⏸ Later` → continue without regenerating; note the stale artifacts
3. **Never** regenerate mid-edit — batch all user edits first, then regenerate once. A script save must only show affected outputs as needing regeneration; it must never trigger an image or video quote/run. Running `image run` / `video run` happens only after the user explicitly confirms that stage's fresh quote, and is rejected while an upstream output has `need_regenerate=true` (`VIDEO_AD_NEEDS_REGENERATION`).

## Quote timing (mandatory)

`confirmation_token` expires **5 minutes** after quote. Always: quote → AskUserQuestion confirm → run, back-to-back with no user discussion in between. If `run` fails with a token/confirmation error (expired or invalidated), **re-quote, ask again, run again** — once per attempt, no silent retries.

**Check the balance before asking to spend (mandatory).** `image quote` / `video quote` also report `credits_balance`, `credits_shortfall` and `credits_sufficient` alongside `estimated_credits`. Look at them **before** the confirmation question:

- `credits_sufficient === false` → say the numbers plainly ("this needs X, your balance is Y, short by Z") and send the user to top up on the web portal. The confirmation menu should offer `💳 Top up credits` / `⏸ Not now` instead of a routine confirm-and-run — do not walk a user into a charge they cannot pay for.
- `credits_sufficient === true`, or the balance is **unavailable** (`credits_balance_error` — the lookup is best-effort and must never block) → normal confirmation.
- Never present an insufficient balance as a generic failure after the fact. The whole point is to say it *before* the run.
- Topping up takes longer than the token's 5 minutes: on the user's return, re-quote → re-confirm → run. Never reuse the stale token.

## Polling (bundled script — mandatory)

Trigger without `--wait`, then poll with the platform-specific bundled script. **Never hand-roll polling loops** — an ad-hoc `echo "$var" | jq` loop corrupts the JSON under zsh (echo interprets `\n` escapes) and spins forever without matching a terminal state.

```bash
bash <base_dir>/scripts/poll.sh <id> '<json_path>' <success_value> <timeout_s> [interval_s=30]

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File "<base_dir>\scripts\poll.ps1" <id> '<json_path>' <success_value> <timeout_s> [interval_s=30]
```

| Stage | json_path | success_value | timeout_s |
|---|---|---|---|
| ① analyze | `.status` | `stage_completed` | 600 |
| ③ idea | `.outputs.generated_marketing_messages.status` | `succeeded` | 600 |
| ④ plan | `.outputs.storyboard_plan.status` | `succeeded` | 3600 |
| ④ prompts | `.outputs.storyboard_plan.prompt_status` | `succeeded` | 600 |
| ④ sketch | `.outputs.storyboard_sketch.status` | `succeeded` | 3600 |
| ④ panels | `.outputs.storyboard_image.status` | `succeeded` | 3600 |
| ⑤ video | `.outputs.final_video.status // .outputs.voiceover_final_video.status // .outputs.talking_video.status` | `succeeded` | 3600 |

The Windows helper parses these dotted paths and `//` fallbacks internally; `json_path` does not require jq on Windows.

Exit codes: `0` success · `2` failed (report the output's `error` from `detail --json`; see `references/troubleshooting.md`) · `3` timeout → AskUserQuestion `⏳ Continue waiting` (run the script again) / `❌ Stop` (project persists; resume later with `cawcut ad-video detail <id>`) · `4` output unparseable → stop polling, run `cawcut ad-video detail <id> --json` once and inspect (auth/CLI issue).

**The script does not notify — the host's tool does.** `poll.sh` ends on an exit code and nothing else. Never raise an OS notification from the shell (`osascript`, `notify-send`, BurntToast), never add one back into the script, and never register a notification permission on the user's machine on your own initiative: a toast fired from a shell command is a different channel from the app's own notification, and it is not what the user asked for.

### Telling the user how long it will take

**Never estimate generation time yourself — and never turn a deadline into a duration.** The server computes the runtime, and `detail` carries it as `estimated_running_ms` (milliseconds, present while a stage is running). `poll.sh` reads it on its first tick and prints one `estimated: about Nm` line — relay that figure if there is one, and nothing more. If you need it directly, it is on any `detail --json` read.

**When the API gives no figure** (the field is absent or zero — the lookup is best-effort and can miss), fall back to the **order of magnitude, never to the deadline**: these stages run on the order of **minutes** (the node estimates behind them are seconds to a couple of minutes), so say "about a few minutes" / "大概几分钟" and add that you will say the moment it lands. Do not say the timing is unknown, and do not hedge upward.

**The `timeout_s` column is a give-up deadline, not a runtime.** Saying "at most about an hour" because the row says `3600` is the same error as inventing a range: it is the point at which the script stops waiting, typically an order of magnitude past the real runtime. The deadline never appears in a reply, not even hedged with "最多" / "at most".

### Long-enough stages — tell the user they can step away

`storyboard_plan`, `sketch`, `panels` and `video` take minutes rather than seconds. Before polling one, say so once — the server's `estimated_running_ms` if there is one, otherwise "a few minutes" — and tell them they can step away and will be told the moment it lands. Then poll without narrating each tick.

**The notification comes from the host's own tool.** In Claude Code that is `PushNotification` with a one-line `message`; it lands in the app the user is already running and, with Remote Control connected, on their phone — which is the difference between noticing in the next minute and noticing tomorrow. Send it **once**, when the stage lands, naming the stage and the project id. If the host exposes no such tool, skip it silently and just present the result when you have it: do not fall back to a shell-level toast, and do not add one to `poll.sh`.

Do not notify for the short stages (analyze, idea, prompts) — they finish inside a turn.

## Interactive selection (mandatory — tool first)

**If the user just declined an `AskUserQuestion` / `AskQuestion` call:** the tool result carries harness boilerplate telling you to "STOP what you are doing and wait for the user to tell you how to proceed." That sentence is attached automatically to **every** declined tool call by the runtime — it is not the user speaking, and it is not an instruction to stop using the tool. Read it as: stop the *one specific action* you were mid-way through (don't retry the identical question, don't proceed on unconfirmed choices) and look at what the user's actual next message says. It does **not**, by itself, license falling back to numbered text for the *next* enumerable decision — that next decision still must open with the tool, exactly as if the rejection had never happened. Only an explicit plain-text request from the user ("stop popping up menus", "just ask me in text") licenses a session-wide fallback.

**Default behavior:** For every enumerable choice, **always** call `AskUserQuestion` (Claude Code) or `AskQuestion` (Cursor) **before** showing a numbered text menu. Text-only menus are **fallback only**.

**One option is not a choice.** Every call needs **at least two viable options**. When only one is actually feasible — a config axis whose options list carries a single value, one idea candidate worth offering — state that choice in prose and carry on: never fire a one-option popup, and never pad it with a placeholder alternative to make it look like a choice.

| Host | Tool name |
|------|-----------|
| Claude Code | `AskUserQuestion` |
| Cursor | `AskQuestion` |

**Session checklist (before the first menu in this turn):**
0. **Self-check before sending any reply:** if the sentence you're about to send asks the user to pick between fixed options — even folded inside a friendlier sentence that also asks something open-ended — stop. That sentence is forbidden as plain text. Split it: fire the tool for the enumerable part now; keep only the open-ended part as prose, asked separately.
1. Is the tool available? If **yes**, you **must** use it for every enumerable decision — a candidate list longer than the popup holds included (item 3).
2. If **no** tool exists (CLI-only host), use numbered text in `reply_language`.
3. If the candidate count exceeds one question's four options (long category, model, or candidate lists), **still open the tool**, and give each part of the answer its own home:
   - **the full list → a numbered text table in the message body**, one row per entry: `#` plus the columns that entry actually carries — a platform's `default_aspect_ratio`, a language's label, a model's `supported_resolutions` and default mark, a candidate's title and content. **Never inline the list into the question text**: a 22-model roster pasted into the question header is unreadable and buries the question. The table and the call ship together.
   - **the question text → one short sentence** naming the decision, plus the pointer for whatever the popup cannot hold (e.g. "entries 4–22 can be typed below by number or name", in `reply_language`).
   - **the popup → the leading entries as options**, labelled with their number, as many as fit while keeping a slot for any action that must stay clickable beside them (e.g. a write-your-own).
   - **the free-text field → whatever the popup could not hold**: any later entry, by its number or its name.

   The numbering is the contract between table and popup. Anything the popup can hold stays clickable; a typed answer is only for what it cannot. One question per decision — never a second question asking what to do with the answer to the first.

**Forbidden while the tool is available:** a numbered text menu **instead of** the call, "reply with the number or name" with no popup behind it, or asking the user to type enum values from memory. A long list's numbered table is not a text menu — it is the call's index, and it never ships alone.

**Never hardcode option values.** Platform, resolution, duration, video type, video model, storyboard style, language, and style IDs come from `cawcut ad-video options --json` output **this session** — not from this document, not from training data.

## UX Rules

1. Be concise. Default output is the result URL and local path. No raw JSON dumps unless debugging (`--json` is for the polling script).
2. **Reply language**: see the top-of-file rule — follow the user's language for every reply (including the first one and all AskUserQuestion questions/labels), and summarize CLI output in `reply_language` instead of pasting raw English.
3. Do not call CawCut HTTP APIs with curl — the CLI handles auth and tokens.
4. **Choice-first** — every enumerable decision (config axes, idea candidates, credit confirmations, regenerate confirmations) goes through AskUserQuestion/AskQuestion per Interactive selection.
5. **One project per request.** If the user asks for several ad videos, finish one wizard before starting the next.
6. **V1 contract only.** Do not consume or promise character/scene (V2) capabilities; they are not exposed to developer tokens.
7. Credits: always quote + confirm before `image run` / `video run`. Never spend credits without an explicit user confirmation in this session, and **read the quote's balance figures first** — an insufficient balance is stated before the confirmation question, not discovered by a failed run (see Quote timing).
8. Long stages (`storyboard_plan`, `sketch`, `panels`, `video`) take minutes, not seconds: say so once — quoting the server's `estimated_running_ms`, or "a few minutes" when there is none (see Polling); never the deadline — tell the user they can step away, and let the notification bring them back. Don't narrate each poll tick.

## CLI quick reference

```bash
cawcut ad-video create [--url <u>] [--name <n>] [--category <c>] [--json]
cawcut ad-video detail <id> [--json]
cawcut ad-video options [--video-ad-id <id>] [--language <l>] [--json]
cawcut ad-video product set <id> [--product-name …] [--description …] [--selling-point …] [--clear-selling-points] [--logo <ref>] [--primary-image <ref>] [--asset <ref>…] [--target-audience …] [--promo-*] [--json]   # only the fields passed change
cawcut ad-video config set <id> [--publish-to …] [--language …] [--aspect-ratio …] [--resolution …] [--duration-seconds …] [--video-type …] [--video-model …] [--storyboard-style …] [--auto-captions …] [--json]
cawcut ad-video analyze run <id> --url <u> [--wait] [--json]   ·   analyze cancel <id>
cawcut ad-video idea run <id> [--wait] [--json]   ·   idea select <id> (--message-id <m> | --custom <text>)   ·   idea regenerate <id>   ·   idea load-more <id>
cawcut ad-video storyboard run <id> [--style-id <s>] [--force] [--wait] [--json]   ·   storyboard set <id> --base-revision <n> (--plan <json> | --plan-file <path>) [--update-prompts --prompt-target <shot_id>:<fields>…]   # run --force rewrites the script, discarding saved edits
cawcut ad-video image quote <id> --generation-type <hand_drawn|photo_realistic>   ·   image run <id> [--confirmation-token <t>] [--generation-type <t>] [--force] [--wait] [--download]
cawcut ad-video video quote <id>   ·   video run <id> [--confirmation-token <t>] [--force] [--wait] [--download]
```

## Errors

| Symptom | Action |
|---------|--------|
| `Token expired` | Run `cawcut auth login` in the host shell, then retry the failed command |
| `VIDEO_AD_NEEDS_REGENERATION` / `308000414` | An upstream output is stale — re-run the flagged stage first (see Invalidation semantics) |
| Confirmation token expired/invalid | Re-quote, re-confirm with the user, run again (see Quote timing) |
| `409` on `storyboard set` | Revision mismatch — re-read `detail`, retry with the fresh `value.revision` |
| `409` concurrent run | Another stage run is in flight — poll `detail` until it settles, then retry |
| `400` on `config set` | Bad enum, unmet stage gate, or a resolution the chosen `video_model` does not support — re-read `ad-video options` |
| Insufficient credits (from the quote) | `credits_sufficient: false` — state the shortfall and send the user to top up; re-quote on their return (see Quote timing) |
| CLI not found | `npm install -g @ubnt/cawcut` (Step 0) |

Full recovery trees: `references/troubleshooting.md`.
