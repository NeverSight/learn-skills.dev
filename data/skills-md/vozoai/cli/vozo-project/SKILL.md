---
name: vozo-project
description: Orchestrate Vozo CLI project workflows—single-tool create-to-download, multi-step pipelines, batch multi-language creation, and filtered bulk downloads. Use for translate dub, translate subtitles, visual translate, lipsync, folder/URL sources, and artifact downloads. Also use when the user asks what Vozo or this CLI is or what it can do (product introduction).
compatibility: cursor, codex, claude-code, workbuddy
metadata:
  author: vozo
  version: '0.7.5'
  homepage: https://www.vozo.ai
  repository: https://github.com/vozoai/cli
  npm: https://www.npmjs.com/package/@vozoai/cli
---

# Vozo Project

## CLI prerequisite

Requires the official `vozo-cli` from npm [`@vozoai/cli`](https://www.npmjs.com/package/@vozoai/cli) (source: [github.com/vozoai/cli](https://github.com/vozoai/cli)). Install with `npm install -g @vozoai/cli` or `npx @vozoai/cli@latest install`. Do not install from third-party mirrors. Auth is handled by `vozo-auth`.

## Follow the documented CLI interface

For normal Vozo project workflows, follow this skill, its referenced documents,
and `vozo-cli ... --help`. Do not inspect the CLI source code to discover how to
perform a documented operation, and do not replace documented CLI commands with
direct calls to inferred internal APIs.

Source inspection is appropriate only when the user explicitly asks to develop,
debug, review, or explain the CLI implementation, or when the documented
interface is missing or inconsistent. If documentation is insufficient, state
the gap instead of silently guessing.

## What is Vozo / what can this CLI do (unified pitch)

When the user asks anything like "what are you / what can you do / what is this / what can the CLI do / introduce Vozo", answer with the following canonical pitch (translate it into the user's language, but keep product names in English):

> **Vozo** ([vozo.ai](https://www.vozo.ai)) is an AI video platform for taking one video to every language and audience. **Vozo CLI** brings its four core tools into your terminal and agent workflows:
>
> 1. **Translate & Dub** — translate a video (or audio) and re-voice it with AI voice cloning that keeps the original speakers' voices.
> 2. **Translate Subtitles** — generate translated subtitles for a video.
> 3. **Visual Translate** — translate the on-screen text burned into the video frames.
> 4. **Lip Sync** — re-sync the speakers' lips to match new audio (including dubbed audio from Translate & Dub).
>
> From the CLI you can create projects from local files, folders, or video URLs (batch supported), track processing, and export/download the results (videos, audio tracks, subtitles). Fine-grained editing — fixing translations, changing voices, redubbing — happens in the Vozo web editor: every project comes with a link you can open anytime.

Keep the pitch to this scope. Do not promise features the CLI does not have (no video generation, no talking photo, no editing from the CLI), and do not enumerate internal flags in the pitch.

## Product Naming

Use Vozo website product names in user-facing text. Keep CLI command paths unchanged:

| Product             | CLI                           |
| ------------------- | ----------------------------- |
| Translate & Dub     | `project translate_dub`       |
| Translate Subtitles | `project translate_subtitles` |
| Visual Translate    | `project visual_translate`    |
| Lip Sync            | `project lipsync`             |

**Write "Translate & Dub" with the ampersand — for video and audio alike; never "Translate dub" / "Translate Dub" without `&`.**

**"Vozo" is a brand name — never translate, transliterate, or localize it.** Always keep it exactly as `Vozo` (capital V) in every language and in all user-facing text, summaries, and messages.

## When to Use This Skill

- Create projects from **local folder / files / URL** for dub, subtitles, visual translate, or lipsync.
- **Create or find dashboard folders** (`project folder create` / `folder list` / `folder search`) and create projects inside them with `--folder`.
- Run **create → poll → export (if needed) → download** for any single tool.
- **Chain** multiple tools (user specifies order, or you propose a plan).
- When the user provides an **existing Translate & Dub project id** and wants one
  or more additional target languages, prefer `translate_dub more-languages` so
  the existing edits are preserved. Consider repeating `create` only when the
  user explicitly wants independent projects from the original media.
- **Create independent projects in many languages from original media** by repeating create with different `--target-language`.
- **Bulk download** after listing/searching with filters (folder, kind, date, language, title).
- Give users **project links** (`webUrl`) and `open` so they can edit on the web.

## Preferred Commands

```text
vozo-cli auth status | points | membership
vozo-cli project list | search | folder list | folder create | folder search | delete
vozo-cli project <tool> create | get | open | export | download
vozo-cli project translate_dub more-languages <id> --target-language <languages...>
```

`<tool>` = `translate_dub` | `translate_subtitles` | `visual_translate` | `lipsync`

## Core Workflow

### 1. Always start with auth

1. `vozo-cli auth status` — if not signed in, use `vozo-auth` / `auth login`.
2. Before **batch create** or expensive chains: `auth points` + `auth membership`.

### 2. Single-tool: create → download

For each project, **only continue past create/poll when the user explicitly asked for export/download**:

1. **Create** with the right `project <tool> create` flags.
2. **Poll** `project <tool> get <id>` until the `processing` field is `false` (or status is failed). Do not interpret status strings yourself — `processing` already covers project status, sub-task, and export in-flight states. **Field path:** `get` stdout nests everything under a top-level `project` key — `{ "project": { ..., "processing": <bool>, "status": "...", "errorCode": <string|null>, "errorMessage": <string|null> } }` — so read `project.processing` (e.g. `jq -e '.project.processing'`), never the top level. If extraction returns null/missing, that is a script error: abort the poll loop instead of treating it as "still processing". When the status reports a failure, summarize with `project.errorCode` and `project.errorMessage` (CLI maps these to web-aligned copy).
3. **Export** `project <tool> export <id>` when a media artifact is missing — **only if the user asked to export or download outputs**. Export checks for an existing download URL first: if one is present it returns `status: "already_exported"` with `downloadUrl` and does not re-export; otherwise it returns `status: "started"`. Treat `already_exported` as success (artifact ready) — not a failure or skip-error.
4. **Download** each requested artifact with `--output` — **only when the user asked for files on disk**. Pass a **directory** per project (trailing `/`) so files get the same product names as web downloads (e.g. `{title}_{language}_translated.mp4`, `{title}_{language}_subtitles.srt`); only pass a file path when the user explicitly asked for a custom name.
5. **Share** `webUrl` from create/get. Whenever you hand out a project link, tell the user (especially first-time users) that they can open it to **review and edit the result** — fix translations, change voices, redub — if they are not satisfied; `project <tool> open <id>` opens it directly.
6. **When processing finishes** (polling ends), proactively tell the user and ask whether they want the outputs downloaded (unless they already opted in/out at plan time). Offering is required; silently downloading is forbidden (§3.2), and silently stopping at "done" with no next step is poor service.

### 2.5. Long-running polling should move to the background

When the user asks for an end-to-end flow such as **upload/create → wait → export → download**, do not keep the foreground agent blocked on dense polling for long processing jobs.

Rules:

1. After `create` / `export`, return quickly with the accepted project `id`, `kind`, `webUrl`, current status, and the planned next step.
2. If the environment supports background work, move the repeated `get` polling to the background and resume the foreground only when:
   - the project is ready for `export`
   - the export is ready for `download`
   - the project fails
3. While polling runs in the background, the foreground response should stay concise:
   - what has started
   - which ids are being watched
   - where outputs will be downloaded
4. If the environment does **not** support true background execution, do not busy-wait in the foreground. Instead:
   - do sparse polling only when useful
   - return control to the user quickly
   - tell the user the current status and the exact follow-up command to resume
5. For batch jobs, background polling should track each project independently and only surface projects that changed state or need the next action.

Foreground waiting is only acceptable for short checks. Long processing and export waits should be treated as background watch tasks whenever possible.

### 2.6. Existing Translate & Dub project → more languages

Prefer `project translate_dub more-languages <id>` when the user provides an
existing Translate & Dub project id and wants its **edited result** translated
into additional target languages. This preserves existing edits, unlike
repeating `create`, which starts independent projects from the original media.
Consider `create` instead only when the user explicitly wants independent
projects based on the original media. More Languages currently supports
**Translate & Dub projects only**; do not use this command for Translate
Subtitles, Visual Translate, Lip Sync, or another project type.

1. The target language list must be an explicit user choice, with at most **40
   unique targets per request**. Show labels and codes, and never include the
   source/current language unless requested. If the user selects more than 40,
   stop before estimation or execution, tell them that one request can process
   at most 40, and ask them to reduce or split the selection; do not silently
   start multiple requests.
2. Run the fully resolved command with `--estimate-only`. This is read-only and
   asks the backend only to return the exact `point` value. It is **not an
   execution precheck** and does not validate project status or eligibility. A
   successful estimate must never be described as precheck success or proof
   that execution will succeed. Do not calculate More Languages points locally.
3. Show a confirmation plan containing source project id, all target languages,
   prompt, glossary ids, resolved video speed adjustment/two-step translation
   settings, estimated
   project count, and the backend-returned `point` value.
4. Omitted prompt, glossary, and video speed adjustment settings inherit the
   source project. Two-step translation does **not** inherit: it defaults to off
   and is enabled only when the user explicitly requests it with
   `--proofread-before-dubbing`. Never enable it merely because the source
   project used it. The video speed adjustment flag only enables that setting,
   matching `translate_dub create`.
5. Wait for explicit confirmation, then rerun the same command once without
   `--estimate-only`. The response may include child project ids under the
   backend `result`; list/get those projects afterward rather than repeating the
   write on uncertainty.

Do not duplicate membership or project-status eligibility checks in the CLI;
the execution endpoint enforces them and the CLI surfaces its More Languages
error messages. The estimate endpoint only calculates points. When presenting
its result, explicitly tell the user that execution can still fail if the
project status or eligibility is invalid.

If execution fails with `code: 1710`, immediately run the read-only
`vozo-cli auth membership` command to fetch the current account's subscription
state. Report the returned membership and status together with the existing
1710 error message. Do not infer the user's current plan from the error alone,
and do not retry the translation automatically.

If `more-languages` returns `Project not found.`, run the read-only
`project search "<id>" --kind all` check and compare exact `items[].id` values.
If the project is found under another `kind`, or the exact-id search reports
that an unsupported kind was omitted, tell the user that the project exists but
its project type is not supported by More Languages. If the search has no exact
match and no unsupported-kind signal, report the project as not found; do not
claim an unsupported type without evidence.

If the backend reports an incompatible library Voice, hand off to the Web More
Languages dialog so the user can choose a replacement Voice; the CLI does not
guess Voice replacements.

### 3. Present plans before writes

**Never run `create` — single or batch — or execute `translate_dub more-languages` without first showing the resolved parameters and getting explicit confirmation.** The read-only `more-languages --estimate-only` point estimate is the exception: run it before confirmation so the plan contains the backend point estimate, but never treat it as an eligibility/status precheck. This applies even when the user's request already sounds fully specified (e.g. "dub this video to English"); "show the plan" means restating the exact resolved values back to the user, not just silently proceeding because you think you understood them.

Before **any** create (single item or batch), executing `translate_dub more-languages` without `--estimate-only`, or bulk download, show a plan that is concrete enough for the user to validate the exact work that is about to happen.

**Use the full checklist in `references/create-plan-checklist.md` — do not improvise a shorter summary.** Present every applicable setting with its **resolved value**, including defaults and batch-unsupported rows.

**How to show the plan (important):**

- Use **semantic, user-facing labels** (Product, Original language, Target language, Voice model, Speakers, …), not a bare dump of `--original-language`, `--target-language`, `--dub-preference`.
- Put language/product meaning first; add the CLI code in parentheses when useful — e.g. `Target language: English (en)`, `Voice model: VoiceNATIVE`.
- Prefer product names: **Translate & Dub**, **Translate Subtitles**, **Visual Translate**, **Lip Sync**.
- Still cover every setting the checklist requires — semantic wording must not drop fields.

Every setting that applies must appear with its **resolved value**, including:

- values you will pass explicitly
- settings omitted from the command but covered by a **CLI default** (write the default in plain language, e.g. `Original language: Auto-detect`, `Voice model: Auto`)
- settings **not supported** for the chosen source mode (write `not supported (batch)` instead of hiding the row)

At minimum, always include:

- product, source type, and source path / URL / folder (local vs dashboard folder)
- target language (label + code; use locale tags like `zh-HK` / `en-AU` when a region/accent is needed), original language when relevant
- dashboard folder and project title (or `none` / `auto from filename`)
- for Translate & Dub: **every** voice/subtitle/alignment setting (voice model, speakers, burn-in subtitles, remove original subs, auto-align, proofread before dubbing, prompt, glossary, custom subtitle file + usage)
- for Translate Subtitles: subtitle display mode, remove original subs, prompt, glossary, custom subtitle file
- for Visual Translate: original language, font choice
- for Lip Sync: source mode and face mode (`--face-mode` is **required**; ask if missing — do not default to single)
- whether the user wants the result **auto-downloaded when processing finishes** — offer it here once; a "yes" in the plan confirmation counts as the explicit download request required by §3.2
- for batch: estimated project count, and whether it is a single-language batch or repeated per language
- **estimated points** (for More Languages, use only the backend-returned `point`; otherwise use formulas in `references/limits.md` / checklist) plus available balance from `auth points` when known
- output / follow-up expectations (`webUrl`, whether `export` will be needed, which artifacts will be downloaded)
- when summarizing languages for users, prefer human labels (`English`, `Chinese (Hong Kong)`); keep codes for the actual create command. For create, pass locale via `--target-language` tags like `zh-HK` when a region/accent is needed
- quota warnings (points, Studio for batch, membership expiry)
- which steps are web-only (fine-tuning text, redub)

**Incomplete plans are invalid.** If you only list “target language + source file” and skip defaults the CLI will apply, the user cannot truly confirm the job. Stop and expand the plan before asking for confirmation.

Wait for explicit user confirmation before running `create` (single or batch), executing `translate_dub more-languages` without `--estimate-only`, or a bulk `download`. A one-word request ("yes" / "go" / "confirm") after you've shown the plan counts as confirmation; a request that jumps straight to naming the action without ever seeing the resolved parameters does not.

**Confirm exactly once — and "once" always means confirming the FULL plan.** The user's confirmation only counts if the message they are replying to contains the complete resolved plan (every applicable checklist row).

Two valid paths, no third:

1. **No missing required fields** → present the full plan as plain text, wait for the user's reply. Do **not** also open a confirmation popup — showing the plan in text and waiting for a reply _is_ the confirmation, and adding a popup on top is redundant double-confirmation.
2. **Missing required fields** (e.g. target language, dub vs subtitles) → use a choice prompt to collect ONLY the missing values. **This prompt is a data question, NOT a create confirmation.** After it resolves, you MUST still present the full plan in text and wait for an explicit reply before running `create`.

**Hard gate before every `create` or executable `translate_dub more-languages` call:** ask yourself — "did the user's last confirmation come as a reply to a message showing the complete plan?" If no, you do not have confirmation. This gate does not block the read-only `--estimate-only` point estimate; that estimate does not validate execution eligibility or status. Answering a language-selection popup is never authorization to create.

- ❌ Wrong: popup asks "original language? target language?" → user picks ko/ja → `create` runs immediately.
- ✅ Right: popup asks ko/ja → agent shows the full plan (source, title, font, folder, prompt/glossary, auto-download) → user replies "yes" → `create` runs.

If required fields are missing, stop before execution and list the missing fields explicitly. **Do not** start create with guessed required values.

**Clarify key requirements before planning, not after creating.** A create plan is only as good as the requirements behind it: when the user's request leaves an outcome-shaping choice open — target language, voice cloning model / accent expectation, speaker count, subtitles on/off, dub vs subtitles vs visual translate — resolve it with the user **before** showing the plan. Do not fill the gap with a default, show a technically-complete plan, and let the user rubber-stamp a project that misses what they actually wanted; a wrong key setting means points spent and the whole project redone.

### 3.1. Target language: never infer (important)

For any `create` that involves translation, dubbing, or visual translate, and for `translate_dub more-languages`, every `--target-language` must come from an **explicit user choice** before you run the command.

**When the user has not named a target language, do not:**

- Guess or default to any language code (`zh`, `en`, `ja`, `zh-CN`, etc.)
- Assume a target because the user chats in Chinese, this skill is localized, or examples in the docs use a particular language
- Infer from source media language, prior projects, `list`/`get` results, or browser/system locale
- Treat vague requests like “translate it”, “dub this”, or “add subtitles” as permission to silently pick a `--target-language`

**Do this instead:**

1. Stop before `create` and ask which target language the user wants (optionally show readable options from `vozo-cli project languages <tool>` — names + codes, not codes alone)
2. Put the resolved `--target-language` in the create plan (use a locale tag like `zh-HK` / `en-AU` when a region/accent is needed) and wait for confirmation
3. Only pass `--target-language` after the user clearly states it (e.g. “into English”, “target en”, “dub to Japanese”) or confirms a plan that names the language

`--original-language` may stay `auto` where supported — **except `visual_translate`, where it is required and must be explicitly given by the user, never guessed**. Do not infer either field from the language the user chats in. **Target language has no default—the CLI will not choose one for you.**

### 3.1.2. Dashboard folders vs local `--from-dir` (important)

Do not confuse these two “folder” concepts:

| Meaning                                         | CLI surface                                                                                | Example                                         |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| **Local directory of media files** on disk      | `create --from-dir <path>`                                                                 | Batch-upload every video in `/Users/me/videos`  |
| **Dashboard folder** in the user's Vozo account | `project folder create`, `folder list`, `folder search`, then `create --folder <folderId>` | Put new projects under a named workspace folder |

**When the user wants a new dashboard folder:**

1. If they gave a folder name, run `vozo-cli project folder create "<name>"` (or confirm the name first if it was vague).
2. Use the returned `folder.folderId` on subsequent `project <tool> create ... --folder <folderId>`.
3. If they named an existing folder instead, prefer `project folder search "<name>"` and reuse a unique match — do not create a duplicate unless they asked for a new one.

**When the user only gave a folder name for create (not an id):** resolve with `folder search` first; create only when no suitable folder exists.

### 3.1.3. Batch local files: use `--from-files` / `--from-dir` (important)

| User intent                | Use                                                  | Do **not** use                          |
| -------------------------- | ---------------------------------------------------- | --------------------------------------- |
| 2+ local video/audio files | **One** `create` with `--from-files path1 path2 ...` | Repeated `create --from-file` per file  |
| A folder of media          | **One** `create` with `--from-dir <path>`            | Listing files and looping `--from-file` |

Applies to `translate_dub`, `translate_subtitles`, `visual_translate`, and `lipsync`. Batch stdout returns **`ids[]`**. Requires **Studio+**. Does **not** support `--subtitle-file` (single-file only). `translate_dub` batch also does not pass `--speaker-number`.

### 3.1.4. Translate & Dub voice cloning model (`--dub-preference`) — surface it, don't silently default (important)

Translate & Dub has a **Voice Cloning Model** setting with three values. Users usually don't know it exists, so you must bring it up whenever it matters:

| Value    | Product name | What it does / when to pick it                                                                                                                   |
| -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `auto`   | Auto         | Automatically selects the best voice model for the content. Fine only when the user expressed **no** preference about voice, accent, or emotion. |
| `real`   | VoiceREAL    | Preserves the **emotion and accent of the original voice**. Best for expressive content: dramas, vlogs, entertainment.                           |
| `native` | VoiceNATIVE  | Delivers a more **natural target-language accent**. Best for clarity-focused content: ads, e-learning, explainers.                               |

**Agent rules:**

- If the user mentions **anything** about accent, voice feel, naturalness, or emotion (e.g. "use a native American accent", "keep the original voice's emotion", "sound like a native speaker"), do **not** leave `--dub-preference` at `auto` — map the request to `real` or `native` and put it in the create plan. A wrong model here means the whole project must be redone.
- Always show the chosen voice cloning model (including `auto`) as one of the key settings in the create plan (§3), with a one-line explanation the first time, so the user can veto it before points are spent.
- If the user's accent/voice expectation is ambiguous, ask which model they want (with the table above summarized) instead of guessing.

### 3.2. Export / download: no inference; never use playback URLs (important)

**Do not run `export` or `download` unless the user explicitly asks to export, download, or save project outputs to disk.** A user opting in to "auto-download when finished" while confirming the create plan (§3) counts as that explicit request.

When the user only asked to **create**, **check status**, **list/search**, or **get a project link**, stop after the requested step — typically share `webUrl` and current status. **Do not** assume they want files on disk because processing finished, because a scenario in this skill shows a full pipeline, or because you think a "complete" workflow should end in a download.

**Never treat preview / playback URLs as export or download URLs.** These are **not** valid substitutes for `export` + `download`:

| Invalid for saving files                                                          | Why                                                         |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `webUrl`, `open` result (`url`)                                                   | Web editor / preview page, not a media file                 |
| `videoUrl`, `video_url`, `videoSrcList`, `video_src_list` from any API JSON       | In-app playback / streaming source                          |
| `thumbUrl`, `thumb_url`, `originURL`, `origin_url`                                | Thumbnail or original upload pointer, not a finished export |
| Any HLS/m3u8 link, signed temp URL, or CDN preview link you scraped from API JSON | Playback-only; may expire; not the CLI export artifact      |

**Correct way to deliver files:**

1. User explicitly asks to export/download (name the artifact if unclear).
2. `project <tool> export <id>` when needed → poll `get` until export is ready.
3. `project <tool> download <id> --artifact <type> --output <path>`.

The `downloadUrl` returned by `export` is for the CLI `download` command to follow internally — **do not** hand it to the user as a "direct download link", and **do not** `curl`/`wget` it yourself instead of running `download`.

If the user later asks for the file, run `export` / `download` then — do not skip ahead early "just to be helpful".

Required-field reminders:

- `translate_dub`: require a source and `--target-language`
- `translate_subtitles`: require a video source and `--target-language`
- `visual_translate`: require a video source, `--target-language`, and explicit `--original-language`
- `lipsync`: require a video source (`--from-url` / `--from-file` / `--from-files` / `--from-dir`) or `--from-translation`
- If the user gives a language and support is uncertain, run `vozo-cli project languages <tool>` before create and only proceed with supported values.
- **When the user asks which languages are supported:** run `project languages <tool>`, then answer with readable names from `supportedOptions` (e.g. `English (en)`, `Chinese (Hong Kong) (zh-HK)`). Do **not** dump raw language codes alone.

After a create succeeds, **do not report how many points it consumed.** Nothing available to the CLI is the actual charge: `estimateConsumedPoints` and the `references/limits.md` formulas are _pre-create estimates_, and real billing diverges from them — a project that fails is not charged at all, and an auto-clipped run bills the clipped length. Presenting an estimate as the deduction states as fact something you did not observe.

1. **Points belong in the create plan, never in the create result.** Show the estimate _before_ the create (§3), labelled as an estimate, so the user can weigh it against their balance. Once the create returns, drop the subject.
2. **Do not restate the estimate as the cost after the fact** — not in the create summary, not in polling updates, not in the completion report. "Consumed N points" is a claim about billing; you have no billing source.
3. **Never derive consumption by diffing `auth points` before and after create.** The balance is account-wide: concurrent projects from the web app, another terminal, or a parallel batch land in the same balance, and expiry/top-ups corrupt it too. A delta is not this create's cost — in either direction.
4. Reading `auth points` is still correct for showing the **available balance** (quota warnings in the create plan, §3) — just never present it, or a delta of it, as this project's charge.
5. If the user explicitly asks what a create cost, say plainly that the CLI only has the pre-create estimate, give that number **as an estimate**, and point them to the web points/billing page for the actual charge.

### 3.3. Auto-clipping when points are insufficient (important)

For some tools, when the user is a **first-time creator** and available points are **insufficient** to process the full media duration, the CLI will automatically create a **clipped interval** (starting at 0s) so the backend can process a partial segment instead of blocking the create entirely.

Currently applies to:

- `translate_dub create`
- `visual_translate create`

When auto-clipping happens:

- The `create` stdout JSON includes:
  - `clip`: `{ originalDurationSeconds, durationSeconds, clipInterval, reason }`
  - `warnings[]`: user-facing message strings
- The CLI also prints each `warnings[]` entry to stderr for human visibility.

Agent guidance:

- Always tell the user the output covers **only the clipped interval** and state the exact seconds range.
- Include the project `webUrl`, and suggest topping up/upgrade or segmenting workflows if they need the full media processed.

### 3.5. Require double confirmation before delete

`project delete` is destructive. Never run it immediately after a user casually says “delete” — this applies identically whether it's a single project or a batch of many; batch is not a "lower ceremony" version of delete, and a single delete is not exempt just because it's only one item.

Before any delete:

1. Show the project `id` / `ids` that will be deleted.
2. State clearly that the action is destructive and cannot be undone from CLI.
3. Ask for a second explicit confirmation that is specific to the delete action.

Rules:

- Do not reuse an earlier confirmation for create / download / export as delete confirmation.
- If the scope is ambiguous, resolve the exact target list first and only then ask for delete confirmation.
- For multiple ids, echo the count and the concrete ids before executing `project delete`.

### 3.6. Multi-tool requests: confirm independent vs chained (important)

When a single user request names 2+ tools (dub, subtitles, visual translate, lipsync), there are two different execution modes and the CLI does **not** default to either — you must resolve which one before creating anything:

- **Independent mode**: each tool creates its own project **from the same original source** (`--from-url` / `--from-file` / `--from-dir`). Outputs don't affect each other; if the user wants one final file with all effects combined, they must merge on the web. This is the default assumption in `references/scenarios.md` Scenario D and is faster/cheaper (steps can run in parallel).
- **Chained mode**: each step after the first uses the **previous step's exported output** as its own source, so effects accumulate into a single output. Since `translate_dub create` / `visual_translate create` only accept `--from-url` / `--from-file` / `--from-files` / `--from-dir` (no project-id source — verified in the CLI's option list), chaining means: `export` the prior step's artifact → `download` it locally → pass that local file via `--from-file` to the next `create`. This is slower (fully sequential, no parallelism) and costs more (each step reprocesses the full output of the previous one).

**Confirmation rule:** if the user's phrasing doesn't make the mode obvious, ask explicitly before creating anything — don't silently default to either mode.

- Treat phrasing like "do X first, then use that result for Y" / "based on the dubbed output, also do..." / "chain X into Y" as chained.
- Treat phrasing like "do X and Y together" / "create separate projects" / "also want subtitles and visual translate" (goals listed together, no dependency implied) as independent — but if truly ambiguous, still ask.

**If chained, watch these details:**

- `lipsync` already has a native chain path: `--from-translation <dub-id>` pulls the dubbed audio track directly from an existing `translate_dub` project. Use that instead of the generic export/download/re-upload pattern when chaining dub → lipsync.
- For `translate_dub` → `visual_translate` (or the reverse), only one channel changed in the prior step's output: dub changes the **audio**, visual translate changes **burned-in on-screen text**. Don't blindly copy the previous step's `--target-language` into the next step's `--original-language`. Ask or infer which channel the next tool actually reads (visual translate cares about on-screen text language; dub cares about spoken audio language) and set `--original-language` to that channel's real language, not the prior step's target language.
- State the pipeline order and the per-step source in the plan (see §3) so the user can confirm before any create runs.

### 4. Display rules

- No raw JSON unless asked.
- Summaries: title, id, kind, languages (readable names), status, `webUrl`, local paths after download.
- Lists: `totalCount` is the server total and may include types CLI omits; use `items[]` + `nextCursor` (and `skippedUnsupportedCount` / `notice` when present). Paginate with `--cursor` when needed.

---

## Per-Tool Create → Download

Read `references/tools.md` for the full per-tool flag tables and download artifacts (`translate_dub`, `translate_subtitles`, `visual_translate`, `lipsync`). **Before asking the user to confirm a create, also open `references/create-plan-checklist.md` and fill every applicable row.** Always check `tools.md` before running `create` for a tool you haven't just used in this conversation, since required fields and Studio+/Creator+ gating differ per tool.

---

## Scenario Playbook

Read `references/scenarios.md` for ready-made command sequences (folder batch, multi-language, multi-step pipelines, bulk download with filters). Match the user's request to the closest scenario (A–G) instead of re-deriving the plan from scratch.

---

## Creation Limits (CLI pre-check)

Read `references/limits.md` before `create` when the media may be near a duration/size/tier cap, or when the user asks for a points estimate. It also has the points-estimate formula per tool.

---

## Confirmation Rules

| Policy                              | Commands                                                                                                                                                                          |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Read-only (run immediately)         | `list`, `search`, `folder list`, `folder search`, `<tool> get`, `<tool> open`, `translate_dub more-languages --estimate-only`                                                     |
| Confirm first                       | `folder create`, `<tool> create` (single or batch — see §3), executable `translate_dub more-languages`, `<tool> export`, `<tool> download`, bulk `download`, multi-project chains |
| Never without explicit user request | `export`, `download` — see §3.2                                                                                                                                                   |
| Confirm twice, see §3.5             | `project delete` (single id or multiple ids — same rule for both)                                                                                                                 |

---

## Failure Recovery

- `status: "upgrade_required"` (not `"failed"`): the CLI is too old for the API. Tell the user to run `vozo-cli upgrade` (or install a newer version), then retry. Do not treat this as a project/auth failure.
- `errorKind: "network"` on a failed command: connectivity/DNS/TLS/proxy issue (not auth or project failure). Report `network.code` / `message`; do **not** auto-retry — wait for the user to decide.
- `upgradeSuggestion` on a **successful** JSON result: soft recommendation only — command already succeeded. Mention a newer CLI is available when convenient; do **not** stop the workflow or treat it as an error.
- Processing: poll `get`; do not claim ready while `processing` is `true`.
- More Languages `code: 1710`: fetch the current subscription state with
  `auth membership`, report it with the existing error message, and do not
  retry automatically.
- More Languages `Project not found.`: search the exact id with `project search "<id>" --kind all`; when the result identifies another/omitted kind, tell the user that More Languages supports only Translate & Dub projects and this project type is unsupported.
- More Languages incompatible Voice: do not invent a replacement Voice id; share the source `webUrl` and ask the user to finish the replacement in the Web More Languages dialog.
- Status `proofreading` with `processing: false`: the dub is done but voices need user confirmation before export/download. Do not keep polling and do not retry `export` or `download`; share `webUrl` and ask the user to confirm the voices in the web editor.
- Download missing URL: `export` → poll `get` until `processing` is `false` → retry `download` — **only when the user already asked for a download**.
- Subtitle download empty: project may lack blocks/segments yet.
- Unsupported request: state clearly; offer web `open` or supported alternative.

## Handoff to Web

After create, always give **project link** (`webUrl`) and mention it can be opened to review and edit the result (fix translations, change voices, redub) if the user is not satisfied. For text edits, redub, or web-only lipsync audio modes:

`vozo-cli project <tool> open <id>`
