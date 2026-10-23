---
name: higgsfield-to-social
description: "Generate an image or video with the Higgsfield CLI (Seedance, Kling, Veo, Nano Banana, GPT Image, Soul, Marketing Studio ads) and publish or schedule it to TikTok, Instagram, YouTube Shorts, LinkedIn, Facebook, X, Threads, Pinterest, Bluesky and more through Upload-Post, with optional Virality Predictor scoring before it goes out. Use when the user wants to create AI content and post it, says 'generate and post', 'make a reel/short/TikTok with Higgsfield', 'publish my Higgsfield video', 'schedule this generation', or chains Higgsfield output into social media. NOT for: generation alone with no publishing (use the Higgsfield skills), or publishing media that already exists (use upload-post)."
license: MIT
compatibility: "Requires the Higgsfield CLI (`higgsfield`, logged in with `higgsfield auth login`) and either the Upload-Post MCP connector or curl plus UPLOAD_POST_API_KEY. Nothing is downloaded locally: Higgsfield returns a public CDN URL and Upload-Post fetches it server side."
allowed-tools: Read, Write, Bash(higgsfield:*), Bash(curl:*), Bash(jq:*)
version: "1.0.0"
author: Upload-Post <support@upload-post.com>
tags:
- higgsfield
- ai-video
- ai-image
- social-media
- publishing
metadata: {"openclaw":{"emoji":"🎬","homepage":"https://upload-post.com","requires":{"bins":["higgsfield"],"env":["UPLOAD_POST_API_KEY"]},"primaryEnv":"UPLOAD_POST_API_KEY"}}
---

# Higgsfield to Social

Generate with Higgsfield, publish with Upload-Post. One prompt becomes a post on every
platform the user has connected, labelled as AI-generated where the platform supports it.

## Overview

1. Find out where the post is going (profile and platforms), because that decides the format.
2. Generate with `higgsfield generate create ... --wait` in the right aspect ratio.
3. Optionally score a video with Higgsfield's Virality Predictor.
4. Show the result and the caption, and get an explicit yes.
5. Publish the result URL with Upload-Post and report the link of each post.

Nothing is published without the user's approval of the final media and caption.

## Prerequisites

- **Higgsfield CLI** on PATH. If missing, point the user to
  https://github.com/higgsfield-ai/cli (Homebrew, npm or the install script) and let them
  install it; do not pipe an install script to a shell on their behalf.
- **Higgsfield session.** If `higgsfield account status` reports `Not authenticated` or
  `Session expired`, ask the user to run `higgsfield auth login` (interactive) and wait.
- **Upload-Post**, one of:
  - the MCP connector at `https://mcp.upload-post.com/mcp` (preferred: OAuth, no key in the
    prompt), or
  - `UPLOAD_POST_API_KEY` in the environment, sent as `Authorization: Apikey $UPLOAD_POST_API_KEY`.
- At least one social account connected to an Upload-Post profile. If none is, send the user to
  https://app.upload-post.com/manage-users (or call `get_connect_link` over MCP) and wait.

## Workflow

### 1. Pick the destination first

List the profiles and their connected accounts before generating anything:

- MCP: `list_users`
- HTTP: `curl -s https://api.upload-post.com/api/uploadposts/users -H "Authorization: Apikey $UPLOAD_POST_API_KEY"`

Use the exact profile `username` from the response; never invent one. Skip accounts with
`reauth_required: true` and tell the user they need reconnecting.

### 2. Choose the format from the platforms

| Target | Media | Aspect ratio | Notes |
|---|---|---|---|
| TikTok, Reels, YouTube Shorts | video | `9:16` | 5 to 12 s works for every short-form feed |
| Instagram feed, Threads, Bluesky | image or video | `4:5` or `1:1` | carousels: up to 10 images |
| YouTube (long), X, LinkedIn, Facebook | video | `16:9` | YouTube needs a title |
| Pinterest | image or video | `2:3` | |

If the targets disagree (a Short and a LinkedIn post), ask whether to generate one vertical
version for everything or one per format. One generation per format looks better and costs
more credits; say so.

### 3. Generate

Follow the Higgsfield defaults unless the user names a model: `seedance_2_5` for video,
`gpt_image_2_5` or `nano_banana_flash` for images. Check parameters with
`higgsfield model get <model> --json` when unsure, and quote the cost first with
`higgsfield generate cost ...` for anything longer than a few seconds.

```bash
# Vertical video for TikTok / Reels / Shorts
higgsfield generate create seedance_2_5 \
  --prompt "slow push-in on a ceramic coffee cup, morning light, steam rising" \
  --aspect_ratio 9:16 --duration 8 --resolution 1080p --wait --json

# Image for an Instagram carousel slide
higgsfield generate create gpt_image_2_5 \
  --prompt "flat-lay of a minimalist desk setup, warm tones" \
  --aspect_ratio 4:5 --wait --json
```

Branded ads (UGC, unboxing, product showcase) come from Marketing Studio; see the
`higgsfield-generate` skill for its avatar, product and hook flags. The publishing steps below
are the same.

`--wait --json` returns the finished job. Take the public `https://` result URL from it; if the
shape is unclear, list every URL in the output:

```bash
higgsfield generate get <job_id> --json | jq -r '.. | strings | select(test("^https://"))'
```

### 4. Score it (video, optional)

Offer the Virality Predictor before publishing a video meant to perform:

```bash
higgsfield generate create brain_activity --video <job_id_or_path> --wait
```

Report the overall score, the hook second and the report link.

If the hook is weak (the attention peak lands late, or the score is low for what the user
wants), offer a re-roll instead of moving straight to approval:

