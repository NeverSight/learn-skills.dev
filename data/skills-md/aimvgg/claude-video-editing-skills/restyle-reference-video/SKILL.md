---
name: restyle-reference-video
description: "Restyles a reference video shot for shot around a new subject, keeping its cuts, timing, camera moves, look and song and swapping the person, text and story. Rebuilds hype videos, music videos, ads, reels and TikToks. Measures the reference first, keeps its audio as the clock, and generates only the shots that have to change. Also replaces a voice or announcer in a clip without losing the music, and cuts podcast clips onto the beat. Use when someone links a video and says 'make this but about X', 'remake this', 'recreate this edit', 'restyle this music video', 'do this shot for shot with my face', 'make a hype video like this one' or 'do this style for our launch', or asks to 'remove the announcer from this clip', 'replace the voiceover with our lines' or 'make these podcast clips hit on the beat'. Not for putting a person into one clip with no edit to rebuild (v2v-video-to-video-swap), finishing shots or adding a film look (clean-up-ai-video), or turning footage into a new art style."
license: Apache-2.0
compatibility: "Needs ffmpeg, Node 20 or newer, uv, Python 3 with librosa, demucs, opencv-python-headless and mediapipe, and headless Chrome. macOS or Linux. A swap needs a generation API such as OpenRouter and an R2 or S3 bucket for signed URLs. Upscales need a rented GPU such as Modal. Deepgram is optional for re-transcription; Whisper works locally."
---

# Restyle a reference video

The reference is the spec. You measure it, keep everything that does not have to change, and replace slots one at a time against the reference's own clock. The worked example is the Dylan Patel hype video, a remake of a 30 s basketball video ([zealous1/dylan-patel-hype-video](https://github.com/zealous1/dylan-patel-hype-video), `RECIPE.md` and `guide/`).

Run every command from the user's project folder. In the commands below, `<skill folder>` is this skill's folder, the one that holds this `SKILL.md`. Downloads, takes and renders land in the project, never in the skill folder.

This skill hands steps to five sibling skills by name. Use each one the way your agent loads skills, or open its `SKILL.md`. If one is not installed, tell the user and give `npx skills add aimvgg/claude-video-editing-skills --skill <name>`.

## Before you start

- **Consent.** Swapping a real person into footage, or putting words in their voice, needs that person's consent, recorded in the project and in the recipe if one is written. Never swap in or voice someone who has not agreed. Keep the original subject's likeness out of anything you publish.
- **Rights.** Say once that a remake of broadcast, film or music-video footage carries copyright risk on every platform. Some video models refuse it on output. `v2v-video-to-video-swap` lists them.
- **Models.** Before choosing a model, check the current leaders on https://aimv.gg/generators. The models named here won in October 2026; newer ones may beat them.
- **Access.** Generation runs through a hosted API such as OpenRouter (`OPENROUTER_API_KEY`). A privacy setting on the provider account can block some video and image models. Read the provider's error, and let the user decide any account change.
- **Tools.** Besides `ffmpeg` and Node, you need Python with librosa, demucs, opencv-python-headless and mediapipe, headless Chrome, an R2 or S3 bucket for signed URLs, and a Modal account for upscales. Tell the user what is missing before step 1.
- **Budget.** Generation bills the user's provider account. Before the first paid call, list each slot you will generate with its model and price, give the total, and wait for a yes. Keep a running total in `costs.json` in the project. Stop and ask again before you pass the agreed amount. For scale, the Dylan Patel hype video spent $21.54 on image and video generation and $11.94 on GPU time.

## 1. Measure the reference

Download the reference with `scripts/pull.mjs` from this skill's folder. It is a copy of the script in `find-youtube-clips-and-quotes`, so this skill works when installed alone. `node "<skill folder>/scripts/pull.mjs" <url> --probe` shows the length first, and `node "<skill folder>/scripts/pull.mjs" <url> --name ref` downloads a short video whole. It lands at `clips/ref/clip.mp4`, with `info.json` beside it. Over 10 minutes it stops; tell the user the length and size, and add `--whole` only after a yes. If a download fails, an old yt-dlp is the usual cause. Set `YTDLP_VERSION` to the newest stable release on https://github.com/yt-dlp/yt-dlp/releases that is at least a day old, never a nightly. Then measure the reference before you watch it.

- `ffmpeg -hide_banner -i clips/ref/clip.mp4 -vf "scdet=threshold=7,signalstats,metadata=print:file=analysis/frames.txt" -f null -` writes every frame's values. Create `analysis/` first. `lavfi.scd.time` lines are hard cuts, jumps in `lavfi.signalstats.YAVG` are flashes, and `lavfi.signalstats.SATAVG` near 0 marks grayscale. Write the times in seconds to `analysis/reference.json`.
- **Contact sheets.** Make a 2 fps overview, then 10 fps only around flagged moments. For a window, put `trim=start=S:end=E,setpts=PTS-STARTPTS` before `fps` and `tile`. With `-ss` after `-i`, the tiles still count from t=0, so the first sheet does not start at the window.
- Per-frame luma, Laplacian sharpness, phase-correlation shift and frame diff give each move's shape and the film flicker you will borrow later.
- **Song.** Read the title from the user, the post text or `info.json` (`track`, `artist`), and ask if none names it. Get beats with librosa, and mark dropouts and hits. The reference's audio is the clock for everything after.

