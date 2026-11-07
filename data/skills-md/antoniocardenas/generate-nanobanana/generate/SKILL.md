---
name: generate
description: Generate images and videos using Google's Gemini media models (Nano Banana 2 Lite, Nano Banana 2, Nano Banana Pro, Gemini Omni Flash) via the Gemini API. Use this whenever the user asks to generate, create, or make an image or video, wants a thumbnail, wants to animate a still image, says "generate on brand" or "generate from reference", wants to link or import a folder of reference images, invokes /generate or /generate frf, or asks to update this skill ("/generate update") — even if they don't name a specific model, and even if they just describe a visual they want without saying "generate."
---

# /generate

Calls Google's Gemini media models directly through the Gemini API — no third-party routing layer. One key, one bill, and access to the newest Google-specific features (Nano Banana Pro's multi-image fusion, Omni Flash's synced audio) as soon as they ship.

## How a generation flows

1. **Route** — pick the model for the job (draft image, standard image, quality image, or video) and read its recipe file before calling anything. Recipes hold the exact request shape and any quirks that have shown up since the model shipped.
2. **Load references** — pull any real reference images (logos, faces, style shots) from `generations/refs/`, or from a named reference set if the request invokes `/generate frf` or says "from reference" or "on brand" (see Reference library). Never substitute a text description for a reference image that exists.
3. **Generate** — call the API per the recipe, through the **Interactions API** (`client.interactions.create`) — the current, documented entry point for every model below. Images reply synchronously; video is a submit-then-poll operation for large outputs. Save the result flat into the generations folder.
4. **Log** — verify the generated file is actually on disk and non-empty, then write the sidecar JSON next to it (see Logging). Never log a generation whose file isn't there.

## Models

| Task | Model | Model ID | Recipe |
|---|---|---|---|
| Image (draft) | Nano Banana 2 Lite | `gemini-3.1-flash-lite-image` | `models/nano-banana-2-lite.md` |
| Image (standard) | Nano Banana 2 | `gemini-3.1-flash-image` | `models/nano-banana-2.md` |
| Image (quality) | Nano Banana Pro | `gemini-3-pro-image` | `models/nano-banana-pro.md` |
| Video | Gemini Omni Flash | `gemini-omni-flash-preview` | `models/gemini-omni-flash.md` |

`gemini-3-pro-image-preview` was deprecated 2026-05-28 and shut down 2026-06-25 — `gemini-3-pro-image` is its GA replacement. Model IDs move on Google's schedule, not this skill's; always read the recipe file rather than trusting this table from memory.

Rough costs, Standard (sync) tier as of August 2026 — re-check https://ai.google.dev/gemini-api/docs/pricing before quoting, these move:

| Job | Ballpark |
|---|---|
| Draft image (Lite) | ~$0.03 (1K) |
| Standard image (Nano Banana 2) | $0.05-0.15 (0.5K-4K) |
| Quality image (Pro) | $0.13-0.24 (1K/2K-4K) |
| Video, per second | ~$0.10 (720p) — quote from docs, this is what the approval gate is for |

Every row above is billable — image generation is not free just because it's cheap. Quote current pricing and get explicit approval before any of them, not only video (see Rules).


## Reference library

Loose files in `generations/refs/` (workspace-relative, like all output — see Output) work as always. On top of that, a folder one level down is a **named reference set** — the images for one brand, product, or recurring character, grouped so the user can pull them all in with one phrase.

A user registers a folder in one of two ways:

- **Import (copy)** — "import ~/company/brand-assets as brand": copy the image files into `generations/refs/brand/`. A snapshot — it survives the original folder being moved or edited.
- **Link (live)** — "link ~/company/brand-assets as brand": don't copy anything; record the path in `generations/refs/sets.json`. The folder is read fresh at generation time, so new assets show up without re-importing.

`sets.json` maps set names to linked folders:

```json
{
  "brand": {
    "path": "~/company/brand-assets",
    "output": "public/images",
    "linked": "2026-08-01T10:00:00Z",
    "notes": "logo_dark.png is the primary mark; palette.png shows brand colors"
  }
}
```

`output` is optional — see "Where the output lands" below. Imported sets can carry the same settings in a `set.json` inside their folder.

