---
name: video-publish
description: Gets a finished video out on YouTube (Shorts or long), Instagram Reels and TikTok - picks the video, makes the light export for Instagram and TikTok, the cover, the caption and the YouTube title, sets the time, shows the plan, then after the creator's yes publishes through Treg on their own connected accounts (setup included), or hands a ready-to-post kit when Treg isn't set up. Use when the user says publish, post it, schedule, upload to YouTube, put it on Instagram, TikTok, publier, poster, programmer, mets-le en ligne.
argument-hint: "[<slug or mp4>] [now | <date and time>] [youtube instagram tiktok]"
allowed-tools: Bash(ffmpeg *) Bash(ffprobe *) Bash(treg --version) Bash(treg connections ls) Bash(treg catalog *) Bash(treg balance)
---

# Video Publish

One finished video out, on the creator's own accounts. Making it is `/video-edit`.

**Nothing is posted before the creator's explicit yes on the plan of step 5.** That yes covers that video only.

Talk to them in their language. `<edit>` = `video-agent/edits/<slug>/`.

## 1. Which video

First match wins:

1. A path, a slug or a title they give: `<edit>/final.mp4`.
2. The video finished in this conversation.
3. Nothing: the newest `video-agent/edits/*/final.mp4`. Name it in the plan.

Then check `<edit>/published.md`: already there with this platform, say so and stop (unless they want to post it again).

Read the format with ffprobe: vertical (a short, for YouTube Shorts, Reels and TikTok) or horizontal (a long video, YouTube only by default).

## 2. Setup Treg (once)

Treg posts for them on their own accounts, free. Check:

```bash
treg --version
treg connections ls
```

Each platform they post on must show in the list with posting rights (`scopes` with `content_publish` on Instagram, `video.publish` on TikTok, `youtube.upload` or `youtube` on YouTube).

Missing: explain in one line, ask, then:

- **Install** (macOS and Linux; on Windows use the MCP: `claude mcp add --transport http treg https://treg.to/mcp/`, then `/mcp` to sign in):
  ```bash
  curl -fsSL https://treg.to/install.sh | sh
  treg login
  ```
