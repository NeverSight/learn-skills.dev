---
name: scenario-elevenlabs
description: "Use when generating or transforming audio with ElevenLabs models on Scenario via MCP: text-to-speech with inline emotion tags, music from a prompt or sectioned songs, sound effects and loops, dubbing audio or video into another language, re-voicing a recording with a preset or cloned voice, or isolating speech from noise. Keywords: ElevenLabs, Eleven v3, Multilingual v2, Turbo 2.5, Music v2, Sound Effects 2, Dubbing, Voice Changer, Speech to Speech, Voice Isolator, TTS, SFX, localization."
license: MIT
---

# Scenario ElevenLabs Audio

## Overview

ElevenLabs covers five audio lanes on Scenario: speech, music, sound effects, dubbing, and voice transforms. Eleven members ship side by side at authoring time, one job each: the deciding move is picking the right member, not coaxing one model into a mode. Discover them with `search` and treat `model_schema_get` as the contract: the members agree on almost nothing.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic audio work: the `scenario-audio` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Job                        | Member                          | Deciding inputs                                  |
| -------------------------- | ------------------------------- | ------------------------------------------------ |
| Expressive speech, dialog  | Eleven v3                       | `text` with inline tags                          |
| Narration, pinned language | Multilingual 2                  | `languageCode`                                   |
| Fast or bulk speech        | Turbo 2.5                       | same shape, lower cost                           |
| Music from one prompt      | Music v2                        | `prompt`, `durationSeconds`, `forceInstrumental` |
| Structured song            | Music Advanced v2               | required `sections` array                        |
| SFX and loops              | Sound Effects 2                 | `text`, `promptInfluence`, `loop`                |
| Localize, protect names    | Dubbing v2                      | `file`, `targetLang`, `keyterms`                 |
| Localize, speaker control  | Dubbing                         | `numSpeakers`, `dropBackgroundAudio`             |
| Re-voice a recording       | Speech to Speech, Voice Changer | `audio` (up to 5 min) plus a voice               |
| Clean a noisy voice        | Voice Isolator                  | `audio`                                          |

The speaking members share one voice contract: `voiceId` takes a cloned ElevenLabs voice and always wins; `publicVoice` picks a preset (21 at authoring time) and is ignored beside it; neither set means the Adam preset. Voice Changer is Speech to Speech plus delivery dials (`stability`, `similarityBoost`, `styleExaggeration`, `useSpeakerBoost`). WAV output exists on the TTS members alone; `outputFormat` elsewhere is MP3 or Opus, absent on Dubbing and Voice Isolator. `seed` gives repeatability, except on Sound Effects 2, both Dubbing members, and Voice Isolator. Cost rides the content: `text` on TTS (40,000 characters at authoring time), `durationSeconds` on Music v2, `sections` on Advanced, `file` or `audio` on the dubbing and voice members, so `dry_run` long jobs and member comparisons.

## Speech: tags on v3, dials elsewhere

Eleven v3 reads inline audio tags in the text, [whispers], [excited], [sighs], to steer delivery moment to moment across 70+ languages, and carries multi-speaker dialogue. Multilingual 2 and Turbo 2.5 do not read tags: direction there lives in `stability`, `styleExaggeration`, and `speed` (0.7 to 1.2), and `languageCode` (ISO 639-1) pins the language, a field v3 lacks. Turbo trades expressiveness for cost, roughly half the other two per run at authoring time.

## Music: one prompt or thirty sections

Music v2 takes one `prompt` (mood, genre, instruments, tempo), `durationSeconds` (3 to 600 at authoring time, cost impact), and `forceInstrumental` to suppress vocals: asking in prose is unreliable. Music Advanced v2 requires `sections`, up to 30 ordered segments at authoring time, each with `text`, its own `durationSeconds` (3 to 120), `positiveStyles` and `negativeStyles` (up to 10 each), and `contextAdherence` (high binds a segment to its neighbors, low frees it). Section grammar: square brackets label ([Verse], [Chorus]), curly braces direct ({soft piano intro}), and plain text is sung as lyrics. Advanced has no instrumental flag, so any plain text will be sung. Neither music member takes `numOutputs`: one run is one composition, and sung lyrics land differently on every draw, so a batch of takes is several parallel runs with distinct `seed` values, each priced alone on its duration, which costs what a batch field would have and returns separate files with real boundaries. Two `[Verse]` blocks in one run to get two takes returns one file with no split point.

## Dubbing replaces the track, not the lips

Both Dubbing members take an audio or video `file` with a required `targetLang`, and the output follows the input kind: video in, dubbed video out. Neither re-animates lips. Source auto-detection is spelled differently: `sourceLang: "auto"` on v2, an empty string on the older member. Pick v2 for `keyterms` (names, brands, and jargon preserved verbatim through translation); pick the older Dubbing for `numSpeakers` (0 auto-detects, up to 10), `dropBackgroundAudio`, `disableVoiceCloning`, and `highestResolution` video. Their prices differ several-fold, so `dry_run` both when either fits. Speech to Speech, Voice Changer and Voice Isolator, by contrast, take `audio` only, whatever the catalog blurb says: for a clip, pull the track with `model_scenario-audio-extract`, run the member, then lay the result over the clip in `model_scenario-compose-video`, the clip as a video layer with `mute: true` (fixed ids: each is Scenario's single deterministic tool for its operation, so discovery would only re-derive it). The same compositor lays a Music v2 bed under a video; layer contract in `scenario-video-assembly`.

## Worked example: dub a trailer into Spanish

1. `search` with `target="models"`, `query="elevenlabs dubbing"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_elevenlabs-dubbing-v2` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: fields and defaults before anything else.
3. `upload_asset` the trailer video (see the `scenario` skill) to get an asset id.
4. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"file": "asset_x", "targetLang": "es", "keyterms": ["Aetherfall", "Kestrel Squad"]}`. The file drives the price: re-estimate per input.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the result (a video, because the input was) and confirm the keyterms survived; `asset_download` with no `format` to save it.

## Common mistakes

- Setting `publicVoice` next to `voiceId` and expecting it to apply: a set `voiceId` always wins.
- Inline tags on Multilingual 2 or Turbo 2.5: that grammar is Eleven v3's; elsewhere a tag can be read aloud.
- Writing "instrumental" in a Music v2 prompt instead of setting `forceInstrumental`; on Music Advanced there is no flag and plain section text is always sung.
- Expecting lip-sync from Dubbing: the track changes, the picture does not.
- Reaching for `numOutputs` on the music members, or repeating one long run hoping for a different take without changing `seed`: same seed and settings reproduce the same music.
- Carrying one member's caps to another: 40,000 characters, 600 seconds, 30 sections, and 5 minutes of input audio are each true of one lane and false of the next.
