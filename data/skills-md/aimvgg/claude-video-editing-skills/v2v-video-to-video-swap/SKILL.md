---
name: v2v-video-to-video-swap
description: "Puts a person into any video clip with video-to-video (V2V) generation, keeping the clip's motion, timing and camera. Builds a character sheet of the person, draws start and end frames per shot, runs Wan 3.0 with the source clip as a reference, fixes residue on short spans, and matches the look to the footage around it. Works on a span of a reference video or on any clip the user has, and records the person's consent first. Use when someone wants a person or face swapped into a clip with video to video (V2V), a face swap, or a deepfake of themselves or someone who agreed, or needs a character sheet for a video model. Use for 'put me in this clip', 'face swap me into this', 'swap his face for mine', 'replace the player with our founder', 'V2V this shot with me in it' or 'make a character sheet of her'. For a style-only V2V pass with no person swapped, this skill does not apply."
license: Apache-2.0
compatibility: "Needs ffmpeg, an OpenRouter key (OPENROUTER_API_KEY) for the image and video calls as written, and a private R2 or S3 bucket that can sign HTTPS URLs. Another provider works if its API takes a video reference by URL."
---

# Swap a person into a clip with video-to-video

You take a source clip and a person who agreed, and give back the same clip with that person in it. The motion, timing and camera stay the source's. The method comes from the Dylan Patel hype video, where Dylan was swapped into a basketball video shot by shot ([zealous1/dylan-patel-hype-video](https://github.com/zealous1/dylan-patel-hype-video), `RECIPE.md` and `guide/`). It works on one clip alone. In a remake, `restyle-reference-video` sends each "swap" slot here.

Run every command from the user's project folder. Clips, sheets, frames and takes land in the project, never in the skill folder.

## Before you start

- **Consent.** Swap in only a person who has agreed to this use. Before the first paid call, write a row to `consent.json` in the project with their name, what they agreed to, how (message, email or in person) and the date. `check-video-render` reads it, and the recipe cites it. Never swap in a minor, and never make anyone appear to do something sexual, criminal or defamatory, even with consent. Keep the original subject's likeness out of anything you publish. Label the result as AI-generated where the platform asks.
- **Rights.** Say once that swapping into broadcast, film or music-video footage carries copyright risk on every platform. Some video models refuse it on output (see Traps).
- **Models.** Before choosing a model, check the current leaders on https://aimv.gg/generators. The models named here won in October 2026. Newer ones may beat them.
- **Access.** Generation runs through a hosted API such as OpenRouter (`OPENROUTER_API_KEY`). A privacy setting on the provider account can block some video and image models. Read the provider's error, and let the user decide any account change.
- **Budget.** Every generated shot bills the user's provider account. Before the first paid call, list each shot with its model and price, give the total, and wait for a yes. A swap costs about $0.50 to $0.90 a shot, and a sheet image about $0.06. Keep a running total in `costs.json` in the project. Stop and ask again before you pass the agreed amount.

## 1. Character sheet first

From three or more photos of the person, draw six views on one image (front, side profile with room in front of the nose, back of head, three-quarter, full body front and back). GPT Image 2.5 Sunburst through OpenRouter `POST /api/v1/images` with `input_references` worked, at about $0.06 an image. Sizes must divide by 16. For 16:9 use 1792x1008. If the safety check refuses a frame with the old subject, grey out their head and retry.

## 2. Start and end frames

Draw a start frame and an end frame for each shot with the same image call as step 1. Send the source clip's first or last frame as the first image and the sheet as the second. Draw a red box around the subject to replace on a copy of the frame, and send that copy too. Prompt "Edit the first image only. Replace the [subject] with the person from the character sheet (second image), same pose and size." Change only what must change. When you edit a frame, change the outfit first, then any number or text on it, then the face.

## 3. Generate