1. Rewrite only the opening of the prompt: motion or a cut in the first second, the subject
   in frame from frame one, no slow fade-in. Keep the rest of the prompt and the settings.
2. Quote the cost of the new generation plus its scoring, and wait for a yes.
3. Generate, score, and show both versions side by side: score, hook second, report link.
4. The user picks one, or asks for another round.

Stop after two re-rolls unless the user explicitly asks for more; every round spends credits.
The score informs the choice, it never blocks it: the user can publish a low-scoring clip,
and the approval in step 5 is still required either way.

### 5. Confirm

Write one caption per platform, not one caption for all of them: each feed handles length,
hashtags and line breaks differently. Keep a shared base text and adapt it:

| Platform | Limit | How to write it |
|---|---|---|
| TikTok | 2,200 chars | hook in the first line, 3 to 5 hashtags at the end |
| Instagram | 2,200 chars, 30 hashtags | hook first, line breaks between ideas, hashtags at the end |
| YouTube | title 100 chars | a real title; the caption goes to the description |
| X | 280 chars on standard accounts | one or two short lines, at most one hashtag |
| Threads | 500 chars | conversational, no hashtag block |
| Bluesky | 300 chars | short, no hashtag block |
| LinkedIn | 3,000 chars | first line readable on its own, few or no hashtags |
| Pinterest | title 100 chars | keyword-led title and description |

Show the user, in one message:

- the result URL (so they can watch it),
- the profile and the platforms it will go to,
- a table with the caption for each platform and its length against the limit,
- whether it publishes now, goes to the queue, or is scheduled.

The user can edit any single caption ("make the X one shorter", "no hashtags on LinkedIn").
Show the table again after every change, and publish only after an explicit yes on the final
version. A post to a public feed cannot be taken back cleanly.

### 6. Publish

Pass the Higgsfield URL straight through; Upload-Post fetches it, nothing is downloaded.
Always send the AI-generated flag: it sets TikTok's AI label and YouTube's synthetic-media
disclosure.

**MCP**

```
upload_video(
  videoPathOrUrl = "<higgsfield result url>",
  user = "<profile>",
  platforms = ["tiktok", "instagram", "youtube"],
  title = "<base caption>",
  platformOptions = {
    tiktokTitle: "<TikTok caption>",
    instagramTitle: "<Instagram caption>",
    youtubeTitle: "<YouTube title, max 100 chars>",
    youtubeDescription: "<YouTube description>",
    tiktokIsAiGenerated: true,
    youtubeContainsSyntheticMedia: true
  }
)
```

Every platform takes its own caption the same way: `<platform>Title` over MCP
(`xTitle`, `linkedinTitle`, `threadsTitle`, `blueskyTitle`, `facebookTitle`, `pinterestTitle`)
and `<platform>_title` over HTTP (`x_title`, `linkedin_title`, …). `title` is the fallback for
any platform without its own.

For images use `upload_photos(photosPathsOrUrls = [...], user, platforms, title, platformOptions)`.
Add `scheduledDate` (ISO-8601) to schedule, or `addToQueue: true` for the next queue slot.

**HTTP**

```bash
curl -s -X POST https://api.upload-post.com/api/upload \
  -H "Authorization: Apikey $UPLOAD_POST_API_KEY" \
  -F "user=<profile>" \
  -F "platform[]=tiktok" -F "platform[]=instagram" -F "platform[]=youtube" \
  -F "video=<higgsfield result url>" \
  -F "title=<base caption>" \
  -F "tiktok_title=<TikTok caption>" \
  -F "instagram_title=<Instagram caption>" \
  -F "youtube_title=<YouTube title, max 100 chars>" \
  -F "youtube_description=<YouTube description>" \
  -F "is_ai_generated=true" \
  -F "async_upload=true"
```

Images go to `/api/upload_photos` with one `-F "photos[]=<url>"` per image (YouTube does not
take images). Add `-F "scheduled_date=2026-11-01T09:00:00Z"` to schedule.

### 7. Report

Poll until every platform has finished:

- MCP: `get_status` with the `request_id` (or the `job_id` of a scheduled or queued post)
- HTTP: `curl -s "https://api.upload-post.com/api/uploadposts/status?request_id=<id>" -H "Authorization: Apikey $UPLOAD_POST_API_KEY"`
  (use `?job_id=<id>` for scheduled or queued posts; they report once they run)

Give the user one line per platform with the `post_url`, or the `error_message` in plain
words. TikTok can take a few minutes to return the URL; a TikTok result with
`fallback_to_inbox: true` is in the account's drafts and must be published from the app.

## Errors

| Symptom | Cause | Fix |
|---|---|---|
| `Not authenticated` / `Session expired` from `higgsfield` | CLI session lapsed | user runs `higgsfield auth login` |
| 401 from Upload-Post | wrong key or `Bearer` scheme | send `Authorization: Apikey <key>` |
| `None of the requested platforms are valid for profile` | platform not connected on that profile | connect it in Manage Users, or drop it |
| YouTube rejects the post | missing title | send `title` / `youtube_title` |
| Instagram rejects the video | aspect or length out of range | regenerate at 9:16 (Reels) or 4:5 (feed); keep it at 3 s or longer |
| `reddit_unavailable` (503) | Reddit posting is paused upstream | leave Reddit out |

## Rules

- Never publish, schedule or queue without an explicit yes on the final media and caption.
- Always send the AI-generated flag; never present generated media as real footage.
- Use only the profile names that `list_users` returns.
- Quote the Higgsfield cost before long or batch generations; credits are the user's money.
- Respond in the user's language.
