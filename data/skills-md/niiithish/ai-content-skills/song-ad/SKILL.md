---
name: song-ad
description: Make an AI singing ad, a video sales letter that is sung like a song over 3D feature-animation. It covers the sub-avatar and hook, the song script (real lyrics with rhyme, meter, a refrain that returns and flips, backing answers and a section-by-section music direction, never plain voiceover), the song generated first in Suno (ElevenLabs Music only when asked) as the timing source, a plan timed to the sung lyrics, lip-sync shots cut from gapless song slices, and silent B-roll on the animated pipeline. Use when the user wants a song ad, singing ad, sung VSL, music-video ad, musical ad or jingle, lyrics for an ad, or to remake a winning song ad (Resilia, Rise style) for a new product. Not for spoken voiceover ads (video-plan).
disable-model-invocation: true
---

# Song Ad

A song ad is a sales letter that is sung. One character sings the worst chapter of their life in the first person, a mentor reframes the problem, the product enters around the middle, and the hard pitch takes the last 10–15%. The winners run from 1 to 10 minutes. They cost more attention than a normal ad, and they hold the right buyer.

The song is the spine. Every shot is timed to the generated song's real timestamps, and the song is never cut.

Files, loaded when a stage needs them:

| File | Load it for |
|---|---|
| [references/story-structure.md](references/story-structure.md) | Stage 1: length tiers, hook archetypes, the beat map with percentages, where the selling goes, how far to push |
| [references/song-craft.md](references/song-craft.md) | Stages 1–2: lyric rules, music direction (measured on the references), genre map, ElevenLabs and Suno, checking a take |
| [references/example-mysa.md](references/example-mysa.md) | Stage 1: a full song script at the quality bar |
| [references/gemini-audio-decode.md](references/gemini-audio-decode.md) | Stage 2, ElevenLabs only: the prompt that has Gemini decode a reference ad's sound into an ElevenLabs prompt |
| `scripts/song.py` | `lyrics` checks a sheet and writes the plan's script; `slice` cuts gapless song slices for lip-sync shots |

`<skill-dir>` is the folder holding this file. Run every command yourself.

## Stage 1: the song script

1. **Product truth.** Read the product page: the mechanism, the ingredients and doses, the offer (price, bundles, guarantee), who it's for and who it isn't. Note which claims the page makes, in its own words.
2. **Sub-avatar and tier.** Write the sub-avatar card, choose the length tier and the genre that fits them, and state all three in one line. Ask only if the brief contradicts itself.
3. **Hooks.** Write three from different archetypes, pick one, and keep the other two as A/B variants. Push the drama (betrayal, revenge, a family secret); keep the claims soft.
4. **Write the song** against the beat map, following every lyric rule in `song-craft.md`. It is a song, not prose: rhymed lines of 4–10 words, one refrain that returns and flips, backing answers, and spoken lines only where they hit hardest.
5. **Music direction.** Global style, an energy line, and a section table (section, length, key, energy, style tags). Keep one tempo throughout; use the key lift at the product, the drum drop at the mentor and the peak at the climax.
6. **Check the sheet:** `python3 <skill-dir>/scripts/song.py lyrics <sheet.md>` gives the word count and length estimate and flags lines that are too long or too short. Fix the flags.
7. **Deliver** the script file (in the project, e.g. `video-N/song/lyrics-v1.md`) with the sub-avatar, lyrics, music direction, beat timings, alternative hooks and a claims and compliance list. In chat, a few lines: the hook, the length, the genre, what to decide.
8. **Gate:** the user approves the lyrics. A rewrite starts from the story and the beat map, not line patches. "Not controversial enough" means a sharper betrayal and a worse twist, not ruder words.

## Stage 2: the song

Follow "Generating the song" in `song-craft.md`. **Suno (a paid plan) is the default**: the user preferred it over ElevenLabs Music on a real job. Follow the method as written; don't improvise on it.

