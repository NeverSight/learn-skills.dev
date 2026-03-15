---
name: topview-skill
description: "Generate, Edit, Collaborate. Access all mainstream AI models in one toolkit. Simply describe your vision to create videos, images, and avatars—zero manual operations. Use this skill whenever the user mentions: Topview, generating videos or images, talking avatars, lip-sync, text-to-speech, TTS, voice cloning, background removal, product photos on models, image-to-video, text-to-video, AI image editing, or any creative content generation workflow—even if they don't explicitly name a specific tool or say 'Topview'."
metadata:
  tags: topview, avatar, video, image, voice, ai, api, i2v, t2v, omni, text2image, image_edit, tts, voice_clone, board
  requires:
    bins: [python3]
  primaryEnv: TOPVIEW_API_KEY
---

# Topview AI Skill

> Modular Python toolkit for the [Topview AI](https://www.topview.ai) API.

✨ **Generate. Edit. Collaborate. — All in One Place.** ✨

- 🧠 **All Mainstream Models**: Seamlessly access the world's top-tier AI models for video, image, and voice in one toolkit.
- 🗣️ **Describe to Create**: Just tell the agent what you want. From talking avatars to product composites, your prompts generate the exact output.
- ⚡ **Zero Manual Ops**: No manual uploads, no tedious tweaking. Everything is automated straight to your shared board.

## What You Can Do

> You don't need to know any API details. Just describe what you want — the agent reads the technical docs below and handles everything.

**Single tasks — one sentence, one result:**

- Describe an image and get it generated in seconds — or batch-generate a whole set at once
- Upload a portrait and a script, get a talking avatar video with lip-sync
- Animate any static image into a video clip
- Generate a video purely from a text description
- Remove backgrounds, edit images, or swap scenes — all by describing what you want
- Put your product on a model with one sentence
- Clone your voice or pick from hundreds of voices for text-to-speech
- Organize everything on a web board for preview and sharing

**Combined workflows — chain capabilities freely:**

These capabilities can be mixed and matched in any combination. For example, tell the agent "create a full product launch kit from this one photo" and it will chain background removal, product showcase, avatar video, and image generation into one pipeline — all in a single conversation. Other examples:

- Generate images for each scene of a storyboard, then animate them all into video clips
- Write a script, produce TTS narration in 3 languages, create avatar videos for each
- Batch-produce a week's worth of brand-consistent social media images and videos from one style reference
- Upload a portrait + clone your voice, then generate unlimited avatar episodes from text scripts alone
- Turn an article into a multi-segment educational video series with AI illustrations and presenter narration

## Execution Rule

> **Always use the Python scripts in `scripts/`.** The scripts handle authentication, S3 file upload, automatic polling, timeout recovery, and structured error handling — bypassing them with raw `curl` or HTTP calls would lose all of this and likely fail on auth alone.

## Prerequisites

- **Python 3.8+**
- Authenticated — see [references/auth.md](references/auth.md) for login flow
- Credits available — see [references/user.md](references/user.md) to check balance
- Env vars `TOPVIEW_UID` + `TOPVIEW_API_KEY` are set automatically after login; or set manually for CI

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## Agent Workflow Rules

> **These rules apply to ALL generation modules (avatar4, video_gen, ai_image, remove_bg, product_avatar, text2voice).**

1. **Always start with `run`** — it submits the task and polls automatically until done. This is the default and correct choice in almost all situations.
2. **The agent owns the polling loop** — users expect a hands-off experience, so the agent should poll until the task completes or the timeout is reached rather than asking the user to check status manually.
3. **Reserve `query` for resuming** — `query` is only useful when `run` has already timed out and you have a `taskId` to resume, or when the user explicitly provides an existing `taskId`. Starting with `query` on a new request will fail because there's no task to poll.
4. **`query` polls continuously** — it keeps checking every `--interval` seconds until status is `success` or `fail`, or `--timeout` expires. It does not stop after one check.
5. **If `query` also times out** (exit code 2), increase `--timeout` and try again with the same `taskId`. Do not resubmit unless the task has actually failed.

```
Decision tree:
  → New request?           use `run`
  → run timed out?         use `query --task-id <id>`
  → query timed out?       use `query --task-id <id> --timeout 1200`
  → task status=fail?      resubmit with `run`
```

**Task Status:**

| Status | Description |
|--------|-------------|
| `init` | Task is queued, waiting to be processed |
| `running` | Task is actively being processed |
| `success` | Task completed successfully |
| `fail` | Task failed |

## Board ID Protocol

> **Every generation task should include a `--board-id` so results are organized and viewable on the web.**

1. **Session start** — before submitting the first task, run `board.py list --default -q` to get the default board ID ("My First Board"). Only need to do this once per session.
2. **Pass to all tasks** — add `--board-id <id>` to every generation command (`avatar4.py`, `video_gen.py`, `ai_image.py`, `product_avatar.py`, `text2voice.py`).
3. **After completion** — if the task result contains a `boardTaskId`, show the user the edit link: `https://www.topview.ai/board/{boardId}?boardResultId={boardTaskId}`. Tell the user they can view and edit the result via this link.
4. **User wants a new board** — run `board.py create --name "..."` and use the returned board ID for subsequent tasks.
5. **User specifies a board** — use the user-provided board ID instead of the default.
6. **Forgot the board ID?** — run `board.py list --default -q` again.

```
Session flow:
  1. BOARD_ID = $(board.py list --default -q)
  2. avatar4.py run --board-id $BOARD_ID ...
  3. video_gen.py run --board-id $BOARD_ID ...
  4. (result shows edit link with boardTaskId)
```

## Modules

| Module | Script | Reference | Description |
|--------|--------|-----------|-------------|
| Auth | `scripts/auth.py` | [auth.md](references/auth.md) | OAuth 2.0 Device Flow — browser login, save credentials |
| Avatar4 | `scripts/avatar4.py` | [avatar4.md](references/avatar4.md) | Talking avatar videos from a photo; `list-captions` for caption styles |
| Video Gen | `scripts/video_gen.py` | [video_gen.md](references/video_gen.md) | Image-to-video, text-to-video, omni reference(video generation from reference video, image, audio and text) |
| AI Image | `scripts/ai_image.py` | [ai_image.md](references/ai_image.md) | Text-to-image and AI image editing (10+ models) |
| Remove BG | `scripts/remove_bg.py` | [remove_bg.md](references/remove_bg.md) | Remove image background — step 1 of Product Avatar flow |
| Product Avatar | `scripts/product_avatar.py` | [product_avatar.md](references/product_avatar.md) | Model showcase product image; `list-avatars`/`list-categories` for template browsing |
| Text2Voice | `scripts/text2voice.py` | [text2voice.md](references/text2voice.md) | Text-to-speech audio generation |
| Voice | `scripts/voice.py` | [voice.md](references/voice.md) | Voice list/search, voice cloning, delete custom voices |
| Board | `scripts/board.py` | [board.md](references/board.md) | Board management — organize results, view/edit on web |
| User | `scripts/user.py` | [user.md](references/user.md) | Credit balance and usage history |

> **Read individual reference docs for usage, options, and code examples.**
> Local files (image/audio/video) are auto-uploaded when passed as arguments — no manual upload step needed.

---

## Creative Guide

> **Core Principle:** Start from the user's intent, not from the API.
> Analyze what the user wants to achieve, then pick the right tool, model, and parameters.

### Step 1 — Intent Analysis

Every time a user requests content, identify:

| Dimension | Ask Yourself | Fallback |
|-----------|-------------|----------|
| **Output Type** | Image? Video? Audio? Composite? | Must ask |
| **Purpose** | Marketing? Education? Social media? Personal? | General social media |
| **Source Material** | What does the user have? What's missing? | Must ask |
| **Style / Tone** | Professional? Casual? Playful? Authoritative? | Professional & friendly |
| **Duration** | How long should the output be? | 5–15s for clips, 30–60s for avatar |
| **Language** | What language? Need captions? | Match user's language |
| **Channel** | Where will it be published? | General purpose |

### Step 2 — Tool Selection

```
What does the user need?
│
├─ A person speaking to camera (talking head)?
│  → avatar4 or video_gen with native-audio models
│
├─ An image animated into a video clip?
│  → video_gen --type i2v
│
├─ A video generated purely from text?
│  → video_gen --type t2v
│
├─ A new video based on reference materials (style transfer, editing)?
│  → video_gen --type omni
│
├─ An image generated from a text prompt?
│  → ai_image --type text2image
│
├─ An existing image edited / modified with AI?
│  → ai_image --type image_edit
│
├─ Remove background from an image (e.g. product cutout)?
│  → remove_bg
│
├─ A product placed into a model/avatar scene?
│  → product_avatar (use remove_bg first if product has background)
│  → product_avatar list-avatars to browse public templates
│
├─ Browse available caption styles for avatar videos?
│  → avatar4 list-captions
│
├─ Text converted to speech audio?
│  → text2voice
│
├─ Need to find a voice / list available voices?
│  → voice list
│
├─ Clone a custom voice from audio sample?
│  → voice clone
│
├─ Delete a custom voice?
│  → voice delete
│
├─ Manage boards / view results on web?
│  → board (list, create, detail, tasks)
│
├─ A combination (e.g., talking head + product clips)?
│  → Use a recipe (see Step 3)
│
└─ Outside current capabilities?
   → See Capability Boundaries below
```

**Quick-reference routing table:**

| User says... | Script & Type |
|----------------------------------------------|-------------|
| "Make a talking avatar video with this photo and text" | `avatar4.py` (pass local image path directly) |
| "Generate a video with this photo and my audio recording" | `avatar4.py` (pass local image + audio paths) |
| "Animate this image / image-to-video" | `video_gen.py --type i2v` (pass local image path) |
| "Generate a video about..." | `video_gen.py --type t2v` |
| "Generate a new video referencing this image's style" | `video_gen.py --type omni` |
| "Generate an image / text-to-image" | `ai_image.py --type text2image` |
| "Modify this image / change background" | `ai_image.py --type image_edit` |
| "Remove image background / cutout" | `remove_bg.py` |
| "Put this product on a model image" | `product_avatar.py` (use `remove_bg.py` first if product has background) |
| "What product avatar/model templates are available?" | `product_avatar.py list-avatars` |
| "What caption styles are available?" | `avatar4.py list-captions` |
| "Convert this text to speech / audio" | `text2voice.py` |
| "What voices are available? / Find a female voice" | `voice.py list --gender female` |
| "Clone a voice from this audio recording" | `voice.py clone --audio <file>` |
| "Delete this custom voice" | `voice.py delete --voice-id <id>` |
| "View my board / check what was generated" | `board.py list` or `board.py tasks --board-id <id>` |
| "Create a new board" | `board.py create --name "..."` |
| "Check how many credits I have left" | `user.py credit` |

> **Video model selection** — see [references/video_gen.md](references/video_gen.md) § Model Recommendation.

> **Image model tip:** For all image tasks, default to **Nano Banana 2** — strongest all-round model with best quality, 14 aspect ratios, up to 4K, and 14 reference images for editing. See [references/ai_image.md](references/ai_image.md) § Model Recommendation.

> **Product Avatar workflow:** For best results, use the 2-step flow: `remove_bg.py` to get a `bgRemovedImageFileId`, then `product_avatar.py` with `--product-image-no-bg`. Use `product_avatar.py list-avatars` to browse public templates and get an `avatarId`. See [references/product_avatar.md](references/product_avatar.md) § Full Workflow.

> **Caption styles for avatar4:** Use `avatar4.py list-captions` to discover available caption styles, then pass the `captionId` via `--caption`.

> **Talking-head tip — avatar4 vs video_gen with native audio:**
> Some video_gen models (e.g. Standard, Kling V3, Veo 3.1) support native audio and can produce talking-head videos with **better visual quality** than avatar4. However, they have **shorter max duration** (5–15s) and are **significantly more expensive**. Avatar4 supports up to 120s per segment at much lower cost.
> **Rule of thumb:** Target video duration less than 15s, default to video_gen native-audio models; otherwise, default to avatar4. But you should always ask the user for their preference with pros and cons analysis.

### Step 3 — Simple vs Complex

**Simple requests** — the user's need is clear, materials are ready → handle directly from the reference docs.

**Complex requests** — the user gives a *goal* (e.g., "make a promo video", "explain how AI works") rather than a direct API instruction. Follow this universal workflow:

1. **Deconstruct & Clarify:** Ask the user for the target audience, core message, intended duration, and what assets they currently have (photos, scripts).
2. **Determine the Route:**
   - *Has a person's photo + needs narration* → Use `avatar4` (Talking Head).
   - *Has a product/reference photo* → Use `video_gen --type i2v` or `omni`.
   - *No assets, purely visual concept* → Use `video_gen --type t2v`.
   - *Requires both* → Plan a Hybrid approach (Avatar narration + B-roll inserts).
3. **Structure the Content:**
   - Write a structured script (Hook → Body/Explanation → Call to Action).
   - Add `<break time="0.5s"/>` tags to TTS scripts for natural pacing.
   - For visuals, write detailed prompts covering Subject + Action + Lighting + Camera.
4. **Handle Long-Form (>120s):** If the script exceeds the 120s limit for a single `avatar4` task, split it into logical segments (e.g., 60s each) at natural sentence boundaries. Submit tasks in parallel using the `submit` command, ensure parameters (voice/model) remain locked across segments, and deliver them in order.

---

## Pre-Execution Protocol

> Follow this before EVERY generation task.

1. **Estimate cost** — use `video_gen.py estimate-cost` for video tasks, `ai_image.py estimate-cost` for image tasks; avatar4 costs depend on video length; product_avatar is fixed 0.5 credits; text2voice is fixed 0.1 credits
2. **Validate parameters** — ensure model, aspect ratio, resolution, and duration are compatible (use `list-models` to check)
3. **Ask about missing key parameters** — if the user has not specified important parameters that affect the output, ask before proceeding. Key parameters by module:
   - **video_gen**: duration, aspect ratio, model
   - **ai_image**: aspect ratio, resolution, model, number of images
   - **avatar4**: (usually determined by input, but confirm voice if not specified)
   - **text2voice**: voice selection
   - These parameters significantly affect output quality and credit cost, so confirming with the user avoids wasted credits and disappointing results.
4. **Confirm before first submission** — before the first generation task in a session, present the plan (tool, model, parameters, cost estimate) and ask in one message: (a) proceed? (b) confirm each future task, or auto-proceed for the rest of the session? If the user said "just do it" upfront, treat as auto-proceed. Even in auto-proceed mode, still ask about missing key parameters.

## Agent Behavior Protocol

### During Execution

1. **Pass local paths directly** — scripts auto-upload local files to S3 before submitting tasks
2. **Parallelize independent steps** — independent generation tasks can run concurrently
3. **Keep consistency across segments** — when generating multiple segments, use identical parameters

### After Execution

1. **Report cost** — tell the user how many credits were consumed (from `costCredit` in response)
2. **Show results clearly** — provide download URLs, duration, resolution; number multiple outputs
3. **Show edit link** — if the result includes a `boardTaskId`, show `https://www.topview.ai/board/{boardId}?boardResultId={boardTaskId}` and tell the user they can view/edit there
4. **Offer iteration** — if the result isn't satisfactory, suggest adjustments; remind that regenerating consumes additional credits

### Error Handling

See [references/error_handling.md](references/error_handling.md) for error codes, task-level failures, and recovery decision tree.

---

## Capability Boundaries

| Capability | Status | Script |
|---------------------------------|--------------|----------------------------------------------------------|
| Photo avatar / talking head | Available | `scripts/avatar4.py` |
| Caption styles | Available | `scripts/avatar4.py list-captions` |
| Credit management | Available | `scripts/user.py` |
| Image-to-video (i2v) | Available | `scripts/video_gen.py --type i2v` |
| Text-to-video (t2v) | Available | `scripts/video_gen.py --type t2v` |
| Omni reference video | Available | `scripts/video_gen.py --type omni` |
| Text-to-image | Available | `scripts/ai_image.py --type text2image` |
| Image editing | Available | `scripts/ai_image.py --type image_edit` |
| Remove background | Available | `scripts/remove_bg.py` |
| Product avatar / image replace | Available | `scripts/product_avatar.py` |
| Product avatar templates | Available | `scripts/product_avatar.py list-avatars` / `list-categories` |
| Text-to-speech (TTS) | Available | `scripts/text2voice.py` |
| Voice list / search | Available | `scripts/voice.py list` |
| Voice cloning | Available | `scripts/voice.py clone` |
| Delete custom voice | Available | `scripts/voice.py delete` |
| Board management | Available | `scripts/board.py` |
| Board task browsing | Available | `scripts/board.py tasks` / `task-detail` |
| Marketing video (m2v) | No module | Suggest [topview.ai](https://www.topview.ai) web UI |

> Promising a capability that doesn't have a corresponding module will lead to a dead end mid-workflow and erode user trust. If a request falls outside the table above, suggest the [Topview web UI](https://www.topview.ai) instead.
