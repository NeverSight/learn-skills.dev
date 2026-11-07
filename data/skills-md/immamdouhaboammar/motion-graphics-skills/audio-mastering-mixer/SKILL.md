---
name: audio-mastering-mixer
description: Mix and master voiceover, sound effects, and music stems to professional broadcast loudness standards. Use when adding SFX cues, balancing audio stems, mastering to minus 14 LUFS, ducking music under voice, or eliminating harsh whooshes.
---

# Audio Mastering and Foley Mixer

Enforces broadcast audio standards and disciplined sound design for code-driven motion graphics.

## The Click and Pop Philosophy

Amateur motion graphics rely on excessive swooshes, abrasive laser sounds, and continuous whooshes that fatigue the listener. Elite motion graphics use minimal, tactile foley:

1. **Subtle Tactile Events**: A tiny tick when each list item appears, a soft rolling mechanical click during number count-ups, and a quiet bell chime on the final card.
2. **The Whoosh Prohibition**: Never attach whooshes to standard card slides, fades, or simple position tweens. Reserve whooshes strictly for high-velocity full-viewport zooms or camera whip transitions.
3. **Hero Hit Isolation**: The climax hit must sit in clean acoustic space. Silence music and ambient effects for at least 60ms prior to the hero impact to maximize perceived dynamic punch.

## Broadcast Loudness Standards

Mastering specifications for mobile video distribution (Instagram Reels, TikTok, YouTube Shorts):

| Parameter | Target Standard | Tolerance | Rationale |
|---|---|---|---|
| Master Integrated Loudness | -14.0 LUFS | +/- 0.5 LUFS | Prevents platform audio normalization degradation |
| Master True Peak (dBTP) | -1.25 dBTP | Maximum -1.0 dBTP | Prevents inter-sample clipping during lossy AAC encoding |
| Voice Over Stem | -16.0 LUFS | +/- 1.0 LUFS | Maintains crisp dialogue clarity above background beds |
| Music Ducking Offset | >= 12.0 dB down | Fixed duck depth | Ensures background bed never masks voice consonants |
| Foley SFX Stem | -20.0 to -24.0 LUFS | Dynamic | Provides physical tactile texture without loudness fatigue |

## FFmpeg Automated Loudness Normalization

Normalize final renders to target LUFS using the `loudnorm` filter:

```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.25:LRA=7 -c:v copy -c:a aac -b:a 192k output.mp4
```

## Further Reading

- [references/stem-organization.md](references/stem-organization.md) for multi-track audio routing.