If the user doesn't name the set, default to the folder's own name. To resolve a set name at generation time, check `generations/refs/<name>/` first, then `sets.json`. If a linked path no longer exists, stop and ask — same rule as any missing reference, never approximate. After registering a set, list back the images found so the user can confirm the right folder came in.

**Bootstrap — the set doesn't exist yet.** When a ref-based request names a set that isn't there (including the very first "on brand"), create the folder (`generations/refs/<name>/`), tell the user its full path and that images dropped there will be used as references from now on, and stop. Never generate from an empty set — "on brand" with zero real brand pixels is exactly the text-description approximation the Rules forbid. Once the folder has at least one image, generation proceeds normally.

### Generating from a set

- **`/generate frf <set> …`** — use that set's images as the reference inputs for the generation. The spoken form "generate from reference `<set>` …" works the same, and a raw folder path in place of a set name is fine too — treat it as a one-off set. Always prefixed with `/generate` — a skill registers exactly one slash command, taken from the name of the folder it's installed into (`generate`, not this file's `name:` frontmatter — see Supported Environments & Agents), so a bare `/frf` is rejected as an unknown command on agents like Claude Code that route slash commands strictly.
- **"generate on brand …"** — shorthand for `/generate frf brand`. If no set named `brand` exists yet, ask the user for a folder to link or import before generating anything.

**Where the output lands.** By default, ref-based generations save flat into the workspace's `generations/` folder like everything else. A set can override that with an `output` folder — set it in `sets.json`, or just say "save these to public/images" — and then the generated file and its sidecar land there instead, ready to use in the project. Outputs never save into the refs folder itself: references in, results out, the two never mix.

Don't dump the whole folder into every call. Pick the images relevant to the job — the logo for a logo placement, style shots for a look, the product photos for that product — up to the model's reference limit: 1-2 on Nano Banana 2 Lite, a handful on Nano Banana 2, up to 14 on Nano Banana Pro. If the set holds more relevant images than a Lite draft can take, use the strongest 1-2 for drafting and the fuller set on the final rerun. Always tell the user which files went into the call; the sidecar log records them regardless.

## Determinism & coherence

Two different jobs hide under "make it again": re-running one image, and keeping a family of images looking related. Neither the image models nor Gemini Omni Flash document a `seed` parameter on the Interactions API — there is no reproducibility contract to lean on, and no sidecar field promises one. Don't tell a user a rerun will reproduce a prior result; be straight that every call is non-deterministic, and lean on the levers below instead.

**Iterate by delta.** For "same image but change X": read the original's sidecar, reuse its exact prompt and reference images, and edit only the words that describe X. Hold model, `image_size`, and `aspect_ratio` fixed too — changing any of them re-rolls the composition. Never reconstruct the prompt from memory when the sidecar holds the exact original — that's the whole reason it's logged.

**Chain edits statefully instead of re-rolling.** The Interactions API supports `previous_interaction_id` for turning one interaction into an edit of the last, rather than a fresh generation — documented for Gemini Omni Flash (see its recipe for the exact shape); re-verify against the current docs before assuming the same holds for the image models. Log the response `id` in every sidecar so a later edit can chain onto it.

**Promoting a draft doesn't carry anything forward automatically.** Promoting a picked Lite draft to Nano Banana 2 or Pro re-rolls the composition from the prompt alone. The coherence lever there is the draft itself: pass the picked draft image as a reference alongside the original prompt, so the final is anchored to approved pixels rather than to a fresh roll of the same words.

**Style anchors for sets.** A reference set may carry a `style.md` — in `generations/refs/<name>/` for imported sets, in the linked folder for linked sets — holding a short, fixed description of the set's look: palette, lighting, camera, rendering style. When present, prepend its contents to the prompt **verbatim** on every generation from that set. Don't paraphrase it; the whole point is that the same words hit the model every time. The sidecar's `prompt` field records the full assembled prompt, style block included. (`style.md` is a text anchor, never a reference image — don't try to send it as one.)

**Series lock.** For a run of images that must match each other — a character across scenes, a product line, episode covers — generate the first, get the user's approval on it, then pass that approved image as a reference into every subsequent call, on top of the set's refs and style block. Character-consistency series belong on Nano Banana Pro.

## Supported Environments & Agents

