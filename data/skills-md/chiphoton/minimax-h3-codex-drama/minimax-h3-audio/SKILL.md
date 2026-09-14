---
name: minimax-h3-audio
description: Create, enhance, diagnose, and optionally execute MiniMax H3 audio-only prompts through the verified fixed 32x32 ComfyUI proxy. Use for prompt-generated dialogue, narration, announcements, ambience, foley, robot sounds, or animal calls when no reference media is required; use R2V for reference-controlled voices or sounds.
---

# MiniMax H3 Audio

Create native H3 audio without retaining a video. The bundled workflow gives the joint FL2VA sampler a disposable 32x32 visual latent, decodes the audio branch, and saves lossless FLAC through `SaveAudio`.

## Route the request

- Use this skill for audio invented entirely from text: one or more voices, narration, announcements, ambience, foley, robot sounds, or animal vocalizations.
- Use `minimax-h3-reference-to-video` when an image, video, or audio reference must control identity, performance, voice, or sound. This audio proxy is prompt-only and is not a voice-cloning workflow.
- Keep requested duration between 0 and 15 seconds. Split longer material into coherent clips.
- Never expose visual size as a creative control. The proxy must remain fixed at 32x32.

## Write the prompt

Return a production-ready prompt when generation was not requested. Preserve user-supplied spoken words exactly inside H3 dialogue tags.

Use a compact structure:

```text
[Integrated audio description: speaker or source, delivery, mood, acoustic setting, event order, and timing]

Dialogue: <d>[English] Exact spoken line.</d>

Soundscape: [diegetic ambience and effects, or "clean studio recording; no music"]
Non-diegetic music: [music direction, or "none"]
```

For people, specify only attributes that affect sound: adult/child/older speaker, vocal register or timbre, pace, intensity, mood, and scenario such as documentary narration, news report, or airline announcement. Do not rely on vague labels like “woman voice” alone.

For speech, fit the script to the duration. As a starting estimate, allow roughly two to three spoken words per second, then leave additional room for pauses, ambience, and sound effects. Exact wording is stochastic and must be checked after generation.

For non-speech audio, state the source, event count and order, distance, room or outdoor acoustics, and whether overlap is allowed. Say `no intelligible human speech` when applicable. For animals, describe audible behavior rather than human emotions or dialogue.

## Execute through ComfyUI

When the user asks to generate, test, submit, render, or retrieve the audio, follow `../minimax-h3-comfyui/SKILL.md` in `audio` mode. Preserve the finished prompt verbatim.

- Use Turbo by default. Use standard sampling only when the user asks for quality-first generation or supplies `[turbo=false]`.
- Prepare `audio-turbo.api.json` or `audio.api.json` through the shared preparer; do not hand-edit node IDs.
- Save the result as FLAC. The prepared workflow has no video decode, mux, or video-save branch.
- If the ComfyUI skill delegated prompt enhancement back to this skill, return the prompt to that workflow and do not recursively start another execution pass.

## Verify the result

Treat the output as generated source audio, not a mastered deliverable.

1. Confirm the exact ComfyUI prompt ID and history entry before claiming success.
2. Confirm the expected duration, decodable FLAC, and native 32 kHz stereo stream.
3. For speech, transcribe the result and compare it with the locked line. Distinguish punctuation or number formatting from missing or changed words.
4. For non-speech audio, listen or inspect a spectrogram for event order, separation, and absence of unwanted dialogue.
5. Measure integrated loudness, true peak, and clipped samples. H3 can generate hot peaks; flag or normalize downstream rather than describing raw output as broadcast-ready.

Read [references/verified-behavior.md](references/verified-behavior.md) when reporting capability, limitations, or test evidence.

## Return

State the mode and variant, duration and seed, prompt ID, output filename, transcript or event check, and any peak/clipping warning. Return the playable local audio when available.
