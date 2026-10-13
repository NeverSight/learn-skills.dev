---
name: codex-images
description: Generates images with Codex (OpenAI's coding agent and its built-in image tool, included in a ChatGPT plan) - YouTube thumbnails, covers, B-roll stills, callout visuals, profile pictures - one Codex job per image, several in parallel, with the creator's photos as reference when the face matters, then copies them into the project with a manifest. Use when the user says generate an image, a thumbnail, a cover, make me a visual, codex images, génère une image, miniature, or when video-publish or video-edit needs an image.
argument-hint: "<what to make> [x<count>] [ref <photo>...] [for <slug>]"
allowed-tools: Bash(codex --version) Bash(codex login status) Bash(ls *) Bash(cp *) Bash(sips *) Bash(ffprobe *)
---

# Codex Images

Images made by Codex's built-in image tool, run from the terminal: one `codex exec` per image, several at once. It uses their ChatGPT plan (Plus or Pro), no API key.

Talk to them in their language. `<out>` = the output folder: `video-agent/edits/<slug>/images/` for a video, else `video-agent/images/<name>/`.

## 1. Codex (once)

```bash
codex --version
codex login status
```

- Not installed: `npm i -g @openai/codex` (needs Node 20+), or `brew install codex` on macOS.
- Not logged in: they run `codex login` themselves (it opens the browser, "Sign in with ChatGPT"). Never ask for an OpenAI key or password in the chat.

## 2. The brief

One image = one prompt. Never pack several ideas into one job.

Ask only what is missing, in one message:

- **What for**: thumbnail (1280x720, 16:9), short cover (1080x1920, 9:16), square post (1:1), a still for a callout or B-roll (the video's format).
- **How many**: 1 by default; 3 variants for a thumbnail (a different idea each, not the same one three times).
- **Their face**: a thumbnail with them in it needs 1 to 3 clear photos (a frame of a take works: `ffmpeg -v error -y -ss <t> -i <take> -frames:v 1 -q:v 2 <out>/ref-face.jpg`). Pass the absolute paths.

Write each prompt in English, concrete: the subject, the framing, the background, the light, the colors, the text on the image (3 words at most, written exactly in quotes, in the video's language), and the format. For a thumbnail: one subject, big readable text, strong contrast, a face with a clear emotion, nothing in the bottom right corner (YouTube puts the duration there). Every claim on the image comes from the video.

Show the prompts in a numbered list and wait for a yes (each image uses some of their Codex usage limit).

## 3. Generate

One job per prompt, at most 3 at a time, each in the background. Always end with `< /dev/null` (without it `codex exec` waits for input forever), and keep the last message in a file:

```bash
mkdir -p <out>/logs
codex exec --skip-git-repo-check -s workspace-write -C "$PWD" \
  --output-last-message <out>/logs/<n>-<name>.txt \
  "Use your built-in image_gen tool to generate exactly one raster image for the prompt below. Do not edit any file. Do not ask questions. No SVG, no HTML, no placeholder.
Reference images (pass them to image_gen as referenced_image_paths): <absolute paths, or none>
When done, reply with exactly these two lines:
ASSET_NAME: <kebab-case-name>
IMAGE_PATH: <absolute path of the generated image>

Image prompt:
<the prompt>" \
  < /dev/null > <out>/logs/<n>-<name>.log 2>&1
```

A job takes about 1 to 3 minutes. When it ends, read its `.txt`, take `IMAGE_PATH` and copy the image:

```bash
cp "<IMAGE_PATH>" <out>/<n>-<name>.png
```

No `IMAGE_PATH` in the answer: the newest file in `~/.codex/generated_images/` (`ls -t ~/.codex/generated_images/*/* | head -3`) created after the job started. Nothing new there: the job failed, show the end of its `.log` (often a usage limit, or `codex login` needed) and run that one again once.

## 4. Check and hand over

- One image per prompt, and no two identical (`shasum <out>/*.png`).
- The size: `sips -g pixelWidth -g pixelHeight <file>` (macOS) or `ffprobe -v error -show_entries stream=width,height -of csv=p=0 <file>`. A thumbnail must be 16:9: crop or scale it to 1280x720 with ffmpeg (`-vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720"`), under 2 MB as JPG.
- Look at each image: the text spelled right, the face like them, nothing odd (hands, extra letters). A wrong one: fix the prompt and run that one again.

Write `<out>/manifest.json`: one entry per image with `file`, `prompt`, `refs`, `date`. Show the images, then:

- A thumbnail or cover: `/video-publish` uses `<edit>/images/` (they pick one, it is copied as `<edit>/cover.jpg`, the cover and the YouTube thumbnail).
- A still for a video: `/video-edit` can place it as a callout image (copy it into `video-agent/studio/public/`).

Delete `<out>/logs/` once everything is fine.

## Honest limits

- The image tool is OpenAI's, inside Codex: the result depends on it, and it changes. Text on the image can come out misspelled: always check it.
- A face from reference photos looks close, rarely perfect. Real photos of them stay the safest for a thumbnail.
- Each image counts against their ChatGPT plan's Codex limits; a limit reached means waiting or a bigger plan.
- Only use photos of people who agreed, and no logos or characters they don't own.
