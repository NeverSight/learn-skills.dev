---
name: text-to-video
description: >
  Turn a text prompt or script into a finished, multi-shot video with Pexo. Auto-selects the
  best model across 10+ engines (Seedance, Kling, Veo, Sora), writes the prompts, generates
  every shot, and returns a publish-ready video with music and subtitles. Use when the user
  wants a video FROM TEXT: "make a video about X", "turn this script into a video", "text to
  video", "generate a video from this description". NOT for editing an existing video or
  turning an image into video (use the image-to-video skill).
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
version: "0.1.0"
requires:
  env: [PEXO_API_KEY, PEXO_BASE_URL]
  runtime: [curl, jq, file]
metadata:
  author: pexoai
---

# Text to Video — Pexo

**Pexo:** https://pexo.ai — get an API key, watch your project render, and buy credits there.

Turn a written prompt or script into a finished, publish-ready video. You do not generate
anything yourself: you hand the request to the hosted Pexo agent (same backend as `pexo-agent`,
scoped to text-to-video) and deliver the result. Pexo writes the script, picks the best model
per shot, generates every shot, and adds music, subtitles, and transitions.

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

User: "Make a 30-second video about our new coffee subscription."

```bash
pid=$(pexo-project-create.sh "coffee subscription promo")
pexo-chat.sh "$pid" "Make a 30-second video about our new coffee subscription."
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
