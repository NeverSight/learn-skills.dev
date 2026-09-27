---
name: scenario-audio
description: Use when generating or handling audio on Scenario via MCP. Triggers include music tracks, full-length songs with vocals written from lyrics, background scores, soundtracks, game sound effects, SFX, foley, ambience, looping audio, voiceover, narration, speech, TTS, text-to-speech, dialogue, voice cloning, re-voicing a recording, scoring or adding sound to a video, transcription, or requests to create, wait on, play, or download audio files (MP3, WAV) with Scenario tools.
license: MIT
---

# Scenario Audio Generation

## Overview

Scenario generates audio through the same loop as images. The live catalog covers three generation lanes (music, sound effects, voice/speech) plus video-to-audio soundtrack models and audio utilities. Connection and the core generation loop: see the `scenario` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step           | Tool                                                                                        | Notes                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Find a model   | `recommend` with the need in the user's own words; `search` only for a member known by name | `capability="txt2audio"` covers music, SFX, and TTS; optional, inferred from the prompt when omitted |
| Inspect inputs | `model_schema_get`                                                                          | audio schemas vary widely: durations, lyrics, voices, looping                                        |
| Generate       | `model_run`                                                                                 | schema-conformant parameters; wait=false for long jobs                                               |
| Wait           | `jobs_wait`                                                                                 | blocks server-side; on timeout re-call with pending_job_ids                                          |
| Listen         | `asset_display`                                                                             | renders an inline audio player                                                                       |
| Save           | `asset_download`                                                                            | returns a download URL: `curl -L -o out.mp3 "<url>"`                                                 |

Find existing audio assets with `search` target="assets", filters={kind: "audio"}. Team and project scope (`team_id`, `project_id`): see the `scenario` skill.

## What the audio surface covers