## 2. Write the slot sheet

One row per reference shot, with its start and end frame, what happens, and a verdict.

| Verdict | Use when | How |
| --- | --- | --- |
| keep | Nothing in it names or shows the old subject | Copy the span |
| overlay | Only text or graphics change (scorebug, banner, lower third) | Draw it in software over the kept span. Do not ask a model for text |
| swap | The subject's body or face is on screen | Use `v2v-video-to-video-swap` (step 4) |
| render | A designed insert (newspaper, card, end logo) | Code-render it (step 6) |
| replace | The beat needs new footage (podcast clips, product) | `find-youtube-clips-and-quotes`, then step 5 for talk clips |

Minimize generated pixels. Each generated span is a place for artifacts to appear.

## 3. Audio

Keep the original mix wherever the old subject is not named. To remove a voice, separate with Demucs `htdemucs_ft` and use the vocal stem as a guide for where the words are; do not mute the stem across a span. The four stems do not sum back to the original, and muting a stem removes sung notes, reverb and width with the words. Replace only the words. Have the user record the new lines dry, or use a voice the user has consent for. Split takes at pauses of 0.8 s or more, place each line by cross-correlation against the line it replaces, EQ toward the original voice, and match loudness section by section to the reference.

Re-transcribe the result (Deepgram Nova-3 or Whisper) to prove the old words are gone. Whisper invents text over silence, so ignore its lines in quiet stretches.

## 4. Swap the subject

Use the `v2v-video-to-video-swap` skill for every swap slot. Give it the slot's span as the source clip. It draws new start and end frames from the character sheet and the span's own first and last frames. It holds the character sheet, the Wan 3.0 call, the residue fixes, the look match and the video model traps. About $0.50 to $0.90 a shot.

## 5. Podcast clips that hit on a beat

For replace slots filled with talk. From the Dylan Patel hype video's 7-second podcast section, which cuts ten beats from ten different videos in a row.

- **Source honestly.** Find every clip with `find-youtube-clips-and-quotes`, one episode per beat. Any on-screen search tag must be the query that actually found the clip. Write tags lowercase, speaker first, under the channel name. In the example the tag read `arcmira.search(speaker: "dylan patel", query: "nvidia")`, a readable form of the real call, not code to run.
- **Beat grid first.** Get the song's beat grid with librosa before you place a clip, and put every cut on a beat.
- **Face-matched zoom-through.** Detect the face in every clip (OpenCV DNN or MediaPipe Face Detection; OpenCV 5 dropped `CascadeClassifier`, so pin `opencv-python-headless<5` if you use it). Scale and place each clip so the face lands at the same size and spot as the last, and keep the zoom moving through the cut. Face wander across cuts went from 6 to 9% of the frame to 2%.
- **Pacing.** Never put three moves in under half a second. Retime a beat later instead. Shake vertically only.
- **Make the person pop.** Brighten the face against the room. Measure the face-to-room brightness ratio in the reference (2.18 in the example; raw podcast footage is about 1.0) and aim near it. Then add a soft glow around the person from a MediaPipe person-segmentation matte (keep the person whose matte holds the target face). It beat a faded print look and heavy burn flashes.
- **Text over flashes.** Bright flash frames wash out on-screen tags. Put a soft shadow under the letters that darkens as the flash brightens.

## 6. Code-rendered inserts

Build designed beats as an HTML canvas page and render it frame by frame in headless Chrome over the DevTools protocol, starting on the previous shot's exact last frame. Render text at 2x to 4x and downscale. Capture big frames in horizontal strips; one multi-megabyte screenshot can stall the socket. Credit every fact on the insert to a source you checked.

## 7. Review and assemble

- **Takes page.** Build a local page that plays the reference audio and lets the user pick one take per slot from `takes.json`. Save the picks to a file in the project.
- Assemble with one deterministic render script that takes scene overrides and a tag, so a candidate never overwrites the current cut. Swap audio with a `-c:v copy` remux.
- Show finishing choices as full exports side by side, not browser previews. Compare frame rate, film look, upscale and opener. In the example, 30 fps beat 60 because RIFE in-betweens smeared text, cuts and whips; Worn film borrowed the reference's measured flicker; SeedVR2 7B at 1440 then Lanczos to 1080 beat a 1080 pass, which pads to 1088 and leaves a seam. `clean-up-ai-video` holds each of these passes.

## 8. Gate and publish

Run `check-video-render` on every candidate before anyone watches it, when that skill is installed. Write the recipe with `write-aimv-recipe`.

## Traps

- Random effects must match across reruns. Fix the random seed, and keep the order of calls that draw from it.
- The video model traps (Seedance refusals, Hailuo frames plus references, signed URLs, Wan flash frames) are in `v2v-video-to-video-swap`.

## About

Made free and open source by [Arcmira](https://arcmira.com), the search engine for what people say in podcasts and videos. This skill is one of the [Claude video editing skills](https://github.com/aimvgg/claude-video-editing-skills), written while making real hype videos and AI music videos. Shipped by [Zeal](https://x.com/zealcaiden).