This skill works across multiple AI agents and CLI tools:
- **Antigravity**: Supports direct Python API execution with `GEMINI_API_KEY` or native `generate_image` tool fallback for instant zero-key image previews.
- **Antigravity CLI**: Invoke via the `agy` binary (e.g. `agy generate`). Migrating from the retired Gemini CLI? Import your existing config/extensions with `agy plugin import gemini`.
- **Claude Code**: Skills load from `~/.claude/skills/<name>/` (global) or `.claude/skills/<name>/` (project-local, checked in every parent directory up to the repo root) — never from `.agents/skills`, which is a different tool's path even though Claude Code's skill format follows the same open standard. The slash command Claude Code registers is the **install folder's name**, not this file's `name:` frontmatter (which is only a display label) — that's why both the install steps below and the `skills` CLI name the folder `generate`; renaming it renames the command too. Sub-commands like `frf` or `update` aren't separately registered, so always type them as arguments to `/generate` (`/generate frf <set> …`, `/generate update`) or as plain language; a bare `/frf` returns "Unknown command." Editing or adding skills inside an already-loaded `skills/` directory takes effect immediately, mid-session — a restart is only needed the first time that top-level `skills/` directory itself is created.
- **Cursor, Codex, OpenCode**: Compatible with any agent reading standard `SKILL.md` definitions in their own skills directory convention.

## Installation

Install using the skills CLI:

```bash
npx skills add AntonioCardenas/generate-nanobanana
```

Or manually clone into your agent's skills directory:

```bash
git clone https://github.com/AntonioCardenas/generate-nanobanana ~/.claude/skills/generate
```

## Updating

"/generate update" — or any ask to update this skill — refreshes the installed copy in place:

1. **Find the install** — the folder this `SKILL.md` was loaded from.
2. **Refresh it** — if the folder is a git clone (has `.git`), run `git pull` inside it. Otherwise re-run `npx skills add AntonioCardenas/generate-nanobanana`, which re-resolves to the latest and overwrites the install; if that's unavailable, clone the repo to a temp folder and copy `SKILL.md`, `models/`, and the READMEs over the installed files.
3. **Report what changed** — summarize the recent commit titles or the diff of `SKILL.md` and `models/`, so the user knows what they just got.
4. **Restart to load it** — the running session keeps the old version; tell the user to restart, same as after a fresh install.

An update touches only the skill's own files. Never touch the workspace's `generations/` folder, reference sets, or `sets.json` — that's the user's data, not the skill's.

## Authentication

Calls use a Google AI Studio key in the `GEMINI_API_KEY` environment variable. Check for it in this order:

1. **Already exported** — if the shell environment already has `GEMINI_API_KEY`, use it as-is.
2. **A `.env` file at the workspace root** — not the skill's own install folder, the root of the project being generated into. If the user has already set one up (`GEMINI_API_KEY=...` in it) and it's not yet exported, load it before the Python call — e.g. `set -a; source .env; set +a` — so the `google-genai` SDK's `genai.Client()` can pick it up from the environment.
3. **Neither exists** — stop and ask the user to set it up themselves: either `export GEMINI_API_KEY=your_key_here` (add it to their shell profile to survive new sessions), or a `.env` file at the workspace root with `GEMINI_API_KEY=your_key_here`. Setting up the key — including any `.env` file, `.env.example` template, or `.gitignore` entry — is the user's own responsibility; this skill only ever reads `GEMINI_API_KEY` once it's there, and never creates or edits those files itself.
- In **Antigravity**: If `GEMINI_API_KEY` is not present, you can seamlessly fall back to Antigravity's built-in `generate_image` tool for instant generation.

The recipes in `models/` call the `google-genai` Python SDK directly. In agents that run this through a shell rather than a native Python tool (Claude Code, Codex, OpenCode, Cursor), check it's importable before the first call (`python3 -c "import google.genai"`). If it's missing, tell the user you're about to install Google's official `google-genai` package from PyPI, then run `pip install google-genai` — never silently, and never any other package on this skill's own initiative.

## Output

