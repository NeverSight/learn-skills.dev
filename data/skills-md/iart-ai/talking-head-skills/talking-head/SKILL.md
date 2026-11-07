---
name: talking-head
description: Create an AI talking head from the user's own photos plus a voice sample, or from a self-recorded video by extracting face frames and speech. Use an authorized cloned or existing ElevenLabs voice and a new script to generate speaking shots with fal MiniMax H3, narration and editable motion graphics, then render an MP4. Use for AI avatars, presenter videos, personal explainers and scripted on-camera clips. For a recording that only needs graphics without generating new speech, use a recording-editing workflow instead.
---

# Talking-head films

Turn the user's script into a film in which the person appears for the lines that benefit from direct address, and graphics explain the rest. The person is footage in the film. A request for a full talking-head performance is also valid; respect that choice.

Work in the user's output directory. `<skill>` below means the folder containing this file. Dependencies live with the skill so it works when installed separately from the repository:

```bash
pnpm --dir <skill> install --frozen-lockfile
node <skill>/scripts/talking-head.mjs --help
```

Requires Node 22+, ffmpeg/ffprobe, `FAL_KEY` and `ELEVENLABS_API_KEY`. Read [the workflow reference](references/workflow.md) for plan fields, commands, recovery and provider limits. Credentials belong in the local environment, never in a plan or output source code. Photos and reference speech are uploaded to fal; voice samples and text go to ElevenLabs.

## Inputs and plan

- Offer two input paths: **photos + voice** (one or more photos of the user and a clean voice recording/existing voice ID), or **self-recorded video** (one clip provides both the user's appearance and voice). A video used as identity input is different from a recording the user wants edited unchanged; do not route the former to b-roll editing.
- For a new recording, have the user save a short phone/webcam video, ideally 30–60 seconds of one person speaking naturally, with a clear face, open eyes, steady lighting and no background music or other speakers. A shorter existing recording can be used, with potentially weaker voice-clone quality. The skill accepts the saved video file; it does not include a camera recorder UI.
- For video input, run `prepare-person --video inputs/me.mov --out inputs/person`. This is local and needs no API keys. Inspect `frames.jpg` and the full-size candidate portraits, pick the clearest frame first, and listen to `voice.wav` when playback is available. The script samples timestamps, not facial quality; discard blinking, blurred or obstructed frames. Use `--frame-times` or an audio interval if better material exists elsewhere. Read [the workflow reference](references/workflow.md#self-recorded-video) for exact commands and file paths.
- Use supplied photos, voice and text. Ask only for missing identity assets or authorization to use someone else's voice. A supplied existing voice ID avoids creating another clone. If the user has already authorized the voice, use that authorization; do not ask again.
- The first image determines the clothing and setting. Additional photos help preserve identity. Do not change someone's face or invent a studio portrait unless requested.
- For a topic rather than a script, write the script first. On-camera lines are typically the hook, a personal observation and the close. Explain steps, evidence and comparisons with motion. Usually one to three short on-camera lines suffice; a full performance costs more generated video.
- Put one short on-camera line in each `talking` scene, roughly 2–11 seconds of speech. Split longer lines at sentence or clause boundaries. The measured audio, not a rough word estimate, determines the shot length. A `motion` scene uses narration and a full-frame graphic.
- Use only facts, names, figures and quotes supplied by the user or present in the script. Keep headings brief. Use captions only when requested.

Write `plan.json` using the reference schema, then dry-run it. Use the user's existing budget; otherwise start with a short sample before generating a long film. Generation is a paid action when requested; no separate confirmation ritual is required for an already authorized run. Never silently retry a paid request.

## Generate

Clone once, or use an existing voice ID. The clone must finish any ElevenLabs verification before synthesis. Set that ID in the plan. Generate into a fresh `runs/<name>` directory:

```bash
node <skill>/scripts/talking-head.mjs generate --plan plan.json --out runs/intro --dry-run
node <skill>/scripts/talking-head.mjs generate --plan plan.json --out runs/intro
```

The script synthesizes all lines, checks actual durations, generates the talking-head footage, and transcribes the returned footage. It saves request IDs and results. Repeating the same command resumes those requests; a changed script or image needs a new output directory. If a request response was lost, follow recovery instructions instead of deleting state and buying another take.

H3 uses the ElevenLabs take as a voice and delivery reference. It creates its own audio; it is not a guaranteed frame-exact lip-sync renderer. **Keep the H3 audio on speaking shots.** For motion scenes use ElevenLabs narration. Do not dub the whole film with a second track or narrate over a speaking shot. Review `verification.json`: differences can be model additions, omissions or transcription errors. Check the actual clip before deciding, and do not automatically buy replacement takes.

## Design the film

`generate` copies `visuals.mjs` into the output folder. Edit it there. The starter artwork is a runnable example, not the final creative brief. The renderer calls `draw(ctx, scene, time, { width, height, fps })` for each frame with a Canvas 2D context. Scene times are local seconds; `scene.words` contains measured speech timings.

- Whenever the speaker appears, share the frame with something designed: a keyword, diagram, lower third, or a framed layout. A watermark or a whole sentence used as a caption is not a substitute for that design.
- Keep overlays off the face. Check actual early, middle and late composited frames. If the face overlaps the default lower third, move or resize the artwork.
- Follow the argument rather than cutting at every noun. Motion should show the idea: a comparison, a process, a growing list, a relationship. Preserve room to read it.
- Graphics can lead their spoken anchor by about six frames; a withheld answer should land on its word. Use the measured returned-video timings for talking scenes, not the original TTS timings. Never shift audio to match graphics.
- Prefer a light, legible surface for explanatory graphics unless the brief calls for another direction. No invented statistics or generic decorative dashboards.
- Use deterministic time-based drawing. No network assets, random values or wall-clock animation inside `draw`. The environment also exposes `registerFont(path, family)`; call it once on the first frame to load a local font if the language needs glyphs unavailable on the host. Check text at the actual output size.

## Render and review

```bash
node <skill>/scripts/talking-head.mjs render --manifest runs/intro/film.json
```

Rendering is local and can be repeated without provider calls. It preserves the original sound of each source scene, adds the artwork, and joins the scenes. Inspect the composited images in `review/` for every scene and play `film.mp4` with sound to review the delivery, joins and lip sync when playback is available. Still images and transcripts alone cannot prove those qualities; state that limitation if you cannot listen or watch.

Deliver the MP4, the editable `visuals.mjs` and plan when useful, and `speech.vtt` if requested. Mention any unreviewed transcript differences or visible issues. Keep private voice samples, provider URLs, credentials and internal run state out of public examples and commits.
