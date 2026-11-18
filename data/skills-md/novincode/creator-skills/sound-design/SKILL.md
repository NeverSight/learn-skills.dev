---
name: sound-design
description: Plans sound for content, covering music cues, sound effects, silence, mix levels, loudness and sonic branding, and writes prompts for AI music and SFX generators. Use when the user needs music for a video, SFX, a sound design pass, a mix plan, loudness targets, a channel's sonic identity, prompts for ElevenLabs sound effects or music, Suno, Udio or similar, or says the audio feels flat, cheesy, too loud or distracting.
license: MIT
metadata:
  version: "0.1.0"
  status: alpha
  category: production
  pack: creator-skills
---

# Sound Design

Audiences forgive bad video faster than bad audio [C]. Sound sets the emotion before the viewer has decided what they think. Your job: the voice is always clear, music supports without steering, and every effect has a reason.

## The floor

1. **Voice first.** Nothing competes with the words. Music ducks under VO; effects never mask a key line.
2. **Silence is a sound.** Dropping music out before a reveal is one of the strongest tools there is. Use it at turns.
3. **Every SFX has a job:** emphasis, realism, transition, joke, or rhythm. Whooshes on every cut become noise.
4. **Music changes when the story changes.** New section, new energy, or a cut-out. Wallpaper music for 10 minutes flattens everything.
5. **Match tempo to pace.** Fast cuts, faster music. A sad beat on a 140 bpm bed fights itself.
6. **Mix to a loudness target.** Platforms normalize loudness; mixing hotter just gets turned down, with your dynamics squashed.
7. **Clear the rights.** Library, licensed, or generated with a plan that grants commercial use. Check the terms of the current plan for AI-generated music.
8. **Lock the sonic identity in the bible:** music style, recurring stings, SFX palette, loudness, voice settings.

## Cue sheet procedure

1. Read the script's `MUSIC:` and `SFX:` lines and the storyboard's sound column.
2. Map the emotional line of the piece (from the beat sheet or color script).
3. Place music cues: in, change, drop, out. Mark silence at turns.
4. Place SFX only where they do a job. For each, write why.
5. Set levels and loudness (below).
6. Write generation prompts if using AI tools.

## Levels and loudness [C; check platform docs for current targets]

| Element | Typical level |
|---|---|
| Dialogue / VO | The anchor; peaks around −6 to −3 dBFS before mastering |
| Music under VO | Roughly 15–25 dB below the voice, ducked |
| Music without VO | Up to near the voice level |
| SFX | Felt, not dominant, except on deliberate hits |

Integrated loudness targets often used [C]: around −14 LUFS for YouTube and most social platforms; around −16 LUFS for podcasts. Check true peak ≤ −1 dBTP.

## Prompting AI music

Anatomy: genre + subgenre + era + instrumentation + tempo (bpm) + mood + structure + production texture + vocals (or "instrumental").

```
Instrumental. Dark ragtime piano and upright bass, 1910s feel, recorded on an old
upright with tape hiss. 92 bpm. Starts playful, turns ominous at 0:20 with low strings.
Ends on a single sustained low note. No vocals.
```

Avoid naming living artists; describe the sound instead. Generate several, cut the best section to picture.

## Prompting AI sound effects

Anatomy: source + action + material + space/acoustics + perspective + duration.

```
Steel rivets bursting out of a large metal tank, three fast sharp cracks like gunfire,
outdoors on a city street, close perspective, 2 seconds.
```

```
Thick liquid flooding a cobblestone street, heavy and slow, wooden debris cracking,
distant shouts, wide perspective, 6 seconds.
```

Generate short, specific effects and layer them; one long "disaster sound" prompt rarely works.

## Output: cue sheet

```markdown
## Cue sheet: <title>
Sonic identity: <from bible>    Loudness: −14 LUFS integrated, −1 dBTP

| Time | Type | Cue | Job | Level / notes |
|---|---|---|---|---|
| 0:00 | MUSIC in | dark ragtime bed | era + irony | −20 dB under VO |
| 0:28 | SFX | rivet pops ×3 | turn, tension | sharp, close |
| 0:30 | MUSIC out | hard cut to silence | the reveal | 1.5 s silence |
```