1. Write the Suno paste (Create → Advanced): the **Style** field from the style template, and the **Lyrics** field with the lyrics word for word under plain section tags, the brand name on its own line. Save both in `video-N/song/suno/` (`style.txt`, `lyrics.txt`).
2. The user generates and listens all the way through. You can't hear it, so never judge the taste. Before any visuals, they confirm every lyric is sung as written, the brand name is clear on a phone speaker, vocals start at once, and the length and tone fit.
3. A failed take: fix only that piece. A mispronounced brand name is respelled (hyphens, the stressed syllable in capitals) and only its section is regenerated.
4. Put the chosen take at `video-N/voiceover/recording.wav`, then write the plan's script from the sheet:

   ```bash
   python3 <skill-dir>/scripts/song.py lyrics video-N/song/lyrics-v1.md --video video-N
   ```

5. Time it with `video-plan`: `plan.py voiceover video-N` finds each sung line in the take with Parakeet (the `transcribe` skill). A line it can't find was probably dropped or mangled by the singer: tell the user which ones to listen to. If many are missing, set `WHISPER_MODEL=medium.en` in `project.conf`, or use the vocal stem the music tool exports.

## Stage 3: plan

Plan with `video-plan`, with the song in place of the voiceover. Its Music row reads: the song is the audio track, never cut. What changes for a song:

- **Every second of the song has picture,** instrumental breaks and the tail included. There is no dead air to remove.
- **Mark the sung shots** in the Voiceover column as **SUNG**. The hero lip-syncs on camera for about 30–40% of the runtime: the hook, each refrain, the climax line and the tag. The rest is silent B-roll that shows what the line says at that moment, with something new every 2–4 s. An ad of only singing faces is dead by verse 2.
- **Lines in the story are scenes in the picture.** The overheard door, the cake photo, the chemo chair, the bottle slid across the table, week by week, the terrace. Name each place, and keep the cast small enough to lock: the hero (a before and an after look), the betrayer, the mentor, the partner, plus the product sheet.
- **Sheets:** the shared layouts in `video-production/references/sheets/` with `animated-video-production`'s `characters.md`, `places.md` and `product.md`. A product mascot with a face is optional.
- **End card:** the last 2–5 s of instrumental tail get a hypermotion product shot. The user adds the headline in the edit.

## Stage 4: make

1. **B-roll:** `animated-video-production` on `video-production`, as usual: sheets, stills, 360p drafts, finals. B-roll clips are silent picture under the song.
2. **Sung shots: stills first, then lip-sync outside Flow.** Flow can't take an audio track, so it can't sync a mouth to the song. Make each sung shot's still in the normal stills batch, then cut its slice:

   ```bash
   python3 <skill-dir>/scripts/song.py slice video-N 1-2 14 38-39
   ```

   The slices land in `voiceover/slices/`, listed with their times in `slices.md`. Consecutive slices share their cut points, so they play back to back with no gap. `--all` slices the whole song into batches of up to 10 s, for a video made entirely with an audio-driven model.
3. **Hand the user each sung shot:** the approved still, the character sheet and the slice, for an audio-driven lip-sync model (MiniMax H3 Max, about $0.80 per 10 s; Seedance 2.0; or a generated clip lip-synced after with Sync Labs, HeyGen or Dzine). One clip per slice, one take unless they ask. A slice over 10 s is split at a line break first.

## Edit and captions

The user edits: the full song on the bottom track, uncut, every clip muted above it. Never use the audio a video model outputs. After the edit, add captions with `captions-filmcraft` when asked. Never run `filmcraft-pacing` tighten on a song ad: the song is the timing. For a song, the wording is the lyric sheet's lead lines. The references show one lyric line per caption; one line per caption is fine.

## Rules

- **The song is the source of truth.** Nothing is storyboarded against a guessed length. The song is never trimmed, sped up or cut, except for the head before the first word.
- **Never write plain voiceover and call it a song.** No rhyme, no meter and no return means it isn't done.
- **Insults come from other characters.** Claims stay in the product page's words and hedged ("may", "support", "around week three").
- **No text, captions or music in generated stills or clips.**
