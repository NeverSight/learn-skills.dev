---
name: sound
description: Sound for a film or animation, covering voiceover, music bed, sound effects, UI cues, mixing and mastering to -14 LUFS. Use when a video needs sound, a voiceover, or a silent render needs a score.
---

# Sound

You design the sound: what plays, where, how loud and from which source. The scripts mix, level and
master; the host tools generate. Provider calls (voice, music, effects, transcription) happen only
through the host tools, which hold the keys: never call a provider API, and never look for a key, in
the sandbox.

| Need | Use |
| --- | --- |
| A voiceover line | `generate_voiceover(text, voice_id, sandbox_path, ...)`: mp3 plus `<name>.words.json` word timings |
| An effect, ambience or loop | `generate_sound_effect(prompt, sandbox_path, duration_seconds=..., loop=...)` |
| A music bed | `generate_music(sandbox_path, prompt=..., length_seconds=...)` or a `composition_plan`; or a track the person supplied |
| Interface sounds, no key needed | `node /workspace/skills/sound/scripts/synth-cue.mjs <recipe> <out.wav>` (`--list`) |
| A transcript with word timings | `transcribe_audio(sandbox_path)` |
| Mix, master, mux, lint | `node /workspace/skills/sound/scripts/score.mjs <jobDir> [plan.json]` |
| Master one file | `node /workspace/skills/sound/scripts/master.mjs <in> <out> [--target -14] [--true-peak -1]` |

Generated files go under `<jobDir>/sound-assets/<music|sfx|vo>/<slug>.mp3|wav`, where the plan finds
them. Every generation spends credits; say what a pass cost.

## How a film gets scored

A starting point, not a procedure; change the order when the film asks for it.

1. **Voiceover first.** A film with voiceover is cut to the voiceover, not the music. Speak every
   line with `generate_voiceover` before anything else, passing the neighbouring lines as
   `previous_text` and `next_text`. The word timings are the anchors that cuts, captions and effects
   land on; timing locks when the animatic is approved against them.
2. **The bed.** Generate or take the supplied track, trimmed to the film. When music must hit the
   acts exactly, use a `composition_plan` with section lengths. Never name an artist or quote lyrics.
3. **The cue sheet.** Mark every interaction and beat while you build: put `data-sfx-intent`,
   `data-sfx-start` and `data-sfx-dur` on the HyperFrames elements, then
   `node scripts/extract-edl.mjs <index.html>` writes the cue list. For a film rendered elsewhere,
   watch it frame by frame (`film-breakdown/scripts/grab.mjs`) and mark each moment.
4. **The effects.** Synth cues for small interface sounds (ticks, confirms, arrivals, swipes); they
   are one family, so repeated actions sound like one instrument. Generate anything bigger or more
   specific (a signature sting, an exact-length riser, an ambience), and reuse one sound across
   repeated actions. Generated effects can come back mis-shaped (a riser that fades before its cut,
   a sting with no tail): listen to each before placing it.
5. **Mix, master, lint.** Write `<jobDir>/plan.json`, run `score.mjs`. It resolves every file,
   levels each voice line to -16 LUFS, keeps the bed 3 dB under the voice and ducks it about 2 dB more
   under speech, levels every cue so `gain` 1.0 peaks about 2 dB under the voice, derives bed
   automation from cue intents (a dip before a transition or flash, a duck under risers, shimmers and
   stings), masters to -14 LUFS integrated with true peak under -1 dBTP, muxes onto the silent render,
   then runs `audio-lint`. A failed stage stops the run.
6. **Listen, then hand it over.** Check the scored file's duration against the picture and listen to
   the joins. The person's ear decides; offer the mix with one line on what you did.

Recipes that already render their own narrated film (`faceless-explainer`, `pr-to-video`,
`general-video`, `website-to-video`): rescoring replaces their audio, so put the narration back as
voice lines with `node scripts/vo-from-index.mjs <hyperframesDir> <jobDir> [voicePattern]`, which
copies each line and writes `vo-from-film.json` for the plan's `vo`. `music-to-video` passes its track
in as the bed (`source: "supplied"`).

## Judgment

- **The voice leads.** Effects and music support it; if a cue covers a word, lower its gain or move it.
- **Density follows the picture.** Sound on the interactions and beats the eye follows, bigger hits on
  the reveals, silence where the picture rests. A cue on every frame is noise.
- **Pace comes from the words.** Write the delivery into the text (bracketed audio tags, ellipses,
  one capitalised word) rather than relying on a speed setting; the tool reports syllables per second
  so you can check. Voice direction and the plan schema: [references/voice-and-plan.md](references/voice-and-plan.md).
- **Masters are measured, not assumed.** `master.mjs` prints the input and the result; the delivery
  target is -14 LUFS integrated (±1) and at or under -1 dBTP. Exit 1 means it wrote a file that misses
  the target; exit 2 means it could not run.
- **Licensing.** Generated audio follows the provider plan behind the host's key (commercial use
  usually needs a paid plan). Supplied music must be the person's to use; ask when it is not clear.