- Music: text-to-music models produce short beds or full-length songs with vocals; the song lane has its own contract, below.
- Sound effects: text-to-SFX models generate short clips from a description; some support seamless looping.
- Voice and speech: text-to-speech with preset voices, multilingual output, and emotion or pacing controls; some clone a voice from a short clip, and speech-to-speech re-voices a recording.
- Video to audio: models that score a silent video or add synchronized effects.
- Utilities: `model_scenario-audio-cut`, `model_scenario-audio-split`, `model_scenario-audio-extract`, and `model_scenario-compose-video` (fixed ids: each is Scenario's single deterministic tool for its operation, so discovery would only re-derive them); the compositor lays a finished track (score, voiceover, re-voiced take) over a clip as an audio layer, per `scenario-video-assembly`; for speech-to-text transcription, `recommend` with the need in the user's own words.
- Stem separation: one named stem per run (discover with `recommend`), vocals included, with no instrumental option. Voice isolation returns the clean speech and never the removed music and effects as a second stem, so a two-stem split (voice against everything else) is a gap to report, not a member to keep hunting for.

Per-family contracts: `scenario-elevenlabs` (speech, dubbing, re-voicing, music, SFX), `scenario-ace-step` and `scenario-minimax-music` (songs), `scenario-sonilo` (SFX and video scoring).

## Worked example: a game sound effect

1. `recommend` with `capability="txt2audio"` and the user's own words as `prompt` ("a game sound effect: a heavy wooden chest creaking open"). The ranking returns txt2audio models such as `model_elevenlabs-sound-effects-v2` (example only).
2. `model_schema_get` with that `model_id`. Returns the exact fields: prompt plus controls such as duration or looping.
3. `model_run` with the same `model_id` and parameters={"prompt": "heavy wooden treasure chest creaking open, single event, dry, no music"}.
4. `jobs_wait` job_ids=["job_xxx"] on any `job_id` returned without assets (`in_progress` after a timed-out wait, the backend's `queued` or `in-progress` after `wait=false`), re-calling with the returned pending_job_ids on timeout.
5. `asset_display` asset_id="asset_xxx" to play it inline.
6. `asset_download` with no `format`, then save the returned URL with `curl -L`.

Prompting tips:

- SFX: name the source, material, action, and acoustic space, and say what to exclude ("no music", "no reverb"). One event per clip; generate variations as separate runs.
- Music: give genre, mood, tempo, and instrumentation. Short beds usually take a single prompt, with duration or looping in the schema.
- Speech: keep the text field to the words to speak; voice, language, emotion, and pacing live in separate schema fields or inline tags.

## Speech and dialogue

Discover a voice member with `recommend` (`capability="txt2audio"`, the user's words, "two-person dialogue" when it is one), then read its text field's description in `model_schema_get`: that is where a member usually states its own delivery grammar.

- **Tag syntax is per member, even within one family**: square brackets (`[whispers]`), angle brackets (`<sigh>`, `<short pause>`), parentheses (`(sighs)`), or wrapping pairs (`<whisper>text</whisper>`), and some read none. A tag in the wrong grammar can be spoken aloud, so copy the spelling from the text field's description; where it names none, from the member's catalog description or `recommend`'s notes, and with no source write no tags. A correctly spelled tag is a request, not a guarantee: two identical runs have disagreed on one, so have the user listen before a take is final and re-run a take whose tag was skipped.
- **Two voices, one take.** A member with a multi-speaker array (up to 2 rows of a speaker label and a voice at authoring time) reads the text as turns, one `Name: line` per turn, each `Name` matching a row's label exactly; an unprefixed line continues the previous turn, and the single-voice field is ignored in that mode. Preset voice names say nothing about gender, age, or tone, so state which preset plays whom and let the user confirm before the paid run. A scene with more speakers is split into takes of at most two, delivered in order or laid over the picture per `scenario-video-assembly`.
- **Text is capped and priced.** The text field carries a `max_length` (5000 characters on one member at authoring time), an overrun is a 400, and `cost_impact` marks it as the price driver: split a long script at turn boundaries and `dry_run` the first take.
- **Pin the language** through the schema's language field when there is one, rather than naming it in the text.

## Songs with vocals

A full-length song is not a longer music bed, and song schemas vary more than the rest of the lane, so `model_schema_get` decides the shape: a style prompt plus a separate lyric sheet, one prose prompt carrying both, or an ordered section array with per-section text and styles.

- **Words never go in a style field.** Where the schema splits the two, the style field carries genre, mood, tempo, key, vocal style, and instrumentation; the lyric field carries the words, shaped by section tags such as `[Verse]` and `[Chorus]`.
- **Instrumental and auto-lyrics are flags** where the schema has them; asking for either in prose is unreliable, and where no flag exists the text fields are the only lever. Flipping the instrumental flag on a rerun gives a different take, not the same song: `seed`, where a model has one, only repeats identical settings. For an instrumental of a track you already have, try an audio2audio cover model (discover with `recommend`), checking the schema since not all carry the flag.
- **Text fields are length-capped** per model and field, and going over is a 400 rather than a truncation.

Where the schema exposes a duration field (flagged `cost_impact`), it caps both length and price; where none exists, the lyric sheet or prompt sets both. Either way, price the song with `dry_run: true` before committing, then launch with `wait: false`; both are `model_run` arguments, not `parameters` keys.

Repeatability and batching are per member, not per lane: at authoring time the repaint members took `numOutputs` (1 to 4) and no `seed`, so a repaint that must keep the same singer is run as a batch and picked from, while the section composers had `seed` and no `numOutputs`. Read both off `model_schema_get` before promising either.

## Extending a song

Making an existing track longer is its own `audio2audio` lane, not a longer text-to-music run: `recommend` with `capability="audio2audio"` and the extension need in the user's words; use `search` only when the member is already known by name. The member that does it takes the song as `audio` and an ordered `sections` array (up to 30 at authoring time) where each entry either keeps a slice of the original (`sourceStartSeconds` and `sourceEndSeconds`) or generates a new one (`text` with `[Verse]`-style tags, `durationSeconds`, `positiveStyles` as an array), with `contextAdherence` deciding how closely new sections follow their neighbors. Kept slices bill like generated audio of the same length, so `dry_run` the whole plan first. The repaint, edit and add-layer members regenerate inside the original's duration and never lengthen it, and `recommend` ranked an older text-to-music member for "extend a song" at authoring time: an extension is not a `txt2audio` need, so do not take that pick.

## Common mistakes

- Hardcoding generative model IDs: availability differs per team and evolves. Re-discover each session, `recommend` for the need or `search` for a name; only the fixed first-party tool ids above stay constant.
- Skipping `model_schema_get`: one audio model's parameters will not fit another (voices, durations, and lyric fields all differ).
- Polling `job_get` in a loop: music jobs can run minutes. Use `jobs_wait`; on timeout re-call with pending_job_ids.
- Pasting raw asset URLs into chat: use `asset_display` to play audio.
- Passing `format` to `asset_download` for audio: it converts image formats only, so omit it.
- Putting voice direction inside TTS text ("say this angrily"): direction can end up spoken. Use the schema's emotion or voice fields.
- Writing a dialogue as one voice reading both parts: on a multi-speaker member, fill the speaker rows and prefix every turn with its label, since with the rows empty the member reads everything in its single voice.
- Pasting lyrics into the style field: the model then describes a song instead of singing one.
- Answering "make it longer" with a repaint or a new text-to-music run: the first keeps the duration, the second loses the song; the extend lane above keeps the slices the user chose.
- Putting `dry_run` or `wait` inside `parameters`: they are `model_run`'s own arguments, so a stray `dry_run` still charges and a stray `wait` blocks up to 180s.