Cut the source span with ffmpeg. Wan fills the whole duration and invents motion past the end of the source. So slow the span by about 2x, picking the factor that lands it on a whole number of seconds, with `ffmpeg -i span.mp4 -vf "setpts=<factor>*PTS,minterpolate=fps=30:mi_mode=blend,tpad=stop_mode=clone:stop=30" -frames:v <seconds*30> span-slow.mp4`. Send that duration. Upload the slowed span to get an HTTPS URL (see Traps).

Send `POST https://openrouter.ai/api/v1/videos` with `model: "alibaba/wan-3.0"`, `prompt`, `duration` (whole seconds), `resolution: "720p"`, `aspect_ratio` and `generate_audio: false`. Put `input_references` in this order. First `{"type": "video_url", "video_url": {"url": "<signed HTTPS URL of the span>"}}`, then the sheet, two or three headshots and the start and end frames, each as `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}`. Images may be data URIs. Only the video needs an HTTPS URL. Omit `frame_images`. Pinned frames make Wan drop the clip without an error, and the bill is the only sign (about $0.43 instead of $0.88 for the same shot). The POST returns a job `id` and a `polling_url`. Poll it every 10 seconds until `status` is `completed` or `failed`. Download `unsigned_urls[0]` with the same `Authorization` header, and read the cost from `usage.cost`. If polling drops, poll the same `id` again. Never resubmit, because each submit bills.

The prompt starts "Edit the reference video." It lists what to keep (camera, blurs, flashes, grade, every move), then names the subject to replace and points at the sheet as the first reference image. Write features the model drops, such as a beard or glasses, into the prompt.

Afterwards, rebuild the shot at its real frame count by taking generated frame round((k + 0.5) * G / N) for output frame k, where G is the generated frame count and N the source count. About $0.50 to $0.90 a shot.

## 4. When the clip leaks

If the result copies text or numbers from the source, run Wan 3.0 again without the clip. Remove the `video_url` entry from `input_references`, keep the sheet, pin the start and end frames in `frame_images` (`frame_type` `first_frame` and `last_frame`), and use a short prompt.

## 5. Fix residue with short spans

A second V2V over half a second costs about $0.50 and is cheaper than regenerating the shot. Cut the half second around the residue from the take (not the source), run it through step 3 as its own span, and splice it back on the same frames with a short crossfade.

## 6. Look match

Grade each generated take to the source span frame by frame. Map each colour channel to the source's quantiles, multiply by a coarse grid of local gain (about 8 by 8) so brightness falls off where the source's does, then blur to match the source's motion blur and softness. Measure the result against the source with Laplacian sharpness and mean luma per frame. Generated shots read too clean beside broadcast footage. `clean-up-ai-video` has the film look and upscale passes that come after.

## 7. After each shot

Step through the last frames of every take. Run `check-video-render` on the shot when that skill is installed. Record the model, settings and cost per shot for `write-aimv-recipe`.

## Traps

- Seedance 2.5 refused every attempt on broadcast sports footage, with the clip removed and scorebugs blurred. It checks the output.
- Hailuo 3 rejects `frame_images` and references together. Frames-only runs invented motion and drifted jersey numbers.
- Video references must be HTTPS URLs. Upload each span to a private R2 or S3 bucket and sign it for an hour or less (for example `aws s3 presign s3://<bucket>/<key> --expires-in 3600`, with `--endpoint-url` for R2). Never use a public bucket. Delete each object as soon as its job reports `completed` or `failed`, and upload again for a retry. Send images inline as data URIs so the person's face is never uploaded to a bucket.
- Wan can hallucinate a flash frame at the end of a take. Step through the last frames.

## About

Made free and open source by [Arcmira](https://arcmira.com), the search engine for what people say in podcasts and videos. This skill is one of the [Claude video editing skills](https://github.com/aimvgg/claude-video-editing-skills), written while making real hype videos and AI music videos. Shipped by [Zeal](https://x.com/zealcaiden).
