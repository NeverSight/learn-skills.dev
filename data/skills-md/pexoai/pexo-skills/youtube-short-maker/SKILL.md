---
name: youtube-short-maker
description: >
  Make YouTube Shorts that hold attention with Pexo — vertical 9:16, fast-paced, hook in the first
  3 seconds. Describe your topic and Pexo writes the script, generates the shots, picks the models,
  and assembles a finished Short with music and captions. Use for YouTube Shorts: "youtube short",
  "make a youtube short", "shorts video", "short-form video". NOT for long-form or landscape
  video.
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
version: "0.1.0"
requires:
  env: [PEXO_API_KEY, PEXO_BASE_URL]
  runtime: [curl, jq, file]
metadata:
  author: pexoai
---

# YouTube Short Maker — Pexo

**Pexo:** https://pexo.ai — get an API key, watch your project render, and buy credits there.

Make a finished YouTube Short built to retain — vertical and hook-first. You pass the user's
topic to the hosted Pexo agent and deliver the result; Pexo scripts it, generates the shots, and
assembles the Short with music and captions.

## Your role: relay, don't create

Create a project, send the user's request **verbatim**, poll, deliver. Pexo's backend handles
all creative work — scriptwriting, model choice, prompts, music. Adding your own direction
(duration, style, models the user didn't ask for) overrides its judgment and produces worse
videos.

## Config

`~/.pexo/config`:
```
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
```
**No account / first run →** read `references/SETUP-CHECKLIST.md` and walk the user through it — it carries the signup flow with the **invite code that grants new users bonus credits**, plus how to create the config above. **Config error →** run `scripts/pexo-doctor.sh` and follow its output.

## Workflow

Scripts live in this skill's `scripts/`. Reply to the user in their language.

1. **Create a project:** `pexo-project-create.sh "<short brief>"` → save the `project_id`.
2. **Upload any files** the user gave: `pexo-upload.sh <project_id> <path>` → save `asset_id`,
   reference it inline as `<original-image>asset_id</original-image>` (or `<original-video>` /
   `<original-audio>`). Tags are required — a bare `asset_id` is ignored. Pexo can't crawl URLs —
   download, then upload.
3. **Send the request:** `pexo-chat.sh <project_id> "<user's exact words> <asset tags>"`.
   Copy the user's words exactly; only add asset tags.
4. **Tell the user** (their language): submitted ✓ · ~15–20 min · `https://pexo.ai/project/<project_id>`.
5. **Poll:** every ≥60s run `pexo-project-get.sh <project_id>` and act on `nextAction`:
   - **WAIT** → keep polling; every ~5 polls send a one-line update with the project link.
   - **RESPOND** → handle each event in `recentMessages`: relay Pexo's text (wait for the
     user's answer if it asked, then `pexo-chat.sh` their reply); for `preview_video`, run
     `pexo-asset-get.sh <project_id> <assetId>` per option, show the URLs (A/B/C), let the user
     pick, then `pexo-chat.sh <project_id> "<choice>" --choice <assetId>`; for a `document`
     event, mention it to the user.
   - **DELIVER** → `pexo-asset-get.sh <project_id> <final assetId>`, then send the user the
     **full** asset URL as plain text — all `?…` query params, never truncated or wrapped in
     markdown — plus the project link.
   - **FAILED** → explain `nextActionHint` in plain terms and offer to retry.
   - **RECONNECT** → `pexo-chat.sh <project_id> "continue"`, tell the user the connection
     dropped and you're resuming, then keep polling.
   - Never call `pexo-chat.sh` during WAIT — it triggers duplicate production.
   - **Taking too long** → if it's been >30 min and still WAIT, tell the user (with the project
     link + `https://pexo.ai/connect/openclaw`) it's running long; ask whether to keep waiting or
     stop. Don't poll forever.

## Revisions

After delivery, the user's tweaks ("make it shorter", "new music", "different shot") reuse the
**same** project: `pexo-chat.sh <project_id> "<their feedback>"`, then poll again (step 5). Never
create a new project for a revision — it throws away Pexo's server-side context.

## Credits

If a script fails with "Credits balance" / "Insufficient credits": if the error carries a
purchase link, pass it to the user; otherwise tell them to add credits at `https://pexo.ai/home`
→ Credits → Buy Credits. Retry after they confirm.

## Example

User: "Make a YouTube Short on 3 quick tips for better sleep."

```bash
pid=$(pexo-project-create.sh "better sleep tips short")
pexo-chat.sh "$pid" "Make a YouTube Short on 3 quick tips for better sleep."
# Tell the user: submitted, ~15–20 min, https://pexo.ai/project/$pid
# Poll pexo-project-get.sh "$pid" until nextAction is DELIVER, then deliver the asset URL.
```

## Scripts

| Script | Usage | Returns |
|---|---|---|
| `pexo-project-create.sh` | `"<brief>"` | `project_id` |
| `pexo-upload.sh` | `<project_id> <file>` | `asset_id` |
| `pexo-chat.sh` | `<project_id> "<message>" [--choice <id>]` | ack (async) |
| `pexo-project-get.sh` | `<project_id>` | JSON: `nextAction`, `recentMessages` |
| `pexo-asset-get.sh` | `<project_id> <asset_id>` | JSON with `url` |
| `pexo-doctor.sh` | — | setup diagnostic |

Error codes and edge cases → `references/TROUBLESHOOTING.md`.