- Save every file flat into the workspace's `generations/` folder — at the root of the project the session is working in, created on first use — no subfolders. The user's images live next to the code that needs them, not off in the home directory. Reference images live in `generations/refs/`, where set folders one level down (and `sets.json`) are the only structure allowed.
- No workspace to root in (a session running loose outside any project)? Fall back to `~/generations` so files still have one predictable home.
- Exception: a reference set with an `output` folder configured saves its generations — sidecars included — to that folder instead (e.g. straight into a project's `public/images/`). Never into the refs folder.
- Naming: `{project}_{description}_{timestamp}.{ext}`
- One flat folder means any future tool — a gallery page, a script, a plain search — can read the whole library with zero setup. Keep it that way rather than organizing into subfolders later. The flat rule is for outputs; the refs library is the one place with structure.

## Rules

**Quote cost and wait for explicit go-ahead before any paid generation — image or video.** Every call in this skill spends real money against the user's Google AI Studio billing, not just video. A quote alone isn't approval, and one approval covers exactly one run. If a rerun is needed, quote and confirm again.

**Draft on Nano Banana 2 Lite first; rerun the picked favorite on Nano Banana 2 or Pro.** This mirrors how the models are priced — Lite for iteration, Nano Banana 2 for most finals, Pro only when the job needs its extras: heavy multi-image fusion, consistent characters across a series, or dense on-image text.

**Never describe a face or logo in a text prompt — pass the real image as a reference instead.** Descriptions of specific people or brand marks drift from the source almost every time. If the reference file is missing, stop and ask rather than approximating.

**Don't promise reproducibility that no model here supports.** No seed or determinism contract is documented on the Interactions API. When varying an existing image, start from its sidecar's exact prompt and references and change only the requested delta — see Determinism & coherence.

**Run generations one at a time, not in parallel.** Keeps rate limits and cost/approval tracking accurate — a batch of parallel video calls could blow past an approved budget before anyone notices.

**Save, verify, then log — in that order.** The generated file must be on disk and non-empty before the sidecar is written; the sidecar is the record that an image exists, so a sidecar without its image is a false log entry. If the API returned no image — only text, an error, a safety block — there is nothing to log: report the failure and the API's text to the user instead of writing anything.

## Logging

After saving a generated file — and verifying it's on disk, per the Rules — write a matching `.json` sidecar with the same base filename next to it (e.g. `hero_thumbnail_1774912000.json` beside `hero_thumbnail_1774912000.png`). `model` is the exact model ID sent to the API (`gemini-3.1-flash-lite-image`), never the recipe's nickname (`nano-banana-2-lite`) — the sidecar is what makes a rerun possible, and a rerun needs the real ID:

```json
{
  "model": "gemini-3.1-flash-lite-image",
  "prompt": "the exact prompt sent",
  "reference_images": ["generations/refs/brand/logo_dark.png"],
  "reference_set": "brand",
  "response_id": "v1_...",
  "params": { "aspect_ratio": "16:9", "image_size": "1K" },
  "cost": "$0.04",
  "created": "2026-07-31T14:20:00Z",
  "approved_by_user": true
}
```

`response_id` is what makes "same image but change X" and stateful edits (`previous_interaction_id`) possible weeks later — log it on every call, image or video. `reference_set` names the set the images came from — omit it when references were passed individually. For linked sets, list the resolved absolute paths in `reference_images` so the log stays accurate even if the link later changes.

This gives a full audit trail — what was generated, from what prompt, at what cost — without reconstructing it from memory weeks later.

## Security

This is the skill's full capability footprint — never expand it on your own initiative:

- **Network** — HTTPS calls to Google's `generativelanguage.googleapis.com` only, per the recipes in `models/`. No other endpoint, ever.
- **Secrets** — `GEMINI_API_KEY` is only ever read (from the environment or a workspace `.env` the user already set up — see Authentication), never written. Never log it, print it, or put it in a sidecar, a prompt, or a committed file. This skill never creates or edits `.env`, `.env.example`, or `.gitignore` — that setup is the user's own responsibility.
- **File writes** — confined to the workspace: `generations/` and `generations/refs/` (including `sets.json`). Nothing outside the current project, and nothing related to key setup.
- **Package installs** — the official `google-genai` PyPI package, and only when it's missing (see Authentication). No other package, and never silently.

A skills marketplace's automated audit flagging this skill as medium risk is consistent with this list, not a sign of something hidden — a real API key, a real network call, and a conditional package install are exactly what a "call an external paid API" skill looks like to a scanner that can't see intent. If a change would add a new endpoint, a new install, or a write outside this list, treat that as a design decision for the user to approve, not something to do quietly.