- **Connect** only the platforms they post on, each opens the platform's own login:
  ```bash
  treg connections connect --provider instagram --capability post
  treg connections connect --provider tiktok --capability post
  treg connections connect --provider youtube --capability post
  ```
  Instagram needs a professional account (Creator or Business, free switch in the app's settings).

They don't want Treg: the manual route (6a) works with no setup.

## 3. The files

- **Master**: `<edit>/final.mp4`, full quality, for YouTube.
- **Social export** (shorts only): `<edit>/social.mp4`, H.264 + AAC, under 30 MB so Treg can host it for Instagram (TikTok accepts up to 64 MB). Missing or older than the master, re-encode at a bitrate that fits (about 28 MB × 8000 ÷ duration in seconds, minus 160 kb/s of audio, in kb/s):
  ```bash
  ffmpeg -y -i <edit>/final.mp4 -c:v libx264 -preset slow -b:v <rate>k -maxrate <rate>k -bufsize <2x rate>k -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart <edit>/social.mp4
  ```
  Check its size, and that it decodes: `ffmpeg -v error -i <edit>/social.mp4 -f null -`.
- **Cover**: `<edit>/cover.jpg`, always. Without one, Instagram takes frame 0, often a blink or a blank frame. Pick it from the hook: the face with the eyes open, the hook card fully in. Contact sheet of the first 3 seconds, read it, then extract the chosen time `<t>`:
  ```bash
  ffmpeg -v error -y -ss 0.1 -t 3 -i <edit>/final.mp4 -vf "fps=10,scale=270:-1,tile=6x5" -frames:v 1 video-agent/.tmp/hook-sheet.jpg
  ffmpeg -v error -y -ss <t> -i <edit>/final.mp4 -frames:v 1 -q:v 2 <edit>/cover.jpg
  ```
  Vertical: keep the key visual inside the central 3:4 (y 240 to 1680), the profile grid crops to it. A long video: a 1280x720 thumbnail is better; offer `/codex-images` to make one, or use a frame.

## 4. The texts

From `<edit>/post.md` (written by video-edit) when it exists, else from the video's script or transcript and `video-agent/voice.md`, in the video's language:

- **Caption** (Instagram and TikTok): a first line that hooks without repeating the spoken hook word for word (the first 125 characters show before "more"), 2 to 4 short lines on what the viewer gets, the ask from voice.md, then 3 to 5 hashtags of the topic. No #fyp, no wall of emoji.
- **TikTok caption** only when it should differ (shorter, other hashtags).
- **YouTube title**: Shorts under 60 characters, long under 70, the promise of the video, true to it.
- **YouTube description**: the caption, the chapters for a long video (from post.md), then their links (ask once and add them to voice.md).

Run the humanize pass of `video-script` (its `references/humanize.md`) on all of them when that skill is installed. Every name, number and claim comes from the video; none is added. Save them in `<edit>/post.md`, one heading per text.

## 5. The plan (mandatory)

- **Platforms**: a short goes to YouTube + Instagram + TikTok, a long video to YouTube, unless they name others.
- **Time**: the one they give (written in their local time and in UTC), else **now**.
- **Route** per platform: Treg (connected) or manual. Instagram and TikTok have no scheduling through Treg: they post **now**. YouTube can wait for a date (private + `publishAt`). A later time on Instagram or TikTok: run `/video-publish` again at that time, or go manual and use the app's scheduler.

Show it and wait for a clear yes:

```text
PLAN · budget-margins · 0:47 · social.mp4 18 MB
Cover: cover.jpg (0.8 s)  [shown as an image]
YouTube Shorts · Treg · 2026-10-11 18:00 Paris (16:00 UTC) · private until then
Instagram Reel · Treg · now
TikTok · manual (not connected)
Title: Your margin is lying to you
Caption: ...
Reply yes to publish, or tell me what to change.
```

A change on the plan: apply it, show the plan again.

## 6a. Manual

Open the folder (macOS `open <edit>`, Windows `explorer <edit>`, Linux `xdg-open <edit>`), then give the steps:

- **YouTube**: studio.youtube.com → Create → Upload videos → `final.mp4` → title and description from `post.md`, `cover.jpg` as thumbnail → Visibility → Schedule or Public.
- **Instagram**: the app → + → Reel → `social.mp4` → the caption → Edit cover → Add from camera roll → `cover.jpg` → Share (or Schedule in the advanced settings of a professional account).
- **TikTok**: the app or tiktok.com/upload → `social.mp4` → the caption → cover at the cover time → Post (or Schedule on the web).

## 6b. Treg

Before each call, `treg catalog get <id>` for the exact parameters (they change). All of these are free on their own accounts. Keep stdout only (`2>/dev/null`). One platform failing never blocks the others.

**Instagram reel**

1. Host the files (30 MB max each, 7 days): `treg host <edit>/social.mp4` and `treg host <edit>/cover.jpg` print public URLs.
2. `instagram.instagram.media.container.create` with `ig_user_id` (the `resource_ref` of their Instagram in `treg connections ls`), `media_type=REELS`, `video_url`, `cover_url`, `caption`.
3. Poll `instagram.instagram.media.container.status` every 10 s until `FINISHED` (`ERROR`: show it and stop for Instagram).
4. `instagram.instagram.post.publish` with the container id. Then its `permalink` (`instagram.instagram.user.posts` with `fields=id,permalink`, the newest one).

**TikTok**

1. `tiktok.tiktok.creator.info`: the privacy options they may use.
2. `tiktok.tiktok.video.publish.init` with the caption, a `privacy_level` from that list (public when it is there), `video_cover_timestamp_ms` = the cover time in ms (TikTok takes a frame, never an image), and `source_info` `FILE_UPLOAD` with the file size as one chunk.
3. PUT `social.mp4` to the returned `upload_url` with `Content-Type: video/mp4` and `Content-Range: bytes 0-<size-1>/<size>`.
4. Poll `tiktok.tiktok.publish.status` until it is published.

An answer `unaudited_client_can_only_post_to_private_accounts` (or only `SELF_ONLY` in the options): send it to their TikTok inbox instead with `tiktok.tiktok.video.inbox.init` (same upload, no caption), and tell them to open TikTok within 24 hours, paste the caption and post.

**YouTube**

1. `youtube.youtube.video.upload` with `uploadType=resumable`, the snippet (title, description) and `status` `{"privacyStatus": "private", "selfDeclaredMadeForKids": false}` plus `"publishAt": "<UTC ISO time>"` for a date (`"public"` for now).
2. PUT `final.mp4` to the session URL it returns.
3. `youtube.youtube.video.thumbnail.set` with `cover.jpg` (works on verified YouTube accounts; a refusal is fine, say it).

No session URL in the answer: go manual for YouTube.

## 7. Record it

Write `<edit>/published.md`, one line per platform: date, time, route, and the link (`https://youtube.com/shorts/<id>` or `https://youtu.be/<id>`, the reel, the TikTok) once live. Manual route: write it when they say it is posted.

Then say what is live, the links, and offer `/video-audit` in a week to see how it did.

## Honest limits

- Instagram and TikTok can't be scheduled through Treg, only posted now. Their own apps can schedule.
- TikTok keeps posts from new third-party apps private until the app is audited; the inbox route works around it.
- A platform can refuse a video (length, format, music rights). The error is shown as is; the manual route always works.
- Only post videos the creator owns or has the rights to, music included.
