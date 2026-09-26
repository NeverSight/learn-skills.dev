---
name: scenario-minimax-music
description: "Use when generating music with MiniMax models on Scenario via MCP: full songs with vocals from a lyric sheet, structure tags like [Verse] and [Chorus], auto-written lyrics from a plain-language brief, instrumental tracks from a style prompt, or covering an uploaded MP3 or WAV in a new genre while keeping the melody. Keywords: MiniMax Music 3.0, Music Cover, Hailuo, text-to-music, audio-to-audio, song generation, lyrics, vocals, instrumental, BPM, genre swap."
license: MIT
---

# Scenario MiniMax Music

## Overview

MiniMax's music family on Scenario splits in two: Music 3.0 composes and performs a complete song from a style prompt plus a lyric sheet, and Music Cover rebuilds an uploaded song in a new style while keeping its melody. Discover both with `search` and treat `model_schema_get` as the contract: the members share `prompt`, `sampleRate`, and `bitrate` and agree on nothing else.

Connection and the core loop: see the `scenario` skill; model-agnostic audio work: the `scenario-audio` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Four modes across two members (names from the live schema):

| Mode         | Member    | Inputs                                                 | Behavior                                     |
| ------------ | --------- | ------------------------------------------------------ | -------------------------------------------- |
| Vocal song   | Music 3.0 | `prompt` + `lyrics`                                    | sings your words; tags shape the arrangement |
| Auto lyrics  | Music 3.0 | `prompt` + brief in `lyrics` + `lyricsOptimizer: true` | writes the structured sheet for you          |
| Instrumental | Music 3.0 | `prompt` + `isInstrumental: true`                      | no lyrics; the prompt is the whole brief     |
| Cover        | Cover     | `audioUrl` + `prompt`                                  | keeps the melody, restyles everything else   |

`prompt` is required on both members (10 to 2,000 characters at authoring time) and carries style only: genre, mood, tempo in BPM, key, vocal timbre, instrumentation. The words go in `lyrics` (up to 3,500 characters), which also sets the bill: about 700 characters per billable minute at authoring time, one to five minutes. Jobs run minutes, so launch with `wait=false`.

## Writing the lyric sheet

The lyric sheet is an arrangement script, not plain text. Structure tags go on their own line in square brackets ([Intro], [Verse], [Pre Chorus], [Chorus], [Hook], [Drop], [Bridge], [Inst], [Outro]; the schema lists more). Newlines separate lines, a blank line between sections reads as a pause, and two to four lines per section sing better than a dense paragraph. Parentheses carry performance cues rather than sung words: (whispered), (belted), or a short direction inside an [Inst] or [Solo] passage. Close with [Outro] so the track resolves instead of cutting off. English and Mandarin sing the most consistently at authoring time.

With `lyricsOptimizer: true` the lyrics field flips meaning: pass a plain-language brief ("indie folk breakup song, walking alone at night") and the model writes the structured sheet itself. With it off, it sings whatever the field holds, briefs included.

## Covers keep the melody

Music Cover takes its source through `audioUrl`: `upload_asset` the MP3 or WAV first (see the `scenario` skill) and pass the asset id. It keeps the melodic line and regenerates the rest from the prompt (genre, vocal character, instruments, production), so it fits genre swaps, not remixes that change the tune. It works best on sources with clear vocals and melody, and there is no lyrics field, so the prompt changes the style, never the words. Its cost sat flat per run at authoring time while 3.0 scales with the sheet, so `dry_run` both when choosing.

## Worked example: a trailer song with vocals

1. `search` with `target="models"`, `query="minimax music"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_minimax-music-3-0` (a live hit at authoring time: re-discover each session); the cover member lists `audio2audio` in capabilities.
2. `model_schema_get` with that id: fields, caps, and defaults before anything else.
3. `model_run` with that `model_id`, `dry_run=true`, and the exact `parameters={"prompt": "epic orchestral trailer, 140 BPM, D minor, female vocals, taiko and strings", "lyrics": "[Intro]\n(Low strings)\n\n[Verse]\nWe were born below the thunder\n...\n\n[Outro]\n(Choir fades)"}`. Re-estimate after lyric edits: character count moves the price.
4. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
5. `asset_display` the output and listen before laying it under a cut.

## Common mistakes

- Lyrics in `prompt` or genre words in `lyrics`: the model then describes a song, or sings your style brief.
- Asking for "no vocals" in the prompt: unreliable; set `isInstrumental: true`.
- Passing finished lyrics with `lyricsOptimizer: true`: they get rewritten; the flag expects a brief.
- Faking instrumental passages with filler words: use [Inst] or [Solo] with a parenthetical cue.
- Sending a local path or external URL as `audioUrl`: upload first, pass the asset id.
- Covering a track with no clear melody: the cover keeps only what it can hear.
